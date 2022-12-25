import frappe 



def submit_supplier_quotation(self) :
    requested = []
    for item in self.items :
        if item.material_request and item.material_request not in requested :
            requested.append(item.material_request)
    for matrial_request in requested  :
        frappe.db.sql(f""" 
        update `tabMaterial Request` set status= 'Requested'  , quotation ='{self.name}' , has_quotation = 1 ,
        WHERE name ='{matrial_request}' and material_request_type = "Purchase"  and status <> "Partially Ordered" and status <> "Ordered"
        
                """)
        frappe.db.commit()
