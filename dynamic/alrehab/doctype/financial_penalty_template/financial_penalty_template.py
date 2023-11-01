# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class Financialpenaltytemplate(Document):

	def validate_equation(self) :
		variables = []
		if self.variables and len(self.variables) > 0 :
			for v in self.variables :
				variables.append(v.variable)
		else :
			frappe.throw(_("Please Set equatio variables"))
		for i in self.equation  :
			if i.isalnum() :
				if i not in variables :
					frappe.throw(_(f"Please set Value for Value {i}"))
	def validate(self) :
		#check variabe table values 
		#set to list 
		#check Equation is it in list 
		if self.has_equation == 1 :
			self.validate_equation()
			pass
