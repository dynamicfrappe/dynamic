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

def get_product_bundle_items(item_code):
	product_bundle = frappe.qb.DocType("Product Bundle")
	product_bundle_item = frappe.qb.DocType("Product Bundle Item")

	query = (
		frappe.qb.from_(product_bundle_item)
		.join(product_bundle)
		.on(product_bundle_item.parent == product_bundle.name)
		.select(
			product_bundle_item.item_code,
			product_bundle_item.qty,
			product_bundle_item.uom,
			product_bundle_item.description,
		)
		.where(product_bundle.new_item_code == item_code)
		.orderby(product_bundle_item.idx)
	)
	return query.run(as_dict=True)
#ckeck if item is pundel and is complicated 

#check if complicated
def is_product_bundle(item_code) :
	return bool(frappe.db.exists("Product Bundle", {"new_item_code": item_code}))

@frappe.whitelist()
def set_complicated_pundel_list(invoice):
    #frappe.throw("Face One ")
    #clear invocie compicated_pund
    
    invoice.set("compicated_pundel" , [])
    complicated_pundel = []
    for item in invoice.items :
        is_pundel =  bool(frappe.db.exists("Product Bundle", {"new_item_code": item.item_code}))
        if is_pundel :
            items = get_product_bundle_items(item.item_code)
            for i in items :
              com_pundel = bool(frappe.db.exists("Product Bundle", {"new_item_code": i.item_code}))
              # add item to new Child table 
              #  
              # 
              if  com_pundel :
                pundel_data = get_product_bundle_items(i.item_code)
                #check if bundel is three level pundel 
                # throw erro in case of three level 
                com_pundel_items = []
                for it in pundel_data :
                    if bool(frappe.db.exists("Product Bundle", {"new_item_code": it.item_code})) :
                        frappe.throw(f"""_( Parent item {pundel_data} Product Pundel {it.item_code})  Has three level of pundels And max level is Tow""")
                    #set child product conf pundel 
                    # pi_row =invoice.append("compicated_pundel", {})
                    # pi_row.parent_item = i.item_code
                    # pi_row.item_code = it.item_code
                    # pi_row.item_group = it.item_group
                com_pundel_items.append(i)
                pi_row =invoice.append("compicated_pundel", {})
                pi_row.parent_item = item.item_code
                pi_row.item_code = i.item_code
                pi_row.qty = i.qty * item.qty
                pi_row.from_warehouse = item.warehouse

                #pi_row.item_group = it.item_group
            complicated_pundel.append({item.item_code : com_pundel_items})
    frappe.msgprint(str( complicated_pundel))


                 
    pass