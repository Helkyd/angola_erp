// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

var prj

taxacambio= cur_frm.call({method:"angola_erp.util.cambios.cambios",args:{"fonte":"BNA"}})
taxacambioLocal = cur_frm.call({method:"angola_erp.util.cambios.cambios_local",args:{"moeda":"USD"}}) //cliente diz USD
prj1= cur_frm.call({method:"get_projecto_status_completed",args:{}})

frappe.ui.form.on('Ficha de Processo', {

	before_save: function(frm){
		frappe.show_alert("antes de salvar",2)
		if (frm.doc.docstatus ==1) {
			cur_frm.doc.status_process = 'Em Curso'
		}
	},

	after_cancel: function(frm){
		frappe.show_alert("vai cancelar o processo",1)
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
			//pega o registo interno em vez do ONLINe vendo que o cliente pode ter alterado...
			cur_frm.doc.taxa_cambio_bna = taxacambioLocal.responseJSON.message[0]["exchange_rate"]

			//cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[1]
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

			frm.clear_custom_buttons()	//Clear the existing one .. so ours can be added.

			//Requisicao de Fundos
			frm.add_custom_button(("Requisicao de Fundos"), function() {				
				cur_frm.reload_doc()
				console.log('rint')
				//var me = this;
				//frappe.route_options = {"name": cur_frm.doc.sales_invoice, "customer":cur_frm.doc.student_name}
				//frappe.route_options = {"project_name": cur_frm.doc.name,"customer": cur_frm.doc.customer_reference}
				//frappe.set_route('query-report#Requisicao_de_Fundos', cur_frm.doctype,cur_frm.docname);
				//var html = frappe.render("Requisicao_de_Fundos", cur_frm.doc)	
				//cur_frm.print_preview.print_formats[1]
				//ur_frm.print_preview.preview(cur_frm.print_preview.print_formats[1])
				//cur_frm.print_preview.get_print_format(cur_frm.print_preview.print_formats[1])
				//cur_frm.print_preview.selected_format(cur_frm.print_preview.print_formats[1])
				cur_frm.print_preview.printit(1)
				//me.print_document(html)
				//frappe.query_reports["Requisicao de Fundos"];
				//frappe.query_report.load();

			});

			//Project
			frm.add_custom_button((cur_frm.doc.project), function() {				
				cur_frm.reload_doc()
				//frappe.route_options = {"name": cur_frm.doc.sales_invoice, "customer":cur_frm.doc.student_name}
				frappe.route_options = {"project_name": cur_frm.doc.name,"customer": cur_frm.doc.customer_reference}
				frappe.set_route("List", "Project");

			});
			
			//Sales Order
			frm.add_custom_button((cur_frm.doc.sales_order), function() {				
				cur_frm.reload_doc()
				//frappe.route_options = {"name": cur_frm.doc.sales_invoice, "customer":cur_frm.doc.student_name}
				frappe.route_options = {"project": cur_frm.doc.name, "customer": cur_frm.doc.customer_reference}
				frappe.set_route("List", "Sales Order");

			});

			//frm.add_custom_button(__("Projecto"), function() {
			//	cur_frm.reload_doc()
			//	frappe.route_options = {"project_name": cur_frm.doc.name,"customer": cur_frm.doc.customer_reference}
			//	frappe.set_route("List", "Project");
			//}, "Criar", true);

			//frm.add_custom_button(__("Ordens de Venda"), function() {
			//	cur_frm.reload_doc()
			//	frappe.route_options = {"project": cur_frm.doc.name, "customer": cur_frm.doc.customer_reference}
			//	frappe.set_route("List", "Sales Order");
			//}, "Criar", true);


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
			var totalfundos = 0;
			for (var d in cur_frm.doc.servicos_processo){
				totalfundos += (flt(cur_frm.doc.servicos_processo[d].preco_ficha_processo) * cur_frm.doc.servicos_processo[d].qtd_ficha_processo);
			}
			cur_frm.doc.broker_funds = totalfundos
			cur_frm.refresh_fields('broker_funds');
		}


		if (frm.doc.docstatus ==1){ //(cur_frm.has_perm("submit")) {
			// close
			console.log('Fecha ou Nao')
			if (prj1.responseJSON != undefined){			
				x = 0
				for (x in prj1.responseJSON.message){
					if (prj1.responseJSON.message[x] == cur_frm.doc.name){
						frm.add_custom_button(("Fechar"), function() {

							frappe.call({
								'async': false,
								'method': 'angola_erp.transitario.doctype.ficha_de_processo.ficha_de_processo.set_ficha_closed',
								'args':{
									'ficha': cur_frm.doc.name,
								}
							});

							cur_frm.reload_doc()
						});

					}
				}
			}
			if (prj.responseJSON != undefined){
				if (prj.responseJSON.message[0][1] == "Completed" && prj.responseJSON.message[0][0] == cur_frm.doc.name) {
					console.log('projeto corrente fechado!!!!')
			//		cur_frm.add_custom_button(__('Fechar'), this.close_ficha_processo, __("Status"))

				}
			}
		}

	}

});


