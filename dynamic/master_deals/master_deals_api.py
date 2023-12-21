


import frappe
from frappe import _
from frappe.utils.user import get_users_with_role
from erpnext import get_default_company
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe import _
from erpnext.controllers.queries import get_fields
from frappe.utils import get_host_name, escape_html,get_url
from erpnext.accounts.doctype.pos_invoice.pos_invoice import get_bin_qty




DOMAINS = frappe.get_active_domains()


@frappe.whitelist()
def alert_cheque_date():
	if "Cheques" in DOMAINS:
		company = get_default_company()
		get_role= frappe.db.get_value("Company",company,"notification_cheque_role")
		if  (get_role):
			cheque_data = frappe.db.sql("""
			SELECT cheque_no,cheque_date 
			FROM `tabCheque Table` 
			WHERE cheque_date < CURDATE() AND (DATE_ADD(cheque_date, INTERVAL 2 DAY)=CURDATE());
			""",as_dict=1)
			cheque_list = [row['cheque_no'] for row in cheque_data]
			msg = cheque_list
			subject="Cheque Notification"
			# send_mail_by_role(get_role,msg,subject)
			sender = frappe.session.user
			recip_list = get_users_with_role(get_role)
			subject = f"Alert For all Cheque Should Be Paid in 2 Days : {cheque_list}"
			get_alert_dict(company,sender,recip_list,subject)

