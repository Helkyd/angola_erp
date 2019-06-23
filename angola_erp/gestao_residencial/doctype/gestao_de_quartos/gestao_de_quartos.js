// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt


var estadoQuarto;
var horaentrada=0;
var debito_p_contab;


lista =cur_frm.call({method:"lista_clientes",args:{"start":"moeda"}})
quartosreservados  =cur_frm.call({method:"quartos_reservados",args:{"start":"moeda"}})
dados_perfil_pos = cur_frm.call({method:"erpnext.accounts.doctype.sales_invoice.pos.get_pos_data",args:{}})

modopagamento = cur_frm.call({method:"mode_of_payment",args:{"company":cur_frm.doc.company}})

frappe.provide("erpnext.accounts");

frappe.ui.form.on('Gestao de Quartos', {
	onload: function(frm) {

		console.log('ONload')
		if (frm.doc.status_quarto=="Ocupado" && frm.doc.horas >=0){
			//frappe.show_alert("aaaa")
			cur_frm.toggle_enable("numero_quarto",false)
			cur_frm.toggle_enable("horas",false)
			cur_frm.toggle_enable("hora_entrada",false)
			cur_frm.toggle_enable("hora_saida",false)
			cur_frm.toggle_enable("tipo_quarto",false)
			cur_frm.toggle_enable("pagamento_por",false)
			cur_frm.set_df_property("reserva_numero","hidden",true)
			cur_frm.set_df_property("servico_pago_por","hidden",true)
			cur_frm.toggle_enable("nome_cliente",false)
			cur_frm.toggle_enable("conta_corrente_status",false)


		}else if (frm.doc.status_quarto=="Ocupado" && frm.doc.horas ==undefined){
			//frappe.show_alert("bbbbbbb")
			cur_frm.toggle_enable("status_quarto",false)	
			cur_frm.set_df_property("reserva_numero","hidden",true)
			cur_frm.set_df_property("servico_pago_por","hidden",true)
			cur_frm.toggle_enable("hora_saida",false)
			cur_frm.toggle_enable("total",false)

		}else if (frm.doc.status_quarto=="Fechado"){
			cur_frm.toggle_enable("numero_quarto",false)
			cur_frm.toggle_enable("horas",false)
			cur_frm.toggle_enable("hora_entrada",false)
			cur_frm.toggle_enable("hora_saida",false)
			cur_frm.toggle_enable("tipo_quarto",false)
			cur_frm.toggle_enable("pagamento_por",false)	
			cur_frm.toggle_enable("status_quarto",false)	
			cur_frm.set_df_property("reserva_numero","hidden",true)
			cur_frm.set_df_property("servico_pago_por","hidden",true)
			//cur_frm.set_df_property("pagar_servicos","hidden",true)
			cur_frm.toggle_enable("nome_cliente",false)
//			cur_frm.doc.docstatus = 1 
			if (frm.doc.conta_corrente_status =="Pago"){
				cur_frm.toggle_enable("conta_corrente_status",false)
			}else{
				cur_frm.toggle_enable("conta_corrente_status",true)
			}

		}else if (frm.doc.status_quarto=="Ativo"){
			cur_frm.set_df_property("horas","label","Dias")
			cur_frm.toggle_enable("numero_quarto",false)
			cur_frm.toggle_enable("horas",false)
			cur_frm.toggle_enable("hora_entrada",false)
			cur_frm.toggle_enable("hora_saida",false)
			cur_frm.toggle_enable("tipo_quarto",false)
			cur_frm.toggle_enable("pagamento_por",false)
			cur_frm.set_df_property("reserva_numero","hidden",true)
			cur_frm.set_df_property("servico_pago_por","hidden",true)
			cur_frm.toggle_enable("nome_cliente",false)

		}


	}
});

