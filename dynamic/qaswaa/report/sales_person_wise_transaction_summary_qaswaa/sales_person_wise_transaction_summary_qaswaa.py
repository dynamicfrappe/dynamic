# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint

from erpnext import get_company_currency


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns(filters)
	entries = get_entries(filters)
	item_details = get_item_details()
	data = []

	company_currency = get_company_currency(filters.get("company"))

	for d in entries:
		reserved_qty = 0
		sql = f'''
				SELECT 
					reserved_qty , actual_qty
				FROM
					`tabBin`
				WHERE
					warehouse = '{d.warehouse}'
					AND
					item_code = '{d.item_code}'
				'''
		reserved_qty = frappe.db.sql(sql , as_dict = 1)
		if d.stock_qty > 0 or filters.get("show_return_entries", 0):
			data.append(
				[
					d.name,
					d.customer,
					d.territory,
					d.item_name,
					d.item_group ,
					d.stock_qty,
					reserved_qty[0]["reserved_qty"] ,
					reserved_qty[0]["actual_qty"] ,

					d.base_net_amount,
					d.sales_person,
					d.warehouse
					
					# item_details.get(d.item_code, {}).get("item_group"),
					# item_details.get(d.item_code, {}).get("brand"),
				]
			)

	if data:
		total_row = [""] * len(data[0])
		data.append(total_row)

	return columns, data


def get_columns(filters):
	if not filters.get("doc_type"):
		msgprint(_("Please select the document type first"), raise_exception=1)

	columns = [
		{
			"label": _(filters["doc_type"]),
			"options": filters["doc_type"],
			"fieldname": frappe.scrub(filters["doc_type"]),
			"fieldtype": "Link",
			"width": 140,
		},
		{
			"label": _("Full Name"),
			"options": "Customer",
			"fieldname": "customer",
			"fieldtype": "Link",
			"width": 140,
		},
		{
			"label": _("Territory"),
			"options": "Territory",
			"fieldname": "territory",
			"fieldtype": "Link",
			"width": 140,
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 140,
		},
				{
			"label": _("Item"),
			"options": "Item",
			"fieldname": "item_code",
			"fieldtype": "Link",
			"width": 140,
		},
		{"label": _("Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 140},
		{"label": _("Reserved qty"), "fieldname": "reserved_qty", "fieldtype": "Float", "width": 140},
		{"label": _("Actual Qty In Warehouse"), "fieldname": "actual_qty", "fieldtype": "Float", "width": 140},


		{
			"label": _("Amount"),
			"options": "currency",
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Sales Person"),
			"options": "Sales Person",
			"fieldname": "sales_person",
			"fieldtype": "Link",
			"width": 140,
		},
		{
			"label": _("Warehouse"),
			"options": "Warehouse",
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"width": 140,
		},
		# {"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 140},
		# {
		# 	"label": _("Brand"),
		# 	"options": "Brand",
		# 	"fieldname": "brand",
		# 	"fieldtype": "Link",
		# 	"width": 140,
		# },
		
		# {"label": _("Contribution %"), "fieldname": "contribution", "fieldtype": "Float", "width": 140},
		# {
		# 	"label": _("Contribution Amount"),
		# 	"options": "currency",
		# 	"fieldname": "contribution_amt",
		# 	"fieldtype": "Currency",
		# 	"width": 140,
		# },
		# {
		# 	"label": _("Currency"),
		# 	"options": "Currency",
		# 	"fieldname": "currency",
		# 	"fieldtype": "Link",
		# 	"hidden": 1,
		# },
	]

	return columns


def get_entries(filters):
	date_field = filters["doc_type"] == "Sales Order" and "transaction_date" or "posting_date"
	if filters["doc_type"] == "Sales Order":
		qty_field = "delivered_qty"
	else:
		qty_field = "qty"
	conditions, values = get_conditions(filters, date_field)

	entries = frappe.db.sql(
		"""
		SELECT
			dt.name, dt.customer, dt.territory, dt.%s as posting_date, dt_item.item_code , dt_item.item_group 
			,st.sales_person, st.allocated_percentage, dt_item.warehouse,`tabItem`.item_name,
		CASE
			WHEN dt.status = "Closed" THEN dt_item.%s * dt_item.conversion_factor
			ELSE dt_item.stock_qty
		END as stock_qty,
		CASE
			WHEN dt.status = "Closed" THEN (dt_item.base_net_rate * dt_item.%s * dt_item.conversion_factor)
			ELSE dt_item.base_net_amount
		END as base_net_amount,
		CASE
			WHEN dt.status = "Closed" THEN ((dt_item.base_net_rate * dt_item.%s * dt_item.conversion_factor) * st.allocated_percentage/100)
			ELSE dt_item.base_net_amount * st.allocated_percentage/100
		END as contribution_amt
		FROM
			`tab%s` dt, `tab%s Item` dt_item, `tabSales Team` st,`tabItem`
		WHERE
			st.parent = dt.name and dt.name = dt_item.parent and st.parenttype = %s
			and dt.docstatus = 1 %s AND dt_item.item_code = `tabItem`.item_code order by st.sales_person, dt.name desc
			
		"""
		% (
			date_field,
			qty_field,
			qty_field,
			qty_field,
			filters["doc_type"],
			filters["doc_type"],
			"%s",
			conditions,
		),
		tuple([filters["doc_type"]] + values),
		as_dict=1,
	)
	# frappe.throw(str(entries))
	return entries


def get_conditions(filters, date_field):
	conditions = [""]
	values = []

	for field in ["company", "customer", "territory"]:
		if filters.get(field):
			conditions.append("dt.{0}=%s".format(field))
			values.append(filters[field])

	if filters.get("sales_person"):
		lft, rgt = frappe.get_value("Sales Person", filters.get("sales_person"), ["lft", "rgt"])
		conditions.append(
			"exists(select name from `tabSales Person` where lft >= {0} and rgt <= {1} and name=st.sales_person)".format(
				lft, rgt
			)
		)

	if filters.get("from_date"):
		conditions.append("dt.{0}>=%s".format(date_field))
		values.append(filters["from_date"])

	if filters.get("to_date"):
		conditions.append("dt.{0}<=%s".format(date_field))
		values.append(filters["to_date"])

	items = get_items(filters)
	if items:
		conditions.append("dt_item.item_code in (%s)" % ", ".join(["%s"] * len(items)))
		values += items

	return " and ".join(conditions), values


def get_items(filters):
	if filters.get("item_group"):
		key = "item_group"
	elif filters.get("brand"):
		key = "brand"
	else:
		key = ""

	items = []
	if key:
		items = frappe.db.sql_list(
			"""select name from tabItem where %s = %s""" % (key, "%s"), (filters[key])
		)

	return items


def get_item_details():
	item_details = {}
	for d in frappe.db.sql("""SELECT `name`, `item_group`, `brand` FROM `tabItem`""", as_dict=1):
		item_details.setdefault(d.name, d)

	return item_details
