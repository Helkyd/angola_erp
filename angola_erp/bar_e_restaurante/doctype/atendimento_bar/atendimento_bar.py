# -*- coding: utf-8 -*-
# Copyright (c) 2015, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr, flt, getdate
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class AtendimentoBar(Document):


	def autoname(self):
		self.name = make_autoname(self.nome_mesa + '-' + '.#####')


	def validate(self):

        	if self.get('__islocal'):
           		print "LOCAL"
       
		elif (self.pagamento_por == "Conta-Corrente"):
			if (self.conta_corrente =="") or (self.conta_corrente == "nome do cliente"):
				frappe.throw(_("Cliente Conta-Corrente nao selecionado !!!! A MESA mantem-se aberta."))

		elif (frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)) ==():
			if (frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Em Curso' """, as_dict=False)) ==():
				validated=False
				frappe.throw(_("CAIXA de Registo esta fechada... Nenhum movimento podera ser feito."))



	def on_update(self):
		self.Mesas_Status()
		#self.Clientes_Status()
		#self.Contas_Correntes()


	def Mesas_Status(self):

		# Change Mesas status 
		mesa = frappe.get_doc("Mesas", self.nome_mesa)
		
		if self.status_atendimento == "Ocupado":
			mesa.status_mesa = "Ocupada"
	
		elif self.status_atendimento == "Livre":
			mesa.status_mesa = "Livre"
		elif self.status_atendimento == "Fechado":
			mesa.status_mesa = "Livre"

		mesa.save()		

	def Clientes_Status(self):
		#Update Cliente caso Conta-Corrente

		if (self.conta_corrente !="nome do cliente") and (self.conta_corrente !=None):
			cliente = frappe.get_doc("Customer", self.conta_corrente)	
			if (self.status_atendimento == "Fechado") and (self.conta_corrente != "nome do cliente") :
				cliente.conta_corrente = "Conta-Corrente"
				cliente.save()
	
	def Contas_Correntes(self):
				#aproveita criar ja o registo no Conta-correntes
		if (self.conta_corrente !="nome do cliente") and (self.conta_corrente !=None) and (self.status_atendimento == "Fechado") and (self.conta_corrente_status == "Não Pago") :
			if (frappe.db.sql("""select cc_nome_cliente from `tabCONTAS_CORRENTES` WHERE cc_nome_cliente =%s """,self.conta_corrente, as_dict=False)) != ():
				#existe faz os calculos da divida
				print " CLIENTE JA EXISTE"
				ccorrente = frappe.get_doc("CONTAS_CORRENTES", self.conta_corrente)
				print "CLIENTE"
				print ccorrente.name
#				ccorrente.cc_conta_corrente = self.conta_corrente
#				ccorrente.cc_status_conta_corrente = "Não Pago"

				totalextra = 0
				#for extras in frappe.db.sql(""" SELECT nome_servico,total_extra from `tabExtras_item` where parent = %s """,self.name,as_dict=True):

				cc_detalhes = frappe.new_doc("CC_detalhes")
				cc_detalhes.parent = ccorrente.name
				cc_detalhes.parentfield = "cc_bar_restaurante"
				cc_detalhes.parenttype = "CONTAS_CORRENTES"
					
				#	print extras.nome_servico
				#	print self.name
				cc_detalhes.descricao_servico = self.name #extras.nome_servico
				cc_detalhes.name = self.name
				cc_detalhes.numero_registo = self.name
				cc_detalhes.total = self.total_servicos #extras.total_extra
				cc_detalhes.data_registo = self.hora_atendimento
				cc_detalhes.tipo = "Bar"
				totalextra = totalextra + self.total_servicos #extras.total_extra

				cc_detalhes.status_conta_corrente = "Não Pago"
				cc_detalhes.idx += 1	
					
				cc_detalhes.insert()

				print (ccorrente.cc_valor_divida + totalextra)
				ccorrente.cc_valor_divida = flt(ccorrente.cc_valor_divida) + totalextra
				#ccorrente.save()

			else:
				#novo
				print " CLIENTE NAO EXISTE"
				print self.conta_corrente
				ccorrente = frappe.new_doc("CONTAS_CORRENTES")
				ccorrente.cc_nome_cliente = self.conta_corrente
				ccorrente.name = self.conta_corrente
				ccorrente.cc_status_conta_corrente = "Não Pago"
				ccorrente.insert()

				print "CONTAS CORRENTES FEITA !!!!!!"

				totalextra = 0
				#for extras in frappe.db.sql(""" SELECT nome_servico,total_extra from `tabExtras_item` where parent = %s """,self.name,as_dict=True):

				cc_detalhes = frappe.new_doc("CC_detalhes")
				cc_detalhes.parent =ccorrente.name
				cc_detalhes.parentfield = "cc_bar_restaurante"
				cc_detalhes.parenttype = "CONTAS_CORRENTES"

					#print extras.nome_servico
				cc_detalhes.descricao_servico = self.name #extras.nome_servico
				cc_detalhes.name = self.name
				cc_detalhes.numero_registo = self.name
				cc_detalhes.total = self.total_servicos #extras.total_extra
				cc_detalhes.data_registo = self.hora_atendimento
				cc_detalhes.tipo = "Bar"
				totalextra = totalextra + self.total_servicos #extras.total_extra

				cc_detalhes.status_conta_corrente = "Não Pago"
				cc_detalhes.insert()

				ccorrente.cc_valor_divida = flt(ccorrente.cc_valor_divida) + totalextra
				#ccorrente.save()

@frappe.whitelist()
def caixa_aberto():
	return frappe.get_list("Caixa de Registo",filters={'status_caixa':['in', 'Aberto, Em Curso']},fields=['name','status_caixa'])

@frappe.whitelist()
def caixa_curso():

	return frappe.get_list("Caixa de Registo",filters={'status_caixa':'Em Curso'},fields=['name','status_caixa'])


@frappe.whitelist()
def lista_clientes():

	#TO BE RE-DONE as using Customer ... need extra field Cliente_tipo
	return frappe.db.sql("""select name from `tabCLIENTES` WHERE cliente_tipo ='Membro' """, as_dict=False)

@frappe.whitelist()
def check_caixa_aberto():

	if (frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)) != ():
		return frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)
	elif (frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Em Curso' """, as_dict=False)) != ():
		return frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Em Curso' """, as_dict=False)



@frappe.whitelist()
def atualiza_ccorrente(cliente,recibo):

	print cliente
	print recibo
	for ccorrente1 in frappe.db.sql("""SELECT name,numero_registo,parent,status_conta_corrente from `tabCC_detalhes` where numero_registo = %s and parent = %s """, (recibo,cliente), as_dict=True):
		print ccorrente1.name
		print "CAMPOS !!!!!"

		reset_idx = frappe.get_doc("CC_detalhes",ccorrente1.name)
	#	print reset_idx.name
	#	print reset_idx.parent
	#	print reset_idx.status_conta_corrente

		reset_idx.status_conta_corrente = "Pago"
	#	ccorrente1.status_conta_corrente = "Pago"
	#	ccorrente1.save()

		reset_idx.save()