frappe.ui.form.on('Gestao de Quartos', {
	refresh: function(frm) {
		console.log('Refresh')
		console.log(cur_frm.doc.__unsaved)
		console.log(cur_frm.doc.__islocal)
		cur_frm.fields_dict['numero_quarto'].get_query = function(doc){
			return{
				filters:{
					"status_quarto":['in','Livre, Reservado'] 
				}
			}
		}

		cur_frm.fields_dict.servicos.grid.get_field('servico_produto').get_query = function(){
			return{
				filters:{
					"is_sales_item": 1 
				}
			}
		
		}


		calculate_totals(frm);

		if (cur_frm.doc.status_quarto=="Livre"){
			frm.set_df_property("status_quarto","options","Ocupado\nFechado")
		}else if (cur_frm.doc.status_quarto=="Ocupado" && frm.doc.horas >=0){

			frm.set_df_property("status_quarto","options","Ocupado\nFechado")
		}else if (cur_frm.doc.status_quarto=="Ativo"){
			frm.set_df_property("status_quarto","options","Ativo\nFechado")

		}
	
		if (frm.doc.status_quarto=="Ocupado" && frm.doc.horas >=0){
			cur_frm.toggle_enable("numero_quarto",false)
			cur_frm.toggle_enable("horas",false)
			cur_frm.toggle_enable("hora_entrada",false)
			cur_frm.toggle_enable("hora_saida",false)
			cur_frm.toggle_enable("tipo_quarto",false)
			cur_frm.toggle_enable("pagamento_por",false)
			cur_frm.set_df_property("reserva_numero","hidden",true)
			cur_frm.set_df_property("servico_pago_por","hidden",true)
			cur_frm.toggle_enable("nome_cliente",false)
			cur_frm.toggle_enable("conta_corrente_status",false)

//			cur_frm.set_df_property("status_quarto","read-only",false)
			//cur_frm.doc.docstatus = 0
//			cur_frm.doc.__unsaved = 1
			cur_frm.toggle_enable("status_quarto",true)
			cur_frm.refresh_fields("status_quarto");	
		}

		if (frm.doc.total_servicos>0 && frm.doc.status_quarto != "Fechado"){

			frm.add_custom_button(__("Pagamento de Serviços"), function() {

				cur_frm.cscript.pagar_servicos(frm,cur_frm.doctype,cur_frm.docname) 
			});

		} 

		if (frm.doc.total_servicos == 0 && frm.doc.status_quarto == "Ocupado"){

			frm.add_custom_button(__("Fechado"), function() {
				frappe.show_alert("QUARTO LIVRE. Sem servicos por pagar...",3)

				console.log(frm.doc.__unsaved)
				console.log(frm.doc.__islocal)
				console.log(frm.doc.docstatus)
				//cur_frm.doc.status_quarto = 'Fechado'
				//frappe.model.set_value(frm.doctype,frm.docname,'status_quarto',"Fechado");
				//xxx = cur_frm.call({method:"update_statusquarto",args:{"doc": frm.docname, "status":"Fechado"}})
				cur_frm.call({
					method:"update_statusquarto",
					args:{
						"doc": frm.docname, 
						"status": "Fechado",
					},
					callback: function(r) {
						cur_frm.reload_doc()
						cur_frm.refresh_fields()
						
					}
				});
				

				//cur_frm.cscript.pagar_servicos(frm,cur_frm.doctype,cur_frm.docname) 
			});

		} 

		if (estadoQuarto != undefined){
			//Reservado
				
		}
		if (cur_frm.doc.__unsaved == undefined && cur_frm.doc.__islocal == undefined) {
//			cur_frm.reload_doc()
//			cur_frm.refresh_fields()

		}

	},


});


frappe.ui.form.on("Gestao de Quartos","numero_quarto",function(frm,cdt,cdn){


	if (cur_frm.doc.numero_quarto != undefined && cur_frm.doc.numero_quarto != ""){

		frappe.model.with_doc("Quartos", cur_frm.doc.numero_quarto, function() { 
			var d = frappe.model.get_doc("Quartos",cur_frm.doc.numero_quarto)
			estadoQuarto = d.status_quarto
			if (horaentrada !=0){
				if (estadoQuarto == "Reservado"){
					if (quartosreservados.responseText != "{}") {
						x = 0
						for (x in quartosreservados.responseJSON.message){
							if (quartosreservados.responseJSON.message[x].numero_quarto == cur_frm.doc.numero_quarto){
								horaentrada = quartosreservados.responseJSON.message[x].check_in
								x = quartosreservados.responseJSON.message.length + 1
							}			
						}
					}			

					if (frappe.datetime.get_hour_diff(horaentrada,moment().defaultDatetimeFormat) <=2){
						alert("Quarto Reservado!!! Menos de duas horas para ficar Ativo.\n Por favor selecione outro Quarto.")
						//horaentrada = 0
						frappe.model.set_value(cdt,cdn,'numero_quarto',"");
			
					}
					frappe.show_alert("Faltam: " + frappe.datetime.get_hour_diff(horaentrada,moment().defaultDatetimeFormat).toString() ) + " Horas."
				}
			}
		});

		if (cur_frm.doc.nome_cliente && cur_frm.doc.debit_to == undefined){
			debito_p_contab = cur_frm.call({method:"debit_to_acc",args:{"company":cur_frm.doc.company}})

		}




	}


	
});

frappe.ui.form.on("Gestao de Quartos","conta_corrente_status",function(frm,cdt,cdn){
	if (cur_frm.doc.conta_corrente_status == "Pago"){
		frappe.confirm('Confirma que pagamento foi feito?' ,
			function(){
				//update Conta-correntes table
	
				ccorrente = cur_frm.call({method:"atualiza_ccorrente",args:{"cliente":cur_frm.doc.conta_corrente,"recibo":cur_frm.doc.name}})
				cur_frm.save()
				cur_frm.disable_save()
//				cur_frm.print_doc()

			},	
			function(){
				frappe.show_alert("Pagamento Cancelado !!!",5)
			}		
		);
		
	}
});




