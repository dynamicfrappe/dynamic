# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 



"""





"""

class ItemGroupNode :

	"""
	Create Tree View For item Group 
	Tree level [ 1   - for parent group root 
				 1/2 - for level one child node
				 1/3 -  or level one child node
				 1/2/1for level tow child 
				 1/2/1/1 for level Three ]
	tree look like 
	        ____1____   1 root node 
	       |         |
      _ _ _2 	     3_ _ _  level one child 1/2
      | 
      1 level tow child 1/2/1
      |
      1 level three child 1/2/1/1
	"""
	def __init__(self) :
		self._parent = None
		self.level = {}
		self.left = None 
		self.right = None
	def set_parent(self, parent) :
		"""
		init root group 
		"""
		self._parent = parent
	def get_parent(self) :
		return self._parent
	
	def set_level_two_childs(self , start_date =False , end_date = False ) :
		items = self.level.get("2")
		for group in items :
			for k , v in group.items():
				is_group = k.get("is_group")
				if is_group :
					#get _childs 
					childs= self.get_all_child_groups(k.get("item_group"))
					group["childs" ] =childs
				#check if group is parent or not 

		pass

	
	def get_level_keys(self) :
		#set level 1 as root level  
		# self.level = 1
		self.level = [
					{	"root" :True  ,"item_group":self._parent ,
						"is_group" :frappe.db.get_value("Item Group" ,self._parent  , "is_group"),
						"parent" : None ,"Amount" :0  }
							] 
		level_two = []
		leve_group = frappe.get_all("Item Group" ,
			      				 {"parent_item_group" : self._parent} , "name")
		for group in leve_group :
			#self.level = "2" 
			obj = {"root":False ,"parent" : self._parent,
	  				"item_group" :group.get('name')  , "Amount" :0 }
			if frappe.db.get_value("Item Group" ,group.get('name')  , "is_group") :
				obj["is_group"] =1
				obj["child"] = self.get_all_child_groups(group.get('name'))
			else :
				obj["is_group"] =0
			self.level.append(obj)
		# self.level["2"] = level_two
		print(self.level)
	
	def get_all_child_groups(self ,group  ) :
		childes= []

		def get_childs(): 
			last_child = False
			if frappe.db.get_value("Item Group" , group , "is_group") :
				groups = frappe.get_all("Item Group" , {"parent_item_group" : group} , "name")
				for gr in groups :
					if  frappe.db.get_value("Item Group" , gr.get("name") , "is_group") :
						data =frappe.db.sql(f""" select name from 
												`tabItem Group` WHERE 
								parent_item_group  = "{gr.get('name')}"
								
								""" ,as_dict=1)
						for name  in data :
							childes.append(name.get("name"))
							a = get_all_child_groups(name.get("name"))
							childes.append(a)
					else :
						childes.append(gr.get("name") )			
			else :
				childes.append(group)
			return childes			
		return get_childs()

def get_all_child_groups(group  ) :
	childes= []
	def get_childs(): 
		last_child = False
		if frappe.db.get_value("Item Group" , group , "is_group") :
			groups = frappe.get_all("Item Group" , {"parent_item_group" : group} , "name")
			for gr in groups :
				if  frappe.db.get_value("Item Group" , gr.get("name") , "is_group") :
					data =frappe.db.sql(f""" select name from 
											`tabItem Group` WHERE 
							parent_item_group  = "{gr.get('name')}"
							
							""" ,as_dict=1)
					for name  in data :
						childes.append(name.get("name"))
						a = get_all_child_groups(name.get("name"))
						childes.append(a)

				else :
					childes.append(gr.get("name") )
				
		else :
			childes.append(group)
		return childes			
	return get_childs()
def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters =None) :
	columns= [
		{
            "label": _("Item Group "),
            "fieldname": "item_group",
            "fieldtype": "Data",
	        #"options" : "Item Group" , 
            "width": 250
        },
	    {
            "label": _("Total Weight"),
            "fieldname": "total_weight",
            "fieldtype": "Data",
            "width": 200
        },
		{
            "label": _("UOM"),
            "fieldname": "uom",
            "fieldtype": "Link",
	    	"options" : "UOM" ,
            "width": 200
        },
	]
	return columns

def get_data(filters=None) :
	"""
	Tables 
	SOI Sales Order Item 
	SO Sales Order 

	
	"""

	condetion = """ 
					WHERE SO.docstatus=1 
				"""
	if filters.get("from_date")  : 
		condetion = condetion + f""" AND  SO.transaction_date >= date('{filters.get("from_date")}')"""
	if filters.get("to_date")  : 
		condetion = condetion + f""" AND  SO.transaction_date <= date('{filters.get("to_date")}')"""
	
	if filters.get("item_group") :
		condetion = condetion +f"""AND SOI.item_group = '{filters.get("item_group")}'"""


	
	sql = f"""
	SELECT 
	SOI.item_group as item_group  ,
	SUM(SOI.total_weight) as total_weight  ,
	SOI.weight_uom as uom
	FROM `tabSales Order Item` SOI  
	INNER JOIN `tabSales Order` SO
	{condetion}
	GROUP BY SOI.item_group
	
	"""
	if filters.get("parent_group") :
		parents = get_all_child_groups(filters.get("parent_group"))
		parent_str="("
		for pr in parents :
			print(pr)
			parent_str += f"('{pr}') ,"
		parent_str+= f"""('{filters.get("parent_group")}' ) )"""
		print(parent_str)
		sql = f"""
				SELECT 
				IG.parent_item_group as item_group  ,
				SUM(SOI.total_weight) as total_weight  ,
				SOI.weight_uom as uom
				FROM `tabSales Order Item` SOI  
				INNER JOIN `tabSales Order` SO 
				ON SOI.parent = SO.name
				INNER JOIN `tabItem Group` IG
				ON SOI.item_group = IG.name
				WHERE IG.parent_item_group in {parent_str}
				GROUP BY IG.parent_item_group
	
			"""
		condetion = condetion + f""" AND SOI.item_group  in 
				(select name from 
				`tabItem Group` WHERE parent_item_group  = '{filters.get("parent_group")}')"""
	
	data = frappe.db.sql(sql ,as_dict =1)
	return data