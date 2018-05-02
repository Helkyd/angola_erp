# -*- coding: utf-8 -*-
# Copyright (c) 2017, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.utils import cstr, flt, getdate
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe import msgprint, throw
from datetime import datetime, timedelta
from frappe.utils import get_datetime, cint, get_datetime_str


class CadastrodeProcesso(Document):

	def autoname(self):

		print(self.numero_de_processo)
		print(len(self.serie_tipo))
		print(make_autoname(self.serie_tipo))
		print(make_autoname(self.serie_tipo)[0:13])
		self.numero_de_processo = self.numero_de_processo + make_autoname(self.serie_tipo)[0:13] # 'FO/' + '.YYYY./.#####')
		self.name = self.numero_de_processo	#make_autoname(self.numero_de_processo + '/' + '.YYYY./.#####')


	def validate(self):


		#Check numero processo is Number and 4 digits.
		if len(self.numero_de_processo) < 4:
			if len(self.numero_de_processo) == 1:
				self.numero_de_processo = '000' + self.numero_de_processo
			elif len(self.numero_de_processo) == 2:
				self.numero_de_processo ='00' + self.numero_de_processo
			elif len(self.numero_de_processo) == 3:
				self.numero_de_processo ='0' + self.numero_de_processo
	
		elif len(self.numero_de_processo) > 4:
			if len(self.numero_de_processo) != 17:
				msgprint('Numero de Processo tem que ter somente 4 digitos')
				self.numero_de_processo =None
				frappe.validated = False

		elif len(self.numero_de_processo) == '0000':
			msgprint('Numero de Processo nao pode ser 0000')
			self.numero_de_processo = None
			frappe.validated = False



#		print "tamanho ", len(self.servicos_processo)
		
#		if len(self.servicos_processo) == 0:
#			validation = False
#			frappe.msgprint("Inserir pelo menos um Servico", raise_exception = 1)
	
		#if self.docstatus == 2:
		#	self.status_process = "Cancelado"

		#elif self.servicos_processo[0].servico_ficha_processo == None:
		#	validation = False
		#	frappe.msgprint("Inserir pelo menos um Servico", raise_exception = 1)
		if self.docstatus == 1 and self.estado == 'Inicial' or self.estado == 'Em Curso'  :
#			print " criarProjeto ", self.status_process
			self.estado = 'Em Curso'
#			self.criar_projecto()
#			self.criar_salesorder()		

#		if self.docstatus == 0 and self.status_process =='Em Curso':
#			print " criarProjeto "
#			self.criar_projecto()

		if self.docstatus == 1 and self.estado == 'Em Curso'  :
			self.criar_projecto()


	def criar_projecto(self):
		if self.estado == "Em Curso":
			print "Verifica o Project ...."
			criarprojeto = False
			if frappe.db.sql("""select name from `tabProject` WHERE name =%s """,(self.numero_de_processo), as_dict=False) ==():
				criarprojeto = True
			if criarprojeto == True: #not frappe.get_doc("Project",self.numero_obra): 
				print "Criar Projeto ...."
				projecto = frappe.get_doc({
					"doctype": "Project",
					"project_name": self.numero_de_processo,
					"priority": "Medium",
					"status": "Open",
					"expected_start_date": get_datetime(frappe.utils.now()), # + timedelta(days=1) ,
#					"expected_end_date": self.data_previsao_saida ,
					"is_active": "Yes",
					"project_type": "External",
					"customer": self.nome_do_autor
				})
				projecto.insert()
				frappe.msgprint('{0}{1}'.format("Processo criado como Projeto ", self.numero_de_processo))
				#create the Tasks

				tarefas = frappe.get_doc({
					"doctype": "Task",
					"project": self.numero_de_processo,
					"subject": "Ficha de Abertura do Processo",
					"status": "Open",
					"description": "Tarefa adicionada pelo Sistema",
					"exp_start_date": get_datetime(frappe.utils.now()) # + timedelta(days=1),

				})
				tarefas.insert()
#		elif self.fo_status == "Aberta":
			#Set OR para Em Curso
#			ordemreparacao = frappe.get_doc("Ordem de Reparacao",self.ordem_reparacao)			
#			ordemreparacao.or_status = "Em Curso"
#			ordemreparacao.save()

@frappe.whitelist()
def get_projecto_status(prj):
	print frappe.db.sql("""select name, status from `tabProject` WHERE status = 'Completed' and name =%s """,(prj), as_dict=False)
	return frappe.db.sql("""select status from `tabProject` WHERE name =%s """,(prj), as_dict=False)

