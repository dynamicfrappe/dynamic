


import frappe 
from frappe import _
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def get_sales_order_items(doc_name,so_name):
	try:
		so_doc = frappe.get_doc("Sales Order",so_name)
		# preparing_containers_doc = frappe.get_doc('Preparing the containers',doc_name)
		return  so_doc.items
	except Exception as er:
		return str(er)
	
@frappe.whitelist()
def create_loading_doc(source_name, target_doc=None, ignore_permissions=True):
	docs = get_mapped_doc(
			"Reservation Is Approved",
			source_name,
			{
				"Reservation Is Approved": {
					"doctype": "Loading Doctype",
					"field_map": {
						"sales_order": "sales_order",
						"customer": "customer",
						"taxes_and_charges": "purchase_taxes_and_charges_template",
					},
					"validation": {
						"docstatus": ["=", 0],
					},
				},
				
			},
			target_doc,
			postprocess=None,
			ignore_permissions=ignore_permissions,
		)
	reservation_approved_doc = frappe.get_doc("Reservation Is Approved",source_name)
	sales_order_doc = frappe.get_doc("Sales Order",reservation_approved_doc.sales_order)
	preparing_containers_doc =  frappe.get_doc("Preparing the containers",reservation_approved_doc.preparing_the_containers)
	docs.items = sales_order_doc.items
	docs.with_a_cover = preparing_containers_doc.with_a_cover

	return docs
	

@frappe.whitelist()
def quality_doc_init(source_name, target_doc=None, ignore_permissions=True):
	docs = get_mapped_doc(
			"Loading Doctype",
			source_name,
			{
				"Loading Doctype": {
					"doctype": "Loading Quality",
					"field_map": {
						"loading_doc": source_name,
						"customer": "customer",
						"loading_date": "loading_date",
						"loading_place": "loading_place",
						"destination": "destination",
						"container_number": "container_number",
						"with_a_cover": "with_a_cover",
					},
					"validation": {
						"docstatus": ["=", 0],
					},
				},
				"Sales Order Item": {
					"doctype": "Sales Order Item",
					# "field_map": {
					# },
				},
				
			},
			target_doc,
			postprocess=None,
			ignore_permissions=ignore_permissions,
		)

	return docs