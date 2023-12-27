



import frappe
from frappe import _
from dynamic.qaswaa.controllers.sales_order_api import validate_item_qty_reserved

Domains=frappe.get_active_domains()

def validate_sales_order(self , event):
    if "Qaswaa" in Domains :
        validate_item_qty_reserved(self,event)
    if 'Logistics' in Domains :
        validate_qotation(self)

def on_update_after_submit(self , event):
    if 'Logistics' in Domains :
        check_composition_request_with_order(self)

def validate_qotation(self):
    diable_order_without_quotation = frappe.db.get_single_value("Selling Settings", "diable_order_without_quotation")
    if diable_order_without_quotation == 0 :
        for d in self.get("items"):
            if d.prevdoc_docname:
                validate_total_payment_of_quotation(self , d)
                
    elif diable_order_without_quotation == 1 :
        for d in self.get("items"):
            if not d.prevdoc_docname:
                frappe.throw(_("Item {} must be from quotation").format(d.item_code))
            validate_total_payment_of_quotation(self , d)


def validate_total_payment_of_quotation(self , d):
    quotation = f'''
                SELECT 
                    Q.grand_total
                FROM 
                    `tabQuotation` Q
                WHERE
                    Q.name = '{d.prevdoc_docname}'
                    AND 
                    Q.docstatus = 1
                '''
    grand_total = frappe.db.sql(quotation , as_dict = 1 )
    grand_total_quotation = grand_total[0]["grand_total"]
    allowed_amount = (grand_total_quotation * 15) / 100 
    if grand_total_quotation :             
        sql = f'''
                SELECT 
                    SUM(PE.paid_amount) as sum
                FROM 
                    `tabPayment Entry` PE
                INNER JOIN 
                    `tabPayment Entry Reference` PER
                ON 
                    PE.name = PER.parent 
                WHERE 
                    PER.reference_name = '{d.prevdoc_docname}' 
                    AND 
                    PE.docstatus = 1
            '''
        data = frappe.db.sql(sql , as_dict = 1)
        total_paid_amout = data[0]["sum"]
        if not total_paid_amout :
            frappe.throw("30% of quotion must be paid")
        if not (total_paid_amout >= allowed_amount):
            frappe.throw("Total paid amount must be bigger than or eqal 30% of quotation total")

def check_composition_request_with_order(self):
    frappe.db.sql(f""" 
                UPDATE 
                    `tabComposition Request` CR
                SET 
                    CR.status = 'Delivered' 
                WHERE 
                    CR.sales_order = '{self.name}' 
                    AND
                    CR.docstatus = 1
                """)