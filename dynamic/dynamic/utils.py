import frappe 
from erpnext.accounts.utils import get_account_currency, get_balance_on
from frappe.utils import today

#dynamic.dynamic.utils



def create_customizations(*args , **kwargs) :
	""" 
		this run on migrate to create custom field in payment entry to avoid any crash 
      """
   # add exchange rate to payment entry
   create_currency_exchange()
   # add field to journal entry account fuction 
   create_currency_exchange_je()
   create_domain_if_not_exists("Qaswaa")


def create_domain_if_not_exists(domain_name):
	domains = frappe.get_all("Domain" , pluck="domain")
	if domain_name not in domains :
		doc = frappe.new_doc("Domain")
		doc.domain = domain_name
		doc.insert(ignore_permissions=True)
		doc.save(ignore_permissions=True)

# Create Field Exchange rate to journal entry account 
def create_currency_exchange_je(*args,**kwargs) :
	old_fields = frappe.db.sql(""" 
			SELECT name FROM `tabCustom Field` WHERE 
			dt = "Journal Entry Account" AND fieldname = "account_currency_exchange"
	""" ,as_dict=1) 
	if old_fields and len(old_fields) > 0 :
		print("currency_exchange Filed is exit")
		return 0
	field = frappe.new_doc("Custom Field")
	field.dt = "Journal Entry Account"
	field.label = "Account Currency Exchange"
	field.fieldname = "account_currency_exchange"
	field.insert_after  ="balance"
	field.read_only = 1
	#field.hidden = 1
	field.fieldtype = "Data"
	field.save()
	print("currency_exchange Filed is created")
#Create Field in payment entry to currency exchange rate
def create_currency_exchange(*args , **kwargs) :
	# chek if field exit
	old_fields = frappe.db.sql(""" 
	SELECT name FROM `tabCustom Field` WHERE 
	dt = "Payment Entry" AND fieldname = "currency_exchange"
	""" ,as_dict=1) 
	if old_fields and len(old_fields) > 0 :
		print("currency_exchange Filed is exit")
		return 0
	field = frappe.new_doc("Custom Field")
	field.dt = "Payment Entry"
	field.label = "Currency Exchange"
	field.fieldname = "currency_exchange"
	field.insert_after  ="paid_from_account_balance"
	field.read_only = 1
	field.hidden = 1
	field.fieldtype = "Data"
	field.save()
	print("currency_exchange Filed is created")

@frappe.whitelist()
def currency_valuation_rate(account ) :
	date = today()
	balance_in_compnay_currency = get_balance_on (account =account ,date =str(date))
	balance_in_account_currency = get_balance_on (account =account ,date =str(date) , in_account_currency=False)
	try :
		valuation =  balance_in_account_currency / balance_in_compnay_currency
		return valuation 
	except Exception as e :
		print("-----------------------------------",str(e))
		return False



# from io import BytesIO
# import io




#  frm.add_custom_button(
#       __("get all files"),
#       function () {
#         var w = window.open(
#           frappe.urllib.get_full_url(
#             "/api/method/dynamic.dynamic.utils.export_invoices"
#           )
#         );
#         if (!w) {
#           frappe.msgprint(__("Please enable pop-ups")); return;
#         }
     
#       },
#     );
	

# @frappe.whitelist()
# def export_invoices(filters=None):
# 	invoices = frappe.get_all(
# 		"Lead", filters ={}, fields=["name"]
# 	)
# 	invoices = [inv["name"] for inv in invoices]
# 	print("invoices",invoices)	

# 	attachments = get_e_invoice_attachments(invoices)

# 	zip_filename = "{0}-journal_entry.zip".format(frappe.utils.get_datetime().strftime("%Y%m%d_%H%M%S"))

# 	download_zip(attachments, zip_filename) 
	 
	
# def get_e_invoice_attachments(invoices):
# 	attachments = frappe.get_all(
# 		"File",
# 		fields=("name", "file_name", "attached_to_name", "is_private"),
# 		filters={"attached_to_name": ("in", invoices), "attached_to_doctype": "Lead"},
# 	)
# 	return attachments



# def download_zip(files, output_filename):
# 	import zipfile

# 	zip_stream = io.BytesIO()
# 	with zipfile.ZipFile(zip_stream, "w", zipfile.ZIP_DEFLATED) as zip_file:
# 		for file in files:
# 			file_path = frappe.utils.get_files_path(file.file_name, is_private=file.is_private)

# 			zip_file.write(file_path, arcname=file.file_name)

# 	frappe.local.response.filename = output_filename
# 	frappe.local.response.filecontent = zip_stream.getvalue()
# 	frappe.local.response.type = "download"
# 	zip_stream.close()



