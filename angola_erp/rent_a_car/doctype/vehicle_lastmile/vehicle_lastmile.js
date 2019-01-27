// Copyright (c) 2019, Helio de Jesus and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle_lastmile', {
	refresh: function(frm) {

	}
});

frappe.ui.form.on('Vehicle_lastmile','matricula',function(frm,cdt,cdn){

	veiculos_('Vehicle',cur_frm.doc.matricula)
});


var veiculos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var carro = frappe.model.get_doc(frm,cdt)
		if (carro){
			cur_frm.doc.chassis = carro.chassis_no

		}
		
		cur_frm.refresh_fields();

	});


}

