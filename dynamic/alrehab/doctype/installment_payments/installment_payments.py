# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now
from frappe import _

class InstallmentPayments(Document):
	def validate(self):
		if self.items:
			# t = sum(item.get('total_payed') for item in self.items)
			# totla_paid = sum(x.total_payed for x in self.items)
			self.total_paid = sum(item.get('total_payed') for item in self.items)





@frappe.whitelist()
def get_customer_instllment(cst,item):
	sql_before_taxes = f"""
	SELECT name 
	FROM `tabinstallment Entry`
	WHERE customer='{cst}'
	"""
	sql_before_taxes_data = frappe.db.sql(sql_before_taxes,as_dict=1)
	for entry in sql_before_taxes_data:
		entry_doc = frappe.get_doc("installment Entry",entry.name)
		entry_doc.caculate_installment_value()
		
	sql = f"""
	SELECT name 
	,delay_penalty
	,total_payed,total_value
	,outstanding_value
	FROM `tabinstallment Entry`
	WHERE customer='{cst}' AND `tabinstallment Entry`.item='{item}' AND IFNULL(total_payed,0)<total_value
	"""
	print(sql)
	data_sql = frappe.db.sql(sql,as_dict=1)
	return data_sql


@frappe.whitelist()
def create_journal_entry(doc_name):
	installment_payments_doc = frappe.get_doc('Installment Payments',doc_name)
	if  installment_payments_doc.items:
		for row in installment_payments_doc.items:
			#create je
			create_je_row(row)
		frappe.msgprint("Created Journal Entry Done")
		



def create_je_row(row):
	installment_entry_doc = frappe.get_doc('installment Entry',row.installment_entry)
	total_payed = float(installment_entry_doc.total_payed or 0) + float(row.total_payed or 0) 
	outstanding_value = float(installment_entry_doc.outstanding_value or 0) - float(row.total_payed or 0)
	if float(row.total_payed) > float(installment_entry_doc.outstanding_value):
		frappe.throw(_("Total Paid Amount More Than Total Value"))

	# frappe.errprint(f'-installment_entry_doc->{installment_entry_doc.__dict__}')
	journal_entry = frappe.new_doc("Journal Entry")
	journal_entry.posting_date = getdate()
	company = frappe.defaults.get_user_default("Company")
	debitor_account = frappe.get_value("Company" , company , "default_receivable_account")
	credit_account = frappe.db.sql(f"""
		SELECT default_account as account FROM `tabMode of Payment Account` WHERE parent='{row.mode_of_payment}'
	""",as_dict=1)[0]
	journal_entry.installment_entry = row.installment_entry
	journal_entry.append("accounts" ,
					{
					"account" :debitor_account 
					,"party_type" : "Customer"
					,"party":installment_entry_doc.customer 
					, "debit_in_account_currency" :0.0
					,"credit_in_account_currency" : row.total_payed
					,"cost_center" : installment_entry_doc.cost_center
					# ,"is_advance" : "Yes"
					}
					)
	journal_entry.append("accounts" ,
					{
					"account" :credit_account.get('account') ,
					"debit_in_account_currency" : row.total_payed,
					"credit_in_account_currency" : 0.0,
					"cost_center" : installment_entry_doc.cost_center})

	journal_entry.insert()
	journal_entry.submit()
	#**update 
	
	installment_entry_doc.db_set("total_payed",total_payed)
	installment_entry_doc.db_set("outstanding_value",outstanding_value)
	installment_entry_doc.append("paid_entry",{
		"type":"Journal Entry",
		"document":journal_entry.name
	})
	installment_entry_doc.save(ignore_permissions=True)