frappe.ui.form.on('Gestao de Quartos','tipo_quarto',function(frm,cdt,cdn){

	quartos_('Tipo de Quartos',frm.doc.tipo_quarto)
	cur_frm.refresh_fields('standard_rate','hora_diaria_noite','total');
	if (cur_frm.doc.hora_diaria_noite =="Noite"){
		//disable Horas and set 1; disable hora_entrada and calculate as from now until 
		cur_frm.set_df_property("horas","label","Noite")
		frappe.model.set_value(cdt,cdn,'horas',1);

		frappe.model.set_value(cdt,cdn,'hora_saida',moment(moment(cur_frm.doc.hora_entrada).add(12,'hours')).format('DD/MM/YY, h:mm a'));
		frappe.model.set_value(cdt,cdn,'total',cur_frm.doc.preco*1)
	}else if (cur_frm.doc.hora_diaria_noite =="Hora"){
		// Horas set 2; 
		cur_frm.set_df_property("horas","label","Horas")
		frappe.model.set_value(cdt,cdn,'horas',2);

		frappe.model.set_value(cdt,cdn,'hora_saida',moment(moment(cur_frm.doc.hora_entrada).add(cur_frm.doc.horas,'hours')));
		cur_frm.doc.hora_saida = moment(cur_frm.doc.hora_entrada).add(cur_frm.doc.horas,'hours');
// moment(frm.doc.hora_entrada).add(frm.doc.horas,'hours')).format('DD/MM/YY, h:mm a'));
		frappe.model.set_value(cdt,cdn,'total',cur_frm.doc.preco*cur_frm.doc.horas)

	}else if (cur_frm.doc.hora_diaria_noite =="Diaria"){
		// Horas set 1 Dia; 
		cur_frm.set_df_property("horas","label","Dias")
		frappe.model.set_value(cdt,cdn,'horas',1);

		frappe.model.set_value(cdt,cdn,'hora_saida',frappe.datetime.add_days(cur_frm.doc.hora_entrada, 1));
		frappe.model.set_value(cdt,cdn,'total',cur_frm.doc.preco*cur_frm.doc.horas)


	}
	frappe.model.set_value(cdt,cdn,'usuario_quarto',frappe.session.user)
	frappe.model.set_value(cdt,cdn,'status_quarto','Ocupado')
//	cur_frm.doc.status_quarto=="Ocupado"
	cur_frm.refresh_fields();


	//Check if Quarto RESERVADO ... calculate time available 	

	if (estadoQuarto != undefined){
		if (estadoQuarto == "Reservado"){
			//Reservado
			if (quartosreservados.responseText != "{}") {
				x = 0
				for (x in quartosreservados.responseJSON.message){
					if (quartosreservados.responseJSON.message[x].numero_quarto == cur_frm.doc.numero_quarto){
						horaentrada = quartosreservados.responseJSON.message[x].check_in
						x = quartosreservados.responseJSON.message.length + 1
					}			
				}
			}
			if (horaentrada !=0){
				if (frappe.datetime.get_hour_diff(horaentrada,moment().defaultDatetimeFormat) <=2){
					alert("Quarto Reservado!!! Menos de duas horas para ficar Ativo.\n Por favor selecione outro Quarto.")
					//horaentrada = 0
					frappe.model.set_value(cdt,cdn,'numero_quarto',"");

				}
				frappe.show_alert("Faltam: " + frappe.datetime.get_hour_diff(horaentrada,moment().defaultDatetimeFormat).toString() ) + " Horas."

			}
		}			
	}

	
	if (debito_p_contab.readyState ==4){
//		frappe.model.set_value(cdt,cdn,'debit_to',debito_p_contab.responseJSON.message[0])		
		cur_frm.doc.debit_to = debito_p_contab.responseJSON.message[0][0]
//		cur_frm.doc.debit_to ='31121000-Clientes Nacionais - CF'
	}


});


frappe.ui.form.on('Gestao de Quartos','horas',function(frm,cdt,cdn){

	if (cur_frm.doc.hora_diaria_noite =="Noite"){
		//disable Horas and set 1; disable hora_entrada and calculate as from now until 
		frappe.model.set_value(cdt,cdn,'horas',1);
	//	frappe.model.set_value(cdt,cdn,'hora_entrada',frappe.utils.data.now_datetime());
		cur_frm.set_df_property("horas","label","Noite")
		frappe.model.set_value(cdt,cdn,'hora_saida',moment(cur_frm.doc.hora_entrada).add(12,'hours'));
		frappe.model.set_value(cdt,cdn,'total',cur_frm.doc.preco*1)
	}else if (cur_frm.doc.hora_diaria_noite =="Diaria"){
		// Horas set 1 Dia; 
		//frappe.model.set_value(cdt,cdn,'horas',1);
	//	frappe.model.set_value(cdt,cdn,'hora_entrada',frappe.utils.data.now_datetime());
		cur_frm.set_df_property("horas","label","Dias")
		frappe.model.set_value(cdt,cdn,'hora_saida',frappe.datetime.add_days(cur_frm.doc.hora_entrada, cur_frm.doc.horas));
		frappe.model.set_value(cdt,cdn,'total',cur_frm.doc.preco*cur_frm.doc.horas)

	}else{
		cur_frm.set_df_property("horas","label","Horas")
		frappe.model.set_value(cdt,cdn,'hora_saida',moment(moment(cur_frm.doc.hora_entrada).add(cur_frm.doc.horas,'hours')));
		//cur_frm.doc.hora_saida = moment(cur_frm.doc.hora_entrada).add(frm.doc.horas,'hours');
		frappe.model.set_value(cdt,cdn,'total',cur_frm.doc.preco*cur_frm.doc.horas)
		cur_frm.refresh_fields();	

	}
});


