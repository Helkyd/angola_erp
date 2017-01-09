// Copyright (c) 2016, Helio de Jesus and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reservas', {

	onload: function(frm) {

//		cur_frm.call({method:"verifica_check_in",args:{"start":"0"}})
		cur_frm.enable_save()
		if (frm.doc.reservation_status=="Nova" && frm.doc.pay_advance !="Sim" && frm.doc.numero_cliente ==undefined){
			cur_frm.toggle_enable("booked_by",true)
			cur_frm.toggle_enable("numero_cliente",true)	
			cur_frm.toggle_enable("reservation_status",false)	
			cur_frm.toggle_enable("number_days",false)
			cur_frm.set_df_property("pagamentos","hidden",true)
		
		}else if (frm.doc.reservation_status=="Nova" && frm.doc.pay_advance !="Sim"){
			cur_frm.toggle_enable("booked_by",false)
			cur_frm.toggle_enable("numero_cliente",false)	
			cur_frm.toggle_enable("check_in",false)	
			cur_frm.toggle_enable("check_out",false)	
			cur_frm.toggle_enable("number_days",false)
			cur_frm.toggle_enable("preco_quarto",false)
			cur_frm.toggle_enable("total_reserva",false)
			cur_frm.toggle_enable("numero_quarto",false)	
			cur_frm.toggle_enable("quarto_tipo",false)	
			cur_frm.toggle_enable("num_adults",false)	
			cur_frm.toggle_enable("num_childs",false)	
			cur_frm.toggle_enable("num_infants",false)	
			cur_frm.toggle_enable("pay_advance",false)	

		}else if (frm.doc.reservation_status=="Cancelada" ){
			cur_frm.toggle_enable("booked_by",false)	
			cur_frm.toggle_enable("check_in",false)	
			cur_frm.toggle_enable("check_out",false)	
			cur_frm.toggle_enable("num_adults",false)	
			cur_frm.toggle_enable("num_childs",false)	
			cur_frm.toggle_enable("num_infants",false)	
			cur_frm.toggle_enable("numero_quarto",false)	
			cur_frm.toggle_enable("numero_cliente",false)	
			cur_frm.toggle_enable("reservation_status",false)
			cur_frm.toggle_enable("pay_advance",false)		
			cur_frm.toggle_enable("number_days",false)
			cur_frm.toggle_enable("preco_quarto",false)
		
		}else if (frm.doc.reservation_status=="Ativo"){
			cur_frm.toggle_enable("booked_by",false)	
			cur_frm.toggle_enable("check_in",false)	
			cur_frm.toggle_enable("check_out",false)	
			cur_frm.toggle_enable("num_adults",false)	
			cur_frm.toggle_enable("num_childs",false)	
			cur_frm.toggle_enable("num_infants",false)	
			cur_frm.toggle_enable("numero_quarto",false)	
			cur_frm.toggle_enable("numero_cliente",false)	
			cur_frm.toggle_enable("pay_advance",false)
			cur_frm.toggle_enable("number_days",false)
			cur_frm.toggle_enable("preco_quarto",false)
			cur_frm.toggle_enable("quarto_tipo",false)
			cur_frm.toggle_enable("paid_type",false)
			cur_frm.toggle_enable("valor_pago",false)
			cur_frm.disable_save()


		}else if (frm.doc.reservation_status=="Fechada" ){
			cur_frm.toggle_enable("booked_by",false)	
			cur_frm.toggle_enable("check_in",false)	
			cur_frm.toggle_enable("check_out",false)	
			cur_frm.toggle_enable("num_adults",false)	
			cur_frm.toggle_enable("num_childs",false)	
			cur_frm.toggle_enable("num_infants",false)	
			cur_frm.toggle_enable("numero_quarto",false)	
			cur_frm.toggle_enable("numero_cliente",false)	
			cur_frm.toggle_enable("reservation_status",false)
			cur_frm.toggle_enable("pay_advance",false)		
			cur_frm.toggle_enable("number_days",false)
			cur_frm.toggle_enable("preco_quarto",false)
			cur_frm.toggle_enable("quarto_tipo",false)
			cur_frm.toggle_enable("paid_type",false)
			cur_frm.toggle_enable("valor_pago",false)
			cur_frm.disable_save()
		}


	},
	refresh: function(frm) {
		cur_frm.fields_dict['numero_quarto'].get_query = function(doc){
			return{
				filters:{
					"status_quarto":"Livre"
				}
			}
		}

		//Filter only Noite
		cur_frm.fields_dict['quarto_tipo'].get_query = function(doc){
			return{
				filters:{
					"diaria_hora":['in','Diaria,Noite'] 
				}
			}
		}


		//Filter Customers * menos Diversos


		if (cur_frm.doc.reservation_status=="Ativo"){
			frm.set_df_property("reservation_status","options","Ativo\nPago")
		}else if (cur_frm.doc.reservation_status=="Nova"){
			frm.set_df_property("reservation_status","options","Nova\nAtivo\nCancelada")

		}

		if (cur_frm.doc.pay_advance=="Sim"){
			cur_frm.set_df_property("pagamentos","hidden",false)
		}else{
			cur_frm.set_df_property("pagamentos","hidden",true)
		}

		cur_frm.refresh_fields()


	}
});



