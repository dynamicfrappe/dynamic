import frappe
from frappe import _

# Terra Domain required
from dynamic.terra.landed_cost import validate_cost, get_doctype_info
from dynamic.terra.sales_invoice import check_return_account, validate_sales_invoices
from dynamic.terra.item import create_item_serial_doc
import random


DOMAINS = frappe.get_active_domains()


def validate_landed_cost(doc, *args, **kwargs):
    """Add domain to run this customization"""
    if "Terra" in DOMAINS:
        validate_cost(doc)
    else:
        pass


def validate_sales_invoice(doc, *args, **kwargs):
    if "Terra" in DOMAINS:
        check_return_account(doc)
        validate_sales_invoices(doc)
    else:
        pass


@frappe.whitelist()
def get_query_type(*args, **kwargs):
    return [["Purchase Invoice"]]


@frappe.whitelist()
def get_purchase_items(invoice=None, *args, **kwargs):
    invoices = frappe.db.sql(
        """SELECT  p.parent  FROM 
                                `tabPurchase Invoice Item`  p
                                inner join   
                                `tabItem`  a 
                                inner join 
                                `tabPurchase Invoice`  c
                                on p.item_code = a.name and c.name = p.parent
                                WHERE a.is_stock_item = 0 and c.docstatus = 1 
                                group by p.parent   """
    )

    invocie_typ = []
    for i in invoices:
        available = get_doctype_info("Purchase Invoice", i[0])
        if available.get("allocated") > 0:
            invocie_typ.append(i)
    return invocie_typ


@frappe.whitelist()
def get_active_domain():
    if "Terra" in DOMAINS:
        return True
    else:
        return False


@frappe.whitelist()
def get_active_domain_gebco():
    if "Gebco" in DOMAINS:
        return True
    else:
        return False


def create_item_specs(doc):
    doc.description = doc.item_name
    # doc.description = doc.item_name + str(doc.get("specs") or "") + str(doc.get("color") or "") + str(doc.get("size") or "") + str(doc.get("cutting_type") or "")
    # print("sssssssssss===================>",doc.description)
    if doc.get("specs"):
        doc.description += doc.get("specs")
    if doc.get("color"):
        doc.description += "-" + doc.get("color")
    if doc.get("size"):
        doc.description += "-" + doc.get("size")
    if doc.get("cutting_type"):
        doc.description += "-" + doc.get("cutting_type")


def generate_item_code(item_group):
    if 'Terra' in DOMAINS:
        group_doc = frappe.get_doc("Item Group", item_group)
        group_code = group_doc.code
        if not group_code:
            frappe.msgprint(_("Item Group Doesnt Have Code"))
            return "false"
        sql = f"""
        select count(*) +1 as 'serial' from `tabitem code serial` where item_group= '{group_doc.name}'
        """
        res = frappe.db.sql(sql, as_dict=1)

        serial = str(group_code or "") + "-" + str(res[0].serial or "")

        return serial


def validate_item_code(doc, *args, **kwargs):
    print("mohsen22")
    if "Terra" in DOMAINS:
        print("mohsen33")
        if doc.is_new():
            item_code = generate_item_code(doc.item_group)
            print("mohsen44", item_code)
            doc.item_code = item_code
            create_item_serial_doc(doc)
            create_item_specs(doc)

    # if "Barcode Item" in DOMAINS:
    #     if len(doc.barcodes) and doc.barcodes[0].get("barcode"):
    #         doc.db_set("barcode_second", doc.barcodes[0].get("barcode"))
    #         doc.db_set("item_barcode_second", doc.barcodes[0].get("barcode"))


# def before_insert_item(doc, *args, **kwargs):
#     if "Barcode Item" in DOMAINS:
#         if len(doc.barcodes) and doc.barcodes[0].get("barcode"):
#             doc.db_set("barcode_second", doc.barcodes[0].get("barcode"))
#             doc.db_set("item_barcode_second", doc.barcodes[0].get("barcode"))

@frappe.whitelist()
def after_insert_journal_entry(doc, *args, **kwargs):
    doc_asset = frappe.get_doc("Asset", doc)
    cnt = sum(1 for schedule in doc_asset.schedules if schedule.journal_entry)
    return cnt

@frappe.whitelist()
def after_insert_variant_item(doc, *args, **kwargs):
    if "Elhamd" in DOMAINS:
        if doc.variant_of:
            if len(doc.attributes):
                for row in doc.attributes:
                    doc.description += (
                        f" <p>  {row.attribute} : {row.attribute_value}</p>"
                    )
                doc.db_set("description", doc.description)
    if "Barcode Item" in DOMAINS:
        barcode_num = ""
        if not len(doc.barcodes):
            barcode_num = generate_barcode()
            doc.append(
                "barcodes", {"item_barcode": barcode_num, "barcode": barcode_num}
            )
        if len(doc.barcodes):
            barcode_num = doc.barcodes[0].get("barcode")
        doc.db_set("barcode", barcode_num)
        doc.db_set("item_barcode", barcode_num)
        doc.save()


def generate_barcode():
    new_barcode = "".join([str(random.randint(0, 9)) for _ in range(13)])
    old_barcodes = frappe.db.sql(
        f"""
        select barcode from `tabItem Barcode` where barcode ='{new_barcode}'
        """,
        as_list=1,
    )
    if len(old_barcodes):
        generate_barcode()
    if not old_barcodes:
        return new_barcode
