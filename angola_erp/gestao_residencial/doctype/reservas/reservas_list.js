// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


// render
frappe.listview_settings['Reservas'] = {
	add_fields: ["numero_quarto", "reservation_status"],

	get_indicator: function(doc) {
		if (doc.reservation_status== "Nova") {
			return [__("Nova "+doc.numero_quarto), "red", "reservation_status,=,Nova"]
		} else if (doc.reservation_status== "Ativo") {
			return [__("Ativo "+doc.numero_quarto), "orange", "reservation_status,=,Ativo"]
		} else if (doc.reservation_status== "Pago") {
			return [__("Pago "+doc.numero_quarto), "green", "reservation_status,=,Pago"]
		} else if (doc.reservation_status== "Cancelada") {
			return [__("Cancelada "+doc.numero_quarto), "blue", "reservation_status,=,Cancelada"]
		} else if (doc.reservation_status== "Fechada") {
			return [__("Fechada "+doc.numero_quarto), "black", "reservation_status,=,Fechada"]

		}
	},
	colwidths: {"subject": 3, "indicator": 3,"Data de Entrada": 3},

	
};


