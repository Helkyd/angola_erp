// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

frappe.ui.form.on('Quartos', {
	refresh: function(frm) {


		if (frm.doc.name != (frm.doc.numero + "-" + frm.doc.nome_quarto)){

			cur_frm.toggle_enable("status_quarto",false)
		}else if ((frm.doc.status_quarto=="Ocupado") || (frm.doc.status_quarto=="Reservado")){
			cur_frm.toggle_enable("status_quarto",false)
		}

	}
});
