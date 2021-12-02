import frappe


@frappe.whitelist()
def add_sales_order_script():
    try :
        print("+ from add script")
        doc = frappe.new_doc("Client Script")
        doc.dt      = "Sales Order"
        doc.view    = "Form"
        doc.enabled = 1
        doc.script = """
                    frappe.ui.form.on('Sales Order', {
                    refresh(frm) {
                        frm.set_query("comparison", function(){
                            return {
                                filters : {
                                    "tender_status": ["in", ["Approved"]]
                                }
                            };
                        });
                        if(!frm.doc.__islocal){
                        frm.add_custom_button(__("create Clearence"), function() {
                            console.log("fom s order")
                        })
                        }
                    }
                })
        """
        doc.save()
    except :
        pass