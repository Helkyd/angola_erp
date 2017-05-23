// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


// render
frappe.listview_settings['Cadastro de Processo'] = {
	add_fields: ["status_ou_fase"],


	colwidths: {"subject": 3, "indicator": 3.1,"Nome do Autor (Cliente)": 2},

	onload: function(listview){
		frappe.route_options = {
			'status_ou_fase':['in','Inicial, Em Curso']

		};
	},	
	
};