frappe.ui.form.on('Gestao de Quartos','hora_entrada',function(frm,cdt,cdn){

	if (frm.doc.hora_diaria_noite =="Noite"){

	}else if (frm.doc.hora_diaria_noite =="Diaria"){

	}else{
		frappe.model.set_value(cdt,cdn,'hora_saida',moment(moment(frm.doc.hora_entrada).add(frm.doc.horas,'hours')));;
		//cur_frm.doc.hora_saida = moment(cur_frm.doc.hora_entrada).add(frm.doc.horas,'hours');
		frappe.model.set_value(cdt,cdn,'total',frm.doc.preco*frm.doc.horas)

	}
	cur_frm.refresh_fields('total','hora_saida');	

});

cur_frm.add_fetch('servico_produto','standard_rate','preco_servico_produto')	

frappe.ui.form.on("Servicos_Quarto","servico_produto",function(frm,cdt,cdn){


	var d =locals[cdt][cdn];
	cur_frm.add_fetch('servico_produto','standard_rate','preco_servico_produto')	

	if (d.servico_produto != ""){ 
		servicos_('Item',d.servico_produto,cdn) 
	}

	cur_frm.refresh_fields('preco_servico_produto')

	if (frm.doc.status_quarto=="Fechado"){
		//frappe.model.set_value(cdt,cdn,'servico_produto',"")
		frappe.utils.filter_dict(frm.fields_dict["servicos"].grid.docfields, {"fieldname": "servico_produto"})[0].read_only = true;	
		frappe.utils.filter_dict(frm.fields_dict["servicos"].grid.docfields, {"fieldname": "quantidade"})[0].read_only = true;	
		frappe.utils.filter_dict(frm.fields_dict["servicos"].grid.docfields, {"fieldname": "preco_servico_produto"})[0].read_only = true;
		frappe.utils.filter_dict(frm.fields_dict["servicos"].grid.docfields, {"fieldname": "total_servico_produto"})[0].read_only = true;	
	
	}else{

//		cur_frm.refresh_fields('preco_servico_produto')

		frappe.model.set_value(cdt,cdn,'total_servico_produto',d.preco_servico_produto*d.quantidade)
		frappe.utils.filter_dict(frm.fields_dict["servicos"].grid.docfields, {"fieldname": "preco_servico_produto"})[0].read_only = true;
		frappe.utils.filter_dict(frm.fields_dict["servicos"].grid.docfields, {"fieldname": "total_servico_produto"})[0].read_only = true;
		calculate_totals(frm, cdt, cdn);
	}

});

frappe.ui.form.on("Servicos_Quarto","quantidade",function(frm,cdt,cdn){

	var d =locals[cdt][cdn];
	cur_frm.add_fetch('servico_produto','standard_rate','preco_servico_produto')

	servicos_('Item',d.servico_produto)

	frappe.model.set_value(cdt,cdn,'total_servico_produto',d.preco_servico_produto*d.quantidade)
	frappe.utils.filter_dict(frm.fields_dict["servicos"].grid.docfields, {"fieldname": "preco_servico_produto"})[0].read_only = true;
	frappe.utils.filter_dict(frm.fields_dict["servicos"].grid.docfields, {"fieldname": "total_servico_produto"})[0].read_only = true;
	calculate_totals(frm, cdt, cdn);


});


frappe.ui.form.on('Gestao de Quartos', {
//	before_save: function(frm){
//		console.log('before save')
		//Pagamentos para os Quartos Insert first and for services secord record
//		var pag = frm.add_child("pagamento")
//		pag.name = cur_frm.name;
//		pag.parentfield = "pagamento"
//		pag.parenttype = "Gestao de Quartos"
//		pag.amount = cur_frm.doc.total
//		pag.base_amount = cur_frm.doc.total
//		if (cur_frm.doc.pagamento_por == "Cash"){
//			pag.mode_of_payment = "Cash"
//		}else if (cur_frm.doc.pagamento_por == "TPA"){
//			pag.mode_of_payment = "TPA"
//
//		}
//		refresh_field("pagamento")
//	},

	validate: function(frm) {


	//Check if reservado selected ....


		console.log("Validando Dados...")
		frappe.show_alert("Validando Dados...",1)


		if (cur_frm.doc.hora_diaria_noite =="Noite"){
			cur_frm.set_df_property("horas","label","Noites")
			cur_frm.doc.hora_saida= moment(cur_frm.doc.hora_entrada).add(12,'hours');
			cur_frm.doc.total=cur_frm.doc.preco*cur_frm.doc.horas
		}else if (cur_frm.doc.hora_diaria_noite =="Diaria"){
			// Horas set 1 Dia; 
			cur_frm.set_df_property("horas","label","Dias")
			cur_frm.doc.hora_saida=frappe.datetime.add_days(cur_frm.doc.hora_entrada, cur_frm.doc.horas);
			cur_frm.doc.total=cur_frm.doc.preco*cur_frm.doc.horas

		}else{
			cur_frm.set_df_property("horas","label","Horas")
			cur_frm.doc.hora_saida=moment(moment(cur_frm.doc.hora_entrada).add(cur_frm.doc.horas,'hours'));
			cur_frm.doc.total = cur_frm.doc.preco*cur_frm.doc.horas
			//cur_frm.call({method:"horas_quarto",args:{"horain":frm.doc.hora_entrada,"horaout":frm.doc.hora_entrada,"registo":frm.doc.name}})
			cur_frm.reload_doc()
			cur_frm.refresh_fields();	

		}
		horaentrada=0;

		if (cur_frm.doc.__unsaved == undefined && cur_frm.doc.__islocal == undefined) {
			console.log('validar undefined unsaved and islocal')
//			cur_frm.reload_doc()
//			cur_frm.refresh_fields()

		}
	
	}

	
});


