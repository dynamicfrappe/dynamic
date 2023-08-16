import frappe 

#dynamic.weh.delevery_note.validate_delevery_note
DOMAINS = frappe.get_active_domains()

def validate_delevery_note(self ,*args , **kwargs) :
   if "WEH" in DOMAINS :
      set_un_set_values(self)

def set_un_set_values(self , *args , **kwargs) :
   """
   this function set delevery note values for customer info 
   branch / doctor sergry
   
   """
   # customer 
   customer =frappe.get_doc("Customer" , self.customer)
   if not self.doctor :
      #
      if customer.doctor :
         self.doctor = customer.doctor 
   if not self.branch :
      if customer.branch :
         self.branch = customer.branch
   if not self.surgery :
      if customer.surgery :
         self.surgery = customer.surgery
   