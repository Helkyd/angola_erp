# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload (sys)
sys.setdefaultencoding('utf8')



import frappe
from frappe import _
from frappe.utils import cint, random_string
from frappe.utils import cstr, flt, getdate
from StringIO import StringIO
from frappeclient import FrappeClient
import csv 
import json


@frappe.whitelist()
def add_jentry(empresa):

	if empresa is None:
		print "Nome da Empresa necessario"
		return

	print "Ficheiro journalentry_dev.csv deve estar no /TMP"
	print "Ficheiro extraido do Primavera"
	print "Conta, ValorAlt, Descricao, Natureza, Datagravacao"
	print "Mudar o IP do Servidor"
	print "Mudar o Usuario e a Senha para Importar"

	client= FrappeClient("http://127.0.0.1:8000","administrator","123")

	with open ('/tmp/journalentry_dev.csv') as csvfile:
		readCSV = csv.reader(csvfile)
		print "Lendo o ficheiro..."

		for row in readCSV:
			print row
			print "======="
			print row[0]
			if "Conta" in row[0]:
				print 'Inicio'
			elif row[0] == "\xef\xbb\xbfConta":
				print 'ainda falta'
			else:
				print row[0]
				print row[1]
				print row[10]

				if (len(row[0]) >1): #(row[0].strip() != "0"):

					conta = row[0]
					valoralt = row[1]
					print 'conta', conta
					print 'valor ', valoralt

					try:
						existe =  frappe.get_list("Account",filters=[['name', 'like',conta + '%']],fields=['name','company'])
						print existe				
					except frappe.DoesNotExistError:
						print "Conta ", unicode(conta.strip()), " nao existe"
						print existe.name == conta


					for contas in existe:
						print contas['company']
						if contas['company'] == empresa:
							print "Lancamento no file"
							print contas['name']
							conta = contas['name']
					
					if (existe.name == nomecliente):
						doc = {
						  "company": empresa, 
						  "conversion_rate": 1.0, 
						  "currency": "KZ", 
						  "customer": nomecliente, 
						  "customer_name": nomecliente, 
						  "debit_to": "31121000-Clientes Nacionais - CF", 
						  "docstatus": 0, 
						  "doctype": "Sales Invoice", 
						  "due_date": frappe.utils.nowdate(), 
						  "is_opening": "Yes", 
						  "is_pos": 0, 
						  "is_recurring": 0, 
						  "is_return": 0, 
						  "items": [
						   {
							"cost_center": "Main - CF", 
							"item_code": "BFWDB", 
							"qty": 1.0,
							"rate": flt(valorcliente)
						   }
						  ],
						  "status": "Draft", 
						  "submit_on_creation": 0, 
						  "taxes": [
						  {
							"account_head": "34210000-Imposto De Producao E Consumo - CF", 
							"charge_type": "On Net Total", 
							"cost_center": "Main - CF", 
							"description": "IPC &nbsp;%10", 
							"included_in_print_rate": 0, 
							"rate": 10.0
						   }
						   ], 
						  "taxes_and_charges": "Imposto de Consumo"
						}

						print doc

						x = client.session.post("http://127.0.0.1:8000/api/resource/Sales Invoice",data={"data":json.dumps(doc)})

						print x

	client.logout()


@frappe.whitelist()
def add_faturas():

	print "Ficheiro clientes_dev.csv deve estar no /TMP"
	print "Formato do ficheiro Nomecliente,valor"
	print "Mudar o IP do Servidor"
	print "Mudar o Usuario e a Senha para Importar"
		

