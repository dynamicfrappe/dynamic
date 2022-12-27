import frappe

Domains = frappe.get_active_domains()

def setup_ifi():
    create_ifi_scripts()
    # frappe.msgprint('created')

def create_ifi_scripts():
    try: 
        create_lead_script()
    except:
        pass

def create_lead_script():
    if 'Terra' not in Domains:
        name = "Lead-Form"
        if frappe.db.exists("Client Script",name) :
            doc = frappe.get_doc("Client Script",name)
        else :
            doc = frappe.new_doc("Client Script")
            doc.dt      = "Lead"
            doc.view    = "Form"
            doc.enabled = 1
            doc.script = """
                
            frappe.ui.form.on("Lead", {
                refresh(frm){
                    if(!frm.doc.__islocal){
                    frm.add_custom_button(
                    __("New Appointment"),
                    function () {
                    frappe.model.open_mapped_doc({
                        method:"dynamic.api.create_new_appointment_ifi",
                        frm: frm
                    });
                    },
                    __("Create")
                );
                
                    }
                }
            
            });
        """
        doc.save()