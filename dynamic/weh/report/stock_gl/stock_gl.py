# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_date(filters)
	return columns, data


def get_date(filters):

	conditions = "i.disabled = 0"
	
	if filters.get("item_code"):
		conditions += f""" AND ste.item_code = '{filters.get("item_code")}'  """
	if filters.get("warehouse"):
		conditions += f""" AND ste.warehouse = '{filters.get("warehouse")}'  """

	if filters.get("brand"):
		conditions += f""" AND i.brand = '{filters.get("brand")}'  """

	if filters.get("item_group"):
		conditions += f""" AND i.item_group = '{filters.get("item_group")}' """

	items = frappe.db.sql(f"""
					SELECT 
						ste.item_code,
						ste.warehouse,
					   	i.item_name
					FROM
						`tabStock Ledger Entry` as ste
					JOIN
					   `tabItem` AS i
					ON
					   ste.item_code = i.name
					WHERE
					   {conditions}
					GROUP BY
						ste.item_code, ste.warehouse
					
	""",as_dict=1)
	return items


def get_columns(filters):
	columns = [
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 200
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 200
		},
		{
			"label": _("Opening"),
			"fieldname": "opening",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Purchase"),
			"fieldname": "purchase",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Transfers"),
			"fieldname": "transfers",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Delivery Note"),
			"fieldname": "delivery_note",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Issues"),
			"fieldname": "issues",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Repack"),
			"fieldname": "repack",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Stock Reconciliation"),
			"fieldname": "stock_reconciliation",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Balance"),
			"fieldname": "balance",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Valuation Rate"),
			"fieldname": "valuation_rate",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Total"),
			"fieldname": "total",
			"fieldtype": "Float",
			"width": 100
		},
		
	]
	return columns




def get_opening_balance(filters, columns, sl_entries):
	if not (filters.item_code and filters.warehouse and filters.from_date):
		return

	from erpnext.stock.stock_ledger import get_previous_sle

	last_entry = get_previous_sle(
		{
			"item_code": filters.item_code,
			"warehouse_condition": get_warehouse_condition(filters.warehouse),
			"posting_date": filters.from_date,
			"posting_time": "00:00:00",
		}
	)

	# check if any SLEs are actually Opening Stock Reconciliation
	for sle in list(sl_entries):
		if (
			sle.get("voucher_type") == "Stock Reconciliation"
			and sle.get("date").split()[0] == filters.from_date
			and frappe.db.get_value("Stock Reconciliation", sle.voucher_no, "purpose") == "Opening Stock"
		):
			last_entry = sle
			sl_entries.remove(sle)

	row = {
		"item_code": _("'Opening'"),
		"qty_after_transaction": last_entry.get("qty_after_transaction", 0),
		"valuation_rate": last_entry.get("valuation_rate", 0),
		"stock_value": last_entry.get("stock_value", 0),
	}

	return row

def get_warehouse_condition(warehouse):
	warehouse_details = frappe.db.get_value("Warehouse", warehouse, ["lft", "rgt"], as_dict=1)
	if warehouse_details:
		return (
			" exists (select name from `tabWarehouse` wh \
			where wh.lft >= %s and wh.rgt <= %s and warehouse = wh.name)"
			% (warehouse_details.lft, warehouse_details.rgt)
		)

	return ""