#	client= FrappeClient("http://192.168.229.139:8000","hcesar@gmail.com","demo123456789")
	client= FrappeClient("http://127.0.0.1:8000","hcesar@gmail.com","demo123456789")

	# loop no txt,csv and get Client, Valor
	# Lancamento de Devedores com IS OPENING=1 

	with open ('/tmp/clientes_dev.csv') as csvfile:
		readCSV = csv.reader(csvfile)
		print "Lendo o ficheiro..."

		for row in readCSV:

			if (len(row[0]) >1): #(row[0].strip() != "0"):

				nomecliente = row[0]
				valorcliente = row[1]
				print nomecliente
				print valorcliente

				try:
					existe =frappe.get_doc("Customer",nomecliente)
				except frappe.DoesNotExistError:
					print "Cliente ", unicode(nomecliente.strip()), " nao existe"
					print existe.name == nomecliente


				if (existe.name == nomecliente):
					doc = {
					  "company": "AngolaERP", 
					  "conversion_rate": 1.0, 
					  "currency": "KZ", 
					  "customer": nomecliente, 
					  "customer_name": nomecliente, 
					  "debit_to": "31121000-Clientes Nacionais - CF", 
					  "docstatus": 0, 
					  "doctype": "Sales Invoice", 
					  "due_date": frappe.utils.nowdate(), 
					  "is_opening": "Yes", 
					  "is_pos": 0, 
					  "is_recurring": 0, 
					  "is_return": 0, 
					  "items": [
					   {
						"cost_center": "Main - CF", 
						"item_code": "BFWDB", 
						"qty": 1.0,
						"rate": flt(valorcliente)
					   }
					  ],
					  "status": "Draft", 
					  "submit_on_creation": 0, 
					  "taxes": [
					  {
						"account_head": "34210000-Imposto De Producao E Consumo - CF", 
						"charge_type": "On Net Total", 
						"cost_center": "Main - CF", 
						"description": "IPC &nbsp;%10", 
						"included_in_print_rate": 0, 
						"rate": 10.0
					   }
					   ], 
					  "taxes_and_charges": "Imposto de Consumo"
					}

					print doc

					x = client.session.post("http://127.0.0.1:8000/api/resource/Sales Invoice",data={"data":json.dumps(doc)})

					print x

	client.logout()



@frappe.whitelist()
def add_faturas_():

	print "Ficheiro clientes_dev.csv deve estar no /TMP"
	print "Formato do ficheiro Nomecliente,valor"
	print "Mudar o IP do Servidor"
	print "Mudar o Usuario e a Senha para Importar"
		

#	client= FrappeClient("http://192.168.229.139:8000","hcesar@gmail.com","demo123456789")
	client= FrappeClient("http://127.0.0.1:8000","hcesar@gmail.com","demo123456789")

	# loop no txt,csv and get Client, Valor
	# Lancamento de Devedores com IS OPENING=1 

	with open ('/tmp/clientes_dev.csv') as csvfile:
		readCSV = csv.reader(csvfile)
		print "Lendo o ficheiro..."

		for row in readCSV:

			if (len(row[0]) >1): #(row[0].strip() != "0"):

				nomecliente = row[0]
				valorcliente = row[1]
				print nomecliente
				print valorcliente

				try:
					existe =frappe.get_doc("Customer",nomecliente)
				except frappe.DoesNotExistError:
					print "Cliente ", unicode(nomecliente.strip()), " nao existe"
					print existe.name == nomecliente
					print type(nomecliente)
					doc =dict( {"doctype":"Customer","disabled":0,"customer_name":nomecliente,"customer_type":"Company","territory":"Angola","customer_group":"Individual"})
#					doc = {
#						"doctype":"Customer",
#						"disabled":0,
#						"customer_name": str(nomecliente),
#						"customer_type": "Company",
#						"customer_group": "Individual",
#						"territory": "Angola"
#						}
					
					#res = self.session.post(self.url + "/api/resource/" + doc.get("doctype"),data={"data":json.dumps(doc))
					data={"data":json.dumps(doc)}

					#client.insert(doc)
					client.session.post("http://127.0.0.1:8000/api/resource/Customer",data={"data":json.dumps(doc)})

					print "Cliente ", nomecliente, " Adicionado"

				#if (existe.name == nomecliente):
				doc = {
				  "company": "AngolaERP", 
				  "conversion_rate": 1.0, 
				  "currency": "KZ", 
				  "customer": nomecliente, 
				  "customer_name": nomecliente, 
				  "debit_to": "31121000-Clientes Nacionais - CF", 
				  "docstatus": 0, 
				  "doctype": "Sales Invoice", 
				  "due_date": frappe.utils.nowdate(), 
				  "is_opening": "Yes", 
				  "is_pos": 0, 
				  "is_recurring": 0, 
				  "is_return": 0, 
				  "items": [
				   {
					"cost_center": "Main - CF", 
					"item_code": "BFWDB", 
					"qty": 1.0,
					"rate": flt(valorcliente)
				   }
				  ],
				  "status": "Draft", 
				  "submit_on_creation": 0, 
				  "taxes": [
				  {
					"account_head": "34210000-Imposto De Producao E Consumo - CF", 
					"charge_type": "On Net Total", 
					"cost_center": "Main - CF", 
					"description": "IPC &nbsp;%10", 
					"included_in_print_rate": 0, 
					"rate": 10.0
				   }
				   ], 
				  "taxes_and_charges": "Imposto de Consumo"
				}

				print doc

				x = client.session.post("http://127.0.0.1:8000/api/resource/Sales Invoice",data={"data":json.dumps(doc)})

				print x

	client.logout()
