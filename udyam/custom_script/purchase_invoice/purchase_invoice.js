frappe.ui.form.on("Purchase Invoice", {

	validate:function(frm){
		if(frm.doc.circulation_list && frm.doc.delivered_qty){
			if (frm.doc.delivered_qty !=frm.doc.total_qty){
				frappe.throw("Total Qty Should be Same as Delivered Qty")
			}
		}
	}	
});