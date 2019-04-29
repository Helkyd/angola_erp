# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint

import angola_erp
from angola_erp.util.cambios import cambios
from angola_erp.util.angola import get_lista_retencoes
from angola_erp.util.angola import get_taxa_retencao
from angola_erp.util.angola import get_taxa_ipc
from angola_erp.util.angola import get_taxa_iva

import erpnext

from frappe.utils import money_in_words, flt
from frappe.utils import cstr, getdate, date_diff
## from erpnext.setup.utils import get_company_currency
from num2words import num2words

import os 
from datetime import datetime

from subprocess import Popen, PIPE

import angola_erp.util.saft_ao

####
# Helkyd modified 24-04-2019
####

ultimoreghash = None



def validate(doc,method):

	taxavenda= cambios("BNA")
	lista_retencoes = get_lista_retencoes()
	lista_retencao = get_taxa_retencao()
	lista_impostos = get_taxa_ipc()

	lista_iva = get_taxa_iva()

	temretencao = False 
	temimpostoconsumo = False 
	retencaofonte = 0
	retencaopercentagem = 0
	totalpararetencao = 0
	totalgeralimpostoconsumo = 0
	totalgeralretencaofonte = 0
	totalbaseretencaofonte = 0
	retencaofonteDESC = ""
	totalservicos_retencaofonte = 0
	totaldespesas_noretencaofonte = 0
	
	percentagem = 0

	
	
	ii=0

	for x in lista_retencoes:
		if x.descricao =='Retencao na Fonte':
			print ('pertagem ', x.percentagem)
			retencaopercentagem = x.percentagem
		elif (x.descricao =='IPC') or (x.descricao =='Imposto de Consumo'):
			print ('IPC % ', x.percentagem)
			percentagem = x.percentagem
		elif (x.descricao.upper() =='IVA'.upper()) or ("Imposto Valor Acrescentado".upper() == x.descricao.upper() or 'Acrescentado'.upper() in x.descricao.upper()):
			print ('IVA % ', x.percentagem)
			percentagem = x.percentagem


	for i in doc.get("items"):			
		print "ITEMS IMPOSTOS +++++++"
		prod = frappe.db.sql("""SELECT item_code,imposto_de_consumo,retencao_na_fonte FROM `tabItem` WHERE item_code = %s """, i.item_code , as_dict=True)
		if prod[0].imposto_de_consumo ==1:
			print ("IMPOSTO CONSUMO")
			#if i.imposto_de_consumo == 0:
			print i.amount

			if percentagem == 0:
				i.imposto_de_consumo = (i.amount * 5) / 100
			else:
				i.imposto_de_consumo = (i.amount * percentagem) / 100

		if prod[0].retencao_na_fonte ==1:
			print ("RETENCAO FONTE")
			i.retencao_na_fonte = (i.amount * retencaopercentagem) / 100
			totalbaseretencaofonte += i.amount
			totalservicos_retencaofonte += totalbaseretencaofonte
		else:
			totaldespesas_noretencaofonte += i.amount		

		totalgeralimpostoconsumo += i.imposto_de_consumo					
		totalgeralretencaofonte +=  i.retencao_na_fonte

	#Save retencao na INVoice 
	doc.total_retencao_na_fonte = totalgeralretencaofonte
	doc.base_retencao_fonte = totalbaseretencaofonte
	print "ANTES DESPESAS"
	print totalgeralimpostoconsumo
	#Calcula_despesas Ticked
	
	iii=0
	print ("Despesas")
	for ai in doc.get("taxes"):
		if ai.parent == doc.name and ai.charge_type !="":
			if ai.calcula_despesas:
				totalgeralimpostoconsumo = 0
				if totaldespesas_noretencaofonte ==0:
					#recalcula
					print ("RECALCULA")

					if (ai.rate == 0) and (percentagem == 0) :
						percentagem = 5
					else:
						percentagem = ai.rate
				
					for aii in doc.get("items"):
						if aii.parent == doc.name:
							print 'Dentro do ITem'
							prod = frappe.db.sql("""SELECT item_code,imposto_de_consumo,retencao_na_fonte FROM `tabItem` WHERE item_code = %s """, aii.item_code , as_dict=True)					

							#if (iii==0){iii=0}
							
							if prod[0].imposto_de_consumo == 1:
								print 'IMPOSTO TEM'
								if aii.imposto_de_consumo == 0:
									print "valor imp ", aii.imposto_de_consumo
								
								if aii.retencao_na_fonte == 1:
										
									totalgeralretencaofonte +=  (aii.amount * retencaopercentagem) / 100
									totalbaseretencaofonte += aii.amount
									totalservicos_retencaofonte += totalbaseretencaofonte

								totalgeralimpostoconsumo += aii.imposto_de_consumo					


								despesas = (percentagem * totaldespesas_noretencaofonte)/100
								print percentagem
								print totaldespesas_noretencaofonte
								print despesas
								print totalgeralimpostoconsumo
								print ai.account_head
								ai.charge_type = "Actual"
								ai.tax_amount = despesas #totalgeralimpostoconsumo 
							else:
								ai.tax_amount = 0

				else:
					print ("CALCULA DESPESAS")
					if (ai.rate == 0) and (percentagem == 0) :
						percentagem = 5
					else:
						percentagem = ai.rate

					despesas = (percentagem * totaldespesas_noretencaofonte)/100

					print percentagem
					print totaldespesas_noretencaofonte
					print despesas

					print totalgeralimpostoconsumo
					if despesas != totalgeralimpostoconsumo:

						ai.charge_type = "Actual"
						ai.tax_amount = totalgeralimpostoconsumo

					else:
						ai.charge_type = "Actual"
						ai.tax_amount = despesas
			elif "34220000" in ai.account_head: #IVA
				print "TEM IVA......"
				print "TEM IVA......"
				print "TEM IVA......"
				print "TEM IVA......"

			else:
				print "SEM DESPESAS MAS CALCULA IPC"
				print "SEM DESPESAS MAS CALCULA IPC"
				ai.charge_type = "Actual"
				ai.tax_amount = totalgeralimpostoconsumo





	#Check if Lead is Converted or Not, if the lead is converted 
	#then don't allow it to be selected without linked customer
	if doc.lead:
		link = frappe.db.sql("""SELECT name FROM `tabCustomer` 
			WHERE lead_name = '%s'"""%(doc.lead), as_list=1)
		if doc.customer is None and link:
			frappe.throw(("Lead {0} is Linked to Customer {1} so kindly make quotation for \
				Customer and not Lead").format(doc.lead, link[0][0]))
		elif doc.customer:
			if doc.customer != link[0][0]:
				frappe.throw(("Customer {0} is not linked to Lead {1} hence cannot be set\
				in the Quotation").format(doc.customer, doc.lead))


	print "VALOR POR EXTENSO"

	company_currency = erpnext.get_company_currency(doc.company)
	print company_currency
	if (company_currency =='KZ'):
		doc.in_words = num2words(doc.rounded_total, lang='pt_BR').title() + ' Kwanzas.'	
	else:
		doc.in_words = money_in_words(doc.rounded_total, company_currency)

	
	ultimodoc = frappe.db.sql(""" select max(name),creation,docstatus,hash_erp,hashcontrol_erp from `tabSales Invoice` where (docstatus = 1 or docstatus = 2)  and hash_erp <> '' """,as_dict=True)
	print 'VALIDARrrrrrrrrrrrrrrrrrr'
	print ultimodoc
	global ultimoreghash
	ultimoreghash = ultimodoc



