# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
import erpnext
# from dynamic.gebco.doctype.stock_ledger import get_valuation_rate
from frappe import _

DOMAINS = frappe.get_active_domains() 


# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import copy
from collections import OrderedDict

import frappe
from frappe import _, qb
from frappe.query_builder import CustomFunction
from frappe.query_builder.functions import Max
from frappe.utils import date_diff, flt, getdate


def execute(filters=None):
	if not filters:
		return [], [], None, []

	validate_filters(filters)

	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)
	so_elapsed_time = get_so_elapsed_time(data)

	if not data:
		return [], [], None, []

	data, chart_data = prepare_data(data, so_elapsed_time, filters)

	return columns, data, None, None


def validate_filters(filters):
	from_date, to_date = filters.get("from_date"), filters.get("to_date")

	if not from_date and to_date:
		frappe.throw(_("From and To Dates are required."))
	elif date_diff(to_date, from_date) < 0:
		frappe.throw(_("To Date cannot be before From Date."))


def get_conditions(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " and so.transaction_date between %(from_date)s and %(to_date)s"

	if filters.get("company"):
		conditions += " and so.company = %(company)s"

	if filters.get("sales_order"):
		conditions += " and so.name in %(sales_order)s"

	if filters.get("status"):
		conditions += " and so.status in %(status)s"
	
	if filters.get("customer"):
		conditions += " and so.customer = '%s' " %(filters.get("customer"))
	print(f'\n\n\n==>{conditions} \n\n')
	return conditions


def get_data(conditions, filters):
	# nosemgrep
	data = frappe.db.sql(
		"""
		SELECT
			so.transaction_date as date,
			soi.delivery_date as delivery_date,
			so.name as sales_order,
			so.status, so.customer,
			soi.item_code,soi.warehouse,
			DATEDIFF(CURDATE(), soi.delivery_date) as delay_days,
			IF(so.status in ('Completed','To Bill'), 0, (SELECT delay_days)) as delay,
			soi.qty, soi.delivered_qty,
			(soi.qty - soi.delivered_qty) AS pending_qty,
			IFNULL(SUM(sii.qty), 0) as billed_qty,
			soi.base_amount as amount,
			(soi.delivered_qty * soi.base_rate) as delivered_qty_amount,
			(soi.billed_amt * IFNULL(so.conversion_rate, 1)) as billed_amount,
			(soi.base_amount - (soi.billed_amt * IFNULL(so.conversion_rate, 1))) as pending_amount,
			soi.warehouse as warehouse,
			so.company, soi.name,
			soi.description as description,
			soi.parenttype ,
			soi.parent
		FROM
			`tabSales Order` so,
			`tabSales Order Item` soi
		LEFT JOIN `tabSales Invoice Item` sii
			ON sii.so_detail = soi.name and sii.docstatus = 1
		WHERE
			soi.parent = so.name
			and so.status not in ('Stopped', 'Closed', 'On Hold')
			and so.docstatus = 1
			{conditions}
		GROUP BY soi.name 
		ORDER BY so.transaction_date ASC, soi.item_code ASC
	""".format(
			conditions=conditions
		),
		filters,
		as_dict=1,
	)

	return data


def get_so_elapsed_time(data):
	"""
	query SO's elapsed time till latest delivery note
	"""
	so_elapsed_time = OrderedDict()
	if data:
		sales_orders = [x.sales_order for x in data]

		so = qb.DocType("Sales Order")
		soi = qb.DocType("Sales Order Item")
		dn = qb.DocType("Delivery Note")
		dni = qb.DocType("Delivery Note Item")

		to_seconds = CustomFunction("TO_SECONDS", ["date"])

		query = (
			qb.from_(so)
			.inner_join(soi)
			.on(soi.parent == so.name)
			.left_join(dni)
			.on(dni.so_detail == soi.name)
			.left_join(dn)
			.on(dni.parent == dn.name)
			.select(
				so.name.as_("sales_order"),
				soi.item_code.as_("so_item_code"),
				(to_seconds(Max(dn.posting_date)) - to_seconds(so.transaction_date)).as_("elapsed_seconds"),
			)
			.where((so.name.isin(sales_orders)) & (dn.docstatus == 1))
			.orderby(so.name, soi.name)
			.groupby(soi.name)
		)
		dn_elapsed_time = query.run(as_dict=True)

		for e in dn_elapsed_time:
			key = (e.sales_order, e.so_item_code)
			so_elapsed_time[key] = e.elapsed_seconds

	return so_elapsed_time


def prepare_data(data, so_elapsed_time, filters):
	completed, pending = 0, 0

	if filters.get("group_by_so"):
		sales_order_map = {}

	for row in data:
		# sum data for chart
		completed += row["billed_amount"]
		pending += row["pending_amount"]
		row['valuation_rate'] = check_item_valuation_rate(row)
		row['profit'] = row['amount'] - (row['valuation_rate'] * row.get('qty'))
		# prepare data for report view
		row["qty_to_bill"] = flt(row["qty"]) - flt(row["billed_qty"])

		row["delay"] = 0 if row["delay"] and row["delay"] < 0 else row["delay"]

		row["time_taken_to_deliver"] = (
			so_elapsed_time.get((row.sales_order, row.item_code))
			if row["status"] in ("To Bill", "Completed")
			else 0
		)

		if filters.get("group_by_so"):
			so_name = row["sales_order"]

			if not so_name in sales_order_map:
				# create an entry
				row_copy = copy.deepcopy(row)
				sales_order_map[so_name] = row_copy
			else:
				# update existing entry
				so_row = sales_order_map[so_name]
				so_row["required_date"] = max(getdate(so_row["delivery_date"]), getdate(row["delivery_date"]))
				so_row["delay"] = min(so_row["delay"], row["delay"])

				# sum numeric columns
				fields = [
					"qty",
					"delivered_qty",
					"pending_qty",
					"billed_qty",
					"qty_to_bill",
					"amount",
					"delivered_qty_amount",
					"billed_amount",
					"pending_amount",
				]
				for field in fields:
					so_row[field] = flt(row[field]) + flt(so_row[field])

	# chart_data = prepare_chart_data(pending, completed)

	if filters.get("group_by_so"):
		data = []
		for so in sales_order_map:
			data.append(sales_order_map[so])
		return data, None

	return data, None

# def prepare_chart_data(pending, completed):
# 	labels = ["Amount to Bill", "Billed Amount"]

# 	return {
# 		"data": {"labels": labels, "datasets": [{"values": [pending, completed]}]},
# 		"type": "donut",
# 		"height": 300,
# 	}


def get_columns(filters):
	columns = [
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 90},
		{
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 160,
		},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 130},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 130,
		},
	]

	if not filters.get("group_by_so"):
		columns.append(
			{
				"label": _("Item Code"),
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options": "Item",
				"width": 100,
			}
		)
		columns.append(
			{"label": _("Description"), "fieldname": "description", "fieldtype": "Small Text", "width": 100}
		)

	columns.extend(
		[
			{
				"label": _("Qty"),
				"fieldname": "qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
			},
			{
				"label": _("Delivered Qty"),
				"fieldname": "delivered_qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
			},
			{
				"label": _("Qty to Deliver"),
				"fieldname": "pending_qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
			},
			{
				"label": _("Billed Qty"),
				"fieldname": "billed_qty",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
			{
				"label": _("Qty to Bill"),
				"fieldname": "qty_to_bill",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
			{
				"label": _("Amount"),
				"fieldname": "amount",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Valuation Rate"),
				"fieldname": "valuation_rate",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Profit"),
				"fieldname": "profit",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Billed Amount"),
				"fieldname": "billed_amount",
				"fieldtype": "Currency",
				"width": 110,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Pending Amount"),
				"fieldname": "pending_amount",
				"fieldtype": "Currency",
				"width": 130,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{
				"label": _("Amount Delivered"),
				"fieldname": "delivered_qty_amount",
				"fieldtype": "Currency",
				"width": 100,
				"options": "Company:company:default_currency",
				"convertible": "rate",
			},
			{"label": _("Delivery Date"), "fieldname": "delivery_date", "fieldtype": "Date", "width": 120},
			{"label": _("Delay (in Days)"), "fieldname": "delay", "fieldtype": "Data", "width": 100},
			{
				"label": _("Time Taken to Deliver"),
				"fieldname": "time_taken_to_deliver",
				"fieldtype": "Duration",
				"width": 100,
			},
		]
	)
	if not filters.get("group_by_so"):
		columns.append(
			{
				"label": _("Warehouse"),
				"fieldname": "warehouse",
				"fieldtype": "Link",
				"options": "Warehouse",
				"width": 100,
			}
		)
	columns.append(
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 100,
		}
	)

	return columns

def check_item_valuation_rate(row): 
	value_rate = get_valuation_rate(row.item_code,
	row.warehouse,
	row.parenttype,
	row.parent,
	allow_zero_rate=False,
	currency=erpnext.get_company_currency(row.company),
	company=row.company,
	raise_error_if_no_rate=True,
	)
	return value_rate or 0

def get_valuation_rate(
	item_code,
	warehouse,
	voucher_type,
	voucher_no,
	allow_zero_rate=False,
	currency=None,
	company=None,
	raise_error_if_no_rate=True, 
):

	if not company:
		company = frappe.get_cached_value("Warehouse", warehouse, "company")

	# Get valuation rate from last sle for the same item and warehouse
	last_valuation_rate = frappe.db.sql(
		"""select valuation_rate
		from `tabStock Ledger Entry` force index (item_warehouse)
		where
			item_code = %s
			AND warehouse = %s
			AND valuation_rate >= 0
			AND is_cancelled = 0
			AND NOT (voucher_no = %s AND voucher_type = %s)
		order by posting_date desc, posting_time desc, name desc limit 1""",
		(item_code, warehouse, voucher_no, voucher_type),
	)

	if not last_valuation_rate:
		# Get valuation rate from last sle for the item against any warehouse
		last_valuation_rate = frappe.db.sql(
			"""select valuation_rate
			from `tabStock Ledger Entry` force index (item_code)
			where
				item_code = %s
				AND valuation_rate > 0
				AND is_cancelled = 0
				AND NOT(voucher_no = %s AND voucher_type = %s)
			order by posting_date desc, posting_time desc, name desc limit 1""",
			(item_code, voucher_no, voucher_type),
		)

	if last_valuation_rate:
		return flt(last_valuation_rate[0][0])

	# If negative stock allowed, and item delivered without any incoming entry,
	# system does not found any SLE, then take valuation rate from Item
	valuation_rate = frappe.db.get_value("Item", item_code, "valuation_rate")

	if not valuation_rate:
		# try Item Standard rate
		valuation_rate = frappe.db.get_value("Item", item_code, "standard_rate")

		if not valuation_rate:
			# try in price list
			valuation_rate = frappe.db.get_value(
				"Item Price", dict(item_code=item_code, buying=1, currency=currency), "price_list_rate"
			)
	
	return valuation_rate or 0