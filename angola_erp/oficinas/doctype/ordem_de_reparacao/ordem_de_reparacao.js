// Copyright (c) 2019, Helio de Jesus and contributors
// For license information, please see license.txt

frappe.ui.form.on('Ordem de Reparacao', {
	onload: function(frm) {
	

//		cur_frm.toggle_enable("or_date",false)
		cur_frm.toggle_enable("or_operador",false)
		cur_frm.toggle_enable("or_marca_veiculo",false)
		cur_frm.toggle_enable("or_modelo_veiculo",false)
		cur_frm.toggle_enable("or_numero_chassi",false)
		cur_frm.toggle_enable("or_numero_motor",false)
		cur_frm.toggle_enable("or_ano_veiculo",false)

		if (cur_frm.doc.pertence_empresa == 0) {
			cur_frm.get_field('or_nome_cliente').df.reqd = true
			cur_frm.get_field('or_terms').df.reqd = true

		}
		cur_frm.get_field('or_matricula').df.reqd = true

	}
		
});

frappe.ui.form.on('Ordem de Reparacao', {
	refresh: function(frm) {

		if (cur_frm.doc.pertence_empresa == 0) {
			cur_frm.get_field('or_nome_cliente').df.reqd = true
			cur_frm.get_field('or_terms').df.reqd = true

		}
		cur_frm.get_field('or_matricula').df.reqd = true

		if (cur_frm.doc.or_status == 'Em Curso'){
			cur_frm.toggle_enable("or_operador",false)
			cur_frm.toggle_enable("or_marca_veiculo",false)
			cur_frm.toggle_enable("or_modelo_veiculo",false)
			cur_frm.toggle_enable("or_numero_chassi",false)
			cur_frm.toggle_enable("or_numero_motor",false)
			cur_frm.toggle_enable("or_ano_veiculo",false)
			cur_frm.toggle_enable("or_nome_cliente",false)
			cur_frm.toggle_enable("or_client_number",false)
			cur_frm.toggle_enable("or_email_cliente",false)
			cur_frm.toggle_enable("or_matricula",false)
			cur_frm.toggle_enable("or_kms_entrada",false)
			cur_frm.toggle_enable("or_date",false)
			cur_frm.toggle_enable("or_previsao_entrega",false)
			cur_frm.toggle_enable("or_nivel_combustivel",false)

			//Acessorios
			cur_frm.toggle_enable("or_macaco",false)
			cur_frm.toggle_enable("or_chave_rodas",false)
			cur_frm.toggle_enable("or_triangulo",false)
			cur_frm.toggle_enable("or_extintor",false)
			cur_frm.toggle_enable("or_ferramentas",false)
			cur_frm.toggle_enable("or_pneu_socorro",false)
			cur_frm.toggle_enable("or_porca_seguranca",false)

			//Interior e Exterior
			cur_frm.toggle_enable("or_radio",false)
			cur_frm.toggle_enable("or_drive_cd",false)
			cur_frm.toggle_enable("or_esqueiro",false)
			cur_frm.toggle_enable("retrovisor",false)
			cur_frm.toggle_enable("or_tapetes",false)
			cur_frm.toggle_enable("or_antena",false)
			cur_frm.toggle_enable("or_retrovisor_esquerdo",false)
			cur_frm.toggle_enable("or_retrovisor_direito",false)
			cur_frm.toggle_enable("or_tampao_combustivel",false)
			cur_frm.toggle_enable("or_limpa_parabrisas",false)
			cur_frm.toggle_enable("or_limpa_parabrisas_traseiro",false)


			cur_frm.toggle_enable("or_avarias_corrigir",false)
			cur_frm.toggle_enable("or_obs_cliente",false)

			cur_frm.toggle_enable("numero_ordem",false)
			frm.set_df_property("or_status","options","Em Curso\nFechada")
		}


		if (!cur_frm.doc.__islocal){

			frm.add_custom_button(__("Folha de Obras"), function() {
				cur_frm.reload_doc()
				cur_frm.reload_doc()
				frappe.route_options = {"ordem_reparacao": cur_frm.doc.name,"nome_cliente":cur_frm.doc.or_nome_cliente}
				frappe.set_route("List", "Folha de Obras");
			});


//			frm.add_custom_button(__("Folha de Obras"), function() {
//				cur_frm.reload_doc()
//				cur_frm.reload_doc()
//				frappe.route_options = {"ordem_reparacao": cur_frm.doc.name,"nome_cliente":cur_frm.doc.or_nome_cliente}
//				frappe.set_route("List", "Folha de Obras");
//			}, "icon-list", true);


		}


	}
});

frappe.ui.form.on('Ordem de Reparacao','pertence_empresa',function(frm,cdt,cdn){

	cur_frm.toggle_enable("or_client_number",false)
	cur_frm.toggle_enable("or_email_cliente",false)

	cur_frm.set_value("or_nome_cliente", "")
	cur_frm.set_value("or_matricula", "")

	cur_frm.fields_dict['or_matricula'].get_query = function(doc){
		return{
			filters:{
				"pertence_empresa":cur_frm.doc.pertence_empresa,
			},
				
		}
	}

});

frappe.ui.form.on('Ordem de Reparacao','or_nome_cliente',function(frm,cdt,cdn){

	cur_frm.toggle_enable("or_client_number",true)
	cur_frm.toggle_enable("or_email_cliente",true)

	cur_frm.get_field('or_terms').df.reqd = true

	frappe.model.set_value(cdt,cdn,'or_operador',frappe.session.user)
	if (cur_frm.doc.or_nome_cliente){
		customer_('Address',cur_frm.doc.or_nome_cliente+ "-Billing")
		cur_frm.refresh_fields('or_client_number');
	}

	cur_frm.fields_dict['or_matricula'].get_query = function(doc){
		return{
			filters:{
				"veiculo_cliente":cur_frm.doc.or_nome_cliente,
			},
				
		}
	}

});

frappe.ui.form.on('Ordem de Reparacao','or_matricula',function(frm,cdt,cdn){
	
	if (cur_frm.doc.or_nome_cliente || cur_frm.doc.pertence_empresa){
		if (cur_frm.doc.or_matricula != ""){
			veiculos_('Veiculos',cur_frm.doc.or_matricula)
			cur_frm.refresh_fields('or_marca_veiculo');
		}
	}
});


var customer_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var endereco = frappe.model.get_doc(frm,cdt)
		if (endereco){
			cur_frm.doc.or_client_number = endereco.phone
			cur_frm.doc.or_email_cliente = endereco.email_id
		//Check if has car already registered ....
		}
		cur_frm.refresh_fields();

	});


}

var veiculos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var carro = frappe.model.get_doc(frm,cdt)
		if (carro){
			cur_frm.doc.or_marca_veiculo = carro.marca
			cur_frm.doc.or_modelo_veiculo = carro.modelo
			cur_frm.doc.or_numero_chassi = carro.veiculo_numero_chassi
			cur_frm.doc.or_numero_motor = carro.veiculo_codigo_motor
			cur_frm.doc.or_ano_veiculo = carro.veiculo_ano
		}
		
		cur_frm.refresh_fields();

	});


}