# @frappe.whitelist()
def send_mail_by_role(role,msg,subject):
	try:
		recip_list = get_users_with_role(role)
		if recip_list:
			email_args = {
				"recipients": recip_list,
				"sender": None,
				"subject": subject,
				"message":msg,
				"now": True
			}
			if not frappe.flags.in_test:
				frappe.enqueue(method=frappe.sendmail, queue="short", timeout=500, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
			return email_args
	except Exception as ex:
		print("exception",str(ex))

		
@frappe.whitelist()
def get_alert_dict(doc,sender,reciever,subject,**kwargs):
	for user in reciever:
		notif_doc = frappe.new_doc('Notification Log')
		notif_doc.subject = subject
		notif_doc.for_user = user
		notif_doc.type = "Alert"
		notif_doc.document_type = ""
		notif_doc.document_name = ''#self.name
		notif_doc.from_user = frappe.session.user or sender
		notif_doc.insert(ignore_permissions=True)





# @frappe.whitelist()
# # @frappe.validate_and_sanitize_search_inputs
# def get_supplier_by_code(doctype, txt, searchfield, start, page_len, filters):
#     frappe.throw("test")
#     sales_order = filters.get("sales_order") or ''
#     search_txt = "%%%s%%" % txt

#     return frappe.db.sql(f"""select item.name , item.item_name
#                     from tabItem item
#                     inner join `tabSales Order Item` child
#                         on  child.item_code = item.name
#                     where child.parent = '{sales_order}'
#                     and (item.name like '{search_txt}' or item.item_name like '{search_txt}' )""")





@frappe.whitelist()
def get_supplier_by_code(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	doctype = "Supplier"
	supp_master_name = frappe.defaults.get_user_default("supp_master_name")
	# frappe.throw("test55")
	fields = ["name"]
	if supp_master_name != "Supplier Name":
		fields.append("supplier_name")

	fields = get_fields(doctype, fields)
	fields.append('supplier_code')
	return frappe.db.sql(
		"""select {field} from `tabSupplier`
		where docstatus < 2
			and ({key} like %(txt)s
			or supplier_name like %(txt)s or supplier_code like %(txt)s)
			  and disabled=0
			and (on_hold = 0 or (on_hold = 1 and CURDATE() > release_date))
			{mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, supplier_name), locate(%(_txt)s, supplier_name), 99999),
			idx desc,
			name, supplier_name
		limit %(start)s, %(page_len)s """.format(
			**{"field": ", ".join(fields), "key": searchfield, "mcond": get_match_cond(doctype)}
		),
		{"txt": "%%%s%%" % txt, "_txt": txt.replace("%", ""), "start": start, "page_len": page_len},
		as_dict=as_dict,
	)



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def customer_query_custom(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	# frappe.throw("test")ظ
	doctype = "Customer"
	conditions = []
	cust_master_name = frappe.defaults.get_user_default("cust_master_name")

	fields = ["name"]
	if cust_master_name != "Customer Name":
		fields.append("customer_name")

	fields = get_fields(doctype, fields)
	searchfields = frappe.get_meta(doctype).get_search_fields()
	searchfields.append('customer_code')
	searchfields = " or ".join(field + " like %(txt)s" for field in searchfields)

	return frappe.db.sql(
		"""select {fields} from `tabCustomer`
		where docstatus < 2
			and ({scond}) and disabled=0
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, customer_name), locate(%(_txt)s, customer_name), 99999),
			idx desc,
			name, customer_name
		limit %(start)s, %(page_len)s""".format(
			**{
				"fields": ", ".join(fields),
				"scond": searchfields,
				"mcond": get_match_cond(doctype),
				"fcond": get_filters_cond(doctype, filters, conditions).replace("%", "%%"),
			}
		),
		{"txt": "%%%s%%" % txt, "_txt": txt.replace("%", ""), "start": start, "page_len": page_len},
		as_dict=as_dict,
	)


@frappe.whitelist()
def get_options(doc, arg=None):
	if frappe.get_meta('Sales Invoice').get_field("naming_series"):
		return frappe.get_meta('Sales Invoice').get_field("naming_series").options
	

def deals_after_insert(doc,*args,**kwargs):
	if 'Master Deals' in DOMAINS:
		if doc.attached_to_doctype == 'Item' and doc.attached_to_name != None:
			item_attach = frappe.db.get_list('File',
			filters={
				'attached_to_doctype': 'Item',
				'attached_to_name': doc.attached_to_name,
			},
			fields=['name'],)
			if len(item_attach) == 1:
				frappe.db.set_value('Item',doc.attached_to_name,'image',doc.file_url)


@frappe.whitelist()
def QRcode_Customer_data(doc):
	server_url = get_host_name() #'192.168.1.11' #
	customer_name=doc.name
	return f'http://{server_url}/app/customer/{customer_name}'
	
	
def escape_html_demo(text):
	if not isinstance(text, str):
		return text

	html_escape_table = {
		"&": "&amp;",
		'"': "&quot;",
		"'": "&apos;",
		">": "&gt;",
		"<": "&lt;",
        "+": "&amp;",
        # " ": "%20",
        " ": ";",
	}

	return "".join(html_escape_table.get(c, c) for c in text)


# @frappe.whitelist()
# def create_cst(cst_name):
# 	new_doc = frappe.new_doc('Sales Invoice')
# 	new_doc.customer = cst_name
# 	new_doc.run_method("set_missing_values")
# 	print(f'\n\n=new_doc=>{new_doc.__dict__}')
# 	print(f'\n\n=new_doc=>{new_doc.name}')
	
# 	return new_doc.name /home/beshoy/Dynamic-13/tera/frappe-tera/apps/dynamic/dynamic/master_deals/master_deals_api.py



def delivery_note_validate_item_qty(doc,*args):
	if 'Master Deals' in DOMAINS:
		for item in doc.items:
			act_qty = get_bin_qty(item.item_code,item.warehouse)
			reqd_qty = float(item.qty or 0) *float(item.conversion_factor or 1)
			if float(act_qty)<float(reqd_qty) :
				frappe.throw(_(f"Item '{item.item_code}'  Has No Qty In Warehouse '{item.warehouse}'"))

def stock_entry_validate_item_qty(doc,*args):
	if 'Master Deals' in DOMAINS:
		entry_type = frappe.get_doc("Stock Entry Type" ,doc.stock_entry_type)
		if entry_type.purpose in ["Material Issue" , "Material Transfer" , 
			   						 "Material Transfer for Manufacture" , "Send to Subcontractor"] :
			for item in doc.items:
				act_qty = get_bin_qty(item.item_code,item.s_warehouse)
				reqd_qty = float(item.qty or 0) *float(item.conversion_factor or 1)
				if float(act_qty)<float(reqd_qty) :
					frappe.throw(_(f" <b>Item '{item.item_code}'</b>  hasn't this qty in warehouse <b>'{item.s_warehouse}'</b>"))
