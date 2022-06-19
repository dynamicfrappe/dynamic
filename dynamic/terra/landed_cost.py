import frappe
from frappe import _

#cacluate rate and tax rescharges
#this function 
# caculate item Percent From The invoice total
# to Get the tax Amount Per every Line 
# the function should handel ame item if it added twice to the landed Cost voucher
def get_purchase_rate_in_supplier_currency( item , document_type  , document  ,line_name):
    if document_type == "Purchase Invoice" :
        # 1- Get Tax Templates rate 
        # 2 - if tax is on item 
        # 3 - get tax from item Line  
        # 4 if tax On the Invocie Caculet The item Percent From invocie To get Item Percent From tax
        purchase_tax = 0 
        # get Item data From item line 
        item_data = frappe.db.sql(f""" SELECT  item_tax_template as tax  , rate  FROM `tabPurchase Invoice Item` WHERE 
        name = '{line_name}'""" ,as_dict =1)
        if item_data and len(item_data) > 0 :
            if item_data[0].get('tax') :
                pass
            return item_data[0].get('rate')
        


    
    if document == "Purchase Receipt" :
        print("Purchase Invoice")

@frappe.whitelist()
def validate_cost(self , *args , **kwargs):
    for item in self.items :
        item.rate_currency = get_purchase_rate_in_supplier_currency(item.item_code ,
                                                               item.receipt_document_type , 
                                                               item.receipt_document ,
                                                               item.purchase_receipt_item
                                                               )

        #frappe.utils.fmt_money(item.rate_currency_price, currency="USD")