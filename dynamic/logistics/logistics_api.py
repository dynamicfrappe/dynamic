import frappe
from frappe import _
from frappe.utils import date_diff , now , add_days , getdate
DOMAINS = frappe.get_active_domains()

def check_data_remaining():
    if 'Logistics' in DOMAINS: 
        containers = frappe.db.get_list(
                    "PO Container",
                    filters={
                        "status": "Ordered",
                    },
                    pluck = "name")
        for container in containers :
            container = frappe.get_doc("PO Container" , container)
            if not container.remaining_date :
                differance = date_diff( container.arrived_date ,now() )
                container.remaining_date = f'{differance}' + " days"
                if differance < 0 :
                    container.status = "Overdue"
                container.save()

def validate_so():
    sql1 = f'''
        SELECT 
            SO.name 
        FROM
            `tabSales Order` SO
        WHERE 
            DATE(SO.valid_until) < DATE('{getdate(now())}')
            and
            SO.advance_paid < (SO.grand_total * 30 )/100
        '''
    data = frappe.db.sql(sql1, as_dict=1)
    if data :
        for entry in data :   
            sql1 = f'''
                SELECT 
                    SI.name 
                FROM
                    `tabSales Invoice Item` SI
                WHERE 
                    SI.sales_order = '{entry["name"]}'
                '''
            sales_invoice_item = frappe.db.sql(sql1 , as_dict = 1)
            if not sales_invoice_item :
                sales_order = frappe.get_doc("Sales Order" , entry["name"])
                for item in sales_order.items :
                    if item.serial_number != 'None' :
                        # frappe.db.set_value('Serial No',item.serial_number,'customer','')
                        # frappe.db.set_value('Serial No',item.serial_number,'customer_name','')
                        frappe.db.sql(f""" UPDATE `tabSerial No` s
                                    SET 
                                        customer = "" ,
                                        customer_name = ""
                                    WHERE
                                      s.name = '{item.serial_number }'
                                      and 
                                      item_code = '{item.item_code}' 
                                      and
                                       customer = '{sales_order.customer}' """)

# def validate_so():
#     if "Logistics" in DOMAINS:
#         sql = f'''
#             SELECT 
#                 SO.name 
#             FROM
#                 `tabSales Order` SO
#             WHERE 
#                 DATE(SO.valid_until) > DATE({now()})
#             '''
#         data = frappe.db.sql(sql , as_dict = 1)
#         frappe.throw(str(data))
        # threshod_date =  add_days(now(), -7)
        # sales_orders = frappe.db.get_list(
        #             "Sales Order",
        #             filters={
        #                 "creation": ["<=" , threshod_date] , "docstatus" : 1,
        #             },
        #             pluck = "name")
        # for sales_order in sales_orders :
        #     s_order = frappe.get_doc("Sales Order" , sales_order)
        #     s_order.docstatus = 2
        #     s_order.save()


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
def get_maintenance_item(doc , name):
    conservation_requestes = frappe.get_all("Conservation Request" ,
                                       filters = {"docstatus" : 1} , pluck = "name") 
    conservation_request = frappe.get_doc("Conservation Request"  , name)
    for req in conservation_requestes :
        conservation_request.append("maintenance" , {"conservation_request" : req})

    # selling_settings = frappe.get_single("Selling Settings")
    # if not selling_settings.item_group :
    #     frappe.throw(_("Please set <b>item group</b> in selling settings"))
    # return frappe.throw(str(conservation_requestes))


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
    sales_invoice.update_stock = 1

    all_items = conservation.items + conservation.service_items
    for item in all_items :
        temp = frappe.get_doc("Item" , item.item)
        sales_invoice.append("items" , {"item_code" : item.item , "rate" : item.rate , "description": temp.description , 'item_name': temp.item_name , 'uom': temp.stock_uom , 'qty' :1 , })
    if conservation.service_items :
        selling_settings = frappe.get_single("Selling Settings")
        if not selling_settings.account :
           frappe.throw(_("Please set <b>account</b> in selling settings to fetch in account head in taxes"))
        for item in conservation.service_items :
            sales_invoice.append("taxes" , {"charge_type" : "Actual" ,
                                            "account_head" :selling_settings.account ,"rate" : item.rate})
    sales_invoice.total = conservation.total_cost
    return sales_invoice

