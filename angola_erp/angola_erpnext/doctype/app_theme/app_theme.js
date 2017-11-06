// Copyright (c) 2017, Helio de Jesus and contributors
// For license information, please see license.txt



/* globals jscolor */
frappe.provide("frappe.website_theme");
$.extend(frappe.website_theme, {
	color_variables: ["background_color", "top_bar_color", "top_bar_text_color",
		"footer_color", "footer_text_color", "text_color", "link_color"]
});

frappe.ui.form.on("App Theme", "onload_post_render", function(frm) {
	frappe.require('assets/frappe/js/lib/jscolor/jscolor.js', function() {
		$.each(frappe.website_theme.color_variables, function(i, v) {
			$(frm.fields_dict[v].input).addClass('color {required:false,hash:true}');
		});
		jscolor.bind();
	});
});

frappe.ui.form.on("App Theme", "onload", function(frm) {
	console.log('Inicio')
	var dd = document.createElement('link')
	dd.setAttribute('rel','stylesheet')
	dd.setAttribute('type','text/css')
	dd.setAttribute('href','assets/angola_erp/css/erpnext/bootstrap.css?ver=1509829457.0')
	document.getElementsByTagName('head')[0].appendChild(dd)
	
	cur_frm.set_value('background_color',$("#body_div").css("background-color"))
	cur_frm.set_value('font_size',$("#body_div").css("font-size"))

	//Should read the default settings from the APP theme ...
	//css_file='./assets/css/desk.min.css'

	css_file='./assets/angola_erp/css/bootstrap.css'
	
	$.get(css_file, function (cssText) {
		//console.log(cssText)

		//frm.doc.css = ".navbar-header {			display: true;		  }"
		//frm.doc.css = '<style />' + cssText;
		cur_frm.set_value('css',cssText)
		console.log('css')

	});
	

});

frappe.ui.form.on("App Theme", "refresh", function(frm) {
	console.log('Refresh')
	
	
	frm.set_intro(__('Default theme is set in {0}', ['<a href="#Form/Website Settings">'
		+ __('Website Settings') + '</a>']));

	frm.toggle_display(["module", "custom"], !frappe.boot.developer_mode);

	if (!frm.doc.custom && !frappe.boot.developer_mode) {
		frm.set_read_only();
		frm.disable_save();
	} else {
		frm.enable_save();
	}
});


frappe.ui.form.on("App Theme", "theme", function(frm,cdt,cdn){
	console.log('theme')
	
});	


frappe.ui.form.on("App Theme","background_color", function (frm,cdt,cdn) {
	console.log ('Aplica cor no fundo')
	$("#body_div").css("background-color", frm.doc.background_color);
	$("#page_modules").css("background-color", frm.doc.background_color);
	//document.querySelector("<link type="text/css" rel="stylesheet" href="assets/angola_erp/css/bootstrap.css") <link type="text/css" rel="stylesheet" href="assets/angola_erp/css/erpnext/bootstrap.css">)
	

});

frappe.ui.form.on("App Theme","font_size", function (frm,cdt,cdn) {
	console.log ('Aplica tamanho Fonte')
	$("#body_div").css("font-size", frm.doc.font_size);

});