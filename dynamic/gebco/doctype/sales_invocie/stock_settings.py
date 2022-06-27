from email import message
from pickletools import read_uint1
import frappe
from frappe import _ 
from collections import Counter
from functools import reduce
from operator import add
#this fuction caculate all shoratge stock item and msg print all aitem with shorage amount to wharehousr 

# function tak items as list of dic
#  and wharehouse

def validate_sql(out) :
    if len(out) > 0 :
        return out[0].get("actual_qty")
    else: return 0 
def get_item_availabel_stock_with_warehouse(item) :
    
    main_item = frappe.get_doc("Item" , item.get("item_code"))
    if main_item.is_stock_item == 1 and item.get('warehouse') :
        actual_qty = frappe.db.sql(f"""SELECT actual_qty FROM`tabBin` WHERE 
                item_code ='{item.get("item_code")}' and 
                warehouse='{item.get("warehouse")}'""",as_dict = 1)
        avilable_qty = validate_sql(actual_qty)
        if avilable_qty :
            required_qty = float(item.get("qty") or 0 )
            if float(avilable_qty)  >  required_qty :
                return{}
            if float(avilable_qty) <  required_qty  :
                shortage = float(avilable_qty) - required_qty
                return {item.get("item_code") : shortage  }   
        if not  avilable_qty:
           return {item.get("item_code") : item.get("qty")  }
    if not main_item.is_stock_item   or not  item.get('warehouse'):
        return{}
        
   
    
def caculate_shortage_item(items , wharehouse,*args ,**kwargs ) :
    data =list(map(get_item_availabel_stock_with_warehouse ,items))
    sum_dict = reduce(add, (map(Counter, data)))
    if len(data) > 0 :
        table = "<table>"
        message = ""
        for i ,v in sum_dict.items() :
            #frappe.msgprint(str(i))
            message = message +  "<tr>  <td>" + str(i) +  "<td>" + str(v) +"</td>" + "</tr>" 
        message = message +"</table>"
        frappe.msgprint(message)
    return []