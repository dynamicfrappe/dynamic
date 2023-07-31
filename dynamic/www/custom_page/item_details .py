

# about.py
import frappe

def get_context(context):
    context.data = frappe.get_doc('Item','Apart0014')
    print('\n\n\n\====>',context,'\n\n\n')
    return context