import frappe 
Domains=frappe.get_active_domains()



@frappe.whitelist()
def befor_naming (self , method):
    if "Healthy Corner" in Domains:
        change_batch_name(self)



def change_batch_name(self):
    self.batch = self.batch + self.item