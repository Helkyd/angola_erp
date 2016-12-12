// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


cx_open =cur_frm.call({method:"check_caixa_aberto",args:{"start":"none"}})



frappe.ui.form.on('Atendimento Bar', {
	onload: function(frm) {

		//Verifica se o Caixa esta aberto ... segudo controle caso cx_aberto nao retorne valores ....
		caixaopen = undefined

		frappe.call({
			method:"frappe.client.get_list",
			args:{
				doctype:"Caixa de Registo",
				filters: {
						"status_caixa":['in', 'Aberto, Em Curso']
				},
				fields: ["status_caixa"]
			},
			callback: function(r) {
				if (r.message) {
					$.each(r.message, function(i,d) {
						console.log(i.toString() + ": " + d.status_caixa);
						caixaopen = d.status_caixa;
					});
				}
			}
		});

		frm.fields_dict.produtos.grid.get_field('produtos').get_query = function(doc) {
			return {
				filters: {			
		 			"disabled":0
				}
			}	
		}

		frm.fields_dict.nome_mesa.get_query = function(doc){
			return{
				filters:{
					"status_mesa":"Livre",

				},
				
			}
		}


		show_alert("Verificando CAIXA ABERTO...",3)
		cur_frm.enable_save()
//		if (cx_open.statusText=="OK" ){

		if ((cur_frm.docname.substring(0,3)=="New" || cur_frm.docname.substring(0,3)=="Nov") && cx_open.responseText != "{}"){
			//CAIXA aberto ...



			if (cx_open.responseText == undefined){

				show_alert("É necessário fazer a Abertura do CAIXA...",3)
			}else if (frm.doc.status_atendimento=="Ocupado" && frm.doc.bar_tender ==undefined && cx_open.responseText != undefined){

				//Novo Registo 
				show_alert("Novo Registo de Caixa...",3)
				cur_frm.toggle_enable("bar_tender",false)
				cur_frm.toggle_enable("pagamento_por",false)
				cur_frm.toggle_enable("status_atendimento",false)
				cur_frm.toggle_enable("total_servicos",false)
				cur_frm.toggle_enable("valor_pago",false)

			}else if (frm.doc.status_atendimento=="Ocupado" && frm.doc.total_servicos !=0){
				cur_frm.toggle_enable("nome_mesa",false)
				cur_frm.toggle_enable("cartao_numero",false)
				cur_frm.toggle_enable("pagamento_por",false)
				cur_frm.toggle_enable("nome_cliente",false)
				cur_frm.toggle_enable("status_atendimento",false)
				cur_frm.toggle_enable("total_servicos",false)
				cur_frm.toggle_enable("valor_pago",false)

		//			cur_frm.toggle_enable("hora_entrada",false)
		//			cur_frm.toggle_enable("hora_saida",false)
		//			cur_frm.toggle_enable("pagamento_por",false)	
		//			cur_frm.toggle_enable("status_reserva",false)	
		//			cur_frm.set_df_property("reserva_numero","hidden",true)
		//			cur_frm.set_df_property("servico_pago_por","hidden",true)
			}else if (frm.doc.status_atendimento=="Fechado"){
				cur_frm.toggle_enable("nome_mesa",false)
				cur_frm.toggle_enable("cartao_numero",false)
				cur_frm.toggle_enable("nome_cliente",false)
				cur_frm.toggle_enable("pagamento_por",false)
				cur_frm.toggle_enable("status_atendimento",false)
				cur_frm.toggle_enable("produtos",false)
				cur_frm.toggle_enable("pagamento_botao",false)
				cur_frm.toggle_enable("total_servicos",false)
				cur_frm.toggle_enable("valor_pago",false)

				if (frm.doc.conta_corrente_status =="Pago"){
					cur_frm.toggle_enable("conta_corrente_status",false)
				}else{
					cur_frm.toggle_enable("conta_corrente_status",true)
				}
	
		//			cur_frm.toggle_enable("status_reserva",false)	
		//			cur_frm.set_df_property("reserva_numero","hidden",true)
		//			cur_frm.set_df_property("servico_pago_por","hidden",true)
			}else{
				alert("Outro coisa")
			}

		

		}else if (cx_open.responseText == "{}" && cx_open.readyState == 4){
			//alert("Faca abertura do Caixa primeiro.")
			cur_frm.toggle_enable("nome_mesa",false)
			cur_frm.toggle_enable("cartao_numero",false)
			cur_frm.toggle_enable("nome_cliente",false)
			cur_frm.toggle_enable("pagamento_por",false)
			cur_frm.toggle_enable("produtos",false)
			cur_frm.toggle_enable("status_atendimento",false)
			cur_frm.toggle_enable("total_servicos",false)
			cur_frm.toggle_enable("valor_pago",false)

			cur_frm.disable_save()
			return
		
		}else{
//			alert("CAIXA")
			//JSON status still 1... no CAIXA Info
			cur_frm.toggle_enable("nome_mesa",false)
			cur_frm.toggle_enable("cartao_numero",false)
			cur_frm.toggle_enable("nome_cliente",false)
			cur_frm.toggle_enable("pagamento_por",false)
			cur_frm.toggle_enable("produtos",false)
			cur_frm.toggle_enable("status_atendimento",false)
			cur_frm.toggle_enable("total_servicos",false)
			cur_frm.toggle_enable("valor_pago",false)

			if (frm.doc.conta_corrente_status =="Pago"){
				cur_frm.toggle_enable("conta_corrente_status",false)
			}else{
				cur_frm.toggle_enable("conta_corrente_status",true)
			}
			
			return

		}


	}
});

