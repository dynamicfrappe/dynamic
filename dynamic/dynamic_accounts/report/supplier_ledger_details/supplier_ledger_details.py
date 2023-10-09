# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

from collections import OrderedDict
import frappe
from frappe import _, _dict
from operator import itemgetter
"""
This report May have issue if it work with other branch of erpnext 
May You have An import error 
this report will work on three document only 
Payment Entry 
Jornal Entry 
Sales Invoice 


first get payment Entry For customer 
"""

# to cache translations
TRANSLATIONS = frappe._dict()





def get_columns(filters=None):
	columns = [
			{
				"label": _("Posting Date"),
				"fieldname": "cur_date",
				"fieldtype": "Date",
				"width": 120,
			},
		
			 {
				"label": _("Document Type"),
				"fieldname": "document_type",
				"fieldtype": "Data",
				"width": 150,
			},
			{
				"label": _("Document Name"),
				"fieldname": "document_Name",
				"fieldtype": "Dynamic Link",
				"options" :"document_type",
				"width": 200,
			},
			{
				"label": _("Credit"),
				"fieldname": "credit",
				"fieldtype": "Data",
				"width": 80,
			},
			{
				"label": _("Depit"),
				"fieldname": "depit",
				"fieldtype": "Data",
				"width": 80,
			},
			{
				"label": _("Balance"),
				"fieldname": "balance",
				"fieldtype": "Data",
				"width": 80,
			},
			{
				"label": _("Descreptiom"),
				"fieldname": "des",
				"fieldtype": "Data",
				"width": 250,
			},
			{
				"label": _("Qty"),
				"fieldname": "qty",
				"fieldtype": "Data",
				"width": 120,
			},
			{
				"label": _("UOM"),
				"fieldname": "uom",
				"fieldtype": "Data",
				"width": 120,
			},
			{
				"label": _("Price"),
				"fieldname": "price",
				"fieldtype": "Data",
				"width": 120,
			},
			{
				"label": _("Total"),
				"fieldname": "total",
				"fieldtype": "Data",
				"width": 120,
			},
			{
				"label": _("Discount"),
				"fieldname": "discount",
				"fieldtype": "Data",
				"width": 120,
			},

		
	]
	return columns

def get_cutomer_purchase_invoice(supplier ,from_date , to_date) :
	
	data_purchase_invoice = frappe.db.sql(f"""SELECT "Purchase Invoice" as document_type ,b.posting_date as cur_date ,
							a.parent as document_Name  ,b.grand_total as  depit , 0 as credit
							FROM `tabPurchase Invoice Item` as a 
							INNER JOIN  `tabPurchase Invoice` as b 
							ON a.parent=b.name
							WHERE b.supplier = '{supplier}' and  b.docstatus =1  and
							b.posting_date between date('{from_date}')   and date('{to_date}')
							GROUP BY a.parent	""",as_dict=True)
	return data_purchase_invoice

def get_cutomer_purchase_return(supplier ,from_date , to_date) :
	
	data_purchase_invoice = frappe.db.sql(f"""SELECT "Purchase Invoice" as document_type ,b.posting_date as cur_date ,
							a.parent as document_Name  ,b.grand_total as depit  , 0 as  credit
							FROM `tabPurchase Invoice Item` as a 
							INNER JOIN  `tabPurchase Invoice` as b 
							ON a.parent=b.name
							WHERE b.supplier = '{supplier}' and  b.docstatus =1 and b.is_return=1 and
							b.posting_date between date('{from_date}')   and date('{to_date}')
							GROUP BY a.parent	""",as_dict=True)
	return data_purchase_invoice

def get_supplier_journal_entry(supplier ,from_date , to_date) :
	data_journal_entry = frappe.db.sql(f""" SELECT a.name ,b.posting_date as cur_date,
	 "Journal Entry" as document_type , a.parent as document_Name ,
	 debit_in_account_currency as depit , credit_in_account_currency as credit
	  FROM 
	`tabJournal Entry Account`  a 
	INNER Join `tabJournal Entry` b
	ON a.parent=b.name
	WHERE a.party_type = "Supplier" and a.party='{supplier}' and b.docstatus =1
	AND b.posting_date between date('{from_date}')   and date('{to_date}')
	""",as_dict=1
	)
	return data_journal_entry
def get_supplier_payment_entry(supplier ,from_date , to_date ) :
	data_payments = frappe.db.sql(f"""
	SELECT posting_date as cur_date,"Payment Entry" as document_type , name as document_Name 
		,paid_amount as credit 
	    FROM `tabPayment Entry` 
	WHERE party_type= "Supplier" and party='{supplier}'  and payment_type="Receive" and docstatus =1
	and posting_date between date('{from_date}')   and date('{to_date}')
	""",as_dict=1)
	
	return data_payments 
def get_data(filters=None):
	data = []
	calculated_data =[]
	if filters :
		#frappe.throw(filters.get("customer"))
		# get Customer Balance For Openning 
		date = filters.get("from_date")
		to_date = filters.get("to_date")
		company = filters.get("company")
		party = filters.get("supplier")	
		data_sql = 	frappe.db.sql (f"""
		select company, sum(debit_in_account_currency) - sum(credit_in_account_currency) as balance ,
		sum(debit_in_account_currency) as depit , sum(credit_in_account_currency) as credit
		,"Opening" as document_type , date('{date}') as cur_date
		from `tabGL Entry`
		where party_type = "Supplier" and party='{party}'
		and is_cancelled = 0 and company = '{company}'
		and posting_date < date('{date}')
		
		""" ,as_dict=1)
		# frappe.throw(str(data_sql))

		data = data_sql
		payment_data = get_supplier_payment_entry(party , date , to_date)
		journal_entry_data = get_supplier_journal_entry(party , date , to_date)
		purchase_invoice_data = get_cutomer_purchase_invoice(party , date , to_date)
		# purchase_return_data = get_cutomer_purchase_return(party , date , to_date)
		data = data + payment_data +journal_entry_data +purchase_invoice_data 
		data = sorted(data , key=itemgetter('cur_date'))
		n = -1 
		depit_total = 0
		credit_total = 0 
		for object in data  :
			# caculate balance 
			depit_total = depit_total + float(object.get("depit") or 0 )
			credit_total = credit_total +float(object.get("credit") or 0 )
			if n != -1 :
				back_row = data[n]
				balance = float(back_row.get("balance") or 0)
				
				
				row_caculate = float(object.get("depit") or 0 ) - float(object.get("credit") or 0 )
				object["balance"] = balance + row_caculate
			if object.get("document_type") != "Purchase Invoice" :
				calculated_data.append(object)
			if object.get("document_type") == "Purchase Invoice" :
				calculated_data.append(object)
				purchase_invoice_items = frappe.db.sql(f"""SELECT item_name as des ,qty  ,
				  uom ,base_rate as price , base_amount as total
				FROM 
				`tabPurchase Invoice Item` WHERE parent='{object.get("document_Name")}'
				
				""",as_dict=1)
				for obj_item in purchase_invoice_items  :
					if filters.get("show_items") ==1 :
						calculated_data.append(obj_item)
			n = n+1
		total_balance  = data[-1].get("balance")
	
		calculated_data.append({"depit" : depit_total , "credit" : credit_total ,
			  "document_type" :"Totals" ,
			  					"balance" :total_balance})
	return calculated_data

def execute(filters=None):
	columns = get_columns(filters=filters)
	data =  get_data(filters=filters)
	return columns, data
