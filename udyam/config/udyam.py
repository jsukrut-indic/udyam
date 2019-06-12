from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
	return [
		{
			"label": _("Documents"),
			"items": [
				{
					"type": "doctype",
					"name": "Magazine Details",
					"description": _("Magazine Details"),
				},	
			]
		},
		{
		"label": _("Masters"),
		"items": [
				{
					"type": "doctype",
					"name": "Postal Codes",
					"description": _("Postal Codes"),
				},
			]
		},
		
	]
