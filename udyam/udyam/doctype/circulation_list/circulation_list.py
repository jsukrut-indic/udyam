# -*- coding: utf-8 -*-
# Copyright (c) 2019, Udyam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
import datetime
from frappe.utils import flt, getdate, get_first_day,get_last_day

class CirculationList(Document):
	def autoname(self):
		current_date = datetime.date.today()
		cur_year = current_date.strftime('%y')
		fiscal_year = str(cur_year) + str(int(cur_year) + 1) 
		self.name = make_autoname(str('CL') + "/" + fiscal_year + "/.#######")
	
	def validate(self):
		suppliers_postal_codes = self.get_suppliers_postal_codes()
		customers = self.get_customers_from_pin_codes(suppliers_postal_codes)
		filtered_customers = self.filter_customer(customers)
		self.filtered_customers = str(filtered_customers)

	def get_suppliers_postal_codes(self):
		suppliers_postal_codes = frappe.get_all('Suppliers Postal Codes',filters={'parent': self.supplier},fields = ["pin_code", "place"])
		return suppliers_postal_codes
	
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
	
	def filter_customer(self,customers):
		filtered_customers = []
		customers = tuple([x.encode('UTF8') for x in list(customers) if x])
		# Filtration of customer having item_group(Magazine) Service
		customers_having_magazine = frappe.db.sql(""" select  parent from tabMagazines 
									where item_group='{0}' and parent in {1}""".format(self.item_group,customers),as_dict=1)
		customers = [ cust.get('parent') for cust in customers_having_magazine if cust]
		customers = tuple([x.encode('UTF8') for x in list(customers) if x])

		# filtration of customer having Paid Subscription,Free Subscription,Is fixed Subcription
		cust_having_paid_subs = frappe.db.sql(""" select distinct name from tabCustomer 
									where (customer_category in ('Subscriber - Paid','Subscriber - Free') or is_fixed_subscription = 1) 
									and name in {0}""".format(customers),as_dict=1)
		cust_having_paid_subs = [ cust.get('name') for cust in cust_having_paid_subs if cust]
		filtered_customers.extend(cust_having_paid_subs)

		# filtration of author and advertiser having document in current month.
		first_date_of_month = get_first_day(getdate())
		last_date_of_month = get_last_day(getdate())
		authors_and_advertiser = frappe.db.sql(""" select customer from `tabMagazine Details` where document_date between 
											'{0}' and '{1}' 
											and customer in {2} """.format(first_date_of_month,last_date_of_month,customers),as_dict=1,debug=1)
		authors_and_advertiser = [ cust.get('customer') for cust in authors_and_advertiser if cust]
		filtered_customers.extend(authors_and_advertiser)
		return filtered_customers
