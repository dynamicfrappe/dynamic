import frappe


# DOMAINS = frappe.get_active_domains()


def create_sales_invoice_script():
    name = "Sales Invoice-Form"
    if frappe.db.exists("Client Script",name) :
        doc = frappe.get_doc("Client Script",name)
    else :
        doc = frappe.new_doc("Client Script")
    doc.dt      = "Sales Invoice"
    doc.view    = "Form"
    doc.enabled = 1
    doc.script = """
            
        frappe.ui.form.on("Sales Invoice", {
            refresh(frm){
                console.log("refresh functions s s s s ")
                if(frm.doc.__islocal && frm.doc.is_return == 1){
                    frm.events.update_return_account(frm)
                }
            },
            is_return(frm){
                console.log("from return   asd ")
                if(frm.doc.__islocal && frm.doc.is_return == 1){
                    frm.events.update_return_account(frm)
                }
            },
            update_return_account(frm){
                frappe.call({
                        method:'dynamic.api.get_sales_return_account',
                        callback(r){
                            console.log("message =============> ",r.message)
                            if(r.message){
                                for(let i=0;i<frm.doc.items.length;i++){
                                    frm.doc.items[i].income_account = r.message
                                }    
                            }
                        }
                    })
                    frm.refresh_fields('items')
            }
        
        });


    """
    doc.save()



def create_item_script():
    name = "Item-Form"
    if frappe.db.exists("Client Script",name) :
        doc = frappe.get_doc("Client Script",name)
    else :
        doc = frappe.new_doc("Client Script")
    doc.dt      = "Item"
    doc.view    = "Form"
    doc.enabled = 1
    doc.script = """
            
        frappe.ui.form.on("Item", {
            item_group(frm){
                if(frm.doc.item_group && frm.doc.__islocal){
                    frappe.call({
                        method:'dynamic.api.generate_item_code',
                        args:{
                            'item_group':frm.doc.item_group
                        },callback(r){
                            if(r.message){
                                if(r.message == 'false'){
                                    frm.set_value("item_group","")
                                    frm.refresh_field('item_group')
                                }else{
                                frm.set_value('item_code',r.message)
                                frm.refresh_field('item_code')
                                }
                            }
                        }
                    })
                }
            }
        
        });


    """
    doc.save()

def create_lead_script():
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
                    method:"dynamic.api.create_new_appointment",
                    frm: frm
                  });
                },
                __("Create")
              );
              frm.add_custom_button(
                __("Show History"),
                function () {
                  frappe.set_route('query-report','Actions Report',{"phone_no":frm.doc.phone_no})
                }
              );
                }
            }
        
        });


    """
    doc.save()

def create_customer_script():
    name = "Customer-Form"
    if frappe.db.exists("Client Script",name) :
        doc = frappe.get_doc("Client Script",name)
    else :
        doc = frappe.new_doc("Client Script")
    doc.dt      = "Customer"
    doc.view    = "Form"
    doc.enabled = 1
    doc.script = """
            
        frappe.ui.form.on("Customer", {
            refresh(frm){
                if(!frm.doc.__islocal){
              frm.add_custom_button(
                __("Show History"),
                function () {
                  frappe.set_route('query-report','Actions Report',{"phone_no":frm.doc.phone_no})
                }
              );
                }
            }
        
        });


    """
    doc.save()

def create_opportunity_script():
    name = "Opportunity-Form"
    if frappe.db.exists("Client Script",name) :
        doc = frappe.get_doc("Client Script",name)
    else :
        doc = frappe.new_doc("Client Script")
    doc.dt      = "Opportunity"
    doc.view    = "Form"
    doc.enabled = 1
    doc.script = """
            
        frappe.ui.form.on("Opportunity", {
            refresh(frm){
                if(!frm.doc.__islocal){
              frm.add_custom_button(
                __("Show History"),
                function () {
                  frappe.set_route('query-report','Actions Report',{"phone_no":frm.doc.phone_no})
                }
              );
                }
            }
        
        });


    """
    doc.save()

def add_property_setters():
    name = "Item-item_code-read_only"
    if frappe.db.exists("Property Setter",name) :
        pass
    else:
        doc = frappe.new_doc("Property Setter")
        doc.doctype_or_field="DocField"
        doc.doc_type="Item"
        doc.field_name="item_code"
        doc.property="read_only"
        doc.property_type="Check"
        doc.value=1
        doc.save()

def add_lead_property_setters():
    name = "Lead-main-search_fields"
    if frappe.db.exists("Property Setter",name) :
        pass
    else:
        doc = frappe.new_doc("Property Setter")
        doc.doctype_or_field="DocType"
        doc.doc_type="Lead"
        doc.property="search_fields"
        doc.property_type="Data"
        doc.value="lead_name,lead_owner,status,phone_no"
        doc.save()

def add_opp_property_setters():
    name = "Opportunity-main-search_fields"
    if frappe.db.exists("Property Setter",name) :
        pass
    else:
        doc = frappe.new_doc("Property Setter")
        doc.doctype_or_field = "DocType"
        doc.doc_type = "Opportunity"
        doc.property = "search_fields"
        doc.property_type = "Data"
        doc.value="status,transaction_date,party_name,opportunity_type,territory,company,phone_no"
        doc.save()

def add_customer_property_setters():
    name = "Customer-main-search_fields"
    if frappe.db.exists("Property Setter",name) :
        pass
    else:
        doc = frappe.new_doc("Property Setter")
        doc.doctype_or_field="DocType"
        doc.doc_type="Customer"
        doc.property="search_fields"
        doc.property_type="Data"
        doc.value="customer_name,customer_group,territory, mobile_no,primary_address,phone_no"
        doc.save()


def install_action():
    data =[
            {
            "type": "Indoor",
            "action_name": "Visit"
            },
            {
                "type": "Indoor",
                "action_name": "Call"
            },
            {
                "type": "Out door",
                "action_name": "Out"
            }

        ]
    for i in data :
        if not frappe.db.exists("Action",i.get("action_name")) :
            frappe.get_doc({
                "doctype":"Action",
                "type":i.get("type"),
                "action_name":i.get("action_name")
            }).insert()
# Create two Stock Entry Types --  Material Send -- Matrial Receive
def create_trans():
    name ="Transfer"
    # if exit 
    exit_name= frappe.db.sql(f""" 
    SELECT name FROM `tabStock Entry Type` WHERE name = '{name}'
    """,as_dict=1)
    if not exit_name or len(exit_name) == 0 :
        #create Stock Entry Type 
        new_type = frappe.new_doc("Stock Entry Type")
        new_type.__newname = name
        new_type.purpose = "Material Transfer"
        new_type.add_to_transit = 1
        new_type.save()




def create_terra_scripts():
    create_trans()
    try:
        create_sales_invoice_script()
    except:
        print("error in create sales order script")

    
    try:
        create_item_script()
    except:
        print("error in create_item_script")

    try:
        create_lead_script()
    except:
        pass
    
    try:
        create_customer_script()
    except:
        pass
    
    try:
        create_opportunity_script()
    except:
        pass
    try:
        add_property_setters()
    except:
        print("error in add_property_setters")

    try:
        add_lead_property_setters()
    except:
        print("add_item_property_setters")

    try:
        add_opp_property_setters()
    except:
        print("add_opp_property_setters")

    try:
        add_customer_property_setters()
    except:
        print("add_customer_property_setters")

    try:
        install_action()
    except Exception as ex:
        print("----------------------- install_actioninstall_actioninstall_action",str(ex))