var close_ficha_processo = function(){
	cur_frm.doc.status_process = "Fechado";	
	//cur_frm.cscript.update_status_process("Close", "Fechado");
}

frappe.ui.form.on("Ficha de Processo","process_number",function(frm,cdt,cdn){
	if (cur_frm.doc.taxa_cambio_bna == 0 || cur_frm.doc.taxa_cambio_bna == undefined ) {
		if (taxacambioLocal.responseJSON == undefined){
			if (taxacambio.responseJSON == undefined){
				cur_frm.doc.taxa_cambio_bna = 0
			}else{
				if ( taxacambio.responseJSON.message == undefined){
			
					cur_frm.doc.taxa_cambio_bna =0
				}else{
					cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[1]
				}
			}

		}else{
			if ( taxacambioLocal.responseJSON.message == undefined){
			
				if (taxacambio.responseJSON == undefined){
					cur_frm.doc.taxa_cambio_bna = 0
				}else{
					if ( taxacambio.responseJSON.message == undefined){
			
						cur_frm.doc.taxa_cambio_bna =0
					}else{
						cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[1]
					}
				}

			}else{
				cur_frm.doc.taxa_cambio_bna = taxacambioLocal.responseJSON.message[0]["exchange_rate"]
			}
		}


/*
		if (taxacambio.responseJSON == undefined){
			cur_frm.doc.taxa_cambio_bna = 0
		}else{
			if ( taxacambio.responseJSON.message == undefined){
			
				cur_frm.doc.taxa_cambio_bna =0
			}else{
				cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[1]
			}
		}
*/
		cur_frm.refresh_fields('taxa_cambio_bna');
	}

	if (cur_frm.doc.process_number.length < 4){
		if (cur_frm.doc.process_number.length == 1){
			frappe.model.set_value(cdt,cdn,'process_number','000' + cur_frm.doc.process_number)
		}else if (cur_frm.doc.process_number.length == 2){
			frappe.model.set_value(cdt,cdn,'process_number','00' + cur_frm.doc.process_number)
		}else if (cur_frm.doc.process_number.length == 3){
			frappe.model.set_value(cdt,cdn,'process_number','0' + cur_frm.doc.process_number)
		}
	}
	if (isNaN(cur_frm.doc.process_number)){
		frappe.model.set_value(cdt,cdn,'process_number',01)
		frappe.show_alert('Numero de Processo tem que ter somente digitos')
	}


});

