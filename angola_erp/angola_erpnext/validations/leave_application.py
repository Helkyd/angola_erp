# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.model.naming import make_autoname
from frappe import _

def autoname(doc,method):

	doc.name = make_autoname(doc.naming_series)


def validate(doc,method):
	#Check if there is any attendance for an employee
	att = frappe.db.sql("""SELECT name, attendance_date FROM `tabAttendance` 
		WHERE docstatus = 1 AND employee = '%s' AND attendance_date >= '%s' AND
		attendance_date <= '%s'"""%(doc.employee, doc.from_date, doc.to_date), as_list=1)
	if att:
		frappe.throw(("Employee: {0} already has attendance between {1} and {2}").format(doc.employee_name, doc.from_date, doc.to_date))

	#Check if there already has Subsidio de Ferias on current Year...
	if doc.subsidio_de_ferias:
		print ('ANO ', frappe.utils.get_datetime(doc.from_date).year)
		subferias = frappe.db.sql("""SELECT name, employee, from_date, subsidio_de_ferias, docstatus FROM `tabLeave Application` 
			WHERE docstatus = 1 AND subsidio_de_ferias = 1 AND employee = '%s' AND year(from_date) = '%s' """%(doc.employee, frappe.utils.get_datetime(doc.from_date).year), as_list=1)
	
		if subferias:
			frappe.throw(("Funcionario: {0} - Ja recebeu o Subsidio de Ferias.").format(doc.employee_name))