frappe.ui.form.on('Reservas','numero_quarto',function(frm,cdt,cdn){




});


frappe.ui.form.on('Reservas','pay_advance',function(frm,cdt,cdn){
	if (cur_frm.doc.pay_advance=="Sim"){
		cur_frm.set_df_property("pagamentos","hidden",false)
	}else{
		cur_frm.set_df_property("pagamentos","hidden",true)
	}

});

frappe.ui.form.on('Reservas','quarto_tipo',function(frm,cdt,cdn){

	quartos_('Tipo de Quartos',frm.doc.quarto_tipo)
	cur_frm.refresh_fields('preco_quarto','total_reserva')
	frappe.model.set_value(cdt,cdn,'total_reserva',(frm.doc.preco_quarto*frm.doc.number_days))
	cur_frm.refresh_fields();



});

frappe.ui.form.on('Reservas','numero_cliente',function(frm,cdt,cdn){

	quartos_('Tipo de Quartos',frm.doc.quarto_tipo)
	cur_frm.refresh_fields('preco_quarto','total_reserva')
	frappe.model.set_value(cdt,cdn,'total_reserva',(frm.doc.preco_quarto*frm.doc.number_days))
	frappe.model.set_value(cdt,cdn,'booked_by',frappe.session.user)
	cur_frm.refresh_fields();



});
frappe.ui.form.on('Reservas','check_in',function(frm,cdt,cdn){

	//Check_in cannot be less than TODAYs date
	if (frm.doc.check_in < frappe.datetime.nowdate()) {
		msgprint(__("Data de Entrada nao pode ser inferior a Data de Hoje."))
		frappe.model.set_value(cdt,cdn,'check_in','')
		frappe.model.set_value(cdt,cdn,'check_out','')
		frappe.model.set_value(cdt,cdn,'total_reserva',(frm.doc.preco_quarto*frm.doc.number_days))
		cur_frm.refresh_fields()		
		return;
	}else{
		frappe.model.set_value(cdt,cdn,'check_out',frappe.datetime.add_days(frm.doc.check_in, 2))
		frappe.model.set_value(cdt,cdn,'number_days',frappe.datetime.get_day_diff(frm.doc.check_out , frm.doc.check_in))
		frappe.model.set_value(cdt,cdn,'total_reserva',(frm.doc.preco_quarto*frm.doc.number_days))
		cur_frm.refresh_fields()

	} 


});
frappe.ui.form.on('Reservas','check_out',function(frm,cdt,cdn){

	//Check_out cannot be less than Check_In
	if (frm.doc.check_out < frm.doc.check_in) {
		msgprint(__("Data de Saida nao pode ser inferior a Data de Entrada."))
		return;
	} 

	frappe.model.set_value(cdt,cdn,'number_days',frappe.datetime.get_day_diff(frm.doc.check_out , frm.doc.check_in))
	frappe.model.set_value(cdt,cdn,'total_reserva',(frm.doc.preco_quarto*frm.doc.number_days))
	cur_frm.refresh_fields()

});

frappe.ui.form.on('Reservas','reservation_status',function(frm,cdt,cdn){


	if (frm.doc.reservation_status =="Cancelada") {
		show_alert("Verificando se pode ser cancelado a Reserva!!!",3)
		frappe.call({
			method: "angola_erp.gestao_residencial.doctype.api.get_gestao_quartos_check",
			args: {
				"quarto":frm.doc.numero_quarto,
				
			},
			callback: function(r) {
//				msgprint(r.message)
				if (r.message !=undefined){
					alert("Ocupado ou Ativo. Nao por ser cancelado!!!")
					frappe.model.set_value(cdt,cdn,'reservation_status',"Ativo")
					return
				}else{
					alert("Salve o registo Cancelar.")
				}

			}
		});

	}else if (frm.doc.reservation_status =="Ativo") {
	//Cria na Gestao_quartos...
		 show_alert("Status do Quarto Ocupado depois de SALVAR O REGISTO...",2)

	}	
});

var quartos_ = function(frm,cdt,cdn){
	frappe.model.with_doc(frm, cdt, function() { 
		var d = frappe.model.get_doc(frm,cdt)
		cur_frm.doc.preco_quarto = d.preco
		cur_frm.refresh_fields()


	});
}
