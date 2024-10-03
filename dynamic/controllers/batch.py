import frappe 
Domains=frappe.get_active_domains()



@frappe.whitelist()
def befor_naming (self , method):
    if "Healthy Corner" in Domains:
        return True
        change_batch_name(self)



def change_batch_name(self):
    self.batch_id = f"""{self.batch_id} - {self.item}"""