frappe.ui.form.on("Ficha de Processo","funds_request_currency",function(frm,cdt,cdn){
	if (cur_frm.doc.docstatus ==0){

		if (cur_frm.doc.funds_request_currency =="USD"){
			//if (cur_frm.doc.taxa_cambio_bna == 0 || cur_frm.doc.taxa_cambio_bna == "Undefined" ) {
			cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[1]
			cur_frm.refresh_fields('taxa_cambio_bna');
			//}

		}else if (cur_frm.doc.funds_request_currency =="AKZ" || cur_frm.doc.funds_request_currency =="AOA"){
			//if (cur_frm.doc.taxa_cambio_bna == 0 || cur_frm.doc.taxa_cambio_bna == "Undefined" ) {
			cur_frm.doc.taxa_cambio_bna = taxacambio.responseJSON.message[0]
			cur_frm.refresh_fields('taxa_cambio_bna');
			//}


		}else{
			//Tem que ir buscar o cambio based on the currency selected
			cur_frm.doc.taxa_cambio_bna = 0
			cur_frm.refresh_fields('taxa_cambio_bna');

			frappe.call({
				method: "angola_erp.util.cambios.cambios_local",
				args: {
					"moeda": cur_frm.doc.funds_request_currency
				},
				callback: function(r){
					if(r.message){
						console.log(r.message[0]['exchange_rate'])
						cur_frm.doc.taxa_cambio_bna = r.message[0]['exchange_rate']
						cur_frm.refresh_fields('taxa_cambio_bna');
					}
				}
			});


/*
			taxacambioLocal1 = cur_frm.call({method:"angola_erp.util.cambios.cambios_local",args:{"moeda":cur_frm.doc.funds_request_currency}})

			if (taxacambioLocal1.responseJSON == undefined){
				cur_frm.doc.taxa_cambio_bna = 0

			}else{
				if ( taxacambioLocal1.responseJSON.message == undefined){
			
					cur_frm.doc.taxa_cambio_bna = 0

				}else{
					cur_frm.doc.taxa_cambio_bna = taxacambioLocal1.responseJSON.message[0]["exchange_rate"]
				}
			}

*/
			console.log('Taxa cambio...aguarde')
			frappe.show_alert("Taxa cambio...aguarde",1) 	
		}
	}
});


frappe.ui.form.on("Ficha de Processo","valor_fob",function(frm,cdt,cdn){
	//Calcula valor_cif mercadoria
	console.log('valor fob')
	cur_frm.doc.valor_cif_mercadoria = cur_frm.doc.valor_fob
	if (cur_frm.doc.frete){
		cur_frm.doc.valor_cif_mercadoria += cur_frm.doc.frete
	}

	if (cur_frm.doc.valor_seguro){
		cur_frm.doc.valor_cif_mercadoria += cur_frm.doc.valor_seguro
	}
	cur_frm.refresh_fields('valor_cif_mercadoria');


});


frappe.ui.form.on("Ficha de Processo","valor_seguro",function(frm,cdt,cdn){
	//Calcula valor_cif mercadoria
	console.log('valor fob')
	cur_frm.doc.valor_cif_mercadoria = cur_frm.doc.valor_fob
	if (cur_frm.doc.frete){
		cur_frm.doc.valor_cif_mercadoria += cur_frm.doc.frete
	}

	if (cur_frm.doc.valor_seguro){
		cur_frm.doc.valor_cif_mercadoria += cur_frm.doc.valor_seguro
	}

	cur_frm.refresh_fields('valor_cif_mercadoria');


});

frappe.ui.form.on("Ficha de Processo","frete",function(frm,cdt,cdn){
	//Calcula valor_cif mercadoria
	console.log('valor fob')
	cur_frm.doc.valor_cif_mercadoria = cur_frm.doc.valor_fob
	if (cur_frm.doc.frete){
		cur_frm.doc.valor_cif_mercadoria += cur_frm.doc.frete
	}

	if (cur_frm.doc.valor_seguro){
		cur_frm.doc.valor_cif_mercadoria += cur_frm.doc.valor_seguro
	}

	cur_frm.refresh_fields('valor_cif_mercadoria');


});

frappe.ui.form.on("Ficha de Processo","valor_cif_mercadoria",function(frm,cdt,cdn){
	//Calcula valor_aduaneiro
	if (cur_frm.doc.taxa_cambio_alfandega){
		cur_frm.doc.valor_aduaneiro = cur_frm.doc.valor_cif_mercadoria * cur_frm.doc.taxa_cambio_alfandega
	}else{
		cur_frm.doc.valor_aduaneiro = cur_frm.doc.valor_cif_mercadoria * cur_frm.doc.taxa_cambio_bna
	}	
	cur_frm.refresh_fields('valor_aduaneiro');


});

