from __future__ import unicode_literals
import frappe
import json
from frappe.utils import flt, cstr, cint, today, getdate
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def validate(doc,method=None):
	if doc.is_customer and not doc.customer:
		customer = create_customer(doc)
		if customer:
			doc.customer = customer
			frappe.db.set_value("Customer",customer, "supplier",doc.name)
			frappe.db.set_value("Customer",customer, "is_supplier",1)
			frappe.msgprint("Associated Customer Created For Author")

@frappe.whitelist()
def create_customer(doc):
	if doc:
		try:
			if not frappe.db.get_value("Customer", {"name":doc.supplier_name }, "name"):	
				if not frappe.db.get_value("Customer Group", {"name":doc.supplier_group }, "name"):
					group_details ={'name':doc.supplier_group}
					customer_group = create_customer_group(group_details)
					
				customer_doc = frappe.new_doc("Customer")
				customer_doc.customer_name = doc.supplier_name
				customer_doc.customer_group = doc.supplier_group
				customer_doc.customer_type = doc.supplier_type
				customer_doc.company_name = doc.company_name
				customer_doc.customer_category = "Authors"
				customer_doc.tax_id = doc.tax_id
				customer_doc.default_bank_account = doc.default_bank_account
				customer_doc.language = doc.language
				customer_doc.website = doc.website
				customer_doc.default_currency = doc.default_currency
				customer_doc.customer_details = doc.supplier_details
				customer_doc.flags.ignore_mandatory = True
				customer_doc.save(ignore_permissions=False)
				if customer_doc:
					map_address_contact(doc,customer_doc)
					return customer_doc.name
			else:
				frappe.throw("There is already customer with name <b> {0} </b>".format(doc.supplier_name))
		except Exception as e:
			raise e

@frappe.whitelist()
def create_customer_group(group_details):
	if group_details:
		customer_group_doc = frappe.new_doc("Customer Group")
		customer_group_doc.parent_customer_group = frappe.db.get_value("Customer Group", {"lft":1}, "name")
		customer_group_doc.customer_group_name = group_details.get('name')
		customer_group_doc.save(ignore_permissions=False)
		if customer_group_doc.name:
			return customer_group_doc.name


@frappe.whitelist()
def map_address_contact(source_doc,target_doc):
	try:
		if source_doc and target_doc:
			lined_contacts_and_addresses =  frappe.get_all('Dynamic Link',filters={'link_name': source_doc.name,'link_doctype':source_doc.doctype},
						fields = ["parenttype", "parent"],debug=1)
	
			if lined_contacts_and_addresses:		
				for contact_or_address in lined_contacts_and_addresses:
					
					if contact_or_address.get('parenttype') == 'Contact' and contact_or_address.get('parent'):
						contact_doc = frappe.get_doc("Contact",contact_or_address.get('parent'))

						link = contact_doc.append("links", {})
						link.link_name = target_doc.name
						link.link_doctype = target_doc.doctype
						contact_doc.save(ignore_permissions=False)
					
					if contact_or_address.get('parenttype') == 'Address':
						address_doc = frappe.get_doc("Address",contact_or_address.get('parent'))

						link = address_doc.append("links", {})
						link.link_name = target_doc.name
						link.link_doctype = target_doc.doctype
						address_doc.save(ignore_permissions=False)
	except Exception as e:
		raise e
	
	