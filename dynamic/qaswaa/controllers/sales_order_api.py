






import frappe
from frappe import _
from frappe import _, bold
from erpnext.stock.get_item_details import (
	get_bin_details,
)


#validate_sales_order
def validate_item_qty_reserved(doc,*args,**kwargs):
    msg = ''
    for row in doc.items:
        bin_details = get_bin_details(row.item_code,row.warehouse)
        #{'projected_qty': 20.0, 'actual_qty': 20.0, 'reserved_qty': 0.0}
        print(f'\n\n==>{row.item_code}--{bin_details}\n\n')
        if bin_details.get('actual_qty') - bin_details.get('reserved_qty') < row.qty:
            row.required_qty = abs(row.qty - (bin_details.get('actual_qty') - bin_details.get('reserved_qty')))
            msg += f"""
                    Item Name {bold(row.item_code)} Need Qty {bold(row.required_qty)} <br>
                    """
    if msg:
        frappe.msgprint(_(msg))



