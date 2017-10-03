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
import datetime



@frappe.whitelist()
def get_lista_retencoes():
	j= frappe.db.sql(""" SELECT name, descricao, percentagem from `tabRetencoes` """,as_dict=True)

	print " LISTA RETENCOES"
	print j	
	return j



@frappe.whitelist()
#TO BE REMOVED IF Client ERPNEXT v8
def set_faltas1(mes,ano,empresa):
	print " DADOS ATTENDANCE"
	print  mes, ' ', ano
	for tra in frappe.db.sql(""" SELECT name,status from tabEmployee where status = 'Active' and company = %s """,(empresa), as_dict=True):
		#print empresa, ' ', tra.name
		j= frappe.db.sql(""" SELECT count(status)
		from `tabAttendance` where employee = %s and status = 'Absent' and month(att_date) = %s and year(att_date) = %s and docstatus=1 """,(tra.name,mes,ano), as_dict=False)

		print " ATTENDANCE"
		print j[0][0]	
		#save on Employee record
		j1 = frappe.get_doc("Employee",tra.name)
		j1.numer_faltas = j[0][0]
		j1.save()
	return j

@frappe.whitelist()
def set_faltas(mes,ano,empresa):
	print " DADOS ATTENDANCE - SET FALTAS"
	print  mes, ' ', ano
	for tra in frappe.db.sql(""" SELECT name,status from tabEmployee where status = 'Active' and company = %s """,(empresa), as_dict=True):
		#print empresa, ' ', tra.name
		j= frappe.db.sql(""" SELECT count(status)
		from `tabAttendance` where employee = %s and status = 'Absent' and month(attendance_date) = %s and year(attendance_date) = %s and docstatus=1 """,(tra.name,mes,ano), as_dict=False)

		print " ATTENDANCE"
		print j[0][0]
		if j[0][0] > 0 :	
			#save on Employee record
			j1 = frappe.get_doc("Employee",tra.name)
			j1.numer_faltas = j[0][0]
			j1.save()
		else:		
			#save on Employee record
			j1 = frappe.get_doc("Employee",tra.name)
			j1.numer_faltas = 0
			j1.save()

		j2 = frappe.db.sql(""" SELECT count(status)
		from `tabLeave Application` where status = 'Approved' and month(from_date) = %s and employee = %s and subsidio_de_ferias=1 and docstatus=1 """,(mes,tra.name), as_dict=False)

		print " LEAVE APPLICATION"
		if j2[0][0] > 0:
			#save on Employee record
			j1 = frappe.get_doc("Employee",tra.name)
			j1.subsidio_de_ferias = 1
			j1.save()
		else:
			#save on Employee record
			j1 = frappe.get_doc("Employee",tra.name)
			j1.subsidio_de_ferias = 0
			j1.save()


	return j



@frappe.whitelist()
def set_salary_slip_pay_days(pag,emp,ano,mes):
	ret = {}
	j= frappe.db.sql(""" UPDATE `tabSalary Slip` SET payment_days = %s where employee = %s and fiscal_year = %s and month = %s """,(pag,emp,ano,mes), as_dict=False)

	print " Atualizar SALARY SLIP"
	print j
	return j


@frappe.whitelist()
def get_faltas(emp,mes,ano, empresa):
	print " DADOS ATTENDANCE"
	print emp, ' ', mes, ' ', ano
	j= frappe.db.sql(""" SELECT count(status)
	from `tabAttendance` where employee = %s and status = 'Absent' and month(attendance_date) = %s and year(attendance_date) = %s and company = %s and docstatus=1 """,(emp,mes,ano, empresa), as_dict=False)

	print " ATTENDANCE"
	print j[0][0]	
	#save on Employee record
	j1 = frappe.get_doc("Employee",emp)
	j1.numer_faltas = j[0][0]
	j1.save()
	return j


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
def get_lista_irt():
	j= frappe.db.sql(""" SELECT valor_inicio, valor_fim, valor_percentual,parcela_fixa
	from `tabIRT` """,as_dict=True)

	print " LISTA IRT"
	print j	
	return j


@frappe.whitelist()
def get_inss():

	return frappe.db.get_value("INSS",None,"seguranca_social")


@frappe.whitelist()
def set_ded(ded,d_val):

#	jj= frappe.db.sql("UPDATE `tabSalary Detail` SET default_amount=%s where name =%s",(flt(d_val),ded))
	jj= frappe.db.sql("UPDATE `tabSalary Detail` SET amount=%s, default_amount=%s where name =%s",(flt(d_val),flt(d_val),ded))

	return jj




@frappe.whitelist()
def seguranca_social(jv_entry):

	#Read values from the JV created and get 72221 account value to calculate 8% and deposit on 7252 (Deb) and 3461 (Cre)
	print "ALGUMA COISA ...."

