import frappe
import json
import requests
@frappe.whitelist()
def post_sales_invoice(invoice_name):
    try:
        result = frappe.db.sql("""
            SELECT  `tabCustomer`.customer_name AS receivername ,
		        `tabCustomer`.name as receiver ,
				`tabCustomer`.receiver_type as receiver_type  ,
				`tabCustomer`.country_code as country_code ,
				`tabCustomer`.regioncity as regioncity ,
				'i' as document_type,
				`tabCustomer`.governate  as governate,
				`tabCustomer`.street  as street, 
				`tabSales Invoice`.datetime_issued as datetime_issued ,
				`tabSales Invoice`.name as internalid , 
				`tabSales Invoice`.taxable_item AS taxable_item ,
				`tabCustomer`.buildingnumber as buildingnumber ,
				`tabCustomer`.branchid as branchid ,
				`tabCustomer`.receiver_id AS receiverid,
				 'items' as items   
				 FROM `tabSales Invoice`
				 inner join `tabCustomer`  
				 ON `tabSales Invoice`.customer = `tabCustomer`.name 
				 WHERE `tabSales Invoice`.name ='%s'
        """%invoice_name,as_dict=1)

        ####### get invoice items ###############33
        items = frappe.db.sql("""
            SELECT 
			item_code ,description ,uom ,item_type ,qty ,rate ,discount_amount,item_tax_template
		 from `tabSales Invoice Item` WHERE parent = '%s'
        """%invoice_name,as_dict=1)
        result[0]["items"]=items

        ########## get server url ############
        server_url = frappe.db.get_single_value('EInvoice Setting', 'url')
        if not server_url:
            frappe.throw("You Must Enter Server Url in E Invoice Setting")
        api_url = "/api/recive_invoice_data"
        full_url = str(server_url)+str(api_url)
        r = requests.post(
             full_url,
            data=json.dumps(result)
        )
        if r.status_code==200:
            print("200 from if")
            sql = """update `tabSales Invoice` set is_send=1 where name='%s'"""%invoice_name
            print("sqlllllllllllllll",sql)
            frappe.db.sql("""update `tabSales Invoice` set is_send=1 where name='%s'"""%invoice_name)
            frappe.db.commit()
            frappe.msgprint("Invoice Send Successfully")
        else:
            frappe.msgprint("Failed To Send Invoice")
    except Exception as e:
        frappe.local.response["message"] = str(e)
        frappe.local.response['http_status_code'] = 400
