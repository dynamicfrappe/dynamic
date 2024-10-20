# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.meta import get_field_precision
from frappe.utils import cstr, flt
from frappe.utils.xlsxutils import handle_html

from erpnext.selling.report.item_wise_sales_history.item_wise_sales_history import	get_item_details

def execute(filters=None):
	return _execute(filters)


def _execute(
	filters=None,
	additional_table_columns=None,
	additional_query_columns=None,
	additional_conditions=None,
):
	if not filters:
		filters = {}
	columns = get_columns(additional_table_columns, filters)

	company_currency = frappe.get_cached_value("Company", filters.get("company"), "default_currency")

	item_list = get_items(filters, additional_query_columns, additional_conditions)
	if item_list:
		itemised_tax, tax_columns = get_tax_accounts(item_list, columns, company_currency)

	mode_of_payments = get_mode_of_payments(set(d.parent for d in item_list))
	# so_dn_map = get_purchase_reciepts_against_purchase_order(item_list)
	# frappe.errprint(f"so_dn_map-->{so_dn_map}")
	data = []
	total_row_map = {}
	skip_total_row = 0
	prev_group_by_value = ""

	if filters.get("group_by"):
		grand_total = get_grand_total(filters, "Purchase Invoice")

	supplier_details = get_supplier_details()
	item_details = get_item_details()

	for d in item_list:
		supplier_record = supplier_details.get(d.supplier)
		item_record = item_details.get(d.item_code)

		# purchase_reciept = None
		# if d.purchase_reciept:
		# 	purchase_reciept = d.purchase_reciept
		# # elif d.po_detail:
		# # 	purchase_reciept = ", ".join(so_dn_map.get(d.po_detail, []))

		# if not purchase_reciept and d.update_stock:
		# 	purchase_reciept = d.parent
		
		# purchase_reciept_name = so_dn_map.get(d.po_detail)

		purchase_reciept_incoming_rate = 0
		# if purchase_reciept_name:
		# 	purchase_reciept_incoming_rate = so_dn_map.get(purchase_reciept_name[0])[0]
		
		row = {
			"item_code": d.item_code,
			"item_name": item_record.item_name if item_record else d.item_name,
			"item_group": item_record.item_group if item_record else d.item_group,
			"discount_amount" : d.discount_amount,
			"discount_account" : d.discount_account,
			"description": d.description,
			"invoice": d.parent,
			"status":d.status,
			"base_discount_amount": d.base_discount_amount,
			"total_discount" : d.total_discount , 
			"gross_profit" : d.gross_profit ,
			"posting_date": d.posting_date,
			"supplier": d.supplier,
			"supplier_name": supplier_record.supplier_name,
			"supplier_group": supplier_record.supplier_group,
			"incoming_rate": purchase_reciept_incoming_rate,
			"total_cost": purchase_reciept_incoming_rate * d.qty,
		}

		if additional_query_columns:
			for col in additional_query_columns:
				row.update({col: d.get(col)})
		mode_of_payment_none = any(elem is None for elem in mode_of_payments.get(d.parent, []))
		mode_of_payment = ''
		if mode_of_payment_none:
			mode_of_payment = ''
		else :
			mode_of_payment = ", ".join(mode_of_payments.get(d.parent, []))
		row.update(
			{
				"credit_to": d.credit_to,
				"mode_of_payment":mode_of_payment,
				"project": d.project,
				"company": d.company,
				"purchase_order": d.purchase_order,
				# "purchase_receipt": d.purchase_receipt,
				"expense_account": d.unrealized_profit_loss_account
				if d.is_internal_supplier == 1
				else d.expense_account,
				"cost_center": d.cost_center,
				"stock_qty": d.stock_qty,
				"stock_uom": d.stock_uom,
			}
		)

		if d.stock_uom != d.uom and d.stock_qty:
			row.update({"rate": (d.base_net_rate * d.qty) / d.stock_qty, "amount": d.base_net_amount})
			row.update({"price_list_rate": (d.price_list_rate * d.qty) / d.stock_qty })
		else:
			row.update({"rate": d.base_net_rate, "amount": d.base_net_amount})
			row.update({"price_list_rate": d.price_list_rate, "amount": d.base_net_amount})
		 
		row['profit_rate'] = row.get('rate',0) - row.get('incoming_rate',0)
		row['total_profit'] = (row.get('rate',0) - row.get('incoming_rate',0)) * (row.get('qty') or row.get('stock_qty') )

		total_tax = 0
		total_other_charges = 0
		for tax in tax_columns:
			item_tax = itemised_tax.get(d.name, {}).get(tax, {})
			row.update(
				{
					frappe.scrub(tax + " Rate"): item_tax.get("tax_rate", 0),
					frappe.scrub(tax + " Amount"): item_tax.get("tax_amount", 0),
				}
			)
			if item_tax.get("is_other_charges"):
				total_other_charges += flt(item_tax.get("tax_amount"))
			else:
				total_tax += flt(item_tax.get("tax_amount"))

		row.update(
			{
				"total_tax": total_tax,
				"total_other_charges": total_other_charges,
				"total": d.base_net_amount + total_tax,
				"currency": company_currency,
			}
		)

		if filters.get("group_by"):
			row.update({"percent_gt": flt(row["total"] / grand_total) * 100})
			group_by_field, subtotal_display_field = get_group_by_and_display_fields(filters)
			data, prev_group_by_value = add_total_row(
				data,
				filters,
				prev_group_by_value,
				d,
				total_row_map,
				group_by_field,
				subtotal_display_field,
				grand_total,
				tax_columns,
			)
			add_sub_total_row(row, total_row_map, d.get(group_by_field, ""), tax_columns)

		data.append(row)

	if filters.get("group_by") and item_list:
		total_row = total_row_map.get(prev_group_by_value or d.get("item_name"))
		total_row["percent_gt"] = flt(total_row["total"] / grand_total * 100)
		data.append(total_row)
		data.append({})
		add_sub_total_row(total_row, total_row_map, "total_row", tax_columns)
		data.append(total_row_map.get("total_row"))
		skip_total_row = 1
	return columns, data, None, None, None, skip_total_row





