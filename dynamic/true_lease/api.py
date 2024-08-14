
import frappe

@frappe.whitelist()
def assign_to_departments(docname, departments):

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
            fields=["email"]
        )
        emails = [user["email"] for user in users]
        if emails:
            frappe.db.set_value("Actions", docname, "_assign", frappe.as_json(emails))
            frappe.db.commit()
            return "Document assigned to departments."
        else:
            return "No users found in the selected departments."
    return 1