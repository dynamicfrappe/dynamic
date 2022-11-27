import frappe




@frappe.whitelist()
def get_iem_sub_uom(item_code,uom,qty):
    item  = frappe.get_doc("Item",item_code)
    if len(item.uoms) >=1:
        if item.uoms[1].uom == uom:
            return {
            "sub_uom":item.uoms[1].uom,
            "sub_uom_conversation_factor":item.uoms[1].conversion_factor,
            "qty_as_per_sub_uom": qty
        }
        return {
            "sub_uom":item.uoms[1].uom,
            "sub_uom_conversation_factor":item.uoms[1].conversion_factor,
            "qty_as_per_sub_uom": float(qty or 0) / float(item.uoms[1].conversion_factor or 0)
        }
    return {
            "sub_uom":"",
            "sub_uom_conversation_factor":0,
            "qty_as_per_sub_uom": 0
        }