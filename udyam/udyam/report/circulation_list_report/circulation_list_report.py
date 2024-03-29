# Copyright (c) 2013, Udyam and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_data(filters):
	if filters:
		circulation_list = filters['circulation_list']
		data = frappe.db.sql(""" SELECT CL.name, CD.name,CD.customer,CD.customer_name,CD.company_name,CD.address,
							CD.address_title,CD.address_line1,CD.city,CD.state,CD.pincode,CD.phone,CD.qty,CD.tracking_id,
							CD.booking_status,CD.transaction_date,CD.delivery_date,CD.transaction_status
							FROM `tabCirculation List` CL
							INNER JOIN `tabCirculation Details` CD
							ON CL.name =CD.circulation_list
							where CL.name ='{0}'""".format(circulation_list))
		return data


def get_columns():
	columns = [
		{
			"fieldname": "circulation_list",
			"label": _("Circulation List"),
			"fieldtype": "Link",
			"options": "Circulation List",
			"width": 100
		},
		{
			"fieldname": "circulation_Detail",
			"label": _("Circulation Detail"),
			"fieldtype": "Link",
			"options": "Circulation Detail",
			"width": 100
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "customer_name",
			"label": _("Full Name"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "company_name",
			"label": _("Company Name"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "address",
			"label": _("Address"),
			"fieldtype": "data",
			"width": 90
		},
		{
			"fieldname": "address_title",
			"label": _("Address Title"),
			"fieldtype": "data",
			"width": 90
		},
		{
			"fieldname": "address_line1",
			"label": _("Address Line 1"),
			"fieldtype": "data",
			"width": 90
		},
		{
			"fieldname": "city",
			"label": _("City"),
			"fieldtype": "data",
			"width": 90
		},
		{
			"fieldname": "state",
			"label": _("State"),
			"fieldtype": "data",
			"width": 120
		},
		{
			"fieldname": "pin_code",
			"label": _("Pin Code"),
			"fieldtype": "Data",
			"width": 170
		},
		{
			"fieldname": "mobile_no",
			"label": _("Mobile No"),
			"fieldtype": "Data",
			"width": 170
		},
		{
			"fieldname": "qty",
			"label": _("Qty"),
			"fieldtype": "float",
			"width": 170
		},
		{
			"fieldname": "tracking_id",
			"label": _("Tracking id"),
			"fieldtype": "Data",
			"width": 170
		},
		{
			"fieldname": "booking_status",
			"label": _("Booking Status"),
			"fieldtype": "Data",
			"width": 170
		},
		{
			"fieldname": "transaction_date",
			"label": _("Transaction Date"),
			"fieldtype": "Date",
			"width": 170
		},
		{
			"fieldname": "delivery_date",
			"label": _("Delivery Date"),
			"fieldtype": "Date",
			"width": 170
		},
		{
			"fieldname": "transaction_status",
			"label": _("Transaction Status"),
			"fieldtype": "Data",
			"width": 170
		},
	]

	return columns