# -*- coding: utf-8 -*-
# Copyright (c) 2019, Udyam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
import datetime,json
from frappe.utils import flt, getdate, get_first_day,get_last_day,add_days,nowdate

class CirculationList(Document):
	def autoname(self):
		current_date = datetime.date.today()
		cur_year = current_date.strftime('%y')
		fiscal_year = str(cur_year) + str(int(cur_year) + 1) 
		self.name = make_autoname(str('CL') + "/" + fiscal_year + "/.#######")
	
	def validate(self):
		pass
	def after_insert(self):
		result = make_circulation_details_records(self.name)
		if result:
			make_po_from_circulation_list(self.name)



@frappe.whitelist()
def make_circulation_details_records(name):
	if name:
		circulation_list_doc = frappe.get_doc("Circulation List",name)
		if circulation_list_doc:
			suppliers_postal_codes = get_suppliers_postal_codes(circulation_list_doc)
			customers = get_customers_from_pin_codes(circulation_list_doc,suppliers_postal_codes)
			filtered_customers = filter_customer(circulation_list_doc,customers)
			try:
				for customer_data in filtered_customers:
					create_circulation_details(circulation_list_doc,customer_data)
			except Exception, e:
				return False
			return True

@frappe.whitelist()
def create_circulation_details(circulation_list_data,customer_data):
	if circulation_list_data and customer_data:
		circulation_details_doc = frappe.new_doc("Circulation Details")
		circulation_details_doc.circulation_list = circulation_list_data.name
		circulation_details_doc.customer = customer_data.get('customer')
		circulation_details_doc.address = customer_data.get('address').split(',')[0]
		circulation_details_doc.contact = customer_data.get('contact')
		circulation_details_doc.qty = 1
		circulation_details_doc.transaction_date = circulation_list_data.posting_date
		circulation_details_doc.save()
		frappe.db.commit()

@frappe.whitelist()
def get_suppliers_postal_codes(self):
	suppliers_postal_codes = frappe.get_all('Suppliers Postal Codes',filters={'parent': self.supplier},fields = ["pin_code", "place"])
	return suppliers_postal_codes

@frappe.whitelist()
def get_customers_from_pin_codes(self,suppliers_postal_codes):
	postal_codes = []
	for postal_code in suppliers_postal_codes:
		postal_codes.append(postal_code.pin_code)
	pin_codes = tuple(postal_codes)
	postal_code= tuple([x.encode('UTF8') for x in list(pin_codes) if x])
	servicable_customers = frappe.db.sql(""" SELECT link.link_name FROM tabAddress address INNER JOIN `tabDynamic Link` link 
				ON address.name = link.parent 
				where address.pincode in {0}""".format(postal_code),as_dict=1)
	customers = [ cust.get('link_name') for cust in servicable_customers if cust]
	return customers

@frappe.whitelist()
def filter_customer(self,customers):
	filtered_customers = []
	customers = tuple([x.encode('UTF8') for x in list(customers) if x])
	
	# Filtration of customer having item_group(Magazine) Service
	customers_having_magazine = frappe.db.sql(""" select  parent from tabMagazines 
								where item_group='{0}' and parent in {1}""".format(self.item_group,customers),as_dict=1)
	customers = [ cust.get('parent') for cust in customers_having_magazine if cust]
	customers = tuple([x.encode('UTF8') for x in list(customers) if x])

	# Filtration of customer having Paid Subscription,Free Subscription,Is fixed Subcription
	cust_having_paid_subs = frappe.db.sql(""" select distinct name from tabCustomer 
								where (customer_category in ('Subscriber - Paid','Subscriber - Free') or is_fixed_subscription = 1) 
								and name in {0}""".format(customers),as_dict=1)
	cust_having_paid_subs = [ cust.get('name') for cust in cust_having_paid_subs if cust]
	filtered_customers.extend(cust_having_paid_subs)

	# Filtration of author and advertiser having document in current month.
	first_date_of_month = get_first_day(getdate())
	last_date_of_month = get_last_day(getdate())
	authors_and_advertiser = frappe.db.sql(""" select customer from `tabMagazine Details` where document_date between 
										'{0}' and '{1}' 
										and customer in {2} """.format(first_date_of_month,last_date_of_month,customers),as_dict=1)
	authors_and_advertiser = [ cust.get('customer') for cust in authors_and_advertiser if cust]
	filtered_customers.extend(authors_and_advertiser)
	
	# Mapping Address with Customer 
	filtered_customers_tuple = tuple([x.encode('UTF8') for x in list(filtered_customers) if x])
	filtered_customers_data = frappe.db.sql(""" select link_name as customer,
						GROUP_CONCAT(case when parenttype='Address' then parent end) address, 
						GROUP_CONCAT(case when parenttype='Contact' then parent end) contact 
						from `tabDynamic Link` where link_name in {0} group by 1 """.format(filtered_customers_tuple),as_dict=1)
	return filtered_customers_data

