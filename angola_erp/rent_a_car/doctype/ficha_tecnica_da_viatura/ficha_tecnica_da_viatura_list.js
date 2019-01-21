// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


// render
frappe.listview_settings['Ficha Tecnica da Viatura'] = {
	add_fields: ["status_viatura","entrada_ou_saida_viatura"],

	get_indicator: function(doc) {

		if (doc.entrada_ou_saida_viatura == "Entrada" ) {
			return [__("Livre  " ), "green"]
		} else if (doc.entrada_ou_saida_viatura == "Saida" ) {
			return [__("Ocupado " + frappe.format(doc.data_saida_estacao,{"fieldtype":"Date"})), "red"]
		} else if (doc.entrada_ou_saida_viatura== "Stand-by" ) {
			return [__("Stand-by" ), "orange"]
		
		}
	},
	colwidths: {"subject": 3, "indicator": 3.1,"Empregado de Mesa": 2},

	onload: function(listview){
		frappe.route_options = {
			"entrada_ou_saida_viatura":"Saida"
		};
	},	
	
};


