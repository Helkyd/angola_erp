# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe import msgprint
from frappe.utils import getdate
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

def validate(doc,method):
	#Validation for Age of Employee should be Greater than 18 years at the time of Joining.
	dob = getdate(doc.date_of_birth)
	doj = getdate(doc.date_of_joining)
	print relativedelta(doj, dob).years
	if relativedelta(doj, dob).years < 18:
		frappe.msgprint("Não é permitido criar trabalhadores menores de 18 anos de idade", raise_exception = 1)
	if doc.relieving_date:
		if doc.status <> "Left":
			frappe.msgprint(_("Status has to be 'LEFT' as the Relieving Date is populated"),raise_exception =1)
	
	doc.employee_number = doc.name
	doc.employee = doc.name


