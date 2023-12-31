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
	return RehabCompoundInfo(filters).run()


class RehabCompoundInfo(object):
	def __init__(self,filters):
		self.filters  = frappe._dict(filters or {})

	def run(self):
		self.get_columns()
		self.get_data()
		return self.columns, self.data

	def get_data(self):
		self.data = []
		self.data = self.get_transaction()
		return self.data


	def get_transaction(self):
		self.conditions = "  1=1 "
		if self.filters.get("contract"):
			self.conditions += " and `tabRehab Contract`.name = '%s'"%self.filters.get("contract")
		if self.filters.get("customer"):
			self.conditions += " and `tabRehab Contract`.unit = '%s'"%self.filters.get("customer")
		# if self.filters.get("supplier"):
		# 	self.conditions += " and tpo.supplier = '%s'"%self.filters.get("supplier")
		# if self.filters.get("purchase_order"):
		# 	self.conditions += " and tpo.name = '%s'"%self.filters.get("purchase_order")
		sql_query_new = f"""
					SELECT `tabRehab Contract`.unit
					,`tabRehab Contract`.installment_entry_type as penalty_template
					,`tabRehab Contract`.maintenance_deposit_value as total_value
					,`tabRehab Contract`.name as contract 
					,Year(`tabRehab Contract`.creation) as year 
					,`tabinstallment Entry Type`.item as item_name
					,`tabItem`.item_name as full_name
					,`tabInstallment Payments Items`.total_payed as paid_amount
					,`tabInstallment Payments Items`.delay_penalty
					,`tabinstallment Entry`.due_date as date_total_value
					,`tabJournal installment`.journal_type
					FROM `tabRehab Contract`
					INNER JOIN `tabInstallment Payments`
					ON `tabInstallment Payments`.unit=`tabRehab Contract`.unit
					INNER JOIN `tabJournal installment`
					ON `tabJournal installment`.contract=`tabRehab Contract`.name
					INNER JOIN `tabInstallment Payments Items`
					ON `tabInstallment Payments Items`.parent=`tabInstallment Payments`.name
					INNER JOIN `tabinstallment Entry` 
					ON `tabinstallment Entry`.name=`tabInstallment Payments Items`.installment_entry
					INNER JOIN `tabinstallment Entry Type`
					ON `tabinstallment Entry Type`.name=`tabRehab Contract`.installment_entry_type
					INNER JOIN `tabItem`
					ON `tabinstallment Entry Type`.item = `tabItem`.name
					WHERE {self.conditions}
		"""
		sql_data = frappe.db.sql(sql_query_new,as_dict=1)
		# frappe.errprint(f"sql_query_new is ==> {sql_data}")
		return sql_data



	def get_columns(self):
		# add columns wich appear data
		self.columns = [
			{
				"label": _("Unit"),
				"fieldname": "unit",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 150,
			},
			{
				"label": _("Item Name"),
				"fieldname": "item_name",
				"fieldtype": "Data",
				"width": 150,
			},
			{
                "label": _("Full Name"),
                "fieldname": "full_name",
                "fieldtype": "Data",
                "width": 130,
            },
			{
				"label": _("Contract"),
				"fieldname": "contract",
				"fieldtype": "Link",
				"options": "Rehab Contract",
				"width": 150,
			},
			{
                "label": _("Financial penalty template"),
                "fieldname": "penalty_template",
                "fieldtype": "Link",
				"options": "Financial penalty template",
                "width": 130,
            },
			{
                "label": _("Paid Amount"),
                "fieldname": "paid_amount",
                "fieldtype": "Float",
                "width": 130,
            },
			{
                "label": _("Total Value"),
                "fieldname": "total_value",
                "fieldtype": "Float",
                "width": 130,
            },
			{
                "label": _("Delay Penalty"),
                "fieldname": "delay_penalty",
                "fieldtype": "Float",
                "width": 130,
            },
			{
                "label": _("Date Total Value"),
                "fieldname": "date_total_value",
                "fieldtype": "Date",
                "width": 130,
            },
			{
                "label": _("Year"),
                "fieldname": "year",
                "fieldtype": "Data",
                "width": 130,
            },
			{
                "label": _("Journal Type"),
                "fieldname": "journal_type",
                "fieldtype": "Data",
                "width": 130,
            },
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