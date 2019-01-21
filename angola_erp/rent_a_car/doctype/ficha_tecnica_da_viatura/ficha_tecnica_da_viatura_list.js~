// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


// render
frappe.listview_settings['Atendimento Bar'] = {
	add_fields: ["status_atendimento","hora_atendimento"],

	get_indicator: function(doc) {

		if (doc.status_atendimento== "Livre" ) {
			return [__("Livre  " ), "green"]
		} else if (doc.status_atendimento== "Ocupado" ) {
			return [__("Ocupado " + frappe.format(doc.hora_atendimento,{"fieldtype":"Date"})), "red"]
		} else if (doc.status_atendimento== "Fechado" ) {
			return [__("Fechado" ), "orange"]
		
		}
	},
	colwidths: {"subject": 3, "indicator": 3.1,"Empregado de Mesa": 2},

	onload: function(listview){
		frappe.route_options = {
			"status_atendimento":"Ocupado"
		};
	},	
	
};


