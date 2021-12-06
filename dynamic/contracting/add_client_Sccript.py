import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def add_sales_order_script():
	try :
		print("+ from add script")
		doc = frappe.new_doc("Client Script")
		doc.dt      = "Sales Order"
		doc.view    = "Form"
		doc.enabled = 1
		doc.script = """
					  
				frappe.ui.form.on('Sales Order', {
				refresh(frm) {
					frm.set_query("comparison", function(){
						return {
							filters : {
								"tender_status": ["in", ["Approved"]]
							}
						};
					});
					if(frm.doc.docstatus==1){
					frm.add_custom_button(__("create Clearence"), function() {
						frappe.model.open_mapped_doc({
					method: "dynamic.contracting.add_client_Sccript.make_clearence",
					frm:frm //this.frm
					})
					})
					}
				}
			})
	
		"""
		doc.save()
	except :
		pass

	try:
		print("+ from add script")
		doc = frappe.new_doc("Client Script")
		doc.dt = "Stock Entry"
		doc.view = "Form"
		doc.enabled = 1
		doc.script = """
			  frappe.ui.form.on('Stock Entry', {
						refresh(frm) {
							// your code here
	
							frm.events.set_child_table_fields(frm)
	
						} ,
						set_child_table_fields(frm) {
							frm.doc.items.forEach((e)=>{
								var df = frappe.meta.get_docfield("Stock Entry Detail","comparison_item", e.name);
								df.hidden =  !frm.doc.against_comparison;
								df.reqd = frm.doc.against_comparison;
							})
	
								frm.refresh_field("items")
						} ,
						against_comparison (frm) {
							frm.events.set_child_table_fields(frm)
						},
						comparison (frm) {
	
							frm.doc.items.forEach((e)=>{
								var df = frappe.meta.get_docfield("Stock Entry Detail","comparison_item", e.name);
								df.get_query = function() {
											var filters = {
												comparison: frm.doc.comparison || ''
											};
	
											return {
												query: "dynamic.contracting.doctype.stock_entry.stock_entry.get_item_query",
												filters: filters
											};
										}
	
	
							})
	
						},
	
				})  
		"""
		doc.save()
	except:
		pass


@frappe.whitelist()
def make_clearence(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		set_missing_values(source, target)

	def set_missing_values(source, target):
		target.flags.ignore_permissions = True
		target.update({'clearance_type': "Outcoming"})
		target.update({'purchase_taxes_and_charges_template':source.taxes_and_charges})
		target.update({'total_after_tax':source.grand_total})

	doclist = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Clearance",
			# "field_map": {
			# 	"customer": "customer",
			# },
		},
		"Sales Order Item": {
			"doctype": "Clearance Items",
			"field_map": {
				"item_code":"clearance_item",
				"rate":"price",
				"qty":"qty",
				"qty":"current_qty",
				"amount":"total_price",
				"uom":"uom"
			},
			"add_if_empty": True
		},
		"Sales Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges Clearances",
			"field_map": {
				"charge_type": "charge_type",
				# "account_head": "account_head",
				# "description":"description"
			},
			"add_if_empty": True
		},
	}, target_doc,postprocess, ignore_permissions=ignore_permissions)

	return doclist
