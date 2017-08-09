// Copyright (c) 2017, Helio de Jesus and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cadastro de Processo', {
	onload: function(frm) {
		if (cur_frm.doc.numero_de_processo != undefined){
			prj= cur_frm.call({method:"get_projecto_status",args:{"prj":cur_frm.doc.numero_de_processo}})
		}
		cur_frm.toggle_enable("data_criacao",false)
		cur_frm.toggle_enable("categoria",false)
		cur_frm.toggle_enable("advogado",false)
		cur_frm.toggle_enable("registado_por",false)

	},

	refresh: function(frm) {

		if (cur_frm.doc.estado == 'Em Curso' && !cur_frm.doc.__islocal || cur_frm.doc.estado == 'Concluido' ){

			frm.add_custom_button(__("Projecto"), function() {
				cur_frm.reload_doc()
				frappe.route_options = {"project_name": cur_frm.doc.name, "customer":cur_frm.doc.nome_do_autor}
				frappe.set_route("List", "Project");
			}, "Criar", true);

		}


	},
	validate: function(frm){
		//Check numero processo is Number and 4 digits.
		if (cur_frm.doc.numero_de_processo.length < 4){
			if (cur_frm.doc.numero_de_processo.length == 1){
				frappe.model.set_value(cdt,cdn,'numero_de_processo','000' + cur_frm.doc.numero_de_processo)
			}else if (cur_frm.doc.numero_de_processo.length == 2){
				frappe.model.set_value(cdt,cdn,'numero_de_processo','00' + cur_frm.doc.numero_de_processo)
			}else if (cur_frm.doc.numero_de_processo.length == 3){
				frappe.model.set_value(cdt,cdn,'numero_de_processo','0' + cur_frm.doc.numero_de_processo)
			}
			console.log(cur_frm.doc.numero_de_processo + cur_frm.doc.naming_series)
			validation = false
	
		}else if (cur_frm.doc.numero_de_processo.length > 4){
			if (cur_frm.doc.numero_de_processo.length != 16){
				alert('Numero de Processo tem que ter somente 4 digitos')
				frappe.model.set_value(cdt,cdn,'numero_de_processo',null)
				validation = false
			}
		}else if (cur_frm.doc.numero_de_processo == '0000'){
			alert('Numero de Processo nao pode ser 0000')
			frappe.model.set_value(cdt,cdn,'numero_de_processo',null)
			validation = false

		}
		if (isNaN(cur_frm.doc.numero_de_processo)){
			if (cur_frm.doc.numero_de_processo.length != 16){
				alert('Numero de Processo tem que ter somente digitos')
				frappe.model.set_value(cdt,cdn,'numero_de_processo',0)
				validation = false
			}
		}


	}
});

frappe.ui.form.on('Cadastro de Processo','nome_do_advogado',function(frm,cdt,cdn){

	frappe.model.set_value(cdt,cdn,'registado_por',frappe.session.user)
	nome_advogado_('Employee',cur_frm.doc.nome_do_advogado)
});

frappe.ui.form.on('Cadastro de Processo','tipo_de_processo',function(frm,cdt,cdn){

	categoria_('Tipo de Processo',cur_frm.doc.tipo_de_processo)
});

frappe.ui.form.on('Cadastro de Processo','nome_do_autor',function(frm,cdt,cdn){
	//Check numero processo is Number and 4 digits.

	if (cur_frm.doc.numero_de_processo.length < 4){
		if (cur_frm.doc.numero_de_processo.length == 1){
			frappe.model.set_value(cdt,cdn,'numero_de_processo','000' + cur_frm.doc.numero_de_processo)
		}else if (cur_frm.doc.numero_de_processo.length == 2){
			frappe.model.set_value(cdt,cdn,'numero_de_processo','00' + cur_frm.doc.numero_de_processo)
		}else if (cur_frm.doc.numero_de_processo.length == 3){
			frappe.model.set_value(cdt,cdn,'numero_de_processo','0' + cur_frm.doc.numero_de_processo)
		}
		console.log(cur_frm.doc.numero_de_processo + cur_frm.doc.naming_series)

	
	}else if (cur_frm.doc.numero_de_processo.length > 4){
		if (cur_frm.doc.numero_de_processo.length != 16){
			alert('Numero de Processo tem que ter somente 4 digitos')
			frappe.model.set_value(cdt,cdn,'numero_de_processo',null)
		}
	}else if (cur_frm.doc.numero_de_processo == '0000'){
		alert('Numero de Processo nao pode ser 0000')
		frappe.model.set_value(cdt,cdn,'numero_de_processo',null)

	}
});


var categoria_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var categ = frappe.model.get_doc(frm,cdt)
		if (categ){

			cur_frm.doc.categoria = categ.categoria

		}
		
		cur_frm.refresh_fields();

	});


}

var nome_advogado_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var advg = frappe.model.get_doc(frm,cdt)
		if (advg){

			cur_frm.doc.advogado = advg.employee_name

		}
		
		cur_frm.refresh_fields();

	});


}
