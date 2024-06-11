import frappe 

@frappe.whitelist()
def create_domain(*args , **kwargs) :
    if not frappe.db.exists("Domain" , "Ram") :
        ram = frappe.new_doc("Domain")
        ram.domain = "Ram"
        ram.save()
        frappe.db.commit()
        print("Ram Domain added successfully!")

def create_property_setter():
    if not frappe.db.exists("Property Setter", {"name": "item_group_fetch_from"}):
        property_setter = frappe.get_doc({
            "doctype": "Property Setter",
            "name": "item_group_fetch_from",
            "doctype_or_field": "DocField",
            "doc_type": "Target Detail",
            "field_name": "item_group",
            "property": "fetch_from",
            "property_type": "Data",
            "value": "item_code.item_group",
            
        })
        property_setter.insert()
        frappe.db.commit()

    if not frappe.db.exists("Property Setter", {"name": "item_group_in_list_view"}):
        property_setter = frappe.get_doc({
            "doctype": "Property Setter",
            "name": "item_group_in_list_view",
            "doctype_or_field": "DocField",
            "doc_type": "Target Detail",
            "field_name": "item_group",
            "property": "in_list_view",
            "property_type": "Check",
            "value": "0",
        })
        property_setter.insert()
        frappe.db.commit()

        