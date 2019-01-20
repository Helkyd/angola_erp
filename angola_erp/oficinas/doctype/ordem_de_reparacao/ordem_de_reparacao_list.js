// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

// render
frappe.listview_settings['Ordem de Reparacao'] = {
	add_fields: ["or_status"],

	get_indicator: function(doc) {

		if (doc.or_status== "Aberta" ) {
			return [__("Aberta" ), "green"]
		} else if (doc.or_status== "Em Curso" ) {
			return [__("Em Curso" ), "red"]
		} else if (doc.or_status== "Fechada" ) {
			return [__("Fechada" ), "orange"]
		
		}
	},
	colwidths: {"subject": 4, "indicator": 2,"Nome do Cliente": 2},

	onload: function(listview){
		frappe.route_options = {
			"or_status":['in','Aberta,Em Curso']
		};
	},	
	
};


