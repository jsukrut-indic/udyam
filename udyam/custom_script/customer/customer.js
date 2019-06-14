frappe.ui.form.on("Customer", {

	refresh:function(frm){
		if(frm.doc.name){
			frm.set_df_property("is_supplier","read_only",1);

			frm.add_custom_button(__("Make Subscription"), function() {
				frappe.model.open_mapped_doc({
					method: "udyam.custom_script.customer.customer.make_subscription",
					frm: cur_frm
				});
			});
		}
	}	
});