@frappe.whitelist()
def make_po_from_circulation_list(name):
	po_items = []
	po_details = {}
	if name:
		circulation_list_doc = frappe.get_doc("Circulation List",name)
		po_details['supplier'] = circulation_list_doc.supplier
		po_details['circulation_list'] = circulation_list_doc.name
		po_details['transaction_date'] =  circulation_list_doc.posting_date
		supplier_warehouse = frappe.db.get_value("Supplier",{'name':circulation_list_doc.supplier},"warehouse")
		po_details['supplier_warehouse'] = supplier_warehouse
		if circulation_list_doc:
			pincode_wise_qty = frappe.db.sql(""" select pincode,sum(qty) as qty from `tabCirculation Details` where 
				circulation_list ='{0}' group by pincode""".format(circulation_list_doc.name),as_dict=1)
			if pincode_wise_qty:
				pincodes = [ pincode_data.get('pincode') for pincode_data in pincode_wise_qty if pincode_data]
				pincodes_tuple = tuple([x.encode('UTF8') for x in list(pincodes) if x])
				pincode_rates = frappe.db.sql("""select pin_code,rate  from `tabSuppliers Postal Codes` where 
								parent ='{0}' and pin_code in {1} """.format(circulation_list_doc.supplier,pincodes_tuple),as_dict=1)
				for pincode_data in pincode_wise_qty:
					rate = get_rate(pincode_data.get('pincode'),pincode_rates)
					temp = {
						'item_code':circulation_list_doc.item,
						'qty': pincode_data.get('qty'),
						'rate': rate,
						'postal_code': pincode_data.get('pincode'),
						'warehouse': supplier_warehouse
					}
					po_items.append(temp)
	purchase_order = create_purchase_order(po_details,po_items)
	if purchase_order:
		circulation_list_doc.purchase_order = purchase_order
		circulation_list_doc.save()

@frappe.whitelist()
def get_rate(pincode,pincode_rates):
	if pincode and pincode_rates:
		for pin in pincode_rates:
			if pin.get('pin_code') == pincode:
				return pin.get('rate')
			else: 
				return 0

@frappe.whitelist()
def create_purchase_order(args,item_args):
	try:
		po = frappe.new_doc("Purchase Order")
		args = frappe._dict(args)
		if args.transaction_date:
			po.transaction_date = args.transaction_date

		po.schedule_date = add_days(nowdate(), 1)
		po.supplier = args.supplier
		po.company = frappe.defaults.get_defaults().company
		po.currency = frappe.defaults.get_defaults().currency
		po.circulation_list = args.get('circulation_list')
		# po.conversion_factor = args.conversion_factor or 1
		# po.supplier_warehouse = args.supplier_warehouse or None

		for item in item_args:
			po.append("items", {
				"item_code": item.get('item_code'),
				"warehouse": item.get('warehouse'),
				"qty": item.get('qty'),
				"rate": item.get('rate'),
				"schedule_date": add_days(nowdate(), 1)
				# "include_exploded_items": args.get('include_exploded_items', 1)
			})
		po.insert()
		po.submit()
		return po.name
	except Exception, e:
		return False

	