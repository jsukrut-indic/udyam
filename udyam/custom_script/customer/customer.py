from __future__ import unicode_literals
import frappe
import json
from frappe.utils import flt, cstr, cint, today, getdate
from frappe.model.mapper import get_mapped_doc



@frappe.whitelist()
def make_subscription(source_name,target_doc=None):
	doclist = get_mapped_doc("Customer", source_name, {
		"Customer": {
			"doctype": "Subscription",
			"field_map": {
				"name": "customer"
			}
		},
	}, target_doc)
	return doclist

