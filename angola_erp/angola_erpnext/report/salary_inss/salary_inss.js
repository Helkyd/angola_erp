// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


frappe.query_reports["Salary INSS"] = {
	"filters": [
		{
			"fieldname":"date_range",
			"label": __("Date Range"),
			"fieldtype": "DateRange",
			"default": [frappe.datetime.add_months(get_today(),-1), frappe.datetime.get_today()],
			"reqd": 1
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		}
	]
},

frappe.ui.form.ControlDateRange = frappe.ui.form.ControlData.extend({
	make_input: function make_input() {
		this._super();
		this.set_date_options();
		this.set_datepicker();
		this.refresh();
	},
	set_date_options: function set_date_options() {
		var me = this;
		this.datepicker_options = {
			language: "en",
			range: true,
			autoClose: true,
			toggleSelected: false
		};
		this.datepicker_options.dateFormat = frappe.boot.sysdefaults.date_format || 'yyyy-mm-dd';
		this.datepicker_options.onSelect = function () {
			me.$input.trigger('change');
		};
	},
	set_datepicker: function set_datepicker() {
		this.$input.datepicker(this.datepicker_options);
		this.datepicker = this.$input.data('datepicker');
	},
	set_input: function set_input(value, value2) {
		this.last_value = this.value;
		if (value && value2) {
			this.value = [value, value2];
		} else {
			this.value = value;
		}
		if (this.value) {
			this.$input && this.$input.val(this.format_for_input(this.value[0], this.value[1]));
		} else {
			this.$input && this.$input.val("");
		}
		this.set_disp_area();
		this.set_mandatory && this.set_mandatory(value);
	},
	parse: function parse(value) {
		if (value && (value.indexOf(',') !== -1 || value.indexOf('to') !== -1)) {
			var vals = value.split(/[( to )(,)]/);
			var from_date = moment(frappe.datetime.user_to_obj(vals[0])).format('YYYY-MM-DD');
			var to_date = moment(frappe.datetime.user_to_obj(vals[vals.length - 1])).format('YYYY-MM-DD');
			return [from_date, to_date];
		}
	},
	format_for_input: function format_for_input(value1, value2) {
		if (value1 && value2) {
			value1 = frappe.datetime.str_to_user(value1);
			value2 = frappe.datetime.str_to_user(value2);
			return ([value1, value2]);
		}
		return "";
	}

});

