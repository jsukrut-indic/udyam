// Copyright (c) 2019, Udyam and contributors
// For license information, please see license.txt

frappe.ui.form.on('Magazine Details', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			frm.set_df_property("customer","read_only",1);
		}

	},
	category:function(frm){
		if (frm.doc.category =='Advertiser'){
			frm.set_df_property("supplier","reqd",0);
			frm.set_df_property("customer","reqd",1);
		}
		else if (frm.doc.category =='Author'){
			frm.set_df_property("supplier","reqd",1);
			frm.set_df_property("customer","reqd",0);
			frm.set_df_property("customer","read_only",1);
		}
		else{
			frm.set_df_property("supplier","reqd",0);
			frm.set_df_property("customer","reqd",0);
		}
	},
	supplier:function(frm){
		var customer =''
		frappe.db.get_value("Supplier", {"name": frm.doc.supplier}, "customer", (r) => {
			customer= r.customer
			frm.set_value("customer",customer);
			frm.set_value("customer_name",frm.doc.supplier);
			
		});
		
		// frappe.db.get_value("Customer", {"name": frm.doc.customer}, "customer_name", (r) => {
		// 	var customer_name= r.customer_name
		// 	frm.set_value("customer_name",supplier);
			
		// });

	}
});


cur_frm.fields_dict["supplier"].get_query = function(doc) {
	return {
			filters: { supplier_group:'Author'
	  		}
	};
};

cur_frm.fields_dict["customer"].get_query = function(doc) {
	return {
			filters: { customer_group:'Advertiser',customer_category:'Advertiser'
	  		}
	};
};
  