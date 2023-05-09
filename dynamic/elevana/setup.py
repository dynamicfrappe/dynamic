import frappe


def install_elevana():
    create_item_script()
    create_sales_order_script()

def create_item_script():
    name = "Item-Form"
    if frappe.db.exists("Client Script", name):
        doc = frappe.get_doc("Client Script", name)
    else:
        doc = frappe.new_doc("Client Script")
        doc.dt = "Item"
        doc.view = "Form"
        doc.enabled = 1
    doc.script = """   
        frappe.ui.form.on('Item', {
            refresh(frm){
                frm.add_custom_button(__("Create item in Shipping"), function() {
                frappe.call({
                method:"dynamic.shipping.api.create_product",
                args:{
                    "product" : frm.doc
                },callback(r){
                    if(r.message){
                        frappe.msgprint(r.message)
                    }
                }
                })
        })
            }
        })
        """
    doc.save()


def create_sales_order_script():
    name = "Sales Order-Form"
    if frappe.db.exists("Client Script", name):
        doc = frappe.get_doc("Client Script", name)
    else:
        doc = frappe.new_doc("Client Script")
        doc.dt = "Sales Order"
        doc.view = "Form"
        doc.enabled = 1
    doc.script = """   
         frappe.ui.form.on('Sales Order', {
            refresh(frm){
                frm.add_custom_button(__("Create Shipping Order"), function() {
                frappe.call({
                method:"dynamic.shipping.api.create_order",
                args:{
                    "doc" : frm.doc
                },callback(r){
                    if(r.message){
                        frappe.msgprint(r.message)
                    }
                }
                })
        })
            }
        })
        """
    doc.save()
