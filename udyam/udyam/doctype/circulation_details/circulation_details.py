# -*- coding: utf-8 -*-
# Copyright (c) 2019, Udyam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, get_first_day,get_last_day,add_days,nowdate,nowtime


class CirculationDetails(Document):
	pass


@frappe.whitelist()
def create_delivery_note():
	first_date_of_month = get_first_day(getdate())
	last_date_of_month = get_last_day(getdate())
	circulation_lists = frappe.db.sql(""" select name from `tabCirculation List` where final_closure = 0 and posting_date between 
										'{0}' and '{1}'""".format(first_date_of_month,last_date_of_month),as_dict=1)
	for circulation_list in circulation_lists:
		delivered_circulation_details = frappe.get_all('Circulation Details',
					filters={'circulation_list': circulation_list.get('name'),'transaction_status': 'Delivered','has_delivery_note':0},
					fields = ["name"])
		for circulation_details in delivered_circulation_details:
			make_dn(circulation_details)

@frappe.whitelist()
def make_dn(circulation_details):
	circulation_details_doc = frappe.get_doc("Circulation Details",circulation_details.get('name'))
	if circulation_details_doc.name:
		dn = frappe.new_doc("Delivery Note")
		dn.posting_date = circulation_details_doc.transaction_date
		dn.posting_time = nowtime()
		dn.customer = circulation_details_doc.customer
		dn.company = frappe.defaults.get_defaults().company
		dn.currency = frappe.defaults.get_defaults().currency
		# po.conversion_factor = args.conversion_factor or 1
		# po.supplier_warehouse = args.supplier_warehouse or None
		item = frappe.db.get_value("Circulation List",
						{'name':circulation_details_doc.circulation_list},"item")
		supplier = frappe.db.get_value("Circulation List",
						{'name':circulation_details_doc.circulation_list},"supplier")
		supplier_warehouse = frappe.db.get_value("Supplier",
						{'name':supplier},"warehouse")
		rate = frappe.db.get_value("Suppliers Postal Codes",
								{'parent':supplier,'pin_code':circulation_details_doc.pincode},"rate")
			
		dn.append("items", {
			"item_code": item,
			"warehouse": supplier_warehouse,
			"qty": circulation_details_doc.qty,
			"rate": rate,
		})
	dn.insert()
	dn.submit()

	if dn.name:
		circulation_details_doc.delivery_note = dn.name
		circulation_details_doc.has_delivery_note =1
		circulation_details_doc.save()
		frappe.db.commit()
