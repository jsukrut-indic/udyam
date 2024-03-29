# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "udyam"
app_title = "Udyam"
app_publisher = "Udyam"
app_description = "Udyam Prakashan Pvt. Ltd."
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "office@udyamprakashan.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/udyam/css/udyam.css"
# app_include_js = "/assets/udyam/js/udyam.js"

# include js, css files in header of web template
# web_include_css = "/assets/udyam/css/udyam.css"
# web_include_js = "/assets/udyam/js/udyam.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "udyam.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "udyam.install.before_install"
# after_install = "udyam.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "udyam.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"udyam.tasks.all"
# 	],
# 	"daily": [
# 		"udyam.udyam.doctype.circulation_list.circulation_list.circulation_details_scheduler"
# 	],
# 	"hourly": [
# 		"udyam.tasks.hourly"
# 	],
# 	"weekly": [
# 		"udyam.tasks.weekly"
# 	]
# 	"monthly": [
# 		"udyam.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "udyam.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "udyam.event.get_events"
# }

scheduler_events = {
	"all": [
		"udyam.udyam.doctype.circulation_list.circulation_list.circulation_details_scheduler"
	],
	"daily": [
		"udyam.udyam.doctype.circulation_details.circulation_details.create_delivery_note"
	],
	# "hourly": [
	# 	"udyam.tasks.hourly"
	# ],
	# "weekly": [
	# 	"udyam.tasks.weekly"
	# ]
	# "monthly": [
	# 	"udyam.tasks.monthly"
	# ]
}

doctype_js = {
	"Customer" : "custom_script/customer/customer.js",
	"Supplier" : "custom_script/supplier/supplier.js",
	"Purchase Invoice":"custom_script/purchase_invoice/purchase_invoice.js"

}

fixtures = ["Custom Field", "Property Setter","Custom DocPerm","Print Format", "Letter Head", "Workflow State", "Workflow Action", "Workflow", "Address Template","Web Page","Report"]

doc_events = {
	"Supplier": {
        "validate": "udyam.custom_script.supplier.supplier.validate",
    },
   
}
