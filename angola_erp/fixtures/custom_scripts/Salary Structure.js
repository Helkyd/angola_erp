// Copyright (c) 2016, HELKyds lda. and contributors
// For license information, please see license.txt

var irt=0;
var inss=0;
var salario = 0;
var numero_faltas =0;

frappe.ui.form.on('Salary Structure', {
	refresh: function(frm) {
			//Get Salario
		var tbl1 = frm.doc.earnings || [];
		var tbl2 = frm.doc.deductions || [];

		inss_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.get_inss",args:{}})	
		for(var i = 0; i < tbl1.length; i++){
			if (tbl1[i].salary_component == "Salario Base" || tbl1[i].salary_component == "Basic" && tbl1[i].amount != 0){
				salario = tbl1[i].amount
				irt_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.get_irt",args:{"start":salario}})
			}
		}	

		if(!frm.doc.__islocal) {
			cur_frm.add_custom_button(__('Calcular IRT & INSS'),function(doc, cdt, cdn) {

				for(var i = 0; i < tbl1.length; i++){
					if (tbl1[i].salary_component == "Salario Base" || tbl1[i].salary_component == "Basic" && tbl1[i].amount != 0){
						if (irt_valor.responseJSON.message[0].valor_inicio !=undefined){
							irt = flt(salario) - irt_valor.responseJSON.message[0].valor_inicio;
							irt = (irt * irt_valor.responseJSON.message[0].valor_percentual/ 100) + irt_valor.responseJSON.message[0].parcela_fixa;
						}else{
							irt = flt(salario) - irt_valor.responseJSON.message[0][0];
							irt = (irt * irt_valor.responseJSON.message[0][2]/ 100) + irt_valor.responseJSON.message[0][3];							
						}							
					}					
				}
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

							//desconto_valor =cur_frm.call({method:"angola_erp.angola_erpnext.validations.irt.set_ded",args:{"ded":tbl2[j].name,"d_val":flt(salario)*numero_faltas}});

					}	
				}
				cur_frm.refresh()
				cur_frm.reload_doc()
				calculate_totals(frm.doc);
			});
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
		calculate_totals(frm.doc);
	},
});