frappe.ui.form.on('Atendimento Bar', {
	refresh: function(frm) {


		if (cx_open.statusText=="OK" ){
			if (cx_open.responseText != "{}"){
				//CAIXA aberto ...
//TEMP DISABLED
//				frm.fields_dict.produtos.grid.get_field('produtos').get_query = function() {
//					return {
//						filters: {
				
//				 			"disabled":0
//						}
//					}
			
//				}
	
//				frm.fields_dict.nome_mesa.get_query = function(doc){
//					return{
//						filters:{
//							"status_mesa":"Livre",

//						},
				
//					}
//				}

// END TEMP DISABLED 

//				if (cur_frm.doc.bar_tender == undefined){

//					cur_frm.fields_dict["bar_tender"].set_value = frappe.session.user	
//					cur_frm.refresh_fields("bar_tender")	

//				}	


				var me = this;
				if(this.load){
					alert(this.load)				
					this.load = false;
				}else {
					//alert("outra coisa")

					if (frm.doc.status_atendimento=="Ocupado" && frm.doc.bar_tender ==undefined){
						//Novo Registo
		//				cur_frm.page.clear_primary_action()
		//				cur_frm.page.clear_secondary_action()
		//				cur_frm.page.set_primary_action()
//TEMP DISABLED						cur_frm.page.clear_user_actions()

					}else if (cur_frm.doc.docstatus==0 &&  frm.doc.status_atendimento !="Fechado" &&  frm.doc.pagamento_por =="None") {
						cur_frm.page.set_secondary_action(__("PAGAMENTO"), function() {
							//me.validate()
							//me.create_invoice();
							//me.make_payment();
							//msgprint("Botao Pagar")
							//Muda o docstatus para poder imprimir.
							cur_frm.doc.docstatus = 1 
							//pagamento_botao(frm)
					
							frm.cscript.pagamento_botao.call()

							// Retira o menu NEW
							//cur_frm.page.clear_primary_action()

						}, "octicon octicon-credit-card");
					}else if(cur_frm.doc.docstatus == 1) {
//TEMP DISABLED
//						cur_frm.page.set_primary_action(__("Imprimir"), function() {
		//					html = frappe.render_template("Recibo_Bar_Restaurante", {"nome_mesa": cur_frm.doc.nome_mesa})
//							frappe.get_print("Print Format","Recibo_Bar_Restaurante",cur_frm.doc.nome_mesa)
//							print_document(html)
//						})
					}else if (frm.doc.status_atendimento !="Fechado") {
		//				cur_frm.page.clear_primary_action()
						//cur_frm.page.set_primary_action()
//TEMP DISABLED						cur_frm.page.clear_user_actions()
					}else if (frm.doc.status_atendimento =="Fechado") {
						show_alert("Registo Fechado. Nao se Altera")
						cur_frm.disable_save()				
//TEMP DISABLED						cur_frm.page.clear_primary_action()
//TEMP DISABLED						cur_frm.page.clear_secondary_action()
					}

		//			cur_frm.page.set_secondary_action(__("Save"), function() {
		//				me.save_previous_entry();
		//				me.create_new();
		//			}, "octicon octicon-plus").addClass("btn-primary");
				}	

		//		if (cur_frm.fields_dict["total_servicos"].df.fieldtype =="Currency" && cur_frm.fields_dict["total_servicos"].df.options){
		//			if (cur_frm.doc.total_servicos.df.fieldtype=="Currency" && cur_frm.doc.total_servicos.df.options) {
		//			if (cur_frm.fields_dict["total_servicos"].df.options!=-1){
		//				add_field(cur_frm.fields_dict["total_servicos"].df.options.split(":")[1]);
		//				}
		
		//			}
		//		}
				//if (cur_frm.doc.status_atendimento=="Ocupado"){
				//	frm.set_df_property("status_atendimento","options","Fechado")
				//}
			}else{
				alert("Por favor abrir o Caixa antes de qualquer movimento. " )
				cur_frm.disable_save()
				return
			}
		}else if (cx_open.readyState==1 ){
		// ++++++ POR RESOLVER 
			console.log("Verificando se o CAIXA Ja esta aberto....")
			if (frm.doc.status_atendimento =="Fechado") {
				show_alert("Registo Fechado. Nao se Altera")
				cur_frm.disable_save()			
			}



		}else{
			alert("PORQUE")
		}

	}
});


