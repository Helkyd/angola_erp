// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

frappe.query_reports["General Ledger 1"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"account",
			"label": __("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"get_query": function() {
				var company = frappe.query_report_filters_by_name.company.get_value();
				return {
					"doctype": "Account",
					"filters": {
						"company": company,
					}
				}
			}
		},
		{
			"fieldname":"voucher_no",
			"label": __("Voucher No"),
			"fieldtype": "Data",
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldtype": "Break",
		},
		{
			"fieldname":"party_type",
			"label": __("Party Type"),
			"fieldtype": "Link",
			"options": "Party Type",
			"default": ""
		},
		{
			"fieldname":"party",
			"label": __("Party"),
			"fieldtype": "Dynamic Link",
			"get_options": function() {
				var party_type = frappe.query_report_filters_by_name.party_type.get_value();
				var party = frappe.query_report_filters_by_name.party.get_value();
				if(party && !party_type) {
					frappe.throw(__("Please select Party Type first"));
				}
				return party_type;
			}
		},
		{
			"fieldname":"group_by_voucher",
			"label": __("Group by Voucher"),
			"fieldtype": "Check",
			"default": 1
		},
		{
			"fieldname":"group_by_account",
			"label": __("Group by Account"),
			"fieldtype": "Check",
		}
	],
	"formatter":function (row, cell, value, columnDef, dataContext, default_formatter) {
				value = default_formatter(row, cell, value, columnDef, dataContext);
		if (columnDef.id == "Debit") {
			if(dataContext.Debit>1){
                        	value = "<span style='color:blue;font-weight:bold'>" + value + "</span>";
                        }
                        msgprint(dataContext.Debit)

		}


		if (dataContext.Debit) {
            	}

            	return value;
        }
	formatter();
}
