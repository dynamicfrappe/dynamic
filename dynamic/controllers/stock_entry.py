


import frappe
from frappe import _
from dynamic.api import get_allowed_stoc_use_submit
DOMAINS = frappe.get_active_domains()


def before_save_stock_entry(doc, *args, **kwargs):
	if "WEH" in DOMAINS:
		...
		# get_allowed_stoc_use_submit(doc,doc.get("from_warehouse"))





def update_target_warehouse(doc, *args, **kwargs):
	if "WEH" in DOMAINS:
		for row in doc.items:
			row.warehouse = doc.set_warehouse
		frappe.db.commit()


def validate(self , event):
    if "Stock Reservation" in DOMAINS :
        validate_item(self)



def validate_item(self):
    purpose = frappe.db.get_value("Stock Entry Type", self.stock_entry_type , fieldname = ['purpose'])
    if purpose == "Material Issue" or purpose == "Material Transfer":
        items = self.get("items")
        for item in items:
            qty = get_all_qty_reserved(item.item_code, item.s_warehouse)
            if item.qty > qty:
                wanted_qty = float(item.qty) - float(qty)
                message = f"""
                    Item Name <b>{item.item_code} </b> in row <b>{item.idx}</b> Over Quantity <b>{wanted_qty}</b><br>
                    """
                frappe.throw(message)


		

def get_all_qty_reserved (item_code, warehouse):
    item_reserved = frappe.db.sql("""
    SELECT
        SUM(`reserved_qty`) as reserved_qty
    FROM 
        `tabStock Reservation Entry`
    WHERE
        `item_code` = %s 
        AND `warehouse` = %s
    """, (item_code, warehouse), as_dict=1)
    qty_reserved = item_reserved[0]['reserved_qty']


    item_delivered = frappe.db.sql("""
    SELECT
        SUM(`delivered_qty`) as delivered_qty
    FROM 
        `tabStock Reservation Entry`
    WHERE
        `item_code` = %s 
        AND `warehouse` = %s
    """, (item_code, warehouse), as_dict=1)
    qty_delivered = item_delivered[0]['delivered_qty']

    actual_qty = (qty_reserved if qty_reserved else 0 ) - (qty_delivered if qty_delivered else 0)

    bin_qty = frappe.db.get_value("Bin" , filters={"item_code":item_code, "warehouse":warehouse} , fieldname = 'actual_qty')
    total = bin_qty - actual_qty
    return total