def before_submit(doc,method):



	#HASH and HASH CONTROL...
	fileregisto = "registo"
	fileregistocontador = 1	#sera sempre aqui 

	#get the last doc generated 
	print 'verifica se ja tem o registo'
	print 'verifica se ja tem o registo' 
	print ultimoreghash

	if ultimoreghash:
		ultimodoc = ultimoreghash
	else:
		#ultimodoc = frappe.db.sql(""" select max(name),creation,modified,posting_date,hash_erp,hashcontrol_erp from `tabSales Invoice` """,as_dict=True)
		ultimodoc = frappe.db.sql(""" select name,creation,modified,transaction_date,hash_erp,hashcontrol_erp from `tabSales Invoice` where creation = (select max(creation) from `tabSales Invoice`) """,as_dict=True)
		


	criado = datetime.strptime(doc.creation,'%Y-%m-%d %H:%M:%S.%f').strftime("%Y-%m-%dT%H:%M:%S") 
	
	print 'ULTIMO HASH.....'
	print ultimodoc
#	print ultimodoc[0].hash_erp
	if ultimodoc[0].hash_erp == "" or ultimodoc[0].hash_erp == None:
		#1st record
		print 'primeiro registo HASH'
		#print doc.posting_date.strftime("%Y-%m-%d")

		print doc.creation	
		print criado
		hashinfo = str(doc.transaction_date) + ";" + str(criado) + ";" + str(doc.name) + ";" + str(doc.rounded_total) + ";"
	else:
		print 'segundo registo'
		#print chaveanterior
		hashinfo = str(doc.transaction_date)  + ";" + str(criado) + ";" + str(doc.name) + ";" + str(doc.rounded_total) + ";" + str(ultimodoc[0].hash_erp)


#	hashfile = open("/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt","wb")
#	hashfile.write(hashinfo)

	#to generate the HASH
#	angola_erp.util.saft_ao.assinar_ssl()
	print "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
#	os.system("/usr/bin/python /tmp/angolaerp.cert2/assinar_ssl.py")	
	print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	print angola_erp.util.saft_ao.assinar_ssl1(hashinfo)
	 

#	p = Popen(["/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh"],shell=True, stdout=PIPE, stderr=PIPE)
#	p = Popen(["exec ~/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh"],shell=True, stdout=PIPE, stderr=PIPE)
#	output, errors = p.communicate()
#	p.wait()
	print 'Openssl Signing...'
#	print output
#	print errors

#	hashfile.close()

	#Reads the file to save the HASH....
#	hashcriado = open('/tmp/registo1.b64','rb')	#open the file created to HASH
#	print 'Hash criado'
#	chaveanterior = str(hashcriado.read())	#para usar no next record...

	doc.hash_erp = str(angola_erp.util.saft_ao.assinar_ssl1(hashinfo))	#Hash created
	
#	hashcriado.close()
	
	#Deve no fim apagar todos os regis* criados ....
#	os.system("rm /tmp/registo* ")	#execute


