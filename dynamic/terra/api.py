import frappe

from frappe.utils import add_days, nowdate, today


@frappe.whitelist()
def get_iem_sub_uom(item_code,uom,qty):
    item  = frappe.get_doc("Item",item_code)
    # if len(item.uoms) >=1:
    #     if item.uoms[1].uom == uom:
    #         return {
    #         "sub_uom":item.uoms[1].uom,
    #         "sub_uom_conversation_factor":item.uoms[1].conversion_factor,
    #         "qty_as_per_sub_uom": qty
    #     }
    #     return {
    #         "sub_uom":item.uoms[1].uom,
    #         "sub_uom_conversation_factor":item.uoms[1].conversion_factor,
    #         "qty_as_per_sub_uom": float(qty or 0) / float(item.uoms[1].conversion_factor or 0)
    #     }
    # return {
    #         "sub_uom":"",
    #         "sub_uom_conversation_factor":0,
    #         "qty_as_per_sub_uom": 0
    #     }
    for u in item.uoms:
        if u.is_sub_uom:
            if u.uom !=uom:
                return {
                    "sub_uom":u.uom,
                    "sub_uom_conversation_factor":u.conversion_factor,
                    "qty_as_per_sub_uom": float(qty or 0) / float(u.conversion_factor or 0)
                }

            if u.uom == uom :
                return {
                    "sub_uom":u.uom,
                    "sub_uom_conversation_factor":u.conversion_factor,
                    "qty_as_per_sub_uom": qty
                }

    return {
            "sub_uom":"",
            "sub_uom_conversation_factor":0,
            "qty_as_per_sub_uom": 0
        }



# material request type ------------> purchase
# validate if no item   ------------> validation error 
@frappe.whitelist()
def create_sales_order_from_opportunity(source_name, target_doc=None):
    source_doc = frappe.get_doc("Opportunity",source_name)
    doc = frappe.new_doc("Sales Order")
    if source_doc.opportunity_from == "Customer":
        doc.customer = source_doc.party_name
    if len(source_doc.items)> 0:
        for item in source_doc.items:
            item_doc = frappe.get_doc("Item",item.item_code)
            doc.append("items",{
                "item_code"     : item.item_code,
                "qty"           : item.qty,
                "item_name"     : item.item_name,
                "description"   : item.item_name,
                "uom"           : item_doc.stock_uom,
                "stock_uom"     : item_doc.stock_uom
            })

    return doc

@frappe.whitelist()
def create_material_request_from_opportunity(source_name, target_doc=None):
    source_doc = frappe.get_doc("Opportunity",source_name)
    doc = frappe.new_doc("Material Request")
    doc.purpose = "Purchase"
    if len(source_doc.items)> 0:
        for item in source_doc.items:
            item_doc = frappe.get_doc("Item",item.item_code)
            doc.append("items",{
                "item_code"     : item.item_code,
                "qty"           : item.qty,
                "item_name"     : item.item_name,
                "description"   : item.item_name,
                "uom"           : item_doc.stock_uom,
                "stock_uom"     : item_doc.stock_uom,
                "schedule_date" : today()
            })
    return doc


