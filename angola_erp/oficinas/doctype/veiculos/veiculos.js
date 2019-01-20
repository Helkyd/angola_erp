// Copyright (c) 2019, Helio de Jesus and contributors
// For license information, please see license.txt

frappe.ui.form.on('Veiculos', {
	onload: function(frm) {
	
		cur_frm.toggle_enable("veiculo_operador",false)
		cur_frm.toggle_enable("veiculo_ultima_revisao",false)
	},

	validate: function(frm){
		//validation of plates
		if (cur_frm.doc.matricula.length < 8 ){
			frappe.show_alert('Matricula tem que ter 11 ou 8 digitos')	
			validated = false
		} else if (cur_frm.doc.matricula.length < 11 && cur_frm.doc.matricula.length != 8){
			frappe.show_alert('Matricula tem que ter 11 ou 8 digitos')
			validated = false
		}
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

frappe.ui.form.on('Veiculos','matricula',function(frm,cdt,cdn){
	//check for lenght and format... 
	//ld0101ld
	if (cur_frm.doc.matricula.length < 8 ){
		frappe.show_alert('Matricula tem que ter 11 ou 8 digitos')	
	} else if (cur_frm.doc.matricula.length < 11 && cur_frm.doc.matricula.length != 8){
		frappe.show_alert('Matricula tem que ter 11 ou 8 digitos')
	}
	//format the plate	
	console.log('plates')
	if (cur_frm.doc.matricula.length == 8 ){
		var tmp_plate = ""
		for (x in cur_frm.doc.matricula) {

			if (x == 1 || x == 3 || x == 5 ){
				tmp_plate += x + "-"

			} else {
				tmp_plate += cur_frm.doc.matricula[x]
			}

		}
		cur_frm.doc.matricula = tmp_plate
		cur_frm.refresh_fields('matricula');

	}else if (cur_frm.doc.matricula.length = 11 ){
		console.log('Nao faz nada...esta certo')
	}
});



var marcas_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var d = frappe.model.get_doc(frm,cdt)

		cur_frm.doc.modelo = d.modelo
		cur_frm.refresh_fields();

	});


}