frappe.ui.form.on("Atendimento Bar","nome_mesa",function(frm,cdt,cdn){

	if (caixaopen == undefined){
		alert("CAIXA ESTA FECHADO. NAO PODE FAZER VENDAS!")
//		show_alert(cx_open.responseText)
		cur_frm.disable_save()	
		cur_frm.toggle_enable("cartao_numero",false)
		cur_frm.toggle_enable("nome_cliente",false)
		cur_frm.toggle_enable("produtos",false)

	}else{
		frappe.model.set_value(cdt,cdn,'bar_tender',frappe.session.user)
		cur_frm.refresh_fields('bar_tender')

	}
	if (cx_open.statusText=="OK" ){
		if (cx_open.responseText != "{}"){
				//CAIXA aberto ...
//			frappe.model.set_value(cdt,cdn,'bar_tender',frappe.session.user)
			cur_frm.refresh_fields('bar_tender')
		}
	}
	frm.fields_dict.produtos.grid.get_field('produtos').get_query = function() {
		return {
			filters: {
				
	 			"disabled":0
			}
		}
			
	}

	cur_frm.toggle_enable("status_atendimento",false)

});

cur_frm.add_fetch('produtos','standard_rate','produtos_preco')	

frappe.ui.form.on("Atendimento Bar Itens","produtos",function(frm,cdt,cdn){

	var d =locals[cdt][cdn];
	
	if (d.produtos !=""){
		servicos_('Item',d.produtos)
	}

	if (frm.doc.status_atendimento=="Fechado"){
		frappe.utils.filter_dict(frm.fields_dict["produtos"].grid.docfields, {"fieldname": "nome_servico"})[0].read_only = true;	
		frappe.utils.filter_dict(frm.fields_dict["produtos"].grid.docfields, {"fieldname": "quantidade"})[0].read_only = true;	
		frappe.utils.filter_dict(frm.fields_dict["produtos"].grid.docfields, {"fieldname": "produtos_preco"})[0].read_only = true;
		frappe.utils.filter_dict(frm.fields_dict["produtos"].grid.docfields, {"fieldname": "produtos_total"})[0].read_only = true;
	
	}else{
		frappe.model.set_value(cdt,cdn,'produtos_total',d.produtos_preco*d.quantidade)
		frappe.utils.filter_dict(frm.fields_dict["produtos"].grid.docfields, {"fieldname": "produtos_preco"})[0].read_only = true;
		frappe.utils.filter_dict(frm.fields_dict["produtos"].grid.docfields, {"fieldname": "produtos_total"})[0].read_only = true;
		
		calculate_totals(frm, cdt, cdn);
	}

});


frappe.ui.form.on("Atendimento Bar Itens","quantidade",function(frm,cdt,cdn){

	var d =locals[cdt][cdn];
//	cur_frm.add_fetch('nome_servico','preco','preco_servico')
//	servicos_('Item',d.nome_servico)

	frappe.model.set_value(cdt,cdn,'produtos_total',d.produtos_preco*d.quantidade)
	frappe.utils.filter_dict(frm.fields_dict["produtos"].grid.docfields, {"fieldname": "produtos_preco"})[0].read_only = true;
	frappe.utils.filter_dict(frm.fields_dict["produtos"].grid.docfields, {"fieldname": "produtos_total"})[0].read_only = true;

	calculate_totals(frm, cdt, cdn);


});

//FUNCOES PARA CALCULOS

var servicos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var d = frappe.model.get_doc(frm,cdt)
		frappe.model.set_value(cdt,cdn,frappe.utils.filter_dict(cur_frm.fields_dict["produtos"].grid.docfields, {"fieldname": "produtos_preco"}),d.standard_rate)
		cur_frm.refresh_fields()


	});
}


