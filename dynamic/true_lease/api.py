
import frappe
import json
from frappe.desk.form.assign_to import add


@frappe.whitelist()
def get_users_by_departments(departments):

    if isinstance(departments, str):
        try:
            departments = frappe.parse_json(departments)
        except Exception as e:
            return f"Invalid departments format: {str(e)}"

    if departments:
        users = frappe.get_all(
            "User",
            filters={
                "department": ["in", departments]
            },
            fields=["full_name", "email"]
        )
        if users:
            return {"users": users}
        else:
            return {"message": "No users found in the selected departments."}

    return {"message": "No departments selected."}

@frappe.whitelist()
def assign_users(docname, selected_users):
    if isinstance(selected_users, str):
        try:
            selected_users = frappe.parse_json(selected_users)
        except Exception as e:
            return {"status": "error", "message": f"Invalid users format: {str(e)}"}

    if selected_users:
        emails = [user.get("user_email") for user in selected_users if user.get("selected")]
        if emails:
            frappe.db.set_value("Actions", docname, "_assign", frappe.as_json(emails))
            frappe.db.commit()
            for user in emails:
                assign_action_to_user(docname, user)
            
            return {"status": "success", "message": "Document assigned to selected users."}
        else:
            return {"status": "error", "message": "No users selected."}
    
    return {"status": "error", "message": "No users provided."}

def assign_action_to_user(doc_name, employee_email):
    if not frappe.db.exists("User", employee_email):
        frappe.throw(f"User {employee_email} does not exist.")
    args = {
        'assign_to': [employee_email], 
        'doctype': "Actions",  
        'name': doc_name,  
        'description': 'Please address this Action'  
    }
    add(args)


@frappe.whitelist()
def approve_actions(name):
    frappe.db.set_value("Actions", name, "status", "Approved")
    frappe.db.commit()

@frappe.whitelist()
def reject_actions(name):
    frappe.db.set_value("Actions", name, "status", "Rejected")
    frappe.db.commit()


@frappe.whitelist()
def approve_leads(name):
    frappe.db.set_value("Lead", name, "cp_status", "Approved")
    frappe.db.commit()

@frappe.whitelist()
def reject_leads(name):
    frappe.db.set_value("Lead", name, "cp_status", "Rejected")
    frappe.db.commit()


@frappe.whitelist()
def fetch_account_manager(lead_name):
    lead_obj = frappe.db.get_value("Lead", lead_name, ["lead_owner" , "sector"] , as_dict = 1)
    if lead_obj["lead_owner"] or lead_obj["sector"]:
        return lead_obj["lead_owner"] , lead_obj["sector"]