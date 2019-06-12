frappe.ui.form.on("Supplier", {

	refresh:function(frm){
		if(frm.doc.customer){
			frm.set_df_property("is_customer","read_only",1);
		}
	}	
});