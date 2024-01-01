import frappe
from frappe import _
from frappe.utils import date_diff , now
DOMAINS = frappe.get_active_domains()


def check_data_remaining():
    if 'Logistics' in DOMAINS: 
        containers = frappe.db.get_list(
                    "PO Container",
                    filters={
                        "status": "Ordered",
                    },
                    pluck = "name")
        print(containers)
        for container in containers :
            container = frappe.get_doc("PO Container" , container)
            if not container.remaining_date :
                differance = date_diff( container.arrived_date ,now() )
                container.remaining_date = f'{differance}' + " days"
                if differance < 0 :
                    container.status = "Overdue"
                container.save()

@frappe.whitelist()
def calculate_payments(quotation):
    if 'Logistics' in DOMAINS:
        sql = f'''
            SELECT SUM(PE.paid_amount) AS sum 
            FROM 
                `tabPayment Entry` PE
            INNER JOIN 
                `tabPayment Entry Reference` PER
            ON
                PE.name = PER.parent
            WHERE
                PER.reference_name = '{quotation}'
                AND 
                PE.docstatus = 1
                '''
        
        data = frappe.db.sql(sql , as_dict = 1)
        if data :
            total_payments = data[0]["sum"]
            if total_payments :
              return total_payments
            
@frappe.whitelist()            
def check_composition_request_with_order(name):
    frappe.db.sql(f""" 
                UPDATE 
                    `tabComposition Request` CR
                SET 
                    CR.status = 'Delivered' 
                WHERE 
                    CR.sales_order = '{name}' 
                    AND
                    CR.docstatus = 1
                """)
    
    frappe.db.sql(f""" 
            UPDATE 
                `tabComposition Order` CO
            SET 
                CO.status = 'Delivered' 
            WHERE 
                CO.sales_order = '{name}' 
                AND
                CO.docstatus = 1
            """)
    
@frappe.whitelist()            
def validate_items():
    selling_settings = frappe.get_single("Selling Settings")
    if not selling_settings.item_group :
        frappe.throw(_("Please set <b>item group</b> in selling settings"))
    return selling_settings.item_group 


@frappe.whitelist()            
def validate_engineering_name():
    selling_settings = frappe.get_single("Selling Settings")
    if not selling_settings.department :
        frappe.throw(_("Please set <b>department</b> in selling settings"))
    return selling_settings.department 

@frappe.whitelist()            
def get_item_price(item):
    selling_settings = frappe.get_single("Selling Settings")
    if not selling_settings.price_list :
        frappe.throw(_("Please set <b>price list</b> in selling settings "))
    sql = f'''
            select 
                price_list_rate 
            from 
                `tabItem Price` 
            where
                item_code = '{item}'
                and 
                price_list = '{selling_settings.price_list}'
            limit 1
            '''
    data = frappe.db.sql(sql , as_dict = 1)
    if data :
        if data[0]["price_list_rate"] :
            return data[0]["price_list_rate"]
        
@frappe.whitelist()
def create_sales_invoice(source_name):
    conservation = frappe.get_doc('Conservation',source_name)
    sales_invoice = frappe.new_doc("Sales Invoice")
    sales_invoice.customer = conservation.customer
    for item in conservation.items :
        sales_invoice.append("items" , {"item_code" : item.item , "rate" : item.rate})
    for item in conservation.service_items :
        sales_invoice.append("items" , {"item_code" : item.item , "rate" : item.rate})
    return sales_invoice
    
