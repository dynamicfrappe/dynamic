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
	return stock_entry_repack(filters).run()


class stock_entry_repack(object):
	def __init__(self,filters):
		self.filters  = frappe._dict(filters or {})
	def run(self):
		self.get_columns()
		self.get_data()
		return self.columns, self.data

	def get_data(self):
		self.data = []
		# self.conditions, self.values = self.get_conditions(self.filters)
		self.data = self.get_transaction(self.filters)
		return self.data

	def get_transaction(self,filters):
		# filter by 1-sales person 2- cost center 3- warehouse 4-item group
		conditions = "  1=1 "
		get_new = self.get_new_opportunity(conditions)
		# frappe.errprint(f"all is ==> {get_new}")
		return get_new

	def get_new_opportunity(self,conditions):
		item_group = ''
		if self.filters.get("from_date"):
			conditions += " and `tabStock Entry`.posting_date >= '%s'"%self.filters.get("from_date")
		if self.filters.get("to_date"):
			conditions += " and `tabStock Entry`.posting_date <= '%s'"%self.filters.get("to_date")
		sql_query_new = f"""
					select `tabStock Entry`.name stock_entry,
					`tabStock Entry`.stock_entry_transfer_type,
					`tabStock Entry Detail`.item_code
					,`tabStock Entry Detail`.qty
					from `tabStock Entry`
					INNER JOIN `tabStock Entry Detail`
					ON `tabStock Entry Detail`.parent=`tabStock Entry`.name
					WHERE {conditions} 
					AND `tabStock Entry`.stock_entry_type='Repack'
					AND `tabStock Entry`.stock_entry_transfer_type <> ''
					
		""".format(conditions=conditions)
		sql_data = frappe.db.sql(sql_query_new,as_dict=1)
		# frappe.errprint(f"sql_query_new is ==> {sql_data}")
		return sql_data



	def get_columns(self):
		# add columns wich appear data
		self.columns = [
			{
				"label": _("Stock Entry"),
				"fieldname": "stock_entry",
				"fieldtype": "Link",
				"options": "Stock Entry",
				"width": 250,
			},
			{
				"label": _("Stock Entry Transfer"),
				"fieldname": "stock_entry_transfer_type",
				"fieldtype": "Link",
				"options": "Stock Entry",
				"width": 250,
			},
			{
				"label": _("Item Code"),
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options": "Item",
				"width": 250,
			},
			{
				"label": _("QTY"),
				"fieldname": "qty",
				"fieldtype": "Flaot",
				"width": 250,
			},
			# {
            #     "fieldname": "purchase_amount",
            #     "label": _("Purchase Amount"),
            #     "fieldtype": "Data",
            #     "width": 130,
            # },
			# {
            #     "fieldname": "total_paid",
            #     "label": _("Total Paid"),
            #     "fieldtype": "Data",
            #     "width": 130,
            # },
			# {
            #     "fieldname": "outstanding",
            #     "label": _("Outstanding"),
            #     "fieldtype": "Data",
            #     "width": 130,
            # },
			# {
            #     "fieldname": "total_count",
            #     "label": _("No.Order"),
            #     "fieldtype": "Data",
            #     "width": 130,
            # },
			# {
            #     "fieldname": "qty",
            #     "label": _("Qty"),
            #     "fieldtype": "Data",
            #     "width": 130,
            # },
			# {
            #     "fieldname": "no.invoices",
            #     "label": _("No.Inovoice"),
            #     "fieldtype": "Data",
            #     "width": 130,
            # },
			# {
            #     "fieldname": "actual_qty",
            #     "label": _("Actual Qty"),
            #     "fieldtype": "Data",
            #     "width": 130,
            # },
		]


"""
SELECT * , (`data`.`purchase_amount` - `data`.`total_paid`)outstanding 
				FROM(
						select `tpo`.`name` purchase_order,`tpo`.`supplier`,
						IFNULL(SUM(`tge`.`debit`),0) as total_paid,`tpo`.`grand_total` purchase_amount
						from `tabPurchase Order` tpo
						LEFT JOIN `tabGL Entry` tge
						ON
						(
						(tge.against_voucher = tpo.name or tge.against_voucher IS NULL)
						AND
						(tge.voucher_type ='Payment Entry' or tge.voucher_type IS NULL) 
						AND
						(tge.against_voucher_type ='Payment Entry' or tge.against_voucher_type IS NULL) 
						)
						WHERE {conditions} AND tpo.docstatus=1 
						GROUP  BY `tpo`.`name`
						) as data


"""