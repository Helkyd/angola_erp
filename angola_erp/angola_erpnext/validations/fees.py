# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe import _

from frappe.utils import cstr, getdate, date_diff
from datetime import datetime, timedelta
from frappe.utils import get_datetime, cint, get_datetime_str
from frappe.utils import cint, flt, round_based_on_smallest_currency_fraction
from frappe.utils import encode


def validate(doc,method):
	doc.calculate_total()
	print "propinas"
	print doc.docstatus
	
	print doc.referente_ao_mes.encode('utf-8') 
	print "MES ", _(frappe.utils.datetime.datetime.now().strftime("%B"))

	if not doc.referente_ao_mes:
		#acrescenta o mes corrente ....
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'January': doc.referente_ao_mes = 'Janeiro'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'February':doc.referente_ao_mes = 'Fevereiro'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'March':doc.referente_ao_mes = 'Março'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'April':doc.referente_ao_mes = 'Abril'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'May':doc.referente_ao_mes = 'Maio'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'June':doc.referente_ao_mes = 'Junho'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'July':doc.referente_ao_mes = 'Julho'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'August':doc.referente_ao_mes = 'Agosto'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'September':doc.referente_ao_mes = 'Setembro'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'October':doc.referente_ao_mes = 'Outubro'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'November':doc.referente_ao_mes = 'Novembro'
		if frappe.utils.datetime.datetime.now().strftime("%B") == 'December':doc.referente_ao_mes = 'Dezembro'

		# doc.referente_ao_mes = doc.referente_ao_mes[int(frappe.utils.formatdate(frappe.utils.nowdate(),'M'))]

	if doc.docstatus == 1 and doc.outstanding_amount > 0:
		criar_faturavenda(doc)


def criar_faturavenda(doc):
	if doc.outstanding_amount > 0:
		print "Verifica Sales Invoice ...."
		print frappe.get_value("Global Defaults",None,"default_company")
		empresa = frappe.get_value("Global Defaults",None,"default_company")
		empresa_abbr = frappe.get_value("Company",empresa,"abbr")

		centrocusto = frappe.get_value("Company",empresa,"cost_center")

		contalucro =  frappe.get_value("Company",empresa,"default_income_account")
		contadespesas =   frappe.get_value("Company",empresa,"default_expense_account")

		armazemdefault = frappe.get_value('Stock Settings',None,'default_warehouse')

		accs = frappe.db.sql("""SELECT name from tabAccount where account_name like '31121000%%' and company = %s """,(empresa),as_dict=True)
		acc = accs[0]['name']

		if doc.due_date:
			datalimite = doc.due_date
		else:
			datalimite = frappe.utils.nowdate()

		criarprojeto = False
		if frappe.db.sql("""select name from `tabSales Invoice` WHERE propina =%s """,(doc.name), as_dict=False) ==():
			criarprojeto = True
		if criarprojeto == True: 
			print "Criar Sales Invoice ...."
			print doc.components[0].fees_category.encode('utf-8')
			print type(doc.components[0].amount)
			valor = flt(doc.components[0].amount)
			print type(valor) #doc.round_floats_in(valor)

			print doc.name
			print doc.student_name.encode('utf-8')
			print doc.referente_ao_mes
			print centrocusto
			print contalucro.encode('utf-8')
			print contadespesas
			print armazemdefault
			print acc
			print valor

			projecto = frappe.get_doc({
				"doctype": "Sales Invoice",
				"propina": doc.name,
				"customer": doc.student_name,	
				"posting_date": frappe.utils.nowdate(),
				"due_date": datalimite,
#				"payment_due_date": get_datetime(frappe.utils.now() + timedelta(days=3)) ,
				"debit_to": acc,
				"company": empresa,
				"status": "Draft",
				"base_grand_total": flt(valor),
				"update_stock":0,
				"items":[
						{

							'doctype': 'Sales Invoice Item',
							'qty': 1,
							'uom':'Unit',
							'item_code': doc.components[0].fees_category,
							'item_name': doc.components[0].fees_category,
							'description': doc.components[0].fees_category.strip() + ' (' + doc.referente_ao_mes + ')',
#							'rate': float(doc.components[0].amount),
#							'price_list_rate': 17000.00, #float(doc.components[0].amount),
#							'amount': 17000.00, #float(doc.components[0].amount),
							'cost_center':centrocusto,
							'income_account': contalucro,
							'expense_account': contadespesas,
							'warehouse': armazemdefault,
						}
					],


			})
			projecto.insert()

			#for now disable; maybe client likes the idea of emailing ...
#			projecto.docstatus = 1
#			projecto.save()
#			print (projecto.items[0].description)

#			x = frappe.get_all('Sales Invoice Item', filters={'parent':doc.name}, fields=['parent','description'])
#			x.item_description = "TTEadfsadfasdfasdfasdfas"
#			projecto.save()


#				frappe.msgprint('{0}{1}'.format("Processo criado como Projeto ", self.numero_de_processo))
			#create the Tasks