var calculate_totals = function(frm, cdt,cdn) {
	var tbl1 = frm.doc.servicos || [];
	var total_valor = 0; 
	for(var i = 0; i < tbl1.length; i++){
		total_valor += flt(tbl1[i].total_servico_produto);
	}
	frappe.model.set_value(cdt,cdn,'total_servicos',total_valor)
	frm.doc.total_servicos = total_valor
	refresh_many(['total_servicos']);
}

var calculate_totals1 = function(frm, cdt,cdn) {
	var d = locals[cdt][cdn]
	var tbl1 = frm.servicos || [];
	var total_valor = 0; 
	for(var i = 0; i < tbl1.length; i++){
		total_valor += flt(tbl1[i].total_servico_produto);
	}
	frappe.model.set_value(cdt,cdn,'total_servicos',total_valor)
	frm.total_servicos = total_valor
	refresh_many(['total_servicos']);
}

cur_frm.cscript.pagar_servicos = function(frm,cdt,cdn) {

//	alert("Apos pagamento dos Serviços o Quarto estará livre.");
	frappe.show_alert("Apos pagamento dos Serviços o Quarto estará livre.",2)
	//show_alert(cur_frm.doc.docstatus)
	if (cur_frm.doc.hora_diaria_noite =="Noite"){
		//disable Horas and set 1; disable hora_entrada and calculate as from now until 
//		frappe.model.set_value(cdt,cdn,'horas',1);
	//	frappe.model.set_value(cdt,cdn,'hora_entrada',frappe.utils.data.now_datetime());
		frappe.model.set_value(cdt,cdn,'hora_saida',moment(cur_frm.doc.hora_entrada).add(12,'hours'));
		frappe.model.set_value(cdt,cdn,'total',cur_frm.doc.preco*cur_frm.doc.horas)
	}else if (cur_frm.doc.hora_diaria_noite =="Diaria"){
		// Horas set 1 Dia; 
		//frappe.model.set_value(cdt,cdn,'horas',1);
	//	frappe.model.set_value(cdt,cdn,'hora_entrada',frappe.utils.data.now_datetime());
		frappe.model.set_value(cdt,cdn,'hora_saida',frappe.datetime.add_days(cur_frm.doc.hora_entrada, cur_frm.doc.horas));
		frappe.model.set_value(cdt,cdn,'total',cur_frm.doc.preco*cur_frm.doc.horas)

	}else{
		frappe.model.set_value(cdt,cdn,'hora_saida',moment(moment(cur_frm.doc.hora_entrada).add(cur_frm.doc.horas,'hours')));;
//		cur_frm.doc.hora_saida = moment(cur_frm.doc.hora_entrada).add(frm.doc.horas,'hours'));
		frappe.model.set_value(cdt,cdn,'total',cur_frm.doc.preco*cur_frm.doc.horas)
		cur_frm.refresh_fields();	

	}
//	if (cdt != undefined && cdn != undefined){
//		calculate_totals1(frm,cdt,cdn)	
//	}else{
		calculate_totals(frm)	
//	}

	console.log(modopagamento)

	opcao0 ="";
	opcao0_tipo = "";
	opcao1 = "";
	opcao1_tipo = "";
	opcao2 = "";
	opcao2_tipo = "";

//	if (modopagamento) {for (mod in modopagamento.responseJSON.message){(modopagamento.responseJSON.message[mod].parent) + "," }}
	if (modopagamento) {
		for (mod in modopagamento.responseJSON.message){
			if (mod == 0){
				opcao0 = modopagamento.responseJSON.message[mod].parent
				opcao0_tipo = modopagamento.responseJSON.message[mod].type
			}else if (mod == 1){ 
				opcao1 = modopagamento.responseJSON.message[mod].parent
				opcao1_tipo = modopagamento.responseJSON.message[mod].type
			} else{
				opcao2 = modopagamento.responseJSON.message[mod].parent
				opcao2_tipo = modopagamento.responseJSON.message[mod].type
			}
		}
		console.log(opcao0)
		console.log(opcao1)
		console.log(opcao2)
	}
	var d = frappe.prompt([
		{label:__("Valor a Pagar: "),fieldtype:"Currency",fieldname:"apagar",read_only: 1,default: cur_frm.doc.total_servicos},
		{label:__("Valor Pago: "),fieldtype:"Currency",fieldname:"vpago",default: cur_frm.doc.total_servicos},
		{label:__("Troco: "),fieldtype:"Currency",fieldname:"troco",read_only: 1},
        	{label:__("Pagamento por:"), fieldtype:"Select",options: [opcao0, opcao1, opcao2, "3-Conta-Corrente","4-Não Pagar"],fieldname:"priority",'reqd': 1,default:opcao0},

        ],
        function(values){
            var c = d.get_values();
            var me = this;
            frappe.show_alert("Selecionado : " + c.priority,5)
		// Status Quarto deve mudar para Livre
		// Status da Gestao_quarto para 
		if (c.priority=="4-Não Pagar"){
			//Manter Gestao_quarto status OCUPADO
			frappe.model.set_value(cdt,cdn,'status_quarto',"Ocupado")
			cur_frm.refresh_fields("status_quarto");	

		} else if (c.priority=="1-Cash") {
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


		}else if (c.priority=="2-TPA") {
			//Gestao_quarto status Fechado ... Ja nao se pode alterar.
			frappe.model.set_value(cdt,cdn,'servico_pago_por',c.priority)
			frappe.model.set_value(cdt,cdn,'status_quarto',"Fechado")
			cur_frm.refresh_fields("status_quarto");	

//			cur_frm.doc.docstatus = 1 

			//Adicionar o PAgamento na Sales Invoice Payment

			cur_frm.disable_save()	
			cur_frm.print_doc()


		} else if (c.priority=="3-Conta-Corrente") {
			//Gestao_quarto status Fechado ... Ja nao se pode alterar.
			//Contas ou valores para a Conta corrente do cliente.
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'status_quarto',"Fechado")
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'pagamento_por',"Conta-Corrente")
			if (cur_frm.doc.conta_corrente ==""){
				frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'conta_corrente',"nome do cliente")
			}
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'valor_pago',cur_frm.doc.total_servicos)
			frappe.model.set_value(cdt,cdn,'servico_pago_por',c.priority)

			cur_frm.refresh_fields("status_quarto");	


			//Dialog a pedir o Cliente
			if (cur_frm.doc.nome_cliente=="Diversos"){
				// Verifica se nome_cliente is empty e pede para selecionar o Cliente autorizado (MEMBROS ONLY!!!!)
				avancar = true	
				CC_nomecliente()	
				//cur_frm.toggle_enable("pagamento_botao",false)		
			}



			cur_frm.refresh_fields("status_quarto");	



		}
		
		if (c.priority == opcao0){
			if (opcao0_tipo == "Cash"){
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
			}else if (opcao0_tipo == "Bank"){
				//Gestao_quarto status Fechado ... Ja nao se pode alterar.
				frappe.model.set_value(cdt,cdn,'servico_pago_por',c.priority)
				frappe.model.set_value(cdt,cdn,'status_quarto',"Fechado")
				cur_frm.refresh_fields("status_quarto");	

				cur_frm.disable_save()	
				cur_frm.print_doc()
			}
		} else if (c.priority == opcao1){
			if (opcao1_tipo == "Cash"){
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
			}else if (opcao1_tipo == "Bank"){
				//Gestao_quarto status Fechado ... Ja nao se pode alterar.
				frappe.model.set_value(cdt,cdn,'servico_pago_por',c.priority)
				frappe.model.set_value(cdt,cdn,'status_quarto',"Fechado")
				cur_frm.refresh_fields("status_quarto");	

				cur_frm.disable_save()	
				cur_frm.print_doc()
			}
	
		} else if (c.priority == opcao2){
			if (opcao2_tipo == "Cash"){
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
			}else if (opcao2_tipo == "Bank"){
				//Gestao_quarto status Fechado ... Ja nao se pode alterar.
				frappe.model.set_value(cdt,cdn,'servico_pago_por',c.priority)
				frappe.model.set_value(cdt,cdn,'status_quarto',"Fechado")
				cur_frm.refresh_fields("status_quarto");	

				cur_frm.disable_save()	
				cur_frm.print_doc()
			}
		}
	


		cur_frm.enable_save()

        },
        	'Pagamento',
	        'Fazer Pagamento'
        );
	
}


