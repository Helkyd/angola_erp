// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt



var caixa_upd=0
var caix = 0

frappe.ui.form.on('Caixa de Registo', {
	onload: function(frm) {

		//Verifica se o Caixa esta aberto ... segudo controle caso cx_aberto nao retorne valores ....
		mesas_open = undefined

		frappe.call({
			method: "angola_erp.util.angola.check_caixa_aberto",
			args: {},
			callback: function(r) {
				if (r.message !=undefined){
					caix = r.message
				}else{
//					alert("CAIXA Fechado")
				}

			}
		});


		//Verifica tables OPEN ....
		frappe.call({
			method:"frappe.client.get_list",
			args:{
				doctype:"Atendimento Bar",
				filters: {
						"status_atendimento":"Ocupado"
				},
				fields: ["status_atendimento"]
			},
			callback: function(r) {
				if (r.message) {
					$.each(r.message, function(i,d) {
						console.log(i.toString() + ": " + d.status_atendimento);
						mesas_open = d.status_atendimento;
					});
				}
			}
		});

		if (cur_frm.doc.docstatus ==1 && cur_frm.doc.status_caixa=="Aberto" ){

			if (caix[0] !=[] ){
				alert("Caixa Registadora ja esta aberta!!!")
				cur_frm.toggle_enable("movimentos_caixa",false)	
				cur_frm.toggle_enable("amount_init",false)
				cur_frm.toggle_enable("data_hora",false)
				cur_frm.toggle_enable("data_hora_fecho",false)
				cur_frm.toggle_enable("status_caixa",false)
				cur_frm.toggle_enable("amount_caixa",false)
				cur_frm.toggle_enable("amount_tpa",false)
				cur_frm.toggle_enable("amount_conta_corrente",false)
				cur_frm.toggle_enable("company",false)
				cur_frm.page.clear_primary_action()
			}else{
			// acrescenta os registos
				show_alert("Abertura do Caixa...",2)
				cur_frm.toggle_enable("movimentos_caixa",false)	
				cur_frm.toggle_enable("amount_init",true)
				cur_frm.toggle_enable("data_hora",false)
				cur_frm.toggle_enable("data_hora_fecho",false)
				cur_frm.toggle_enable("amount_caixa",false)
				cur_frm.toggle_enable("amount_tpa",false)
				cur_frm.toggle_enable("amount_conta_corrente",false)
				cur_frm.toggle_enable("company",false)
				//movimentos_add(frm)
			}
		}else if (cur_frm.doc.docstatus ==0 && frm.doc.__unsaved==1){

//			alert("Caixa aberto!!! Por favor fechar antes.")
		}else if (cur_frm.doc.status_caixa=="Em Curso"){
			cur_frm.toggle_enable("data_hora",false)
			cur_frm.toggle_enable("data_hora_fecho",false)
			cur_frm.toggle_enable("amount_init",false)
			cur_frm.toggle_enable("amount_caixa",false)
			cur_frm.toggle_enable("amount_tpa",false)
			cur_frm.toggle_enable("amount_conta_corrente",false)
			cur_frm.toggle_enable("company",false)
			cur_frm.set_df_property("movimentos_caixa","hidden",false)	
			if (caixa_upd==0){
				movimentos_add(frm)
				caixa_upd=1
				cur_frm.reload_doc()
			}

		}else if (cur_frm.doc.status_caixa=="Fechado"){
			cur_frm.toggle_enable("data_hora",false)
			cur_frm.toggle_enable("data_hora_fecho",false)
			cur_frm.toggle_enable("amount_init",false)
			cur_frm.toggle_enable("amount_caixa",false)
			cur_frm.toggle_enable("amount_tpa",false)
			cur_frm.toggle_enable("amount_conta_corrente",false)
			cur_frm.toggle_enable("company",false)
			cur_frm.toggle_enable("status_caixa",false)
			cur_frm.toggle_enable("movimentos_caixa",false)	
			cur_frm.disable_save()

		}else if (cur_frm.doc.docstatus ==1)  {
			//ADD New RECORD
			alert("bbbbb " + cur_frm.docname)
			cur_frm.toggle_enable("amount_init",true)
			cur_frm.enable_save()
//			movimentos_add(frm)
//			cur_frm.reload_doc()

		}else if (cur_frm.doc.docstatus ==1) {

			//Ja tem caixa Aberto
			cur_frm.toggle_enable("data_hora",false)
			cur_frm.toggle_enable("data_hora_fecho",false)
			cur_frm.toggle_enable("amount_init",false)
			cur_frm.toggle_enable("amount_caixa",false)
			cur_frm.toggle_enable("amount_tpa",false)
			cur_frm.toggle_enable("amount_conta_corrente",false)
			cur_frm.toggle_enable("company",false)

			cur_frm.disable_save()

		}else if (cur_frm.doc.status_caixa=="Aberto"){
			cur_frm.toggle_enable("data_hora",false)
			cur_frm.toggle_enable("data_hora_fecho",false)
			cur_frm.toggle_enable("amount_init",false)
			cur_frm.toggle_enable("amount_caixa",false)
			cur_frm.toggle_enable("amount_tpa",false)
			cur_frm.toggle_enable("amount_conta_corrente",false)
			cur_frm.toggle_enable("company",false)
		}


	}
});

