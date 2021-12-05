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
    try :
        print("+ from add script")
        doc = frappe.new_doc("Client Script")
        doc.dt      = "Stock Entry"
        doc.view    = "Form"
        doc.enabled = 1
        doc.script = """
                  frappe.ui.form.on('Stock Entry', {
                            refresh(frm) {
                                // your code here
                                
                                frm.events.set_child_table_fields(frm)
                                
                            } ,
                            set_child_table_fields(frm) {
                                frm.doc.items.forEach((e)=>{
                                    var df = frappe.meta.get_docfield("Stock Entry Detail","comparison_item", e.name);
                                    df.hidden =  !frm.doc.against_comparison;
                                    df.reqd = frm.doc.against_comparison;
                                })
                                
                                    frm.refresh_field("items")
                            } ,
                            against_comparison (frm) {
                                frm.events.set_child_table_fields(frm)
                            },
                            comparison (frm) {
                                
                                frm.doc.items.forEach((e)=>{
                                    var df = frappe.meta.get_docfield("Stock Entry Detail","comparison_item", e.name);
                                    df.get_query = function() {
                                                var filters = {
                                                    comparison: frm.doc.comparison || ''
                                                };

                                                return {
                                                    query: "dynamic.contracting.doctype.stock_entry.stock_entry.get_item_query",
                                                    filters: filters
                                                };
                                            }
                            

                                })

                            },
                            
                    })  
        """
        doc.save()
    except :
        pass





    