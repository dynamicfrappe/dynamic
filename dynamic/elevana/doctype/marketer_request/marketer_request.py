# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.utils.data import get_link_to_form
from frappe import _

from frappe import utils
import random
import string
#from dynamic.elevana.api import create_coupon_code

class MarketerRequest(Document):
    def validate(self) :
        #create refal Code 
        if not self.referral_code :
            self.referral_code = ''.join(random.choice(string.ascii_letters) for i in range(5))
    def on_submit(self):
        self.create_customer()
        self.create_sales_partner()
        self.status = "Approved"
        self.db_set("status", self.status)
        if self.item_groups :
            self.create_pricing_rule()
            self.createcoupon_code()
    def create_pricing_rule(self):
        rule = frappe.new_doc("Pricing Rule")
        rule.title = self.marketer_name
        rule.apply_on = "Item Group"
        rule.price_or_product_discount = "Price"
        rule.mixed_conditions = 1
        rule.is_cumulative = 1 
        rule.coupon_code_based = 1 
        rule.selling = 1 
        rule.min_qty = 1 
        rule.max_qty =1000 
        rule.min_amt = 1
        rule.max_amt =1000
        for itemgroup in self.item_groups :
            rule.append('item_groups', {
                "item_group": itemgroup.item_group
            })
        rule.valid_from = utils.today()
        rule.valid_upto = "2999-01-01"
        rule.rate_or_discount = self.rate_or_discount
        rule.discount_percentage = self.discount_percentage
        rule.rate = self.rate
        rule.discount_amount = self.discount_amount
        rule.save()
        self.pricing_rule = rule.name

    def createcoupon_code(self) :
        if self.pricing_rule :
            coupon = frappe.new_doc("Coupon Code")
            coupon.coupon_type = "Promotional"
            coupon.coupon_name = self.marketer_name
            coupon.coupon_code = self.referral_code
            coupon.pricing_rule = self.pricing_rule
            coupon.valid_from = utils.today()
            coupon.valid_upto = "2999-01-01"
            coupon.save()
            self.coupon_code = coupon.name





    def create_sales_partner(self):
        default_customer_territory = frappe.db.get_single_value(
            "Selling Settings", "default_marketer_territory")

        if not default_customer_territory:
            frappe.throw(
                _("Please set Marketer Settings in Selling Settings"))

        sales_partner = frappe.new_doc("Sales Partner")
        sales_partner.partner_name = self.marketer_name
        sales_partner.commission_rate = self.commission_rate
        sales_partner.partner_type = self.partner_type
        sales_partner.ref_doctype = self.doctype
        sales_partner.ref_docname = self.name
        sales_partner.territory = default_customer_territory
        sales_partner.referral_code = self.referral_code
        sales_partner.set("item_groups", [])
        for row in self.item_groups:
            sales_partner.append('item_groups', {
                "item_group": row.item_group
            })
        sales_partner.insert()

        lnk = get_link_to_form(sales_partner.doctype, sales_partner.name)
        frappe.msgprint(_("{} {} was Created").format(
            sales_partner.doctype, lnk))

    def create_customer(self):
        default_customer_group = frappe.db.get_single_value(
            "Selling Settings", "default_marketer_customer_group")
        default_customer_territory = frappe.db.get_single_value(
            "Selling Settings", "default_marketer_territory")

        if not (default_customer_group and default_customer_territory):
            frappe.throw(
                _("Please set Marketer Settings in Selling Settings"))

        customer = frappe.new_doc("Customer")
        customer.customer_name = self.marketer_name
        customer.customer_type = "Marketer"
        customer.customer_group = default_customer_group
        customer.territory = default_customer_territory
        customer.ref_doctype = self.doctype
        customer.ref_docname = self.name
        customer.save()
        # create Address
        address_type = "Billing"

        address = frappe.new_doc("Address")
        address.address_type = address_type
        address.address_title = customer.name
        address.address_line1 = self.address_line
        address.building_no = "1"
        address.floor_no = "1"
        address.apartment_no = "1"
        address.city = self.city
        address.country = self.country

        address.set("links", [])
        address.append("links", {
            "link_doctype": customer.doctype,
            "link_name": customer.name,
            "link_title": customer.customer_name,
        })
        # add link ref to address
        address.append("links", {
            "link_doctype": self.doctype,
            "link_name": self.name,
            "link_title": self.marketer_name,
        })

        address.insert()
        # link address to customer
        customer.customer_primary_address = address.name
        customer.save()

        lnk = get_link_to_form(customer.doctype, customer.name)
        frappe.msgprint(_("{} {} was Created").format(customer.doctype, lnk))
