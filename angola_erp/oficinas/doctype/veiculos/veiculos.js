// Copyright (c) 2019, Helio de Jesus and contributors
// For license information, please see license.txt

frappe.ui.form.on('Veiculos', {
	onload: function(frm) {
	
		cur_frm.toggle_enable("veiculo_operador",false)
		cur_frm.toggle_enable("veiculo_ultima_revisao",false)
	}
		
});

frappe.ui.form.on('Veiculos', {
	refresh: function(frm) {

	}
});


frappe.ui.form.on('Veiculos','marca',function(frm,cdt,cdn){
	
	frappe.model.set_value(cdt,cdn,'veiculo_operador',frappe.session.user)

	marcas_('Marca Carros',cur_frm.doc.marca)
	cur_frm.refresh_fields('veiculo_operador');


});

frappe.ui.form.on('Veiculos','veiculo_kms',function(frm,cdt,cdn){
	//accept only numbers

});


frappe.ui.form.on('Veiculos','veiculo_ano',function(frm,cdt,cdn){
	//accept only numbers

});

frappe.ui.form.on('Veiculos','veiculo_cilindrada',function(frm,cdt,cdn){
	//accept only numbers

});

frappe.ui.form.on('Veiculos','veiculo_potencia',function(frm,cdt,cdn){
	//accept only numbers

});


frappe.ui.form.on('Veiculos','veiculo_cor',function(frm,cdt,cdn){
	//accept only Letras

});



var marcas_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var d = frappe.model.get_doc(frm,cdt)

		cur_frm.doc.modelo = d.modelo
		cur_frm.refresh_fields();

	});


}

