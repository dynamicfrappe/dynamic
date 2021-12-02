import frappe



@frappe.whitelist()
def get_comparison_data(comparison , *args ,**kwatgs):
    comparison_doc=  frappe.get_doc("Comparison" , comparison)
    #get customer from comparison 
    if comparison_doc.comparison_type == "Direct" :
        customer = comparison_doc.customer

    else :
         customer = comparison_doc.contractor
    #get insurance from comparison
    insurance = float(comparison_doc.insurance_value_rate or 0 )
    delievry_insurance = float(comparison_doc.delevery_insurance_value_rate_ or 0 )
    
    items =[]
    #get comparison item 
    for item in comparison_doc.item :
       

        f = {   "item_code"   : item.clearance_item,
                "item_name"   : item.clearance_item_name ,
                "uom"         : item.uom ,
                "description" : item.clearance_item_description ,
                "current_qty" : item.current_qty ,
                "price" : item.price ,
                "amount" : float(item.price or 0 )  * float(item.current_qty or 0 ) }
        items.append(f)
    
    data = {
        "customer"    : customer , 
        "insurance"   : insurance , 
        "d_insurance" : delievry_insurance ,
        "items"       : items
    }
    return data



@frappe.whitelist()
def get_sales_order_data(order , *args , **kwargs):
    sales_order  = frappe.get_doc("Sales Order" , order)
    customer     = sales_order.customer
    required_by = sales_order.delivery_date
    insurance    =sales_order.down_payment_insurance_rate
    d_insurance  = sales_order.payment_of_insurance_copy
    project      = sales_order.project
    data = {
        "customer"    : customer    ,
        "required_by" : required_by ,
        "insurance"   : insurance   ,
        "d_insurance" : d_insurance ,
        "project"     : project     ,


    }


    return data