#validate backed item with 

# 1 - git stock item 
# 2 git single bundle Item 
# 3- git complicated pundel from invocie items 



#solution

# 1 - create child table in sales invoice to set complicated pundel to clear the data 
# doc Tybe name Compicated Pundel 
# fields  = ["Parent Item" , -- > to git parent pundel 
#           "Item Code" , -- > to git current bundel item code 
#            "Item Group" , -- > to br ablicable for commetion template 
#            "From Warehouse" ,  -- > to set the child paked list template 
#            "Qty"  , 
#            "Actual Qty" , -- > add this field if we need it 
#            "Picked Qty" , --> if we need to set 
#               ]

from itertools import product
import frappe 
from frappe import _


#ckeck if item is pundel and is complicated 
def validate_com_pundel(item_code):
    # get pundel _item 
    is_stock_item = frappe.db.sql(f"""SELECT is_stock_item as stock 
                                    FROM `tabItem` WHERE item_code ='{item_code}'""",as_dict=1)
    if is_stock_item and len(is_stock_item) > 0 :
        if is_stock_item[0].get("stock") == '1' :
            return False
    if not is_stock_item :
        frappe.throw("UnKnown Item code {}".format(str(item_code)))
    pundel_name = frappe.db.sql(f""" SELECT name FROM `tabProduct Bundle` 
    WHERE new_item_code  = '{item_code}'
    """ ,as_dict = True)
    if pundel_name and len(pundel_name) > 0 :
            return pundel_name[0].get("name")
    return 0
#check if complicated


@frappe.whitelist()
def set_complicated_pundel_list(invoice):
    #frappe.throw("Face One ")
    complicated_pundel = []
    for item in invoice.items :
        # check if stock Item Pass
        # if sigle pundel pass
        # check If item is pundel of pundel -- > add child pundels 
        is_pundel = validate_com_pundel(item.item_code)
        if is_pundel :
            pass 
    
    pass