 


import frappe 
import json
from frappe.model.naming import make_autoname,set_name_by_naming_series,determine_consecutive_week_number,NAMING_SERIES_PART_TYPES
import datetime
import re

from six import string_types

import frappe
from frappe import _
from frappe.model import log_types
from frappe.utils import cint, cstr, now_datetime

@frappe.whitelist()
def show_next_name(doc):
	# pass
	item_naming_by = frappe.db.get_single_value('Stock Settings','item_naming_by')
	nex_name = ''
	if item_naming_by == "Naming Series":
		doc = json.loads(doc)
		nex_name = make_autoname(doc.get('naming_series'), "", doc)
	return {'new_name':nex_name}
	

def make_autoname(key="", doctype="", doc=""):
	"""
	     Creates an autoname from the given key:

	     **Autoname rules:**

	              * The key is separated by '.'
	              * '####' represents a series. The string before this part becomes the prefix:
	                     Example: ABC.#### creates a series ABC0001, ABC0002 etc
	              * 'MM' represents the current month
	              * 'YY' and 'YYYY' represent the current year


	*Example:*

	              * DE/./.YY./.MM./.##### will create a series like
	                DE/09/01/0001 where 09 is the year, 01 is the month and 0001 is the series
	"""
	if key == "hash":
		return frappe.generate_hash(doctype, 10)

	if "#" not in key:
		key = key + ".#####"
	elif "." not in key:
		error_message = _("Invalid naming series (. missing)")
		if doctype:
			error_message = _("Invalid naming series (. missing) for {0}").format(doctype)

		frappe.throw(error_message)

	parts = key.split(".")
	n = parse_naming_series(parts, doctype, doc)
	return n

def parse_naming_series(parts, doctype="", doc=""):
	n = ""
	if isinstance(parts, str):
		parts = parts.split(".")
	series_set = False
	today = now_datetime()
	for e in parts:
		if not e:
			continue

		part = ""
		if e.startswith("#"):
			if not series_set:
				digits = len(e)
				part = getseries(n, digits)
				series_set = True
		elif e == "YY":
			part = today.strftime("%y")
		elif e == "MM":
			part = today.strftime("%m")
		elif e == "DD":
			part = today.strftime("%d")
		elif e == "YYYY":
			part = today.strftime("%Y")
		elif e == "WW":
			part = determine_consecutive_week_number(today)
		elif e == "timestamp":
			part = str(today)
		elif e == "FY":
			part = frappe.defaults.get_user_default("fiscal_year")
		elif e.startswith("{") and doc:
			e = e.replace("{", "").replace("}", "")
			part = doc.get(e)
		elif doc and doc.get(e):
			part = doc.get(e)
		else:
			part = e

		if isinstance(part, str):
			n += part
		elif isinstance(part, NAMING_SERIES_PART_TYPES):
			n += cstr(part).strip()
	
	return n

def getseries(key, digits):
	# series created ?
	sql ="SELECT `current` FROM `tabSeries` WHERE `name`='%s' "%key

	current = frappe.db.sql(sql)
	
	if current and current[0][0] is not None:
		current = current[0][0] +1
	else:
		# no, create it
		current = 1
	return ("%0" + str(digits) + "d") % current


def get_users_warehouse(warehouse):
	warehouse_obj = frappe.get_doc("Warehouse" , warehouse)
	users = warehouse_obj.get("users")
	if users:
		return users