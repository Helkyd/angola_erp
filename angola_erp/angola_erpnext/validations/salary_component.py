# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint

def validate(doc, method):
	if doc.abono == 1:
		if doc.desconto == 1:
			frappe.throw("Componente Salarial so pode ser Abono ou Desconto")
	
	if doc.desconto == 1:
		if doc.abono == 1:
			frappe.throw("Componente Salarial so pode ser Abono ou Desconto")
			
			
	if doc.desconto == 0 and doc.abono == 0:
		frappe.throw("Componente Salarial tem que ser Abono ou Desconto")


