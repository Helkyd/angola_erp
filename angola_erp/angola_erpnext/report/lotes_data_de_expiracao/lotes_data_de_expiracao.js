// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lotes data de Expiracao"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.sys_defaults.year_start_date,
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"in_days",
			"label": __("Expiry (In Days)"),
			"fieldtype": "Data",
			"width": "10",
			"default": 90
		},

	]
}
