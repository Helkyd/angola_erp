// Copyright (c) 2019, Helio de Jesus and contributors
// For license information, please see license.txt

var ordem
var prj
ordens= cur_frm.call({method:"get_avarias_clientes",args:{"Parent":""}})
ordens1 = undefined

frappe.ui.form.on('Folha de Obras', {
	onload: function(frm) {
		if (cur_frm.doc.numero_obra != undefined){
			prj= cur_frm.call({method:"get_projecto_status",args:{"prj":cur_frm.doc.numero_obra}})
		}

		if (cur_frm.doc.ordem_reparacao != undefined){
			ordens1= cur_frm.call({method:"get_avaria_cliente",args:{"cdt":cur_frm.doc.ordem_reparacao}})
		}
	}
		
});

frappe.ui.form.on('Folha de Obras', {
	refresh: function(frm) {


		cur_frm.toggle_enable("data_abertura",false)
		cur_frm.toggle_enable("fo_operador",false)
		cur_frm.toggle_enable("data_entrada_or",false)
		cur_frm.toggle_enable("data_previsao_saida",false)
		cur_frm.toggle_enable("obs_cliente",false)

		cur_frm.fields_dict['ordem_reparacao'].get_query = function(doc){
			return{
				filters:{
					"or_status":"Aberta",
				},
				
			}
		}	

		if (cur_frm.doc.fo_status == 'Em Curso'){
			cur_frm.toggle_enable("ordem_reparacao",false)
			frm.set_df_property("fo_status","options","Em Curso\nFechada")
		}else if (cur_frm.doc.fo_status == 'Aberta'){
			if (cur_frm.docname.substring(0,3)=="New" || cur_frm.docname.substring(0,3)=="Nov"){
				cur_frm.toggle_enable("ordem_reparacao",true)
			}else{
			cur_frm.toggle_enable("ordem_reparacao",false)
			}

		}else if (cur_frm.doc.fo_status == 'Fechada'){
			cur_frm.toggle_enable("ordem_reparacao",false)
			cur_frm.toggle_enable("kms_entrada",false)
			cur_frm.toggle_enable("kms_saida",false)
			cur_frm.toggle_enable("avarias_cliente",false)
			cur_frm.toggle_enable("fo_status",false)
			cur_frm.toggle_enable("revisao_feita",false)
			cur_frm.toggle_enable("proxima_revisao",false)

		}

		if (cur_frm.doc.fo_status == 'Em Curso' && !cur_frm.doc.__islocal || cur_frm.doc.fo_status == 'Fechada' ){

			frm.add_custom_button(__("Projecto"), function() {
				cur_frm.reload_doc()
				frappe.route_options = {"project_name": cur_frm.doc.name}
				frappe.set_route("List", "Project");
			}, "Criar", true);

			frm.add_custom_button(__("Proformas"), function() {
				cur_frm.reload_doc()
				frappe.route_options = {"project": cur_frm.doc.name, "customer": cur_frm.doc.nome_cliente}
				frappe.set_route("List", "Sales Order");
			}, "Criar", true);


		}

		//Assuming already saved now will criate the Projet so Sales Order can also be created.

		if (frm.doc.docstatus ==0 && cur_frm.doc.fo_status == 'Aberta' && frm.docname.substring(0,3) !="New" && frm.docname.substring(0,3) !="Nov") {

			cur_frm.doc.fo_status = "Em Curso"	
			cur_frm.save() 
		}

		//teste para pegar as avarias
		console.log('teste pegar avarias')
		if (ordens1 != undefined){
			if (ordens1.responseJSON){
				if (frm.doc.avarias_cliente == undefined){
					for (var x = 0; x < ordens1.responseJSON.message.length;x++){
						if (ordens1.responseJSON.message[x].Parent == cur_frm.doc.ordem_reparacao){
							var av = frm.add_child("avarias_cliente")
							av.avcliente_descricao = ordens1.responseJSON.message[x].avcliente_descricao

						}
					}
					frm.refresh_field("avarias_cliente")
				}
			}
		}else if (ordens != undefined){
			if (ordens.responseJSON){
				if (frm.doc.avarias_cliente == undefined){
					for (var x = 0; x < ordens.responseJSON.message.length;x++){
						if (ordens.responseJSON.message[x].Parent == cur_frm.doc.ordem_reparacao){
							var av = frm.add_child("avarias_cliente")
							av.avcliente_descricao = ordens.responseJSON.message[x].avcliente_descricao

						}
					}
					frm.refresh_field("avarias_cliente")
					//cur_frm.doc.avarias_cliente = cur_frm.doc.avarias_cliente + '\n'
				}

			}
		}
	}
});