frappe.ui.form.on("Gestao de Quartos","status_quarto",function(frm,cdt,cdn){


	if (frm.doc.status_quarto=="Livre"){
	// Tem que verificar se as contas estao pagas.
		alert("Verificando contas")

	}else if (frm.doc.status_quarto=="Fechado"){
	// Tem que verificar os pagamentos ....
		cur_frm.toggle_display("servico_pago_por",true)
		if (cur_frm.doc.total_servicos != 0) {
			if (frm.doc.servico_pago_por == opcao0){
				//any opcao as long is Cash or TPA
				if ((opcao0_tipo == "Bank") || (opcao0_tipo == "Cash")){
					// Pode prosseguir com pagamento
					//alert("Pagamento de Serviços feito. Por favor salvar registo para liberar o Quarto.")	
					frappe.show_alert("Pagamento de Serviços feito. QUARTO LIVRE",3)
					this.cur_page.page.frm._save()

				}

			}else if (frm.doc.servico_pago_por == opcao1){
				//any opcao as long is Cash or TPA
				if ((opcao1_tipo == "Bank") || (opcao1_tipo == "Cash")){
					// Pode prosseguir com pagamento
					//alert("Pagamento de Serviços feito. Por favor salvar registo para liberar o Quarto.")	
					frappe.show_alert("Pagamento de Serviços feito. QUARTO LIVRE",3)
					this.cur_page.page.frm._save()

				}
		
			}else if (frm.doc.servico_pago_por == opcao2){
				//any opcao as long is Cash or TPA
				if ((opcao2_tipo == "Bank") || (opcao2_tipo == "Cash")){
					// Pode prosseguir com pagamento
					//alert("Pagamento de Serviços feito. Por favor salvar registo para liberar o Quarto.")	
					frappe.show_alert("Pagamento de Serviços feito. QUARTO LIVRE",3)
					this.cur_page.page.frm._save()

				}

			} else if ((frm.doc.servico_pago_por =="1-Cash") || (frm.doc.servico_pago_por =="2-TPA")){
				// Pode prosseguir com pagamento
				//alert("Pagamento de Serviços feito. Por favor salvar registo para liberar o Quarto.")	
				frappe.show_alert("Pagamento de Serviços feito. QUARTO LIVRE",3)
				this.cur_page.page.frm._save()
			} else if (frm.doc.pagamento_por =="Conta-Corrente"){ 
				//Conta-Corrente, can close as long as client name is correct
				if (frm.doc.nome_cliente !="Diversos"){ 

				}
			} else if (frm.doc.total_servicos==0) {	
				frappe.show_alert("QUARTO LIVRE. Sem servicos por pagar...",3)

				console.log(frm.doc.__unsaved)
				console.log(frm.doc.__islocal)
				console.log(frm.doc.docstatus)
	//			cur_frm.doc.__unsaved = 1
				if (cur_frm.doc.docstatus == 0) {
					cur_frm.doc.docstatus = 1 //TO Submit
		//			cur_frm.save() 
		//			this.cur_page.page.frm._save()
					this.cur_page.page.frm.savesubmit()
		//			this.cur_page.page.frm._update()
					cur_frm.toggle_enable("status_quarto",false)

		//			cur_frm.reload_doc()
		//			cur_frm.refresh_fields()
				}	
			} else {
				// Esta vazio .....
				alert("Pagamento de servicos em falta!!!")	
				cur_frm.disable_save()
	//			frappe.model.set_value(cdt,cdn,'status',"Ocupado")
	//			cur_frm.refresh_fields("status");	
			}

		} else if (frm.doc.total_servicos==0) {	
			frappe.show_alert("QUARTO LIVRE. Sem servicos por pagar...",3)

			console.log(frm.doc.__unsaved)
			console.log(frm.doc.__islocal)
			console.log(frm.doc.docstatus)
//			cur_frm.doc.__unsaved = 1
			if (cur_frm.doc.docstatus == 0) {
				cur_frm.doc.docstatus = 1 //TO Submit
	//			cur_frm.save() 
	//			this.cur_page.page.frm._save()
				this.cur_page.page.frm.savesubmit()
	//			this.cur_page.page.frm._update()
				cur_frm.toggle_enable("status_quarto",false)

	//			cur_frm.reload_doc()
	//			cur_frm.refresh_fields()
			}	
		} else {
			// Esta vazio .....
			alert("Pagamento de servicos em falta!!!")	
			cur_frm.disable_save()
//			frappe.model.set_value(cdt,cdn,'status',"Ocupado")
//			cur_frm.refresh_fields("status");	
		}

//	}else if ((frm.doc.status_quarto=="Ativo") && (frm.doc.reserva_numero !="")){
	//ATIVO only from RESERVAS
//		alert("Quarto Ativo... por favor Salvar registo")
//		frappe.show_alert("QUARTO ATIVO. Salvando registo...",3)
//		this.cur_page.page.frm._save()	
//		cur_frm.reload_doc()	
	}

});

