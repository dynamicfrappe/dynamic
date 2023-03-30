# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

# import frappe



import frappe
from frappe import _
from frappe.utils import  getdate
from frappe.utils import (
	flt,
)

def execute(filters=None):
	return WarehouseReservationAvailQty(filters).run()


class WarehouseReservationAvailQty(object):
	def __init__(self,filters):
		self.filters  = frappe._dict(filters or {})
	def run(self):
		self.get_columns()
		self.get_data()
		return self.columns, self.data

	def get_data(self):
		self.data = []
		self.data = self.get_transaction(self.filters)
		return self.data

	def get_transaction(self,filters):
		conditions = "  1=1 "
		get_new = self.get_avail_qty(conditions)
		return get_new

	def get_avail_qty(self,conditions):
		if self.filters.get("from_date"):
			conditions += " AND `tabPurchase Invoice`.creation >= '%s'"%self.filters.get("from_date")
		if self.filters.get("to_date"):
			conditions += " AND `tabPurchase Invoice`.creation <= '%s'"%self.filters.get("to_date")
		sql_query_new = f"""
		
		"""
		sql_data = frappe.db.sql(sql_query_new,as_dict=1)

		return sql_data



	def get_columns(self):
		# add columns wich appear data
		self.columns = [
			{
				"label": _("Purchase Order"),
				"fieldname": "purchase_order",
				"fieldtype": "Link",
				"options": "Purchase Order",
				"width": 180,
			},
			{
				"label": _("Purchase Invoice"),
				"fieldname": "purchase_invoice",
				"fieldtype": "Link",
				"options": "Purchase Invoice",
				"width": 180,
			},
			{
				"label": _("Payment Entry"),
				"fieldname": "payment_entry",
				"fieldtype": "Link",
				"options": "Payment Entry",
				"width": 180,
			},
			{
				"label": _("Purchase Order Grand Total"),
				"fieldname": "po_order_amount",
				"fieldtype": "Currency",
				"width": 120,
			},
			{
				"label": _("Purchase Invoice Grand Total"),
				"fieldname": "pi_invoice_amount",
				"fieldtype": "Currency",
				"width": 120,
			},
			{
				"label": _("Paid Amount"),
				"fieldname": "paid_amount",
				"fieldtype": "Currency",
				"width": 120,
			},
			{
				"label": _("Unallocated Amount"),
				"fieldname": "unallocated_amount",
				"fieldtype": "Currency",
				"width": 120,
			},
			{
				"label": _("Total Allocated Amount"),
				"fieldname": "total_allocated_amount",
				"fieldtype": "Currency",
				"width": 120,
			},
	
		]


  