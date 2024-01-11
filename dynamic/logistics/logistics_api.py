import frappe
from frappe import _
from frappe.utils import date_diff , now , add_days
from erpnext.accounts.party import get_party_account
from erpnext.controllers.accounts_controller import get_advance_journal_entries, get_advance_payment_entries

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
def create_request_item(source_name):
    opportunity = frappe.get_doc('Opportunity',source_name)
    request_item = frappe.new_doc("Request Editing Item")
    request_item.opportunity = opportunity.name
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
    
# @frappe.whitelist()
# def get_advanced_so_ifi(doc_name):
# 	"""Returns list of advances against Account, Party, Reference"""
# 	self = frappe.get_doc('Sales Order', doc_name)
# 	# frappe.throw(str(self))
# 	res = get_advance_entries(self)
# 	self.set("advancess", [])
# 	# print('\n\n\n-->res:',res)
# 	advance_allocated = 0
# 	for d in res:
# 		if d.against_order:
# 			allocated_amount = flt(d.amount)
# 			d['allocated_amount'] = allocated_amount
# 		else:
# 			if self.get("party_account_currency") == self.company_currency:
# 				amount = self.get(
# 					"base_rounded_total") or self.base_grand_total
# 			else:
# 				amount = self.get("rounded_total") or self.grand_total

# 			allocated_amount = min(amount - advance_allocated, d.amount)
# 			d['allocated_amount'] = allocated_amount
# 		advance_allocated += flt(allocated_amount)
		

# 		# self.append("advancess", advance_row)
# 	# print('\n\n\n-->after update:',res)
# 	return res

# def get_advance_entries(self, include_unallocated=True):
# 	if self.doctype == "Sales Invoice":
# 		party_account = self.debit_to
# 		party_type = "Customer"
# 		party = self.customer
# 		amount_field = "credit_in_account_currency"
# 		order_field = "sales_order"
# 		order_doctype = "Sales Order"
# 	elif self.doctype == "Sales Order":
# 		party_account = get_party_account("Customer", party=self.customer, company=self.company)
# 		party_type = "Customer"
# 		party = self.customer
# 		amount_field = "credit_in_account_currency"
# 		order_field = "sales_order"
# 		order_doctype = "Sales Order"
# 	else:
# 		party_account = self.credit_to
# 		party_type = "Supplier"
# 		party = self.supplier
# 		amount_field = "debit_in_account_currency"
# 		order_field = "purchase_order"
# 		order_doctype = "Purchase Order"

# 	# print('\n\n-->party_type',party_account)
# 	# order_list = list(set(d.get(order_field) for d in self.get("items") if d.get(order_field)))
# 	order_list = [self.name, ]
# 	journal_entries = get_advance_journal_entries(
# 		party_type, party, party_account, amount_field, order_doctype, order_list, include_unallocated
# 	)

# 	payment_entries = get_advance_payment_entries(
# 		party_type, party, party_account, order_doctype, order_list, include_unallocated
# 	)

# 	res = journal_entries + payment_entries

# 	return res