frappe.ui.form.on("Gestao de Quartos","pagamento_por",function(frm,cdt,cdn){

	if (frm.doc.pagamento_por=="Conta-Corrente"){
	// Pedir o Cliente e se o mesmo for membro e autorizado ...
 
//		alert("Somente Membros podem ter Conta-corrente")
		//Gestao_quarto status Fechado ... Ja nao se pode alterar.
		//Contas ou valores para a Conta corrente do cliente.
		//frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'status_quarto',"Fechado")
		frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'pagamento_por',"Conta-Corrente")
		frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'conta_corrente',"nome do cliente")
		frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'valor_pago',cur_frm.doc.total_servicos)
//		frappe.model.set_value(cdt,cdn,'servico_pago_por',c.priority)

		cur_frm.refresh_fields("status_quarto");	

		//Dialog a pedir o Cliente
		if (cur_frm.doc.nome_cliente=="Diversos"){
			// Verifica se nome_cliente is empty e pede para selecionar o Cliente autorizado (MEMBROS ONLY!!!!)
			avancar = true	
			CC_nomecliente()	
			//cur_frm.toggle_enable("pagamento_botao",false)		
		}

	} else if (frm.doc.pagamento_por=="Cash"){

	} else if (frm.doc.pagamento_por=="TPA"){

	}

});


