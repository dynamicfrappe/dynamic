# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Car(Document):
	pass


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_serial_no_query(doctype, txt, searchfield, start, page_len, filters):
	docname = filters.get("docname") or ""
	return frappe.db.sql(f"""
	select name,item_code from `tabSerial No` where name not in (
		select serial_no from tabCar where docstatus < 2
		and name <> '{docname}'
 		) and( name like '%{txt}%' or item_code like '%{txt}%' )
		limit {start} , {page_len}""")