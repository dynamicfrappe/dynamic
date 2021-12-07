import frappe

@frappe.whitelist()
def on_submit (self,fun=''):
    if 'Contracting' not in frappe.get_active_domains():
        return



    for item in self.items :
        if getattr(item,"comparison" , None) and getattr(item,"comparison_item" , None):
            comparison_item = frappe.get_doc("Comparison Item",item.comparison_item)
            comparison_item.purchased_qty = (comparison_item.purchased_qty or 0 ) + item.qty
            comparison_item.remaining_purchased_qty = max(0,(comparison_item.qty or 0 ) - comparison_item.purchased_qty)
            comparison_item.save()















@frappe.whitelist()
def on_cancel (self,fun=''):
    if 'Contracting' not in frappe.get_active_domains():
        return
    for item in self.items :
        
            comparison_item = frappe.get_doc("Comparison Item",item.comparison_item)
            comparison_item.purchased_qty = min(0,(comparison_item.purchased_qty or 0 ) - item.qty)
            comparison_item.remaining_purchased_qty = max(comparison_item.qty,(comparison_item.qty or 0 ) - comparison_item.purchased_qty)
            comparison_item.save()