cur_frm.set_query("debit_to", function(doc) {
	// filter on Account
	if (cur_frm.doc.nome_cliente) {
		return {
			filters: {
				'account_type': 'Receivable',
				'is_group': 0,
				'company': cur_frm.doc.company
			}
		}
	} else {
		return {
			filters: {
				'report_type': 'Balance Sheet',
				'is_group': 0,
				'company': cur_frm.doc.company
			}
		}
	}
});


var quartos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var d = frappe.model.get_doc(frm,cdt)

		cur_frm.doc.preco = d.preco
		cur_frm.doc.hora_diaria_noite = d.diaria_hora
		cur_frm.set_value("horas",2)
		cur_frm.refresh_fields()

	});


}


var servicos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var d = frappe.model.get_doc(frm,cdt)
//		cur_frm.doc.preco_servico_produto = d.standard_rate
		frappe.model.set_value(cdt,cdn,frappe.utils.filter_dict(cur_frm.fields_dict["servicos"].grid.docfields, {"fieldname": "preco_servico_produto"}),d.standard_rate)
	
		frappe.model.set_value(cdt,cdn,frappe.utils.filter_dict(cur_frm.fields_dict["servicos"].grid.docfields, {"fieldname": "income_account"}),"Sales - CF") //dados_perfil_pos['income_account'] || d.income_account)


		frappe.model.set_value(cdt,cdn,frappe.utils.filter_dict(cur_frm.fields_dict["servicos"].grid.docfields, {"fieldname": "warehouse"}),dados_perfil_pos['warehouse'] || d.default_warehouse)

		frappe.model.set_value(cdt,cdn,frappe.utils.filter_dict(cur_frm.fields_dict["servicos"].grid.docfields, {"fieldname": "cost_center"}),dados_perfil_pos['cost_center'] || d.selling_cost_center)




		if ( d.is_stock_item && d.total_projected_qty == 0 ){
			alert("Este produto nao tem em Stock!!!")
		}

		cur_frm.refresh_fields()


	});
}


var CC_nomecliente = function(frm,cdt,cdn){
	var listaclientes= []
	if (lista.statusText=="OK"){
		for (x in lista.responseJSON.message){
			if (lista.responseJSON.message[x] != "Diversos" && lista.responseJSON.message[x] != undefined){
				listaclientes[x]= lista.responseJSON.message[x]
			}
		}
	}

	if (avancar==true){
		var dd = frappe.prompt([
			{label:__("Nome do Cliente: "),fieldtype:"Select",fieldname:"pcliente",options: [listaclientes[0],listaclientes[1],listaclientes[2],listaclientes[3],listaclientes[4]]},
	        ],
        	function(values){
	        	var cc = dd.get_values();
            		var mee = this;
			frappe.show_alert("Selecionado : " + cc.pcliente,5)
			if (cc.pcliente !=""){
				cur_frm.set_value(cdt,cdn,'status_quarto',"Fechado")
				cur_frm.set_value(cdt,cdn,'pagamento_por',"Conta-Corrente")
				cur_frm.set_value('conta_corrente',cc.pcliente)
				cur_frm.set_value('servico_pago_por',"Conta-Corrente")

				cur_frm.refresh_fields("status_quarto","conta_corrente");	
				//Click SAVE				
//				cur_frm.page.btn_primary.click()
				this.cur_page.page.frm._save()
				cur_frm.page.clear_primary_action()
				cur_frm.page.clear_secondary_action()



				cur_frm.page.set_primary_action(__("Imprimir"), function() {
//					html = frappe.render_template("Recibo_Bar_Restaurante", {"nome_mesa": cur_frm.doc.nome_mesa})
					frappe.get_print("Print Format","GESTAO_QUARTOS_1",cur_frm.doc.numero_quarto)
					print_document(html)
				})

				//alert("Cliente " + cc.pcliente + " selecionado")
			}
		},
			'Lista de Clientes Membros',
			'Processar Conta-Corrente'
		);

	}



}

var pagamento_cash = function(prioridade){
	
	console.log('pagamento cash')
	//Quarto Status Fechado ... Ja nao se pode alterar.
	frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'servico_pago_por',prioridade)
	frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'status_quarto',"Fechado")


	cur_frm.refresh_fields("status_quarto");	
	cur_frm.toggle_enable("status_quarto",false)

//	frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'valor_pago',cur_frm.doc.total_servicos)

//	cur_frm.doc.docstatus = 1 
//	cur_frm.save() //this.cur_page.page.frm._save()


	//Adicionar o PAgamento na Sales Invoice Payment


	cur_frm.disable_save()	
	cur_frm.print_doc()


}

// Income Account in Details Table
// --------------------------------
cur_frm.set_query("income_account", "servicos", function(doc) {
	return{
		query: "erpnext.controllers.queries.get_income_account",
		filters: {'company': doc.company}
	}
});

// Cost Center in Details Table
// -----------------------------
cur_frm.fields_dict["servicos"].grid.get_field("cost_center").get_query = function(doc) {
	return {
		filters: {
			'company': doc.company,
			"is_group": 0
		}
	}
}

cur_frm.cscript.cost_center = function(doc, cdt, cdn) {
	erpnext.utils.copy_value_in_all_row(doc, cdt, cdn, "servicos", "cost_center");
}
