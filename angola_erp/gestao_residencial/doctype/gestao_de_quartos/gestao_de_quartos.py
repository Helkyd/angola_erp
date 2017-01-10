# -*- coding: utf-8 -*-
# Copyright (c) 2015, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime, timedelta
from frappe.utils import cstr, get_datetime, getdate, cint, get_datetime_str, flt
from frappe.model.document import Document
from frappe.model.naming import make_autoname

form_grid_templates = {
	"items": "templates/form_grid/gestao_quartos_list.html"
}

class GestaodeQuartos(Document):


	def autoname(self):
		self.name = make_autoname(self.numero_quarto + '-' + '.#####')


	def validate(self):
		print "DOC STATUS"
		print self.docstatus
		self.Validar_Numero_Dias()
		self.Check_ContaCorrente()
		self.Sethoras_Quarto()
		self.Contas_Correntes()

	def Validar_Numero_Dias(self):
		if self.horas <= 0:
			validated=False
			frappe.throw(_("Horas/Dias tem que ser 1 ou mais."))

		elif self.hora_entrada == self.hora_saida:
			validated=False
			frappe.throw(_("Hora de Saida tem que sair diferente que Hora de Entrada."))


	def on_update(self):
		self.Quartos_Status()
		self.Reservas_Status()
		#self.valor_pago = self.total_servicos


	def Quartos_Status(self):

		# Change Quarto status 
		quarto = frappe.get_doc("Quartos", self.numero_quarto)
		
		if self.status_quarto == "Ocupado":
			quarto.status_quarto = "Ocupado"
		elif self.status_quarto == "Ativo":
			quarto.status_quarto = "Ocupado"
		elif self.status_quarto == "Livre":
			quarto.status_quarto = "Livre"
		elif self.status_quarto == "Fechado":
			quarto.status_quarto = "Livre"

		quarto.save()		

	def Reservas_Status(self):
		#Change Reservas status
		if (self.status_quarto == "Fechado") and  (self.reserva_numero != None) :
			reserva = frappe.get_doc("RESERVAS",self.reserva_numero)
			reserva.reservation_status = "Fechada"
			reserva.save()
			
			

	def Check_ContaCorrente(self):
		# Not yet Implemented...
		if (self.servico_pago_por=="Conta-Corrente"):
			self.nome_cliente = self.conta_corrente
			if (self.conta_corrente == "") or (self.conta_corrente == "nome do cliente"):
				validated= False
				frappe.throw(_("Nao foi selecionado o Cliente para Conta-Corrente."))

#			validated= False
#			frappe.throw(_("Modulo nao funcional de momento."))

		if (self.pagamento_por=="Conta-Corrente"):
			if (self.conta_corrente == "") or (self.conta_corrente == "nome do cliente"):
				validated= False
				frappe.throw(_("Nao foi selecionado o Cliente para Conta-Corrente."))


	def Sethoras_Quarto(self):
		
		if self.hora_diaria_noite == "Noite":			
			self.hora_saida= get_datetime(self.hora_entrada) + timedelta(hours=12)			
		elif self.hora_diaria_noite == "Diaria":
			self.hora_saida= get_datetime(self.hora_entrada) + timedelta(days=self.horas)
		elif self.hora_diaria_noite == "Hora":
			self.hora_saida = get_datetime(self.hora_entrada) + timedelta(hours=self.horas)

		print "DEPOIS DE CALCULAR"
		print self.hora_saida


	def Contas_Correntes(self):
				#aproveita criar ja o registo no Conta-correntes
		if (self.conta_corrente !="nome do cliente") and (self.conta_corrente !=None) and (self.status_quarto == "Fechado") and (self.conta_corrente_status == "Não Pago") :
			if (frappe.db.sql("""select cc_nome_cliente from `tabContas Correntes` WHERE cc_nome_cliente =%s """,self.conta_corrente, as_dict=False)) != ():
				#existe faz os calculos da divida
				print " CLIENTE JA EXISTE"
				ccorrente = frappe.get_doc("Contas Correntes", self.conta_corrente)
				print "CLIENTE"
				print ccorrente.name

				totalextra = 0

				cc_detalhes = frappe.new_doc("CC_detalhes")
				cc_detalhes.parent = ccorrente.name
				cc_detalhes.parentfield = "cc_table_detalhes"
				cc_detalhes.parenttype = "Contas Correntes"
					
				cc_detalhes.descricao_servico = self.name #extras.nome_servico
				cc_detalhes.name = self.name
				cc_detalhes.numero_registo = self.name
				cc_detalhes.total = self.total #extras.total_extra
				cc_detalhes.total_servicos = self.total_servicos #extras.total_extra
				cc_detalhes.data_registo = self.hora_entrada
				totalextra = totalextra + self.total_servicos  + self.total #extras.total_extra

				cc_detalhes.status_conta_corrente = "Não Pago"
				cc_detalhes.tipo = "Quarto"
				cc_detalhes.idx += 1	
					
				cc_detalhes.insert()

				print (ccorrente.cc_valor_divida + totalextra)
				ccorrente.cc_valor_divida = flt(ccorrente.cc_valor_divida) + totalextra
				#ccorrente.save()

			else:
				#novo
				print " CLIENTE NAO EXISTE"
				print self.conta_corrente
				ccorrente = frappe.new_doc("Contas Correntes")
				ccorrente.cc_nome_cliente = self.conta_corrente
				ccorrente.name = self.conta_corrente
				ccorrente.cc_status_conta_corrente = "Não Pago"
				ccorrente.insert()

				print "CONTAS CORRENTES FEITA !!!!!!"

				totalextra = 0

				cc_detalhes = frappe.new_doc("CC_detalhes")
				cc_detalhes.parent =ccorrente.name
				cc_detalhes.parentfield = "cc_table_detalhes"
				cc_detalhes.parenttype = "Contas Correntes"

					#print extras.nome_servico
				cc_detalhes.descricao_servico = self.name #extras.nome_servico
				cc_detalhes.name = self.name
				cc_detalhes.numero_registo = self.name
				cc_detalhes.total = self.total #extras.total_extra
				cc_detalhes.total_servicos = self.total_servicos #extras.total_extra
				cc_detalhes.data_registo = self.hora_entrada
				totalextra = totalextra + self.total_servicos  + self.total #extras.total_extra

				cc_detalhes.status_conta_corrente = "Não Pago"
				cc_detalhes.tipo = "Quarto"
				cc_detalhes.insert()

				ccorrente.cc_valor_divida = flt(ccorrente.cc_valor_divida) + totalextra


@frappe.whitelist()
def lista_clientes():

	return frappe.db.sql("""select name from `tabCustomer` """, as_dict=False)


@frappe.whitelist()
def quartos_reservados():

	return frappe.db.sql("""select name,numero_quarto,check_in,reservation_status from `tabReservas` where reservation_status = 'Nova' """, as_dict=True)



@frappe.whitelist()
def atualiza_ccorrente(cliente,recibo):

	print cliente
	print recibo
	for ccorrente1 in frappe.db.sql("""SELECT name,numero_registo,parent,status_conta_corrente from `tabCC_detalhes` where numero_registo = %s and parent = %s """, (recibo,cliente), as_dict=True):
		print ccorrente1.name
		print "CAMPOS !!!!!"

		reset_idx = frappe.get_doc("CC_detalhes",ccorrente1.name)
		reset_idx.status_conta_corrente = "Pago"
		reset_idx.save()


