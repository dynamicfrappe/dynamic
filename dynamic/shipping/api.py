import frappe
import json
import requests
from frappe import _


# 1. Authentication  URL: https://staging.flextock.com/base/auth/,


def authenticate():
    method_url = "/base/auth/"
    data = validate_shipping_settings()
    if data.status:
        base_url = data.get("url")
        body = {
            "username": data.get("user_name"),
            "password": data.get("password"),
            "key": data.get("key")
        }
        url = base_url + method_url
        r = requests.post(url, body)
        if r.status_code == 200:
            frappe.set_value("Shipping Settings", "Shipping Settings", "token", r.text)
        else:
            frappe.log_error(
                title=_("Error while shiiping authentications"),
                message=r.text,
            )
    else:
        frappe.log_error(
            title=_("Error while shiiping authentications"),
            message="Error while shiiping authentications",
        )


# 2. Create Product   ---> take list of product
def create_product(products):
    """
    Args:
        products: list of products
    Returns:
        listOfObjects : list<Object>
    """
    data = validate_shipping_settings()
    if data.status:
        method_url = "/create-products/"
        base_url = data.get("url")
        url = base_url + method_url
        body = {"products": products}
        r = requests.post(url, )
        if r.status_code == 200:
            return r.text
        else:
            frappe.log_error(
                title=_("Error while create products"),
                message=r.text,
            )


# create order
def create_order(doc, *args, **kwargs):
    """
    Args:
        doc: order object
        *args:
        **kwargs:
    Returns:
        obj: message
    """
    data = validate_shipping_settings()
    if data.status:
        method_url = "/create-order/"
        base_url = data.get("url")
        url = base_url + method_url
        customer = frappe.get_doc("Customer", doc.customer)
        customer_name = customer.split(" ")
        address_obj = {}
        if doc.customer_primary_address and doc.customer_primary_contact:
            customer_address = frappe.get_doc("Address", doc.customer_primary_address)
            cutomer_contact = frappe.get_doc("Contact", doc.customer_primary_contact)
            address_obj = {
                "city": customer_address.city,
                "area": customer_address.state,
                "address_line1": customer_address.address_line1,
                "address_line2": customer_address.address_line2,
                "building_no": customer_address.building_no,
                "floor_no": customer_address.floor_no,
                "apartment_no": customer_address.apartment_no,
                "is_work_address": False,
                "first_name": customer_name[0],
                "last_name": customer_name[1] if len(customer_name) > 1 else "",

                "phone_number": cutomer_contact.phone_nos[0].phone if len(cutomer_contact.phone_nos) > 0 else "",
                "secondary_phone_number": cutomer_contact.phone_nos[1].phone if len(
                    cutomer_contact.phone_nos) > 1 else "",
                "note": doc.note
            }
        body = {
            "order_code": doc.name,
            "order_date": doc.transaction_date,
            "cash_on_delivery": doc.total,
            "integration_source": "elevana",
            "customer_address": address_obj,
            "line_items": [
                {
                    "sku_code": item.item_code,
                    "quantity": item.qty
                } for item in doc.items
            ]
        }

        r = requests.post(url, body)
        if r.status_code == 200:
            pass
        else:
            frappe.log_error(
                title=_("Error while create order"),
                message=r.text,
            )


# 4. Get Order status:
def get_order_status(order_code):
    """
    Args:
        order_code:
    Returns:
        obj : courier_name,order_status,tracking_number,tracking_url
    """
    data = validate_shipping_settings()
    if data.status:
        method_url = "/order-status/"
        base_url = data.get("url")
        url = base_url + method_url
        r = requests.post(url, data)
        if r.status_code == 200:
            return r.text
        else:
            frappe.log_error(
                title=_("Error while get order status"),
                message=r.text,
            )


def validate_shipping_settings():
    """
    Returns:
        object: object
    """
    shipping_settings = frappe.get_single("Shipping Settings")
    if shipping_settings.get("url") and shipping_settings.get("user_name") and shipping_settings.get(
            "password") and shipping_settings.get("key"):
        return {
            "status": True,
            "url": shipping_settings.get("url"),
            "user_name": shipping_settings.get("user_name"),
            "password": shipping_settings.get("password"),
            "key": shipping_settings.get("key")

        }

    return {"status": False}
