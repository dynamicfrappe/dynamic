import frappe 
DOMAINS = frappe.get_active_domains()



#dynamic.elevana.hooks
@frappe.whitelist()
def add_partener_to_sales_order(self , *args, **kwargs) :
   """
   if sales order has coupon code and coupon code related with sales partener 
   set Sales Partener automated is sales order on save and check on submit 
   """
   if  'Elevana' in DOMAINS: 
      if self.coupon_code :
         # check if coupin code related with sales partner
         #  Set required data
         referral_code = frappe.db.get_value('Coupon Code', f'{self.coupon_code}', 'coupon_code')
         sales_partner = frappe.db.sql(f""" 
         SELECT name ,commission_rate FROM `tabSales Partner` WHERE referral_code ='{referral_code}'
         """,as_dict=1)
         if sales_partner and len(sales_partner) > 0 :
            self.sales_partner = sales_partner[0].get('name')
            self.commission_rate =sales_partner[0].get('commission_rate')
            self.total_commission = (float(self.commission_rate)/100) \
                     * float(self.amount_eligible_for_commission or 0	)

