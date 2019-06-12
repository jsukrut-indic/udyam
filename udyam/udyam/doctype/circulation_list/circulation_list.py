# -*- coding: utf-8 -*-
# Copyright (c) 2019, Udyam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
import datetime

class CirculationList(Document):
	def autoname(self):
		current_date = datetime.date.today()
		cur_year = current_date.strftime('%y')
		fiscal_year = str(cur_year) + str(int(cur_year) + 1) 
		self.name = make_autoname(str('CL') + "/" + fiscal_year + "/.#######")
	
	def validate(self):
		self.get_suppliers_postal_codes()
			
	def get_suppliers_postal_codes(self):
		suppliers_postal_codes = frappe.get_all('Suppliers Postal Codes',filters={'parent': self.supplier},fields = ["pin_code", "place"])
		print "------------------------",suppliers_postal_codes
	
