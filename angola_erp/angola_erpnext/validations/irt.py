# -*- coding: utf-8 -*-
# Copyright (c) 2015, helio and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr, flt, getdate
from frappe.model.document import Document
import frappe.model
import frappe.utils

@frappe.whitelist()
def get_irt(start):
	ret = {}
	j= frappe.db.sql(""" SELECT valor_inicio, valor_fim, valor_percentual,parcela_fixa
	from `tabIRT` where valor_inicio <= %(start)s and valor_fim >=%(start)s """,{
	"start": start}, as_dict=True)

	print " PRIMEIRO"
	print j	
	# if J is ZERO than should get LAST RECORD.

	if not j:
		ret = frappe.db.sql("""SELECT valor_inicio, valor_fim, valor_percentual, parcela_fixa
		from `tabIRT` ORDER BY valor_inicio DESC LIMIT 1""");
		j = ret

		print " SEGUNDO"
	print  j
	return j


@frappe.whitelist()
def get_inss():

	return frappe.db.get_value("INSS",None,"seguranca_social")


@frappe.whitelist()
def set_ded(ded,d_val):

	jj= frappe.db.sql("UPDATE `tabSalary Detail` SET amount=%s where name =%s",(flt(d_val),ded))

	return jj



		