@frappe.whitelist()
def create_stock_entry_from_conservation(source_name):
    conservation = frappe.get_doc('Conservation',source_name)
    stock_entry = frappe.new_doc("Stock Entry")
    stock_entry.stock_entry_type = "Matrial Issue"
    for item in conservation.items:
        temp = frappe.get_doc("Item" , item.item  )
        stock_entry.append("items" , {"item_code" : item.item , "basic_rate" : item.rate , 'qty' : 1 , 'uom': temp.stock_uom , 'description': temp.description , 'item_group': temp.item_group , 'item_name': temp.item_name})
    return stock_entry

@frappe.whitelist()
def get_serial_no(item_code):
    list = []
    sql =f'''
        SELECT 
            S.name
        FROM
            `tabSerial No` S
        WHERE
            S.item_code = '{item_code}'
            AND
            S.customer = '' 
        '''
    data = frappe.db.sql(sql , as_dict = 1)
    if data :
        for row in data :
            list.append(row["name"])

        return list


@frappe.whitelist()
def create_composition_request(source_name):
    sales_order = frappe.get_doc('Sales Order',source_name)
    composition_request = frappe.new_doc("Composition Request")
    composition_request.sales_order = sales_order.name
    composition_request.customer = sales_order.customer
    composition_request.items = sales_order.items
    composition_request.set_address_and_numbers()
    return composition_request



@frappe.whitelist()
def create_request_item_opportunity(source_name)  :
    return create_request_item(source_name  ,doctype ='Opportunity')
@frappe.whitelist()
def create_request_item_lead(source_name)  :
    return create_request_item(source_name  ,doctype ='Lead')
@frappe.whitelist()
def create_request_item_customer(source_name)  :
    return create_request_item(source_name  ,doctype ='Customer')
@frappe.whitelist()
def create_request_item(source_name  ,doctype = None):
    # opportunity = frappe.get_doc('Opportunity',source_name)
    request_item = frappe.new_doc("Request Editing Item")
    request_item.link_type = doctype
    request_item.opportunity = source_name
    return request_item


@frappe.whitelist()
def create_stock_entry(source_name):
    request_item = frappe.get_doc('Request Editing Item',source_name)
    stock_entry = frappe.new_doc("Stock Entry")
    stock_entry.request_editing_item = request_item.name
    stock_entry.stock_entry_type = "Repack"
    stock_entry.from_warehouse = request_item.source_warehouse
    stock_entry.to_warehouse = request_item.target_warehouse
    for item in request_item.main_item:
        stock_entry.append("items" ,{
            "item_code" : item.item_code ,
            "qty" : item.reqd_qty,
            "s_warehouse" : request_item.source_warehouse,
            # "t_warehouse" : request_item.target_warehouse,
        })
    for item in request_item.spear_part_item:
        stock_entry.append("items" ,{
            "item_code" : item.item_code ,
            "qty" : item.reqd_qty,
            "s_warehouse" : request_item.source_warehouse,
            # "t_warehouse" : request_item.target_warehouse,
        })
    stock_entry.append("items" ,{
            "item_code" : request_item.item_code ,
            "qty" : float(1),
            # "s_warehouse" : request_item.source_warehouse,
            "t_warehouse" : request_item.target_warehouse,
        })
    return stock_entry

@frappe.whitelist()
def create_contact(name , type , contact):
    sql = f'''
        SELECT 
            C.name 
        FROM 
            `tabContact` C 
        INNER JOIN
            `tabDynamic Link` D
        ON
            C.name = D.parent
        WHERE 
            D.link_doctype = "Lead"
            AND 
            D.link_name = '{name}' 
            '''
    data = frappe.db.sql(sql , as_dict = 1)
    contact_doc = frappe.get_doc("Contact" , data[0]["name"])
    if type == "Email":
        contact_doc.append("email_ids" , {"email_id" : contact})
    if type == "Phone" :
        contact_doc.append("phone_nos" , {"phone" : contact})
    contact_doc.save()

@frappe.whitelist()
def validate_sales_order_items(item):
    sql = f'''
        SELECT 
            I.has_serial_no
        FROM 
            `tabItem` I
        WHERE
            I.has_serial_no  
            AND 
            I.name = '{item}'
        '''
    data = frappe.db.sql(sql , as_dict = 1)
    if data:
        return True
    

@frappe.whitelist()
def fetch_serial_numbers(item_code , warehouse , qty):
    sql = f'''
        select 
            name 
        from
            `tabSerial No`
        where
            warehouse = '{warehouse}'
            and
            item_code = '{item_code}'
            limit {qty}
        '''
    serials = frappe.db.sql(sql , as_dict = 1)
    serial_list = ""
    for serial in serials :
        serial_list +=f"{serial.name} \n"
    
    return serial_list