def get_columns(additional_table_columns, filters):
	columns = []

	if filters.get("group_by") != ("Item"):
		columns.extend(
			[
				{
					"label": _("Item Code"),
					"fieldname": "item_code",
					"fieldtype": "Link",
					"options": "Item",
					"width": 120,
				},
				{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 120},
				{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 150},
				# {"label": _("Discount Account"), "fieldname": "discount_account", "fieldtype": "Link", "options": "Account", "width": 150},
			
				#
			]
		)

	if filters.get("group_by") not in ("Item", "Item Group"):
		columns.extend(
			[
				{
					"label": _("Item Group"),
					"fieldname": "item_group",
					"fieldtype": "Link",
					"options": "Item Group",
					"width": 120,
				},
				{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
			]
		)

	columns.extend(
		[
			{
			"label": _("Purchase Order"),
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 100,
		},
		# {
		# 	"label": _("Purchase Receipt"),
		# 	"fieldname": "purchase_receipt",
		# 	"fieldtype": "Link",
		# 	"options": "Purchase Receipt",
		# 	"width": 100,
		# },
			
		{
			"label": _("Invoice"),
			"fieldname": "invoice",
			"fieldtype": "Link",
			"options": "Purchase Invoice",
			"width": 120,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120,
		},	

			
		]
	)

	if filters.get("group_by") not in ("Supplier", "Supplier Group"):
		columns.extend(
			[
				{
					"label": _("Supplier"),
					"fieldname": "supplier",
					"fieldtype": "Link",
					"options": "Supplier",
					"width": 120,
				},
				{"label": _("Supplier Name"), "fieldname": "supplier_name", "fieldtype": "Data", "width": 120},
			]
		)

	# if filters.get("group_by") != "Supplier":
	# 	columns.extend(
	# 		[
	# 			{
	# 				"label": _("Supplier Group"),
	# 				"fieldname": "supplier_group",
	# 				"fieldtype": "Link",
	# 				"options": "Supplier Group",
	# 				"width": 120,
	# 			}
	# 		]
	# 	)

	
	columns.extend(
		[
		# 	{
		# 	"label": _("Mode Of Payment"),
		# 	"fieldname": "mode_of_payment",
		# 	"fieldtype": "Data",
		# 	"width": 120,
		# },
		{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 80,
		},
		{
			"label": _("Cost Center"),
			"fieldname": "cost_center",
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 100,
		},
		{"label": _("Stock Qty"), "fieldname": "stock_qty", "fieldtype": "Float", "width": 100},
		{
			"label": _("Stock UOM"),
			"fieldname": "stock_uom",
			"fieldtype": "Link",
			"options": "UOM",
			"width": 100,
		},
		#  {"label": _("Cost Rate"), "fieldname": "incoming_rate", "fieldtype": "Float", "width": 120},
		#  {"label": _("Total Cost"), "fieldname": "total_cost", "fieldtype": "Float", "width": 120},
		 {
			"label": _("Purchase Rate"),
			"fieldname": "rate",
			"fieldtype": "Float",
			"options": "currency",
			"width": 100,
		},
		{
			"label": _("Rate before Discount"),
			"fieldname": "price_list_rate",
			"fieldtype": "Float",
			"options": "currency",
			"width": 100,
		},
		{
			"label": _("Total Purchase"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		# {
		# 	"label": _("Profit Rate"),
		# 	"fieldname": "profit_rate",
		# 	"fieldtype": "Currency",
		# 	"options": "currency",
		# 	"width": 100,
		# },
		# {
		# 	"label": _("Total Profit"),
		# 	"fieldname": "total_profit",
		# 	"fieldtype": "Currency",
		# 	"options": "currency",
		# 	"width": 100,
		# },
		{
			"label": _("Total Tax"),
			"fieldname": "total_tax",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"label": _("Total Other Charges"),
			"fieldname": "total_other_charges",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		

		]
	)
	if filters.get("group_by") != ("Item"):
		columns.extend(
			[
				{"label": _("Item Discount Amount"), "fieldname": "discount_amount", "fieldtype": "Currency", "options": "currency","width": 150},
			]
		)
	columns.extend(
			[
		{
			"label": _("Additional Discount Amount"),
			"fieldname": "base_discount_amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120,
		},
		{
			"label": _("Total Discount"),
			"fieldname": "total_discount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120,
		},
		# {
		# 	"label": _("Gross Profit"),
		# 	"fieldname": "gross_profit",
		# 	"fieldtype": "Currency",
		# 	"options": "currency",
		# 	"width": 120,
		# },			
		]
		)
	if additional_table_columns:
		columns += additional_table_columns


	if filters.get("group_by"):
		columns.append(
			{"label": _("% Of Grand Total"), "fieldname": "percent_gt", "fieldtype": "Float", "width": 80}
		)

	return columns


def get_conditions(filters, additional_conditions=None):
	conditions = ""

	for opts in (
		("company", " and company=%(company)s"),
		("supplier", " and `tabPurchase Invoice`.supplier = %(supplier)s"),
		("item_code", " and `tabPurchase Invoice Item`.item_code = %(item_code)s"),
		("from_date", " and `tabPurchase Invoice`.posting_date>=%(from_date)s"),
		("to_date", " and `tabPurchase Invoice`.posting_date<=%(to_date)s"),
	):
		if filters.get(opts[0]):
			conditions += opts[1]

	if additional_conditions:
		conditions += additional_conditions

	if filters.get("mode_of_payment"):
		conditions += """ and exists(select name from `tabPurchase Invoice Payment`
			where parent=`tabPurchase Invoice`.name
				and ifnull(`tabPurchase Invoice Payment`.mode_of_payment, '') = %(mode_of_payment)s)"""

	if filters.get("warehouse"):
		conditions += """and ifnull(`tabPurchase Invoice Item`.warehouse, '') = %(warehouse)s"""

	if filters.get("brand"):
		conditions += """and ifnull(`tabPurchase Invoice Item`.brand, '') = %(brand)s"""

	if filters.get("item_group"):
		conditions += """and ifnull(`tabPurchase Invoice Item`.item_group, '') = %(item_group)s"""
	
	if filters.get("item_code"):
		conditions += """and ifnull(`tabPurchase Invoice Item`.item_code, '') = %(item_code)s"""

	if not filters.get("group_by"):
		conditions += (
			"ORDER BY `tabPurchase Invoice`.posting_date desc, `tabPurchase Invoice Item`.item_group desc"
		)
	else:
		conditions += get_group_by_conditions(filters, "Purchase Invoice")

	return conditions


def get_group_by_conditions(filters, doctype):
	if filters.get("group_by") == "Invoice":
		return "ORDER BY `tab{0} Item`.parent desc".format(doctype)
	elif filters.get("group_by") == "Item":
		return "ORDER BY `tab{0} Item`.`item_code`".format(doctype)
	elif filters.get("group_by") == "Item Group":
		return "ORDER BY `tab{0} Item`.{1}".format(doctype, frappe.scrub(filters.get("group_by")))
	elif filters.get("group_by") in ("Supplier", "Supplier Group"):
		return "ORDER BY `tab{0}`.{1}".format(doctype, frappe.scrub(filters.get("group_by")))


def get_items(filters, additional_query_columns, additional_conditions=None):
	conditions = get_conditions(filters, additional_conditions)

	if additional_query_columns:
		additional_query_columns = ", " + ", ".join(additional_query_columns)
	else:
		additional_query_columns = ""

	return frappe.db.sql(
		"""
		select
			`tabPurchase Invoice Item`.name, `tabPurchase Invoice Item`.parent,
			`tabPurchase Invoice`.posting_date, `tabPurchase Invoice`.credit_to,
			`tabPurchase Invoice`.unrealized_profit_loss_account,
			`tabPurchase Invoice`.is_internal_supplier,
    		COALESCE(`tabPurchase Invoice`.discount_amount, 0) as base_discount_amount,
    		(COALESCE(`tabPurchase Invoice`.discount_amount, 0) + COALESCE(`tabPurchase Invoice Item`.`discount_amount`, 0)) as total_discount ,
			`tabPurchase Invoice`.project, `tabPurchase Invoice`.supplier, `tabPurchase Invoice`.remarks,`tabPurchase Invoice`.status,
			`tabPurchase Invoice`.company, `tabPurchase Invoice`.base_net_total,
			`tabPurchase Invoice Item`.item_code, `tabPurchase Invoice Item`.description,
			`tabPurchase Invoice Item`.`item_name`, `tabPurchase Invoice Item`.`item_group`,
			`tabPurchase Invoice Item`.`discount_account` , `tabPurchase Invoice Item`.`discount_amount` ,
			`tabPurchase Invoice Item`.purchase_order, 
			`tabPurchase Invoice Item`.expense_account, `tabPurchase Invoice Item`.cost_center,
			`tabPurchase Invoice Item`.stock_qty, `tabPurchase Invoice Item`.stock_uom,
			`tabPurchase Invoice Item`.base_net_rate, 
			`tabPurchase Invoice Item`.price_list_rate, 
			COALESCE(`tabPurchase Invoice Item`.base_net_amount, 0) as base_net_amount ,
			COALESCE(`tabPurchase Invoice Item`.base_net_amount, 0) + 
			(COALESCE(`tabPurchase Invoice`.discount_amount, 0) + COALESCE(`tabPurchase Invoice Item`.`discount_amount`, 0)) as gross_profit ,
			`tabPurchase Invoice`.supplier_name, `tabSupplier`.supplier_group, `tabPurchase Invoice Item`.po_detail,
			`tabPurchase Invoice`.update_stock, `tabPurchase Invoice Item`.uom, `tabPurchase Invoice Item`.qty {0}
			
		from `tabPurchase Invoice`, `tabPurchase Invoice Item`, `tabSupplier`
		where `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent AND `tabPurchase Invoice`.supplier = `tabSupplier`.name
			and `tabPurchase Invoice`.docstatus = 1 {1}
		""".format(
			additional_query_columns or "", conditions
		),
		filters,
		as_dict=1,
	) 
	 # nosec


# def get_purchase_reciepts_against_purchase_order(item_list):
# 	print("8888888888")
# 	so_dn_map = frappe._dict()
# 	so_item_rows = list(set([d.po_detail for d in item_list]))
# 	if so_item_rows:
# 		purchase_receipts = frappe.db.sql(
# 			"""
# 			select parent ,incoming_rate
# 			from `tabPurchase Receipt Item` 
# 			where docstatus=1
# 			group by parent
# 		"""
# 			% (", ".join(["%s"] * len(so_item_rows))),
# 			tuple(so_item_rows),
# 			as_dict=1,
# 		)

# 		for pr in purchase_receipts:
# 			# so_dn_map.setdefault(pr.po_detail, []).append(pr.parent)
# 			so_dn_map.setdefault(pr.parent, []).append(pr.incoming_rate)

# 	# return so_dn_map
# 	return {}



def get_grand_total(filters, doctype):

	return frappe.db.sql(
		""" SELECT
		SUM(`tab{0}`.base_grand_total)
		FROM `tab{0}`
		WHERE `tab{0}`.docstatus = 1
		and posting_date between %s and %s
	""".format(
			doctype
		),
		(filters.get("from_date"), filters.get("to_date")),
	)[0][
		0
	]  # nosec


def get_tax_accounts(
	item_list,
	columns,
	company_currency,
	doctype="Purchase Invoice",
	tax_doctype="Purchase Taxes and Charges",
):
	import json

	item_row_map = {}
	tax_columns = []
	invoice_item_row = {}
	itemised_tax = {}
	add_deduct_tax = "charge_type"

	tax_amount_precision = (
		get_field_precision(
			frappe.get_meta(tax_doctype).get_field("tax_amount"), currency=company_currency
		)
		or 2
	)

	for d in item_list:
		invoice_item_row.setdefault(d.parent, []).append(d)
		item_row_map.setdefault(d.parent, {}).setdefault(d.item_code or d.item_name, []).append(d)

	conditions = ""
	if doctype == "Purchase Invoice":
		conditions = " and category in ('Total', 'Valuation and Total') and base_tax_amount_after_discount_amount != 0"
		add_deduct_tax = "add_deduct_tax"

	tax_details = frappe.db.sql(
		"""
		select
			name, parent, description, item_wise_tax_detail, account_head,
			charge_type, {add_deduct_tax}, base_tax_amount_after_discount_amount
		from `tab%s`
		where
			parenttype = %s and docstatus = 1
			and (description is not null and description != '')
			and parent in (%s)
			%s
		order by description
	""".format(
			add_deduct_tax=add_deduct_tax
		)
		% (tax_doctype, "%s", ", ".join(["%s"] * len(invoice_item_row)), conditions),
		tuple([doctype] + list(invoice_item_row)),
	)

	account_doctype = frappe.qb.DocType("Account")

	query = (
		frappe.qb.from_(account_doctype)
		.select(account_doctype.name)
		.where((account_doctype.account_type == "Tax"))
	)

	tax_accounts = query.run()

	for (
		name,
		parent,
		description,
		item_wise_tax_detail,
		account_head,
		charge_type,
		add_deduct_tax,
		tax_amount,
	) in tax_details:
		description = handle_html(description)
		if description not in tax_columns and tax_amount:
			tax_columns.append(description)

		if item_wise_tax_detail:
			try:
				item_wise_tax_detail = json.loads(item_wise_tax_detail)

				for item_code, tax_data in item_wise_tax_detail.items():
					itemised_tax.setdefault(item_code, frappe._dict())

					if isinstance(tax_data, list):
						tax_rate, tax_amount = tax_data
					else:
						tax_rate = tax_data
						tax_amount = 0

					if charge_type == "Actual" and not tax_rate:
						tax_rate = "NA"

					item_net_amount = sum(
						[flt(d.base_net_amount) for d in item_row_map.get(parent, {}).get(item_code, [])]
					)

					for d in item_row_map.get(parent, {}).get(item_code, []):
						item_tax_amount = (
							flt((tax_amount * d.base_net_amount) / item_net_amount) if item_net_amount else 0
						)
						if item_tax_amount:
							tax_value = flt(item_tax_amount, tax_amount_precision)
							tax_value = (
								tax_value * -1
								if (doctype == "Purchase Invoice" and add_deduct_tax == "Deduct")
								else tax_value
							)

							itemised_tax.setdefault(d.name, {})[description] = frappe._dict(
								{
									"tax_rate": tax_rate,
									"tax_amount": tax_value,
									"is_other_charges": 0 if tuple([account_head]) in tax_accounts else 1,
								}
							)

			except ValueError:
				continue
		elif charge_type == "Actual" and tax_amount:
			for d in invoice_item_row.get(parent, []):
				itemised_tax.setdefault(d.name, {})[description] = frappe._dict(
					{
						"tax_rate": "NA",
						"tax_amount": flt((tax_amount * d.base_net_amount) / d.base_net_total, tax_amount_precision),
					}
				)

	tax_columns.sort()

	return itemised_tax, tax_columns


def add_total_row(
	data,
	filters,
	prev_group_by_value,
	item,
	total_row_map,
	group_by_field,
	subtotal_display_field,
	grand_total,
	tax_columns,
):
	if prev_group_by_value != item.get(group_by_field, ""):
		if prev_group_by_value:
			total_row = total_row_map.get(prev_group_by_value)
			data.append(total_row)
			data.append({})
			add_sub_total_row(total_row, total_row_map, "total_row", tax_columns)

		prev_group_by_value = item.get(group_by_field, "")

		total_row_map.setdefault(
			item.get(group_by_field, ""),
			{
				subtotal_display_field: get_display_value(filters, group_by_field, item),
				"stock_qty": 0.0,
				"amount": 0.0,
				"bold": 1,
				"total_tax": 0.0,
				"total": 0.0,
				"percent_gt": 0.0,
			},
		)

		total_row_map.setdefault(
			"total_row",
			{
				subtotal_display_field: "Total",
				"stock_qty": 0.0,
				"amount": 0.0,
				"bold": 1,
				"total_tax": 0.0,
				"total": 0.0,
				"percent_gt": 0.0,
			},
		)

	return data, prev_group_by_value


def get_display_value(filters, group_by_field, item):
	if filters.get("group_by") == "Item":
		if item.get("item_code") != item.get("item_name"):
			value = (
				cstr(item.get("item_code"))
				+ "<br><br>"
				+ "<span style='font-weight: normal'>"
				+ cstr(item.get("item_name"))
				+ "</span>"
			)
		else:
			value = item.get("item_code", "")
	elif filters.get("group_by") in ("Customer", "Supplier"):
		party = frappe.scrub(filters.get("group_by"))
		if item.get(party) != item.get(party + "_name"):
			value = (
				item.get(party)
				+ "<br><br>"
				+ "<span style='font-weight: normal'>"
				+ item.get(party + "_name")
				+ "</span>"
			)
		else:
			value = item.get(party)
	else:
		value = item.get(group_by_field)

	return value


def get_group_by_and_display_fields(filters):
	if filters.get("group_by") == "Item":
		group_by_field = "item_code"
		subtotal_display_field = "invoice"
	elif filters.get("group_by") == "Invoice":
		group_by_field = "parent"
		subtotal_display_field = "item_code"
	else:
		group_by_field = frappe.scrub(filters.get("group_by"))
		subtotal_display_field = "item_code"

	return group_by_field, subtotal_display_field


def add_sub_total_row(item, total_row_map, group_by_value, tax_columns):
	total_row = total_row_map.get(group_by_value)
	total_row["stock_qty"] += item["stock_qty"]
	total_row["amount"] += item["amount"]
	total_row["total_tax"] += item["total_tax"]
	total_row["total"] += item["total"]
	total_row["percent_gt"] += item["percent_gt"]

	for tax in tax_columns:
		total_row.setdefault(frappe.scrub(tax + " Amount"), 0.0)
		total_row[frappe.scrub(tax + " Amount")] += flt(item[frappe.scrub(tax + " Amount")])

def get_supplier_details():
	details = frappe.get_all("Supplier", fields=["name", "supplier_name", "supplier_group"])
	supplier_details = {}
	for d in details:
		supplier_details.setdefault(
			d.name, frappe._dict({"supplier_name": d.supplier_name, "supplier_group": d.supplier_group})
		)
	return supplier_details


def get_mode_of_payments(invoice_list):
	mode_of_payments_2 = {}
	
	if invoice_list:
		inv_mod = frappe.db.sql(
			"""select `tabPayment Entry`.name, `tabPayment Entry`.mode_of_payment
			,`tabPayment Entry Reference`.reference_name as parent
			from `tabPayment Entry` 
			INNER JOIN
			`tabPayment Entry Reference`
			 ON`tabPayment Entry`.name = `tabPayment Entry Reference`.parent
			where `tabPayment Entry Reference`.reference_name in (%s)
			group by `tabPayment Entry Reference`.reference_name"""
			% ", ".join(["%s"] * len(invoice_list)),
			tuple(invoice_list),
			as_dict=1,
		)
		for d in inv_mod:
			mode_of_payments_2.setdefault(d.parent, []).append(d.mode_of_payment)

	return mode_of_payments_2