// Copyright (c) 2016, HELKyds lda. and contributors

// For license information, please see license.txt



var irt=0;
var inss=0;
var salario = 0;
var numero_faltas =0;
var valor_inicio =0;
var valor_fim = 0;
var valor_percentual = 0;
var parcela_fixa = 0;

lista_irt = cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.get_lista_irt",args:{}})



frappe.ui.form.on('Salary Slip', {

	refresh: function(frm) {

			//Get Salario

		var tbl1 = frm.doc.earnings || [];

//		var tbl2 = frm.doc.deductions || [];

		inss_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.get_inss",args:{}})	

		if (frm.doc.employee != undefined){
			if (numero_faltas.readyState == 4){
				cur_frm.doc.numero_de_faltas = numero_faltas.responseJSON.message[0]
			}else{
				numero_faltas = cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.get_faltas",args:{"emp":frm.doc.employee, "mes":frm.doc.month, "ano":frm.doc.fiscal_year}}) 
			}

		}else if (numero_faltas !=0){
			if (numero_faltas.readyState != 1){
				cur_frm.doc.numero_de_faltas = numero_faltas.responseJSON.message[0]
			}
		}
		
		for(var i = 0; i < tbl1.length; i++){

			if (tbl1[i].salary_component == "Salario Base" || tbl1[i].salary_component == "Basic" && tbl1[i].amount != 0){

				salario = tbl1[i].amount
				if (lista_irt.readyState !=1){
					for (var x =0; x < lista_irt.responseJSON.message.length; x++){
						//valor_inicio <= %(start)s and valor_fim >=%(start)s
						if (lista_irt.responseJSON.message[x].valor_inicio <= salario && lista_irt.responseJSON.message[x].valor_fim >= salario){
							valor_inicio = lista_irt.responseJSON.message[x].valor_inicio
							valor_fim = lista_irt.responseJSON.message[x].valor_fim
							valor_percentual = lista_irt.responseJSON.message[x].valor_percentual
							parcela_fixa = lista_irt.responseJSON.message[x].parcela_fixa	
							x = lista_irt.responseJSON.message.length +1 
	
						}else if (lista_irt.responseJSON.message[x].valor_fim >= salario){
							valor_inicio = lista_irt.responseJSON.message[x].valor_inicio
							valor_fim = lista_irt.responseJSON.message[x].valor_fim
							valor_percentual = lista_irt.responseJSON.message[x].valor_percentual
							parcela_fixa = lista_irt.responseJSON.message[x].parcela_fixa	

						}
					}
				}else{
					irt_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.get_irt",args:{"start":salario}})
				}

			}

		}	



		if(!frm.doc.__islocal) {

			cur_frm.add_custom_button(__('Calcular IRT & INSS'),cur_frm.cscript['calcular_irt_inss'], "icon-exclamation", "btn-default");


		}


	},

	

	onload: function(frm){

		frm.set_query("salary_component", "earnings", function(doc, cdt, cdn) {

			return {

				"filters": {

					"abono": 1,

				}

			};

		});

		frm.set_query("salary_component", "deductions", function(doc, cdt, cdn) {

			return {

				"filters": {

					"desconto": 1,

				}

			};

		});

		//calculate_all(frm.doc);


	},

});




cur_frm.cscript.calcular_irt_inss = function(doc,cdt,cdn){


//			cur_frm.add_custom_button(__('Calcular IRT & INSS'),function(doc, cdt, cdn) {

		var tbl1 = cur_frm.doc.earnings || [];

		var tbl2 = cur_frm.doc.deductions || [];

				for(var i = 0; i < tbl1.length; i++){

					if (tbl1[i].salary_component == "Salario Base" || tbl1[i].salary_component == "Basic" && tbl1[i].amount != 0){

						if (valor_fim !=0){
							irt = flt(salario) - valor_inicio;

							irt = (irt * valor_percentual/ 100) + parcela_fixa;
 						
						}else if (irt_valor.responseJSON.message[0].valor_inicio !=undefined){

							irt = flt(salario) - irt_valor.responseJSON.message[0].valor_inicio;

							irt = (irt * irt_valor.responseJSON.message[0].valor_percentual/ 100) + irt_valor.responseJSON.message[0].parcela_fixa;

						}else{

							irt = flt(salario) - irt_valor.responseJSON.message[0][0];

							irt = (irt * irt_valor.responseJSON.message[0][2]/ 100) + irt_valor.responseJSON.message[0][3];							

						}							

					}					

				}

				totaldeducoes = 0
				for(var j = 0; j < tbl2.length; j++){

					if (tbl2[j].salary_component == "IRT" ){

						irt_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.set_ded",args:{"ded":tbl2[j].name,"d_val":irt}});

					}else if (tbl2[j].salary_component == "INSS" ){	

						if (inss_valor.responseJSON.message !=undefined){

							//inss_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.get_inss",args:{}})	

							inss_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.set_ded",args:{"ded":tbl2[j].name,"d_val":flt(salario)*inss_valor.responseJSON.message}});

						}else{

							alert("INSS")

						}
					}else if (tbl2[j].salary_component == "Faltas Injustificadas" ){	
						//so pode ser feito no SALARY SLIP due to the Month being processed.
						//alert(total_days_in_month - numero_faltas.responseJSON.message[0])
							//desconto_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.set_ded",args:{"ded":tbl2[j].name,"d_val":(flt(salario)/26)*numero_faltas.responseJSON.message[0]}});

						//OUTRA Formula para desconto de Faltas SB/26/2+SB/26*numero_faltas
						desconto_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.set_ded",args:{"ded":tbl2[j].name,"d_val":(((flt(salario)/26)/2)+(flt(salario)/26))*numero_faltas.responseJSON.message[0]}});

						//if leave without pay 0 than payment days less numero_faltas otherwise working days - leave without - numero_faltas
						if (cur_frm.doc.leave_without_pay ==0){
							pagamentodias = cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.set_salary_slip_pay_days",args:{"emp":cur_frm.doc.employee, "mes":cur_frm.doc.month, "ano":cur_frm.doc.fiscal_year, "pag":(cur_frm.doc.total_days_in_month - numero_faltas.responseJSON.message[0]) }});
							frappe.model.set_value(cur_frm.doc.doctype,cur_frm.doc.name,'payment_days',cur_frm.doc.total_days_in_month  - numero_faltas.responseJSON.message[0]) 
						}else{
							pagamentodias = cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.set_salary_slip_pay_days",args:{"emp":cur_frm.doc.employee, "mes":cur_frm.doc.month, "ano":cur_frm.doc.fiscal_year, "pag":(cur_frm.doc.total_days_in_month - cur_frm.doc.leave_without_pay - numero_faltas.responseJSON.message[0]) }});
	
						}



					}	
					totaldeducoes += tbl2[j].amount

				}
				
				//calculate_earning_total(cur_frm.doc, cur_frm.doc.doctype, cur_frm.doc.name,true);

				//calculate_ded_total(cur_frm.doc, cur_frm.doc.doctype, cur_frm.doc.name,true);
//				cur_frm.doc.total_deduction = totaldeducoes
				frappe.model.set_value(cur_frm.doc.doctype,cur_frm.doc.name,'total_deduction',totaldeducoes)
				refresh_field('gross_pay','total_deduction');
				calculate_net_pay(cur_frm.doc, cur_frm.doc.doctype, cur_frm.doc.name);


//				cur_frm.refresh()

//				cur_frm.reload_doc()


//			});
}
