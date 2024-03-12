import frappe
from frappe import _

Domains=frappe.get_active_domains()

def validate_delivery_note(self , event):
    if "Qaswaa"  in Domains :
        validtate_items_qty(self)

def validtate_items_qty(self):
    for item in self.items :
        sql = f'''
                SELECT 
                    A.rate 
                FROM
                    `tabDelivery Note Item` A
                INNER JOIN 
                    `tabDelivery Note` B
                ON
                    A.parent = B.name
                WHERE 
                    B.name = '{self.return_against}'
                    AND
                    A.item_code = '{item.item_code}'
                '''
        date = frappe.db.sql(sql , as_dict =1 )            
        if item.qty > 0 :
            frappe.throw(_( f"<b>Qty</b> of item {item.item_code} in row {item.idx} should be smaller than 0"))
        if item.rate != date[0].rate :
            frappe.throw(_( f"<b>Rae</b> of item {item.item_code} in row {item.idx} should be equal {date[0].rate}"))
                 