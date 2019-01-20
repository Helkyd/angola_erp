// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

// render
frappe.listview_settings['Folha de Obras'] = {
	add_fields: ["fo_status"],

	get_indicator: function(doc) {

		if (doc.fo_status== "Aberta" ) {
			return [__("Aberta" ), "green"]
		} else if (doc.fo_status== "Em Curso" ) {
			return [__("Em Curso" ), "red"]
		} else if (doc.fo_status== "Fechada" ) {
			return [__("Fechada" ), "orange"]
		
		}
	},
	colwidths: {"subject": 4, "indicator": 2,"Nome do Cliente": 2},

	onload: function(listview){
		frappe.route_options = {
			"fo_status":['in','Aberta,Em Curso']
		};
	},	
	
};


