
import frappe

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
            return {"status": "success", "message": "Document assigned to selected users."}
        else:
            return {"status": "error", "message": "No users selected."}
    
    return {"status": "error", "message": "No users provided."}