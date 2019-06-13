// Copyright (c) 2016, Udyam and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Circulation List Report"] = {
	"filters": [
		{
			"fieldname":"circulation_list",
			"label": __("Circulation List"),
			"fieldtype": "Link",
			"options": "Circulation List",
			"reqd": 1,
		}

	]
}