frappe.ui.form.on('Caixa de Registo', {
	refresh: function(frm) {

		cur_frm.page.set_secondary_action(__("ACTUALIZAR CAIXA"), function() {
			//Actualiza o CAIXA
			movimentos_add(frm)
			cur_frm.reload_doc()
		}, "");



		if (cur_frm.doc.docstatus ==1 && caix[0] !=[] ) { //cx_aberto.statusText=="OK"){

			if (caix[0] !=[]){
				alert("O CAIXA ja esta aberto")	
				cur_frm.toggle_enable("amount_init",true)
				cur_frm.toggle_enable("data_hora",false)
				cur_frm.toggle_enable("data_hora_fecho",false)
				cur_frm.toggle_enable("amount_caixa",false)
				cur_frm.toggle_enable("amount_tpa",false)
				cur_frm.toggle_enable("amount_conta_corrente",false)
				cur_frm.toggle_enable("company",false)
				cur_frm.toggle_enable("status_caixa",false)
				cur_frm.set_df_property("movimentos_caixa","hidden",false)
				cur_frm.disable_save()
		
			}else{
			// acrescenta os registos
				//alert("aqui!!!")
				cur_frm.toggle_enable("movimentos_caixa",false)	
				cur_frm.toggle_enable("amount_init",true)
				cur_frm.toggle_enable("data_hora",false)
				cur_frm.toggle_enable("data_hora_fecho",false)
				cur_frm.toggle_enable("amount_caixa",false)
				cur_frm.toggle_enable("amount_tpa",false)
				cur_frm.toggle_enable("amount_conta_corrente",false)
				cur_frm.toggle_enable("company",false)
			}


		}else if (cur_frm.doc.status_caixa=="Fechado"){
			cur_frm.toggle_enable("data_hora",false)
			cur_frm.toggle_enable("data_hora_fecho",false)
			cur_frm.toggle_enable("amount_init",false)
			cur_frm.toggle_enable("amount_caixa",false)
			cur_frm.toggle_enable("amount_tpa",false)
			cur_frm.toggle_enable("amount_conta_corrente",false)
			cur_frm.toggle_enable("company",false)
			cur_frm.toggle_enable("status_caixa",false)
			cur_frm.set_df_property("movimentos_caixa","hidden",false)
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "descricao_movimento"})[0].read_only = true;	
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "tipo_pagamento"})[0].read_only = true;	
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "valor_pago"})[0].read_only = true;
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "hora_atendimento"})[0].read_only = true;


		}else if (cur_frm.doc.docstatus ==1 && frm.doc.status_caixa=="Aberto" && caix[0] !=[]){
			alert("O CAIXA ja foi aberto!!!")	
			cur_frm.toggle_enable("data_hora",false)
			cur_frm.toggle_enable("data_hora_fecho",false)
			cur_frm.toggle_enable("amount_init",false)
			cur_frm.toggle_enable("amount_caixa",false)
			cur_frm.toggle_enable("amount_tpa",false)
			cur_frm.toggle_enable("amount_conta_corrente",false)
			cur_frm.toggle_enable("company",false)
			cur_frm.set_df_property("movimentos_caixa","hidden",false)
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "descricao_movimento"})[0].read_only = true;	
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "tipo_pagamento"})[0].read_only = true;	
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "valor_pago"})[0].read_only = true;
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "hora_atendimento"})[0].read_only = true;
			cur_frm.disable_save()

		}else if (cur_frm.doc.docstatus ==0 && frm.doc.status_caixa=="Aberto" && caix[0] !=undefined){
			if (cur_frm.docname.substring(0,3)=="New" || cur_frm.docname.substring(0,3)=="Nov"){
				alert("O CAIXA ja foi aberto!!!")	
				cur_frm.disable_save()
			}
			cur_frm.toggle_enable("data_hora",false)
			cur_frm.toggle_enable("data_hora_fecho",false)
			cur_frm.toggle_enable("amount_init",false)
			cur_frm.toggle_enable("amount_caixa",false)
			cur_frm.toggle_enable("amount_tpa",false)
			cur_frm.toggle_enable("amount_conta_corrente",false)
			cur_frm.toggle_enable("company",false)
			cur_frm.set_df_property("movimentos_caixa","hidden",false)
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "descricao_movimento"})[0].read_only = true;	
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "tipo_pagamento"})[0].read_only = true;	
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "valor_pago"})[0].read_only = true;
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "hora_atendimento"})[0].read_only = true;

		}else if (cur_frm.doc.docstatus ==0 && frm.doc.status_caixa=="Aberto" && caix[0] ==undefined){
//			alert("aqui")
//			if (cx_aberto.responseText != []){
//				cur_frm.toggle_enable("amount_init",false)
//			}else{
			cur_frm.toggle_enable("amount_init",true)
//			}
			cur_frm.toggle_enable("movimentos_caixa",false)	
			cur_frm.toggle_enable("amount_tpa",false)
			cur_frm.toggle_enable("amount_conta_corrente",false)
			cur_frm.toggle_enable("company",false)
			cur_frm.toggle_enable("data_hora",false)
			cur_frm.toggle_enable("data_hora_fecho",false)
			cur_frm.toggle_enable("amount_caixa",false)
		}

		if (cur_frm.doc.status_caixa=="Em Curso"){
			show_alert("Caro " + frappe.session.user + "\n Antes fazer o Fecho de CAIXA, melhor ATUALIZAR O CAIXA/SALDO",4)	
			frm.set_df_property("status_caixa","options","Em Curso\nFechado")
		}else if (cur_frm.doc.status_caixa=="Aberto"){
			frm.set_df_property("status_caixa","options","Aberto\nEm Curso")

		}
	


	}
});



