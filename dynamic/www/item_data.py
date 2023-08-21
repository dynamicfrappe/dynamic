

import frappe
from frappe import _
from frappe.utils import get_host_name, escape_html
no_cache = 1
import urllib 
server_url = get_host_name() #'10.0.0.13:8000'

@frappe.whitelist(allow_guest=False)
def get_context(context):
    # if not frappe.session.user:
    code = frappe.form_dict.item_code
    item_code = escape_html_show(code)
    item_doc = frappe.get_doc('Item',item_code)
    img_link = get_image_link(item_code)
    server_url = get_host_name() #'10.0.0.13:8000' # get_host_name()
    img_link =  f'http://{server_url}{img_link}'
    print('\n\n\n---img_link->',img_link,'\n\n\n')
    item_price, price_list = get_item_price(context.item_code)
    item_doc.description = f"{item_doc.item_name} - {item_doc.size or 'None Size'}  - {item_doc.color  or 'None Color'} - " + item_doc.description
    item_doc.price_list = price_list
    context.item_doc = item_doc
    context.img_link = img_link if img_link else '/assets/dynamic/images/cocaola.jpg'
    context.item_price = item_price or 0
    context.qty = get_item_stock(context.item_code) or 0
    # server_url = get_host_name()#frappe.local.conf.host_name or frappe.local.conf.hostname
    return context

def escape_html_show(text):
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
        ";": " ",
	}

	return "".join(html_escape_table.get(c, c) for c in text)

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

@frappe.whitelist()
def encode_item_data(doc):
    
    import urllib.parse
    
    item_code = doc.name
    item_code_55 = escape_html_demo(doc.name)
    # item_url = urllib.parse.quote(item_code)
    server_url = get_host_name()#'10.0.0.13:8000' # get_host_name()
    return f'http://{server_url}/item_data?item_code={item_code_55}'

@frappe.whitelist()
def test_encode_item_data(doc):
    
    import urllib.parse
    
    item_code = doc.name
    item_code_55 = escape_html_demo(doc.name)
    # item_url = urllib.parse.quote(item_code)
    server_url = get_host_name()#'10.0.0.13:8000' # get_host_name()
    img_link = get_image_link(item_code)
    img_link =  f'http://{server_url}{img_link}'
    return {'url':f'http://{server_url}/item_data?item_code={item_code_55}','image_link':img_link}

def get_image_link(item_code):
    imag_link =  frappe.db.get_value('File', {'attached_to_doctype': 'Item','attached_to_name': item_code}, ['file_url'])
    if not imag_link:
        imag_link =  frappe.db.get_value('File', {'attached_to_doctype': 'Stock Settings','attached_to_name': 'Stock Settings'}, ['file_url'])
    return imag_link or ''

def get_item_price(item_code):
    item_price = 0
    price_list =None
    price_list = frappe.db.get_single_value('Stock Settings','price_list')
    if price_list:
        item_price = frappe.db.get_value('Item Price',{'item_code':item_code,'price_list':price_list,'selling':1},'price_list_rate')
    return [item_price,price_list]

def get_item_stock(item) :
    warehouse  = frappe.db.get_single_value('Stock Settings','warehouse')
    qty=0
    if warehouse:
        qty = frappe.db.sql(f""" SELECT SUM(actual_qty-reserved_qty) as qty FROM `tabBin` WHERE item_code ='{item}' and warehouse='{warehouse}'""",as_dict=1)
        if qty and len(qty) > 0 :
            qty= qty[0].get("qty")
        return qty