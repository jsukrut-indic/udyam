frappe.ui.form.on("Supplier", {
	onload: function (frm) {
	},
	refresh:function(frm){
		if(frm.doc.customer){
			frm.set_df_property("is_customer","read_only",1);
		}
	}	
});