frappe.ui.form.on("Caixa de Registo","status_caixa",function(frm,cdt,cdn){

	var me = this;
	if (cur_frm.doc.status_caixa=="Fechado"){

		if (frappe.session.user != cur_frm.doc.usuario_caixa){
			//Verify if GESTAO_PENSAO group than Admin is allowed otherwise 
			if (tem_acesso.responseJSON.message == "GesPensao"){	
				//Tem Acesso
				show_alert("ESTE USUARIO PODE FAZER O FECHO DE CAIXA " + frappe.session.user,2)	
				frappe.model.set_value(cdt,cdn,'usuario_caixa_fecho',frappe.session.user)				
				frappe.model.set_value(cdt,cdn,'data_hora_fecho',frappe.datetime.nowdate())
			}else{
				alert("FECHO DE CAIXA SO PODE SER FEITO PELO USUARIO " + cur_frm.doc.usuario_caixa)
				frappe.model.set_value(cdt,cdn,'status_caixa','Em Curso')
				cur_frm.reload_doc()
			}
			

		}else{	
		    	show_alert("Verificando Mesas Abertas...",2)
			cur_frm.set_df_property("movimentos_caixa","hidden",false)			
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "descricao_movimento"})[0].read_only = false;	
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "tipo_pagamento"})[0].read_only = false;	
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "valor_pago"})[0].read_only = false;
			frappe.utils.filter_dict(frm.fields_dict["movimentos_caixa"].grid.docfields, {"fieldname": "hora_atendimento"})[0].read_only = false;

			if (mesas_open =="Ocupado" ){

				alert("NAO PODE FECHAR O CAIXA. Ainda tem Mesas Abertas")
				cur_frm.disable_save()
				cur_frm.reload_doc()

			}else if (mesas_open ==undefined){
				// Mesas Fechadas ...
			    	show_alert("Fechando o Caixa...",2)
				frappe.model.set_value(cdt,cdn,'data_hora_fecho',frappe.datetime.nowdate())
				this.cur_page.page.frm._save()

			}else if (cur_frm.doc.amount_caixa==0){
				//Nao pode fechar o Caixa ... nao tem NADA !!!!
		
			}		

		
		}
	}
});


var movimentos_add = function(frm) {
	var me = this; 
	var fecho = 0;

	if (cur_frm.doc.status_caixa=="Fechado"){
		fecho = 2	
	}

	show_alert("Processando Movimento do dia!!! Por favor aguarde...",3)

	frappe.call({
		method: "angola_erp.util.angola.caixa_movimentos_in",
		args: {
			"start":frm.doc.data_hora,
			"caixa":frm.doc.name,
			"fecho":fecho,
				
		},
		callback: function(r) {
			if (r.message !=undefined){
				show_alert("Calculos do Fecho concluidos",2)
				
				cur_frm.reload_doc()

			}else{
				//alert("Os Calculos do Fecho de Caixa nao foram feitos!")
				return
			}

		}
	});

}
