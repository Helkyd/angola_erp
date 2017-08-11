# -*- coding: utf-8 -*-
# Copyright (c) 2017, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr, flt, getdate
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe import msgprint, throw

class CadastrodeProcesso(Document):

	def autoname(self):

		print(self.numero_de_processo)
		print(len(self.serie_tipo))
		print(make_autoname(self.serie_tipo))
		print(make_autoname(self.serie_tipo)[0:12])
		self.numero_de_processo = self.numero_de_processo + make_autoname(self.serie_tipo)[0:12] # 'FO/' + '.YYYY./.#####')
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
			if len(self.numero_de_processo) != 16:
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




@frappe.whitelist()
def get_projecto_status(prj):
	print frappe.db.sql("""select name, status from `tabProject` WHERE status = 'Completed' and name =%s """,(prj), as_dict=False)
	return frappe.db.sql("""select status from `tabProject` WHERE name =%s """,(prj), as_dict=False)

