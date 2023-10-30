


# run a test using module path
# bench --site [sitename] run-tests --module frappe.tests.test_api
#bench --site watny run-tests --module  dynamic.dynamic.test_data --test test_emolyee_name
#/home/abanoub/frappe-13/apps/dynamic/dynamic/test_data.py
import frappe
import unittest
from frappe.utils import getdate



class TestEvent(unittest.TestCase):
    def test_emolyee_name(self):
        doc = frappe.get_doc({
            "doctype":'Employee',
            "first_name":'abanoub',
            "middle_name":'mn',
            "last_name":'bakheet',
            "gender":'Male',
            "date_of_birth":getdate('08-05-1996'),
            "date_of_joining":getdate('23-10-2023'),
        }).insert()

        self.assertEqual(doc.employee_name,'abanoub xx bakheet')