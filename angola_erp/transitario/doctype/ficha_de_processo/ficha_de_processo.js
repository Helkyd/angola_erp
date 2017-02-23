// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

var prj

taxacambio= cur_frm.call({method:"angola_erp.util.cambios.cambios",args:{"fonte":"BNA"}})
prj1= cur_frm.call({method:"get_projecto_status_completed",args:{}})

frappe.ui.form.on('Ficha de Processo', {

	before_save: function(frm){
		show_alert("antes de salvar",2)
		if (frm.doc.docstatus ==1) {
			cur_frm.doc.status_process = 'Em Curso'
		}
	},

	after_cancel: function(frm){
		show_alert("vai cancelar o processo",1)
		cur_frm.doc.status_process ='Cancelado'	
		cur_frm.save()
	},

	onload:	function(frm) {
		if (cur_frm.doc.process_number != undefined){
			prj= cur_frm.call({method:"get_projecto_status",args:{"prj":cur_frm.doc.name}})
		}

		if (frm.doc.docstatus == 2) {
			frm.doc.status_process ="Cancelado"
		}

	},

	refresh: function(frm) {
		
		//Taxa de Cambio
		if (taxacambio.responseJSON != undefined && cur_frm.doc.taxa_cambio_bna == 0){
			cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[1]
		}
	
		if (cur_frm.doc.status_process == 'Em Curso'){
			cur_frm.toggle_enable("servicos_processo",false)
			frm.set_df_property("status_process","options","Em Curso\nFechado")
			cur_frm.toggle_enable("customer_reference",false)	
		}else if (cur_frm.doc.status_process == 'Aberto'){
			if (cur_frm.docname.substring(0,3)=="New" || cur_frm.docname.substring(0,3)=="Nov"){
				cur_frm.toggle_enable("servicos_processo",true)
			}else{
				//if (cur_frm.doc.servicos_processo.length !=0) {
				//	cur_frm.toggle_enable("servicos_processo",false)
				//}else{
					cur_frm.toggle_enable("servicos_processo",true)
				//}

			}

		}else if (cur_frm.doc.status_process == 'Fechado'){
			cur_frm.toggle_enable("servicos_processo",false)
			cur_frm.toggle_enable("process_number",false)
			cur_frm.toggle_enable("bil_landing",false)
			cur_frm.toggle_enable("shipping_line",false)
			cur_frm.toggle_enable("status_process",false)
			


		}

		if (cur_frm.doc.status_process == 'Em Curso' && !cur_frm.doc.__islocal || cur_frm.doc.status_process == 'Fechado' ){

			frm.add_custom_button(__("Projecto"), function() {
				cur_frm.reload_doc()
				frappe.route_options = {"project_name": cur_frm.doc.name,"customer": cur_frm.doc.customer_reference}
				frappe.set_route("List", "Project");
			}, "Criar", true);

			frm.add_custom_button(__("Ordens de Venda"), function() {
				cur_frm.reload_doc()
				frappe.route_options = {"project": cur_frm.doc.name, "customer": cur_frm.doc.customer_reference}
				frappe.set_route("List", "Sales Order");
			}, "Criar", true);


		}
		//Assuming already saved now will criate the Projet so Sales Order can also be created.
//		if (frm.doc.docstatus ==1 && cur_frm.doc.status_process == 'Aberto' && frm.docname.substring(0,3) !="New" && frm.docname.substring(0,3) !="Nov") {
			//May should only when docstatus ==1
//			if (cur_frm.doc.servicos_processo) {
//				cur_frm.doc.status_process = "Em Curso"	
				//cur_frm.save() 
//			}
//		}else if (frm.doc.docstatus ==2 && cur_frm.doc.status_process == 'Cancelado') {
			//cur_frm.save()
		if (frm.doc.docstatus == 0) { //(frm.docname.substring(0,3) !="New" && frm.docname.substring(0,3)) {
			cur_frm.doc.status_process ='Aberto'	

		}

		if (cur_frm.docstatus ==1){ //(cur_frm.has_perm("submit")) {
			// close
			if (prj1.responseJSON != undefined){			
				x = 0
				for (x in prj1.responseJSON.message){
					if (prj1.responseJSON.message[x] == cur_frm.doc.name){
						cur_frm.add_custom_button(__('Fechar'), this.close_ficha_processo, __("Status"))
					}
				}
			}
			//if (prj.responseJSON != undefined){
			//	if (prj.responseJSON.message == "Completed") {
			//		cur_frm.add_custom_button(__('Fechar'), this.close_ficha_processo, __("Status"))

			//	}
			//}
		}

	},
	close_ficha_processo: function(){
		cur_frm.cscript.update_status_process("Close", "Fechado")
	}

});

frappe.ui.form.on("Ficha de Processo","process_number",function(frm,cdt,cdn){
	if (cur_frm.doc.taxa_cambio_bna == 0 || cur_frm.doc.taxa_cambio_bna == undefined ) {
		if (taxacambio.responseJSON == undefined){
			cur_frm.doc.taxa_cambio_bna = 0
		}else{
			if ( taxacambio.responseJSON.message == undefined){
			
				cur_frm.doc.taxa_cambio_bna =0
			}else{
				cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[1]
			}
		}
		cur_frm.refresh_fields('taxa_cambio_bna');
	}

});

