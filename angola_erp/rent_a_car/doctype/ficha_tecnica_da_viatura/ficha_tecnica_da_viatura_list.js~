// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


// render
frappe.listview_settings['Ficha Tecnica da Viatura'] = {
	add_fields: ["status_viatura","entrada_ou_saida_viatura","docstatus","data_estimada_entrada_estacao"],

	
	get_indicator: function(doc) {

		if (doc.data_estimada_entrada_estacao < frappe.datetime.nowdate() ) {
			return [__("Em Atraso" ), "blue"]
		} else if (doc.entrada_ou_saida_viatura == "Entrada" ) {
			return [__(doc.entrada_ou_saida_viatura ), "green"]
		} else if (doc.entrada_ou_saida_viatura == "Saida" && doc.status_viatura == "Alugada" ) {
			return [__(doc.status_viatura ), "red"]
		} else if (doc.status_viatura== "Stand-by" ) {
			return [__(doc.status_viatura ), "orange"]
		
		} else if (doc.status_viatura== "Devolvida" ) {
			return [__(doc.status_viatura ), "grey"]

		}

	},
	colwidths: {"subject": 1, "indicator": 4.1},

	onload: function(listview){
		frappe.route_options = {
			'docstatus':['!=',2],
			'status_viatura':'Alugada'

		};
	},

};


