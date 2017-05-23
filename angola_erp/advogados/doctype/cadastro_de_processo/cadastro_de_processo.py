# -*- coding: utf-8 -*-
# Copyright (c) 2017, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr, flt, getdate
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class CadastrodeProcesso(Document):

	def autoname(self):

		#self.numero_obra = make_autoname('FO/' + '.YYYY./.#####')
		self.name = make_autoname(self.numero_de_processo + '/' + '.YYYY./.#####')


	def validate(self):
#		print "tamanho ", len(self.servicos_processo)
		
#		if len(self.servicos_processo) == 0:
#			validation = False
#			frappe.msgprint("Inserir pelo menos um Servico", raise_exception = 1)
	
		#if self.docstatus == 2:
		#	self.status_process = "Cancelado"

		#elif self.servicos_processo[0].servico_ficha_processo == None:
		#	validation = False
		#	frappe.msgprint("Inserir pelo menos um Servico", raise_exception = 1)
		if self.docstatus == 1 and self.status_ou_fase == 'Inicial' or self.status_ou_fase == 'Em Curso'  :
#			print " criarProjeto ", self.status_process
			self.status_ou_fase = 'Em Curso'
#			self.criar_projecto()
#			self.criar_salesorder()		

#		if self.docstatus == 0 and self.status_process =='Em Curso':
#			print " criarProjeto "
#			self.criar_projecto()




@frappe.whitelist()
def get_projecto_status(prj):
	print frappe.db.sql("""select name, status from `tabProject` WHERE status = 'Completed' and name =%s """,(prj), as_dict=False)
	return frappe.db.sql("""select status from `tabProject` WHERE name =%s """,(prj), as_dict=False)

