from frappe import _

data = {
    
    'custom_fields': {
        
        'Healthcare Practitioner': [
           {
            "fieldname": "medical_specialty",
            "fieldtype": "Link",
            "insert_after": "department",
            "label": "Medical Specialty",
            "options": "Medical Specialty"
           } ,{
            "fieldname": "services_details",
            "fieldtype": "Section Break",
            "insert_after": "hospital"
            
           } ,
           {
            "fieldname": "services",
            "fieldtype": "Table",
            "insert_after": "services_details",
            "label": "Services",
            "options": "Healthcare Practitioner services"
           } 

        ]
    }
}