import frappe

@frappe.whitelist()
def on_submit (self,fun=''):
    if 'Contracting' not in frappe.get_active_domains():
        return



    for item in self.items :
        if getattr(item,"comparison" , None) and getattr(item,"comparison_item" , None):
            frappe.db.sql(f"""
            update `tabComparison Item` set purchased_qty = LEAST(qty,purchased_qty + {item.qty}) , remaining_purchased_qty = qty - LEAST(qty,purchased_qty + {item.qty})
            where name = '{item.comparison_item}'
            """)
        frappe.db.commit()













@frappe.whitelist()
def on_cancel (self,fun=''):
    if 'Contracting' not in frappe.get_active_domains():
        return
    for item in self.items :
        if getattr(item,"comparison" , None) and getattr(item,"comparison_item" , None):
            frappe.db.sql(f"""
            update `tabComparison Item` set purchased_qty = GREATEST(0,purchased_qty - {item.qty}) , remaining_purchased_qty = qty - GREATEST(0,purchased_qty - {item.qty})
            where name = '{item.comparison_item}'
            """)
        frappe.db.commit()
