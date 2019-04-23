# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe import msgprint
from frappe.utils import getdate
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

def after_insert(doc,method):
	#Adds BI to Customer only after a change being made
	print "After Insert"
	frappe.db.set_value("Customer", doc.name, "bi", doc.bi)
	frappe.db.set_value("Customer", doc.name, "email_id", doc.email)
	frappe.db.set_value("Customer", doc.name, "mobile_no", doc.mobile)

def validate(doc,method):
	#Seguros should not be null Numero seguro, data emissao if Seguradora...
	if doc.seguradora:	
		if not doc.plano:
			frappe.msgprint("Escolha o Plano da Seguradora.", raise_exception = 1)
		elif not doc.numero_do_seguro:
			frappe.msgprint("Digite o Numero do Seguro.", raise_exception = 1)
		elif not doc.data_de_emissao:			
			frappe.msgprint("Digite a Data de Emissao.", raise_exception = 1)
