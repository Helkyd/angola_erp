# -*- coding: utf-8 -*-
# Copyright (c) 2015, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class CaixadeRegisto(Document):


	def autoname(self):
		self.name = make_autoname(self.abertura_fecho + '-' + '.#####')
		self.usuario_caixa= frappe.session.user

	def validate(self):
		print "VAAAAAALIIIIIIDAR"
		d=caixa_aberto()
		if (d !=None):
			print d[0]
			print self.name
			if (d[0][0] != self.name):
				validated=False
				frappe.throw(_("CAIXA JA ESTA ABERTO!!! NAO PODE TER MAIS QUE UM ABERTO"))
		if self.status_caixa =="Aberto":
			self.status_caixa ="Em Curso"


@frappe.whitelist()
def caixa_aberto():

	if (frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)) != ():
		print "AAAAAAAA"
		print frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)	
		return frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)
	elif (frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Em Curso' """, as_dict=False)) != ():
		return frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Em Curso' """, as_dict=False)
		print "BBBBBBBBB"
		print frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)	




