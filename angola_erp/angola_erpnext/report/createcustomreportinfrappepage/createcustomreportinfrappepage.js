// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


frappe.provide('frappe.pages');
frappe.provide('frappe.views');
frappe.provide('sample_register');
frappe.require("assets/frappe/js/lib/slickgrid/slick.grid.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.grid.css");
frappe.require("assets/frappe/js/lib/slickgrid/slick.core.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.editors.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.formatters.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.checkboxselectcolumn.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.rowselectionmodel.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.autotooltips.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellrangedecorator.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellrangeselector.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellcopymanager.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellexternalcopymanager.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellselectionmodel.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.rowselectionmodel.js");
frappe.require("assets/frappe/js/lib/slickgrid/plugins/slick.cellselectionmodel.js");

var cur_page = null;
frappe.pages['jobboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Job Card Creation',
		single_column: true
	});
	var options = {
		doctype: "Sample Entry Register",
		parent: page
	};
	$("<table width='100%>\
  <tr>\
    <td valign='top' width='50%'>\
      <div id='myGrid' style='width:600px;height:500px;''></div>\
    </td>\
  </tr>\
</table>").appendTo($(wrapper).find('.layout-main-section'));
	setTimeout(function(){
		new new sample_register.JobCard(options, wrapper, page);	
	}, 1)
	frappe.breadcrumbs.add("Sample Register");

}

sample_register.JobCard = Class.extend({
	init: function(opts, wrapper,page) {
		$.extend(this, opts);
		this.make_filters(wrapper);
		this.prepare_data();
			this.page.main.find(".page").css({"padding-top": "0px"});
	},
	make_fun: function(){
            this.page.set_title(__("Dashboard") + " - " + __("Job Card Creation"));

     },
    make: function(){
        this._super();
        this.make_fun();
    },
    make_filters: function(wrapper){
		var me = this;
		this.page = wrapper.page;

		this.page.set_primary_action(__("Refresh"),
			function() { me.refresh(); }, "icon-refresh")

		this.department = this.page.add_field({fieldtype:"Link", label:"Sample Entry Register",
			fieldname:"sample_entry_register", options:"Sample Entry Register"});
	},
    create_job: function(){
    	frappe.msgprint("Creating job in JobCard")
     },

	check_formatter: function(row, cell, value, columnDef, dataContext) {
		return repl('<input type="checkbox" data-id="%(id)s" \
			class="plot-check" %(checked)s>', {
				"id": dataContext.id,
				"checked": dataContext.checked ? 'checked="checked"' : ""
			})
	},
	refresh: function(){
		var me = this;
		msgprint("refresh clicked");
		msgprint(this.page.fields_dict.sample_entry_register.get_parsed_value());

//print selected rows data
			var selectedData = [],
			    selectedIndexes;

			selectedIndexes = grid.getSelectedRows();
			jQuery.each(selectedIndexes, function (index, value) {
			  selectedData.push(grid.getData()[value]);
			});
			msgprint(selectedData);  //selected data contains row data of currently selected checkbox
//print selected rows data end
            var rows = grid.getData();
            //msgprint(rows[0]["sampleid"]);
           // msgprint(rows[1]["sampleid"]);
            msgprint(rows[2]["sampleid"]);

        for (r in rows) {
            var row = rows[r]
            for (i = 1; i < 4; ++i) {
                msgprint(rows[r][i]);
            }
        }
	},

	prepare_data: function() {
		var me = this;
	        function requiredFieldValidator(value) {
                if (value == null || value == undefined || !value.length) {
                    return {valid: false, msg: "This is a required field"};
                } else {
                    return {valid: true, msg: null};
                }
            }
	var columns = [ ];
  var options = {
    enableCellNavigation: true,
    enableColumnReorder: false
  };

		var grid;
  		var data=[];
		 frappe.call({
			method: "sample_register.sample_register.page.dashboard.dashboard.get_sample_data",
			type: "GET",
			args: {
				args:{

				}
			},
			callback: function(r){
				if(r.message){
					me.data = r.message;
					me.make_grid(r.message,columns,options)
				}
			}
		});
	},
	make_grid:function(data1,columns,options){
			$(function () {
		    var data = [];

		    for (var i = 0; i<data1.get_sample_data.length; i++) {
		      data[i] = {
		      	checked:true,
		        sampleid: data1.get_sample_data[i][1],
		        customer: data1.get_sample_data[i][2],
		        type: data1.get_sample_data[i][3],
		        priority: 1,
		        standard: "1",
		        test_group: 1
		      };
		    }
		    grid = new Slick.Grid("#myGrid", data, columns, options);
		    
		        var checkboxSelector = new Slick.CheckboxSelectColumn({
      			cssClass: "slick-cell-checkboxsel"
   				 });
    			columns.push(checkboxSelector.getColumnDefinition());
			      columns.push(
    {id: "sample_id", name: "Sample Id", field: "sampleid"},
    {id: "customer", name: "Customer", field: "customer"},
    {id: "type", name: "Type", field: "type"},
    {id: "priority", name: "Priority", field: "priority"},
    {id: "standard", name: "Standard", field: "standard"},
    {id: "test_group", name: "Test Group", field: "test_group"}
			       );

			grid = new Slick.Grid("#myGrid", data, columns, options);	
		    grid.setSelectionModel(new Slick.RowSelectionModel({selectActiveRow: false}));
		    grid.registerPlugin(checkboxSelector);

	        var columnpicker = new Slick.Controls.ColumnPicker(columns, grid, options);


		  })


	},
});


frappe.query_reports["createCustomReportinFrappePage"] = {
	"filters": [

	]
}