frappe.ui.form.on("Ficha de Processo","commodity",function(frm,cdt,cdn){
	//Calcula valor_aduaneiro
	if (cur_frm.doc.valor_cif_mercadoria && (cur_frm.doc.valor_aduaneiro == 0 || cur_frm.doc.valor_aduaneiro == undefined )){
		if (cur_frm.doc.taxa_cambio_alfandega){
			cur_frm.doc.valor_aduaneiro = cur_frm.doc.valor_cif_mercadoria * cur_frm.doc.taxa_cambio_alfandega
		}else{
			cur_frm.doc.valor_aduaneiro = cur_frm.doc.valor_cif_mercadoria * cur_frm.doc.taxa_cambio_bna
		}	

		cur_frm.refresh_fields('valor_aduaneiro');
	}
});


frappe.ui.form.on("Ficha de Processo","taxa_cambio_company",function(frm,cdt,cdn){
	if (!isNumber(cur_frm.doc.broker_request_customs)){
		frappe.show_alert("Somente numeros")
	}
});

frappe.ui.form.on("Ficha de Processo","invoice_currency_roe",function(frm,cdt,cdn){
	if (!isNumber(cur_frm.doc.broker_request_customs)){
		frappe.show_alert("Somente numeros")
	}
});

frappe.ui.form.on("Ficha de Processo","credit_customer_value",function(frm,cdt,cdn){
	if (!isNumber(cur_frm.doc.broker_request_customs)){
		frappe.show_alert("Somente numeros")
	}
});

frappe.ui.form.on("Ficha de Processo","broker_funds",function(frm,cdt,cdn){
	if (!isNumber(cur_frm.doc.broker_request_customs)){
		frappe.show_alert("Somente numeros")
	}
});

frappe.ui.form.on("Ficha de Processo","broker_request_customs",function(frm,cdt,cdn){
	if (!isNumber(cur_frm.doc.broker_request_customs)){
		frappe.show_alert("Somente numeros")
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
		console.log('table')
		calculate_totals(frm, cdt, cdn);
	}


});

frappe.ui.form.on("Servicos_Ficha_Processo","preco_ficha_processo",function(frm,cdt,cdn){
		console.log('preco')
		var d =locals[cdt][cdn];
		calculate_totals(frm, cdt, cdn);
});

frappe.ui.form.on('Ficha de Processo','status_process',function(frm,cdt,cdn){
	//When changed to EM CURSO ... copies the info to Project and create the tasks.
	if (cur_frm.doc.status_process == 'Em Curso'){
		if (frm.docname.substring(0,3)=="New" || frm.docname.substring(0,3)=="Nov"){
			frappe.show_alert("Nao se esqueca de salvar primeiro o registo antes de mudar o Status para Em Curso\nDepois de Salvo podera mudar o status e criar o Projecto com as tarefas")
			cur_frm.doc.status_process = "Aberto"
			cur_frm.reload_doc()	
		}else{
			frappe.show_alert("Os servicos do Cliente serao criados e incluidos como Projecto!!!",2)
		}
	}else if (cur_frm.doc.status_process == 'Fechado'){
		//Verifica se o Projecto ja esta completed.
		if (prj.responseJSON.message == "Completed"){
			//Pode fechar a Obra ... transfer the list of Material added to Material_obra
			frappe.show_alert("Ficha de Processo pode ser fechado !!!",3)
		}else{
			//Ooooopppssss still oopen
			frappe.show_alert("O Projecto " + cur_frm.doc.process_number + " ainda nao esta fechado ou concluido.\nPor favor rever as tarefas alocadas.")
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

function isNumber(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}

var calculate_totals = function(frm, cdt,cdn) {
	var tbl1 = frm.doc.servicos_processo || [];
	var total_valor = 0; 
	for(var i = 0; i < tbl1.length; i++){
		total_valor += (flt(tbl1[i].preco_ficha_processo) * tbl1[i].qtd_ficha_processo);
	}
	frappe.model.set_value(cdt,cdn,'broker_funds',total_valor)
	frm.doc.broker_funds = total_valor
	refresh_many(['broker_funds']);
}