var calculate_totals = function(frm, cdt,cdn) {
	var tbl1 = frm.doc.produtos || [];
	var total_valor = 0; 
	for(var i = 0; i < tbl1.length; i++){
		total_valor += flt(tbl1[i].produtos_total);
	}
	frappe.model.set_value(cdt,cdn,'total_servicos',total_valor)
	frm.doc.total_servicos = total_valor
	refresh_many(['total_servicos']);
}


var pagamento_cash = function(prioridade){

	//Bar_Restaurante status Fechado ... Ja nao se pode alterar.
	frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'status_atendimento',"Fechado")
	frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'pagamento_por',prioridade)
	frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'valor_pago',cur_frm.doc.total_servicos)
	cur_frm.refresh_fields("status_atendimento");	
	cur_frm.doc.docstatus = 1 
	cur_frm.save() //this.cur_page.page.frm._save()
	cur_frm.disable_save()	
	cur_frm.print_doc()
}


cur_frm.cscript.pagamento_botao = function() {

	var d = locals[cur_frm.doctype][cur_frm.docname]

	//alert("Apos pagamento a Mesa estará livre.");
	calculate_totals(cur_frm,cur_frm.doctype,cur_frm.docname)	
	avancar = false

	var d = frappe.prompt([
		{label:__("Valor a Pagar: "),fieldtype:"Currency",fieldname:"apagar",read_only: 1,default: cur_frm.doc.total_servicos},
		{label:__("Valor Pago: "),fieldtype:"Currency",fieldname:"vpago",default: cur_frm.doc.total_servicos},
		{label:__("Troco: "),fieldtype:"Currency",fieldname:"troco",read_only: 1},
        	{label:__("Pagamento por:"), fieldtype:"Select",options: ["Cash","TPA", "Conta-Corrente","Não Pagar"],fieldname:"priority",'reqd': 1,default:"Cash"},
        ],
        function(values){
            var c = d.get_values();
            var me = this;
            show_alert("Selecionado : " + c.priority,5)
		// Status Mesa deve mudar para Livre
		// Status do Bar_Restaurante para 


		if (c.priority=="Não Pagar"){
			//Manter bar_restaurante status OCUPADO
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'status_atendimento',"Ocupado")
			cur_frm.refresh_fields("status_atendimento");	

		} else if (c.priority=="Cash")  {
			if ((c.vpago-c.apagar) !=0){
				frappe.confirm('Troco de: ' + (c.vpago-c.apagar) + ' Confirma?',
					function(){
						pagamento_cash(c.priority)

					},	
					function(){
						show_alert("Pagamento Cancelado !!!",5)

					}		

				);
			}else{
				pagamento_cash(c.priority)
			}
		} else if (c.priority=="TPA") {
			//Bar_Restaurante status Fechado ... Ja nao se pode alterar.
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'status_atendimento',"Fechado")
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'pagamento_por',c.priority)
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'valor_pago',cur_frm.doc.total_servicos)
			cur_frm.refresh_fields("status_atendimento");	
			cur_frm.doc.docstatus = 1 
//			cur_frm.toggle_enable("pagamento_botao",false)

//			cur_frm.page.btn_primary.click()
			cur_frm.save() //this.cur_page.page.frm._save()
			cur_frm.disable_save()
			cur_frm.print_doc()

//TEMP DISABLED			cur_frm.page.clear_primary_action()
//TEMP DISABLED			cur_frm.page.clear_secondary_action()

//			cur_frm.page.set_primary_action(__("Imprimir"), function() {
//					html = frappe.render_template("Recibo_Bar_Restaurante", {"nome_mesa": cur_frm.doc.nome_mesa})
//				frappe.get_print("Print Format","Recibo_Bar_Restaurante",cur_frm.doc.nome_mesa)
//				print_document(html)
//			})
			

		} else if (c.priority=="Conta-Corrente") {
			alert("Modulo nao ativo ...")
			avancar = false
			return
			//Bar_Restaurante status Fechado ... Ja nao se pode alterar.
			//Contas ou valores para a Conta corrente do cliente.
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'status_atendimento',"Fechado")
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'pagamento_por',"Conta-Corrente")
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'conta_corrente',"nome do cliente")
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'valor_pago',cur_frm.doc.total_servicos)
			cur_frm.refresh_fields("status_atendimento");	
			//Dialog a pedir o Cliente
			// Status tem que mudar para conta-corrente ...
			
			if (cur_frm.doc.nome_cliente=="Diversos"){
				// Verifica se nome_cliente is empty e pede para selecionar o Cliente autorizado (MEMBROS ONLY!!!!)
				avancar = true	
				CC_nomecliente()	
				cur_frm.toggle_enable("pagamento_botao",false)		
			}


		}

        },
        	'Pagamento',
	        'Fazer Pagamento'
     
        );
}


