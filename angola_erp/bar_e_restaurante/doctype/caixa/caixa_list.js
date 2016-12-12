// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

// render


frappe.listview_settings['Caixa'] = {
	add_fields: ["status_caixa","data_hora"],

	get_indicator: function(doc) {

		if (doc.status_caixa== "Aberto" ) {
			return [__("Aberto " + doc.data_hora), "green"]
		} else if (doc.status_caixa== "Em Curso" ) {
			return [__("Em Curso " + doc.data_hora ), "red"]
		} else if (doc.status_caixa== "Fechado" ) {
			return [__("Fechado "  + doc.data_hora ), "orange"]
		
		}
	},
	colwidths: {"subject": 3, "indicator": 3,"Data e Hora Fecho": 3},

	onload: function(listview){
		frappe.route_options = {
			'status_caixa':['in','Aberto, Em Curso']

		};
	},	
	
};

