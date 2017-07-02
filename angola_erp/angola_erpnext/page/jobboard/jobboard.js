//frappe.provide("erpnext.pos");
//frappe.provide('angola_erp.testgrid');
frappe.provide('frappe.pages');
frappe.provide('frappe.views');


frappe.require("assets/frappe/js/lib/slickgrid/slick.grid.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.grid.css");
frappe.require("assets/frappe/js/lib/slickgrid/slick.core.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.editors.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.formatters.js");
frappe.require("assets/frappe/js/lib/slickgrid/slick.dataview.js");


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



frappe.require("assets/angola_erp/js/lib/slickgrid_extended/slickgrid_extended.js");
frappe.require("assets/angola_erp/js/lib/slickgrid_extended/plot_diagram.js");
frappe.require("assets/angola_erp/js/lib/slickgrid_extended/slickgrid_extended.css");

frappe.require("assets/angola_erp/js/lib/flot/jquery-ui.js");
frappe.require("assets/angola_erp/js/lib/flot/jquery-ui.css");
frappe.require("assets/angola_erp/js/lib/flot/jquery.flot.js");
frappe.require("assets/angola_erp/js/lib/flot/jquery.flot.resize.js");
frappe.require("assets/angola_erp/js/lib/flot/jquery.flot.crosshair.js");
frappe.require("assets/angola_erp/js/lib/flot/jquery.flot.time.js");
frappe.require("assets/angola_erp/js/lib/flot/jquery.contextmenu.js");



var cur_page = null;
frappe.pages['jobboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Job Card Creation',
		single_column: true
	});

var columns = [{ id: 'col0', name: 'Time',      toolTip: 'Date/Time',   sort_type: 'date' , plot_master_time: 'true' },
                   { id: 'col1', name: 'Value 1',   toolTip: 'Value 1',     sort_type: 'float',     style: 'text-align: right;'},
                   { id: 'col2', name: 'Value 2',   toolTip: 'Value 2',     sort_type: 'float',     style: 'text-align: right;'},
                   { id: 'col3', name: 'Value 3',   toolTip: 'Value 3',     sort_type: 'float',     style: 'text-align: right;'},
    ];                                                                                                                      
                                                                                                                            
    var options = { caption:            'Time line with diagram',                 
                    width:              '100%',                                                                             
                    maxHeight:          '100',                                                                              
                    locale:              'en',
    };                                                                                                                      
                                                                                                                            
    var data = [{ col0: '2013/10/01 14:05', col1: '66,20', col2: '12124', col3: '12' },
                { col0: '2013/10/01 14:10', col1: '22,10', col2: '23344', col3: '22' },
                { col0: '2013/10/01 14:20', col1: '33,40', col2: '65472', col3: '55' },
                { col0: '2013/10/01 14:30', col1: '77,90', col2: '81224', col3: '22' },
                { col0: '2013/10/01 14:40', col1: '10,20', col2: '12421', col3: '55' },
                { col0: '2013/10/01 14:50', col1: '12,24', col2: '23552', col3: '88' },
                { col0: '2013/10/01 15:00', col1: '88,20', col2: '36333', col3: '65' },
                { col0: '2013/10/01 15:20', col1: '45,30', col2: '23355', col3: '14' },
                { col0: '2013/10/01 15:40', col1: '55,40', col2: '23566', col3: '23' },
    ];                                                                                                                      

	$("<table width='100%>\
	  <tr>\
	    <td valign='top' width='50%'>\
	      <div id='demo_div' style='width:600px;height:500px;''></div>\
	    </td>\
	  </tr>\
	</table>").appendTo($(wrapper).find('.layout-main-section'));
                                                                                                                            
    var additional_menu_entries = [{ label: 'Additional entry', hint: 'Additional entry just for fun', action: function(t){alert('Just for fun');} }];   
                                                                                                                            
    createSlickGridExtended('demo_div', data, columns, options, additional_menu_entries);                                                            


}
