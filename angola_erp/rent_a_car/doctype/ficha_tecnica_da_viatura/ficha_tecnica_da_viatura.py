# -*- coding: utf-8 -*-
# Copyright (c) 2019, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe import throw
from frappe.utils import formatdate, encode
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from datetime import datetime, timedelta
from frappe.utils import cstr, get_datetime, getdate, cint, get_datetime_str

class FichaTecnicadaViatura(Document):

	def autoname(self):

		self.ficha_numero = make_autoname(self.naming_series)
		self.name = self.ficha_numero

		if self.entrada_ou_saida_viatura == "Entrada":
			print('autoname entrada')	
			self.docstatus = 0

		else:

			frappe.db.set_value("Vehicle",self.matricula_veiculo, "entrada_ou_saida", "Stand-by")
			frappe.db.commit()
			print('primeiro registo...')
			print('primeiro registo...')
			print('primeiro registo...')
			print('primeiro registo...')

			self.docstatus = 0



	def validate(self):
		#validar 
	
		if self.entrada_ou_saida_viatura == "Entrada":
			print('validar entrada')

			if self.kms_entrada < self.kms_saida:
				frappe.throw(_("Kilometros de Entrada errada!!!"))
				validated = False	

			self.docstatus = 0			
		else:
		
			#tem que verificar se o vehicle esta em Stand-by... caso nao alguem ja alugou...
			is_free = frappe.get_doc("Vehicle",self.matricula_veiculo)
			if not is_free.entrada_ou_saida == "Stand-by":
				frappe.throw(_("Esta viatura já está alugada, não é possivel continuar!!!"))
				validated = False	

	def on_submit(self):

		#self.docstatus = 1
		print('on submit')
		print('on submit')
		print('on submit')
		print('on submit')
		print('on submit')

		
	def on_cancel(self):
		self.docstatus = 2	#cancela o submeter

	def before_cancel(self):

		if self.entrada_ou_saida_viatura == "Entrada":
			frappe.db.set_value("Vehicle",self.matricula_veiculo, "entrada_ou_saida", "Saida")			
			frappe.db.commit()
			self.status_viatura = 'Alugada'

			#ainda falta repor o Contracto.....

		else:
			#set the car leased on Vehicle so no one can rent....
			frappe.db.set_value("Vehicle",self.matricula_veiculo, "entrada_ou_saida", "Stand-by")
			frappe.db.commit()
			self.status_viatura = 'Stand-by'



	def before_submit(self):

		if self.entrada_ou_saida_viatura == "Entrada":
			print('Entradadada')
			print('Entradadada')
			print('Entradadada')
			print('Entradadada')

			#set carro as Saida
			frappe.db.set_value("Vehicle",self.matricula_veiculo, "entrada_ou_saida", "Stand-by")
			frappe.db.set_value("Vehicle",self.matricula_veiculo, "veiculo_alugado", 0)
			frappe.db.commit()

			#set contracto as Terminado.
			frappe.db.set_value("Contractos Rent",self.contracto_numero, "status_contracto", "Terminou")
			frappe.db.commit()

			#procura a Ficha de SAIDA para por como 
			fichasaida = frappe.model.frappe.get_all('Ficha Tecnica da Viatura',filters={'contracto_numero':self.contracto_numero,'docstatus':1,'entrada_ou_saida_viatura': 'Saida'},fields=['name','contracto_numero'])			

			print(fichasaida[0].name)
			print(fichasaida)
	
			if fichasaida:
				frappe.db.set_value("Ficha Tecnica da Viatura",fichasaida[0].name, "status_viatura", "Devolvida")
				frappe.db.commit()

			#NAO SERVE AQUI...


			self.status_viatura = 'Devolvida'
			self.docstatus = 1
		else:
			#set carro as Saida
			print('before submit')
			print('saida')
			frappe.db.set_value("Vehicle",self.matricula_veiculo, "entrada_ou_saida", "Saida")
			frappe.db.commit()
			self.status_viatura = 'Alugada'


