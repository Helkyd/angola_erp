// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

// render
frappe.listview_settings['Mesas'] = {
	add_fields: ["status_mesa"],

	get_indicator: function(doc) {


		if (doc.status_mesa== "Livre" ) {
			return [__("Livre") , "green"]
		} else if (doc.status_mesa== "Ocupada" ) {
			return [__("Ocupada") , "red"]
		} else if (doc.status_mesa== "Reservada" ) {
			return [__("Reservada"), "orange"]
		}
	},

	
};