frappe.ui.form.on("Ficha de Processo","funds_request_currency",function(frm,cdt,cdn){
	if (cur_frm.doc.docstatus ==0){

		if (cur_frm.doc.funds_request_currency =="USD"){
			//if (cur_frm.doc.taxa_cambio_bna == 0 || cur_frm.doc.taxa_cambio_bna == "Undefined" ) {
			cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[1]
			cur_frm.refresh_fields('taxa_cambio_bna');
			//}

		}else if (cur_frm.doc.funds_request_currency =="AKZ"){
			//if (cur_frm.doc.taxa_cambio_bna == 0 || cur_frm.doc.taxa_cambio_bna == "Undefined" ) {
			cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[0]
			cur_frm.refresh_fields('taxa_cambio_bna');
			//}


		}else{
			//Tem que ir buscar o cambio based on the currency selected
			show_alert("Taxa cambio...aguarde",1) 	
		}
	}
});

cur_frm.add_fetch('servico_ficha_processo','standard_rate','preco_ficha_processo')	
cur_frm.add_fetch('servico_ficha_processo','item_name','descricao_ficha_processo')

frappe.ui.form.on("Servicos_Ficha_Processo","servico_ficha_processo",function(frm,cdt,cdn){

	var d =locals[cdt][cdn];

	if (d.servico_ficha_processo !=""){

		servicos_('Item',d.servico_ficha_processo,cdn) 
	}

	if (frm.doc.status_process=="Fechado"){
		//Disable the fields on the table
		frappe.utils.filter_dict(frm.fields_dict["servicos_processo"].grid.docfields, {"fieldname": "servico_ficha_processo"})[0].read_only = true;
		frappe.utils.filter_dict(frm.fields_dict["servicos_processo"].grid.docfields, {"fieldname": "descricao_ficha_processo"})[0].read_only = true;		
		frappe.utils.filter_dict(frm.fields_dict["servicos_processo"].grid.docfields, {"fieldname": "preco_ficha_processo"})[0].read_only = true;	
		frappe.utils.filter_dict(frm.fields_dict["servicos_processo"].grid.docfields, {"fieldname": "qtd_ficha_processo"})[0].read_only = true;

	}else{

		frappe.model.set_value(cdt,cdn,'qtd_ficha_processo',1)
		//frappe.utils.filter_dict(frm.fields_dict["servicos_processo"].grid.docfields, {"fieldname": "preco_ficha_processo"})[0].read_only = true;
		frappe.utils.filter_dict(frm.fields_dict["servicos_processo"].grid.docfields, {"fieldname": "qtd_ficha_processo"})[0].read_only = true;
		//frappe.utils.filter_dict(frm.fields_dict["servicos_processo"].grid.docfields, {"fieldname": "descricao_ficha_processo"})[0].read_only = true;		

	}


});

frappe.ui.form.on('Ficha de Processo','status_process',function(frm,cdt,cdn){
	//When changed to EM CURSO ... copies the info to Project and create the tasks.
	if (cur_frm.doc.status_process == 'Em Curso'){
		if (frm.docname.substring(0,3)=="New" || frm.docname.substring(0,3)=="Nov"){
			alert("Nao se esqueca de salvar primeiro o registo antes de mudar o Status para Em Curso\nDepois de Salvo podera mudar o status e criar o Projecto com as tarefas")
			cur_frm.doc.status_process = "Aberto"
			cur_frm.reload_doc()	
		}else{
			show_alert("Os servicos do Cliente serao criados e incluidos como Projecto!!!",2)
		}
	}else if (cur_frm.doc.status_process == 'Fechado'){
		//Verifica se o Projecto ja esta completed.
		if (prj.responseJSON.message == "Completed"){
			//Pode fechar a Obra ... transfer the list of Material added to Material_obra
			show_alert("Ficha de Processo pode ser fechado !!!",3)
		}else{
			//Ooooopppssss still oopen
			alert("O Projecto " + cur_frm.doc.process_number + " ainda nao esta fechado ou concluido.\nPor favor rever as tarefas alocadas.")
			cur_frm.doc.status_process = "Em Curso"
			cur_frm.reload_doc()	

		}
	}



});

var servicos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var serv = frappe.model.get_doc(frm,cdt)
		if (serv){
			frappe.model.set_value(cdt,cdn,frappe.utils.filter_dict(cur_frm.fields_dict["servicos_processo"].grid.docfields, {"fieldname": "preco_ficha_processo"}),serv.standard_rate)

			frappe.model.set_value(cdt,cdn,frappe.utils.filter_dict(cur_frm.fields_dict["servicos_processo"].grid.docfields, {"fieldname": "descricao_ficha_processo"}),serv.item_name)

		}
		cur_frm.refresh_fields('preco_ficha_processo','descricao_ficha_processo');

	});


}

