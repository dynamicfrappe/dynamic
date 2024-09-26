import frappe
from frappe import _
Domains=frappe.get_active_domains()

def validate(self , event):
	if "Lormed" in Domains :
		validate_items(self)
	if "Qaswaa" in Domains :
		validate_rate_of_items(self)
		warehouse1(self)
		validate_sales_team(self)
		item_discount_rate(self)
	
	if "Healthy Corner" in Domains:
		item_discount_rate2(self)
		calculate_total(self)
		set_discount(self)
		# calculate_all_total(self)
		
		

# def before_save(self,event):
# 	if "Qaswaa" in Domains :
# 		# items1(self)

def after_submit(self , event):
	if "Stock Reservation" in Domains:
		edit_of_reseration(self)
	
def after_cancel(self , event):
	if "Stock Reservation" in Domains :
		validate_when_cancel(self)

	
	
def before_submit(self , event):
	if "Lormed" in Domains  and not self.ignore_validation: #and not self.ignore_validation
		check_open_sales_invoices(self)
	if "Qaswaa" in Domains :
		submit_invoice(self)

def validate_items(self):
	for item in self.items :
		if item.brand != self.brand:
			frappe.throw(_("Brand of <b>{0}</b> should be <b>{1}</b>").format(item.item_code , self.brand))
			
def validate_rate_of_items(self):
	for item in self.items:
		if item.rate <= 0:
			frappe.throw(_(f"<b>Rae</b> of item {item.item_code} in row {item.idx} should be equal bigger than 0")) 

def check_open_sales_invoices(self):
   if frappe.db.exists("Sales Invoice", {"customer": self.customer ,"brand" :self.brand , "docstatus" : 1 ,"outstanding_amount" : [">" ,1.00] , "name" :["!=", self.name]}):
	   frappe.throw(_("There are open sales invoice for <b>{0}</b> with the same brand <b>{1}</b>").format(self.customer, self.brand))

def submit_invoice(self):
	sales_document = frappe.new_doc("Sales Document States")
	sales_document.posting_date = self.posting_date
	sales_document.invoice_type = self.doctype
	sales_document.invoice_name = self.name
	# sales_document.shipping_company = self.company
	sales_document.customer = self.customer
	sales_document.customer_name = self.customer_name
	sales_document.grand_total = self.grand_total
	sales_document.insert(ignore_permissions=True)

def validate_sales_team(self):
		if not self.sales_team:
			frappe.throw("Sales Team was mandatory")

def item_discount_rate(self):
    item_discount_rate = self.item_discount_rate or 0
    for item in self.items:
        item.discount_percentage = item_discount_rate
        if item_discount_rate is not None:
            item.discount_amount = item.price_list_rate * (item_discount_rate / 100)
        else:
            item.discount_amount = 0  
        item.rate = item.price_list_rate - item.discount_amount
        item.amount = item.rate * item.qty

def item_discount_rate2(self):
    item_discount_rate = self.discount_item or 0
    for item in self.items:
        item.discount_percentage = item_discount_rate
        if item_discount_rate is not None:
            item.discount_amount = item.price_list_rate * (item_discount_rate / 100)
        else:
            item.discount_amount = 0  
        item.rate = item.price_list_rate - item.discount_amount
        item.amount = item.rate * item.qty
def calculate_total(self):
	total_price = 0
	# for item in self.items:
	# 	total_price+=item.price_list_rate 

	total_price = float(self.total or 0) * (100+float(self.discount or 0))/100
	self.total_price = total_price 
	self.all_total = (self.total or 0) - total_price

def set_discount(self):
	if self.customer:
		discount =frappe.db.get_value(
				"Customer",
				{"name": self.customer},
				["customer_discount"],
				as_dict=1,)
		if discount["customer_discount"]:
			self.discount = discount["customer_discount"]

def calculate_all_total(self):
	if self.discount :
		self.all_total = (float(self.total_price) * float(self.discount) ) /100
	else:
		self.all_total = float(self.total_price) 

def edit_of_reseration(self ):
	items = self.get("items")
	for item in items:
		if frappe.db.exists("Stock Reservation Entry" ,{
				"item_code":item.item_code,
				"warehouse":item.warehouse,
				"voucher_no":item.sales_order,
				"voucher_detail_no" : item.so_detail
				}):
			doc = frappe.get_doc("Stock Reservation Entry" , {
				"item_code":item.item_code,
				"warehouse":item.warehouse,
				"voucher_no":item.sales_order,
				"voucher_detail_no" : item.so_detail
				})
			qty = (doc.delivered_qty if doc.delivered_qty else 0 ) + item.stock_qty 
			doc.delivered_qty = qty 
			doc.save()
			frappe.db.commit()
			print("Updated")
		else:
			print("Not Updated")


def validate_when_cancel(self):
	items = self.get("items")
	for item in items:
		if frappe.db.exists("Stock Reservation Entry" ,{
				"item_code":item.item_code,
				"warehouse":item.warehouse,
				"voucher_no":item.sales_order,
				"voucher_detail_no" : item.so_detail
				}):
			doc = frappe.get_doc("Stock Reservation Entry" , {
			"item_code":item.item_code,
			"warehouse":item.warehouse,
			"voucher_no":item.sales_order,
			"voucher_detail_no" : item.so_detail
			})
			qty = (doc.delivered_qty if doc.delivered_qty else 0 ) - item.stock_qty 
			doc.delivered_qty = qty 
			doc.save()
			frappe.db.commit()
def warehouse1(self):
	if self.update_stock == 1:
		if not self.set_warehouse:
			frappe.throw("Warehouse was mandatory")

	



