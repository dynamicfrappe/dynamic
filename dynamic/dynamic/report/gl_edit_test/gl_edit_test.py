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
	return GLEditTest(filters).run()


class GLEditTest(object):
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
		get_new = self.get_all_data(conditions)
		return get_new

	def get_all_data(self,conditions):
		data = []
		if self.filters.get("from_date"):
			conditions += " AND `tabPurchase Invoice`.creation >= '%s'"%self.filters.get("from_date")
		if self.filters.get("to_date"):
			
			conditions += " AND `tabPurchase Invoice`.creation <= '%s'"%self.filters.get("to_date")

		gl_sql = f"""
		SELECT name as gl_name,voucher_no as invoice_or_item,voucher_type ,party ,debit, credit
		,if(voucher_type='Sales Invoice' ,0,1) as indent,
		'' as parent_invoice
		  FROM `tabGL Entry` tge
		WHERE party_type='Customer' AND voucher_type='Sales Invoice' AND party='ابراهيم عبده'
		LIMIT 5
		"""
		gl_data = frappe.db.sql(gl_sql,as_dict=1)
		for index, row in  enumerate(gl_data):
			data.append(row)
			if row.voucher_type == 'Sales Invoice' and row.invoice_or_item=='ACC-SINV-2023-04734':
				sinv_items = frappe.db.sql(f'''
					SELECT parent as parent_invoice,parent, 'zzzzzzzzzzzzzzz' as t,1 as indent, item_code as invoice_or_item,
			        qty FROM `tabSales Invoice Item`
					WHERE parent='{row.invoice_or_item}'
				''',as_dict=1)
				for item in sinv_items:
					data.append(item)


		print(f'\n\n\n\n==data==>',data,'\n\n\n\n')

		x = [{'gl_name': '5f5043b6dc', 'invoice_or_item': 'ACC-SINV-2023-04734', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 8.0, 'credit': 0.0, 'indent': 1, 'parent_invoice': ''},
        {'parent_invoice': 'ACC-SINV-2023-04734', 'parent': 'ACC-SINV-2023-04734', 't': 'zzzzzzzzzzzzzzz', 'indent': 0, 'invoice_or_item': '312170171', 'qty': 1.0},
		{'parent_invoice': 'ACC-SINV-2023-04734', 'parent': 'ACC-SINV-2023-04734', 't': 'zzzzzzzzzzzzzzz', 'indent': 0, 'invoice_or_item': '10352004', 'qty': 1.0},
		  {'parent_invoice': 'ACC-SINV-2023-04734', 'parent': 'ACC-SINV-2023-04734', 't': 'zzzzzzzzzzzzzzz', 'indent': 0, 'invoice_or_item': '3121604', 'qty': 1.0}, {'gl_name': 'ACC-GLE-2023-01208', 'invoice_or_item': 'ACC-SINV-2023-00042', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 770.0, 'credit': 0.0, 'indent': 1, 'parent_invoice': ''}, {'gl_name': 'ACC-GLE-2023-19605', 'invoice_or_item': 'ACC-SINV-2023-02053', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 2300.0, 'credit': 0.0, 'indent': 1, 'parent_invoice': ''}, {'gl_name': 'ACC-GLE-2023-68660', 'invoice_or_item': 'ACC-SINV-2023-04733', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 4691.0, 'credit': 0.0, 'indent': 1, 'parent_invoice': ''}, {'gl_name': 'ACC-GLE-2023-68661', 'invoice_or_item': 'ACC-SINV-2023-04733', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 0.0, 'credit': 4691.0, 'indent': 1, 'parent_invoice': ''}]

		y = [
			{"parent_invoice":"",'gl_name': '5f5043b6dc', 'invoice_or_item': 'ACC-SINV-2023-04734', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 8.0, 'credit': 0.0, 'indent': 0},
			{'parent_invoice':'ACC-SINV-2023-04734','parent': 'ACC-SINV-2023-04734','parent': 'ACC-SINV-2023-04734', 't': 'zzzzzzzzzzzzzzz', 'indent': 1, 'invoice_or_item': '312170171', 'qty': 1.0,'gl_name':'test'},
			{'parent_invoice':'ACC-SINV-2023-04734','parent': 'ACC-SINV-2023-04734','parent': 'ACC-SINV-2023-04734', 't': 'zzzzzzzzzzzzzzz', 'indent': 1, 'invoice_or_item': '10352004', 'qty': 1.0},
			{'parent_invoice':'ACC-SINV-2023-04734','parent': 'ACC-SINV-2023-04734','parent': 'ACC-SINV-2023-04734', 't': 'zzzzzzzzzzzzzzz', 'indent': 1, 'invoice_or_item': '3121604', 'qty': 1.0},
			# {'gl_name': 'ACC-GLE-2023-01208', 'voucher_no': 'ACC-SINV-2023-00042', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 770.0, 'credit': 0.0, 'indent': 1}, {'gl_name': 'ACC-GLE-2023-19605', 'voucher_no': 'ACC-SINV-2023-02053', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 2300.0, 'credit': 0.0, 'indent': 1}, {'gl_name': 'ACC-GLE-2023-68660', 'voucher_no': 'ACC-SINV-2023-04733', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 4691.0, 'credit': 0.0, 'indent': 1}, {'gl_name': 'ACC-GLE-2023-68661', 'voucher_no': 'ACC-SINV-2023-04733', 'voucher_type': 'Sales Invoice', 'party': 'ابراهيم عبده', 'debit': 0.0, 'credit': 4691.0, 'indent': 1}
			]
		return gl_data



	def get_columns(self):
		# add columns wich appear data
		self.columns = [
			{
				"label": _("Voucher No"),
				"fieldname": "invoice_or_item",
				"fieldtype": "Data",
				"width": 180,
			},
			{
				"label": _("GL"),
				"fieldname": "gl_name",
				"fieldtype": "Link",
				"options": "GL Entry",
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
				"label": _("qty"),
				"fieldname": "qty",
				"fieldtype": "Float",
				"width": 120,
			},
			{
				"label": _("rate"),
				"fieldname": "rate",
				"fieldtype": "Float",
				"width": 120,
			},
			{
				"label": _("Total Allocated Amount"),
				"fieldname": "total_allocated_amount",
				"fieldtype": "Currency",
				"width": 120,
			},
	
		]


  