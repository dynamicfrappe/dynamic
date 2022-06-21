import frappe
from frappe import _



DOMAINS = frappe.get_active_domains()
#cacluate rate and tax rescharges
#this function 
# caculate item Percent From The invoice total
# to Get the tax Amount Per every Line 
# the function should handel ame item if it added twice to the landed Cost voucher
def get_purchase_rate_in_supplier_currency( item ,
                         document_type  , document  ,line_name):

    # Function Params 
    # item = item Code
    # document type = [Purchase invocie  , Purchase reciept ]
    # document Name of the Document 
    #line name Purchase Invocie Item line name 
    #
    a_table = '`tabPurchase Invoice`'
    b_table = '`tabPurchase Invoice Item`'
    
    if document_type == "Purchase Receipt" :
       a_table = '`tabPurchase Receipt`'
       b_table = '`tabPurchase Receipt Item`'
        # 1- Get Tax Templates rate 
        # 2 - if tax is on item 
        # 3 - get tax from item Line  
        # 4 if tax On the Invocie Caculet The item Percent From invocie To get Item Percent From tax

    item_data = frappe.db.sql(f""" SELECT   
                                    b.rate  as rate  ,
                                    a.conversion_rate as factor , 
                                    a.currency as currency ,
                                    a.discount_amount as discount_amount,
                                    a.base_discount_amount  ,
                                    a.total_taxes_and_charges as taxes ,
                                    a.total as total 
                                    FROM 
                                    {b_table}  b 
                                    INNER JOIN 
                                    {a_table}  a 
                                    ON b.parent = a.name 
                                    WHERE 
                                    b.name = '{line_name}' 
    """ ,as_dict =1)
    if item_data and len(item_data) > 0 :
    
        #caculet Item Percent From Total Invocie 
            
        item_price = float(item_data[0].get('rate') or 0 )
        total_in_supplier_currency = float(item_data[0].get('total') or 0 )
        #caculate item percint From the invocie to Caculate Tax and Discount Amount
        item_precent = (item_price / total_in_supplier_currency)
        discount_amount = 0
        item_tax = 0
        #caculate total after discount on supplier currencyy 
        if float(item_data[0].get('discount_amount') or 0) > 0  : 
            total_in_supplier_currency = total_in_supplier_currency -float(item_data[0].get('discount_amount') or 0)
            discount_amount = float(item_data[0].get('discount_amount') or 0) * item_precent
            item_price = item_price - discount_amount
        #add Tax amount To item Price If User Dont Use Tax Account 
        # ignored for handel case
        # if float(item_data[0].get("taxes") or 0 ) > 0 :
        #     item_tax = float(item_data[0].get("taxes") or 0 ) * item_precent
        #     item_price = item_price + item_tax
        # check Currency Factor if > 1 Update item
        #if float(item_data[0].get('factor') or 0 ) > 1 :
        data = {
                "rate"     : item_price ,
                "currency" : item_data[0].get("currency")  ,
                "factor"   : item_data[0].get("factor")
                }
       
        return data
    
    

@frappe.whitelist()
def validate_cost(self , *args , **kwargs):
    for item in self.items :
        data = get_purchase_rate_in_supplier_currency(item.item_code ,
                                                    item.receipt_document_type , 
                                                    item.receipt_document ,
                                                    item.purchase_receipt_item
                                                               )
        item.rate_currency     = float(data.get("rate" ) or 0 )
        item.purchase_currency = data.get("currency")
        item.currency          = float( data.get("factor") or 1)
       

        item.item_cost_value = float(item.applicable_charges or 0) / float(item.qty or 1)
        item.item_after_cost =( item.rate_currency *  item.currency ) +item.item_cost_value 



@frappe.whitelist()
def get_query_type (*args,**kwargs):
	return[[ "Purchase Invoice"],["Payment Entry"] ]


@frappe.whitelist()
def get_doctype_info(doc_type , document  ,*args , **kwargs) :
    doc_total = 0 
    unallocate = 0 
    doc= False
    account = ""
    if doc_type == "Purchase Invoice" :
        doc = frappe.db.sql(f""" SELECT SUM(b.base_amount) as total 
           FROM 
         `tabItem` a
          INNER JOIN 
         `tabPurchase Invoice Item` b
          ON a.item_code = b.item_code 
          WHERE
          a.is_stock_item= 0 AND
          b.parent = '{document}'""",as_dict =1)
        
    if doc_type == "Payment Entry" :
        doc=  frappe.db.sql(f""" SELECT unallocated_amount as total FROM
                         `tabPayment Entry` WHERE name = '{document}'""" ,as_dict =1)
    if doc and len(doc) > 0 : 
            if doc[0].get("total") and float(doc[0].get("total") or 0 ) > 0 :
                doc_total = float(doc[0].get("total") )
    old_allocated = 0 
    caculate_old = frappe.db.sql(f""" 
    SELECT SUM(allocated_amount) as allocated FROM `tabLanded Cost Voucher Child` WHERE 
    doc_type ='{doc_type}' and invoice ='{document}'
    """,as_dict =1)
    if caculate_old and len(caculate_old) > 0 :
        old_allocated = float(caculate_old[0].get("allocated") or 0 )
    unallocate = float(doc_total or 0) - float(old_allocated or 0 )
    return ({
        "total" : doc_total  , "allocated" : unallocate
    })

def get_old_laned_cost_ex(line_name , docment_type) :
    amount = frappe.db.sql(""" SELECT SUM(base_amount) as total FROM `tabLanded Cost Taxes and Charges`
       WHERE line_name='{line_name}' and docment_type='{docment_type}'  """,as_dict=1)
    if amount and len(amount) > 0 :
        return float(amount[0].get('total') or 0 )
    else :
        return 0 

@frappe.whitelist()    
def get_line_info( allocated_amount ,doc_type , document ,*args ,**kwargs):
    amount = 0
    allcoated = 0
    if doc_type  == "Payment Entry" :
        return 0
    if doc_type  == "Purchase Invoice" :
        invocie_lines  = []
        line_data = frappe.db.sql(f"""  SELECT b.name ,
                                               b.item_code , 
                                               b.base_amount  ,
                                               b.expense_account
                                        FROM  `tabPurchase Invoice Item`  b
                                        INNER JOIN 
                                        `tabPurchase Invoice` a
                                        INNER JOIN `tabItem`   c 
                                        ON
                                        a.name = b.parent AND b.item_code = c.item_code
                                        WHERE 
                                        c.is_stock_item = 0 AND
                                        b.parent = '{document}' 
                                      """,as_dict =1 )
        if line_data and len(line_data) > 0 :
            for item in line_data:
                old_expens = get_old_laned_cost_ex(item.get("b.name") ,)