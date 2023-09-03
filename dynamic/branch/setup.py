from __future__ import unicode_literals
import frappe

def create_branch_script():
    # try:
        create_quotation_branch_script()
        create_sales_invoice_branch_script()
        create_sales_order_branch_script()
        create_delivery_note_branch_script()
    # except:
    #     pass

def create_quotation_branch_script():
    name = "Quotation-Form"
    if frappe.db.exists("Client Script",name) :
        doc = frappe.get_doc("Client Script",name)
    else :
        doc = frappe.new_doc("Client Script")
        doc.dt      = "Quotation"
        doc.view    = "Form"
        doc.enabled = 1
    doc.script = """   
                frappe.ui.form.on('Quotation', { 
                party_name:(frm)=>{
                console.log("hello")
              if(frm.doc.party_name){
        	        frappe.call({
        	            method:"dynamic.api.get_customer_branches",
        	            args:{
        	                "customer":frm.doc.party_name
        	            },callback(r){
        	                console.log(r.message)
        	                if(r.message){
        	                    frm.set_query("customer_branch", () => {
                        			return {
                        				filters: {
                        					name: ["in", r.message]
                        				},
                        			};
                        		});
        	                }
        	            }
        	        })
        	    }  
            }
            })
        """
    doc.save()

def create_sales_invoice_branch_script():
    name = "Sales Invoice-Form"
    if frappe.db.exists("Client Script",name) :
        doc = frappe.get_doc("Client Script",name)
    else :
        doc = frappe.new_doc("Client Script")
        doc.dt      = "Sales Invoice"
        doc.view    = "Form"
        doc.enabled = 1
    doc.script = """   
                frappe.ui.form.on('Sales Invoice', { 
                customer:(frm)=>{
                console.log("hello")
              if(frm.doc.customer){
        	        frappe.call({
        	            method:"dynamic.api.get_customer_branches",
        	            args:{
        	                "customer":frm.doc.customer
        	            },callback(r){
        	                console.log(r.message)
        	                if(r.message){
        	                    frm.set_query("customer_branch", () => {
                        			return {
                        				filters: {
                        					name: ["in", r.message]
                        				},
                        			};
                        		});
        	                }
        	            }
        	        })
        	    }  
            },
            customer_branch:(frm)=>{
                if(frm.doc.customer_branch){
                    frm.set_value("remarks",frm.doc.customer_branch)
                }
            }
            })
        """
    doc.save()


def create_sales_order_branch_script():
    name = "Sales Order-Form"
    if frappe.db.exists("Client Script",name) :
        doc = frappe.get_doc("Client Script",name)
    else :
        doc = frappe.new_doc("Client Script")
        doc.dt      = "Sales Order"
        doc.view    = "Form"
        doc.enabled = 1
    doc.script = """   
                frappe.ui.form.on('Sales Order', { 
                customer:(frm)=>{
                console.log("hello")
              if(frm.doc.customer){
        	        frappe.call({
        	            method:"dynamic.api.get_customer_branches",
        	            args:{
        	                "customer":frm.doc.customer
        	            },callback(r){
        	                console.log(r.message)
        	                if(r.message){
        	                    frm.set_query("customer_branch", () => {
                        			return {
                        				filters: {
                        					name: ["in", r.message]
                        				},
                        			};
                        		});
        	                }
        	            }
        	        })
        	    }  
            },
            })
        """
    doc.save()

def create_delivery_note_branch_script():
    name = "Delivery Note-Form"
    if frappe.db.exists("Client Script",name) :
        doc = frappe.get_doc("Client Script",name)
    else :
        doc = frappe.new_doc("Client Script")
        doc.dt      = "Delivery Note"
        doc.view    = "Form"
        doc.enabled = 1
    doc.script = """   
                frappe.ui.form.on('Delivery Note', { 
                customer:(frm)=>{
              if(frm.doc.customer){
        	        frappe.call({
        	            method:"dynamic.api.get_customer_branches",
        	            args:{
        	                "customer":frm.doc.customer
        	            },callback(r){
        	                console.log(r.message)
        	                if(r.message){
        	                    frm.set_query("customer_branch", () => {
                        			return {
                        				filters: {
                        					name: ["in", r.message]
                        				},
                        			};
                        		});
        	                }
        	            }
        	        })
        	    }  
            },
            
            })
        """
    doc.save()