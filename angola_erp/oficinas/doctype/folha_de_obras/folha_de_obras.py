# -*- coding: utf-8 -*-
# Copyright (c) 2019, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from datetime import datetime, timedelta
from frappe.utils import cstr, get_datetime, getdate, cint, get_datetime_str


class FolhadeObras(Document):

	def autoname(self):

		#self.numero_obra = make_autoname('FO/' + '.#####' + './.' + 'YYYY')
		self.numero_obra = make_autoname('FO/' + '.YYYY./.#####')
		self.name = self.numero_obra


	def validate(self):
		self.criar_projecto()
				



	def criar_projecto(self):
		if self.fo_status == "Em Curso":
			print "Verifica o Project ...."
			criarprojeto = False
			if frappe.db.sql("""select name from `tabProject` WHERE name =%s """,(self.numero_obra), as_dict=False) ==():
				criarprojeto = True
			if criarprojeto == True: #not frappe.get_doc("Project",self.numero_obra): 
				print "Criar Projeto ...."
				projecto = frappe.get_doc({
					"doctype": "Project",
					"project_name": self.numero_obra,
					"priority": "Medium",
					"status": "Open",
					"expected_start_date": get_datetime(frappe.utils.now()) + timedelta(days=1) ,
					"expected_end_date": self.data_previsao_saida ,
					"is_active": "Yes",
					"project_type": "Internal",
					"customer": self.nome_cliente
				})
				projecto.insert()
				frappe.msgprint('{0}{1}'.format("Numero da Folha de Obra criado como Projeto ", self.numero_obra))
				#create the Tasks

	#			fo_avarias = frappe.get_doc("FO_Avarias_Cliente",self.numero_obra)
				for num_avarias in frappe.get_all("FO_Avarias_Cliente",filters={'Parent':self.numero_obra},fields=['Parent','avcliente_descricao']):
					if num_avarias.avcliente_descricao:
		#			for num_avarias in fo_avarias:
						tarefas = frappe.get_doc({
								"doctype": "Task",
								"project": self.numero_obra,
								"subject": num_avarias.avcliente_descricao,
								"status": "Open",
								"description": "Tarefa adicionada pelo Sistema",
								"exp_start_date": get_datetime(frappe.utils.now()) + timedelta(days=1),
								"exp_end_date": self.data_previsao_saida 

						})
						tarefas.insert()
						frappe.msgprint('{0}{1}'.format(num_avarias.avcliente_descricao, " Criado como tarefa no Projecto ", self.numero_obra))
				if self.obs_cliente:	
					#Add OBS_Cliente to Tasks
					tarefas = frappe.get_doc({
						"doctype": "Task",
						"project": self.numero_obra,
						"subject": self.obs_cliente,
						"status": "Open",
						"description": self.obs_cliente,
						"exp_start_date": get_datetime(frappe.utils.now()) + timedelta(days=1),
						"exp_end_date": self.data_previsao_saida 

					})
					tarefas.insert()
			#Set OR para Fechado
			ordemreparacao = frappe.get_doc("Ordem de Reparacao",self.ordem_reparacao)			
			ordemreparacao.or_status = "Fechada"
			ordemreparacao.save()
		elif self.fo_status == "Aberta":
			#Set OR para Em Curso
			ordemreparacao = frappe.get_doc("Ordem de Reparacao",self.ordem_reparacao)			
			ordemreparacao.or_status = "Em Curso"
			ordemreparacao.save()

				
	def _criar_projecto(self):
			i=0
			d=self.avarias_cliente
			print unicode(d).encode('utf-8')
			while i <> -1:
				posic = d.find(';\n', i,len(d)+1)
				if posic != -1:
					palavratmp = d[0:posic]
					dd = d[posic+1:len(d)] 
					d = dd #d[posic:len(d)]
					i = posic

				else:
					palavratmp= d
					i =-1
				print posic, unicode(dd).encode('utf-8')
				print i, unicode(d).encode('utf-8')
				if palavratmp !='':
					tarefas = frappe.get_doc({
						"doctype": "Task",
						"project": self.numero_obra,
						"subject": unicode(palavratmp), #.encode('utf-8'),
						"status": "Open",
						"description": "Tarefa adicionada pelo Sistema",
						"exp_start_date": get_datetime(frappe.utils.now()) + timedelta(days=1)

					})
					tarefas.insert()
					frappe.msgprint('{0}{1}'.format(unicode(palavratmp), " Criada como tarefa no Projecto ", self.numero_obra))
			

@frappe.whitelist()
def get_projecto_status(prj):
	print frappe.db.sql("""select name, status from `tabProject` WHERE status = 'Completed' and name =%s """,(prj), as_dict=False)
	return frappe.db.sql("""select status from `tabProject` WHERE name =%s """,(prj), as_dict=False)

@frappe.whitelist()
def get_avaria_cliente(cdt):
	print frappe.get_all("Avarias_Cliente",filters={'Parent':cdt},fields=['Parent','avcliente_descricao'])	
	return frappe.get_all("Avarias_Cliente",filters={'Parent':cdt},fields=['Parent','avcliente_descricao'])

@frappe.whitelist()
def get_avarias_clientes():
	print "GET_AVARIAS_CLIENTE"
	print frappe.get_all("Avarias_Cliente",filters={'Parent':['!=','']},fields=['Parent','avcliente_descricao'])
	return frappe.get_all("Avarias_Cliente",filters={'Parent':['!=','']},fields=['Parent','avcliente_descricao'])



