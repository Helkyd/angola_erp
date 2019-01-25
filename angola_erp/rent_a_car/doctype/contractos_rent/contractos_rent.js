// Copyright (c) 2019, Helio de Jesus and contributors
// For license information, please see license.txt


//clientes1 = cur_frm.call({method:"get_clientaddres",args:{}})
var cliente_


frappe.ui.form.on('Contractos Rent', {

	onload: function(frm) {
		cur_frm.fields_dict['matricula'].get_query = function(doc){
			return{
				filters:{
					"veiculo_alugado":0,
				},
				
			}
		}	

	},
	refresh: function(frm) {
		if (cliente_ != undefined){
			if (cliente_.responseJSON.message != undefined){
				cur_frm.doc.morada_cliente = cliente_.responseJSON.message.address_line1
				cur_frm.doc.contact = cliente_.responseJSON.message.phone
				cur_frm.refresh_fields('morada_cliente')
			}
		}

		if (cur_frm.doc.docstatus == 1) {
			if(cur_frm.doc.status_contracto == "Activo") {
				console.log('adiciona botao')
				frm.add_custom_button(__('Gerar Factura'), function() {
					agora_entrada = true
					botao_checkin = false

					criarFacturas = cur_frm.call({method:"angola_erp.angola_erp.angola_erp.rent_a_car.doctype.contractos_rent.criar_faturavenda",args:{frm:cur_frm}})

			}else{
				console.log('limpa botoes')
				frm.clear_custom_buttons()
			}

		}
	},




});


frappe.ui.form.on('Contractos Rent','nome_do_cliente',function(frm,cdt,cdn){

	if (cur_frm.doc.nome_do_cliente){

		console.log('endereco clientes')	
		cliente_ = cur_frm.call({method:"angola_erp.util.angola.get_cliente_address",args:{"cliente":cur_frm.doc.nome_do_cliente}})

	}

	cur_frm.toggle_enable("status_contracto",false)
	cur_frm.toggle_enable("operador",false)
	frappe.model.set_value(cdt,cdn,'operador',frappe.session.user)


	frappe.model.set_value(cdt,cdn,'data_de_saida',moment(cur_frm.doc.data_do_contracto).add(3,'hours'));
	frappe.model.set_value(cdt,cdn,'devolucao_prevista',frappe.datetime.add_days(cur_frm.doc.data_do_contracto, 3));



});

frappe.ui.form.on('Contractos Rent','matricula',function(frm,cdt,cdn){
	console.log('matricula')
	if (cur_frm.doc.nome_do_cliente){
		if (cur_frm.doc.matricula != undefined){
			veiculos_('Vehicle',cur_frm.doc.matricula)
			cur_frm.refresh_fields('marca_modelo');
		}
	}
});


frappe.ui.form.on('Contractos Rent','data_nascimento_cliente',function(frm,cdt,cdn){
	//nao pode ser < 18 anos.
	console.log('menor de idade')
	if (cint(frappe.datetime.get_day_diff(frappe.datetime.nowdate() , cur_frm.doc.data_nascimento_cliente)) < 18){
		frappe.show_alert("Menor de idade não é permitido",5)
		cur_frm.doc.data_nascimento_cliente = ""
	}


});


frappe.ui.form.on('Contractos Rent','kms_out',function(frm,cdt,cdn){
	//so pode ser numeros...
	console.log('kms out')
	if (isNaN(cur_frm.doc.kms_out) == true){
 		frappe.show_alert("Somente numeros",5)
		cur_frm.doc.kms_out = ""
	}


});

frappe.ui.form.on('Contractos Rent','carta_conducao_cliente',function(frm,cdt,cdn){

	if (cliente_ != undefined){
		if (cliente_.responseJSON.message != undefined){
			cur_frm.doc.morada_cliente = cliente_.responseJSON.message.address_line1
			cur_frm.doc.contact = cliente_.responseJSON.message.phone
			cur_frm.refresh_fields('morada_cliente')
		}
	}

});


frappe.ui.form.on('Contractos Rent','local_de_saida',function(frm,cdt,cdn){

	if (cur_frm.doc.local_de_saida){
		frappe.model.set_value(cdt,cdn,'local_previsto_entrada',cur_frm.doc.local_de_saida)		
	}

});


frappe.ui.form.on('Contractos Rent','grupo',function(frm,cdt,cdn){
	console.log('grpuos')
	if (cur_frm.doc.grupo){
		tarifario_("Tarifas",frm)

	}

});



var veiculos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var carro = frappe.model.get_doc(frm,cdt)
		if (carro){
			cur_frm.doc.marca_modelo = carro.model
			//cur_frm.doc.or_modelo_veiculo = carro.modelo
			cur_frm.doc.cor = carro.color
			cur_frm.doc.combustivel = carro.fuel_type
			cur_frm.doc.kms_out = carro.last_odometer

		}
		
		cur_frm.refresh_fields();

	});


}



var termos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var termos1 = frappe.model.get_doc(frm,cdt)
		if (termos1){
			cur_frm.doc.termos = termos1.terms

		}
		
		cur_frm.refresh_fields();

	});


}


var tarifario_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var termos1 = frappe.model.get_doc(frm,cdt)
		if (termos1){
			console.log ('Dias')
			console.log(frappe.utils.date_diff(frappe.utils.now(),doc.devolucao_prevista))

			cur_frm.doc.valor_pdia = termos1.basico_dia
			cur_frm.doc.total_dia = termos1.basico_dia * (frappe.utils.date_diff(frappe.utils.now(),doc.devolucao_prevista))

		}
		
		cur_frm.refresh_fields();

	});


}


