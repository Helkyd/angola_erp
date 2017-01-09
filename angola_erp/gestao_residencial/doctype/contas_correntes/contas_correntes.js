// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contas Correntes', {

	onload: function(frm, cdt,cdn) {


		cur_frm.toggle_enable("cc_nome_cliente",false)	
		cur_frm.toggle_enable("cc_table_detalhes",false)	
		cur_frm.toggle_enable("cc_valor_divida",false)	
		cur_frm.toggle_enable("cc_valores_pagos",false)	

		frappe.utils.filter_dict(frm.fields_dict["cc_table_detalhes"].grid.docfields, {"fieldname": "numero_registo"})[0].read_only = true;	
		frappe.utils.filter_dict(frm.fields_dict["cc_table_detalhes"].grid.docfields, {"fieldname": "descricao_servico"})[0].read_only = true;	
		frappe.utils.filter_dict(frm.fields_dict["cc_table_detalhes"].grid.docfields, {"fieldname": "total"})[0].read_only = true;	
		frappe.utils.filter_dict(frm.fields_dict["cc_table_detalhes"].grid.docfields, {"fieldname": "total_servicos"})[0].read_only = true;	
		frappe.utils.filter_dict(frm.fields_dict["cc_table_detalhes"].grid.docfields, {"fieldname": "data_registo"})[0].read_only = true;	

		frappe.utils.filter_dict(frm.fields_dict["cc_table_detalhes"].grid.docfields, {"fieldname": "cc_tipo"})[0].read_only = true;	
	
	},
	refresh: function(frm) {

		frappe.ui.form.GridRow = frappe.ui.form.GridRow.extend(
		{
			set_data: function() {

				console.log(this.doc.status_conta_corrente)
			},

		});

		cur_frm.page.set_secondary_action(__("ACTUALIZAR CONTAS"), function() {

			//Look for all records not inserted to update the debt
			ordem = cur_frm.call({method:"get_bar_restaurante_cc",args:{"cliente":cur_frm.doc.cc_nome_cliente}})

			divida = 0
			pago = 0
			var contas = frm.doc.cc_table_detalhes || 	 [];
			for (var i = 0; i < contas.length; i++){
				if (contas[i].status_conta_corrente == "Não Pago") {
					divida += contas[i].total
				}else if (contas[i].status_conta_corrente == "Pago") {
					pago += contas[i].total
				}

			}
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'cc_valor_divida',divida)
			frappe.model.set_value(cur_frm.doctype,cur_frm.docname,'cc_valores_pagos',pago)

			refresh_field("cc_valor_divida","cc_table_detalhes")
			

			//Reorder IDX

		}, "octicon octicon-credit-card");

		if (cur_frm.doc.cc_status_conta_corrente =="Não Pago"){
			cur_frm.toggle_enable("cc_status_conta_corrente",true)	
		}else{
			cur_frm.toggle_enable("cc_status_conta_corrente",false)	
		}




	}
});


frappe.ui.form.on("Contas Correntes","valor_divida",function(frm,cdt,cdn){

});


cur_frm.set_query("status_conta_corrente","cc_table_detalhes",function(doc,cdt,cdn){
	var d = locals[cdt][cdn]
	return{
		filters: [
			['status_conta_corrente','=','Pago']
		]
			
	}

});



frappe.ui.form.on("CC_detalhes","status_conta_corrente",function(doc,cdt,cdn){

	//Needs to update the Record from BAR or Quarto to PAGO
	var d =locals[cdt][cdn];
	if (d.status_conta_corrente == "Pago"){	

		if (d.cc_tipo == "Bar"){
			qq = cur_frm.call({method:"set_bar_cc",args:{"cliente":d.numero_registo}})
		}else if  (d.cc_tipo == "Quarto"){
			qq = cur_frm.call({method:"set_quartos_cc",args:{"cliente":d.numero_registo}})
		}
	}	
});

frappe.ui.form.on("Contas Correntes","cc_status_conta_corrente",function(frm,cdt,cdn){
	if (cur_frm.doc.cc_status_conta_corrente =="Pago"){

		frappe.confirm(
		    'Todas as contas NAO PAGAS seram fechadas. Tem a certeza?',
		    function(){
//			cur_frm.save()
//			cur_frm.refresh()
			show_alert("Processando Contas...por favor aguarde",3 )

			fechar_contas = cur_frm.doc.cc_table_detalhes || [];

			for (var i = 0; i < fechar_contas.length; i++){
				if (fechar_contas[i].cc_tipo == "Bar"){
					qq = cur_frm.call({method:"set_bar_cc",args:{"cliente":fechar_contas[i].numero_registo}})
				}else if  (fechar_contas[i].cc_tipo == "Quarto"){
					qq = cur_frm.call({method:"set_quartos_cc",args:{"cliente":fechar_contas[i].numero_registo}})
				}
				fechar_contas[i].status_conta_corrente = "Pago"

			}
			cur_frm.save()
			cur_frm.refresh()

		
			
		    },
		    function(){
			show_alert('Cancelada!')
			cur_frm.doc.cc_status_conta_corrente =="Não Pago"
		    }
		)

	}

});