frappe.ui.form.on('Folha de Obras','ordem_reparacao',function(frm,cdt,cdn){

	frappe.model.set_value(cdt,cdn,'fo_operador',frappe.session.user)

	if (cur_frm.doc.ordem_reparacao){
		reparar_('Ordem de Reparacao',cur_frm.doc.ordem_reparacao)

		//Enters Avarias reported by client to serve as Tasks

		if (ordens1 != undefined){
			for (var x = 0; x < ordens1.responseJSON.message.length;x++){
				if (ordens1.responseJSON.message[x].Parent == cur_frm.doc.ordem_reparacao){
					var av = frm.add_child("avarias_cliente")
					av.avcliente_descricao = ordens1.responseJSON.message[x].avcliente_descricao

				}
			}
			frm.refresh_field("avarias_cliente")

		}else if (ordens != undefined){
			for (var x = 0; x < ordens.responseJSON.message.length;x++){
				if (ordens.responseJSON.message[x].Parent == cur_frm.doc.ordem_reparacao){
					var av = frm.add_child("avarias_cliente")
					av.avcliente_descricao = ordens.responseJSON.message[x].avcliente_descricao

				}
			}
			frm.refresh_field("avarias_cliente")
			//cur_frm.doc.avarias_cliente = cur_frm.doc.avarias_cliente + '\n'

		}

		cur_frm.refresh_fields('avarias_cliente');
		cur_frm.refresh_fields('nome_cliente');
	}


});


frappe.ui.form.on('Folha de Obras','fo_status',function(frm,cdt,cdn){
	//When changed to EM CURSO ... copies the info to Project and create the tasks.
	if (cur_frm.doc.fo_status == 'Em Curso'){
		if (frm.docname.substring(0,3)=="New" || frm.docname.substring(0,3)=="Nov"){
			alert("Nao se esqueca de salvar primeiro o registo antes de mudar o Status para Em Curso\nDepois de Salvo podera mudar o status e criar o Projecto com as tarefas")
			cur_frm.doc.fo_status = "Aberta"
			cur_frm.reload_doc()	
		}else{
			show_alert("As Avarias do Cliente serao criadas e incluidas como um Projecto!!!\nDevera a folha depois ser enviar ou assignada ao Chefe de Oficina ou Area da Oficina para dar seguimento",2)
		}
	}else if (cur_frm.doc.fo_status == 'Fechada'){
		//Verifica se o Projecto ja esta completed.
		if (prj.responseJSON.message == "Completed"){
			//Pode fechar a Obra ... transfer the list of Material added to Material_obra
			show_alert("Folha de Obra pode ser fechada !!!",3)
		}else{
			//Ooooopppssss still oopen
			alert("O Projecto " + cur_frm.doc.numero_obra + " ainda nao esta fechado ou concluido.\nPor favor rever se as tarefas alocadas estao completadas.")
			cur_frm.doc.fo_status = "Em Curso"
			cur_frm.reload_doc()	

		}
	}



});

frappe.ui.form.on("Avarias_Cliente","avarias_cliente",function(frm,cdt,cdn){



		cur_frm.refresh_fields('avarias_cliente');


});






var reparar_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var ordem = frappe.model.get_doc(frm,cdt)
		if (ordem){

			cur_frm.doc.nome_cliente = ordem.or_nome_cliente
			cur_frm.doc.cliente_telefone = ordem.or_client_number
			cur_frm.doc.email_cliente = ordem.or_email_cliente

			cur_frm.doc.marca_veiculo = ordem.or_marca_veiculo
			cur_frm.doc.matricula_veiculo = ordem.or_matricula
			cur_frm.doc.numero_chassi = ordem.or_numero_chassi

			cur_frm.doc.kms_entrada = ordem.or_kms_entrada
			cur_frm.doc.data_entrada_or = ordem.or_date
			cur_frm.doc.data_previsao_saida = ordem.or_previsao_entrega

			cur_frm.doc.obs_cliente = ordem.or_obs_cliente


		}
		
		cur_frm.refresh_fields();

	});


}


var pedidocliente_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm,cdt,function(){

//		var ordem = frappe.get_all(frm,filters={'Parent':cdt},fields=['Parent','avcliente_descricao'])
//		var ordem  = cur_frm.call({method:"get_avaria_cliente",args:{"frm":frm}})

		frappe.call({
			method: "gestoficinas.gestoficinas.doctype.api.get_avaria_cliente",
			args: {
				"cdt":cdt				
			},
			callback: function(r) {
//				var caix = frappe.model.sync(r.message);
//				msgprint(r.message)
				if (r.message !=undefined){
//					alert("Aberto ou em Curso")
					ordem = r.message
//					return
				}else{
					alert("CAIXA Fechado")
					
				}

			}
		});
	
//		if (ordem !=undefined){

//			for (var x = 0; x < ordem.length;x++){
//				cur_frm.doc.avarias_cliente = ordem[x].avcliente_descricao + ';' + cur_frm.doc.avarias_cliente
//			}


//		}
		
		cur_frm.refresh_fields();

	});

}
