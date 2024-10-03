# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import json
import re
import operator
import frappe

class CalculationSheet(Document):
	pass





@frappe.whitelist()
def operations(equation, data):
    data = json.loads(data)
    
    try:
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        
        split_expression = re.split(r'(\+|\*|\/|\-)', equation)
        split_expression = [item.strip() for item in split_expression if item.strip()]

        stack = []
        
        for item in split_expression:
            if item[0] in ['c', 'd']:  
                index = int(item[1:]) - 1 
                key = item[0] 
                if index < len(data) and key in data[index]:
                    value = data[index][key]
                    stack.append(value)
                else:
                    return False
            elif item.isdigit(): 
                stack.append(int(item))
            elif item in ops: 
                stack.append(item)
            else:
                return False

        if not stack:
            return False

        result = stack.pop(0)
        while stack:
            op = stack.pop(0)
            value = stack.pop(0)
            result = ops[op](result, value)

        return result
    except Exception as e:
        return False


