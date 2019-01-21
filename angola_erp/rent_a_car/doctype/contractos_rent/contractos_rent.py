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


class ContractosRent(Document):

	def autoname(self):

		self.contracto_numero = make_autoname('RaC/' + '.YYYY./.#####')
		self.name = self.contracto_numero
		self.docstatus = 0



	def validate(self):
		#validar data de nascimento, carta de conducao
		if not self.data_nascimento_cliente:
			frappe.throw(_("Data de Nascimento é necessária!!!"))
			validated = False
		
		if not self.carta_conducao_cliente:
			frappe.throw(_("Numero da Carta de Condução é necessária!!!"))
			validated = False


	def on_submit(self):

		self.docstatus = 1

		
	def on_cancel(self):
		#set the car leased on Vehicle so no one can rent....
		print("submeter .... tem que CANCeLAR leased no Vehicle ...")
		frappe.db.set_value("Vehicle",self.matricula, "veiculo_alugado", 0)
		frappe.db.set_value("Vehicle",self.matricula, "entrada_ou_saida", "Entrada")
		frappe.db.commit()

		self.docstatus = 2	#cancela o submeter

	def before_submit(self):
		#set the car leased on Vehicle so no one can rent....
		print("submeter .... tem que set leased no Vehicle ...")
		#carro = frappe.get_doc("Vehicle",self.matricula)

		frappe.db.set_value("Vehicle",self.matricula, "veiculo_alugado", 1)
		frappe.db.set_value("Vehicle",self.matricula, "entrada_ou_saida", "Stand-by")
		frappe.db.commit()


