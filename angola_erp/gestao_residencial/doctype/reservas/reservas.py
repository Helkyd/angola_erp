# -*- coding: utf-8 -*-
# Copyright (c) 2015, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe import utils 
import datetime 

from frappe.utils import flt, time_diff_in_hours, get_datetime, getdate, cint, get_datetime_str


class Reservas(Document):


	def autoname(self):
		self.codigo = make_autoname('RESERVA/' + '.#####')
		self.name = self.codigo


	def validate(self):
		if (self.reservation_status !="Cancelada"):
			self.Validar_Numero_Dias()

	def on_update(self):
		self.Quartos_Status()


	def Validar_Numero_Dias(self):
		if self.number_days <1:
			frappe.throw(_("Verificar Datas de Entrada e Saida. Numero de Dias tem que ser 1 ou mais."))

		# Retirar de momento vendo que nao tenho contornar este check

		#if (str(self.check_in) < frappe.utils.today()):
		#	frappe.throw(_("Verificar Data de Entrada. Inferior a Data de Hoje."))

	def Quartos_Status(self):
		if (self.reservation_status=="Nova"):
			# Change Quarto status 
			quarto = frappe.get_doc("Quartos", self.numero_quarto)			
			quarto.status_quarto = "Reservado"
			quarto.save()		

		elif (self.reservation_status=="Ativo"):
			
			quarto = frappe.get_doc("Quartos",self.numero_quarto)
			hdn = frappe.get_doc("Tipo de Quartos",self.quarto_tipo)
			# Criar o registo no Gestao_Quartos poe ATIVO
			frappe.get_doc({
				"doctype":"Gestao de Quartos",
				"name": make_autoname(self.numero_quarto + '-' + '.#####'),
				"numero_quarto": self.numero_quarto,			
				"tipo_quarto": self.quarto_tipo,
				"preco":self.preco_quarto,		
				"hora_entrada":self.check_in,
				"hora_saida":self.check_out,
				"horas": self.number_days,
				"total": int(self.number_days) * self.preco_quarto,
				"pagamento_por": "Cash",
				"status_quarto": "Ativo",
				"hora_diaria_noite": hdn.diaria_hora,
				"nome_cliente":self.numero_cliente,
				"reserva_numero":self.name
			}).insert()

			# Change Quarto status 
			quarto = frappe.get_doc("Quartos", self.numero_quarto)		
			quarto.status_quarto = "Ocupado"

			quarto.save()

		elif (self.reservation_status=="Cancelada"):


			# Change Quarto status 
			quarto = frappe.get_doc("Quartos", self.numero_quarto)		
			quarto.status_quarto = "Livre"

			quarto.save()


