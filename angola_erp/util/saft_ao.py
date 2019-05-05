# -*- coding: utf-8 -*-
# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt

#Date Changed: 24/04/2019
#Version: 1.0.4

from __future__ import unicode_literals

import sys
reload (sys)
sys.setdefaultencoding('utf-8')

import frappe.async
from frappe.utils import cstr

from frappe.model.document import Document
import frappe.model
import frappe
from frappe.utils import nowdate, cstr, flt, cint, now, getdate
from frappe import throw, _
from frappe.utils import formatdate, encode
from frappe.model.naming import make_autoname
from frappe.model.mapper import get_mapped_doc

from frappe.email.doctype.email_group.email_group import add_subscribers

from frappe.contacts.doctype.address.address import get_company_address # for make_facturas_venda
from frappe.model.utils import get_fetch_values

import os 

import csv 
import json

import xml.etree.ElementTree as ET
from xml.dom import minidom 
from lxml import etree

from datetime import datetime, date, timedelta

import angola
import re

#HASH
import OpenSSL
from OpenSSL import crypto
import base64
from oauth2client._helpers import _to_bytes

import requests
from M2Crypto import BIO, RSA, EVP, X509

from frappe.utils.background_jobs import enqueue, get_jobs
   

@frappe.whitelist()
def gerar_hash_erp():

	os.system("~/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")

@frappe.whitelist()
def get_xml(args):
	from werkzeug.wrappers import Response
	response = Response()
	response.mimetype = 'text/xml'
	response.charset = 'utf-8'
	response.data = '<xml></xml>'

	print 'AAAAA'

	print response	

	return response

@frappe.whitelist()
def update_accs_codes():
	#Update account_number with the number of name

#Check is eating the last digit.

	accs = frappe.db.sql(""" select name,account_number from `tabAccount` """,as_dict=True)
	for acc in accs:
		if acc.name[0:1].isnumeric() == True:
			#starts with Numbers
			conta = acc.name[0:acc.name.find("-")]
			#print acc.name[0:acc.name.find("-")-1]
			#acc.account_number = conta
			frappe.db.set_value('Account',acc.name,'account_number',conta)
			frappe.db.commit()
@frappe.whitelist()
def set_saft_ao(** kwargs):
	#Prepara o file /tmp/saft_ao.txt

	
	if kwargs['company'] != None:

		print kwargs['company']
		print kwargs['processar']
		company = kwargs['company']
		processar = kwargs['processar']
		datainicio = kwargs['datainicio']
		datafim = kwargs['datafim']
		update_acc_codes = kwargs['update_acc_codes']
		download_file = kwargs['download_file']
		ficheiro_tipo = kwargs['ficheiro_tipo']
		usuario = kwargs['usuario']

		#company = json.dumps(company1)
		
		#ff = open('/tmp/saft_ao.txt','wb')
		#conteudo = company + "\n" + processar + "\n" + datainicio + "\n" + datafim + "\n" + str(update_acc_codes) + "\n"  + str(download_file) + "\n" + str(ficheiro_tipo.encode('utf-8'))
		#conteudo = dict( company = company, 
		#		datainicio = datainicio, 
		#		datafim = datafim, 
		#		update_acc_codes = update_acc_codes, 
		#		download_file = download_file, 
		#		ficheiro_tipo = ficheiro_tipo
		#	)
		#ff.write(str(conteudo))
		#ff.close()		
		#enqueue(gerar_saft_ao, queue='default', timeout=6000, event = 'saft_ao', args = company)
		#company,processar,datainicio,datafim,update_acc_codes,download_file,ficheiro_tipo

		enqueue('angola_erp.util.saft_ao.gerar_saft_ao', queue='default', timeout=6000, event = 'saft_ao',company = company, processar = processar, datainicio = datainicio, datafim = datafim, update_acc_codes = update_acc_codes, download_file = download_file, ficheiro_tipo = ficheiro_tipo, usuario = usuario)
	
@frappe.whitelist()
def correr_saft_ao():
	#company = None, processar = "Mensal", datainicio = None, datafim = None, update_acc_codes = 0, download_file = 0):
	'''
	if kwargs['company'] != None:
		print kwargs['company']
		print kwargs['processar']
		company1 = kwargs['company']
		processar = kwargs['processar']
		datainicio = kwargs['datainicio']
		datafim = kwargs['datafim']
		update_acc_codes = kwargs['update_acc_codes']
		download_file = kwargs['download_file']
		ficheiro_tipo = kwargs['ficheiro_tipo']
		company = company1
	'''
	#print frappe.utils.get_url(frappe.utils.cstr(frappe.local.site))
	#frappe.init(frappe.local.site)	
	#frappe.publish_realtime('msgprint', 'Iniciando processamento SAFT-AO...')
	#frappe.enqueue(gerar_saft_ao,'long',event = 'saft_ao',async = True, job_name = 'saft_ao',kwargs= [company,processar,datainicio,datafim,update_acc_codes,download_file,ficheiro_tipo])
	#frappe.enqueue(gerar_saft_ao(company,processar,datainicio,datafim,update_acc_codes,download_file,ficheiro_tipo),'long',event = 'saft_ao',async = True, job_name = 'saft_ao')

	#frappe.enqueue(gerar_saft_ao(), 'short', event='gerar_saft_ao',job_name="gerar_saft_ao",kwargs = kwargs)
	#frappe.publish_realtime('msgprint', 'Terminou de processar SAFT-AO...')
	print "XXXXXXXX"
	linha = 1
	with open('/tmp/saft_ao.txt','rb') as fn:
		for line in fn:
			if linha == 1: company = line
			elif linha == 2: processar = line
			elif linha == 3: datainicio = line
			elif linha == 4: datafim = line
			elif linha == 5: update_acc_codes = line
			elif linha == 6: download_file = line
			elif linha == 7: ficheiro_tipo = line

			linha += 1
	
	#if company:
	#	saft = gerar_saft_ao(company,processar,datainicio,datafim,update_acc_codes,download_file,ficheiro_tipo)

	#ff = open('/tmp/saft_ao.txt','rb').read()
	#ff1 = ff
	#print ff
	#print ff1
	#for f in ff1:
	#	print ff1[f]

	

@frappe.whitelist()
def gerar_saft_ao(company = None, processar = "Mensal", datainicio = None, datafim = None, update_acc_codes = 0, download_file = 0, ficheiro_tipo = "I", usuario = None):

	Versao = "0.1.10" 
	#frappe.publish_realtime('msgprint', 'Iniciando processamento SAFT-AO...', user=frappe.session.user)

	print "EMPRESA Kwars"
	print company
	'''
	if company['company']:
		print company['company']
		print company['processar']
		company1 = company['company']
		processar = company['processar']
		datainicio = company['datainicio']
		datafim = company['datafim']
		update_acc_codes = company['update_acc_codes']
		download_file = company['download_file']
		company = company1


		print company
		print processar
		print datainicio
		print datafim
		print update_acc_codes
		print int(update_acc_codes) == 1
		print download_file
		print int(download_file) == 1

	else:
	'''
	print company
	print processar
	print datainicio
	print datafim
	print update_acc_codes
	print int(update_acc_codes) == 1
	print download_file
	print int(download_file) == 1

	print ficheiro_tipo
	print ficheiro_tipo[0:1]



	#Tipo de File
	#### I - Contabilidade Integrada
	# All tables
	#### C - Contabilidade
	#Header, MasterTables, Account Plan, Customer, Supplier, Taxes, Accounting Ledger
	#### F- Facturacao
	# Header, MasterTables, Customer, Supplier, Produtcs, Taxes, SI, DN,Payments
	#### R - Recibos
	# Header, MasterTables, Customers, Taxes, Payments

	######	Ficheiro_tipo = I	#Default



	#return 
	######## Inside MasterFiles
		###GeneralLedgerAccounts
			###Accounts
		###Customer
		###Supplier
		###Product
		###TaxTable
	######## END MasterFiles	

	######## Inside GeneralLedgerEntries
		###Journal

	######## END GeneralLedgerEntries

	######## Inside SourceDocuments
		###SalesInvoice
		###MovementOfGoods
		###WorkingDocuments
		###Payments


	######## END SourceDocuments

	'''
	Documentos Gerais devem ter Header, Customer, TaxTable, Payments

	Documentos Accounting/Contabilidade: GeneralLedgerAccounts, Supppier, GeneralLedgerEntries
	
	Documentos Invoices: Supplier, Products, SalesInvoice, WorkingDocuments, Payments 																																																																																																																																
	'''

	'''
	Para gerar:	openssl genrsa -out ChavePrivada.pem 1024
	Para gerar:	openssl rsa -in ChavePrivada.pem -out ChavePublica.pem -outform PEM –pubout



	'''
	
	#read from source ...
	print company == None
	print processar
	print datainicio
	print datafim
	print update_acc_codes

	if company == None or company =="None":
		empresa = frappe.get_doc('Company', '2MS - Comercio e Representacoes, Lda')	#Should get as arg or based on default...
		#('Company','Farmacia Xixa') #
		#('Company', '2MS - Comercio e Representacoes, Lda')	#Should get as arg or based on default...
		#('Company','Fazenda-Aurora') #
	else:
		empresa = frappe.get_doc('Company', company)	#Should get as arg or based on default...
		#nome do file sera a (Empresa + "_" + SAFT_AO + "_" + NIF + data today)
		print empresa.tax_id
		if empresa.tax_id:
			nomeficheiro = re.sub(r",|-|\s+","",empresa.name.replace(" ","_")) + "_SAFT_AO_" + empresa.tax_id.replace(" ","").strip() + "_" + datetime.today().strftime("%Y%m%d%H%M%S")
		else:
			nomeficheiro = re.sub(r",|-|\s+","",empresa.name.replace(" ","_")) + "_SAFT_AO_999999999" + "_" + datetime.today().strftime("%Y%m%d%H%M%S")
		#re.sub(r",|-|\s+","",s)

		agtvalidationnumber = str(angola.get_agt_lic()[0])	#AGT Validation Number
		print 'nome file ', nomeficheiro
		print 'agt validar ', agtvalidationnumber



	emp_enderecos = angola.get_all_enderecos("Company",empresa.name)
	print 'ENdereco Empresa'
	print emp_enderecos

	#Updates Accounting number on TabAccount
	if int(update_acc_codes) == 1 :
		#updates 
		print "updating accounts..."
		update_accs_codes()


	'''
	DEFAULT processar = Mensal
	Processar pode ser Mensal, Semanal ou Diario
	'''

	print 'mes inicial ', angola.get_first_day(datetime.today())
	print 'mes fim ', angola.get_last_day(datetime.today())


	if datainicio == None:
		primeirodiames = angola.get_first_day(datetime.today())
		ultimodiames = angola.get_last_day(datetime.today())

		#primeirodiames = datetime.strptime('2019-01-01',"%Y-%m-%d")
		#ultimodiames = datetime.strptime('2019-04-30',"%Y-%m-%d")

		AnoFiscal = frappe.db.sql(""" select year, year_start_date, year_end_date, disabled from `tabFiscal Year` where year = %s """,(datetime.today().year)
,as_dict=True)

	else:
		print 'User type'
		print type(datainicio)
		print str(datetime.strptime(datainicio,"%Y-%m-%d").year)	
		print datafim
		#datainicio = datetime.strptime(datainicio,"%Y-%m-%d").year
		primeirodiames = angola.get_first_day(datetime.strptime(datainicio,"%Y-%m-%d")) #datetime.datetime.strptime(datainicio,("%Y-%m-%d"))
		ultimodiames = angola.get_last_day(datetime.strptime(datainicio,"%Y-%m-%d")) #datetime.datetime.strptime(datafim,("%Y-%m-%d"))

		print 'Processar ', processar
		#case Semanal changes datafim
		#case Diario changes datafim to datainicio
		if processar:
			if processar.upper() == 'SEMANA':
				primeirodiames, ultimodiames = angola.get_firstlast_week_day(datetime.strptime(datainicio,"%Y-%m-%d"))
				print angola.get_firstlast_week_day(datetime.strptime(datainicio,"%Y-%m-%d"))
				print primeirodiames.strftime("%Y-%m-%d")
				print ultimodiames.strftime("%Y-%m-%d")


			if processar.upper() == 'DIARIO':
	
				ultimodiames = primeirodiames = datetime.strptime(datainicio,"%Y-%m-%d")
				print primeirodiames.strftime("%Y-%m-%d")
				print ultimodiames.strftime("%Y-%m-%d")



		AnoFiscal = frappe.db.sql(""" select year, year_start_date, year_end_date, disabled from `tabFiscal Year` where year = %s """,(str(datetime.strptime(datainicio,"%Y-%m-%d").year)),as_dict=True)

	print 'AnoFiscal'
	print AnoFiscal 
	print datetime.today().year


	#### Create Header

	data = ET.Element('AuditFile')
	print 'creating Header'
	head = ET.SubElement(data,'Header')

	auditfileversion = ET.SubElement(head,'AuditFileVersion')
	auditfileversion.text = str(Versao)

	companyid = ET.SubElement(head,'CompanyID')	
	companyid.text = empresa.name

	taxregistrationnumber = ET.SubElement(head,'TaxRegistrationNumber')
	taxregistrationnumber.text = empresa.tax_id.replace(" ","").strip()

	taxaccountingbasis = ET.SubElement(head,'TaxAccountingBasis')
	if ficheiro_tipo == "I":
		taxaccountingbasis.text = ficheiro_tipo 	#"I"	#I contab. integrada c/Factur, C - Contab, F - Fact, Q - bens, services, Fact.
	else:
		taxaccountingbasis.text = ficheiro_tipo[0:1] 	#"I"	#I contab. integrada c/Factur, C - Contab, F - Fact, Q - bens, services, Fact.

	companyname = ET.SubElement(head,'CompanyName')
	companyname.text = str(empresa.name).strip()

	businessname = ET.SubElement(head,'BusinessName')
	businessname.text = str(empresa.name).strip()

	#START CompanyAddress
	companyaddress = ET.SubElement(head,'CompanyAddress')
	#buildingnumber = ET.SubElement(companyaddress,'BuildingNumber')
	if emp_enderecos:
		if emp_enderecos.address_line1:
			streetname = ET.SubElement(companyaddress,'StreetName')
			streetname.text = str(emp_enderecos.address_line1).strip()
		if emp_enderecos.address_line1:
			addressdetail = ET.SubElement(companyaddress,'AddressDetail')
			addressdetail.text = str(emp_enderecos.address_line1).strip()
		if emp_enderecos.city:
			city = ET.SubElement(companyaddress,'City')
			city.text = emp_enderecos.city
		if emp_enderecos.pincode:	
			print emp_enderecos.pincode
			return
			postalcode = ET.SubElement(companyaddress,'PostalCode')
			postalcode.text = emp_enderecos.pincode
		if emp_enderecos.city:
			province = ET.SubElement(companyaddress,'Province')
			province.text = emp_enderecos.city

	country = ET.SubElement(companyaddress,'Country')
	country.text = "AO"	#default

	#END CompanyAddress
	fiscalyear = ET.SubElement(head,'FiscalYear')
	fiscalyear.text = AnoFiscal[0].year

	print 'Ano Inicio'
	print AnoFiscal[0].year_start_date

	startdate = ET.SubElement(head,'StartDate')	#iniciomes
	startdate.text = primeirodiames.strftime("%Y-%m-%d") #AnoFiscal[0].year_start_date.strftime("%Y-%m-%d")

	enddate = ET.SubElement(head,'EndDate')		#fimmes
	enddate.text = ultimodiames.strftime("%Y-%m-%d") #AnoFiscal[0].year_end_date.strftime("%Y-%m-%d")

	currencycode = ET.SubElement(head,'CurrencyCode')
	currencycode.text = "AOA"	#default

	datecreated = ET.SubElement(head,'DateCreated')
	datecreated.text = frappe.utils.nowdate()	#XML created

	taxentity = ET.SubElement(head,'TaxEntity')
	if ficheiro_tipo[0:1] == "I":
		taxentity.text = "sede"	#default por ser INTEGRADO
	elif ficheiro_tipo[0:1] == "F":
		taxentity.text = empresa.tax_id.replace(" ","").strip()
	else:
		taxentity.text = "global"

	#Se for um documento de "fatura", preencha o número de identificação da empresa do xml gerado,（o TaxEntity），se não,  preencherá "global", se for um documento "contábil" ou "integrado", no TaxEntity preencherá a "sede", especificamente: Header -TaxEntity


	productcompanytaxid = ET.SubElement(head,'ProductCompanyTaxID')
	productcompanytaxid.text = "5417537802"	#TeorLogico

	
	softwarevalidationnumber = ET.SubElement(head,'SoftwareValidationNumber')
	softwarevalidationnumber.text = agtvalidationnumber	#AGT number

	productid = ET.SubElement(head,'ProductID')
	productid.text = "AngolaERP / TeorLogico"	#TeorLogico

	productversion = ET.SubElement(head,'ProductVersion')
	productversion.text = str(angola.get_versao_aoerp())


	headercomment = ET.SubElement(head,'HeaderComment')
	headercomment.text = "Ficheiro Financeiro."	
	if emp_enderecos:
		if emp_enderecos.phone:
			telephone = ET.SubElement(head,'Telephone')
			telephone.text = emp_enderecos.phone
		if emp_enderecos.fax:
			fax = ET.SubElement(head,'Fax')
			fax.text = emp_enderecos.fax
		if emp_enderecos.email_id:
			email = ET.SubElement(head,'Email')
			email.text = emp_enderecos.email_id
	if empresa.website:
		website = ET.SubElement(head,'Website')
		website.text = empresa.website


	# END OF HEADER



	####MASTER Files
	masterfiles = ET.SubElement(data,'MasterFiles')


	##### Create GeneralLedgerAccounts
	#GeneralLedgerAccounts
	#masterfiles = ET.Element('MasterFiles')

	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "C": 

		generalledgeraccounts = ET.SubElement(masterfiles,'GeneralLedgerAccounts')
		planocontas = frappe.db.sql(""" select * from `tabAccount` where docstatus = 0 and company = %s and mid(name,1,1) REGEXP '[0-9]' order by name, lft """,(empresa.name), as_dict=True)


		for planoconta in planocontas:
			account = ET.SubElement(generalledgeraccounts,'Account')
			accountid = ET.SubElement(account,'AccountID')
			#accountid.text = str(planoconta.name.strip())			#Due to 30 chars limit we have to add 
			accountid.text = str(planoconta.account_number.strip())	#Make sure update_acc_codes was run before...

			accountdescription = ET.SubElement(account,'AccountDescription')		
			#accountdescription.text = str(planoconta.account_name.strip())
			if planoconta.account_name.find('-'):
				accountdescription.text = str(planoconta.account_name[planoconta.account_name.find('-')+1:len(planoconta.account_name)]).strip()
			else:
				accountdescription.text = str(planoconta.account_name[planoconta.account_name.find(' ')+1:len(planoconta.account_name)]).strip()
			# str(planoconta.account_name[planoconta.account_name.find('-')+1:planoconta.account_name.rfind('-')])

			openingdeditbalance = ET.SubElement(account,'OpeningDebitBalance')
			openingcrebitbalance = ET.SubElement(account,'OpeningCreditBalance')
			closingdebitbalance = ET.SubElement(account,'ClosingDebitBalance')
			closingcreditbalance = ET.SubElement(account,'ClosingCreditBalance')

			aberturadebitoanoprev = 0 
			aberturacreditoanoprev = 0

			#GL Entry from previous year
			glentry = frappe.db.sql(""" select sum(debit), sum(credit), sum(debit-credit) from `tabGL Entry` where company = %s and fiscal_year = %s and account = %s """,(empresa.name,int(AnoFiscal[0].year)-1,planoconta.name), as_dict=True)


			if glentry:	#for Previous YEAR
				if flt(glentry[0]['sum(debit)']) != 0:
					aberturadebitoanoprev = glentry[0]['sum(debit)']
					openingdeditbalance.text = "{0:.2f}".format(flt(glentry[0]['sum(debit)'])) 
				else:
					openingdeditbalance.text = "0.00"

				print flt(glentry[0]['sum(credit)'])

				if flt(glentry[0]['sum(credit)']) != 0:
					aberturacreditoanoprev = glentry[0]['sum(credit)']
					openingcrebitbalance.text = "{0:.2f}".format(flt(glentry[0]['sum(credit)'])) 	
				else:
					#print "aaa"
					#return
					openingcrebitbalance.text = "0.00"

			glentry = frappe.db.sql(""" select sum(debit), sum(credit), sum(debit-credit) from `tabGL Entry` where company = %s and fiscal_year = %s and account = %s """,(empresa.name,int(AnoFiscal[0].year),planoconta.name), as_dict=True)

			if glentry:	#Current YEAR
				print flt(glentry[0]['sum(debit)'])
				print flt(aberturadebitoanoprev)

				print 'adasdfasfsafasfda'
				print flt(glentry[0]['sum(debit-credit)'])

				print 'close db'
				print flt(glentry[0]['sum(debit)']) + flt(aberturadebitoanoprev)
				print (flt(glentry[0]['sum(debit)']) + flt(aberturadebitoanoprev)) - flt(glentry[0]['sum(credit)']) 			


				print 'ZERO ', flt(glentry[0]['sum(debit)']) == 0

				fechodebitoano = 0
				fechocreditoano = 0

				if flt(glentry[0]['sum(debit)']) != 0:

					fechodebitoano = (flt(glentry[0]['sum(debit)']) + flt(aberturadebitoanoprev)) - flt(glentry[0]['sum(credit)'])
					closingdebitbalance.text = "{0:.2f}".format(abs(flt(fechodebitoano)))
				else:
					closingdebitbalance.text = "0.00"

				if flt(glentry[0]['sum(credit)']) != 0:
					#if fechodebitoano == 0:
					fechocreditoano = (flt(glentry[0]['sum(credit)']) + flt(aberturacreditoanoprev)) - flt(glentry[0]['sum(debit)'])
					closingcreditbalance.text = "{0:.2f}".format(abs(flt(fechocreditoano)))
				else:
						closingcreditbalance.text = "0.00"
	#			if "2630" in planoconta.name: break

			groupingcategory = ET.SubElement(account,'GroupingCategory')
			if planoconta.is_group:	#fica GR
				#len(1 digit)
				if len(planoconta.account_number) == 1:
					groupingcategory.text = "GR"	#Ainda por verificar com os Contabilistas
				else:
					groupingcategory.text = "GA"	#Ainda por verificar com os Contabilistas
			elif not planoconta.is_group:
				#len(2,3,4... digits)
				groupingcategory.text = "GM"	#Ainda por verificar com os Contabilistas


			if planoconta.parent_account:
				groupingcode = ET.SubElement(account,'GroupingCode')
				groupingcode.text = str(planoconta.parent_account[0:planoconta.parent_account.find('-')-1]).strip()
				# str(planoconta.parent_account)
		
		##### END 2.1 Accounts

	#Customers
	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "C" or ficheiro_tipo[0:1].upper() == "F" or ficheiro_tipo[0:1].upper() == "R" or ficheiro_tipo[0:1].upper() == "S" or ficheiro_tipo[0:1].upper() == "Q": 

		customers = ET.SubElement(masterfiles,'Customers')

		#masterfiles = ET.Element('MasterFiles')

		#create Customer
		clientes = frappe.db.sql(""" select * from `tabCustomer` where docstatus = 0 """,as_dict=True)

		adicionacliente = True

		#Faz loop
		for cliente in clientes:
			contascliente = frappe.db.sql(""" select * from `tabParty Account` where parenttype = 'Customer' and parentfield = 'accounts' and parent = %s and company = %s """,(cliente.name, empresa.name), as_dict=True)
			print 'account cliente'
			print cliente.name
			print contascliente

			if not contascliente:
				#test to see if exists ... but on diff company

				contascliente = frappe.db.sql(""" select * from `tabParty Account` where parenttype = 'Customer' and parentfield = 'accounts' and parent = %s """,(cliente.name), as_dict=True)
				print 'outra empresa'
				print contascliente
				if contascliente:
					#Outra empresa..
					adicionacliente = False
				else:
					adicionacliente = True
		
		
			if adicionacliente == True:
				print 'Add cliente'
				print 'Add cliente'
				print 'Add cliente'
				#Customers
				#customers = ET.SubElement(masterfiles,'Customers')
				customer = ET.SubElement(customers,'Customer')
				customerid = ET.SubElement(customer,'CustomerID')
				customerid.text = cliente.name

				accountid = ET.SubElement(customer,'AccountID')



				if not contascliente:
						contascliente = frappe.db.sql(""" select * from `tabAccount` where name like '31121000%%' and company = %s """,(empresa.name), as_dict=True)
						print contascliente
						#accountid.text = contascliente[0].account_name.strip()
						accountid.text = str(contascliente[0].account_name[0:contascliente[0].account_name.find('-')]).strip()
						#accountid.text = contascliente[0].account_number
	#				else:
	#					accountid.text = "Desconhecido"				
				else:

					#accountid.text = contascliente[0].account
					accountid.text = str(contascliente[0].account[0:contascliente[0].account.find('-')]).strip()
					#In case we need to get account_number instead
					#contascliente = frappe.db.sql(""" select * from `tabAccount` where name = %s and company = %s """,(contascliente[0].account,empresa.name), as_dict=True)
					#accountid.text = contascliente[0].account_number


				customertaxid = ET.SubElement(customer,'CustomerTaxID')
				if (cliente.tax_id != None and cliente.tax_id.upper() != "N/A" and cliente.tax_id.upper() != "N-A" and cliente.tax_id.upper() != "ND") :
					customertaxid.text = cliente.tax_id
				else:
					customertaxid.text = "999999990"

				companyname = ET.SubElement(customer,'CompanyName')
				if cliente.customer_name == 'Diversos' or cliente.customer_name == 'General':
					companyname.text = "Consumidor final"
				else:	
					companyname.text = cliente.customer_name


				if cliente.customer_primary_contact:
					contact = ET.SubElement(customer,'Contact')
					contact.text = cliente.customer_primary_contact

				#START BILLING address
				#address = ET.SubElement(customer,'Address')

				billingaddress = ET.SubElement(customer,'BillingAddress')
				cliente_endereco = angola.get_all_enderecos_a("Customer",cliente.name)
				print cliente_endereco
				#if cliente_endereco:
				#	print cliente_endereco.address_line1
				#	billingaddress.text = cliente_endereco.address_line1

				#buildingnumber = ET.SubElement(billingaddress,'BuildingNumber')
				if cliente_endereco:
					print "AQUIIIIII"
				#	buildingnumber.text = cliente_endereco.address_line1
					if cliente_endereco.address_line1:
						streetname = ET.SubElement(billingaddress,'StreetName')
						streetname.text = cliente_endereco.address_line1


					if cliente.customer_name == 'Diversos' or cliente.customer_name == 'General':
						addressdetail = ET.SubElement(billingaddress,'AddressDetail')
						addressdetail.text = "Consumidor final"
					elif cliente_endereco.address_line1:				
						addressdetail = ET.SubElement(billingaddress,'AddressDetail')
						addressdetail.text = cliente_endereco.address_line1
					else:
						addressdetail = ET.SubElement(billingaddress,'AddressDetail')
						addressdetail.text = "Desconhecido"	#default



					if cliente.customer_name == 'Diversos' or cliente.customer_name == 'General':
						city = ET.SubElement(billingaddress,'City')
						city.text = "Desconhecido"	#default
					elif cliente_endereco.city:				
						city = ET.SubElement(billingaddress,'City')
						city.text = cliente_endereco.city

					else:
						city = ET.SubElement(billingaddress,'City')
						city.text = "Desconhecido"	#default


					#if cliente_endereco:
					#	city.text = cliente_endereco.city


					if cliente.customer_name == 'Diversos' or cliente.customer_name == 'General':
						postalcode = ET.SubElement(billingaddress,'PostalCode')
						postalcode.text = "Desconhecido"	#default
					elif cliente_endereco.pincode:				
						postalcode = ET.SubElement(billingaddress,'PostalCode')
						postalcode.text = cliente_endereco.pincode

					else:
						postalcode = ET.SubElement(billingaddress,'PostalCode')
						postalcode.text = "Desconhecido"	#default



					if cliente_endereco.city:
						province = ET.SubElement(billingaddress,'Province')
						province.text = cliente_endereco.city



					if cliente.customer_name == 'Diversos' or cliente.customer_name == 'General':
						country = ET.SubElement(billingaddress,'Country')
						country.text = "Desconhecido"	#default
					elif cliente_endereco:				
						country = ET.SubElement(billingaddress,'Country')
						if cliente_endereco.country == 'Angola':
							country.text = "AO"
						else:
							country.text = cliente_endereco.country


					else:
						country = ET.SubElement(billingaddress,'Country')
						country.text = "Desconhecido"	#default
				else:
					addressdetail = ET.SubElement(billingaddress,'AddressDetail')
					addressdetail.text = "Desconhecido"	#default

					city = ET.SubElement(billingaddress,'City')
					city.text = "Desconhecido"	#default
					#postalcode = ET.SubElement(billingaddress,'PostalCode')
					#postalcode.text = cliente_endereco.pincode

					country = ET.SubElement(billingaddress,'Country')
					country.text = "Desconhecido"	#default

				#END BILLING address

				#START SHIPTO address
				if cliente_endereco:
					if cliente_endereco.address_line1:
						shiptoaddress = ET.SubElement(customer,'ShipToAddress')

						#buildingnumber = ET.SubElement(shiptoaddress,'BuildingNumber')

						streetname = ET.SubElement(shiptoaddress,'StreetName')
						streetname.text = cliente_endereco.address_line1

						addressdetail = ET.SubElement(shiptoaddress,'AddressDetail')
						if cliente.customer_name == 'Diversos' or cliente.customer_name == 'General':
							addressdetail.text = "Consumidor final"
						elif cliente_endereco:				
							addressdetail.text = cliente_endereco.address_line1

					else:
						shiptoaddress = ET.SubElement(customer,'ShipToAddress')
						addressdetail = ET.SubElement(shiptoaddress,'AddressDetail')
						addressdetail.text = "Desconhecido"	#default

					city = ET.SubElement(shiptoaddress,'City')
					if cliente.customer_name == 'Diversos' or cliente.customer_name == 'General':
						city.text = "Desconhecido"	#default
					elif cliente_endereco.city:				
						city.text = cliente_endereco.city

					else:
						city.text = "Desconhecido"	#default

					if cliente.customer_name == 'Diversos' or cliente.customer_name == 'General':
						postalcode = ET.SubElement(shiptoaddress,'PostalCode')
						postalcode.text = "Desconhecido"	#default
					elif cliente_endereco.pincode:				
						postalcode.text = cliente_endereco.pincode

					else:
						postalcode.text = "Desconhecido"	#default

					province = ET.SubElement(shiptoaddress,'Province')
					if cliente_endereco.city:
						province.text = cliente_endereco.city

					country = ET.SubElement(shiptoaddress,'Country')
					if cliente.customer_name == 'Diversos' or cliente.customer_name == 'General':
						country.text = "Desconhecido"	#default
					#elif cliente_endereco:				
					if cliente_endereco.country == 'Angola':
						country.text = "AO"
						#else:
						#	country.text = cliente_endereco.country


					else:
						country.text = "Desconhecido"	#default



				#END SHIPTO address


					if cliente_endereco.phone:
						telephone = ET.SubElement(customer,'Telephone')
						telephone.text = cliente_endereco.phone


					if cliente_endereco.fax:
						fax = ET.SubElement(customer,'Fax')
						fax.text = cliente_endereco.fax


					if cliente_endereco.email_id:
						email = ET.SubElement(customer,'Email')
						email.text = cliente_endereco.email_id
				if cliente.website:
					website = ET.SubElement(customer,'Website')
					website.text = cliente.website


				selfbillingindicator = ET.SubElement(customer,'SelfBillingIndicator')
				selfbillingindicator.text = "0"	#default

			#END OF Customers

	#create Suppliers

	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "C" or ficheiro_tipo[0:1].upper() == "F" or ficheiro_tipo[0:1].upper() == "A" or ficheiro_tipo[0:1].upper() == "Q":

		#Suppliers
		suppliers = ET.SubElement(masterfiles,'Suppliers')
		fornecedores = frappe.db.sql(""" select * from `tabSupplier` where docstatus = 0 """,as_dict=True)

		adicionafornecedor = True

		for fornecedor in fornecedores:
			contasfornecedor = frappe.db.sql(""" select * from `tabParty Account` where parenttype = 'Supplier' and parentfield = 'accounts' and parent = %s and company = %s """,(fornecedor.name, empresa.name), as_dict=True)
			print 'account fornecedor'
			print fornecedor.name
			print contasfornecedor

			if not contasfornecedor:
				#test to see if exists ... but on diff company

				contasfornecedor = frappe.db.sql(""" select * from `tabParty Account` where parenttype = 'Supplier' and parentfield = 'accounts' and parent = %s """,(fornecedor.name), as_dict=True)
				print 'outra empresa'
				print contasfornecedor
				if contasfornecedor:
					#Outra empresa..
					adicionafornecedor = False
				else:
					adicionafornecedor = True
		
		
			if adicionafornecedor == True:
				print 'Add Fornecedor'
				print 'Add Fornecedor'
				print 'Add Fornecedor'



				supplier = ET.SubElement(suppliers,'Supplier')
				supplierid = ET.SubElement(supplier,'SupplierID')
				supplierid.text = fornecedor.name

		
				accountid = ET.SubElement(supplier,'AccountID')

				if not contasfornecedor:
						contasfornecedor = frappe.db.sql(""" select * from `tabAccount` where name like '31121000%%' and company = %s """,(empresa.name), as_dict=True)
						print contasfornecedor
						#accountid.text = contasfornecedor[0].account_name.strip()
						accountid.text = str(contasfornecedor[0].account_name[0:contasfornecedor[0].account_name.find('-')]).strip()
						#accountid.text = contasfornecedor[0].account_number
	#				else:
	#					accountid.text = "Desconhecido"				
				else:

					#accountid.text = contasfornecedor[0].account
					accountid.text = str(contasfornecedor[0].account[0:contasfornecedor[0].account.find('-')]).strip()
					#In case we need to get account_number instead
					#contasfornecedor = frappe.db.sql(""" select * from `tabAccount` where name = %s and company = %s """,(contascliente[0].account,empresa.name), as_dict=True)
					#accountid.text = contasfornecedor[0].account_number



				suppliertaxid = ET.SubElement(supplier,'SupplierTaxID')
				suppliertaxid.text = fornecedor.tax_id
				if (fornecedor.tax_id != None and fornecedor.tax_id.upper() != "N/A" and fornecedor.tax_id.upper() != "N-A") :	
					suppliertaxid.text = fornecedor.tax_id
				else:
					suppliertaxid.text = "999999990"


				companyname = ET.SubElement(supplier,'CompanyName')
				companyname.text = fornecedor.supplier_name

				#contact = ET.SubElement(supplier,'Contact')
				#contact.text = fornecedor.contact

				#START BILLING address
				#address = ET.SubElement(supplier,'Address')

				fornecedor_endereco = angola.get_all_enderecos_a("Supplier",fornecedor.name)
				if fornecedor_endereco:
				#	print fornecedor_endereco.address_line1
				#	billingaddress.text = fornecedor_endereco.address_line1

					if fornecedor_endereco.address_line1:
						billingaddress = ET.SubElement(supplier,'BillingAddress')

						#buildingnumber = ET.SubElement(billingaddress,'BuildingNumber')

						streetname = ET.SubElement(billingaddress,'StreetName')

						streetname.text = fornecedor_endereco.address_line1


						addressdetail = ET.SubElement(billingaddress,'AddressDetail')
						addressdetail.text = fornecedor_endereco.address_line1


					if fornecedor_endereco.city:
						city = ET.SubElement(billingaddress,'City')
						city.text = fornecedor_endereco.city



					if fornecedor_endereco.pincode:
						postalcode = ET.SubElement(billingaddress,'PostalCode')
						postalcode.text = fornecedor_endereco.pincode


					if fornecedor_endereco.city:
						province = ET.SubElement(billingaddress,'Province')
						province.text = fornecedor_endereco.city


					if fornecedor_endereco.country:
						country = ET.SubElement(billingaddress,'Country')
						if fornecedor_endereco.country == 'Angola':
							country.text = "AO"
						else:
							country.text = fornecedor_endereco.country


				#END BILLING ADDRESS

				#START SHIPTO address
				if fornecedor_endereco:
					shipfromaddress = ET.SubElement(supplier,'ShipFromAddress')
					#buildingnumber = ET.SubElement(shipfromaddress,'BuildingNumber')

					if fornecedor_endereco.address_line1:
						streetname = ET.SubElement(shipfromaddress,'StreetName')
						streetname.text = fornecedor_endereco.address_line1

						addressdetail = ET.SubElement(shipfromaddress,'AddressDetail')
						addressdetail.text = fornecedor_endereco.address_line1

					if fornecedor_endereco.city:
						city = ET.SubElement(shipfromaddress,'City')
						city.text = fornecedor_endereco.city


					if fornecedor_endereco.pincode:
						postalcode = ET.SubElement(shipfromaddress,'PostalCode')
						postalcode.text = fornecedor_endereco.pincode


					if fornecedor_endereco.city:
						province = ET.SubElement(shipfromaddress,'Province')
						province.text = fornecedor_endereco.city


					if fornecedor_endereco.country:
						country = ET.SubElement(shipfromaddress,'Country')
						if fornecedor_endereco.country == 'Angola':
							country.text = "AO"
						else:
							country.text = fornecedor_endereco.country


				#END SHIPTO ADDRESS


					if fornecedor_endereco.phone:
						telephone = ET.SubElement(supplier,'Telephone')
						telephone.text = fornecedor_endereco.phone


					if fornecedor_endereco.fax:
						fax = ET.SubElement(supplier,'Fax')
						fax.text = fornecedor_endereco.fax


					if fornecedor_endereco.email_id:
						email = ET.SubElement(supplier,'Email')
						email.text = fornecedor_endereco.email_id
				if fornecedor.website:
					website = ET.SubElement(supplier,'Website')
					website.text = fornecedor.website

				selfbillingindicator = ET.SubElement(supplier,'SelfBillingIndicator')
				selfbillingindicator.text = "0" #default

	#END OF Suppliers



	#create Products / Services
	#Products

	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "F" or ficheiro_tipo[0:1].upper() == "S" or ficheiro_tipo[0:1].upper() == "Q":

		products = ET.SubElement(masterfiles,'Products')

		produtos = frappe.db.sql(""" select * from `tabItem` where docstatus = 0 """,as_dict=True)

		for produto in produtos:
	
			product = ET.SubElement(products,'Product')
			producttype = ET.SubElement(product,'ProductType')
			if produto.is_stock_item:
				producttype.text = "P" #Produto
			else:
				producttype.text = "S" #Servico

		
			productcode = ET.SubElement(product,'ProductCode')
			productcode.text = produto.item_code

			if produto.item_group:
				productgroup = ET.SubElement(product,'ProductGroup')
				productgroup.text = produto.item_group

			productdescription = ET.SubElement(product,'ProductDescription')
			productdescription.text = produto.item_name.strip()

			if produto.barcode:
				productnumbercode = ET.SubElement(product,'ProductNumberCode')
				productnumbercode.text = produto.barcode
			else:
				productnumbercode = ET.SubElement(product,'ProductNumberCode')
				productnumbercode.text = produto.item_code

			#if produto.barcode:
			#customsdetails = ET.SubElement(product,'CustomsDetails')
			#unnumber = ET.SubElement(product,'UNNumber')

		#END OF Products

	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "C" or ficheiro_tipo[0:1].upper() == "F" or ficheiro_tipo[0:1].upper() == "R" or ficheiro_tipo[0:1].upper() == "S" or ficheiro_tipo[0:1].upper() == "Q" or ficheiro_tipo[0:1].upper() == "A":
		#create Retencoes...
		#TaxTable

	
		taxtable = ET.SubElement(masterfiles,'TaxTable')
		retencoes = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 """,as_dict=True)

		for retencao in retencoes:

			taxtableentry = ET.SubElement(taxtable,'TaxTableEntry')
			taxtype = ET.SubElement(taxtableentry,'TaxType')
			if "IPC" in retencao.name.upper():
				taxtype.text = "NS"
			elif "SELO" in retencao.name.upper():
				taxtype.text = "IS"
			elif "IVA" in retencao.name.upper():
				taxtype.text = "IVA"
			else:
				taxtype.text = "NS"

			taxcountryregion = ET.SubElement(taxtableentry,'TaxCountryRegion')
			taxcountryregion.text = "AO"


			taxcode = ET.SubElement(taxtableentry,'TaxCode')
			if "IPC" in retencao.name.upper():
				taxcode.text = "NS"
			elif "SELO" in retencao.name.upper():
				taxcode.text = "ISE"
			elif "IVA" in retencao.name.upper():
				taxcode.text = "ISE"
			else:
				taxcode.text = "NS"

			if retencao.descricao:
				description = ET.SubElement(taxtableentry,'Description')
				description.text = retencao.descricao.strip()


			if retencao.data_limite:
				taxexpirationdate = ET.SubElement(taxtableentry,'TaxExpirationDate')
				taxexpirationdate.text = str(retencao.data_limite.strftime("%Y-%m-%d"))

			taxpercentage = ET.SubElement(taxtableentry,'TaxPercentage')
			taxamount = ET.SubElement(taxtableentry,'TaxAmount')
			if retencao.percentagem:
				taxpercentage.text = str("{0:.0f}".format(retencao.percentagem)) #str(retencao.percentagem)
				taxamount.text = "0.00"	#default POR VERIFICAR
			else:
				taxpercentage.text = "0"
				taxamount.text = "0.00"	#default 
	



		#END OF TaxTable

		'''

		#GeneralLEdgerEntries
		generalledgerentries = ET.SubElement(data,'GeneralLedgerEntries')
		#generalledgerentries = ET.Element('GeneralLedgerEntries')

		#primeirodiames = '2019-02-18'
		#ultimodiames = '2019-02-18'


		jvs = frappe.db.sql(""" select count(name), sum(total_debit), sum(total_credit) from `tabJournal Entry` where company = %s and docstatus = 1 and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		numberofentries = ET.SubElement(generalledgerentries,'NumberOfEntries')
		totaldebit = ET.SubElement(generalledgerentries,'TotalDebit')
		totalcredit = ET.SubElement(generalledgerentries,'TotalCredit')

		if int(jvs[0]['count(name)']) !=0:
			numberofentries.text = str(jvs[0]['count(name)'])
			totaldebit.text = str(jvs[0]['sum(total_debit)'])
			totalcredit.text = str(jvs[0]['sum(total_credit)'])



			print 'Journal Entry'
			print 'Journal Entry'
			print jvs


			#JV
			jvs = frappe.db.sql(""" select * from `tabJournal Entry` where company = %s and docstatus = 1 and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

			for jv in jvs:
				print jv.name
				print jv.cheque_date	
				journal = ET.SubElement(generalledgerentries,'Journal')
				journalid = ET.SubElement(journal,'JournalID')
				journalid.text = str(jv.name)
		
				description = ET.SubElement(journal,'Description')
				if jv.user_remark != None:
					description.text = str(jv.user_remark.strip())
				elif jv.cheque_no != None:
					description.text = str(jv.cheque_no.strip())
				elif jv.remark != None:
					description.text = str(jv.remark.strip())


				#transaction

				transaction = ET.SubElement(journal,'Transaction')
				transactionid = ET.SubElement(transaction,'TransactionID')
				transactionid.text = str(jv.posting_date.strftime("%Y-%m-%d")) + "  " + str(jv.name)

				period = ET.SubElement(transaction,'Period')
				period.text = str(jv.modified.year)		#check date YEAR

				transactiondate = ET.SubElement(transaction,'TransactionDate')
				if jv.cheque_date:
					transactiondate.text = str(jv.cheque_date)
				else:
					transactiondate.text = str(jv.posting_date.strftime("%Y-%m-%d"))

				sourceid = ET.SubElement(transaction,'SourceID')
				if jv.owner.find("@"):
					sourceid.text = str(jv.owner[0:jv.owner.find("@")])	#Retirar o Email only names...
				else:
					sourceid.text = str(jv.owner)	#Retirar o Email only names...

				description = ET.SubElement(transaction,'Description')
				if jv.user_remark != None:
					description.text = str(jv.remark.strip())	

				docarchivalnumber = ET.SubElement(transaction,'DocArchivalNumber')
				#Sera o GL ou pode ser o jv.name !!!!
				#Pode ser o REFERENCE NUMBER

				transactiontype = ET.SubElement(transaction,'TransactionType')
				#jv.voucher_type
				transactiontype.text = "N"	# default para APP

				glpostingdate = ET.SubElement(transaction,'GLPostingDate')
				#glpostingdate.text = str(jv.posting_date.strftime("%Y-%m-%d")) + "T" + str(jv.posting_date.strftime("%H:%M:%S"))	#Posting date to JV
				glpostingdate.text = str(jv.posting_date.strftime("%Y-%m-%d"))

				customerid = ET.SubElement(transaction,'CustomerID')
				supplierid = ET.SubElement(transaction,'SupplierID')

				#lines
				lines = ET.SubElement(transaction,'Lines')
				jvaccounts = frappe.db.sql(""" select * from `tabJournal Entry Account` where parent = %s order by idx """,(jv.name), as_dict=True)

				for jvaccount in jvaccounts:
					#In case we need to get account_number instead
					#conta = frappe.db.sql(""" select * from `tabAccount` where name = %s and company = %s """,(jvaccount.account,empresa.name), as_dict=True)
					#accountid.text = conta[0].account_number

					#DEBIT
					if jvaccount.debit != 0:
						debitline = ET.SubElement(lines,'DebitLine')
						recordid = ET.SubElement(debitline,'RecordID')
						recordid.text = str(jvaccount.idx)

						accountid = ET.SubElement(debitline,'AccountID')
						accountid.text = str(jvaccount.account.strip())
						#accountid.text = conta[0].account_number

						#Is this SI/DN or the JV ID
						sourcedocumentid = ET.SubElement(debitline,'SourceDocumentID')
						sourcedocumentid.text = str(jv.name) #str(jvaccount.account)

						systementrydate = ET.SubElement(debitline,'SystemEntryDate')
						systementrydate.text = str(jvaccount.creation.strftime("%Y-%m-%dT%H:%M:%S"))	#Creation


						description = ET.SubElement(debitline,'Description')
						description.text = str(jvaccount.account.strip())	

						debitamount = ET.SubElement(debitline,'DebitAmount')
						debitamount.text = str("{0:.2f}".format(jvaccount.debit)) #str(jvaccount.debit)	

						#para cliente ou supplier
						if jvaccount.party_type == "Customer":
							customerid.text = str(jvaccount.party)	

						elif jvaccount.party_type == "Supplier":
							supplierid.text = str(jvaccount.party)	

					elif jvaccount.credit != 0:
						#CREDIT
						creditline = ET.SubElement(lines,'CreditLine')
						recordid = ET.SubElement(creditline,'RecordID')
						recordid.text = str(jvaccount.idx)

						accountid = ET.SubElement(creditline,'AccountID')
						accountid.text = str(jvaccount.account.strip())
						#accountid.text = conta[0].account_number

						sourcedocumentid = ET.SubElement(creditline,'SourceDocumentID')
						#JV NAME or SI/ASSETS .... needs to check first ...

						sourcedocumentid.text = str(jv.name) # Now as DEFAULT
						#str(jvaccount.account)

						systementrydate = ET.SubElement(creditline,'SystemEntryDate')
						systementrydate.text = str(jvaccount.creation.strftime("%Y-%m-%dT%H:%M:%S"))	#Creation

						description = ET.SubElement(creditline,'Description')
						description.text = str(jvaccount.account.strip())	

						creditamount = ET.SubElement(creditline,'CreditAmount')
						creditamount.text = str("{0:.2f}".format(jvaccount.credit)) #str(jvaccount.credit)	

						#para cliente ou supplier
						if jvaccount.party_type == "Customer":
							customerid.text = str(jvaccount.party)	

						elif jvaccount.party_type == "Supplier":
							supplierid.text = str(jvaccount.party)	
	
		'''
	#END OF GeneralLEdgerEntries


	# ===================================== GeneralLedgerEntries GL ENTRY
	
	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "C":

		#GeneralLEdgerEntries
		generalledgerentries = ET.SubElement(data,'GeneralLedgerEntries')
		#generalledgerentries = ET.Element('GeneralLedgerEntries')

		#primeirodiames = '2019-02-18'
		#ultimodiames = '2019-02-18'


		jvs = frappe.db.sql(""" select count(name), sum(debit), sum(credit) from `tabGL Entry` where company = %s and docstatus = 1 and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		numberofentries = ET.SubElement(generalledgerentries,'NumberOfEntries')
		totaldebit = ET.SubElement(generalledgerentries,'TotalDebit')
		totalcredit = ET.SubElement(generalledgerentries,'TotalCredit')

		if int(jvs[0]['count(name)']) !=0:
			numberofentries.text = str(jvs[0]['count(name)'])
			totaldebit.text = str("{0:.2f}".format(jvs[0]['sum(debit)']))
			if jvs[0]['sum(credit)'] != 0:
				totalcredit.text = str("{0:.2f}".format(jvs[0]['sum(credit)']))
			else:
				totalcredit.text = "0.00"

			print 'GL Entry'
			print 'GL Entry'
			print jvs


			#JV	group by voucher_type ??????
			jvs = frappe.db.sql(""" select * from `tabGL Entry` where company = %s and docstatus = 1 and posting_date >= %s and posting_date <= %s  """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

			#processa por SI, PI... assim busca todos os movimentos...mesmo sem JV
			for jv in jvs:
				print "asdfsadfsafsaddfsafdfasdfsadfas"
				print jv.name
				print primeirodiames
				print ultimodiames
	#			if jv.voucher_type == "Payment Entry":	# or jv.voucher_type == "Journal Entry":
				print "Entrada ", jv.voucher_no


					#pagamentos = frappe.db.sql(""" select * from `tabPayment Entry` where company = %s and docstatus = 1 and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)
					#if "0045" in jv.voucher_no: # or jv.voucher_no == "JV-29779":

	#				if jv.voucher_no == 'PE-19/0045': # or jv.voucher_no == "JV-29779":

				journal = ET.SubElement(generalledgerentries,'Journal')
				journalid = ET.SubElement(journal,'JournalID')
				journalid.text = str(jv.name)
					

				if jv.voucher_type: #jv.remarks != None:
					description = ET.SubElement(journal,'Description')
					description.text = str(jv.voucher_type.strip())

				#transaction

				transaction = ET.SubElement(journal,'Transaction')
				transactionid = ET.SubElement(transaction,'TransactionID')
				transactionid.text = str(jv.posting_date.strftime("%Y-%m-%d")) + "  " + str(jv.name) #str(jv.voucher_no)

				period = ET.SubElement(transaction,'Period')
				period.text = str(jv.posting_date.strftime("%m"))	#str(jv.modified.year)		#check date YEAR

				transactiondate = ET.SubElement(transaction,'TransactionDate')
				transactiondate.text = str(jv.posting_date)

				sourceid = ET.SubElement(transaction,'SourceID')
				if jv.owner.find("@"):
					#sourceid.text = str(jv.owner[0:jv.owner.find("@")])	#Retirar o Email only names... busca o username
					print frappe.get_doc('User',jv.owner)
					utilizador = frappe.get_doc('User',jv.owner)
					sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username
				else:
					sourceid.text = str(jv.owner)	#Retirar o Email only names...

				if jv.remarks != None:
					description = ET.SubElement(transaction,'Description')
					description.text = str(jv.remarks.strip())	

				docarchivalnumber = ET.SubElement(transaction,'DocArchivalNumber')
				docarchivalnumber.text = "N/A"	#ERPNext does not have...

				#Sera o GL ou pode ser o jv.name !!!!
				#Pode ser o REFERENCE NUMBER

				transactiontype = ET.SubElement(transaction,'TransactionType')
				#jv.voucher_type
				transactiontype.text = "N"	# default para APP

				glpostingdate = ET.SubElement(transaction,'GLPostingDate')
				#glpostingdate.text = str(jv.posting_date.strftime("%Y-%m-%d")) + "T" + str(jv.posting_date.strftime("%H:%M:%S"))	#Posting date to JV
				glpostingdate.text = str(jv.posting_date.strftime("%Y-%m-%d"))


				#if jv.party_type == "Sales Invoice":
				#	customerid = ET.SubElement(transaction,'CustomerID')
				#	customerid.text = jv.party

				#elif jv.party_type == "Purchase Invoice":
				#	supplierid = ET.SubElement(transaction,'SupplierID')
				#	customerid.text = jv.party



				jvs1 = frappe.db.sql(""" select * from `tabGL Entry` where company = %s and docstatus = 1 and posting_date >= %s and posting_date <= %s and name = %s """,(empresa.name,primeirodiames,ultimodiames, jv.name), as_dict=True)
				for jv1 in jvs1:

					#return	

					#lines
					lines = ET.SubElement(transaction,'Lines')
					jvaccounts = frappe.db.sql(""" select * from `tabJournal Entry Account` where parent = %s order by idx """,(jv.name), as_dict=True)
	
					#DEBIT GL
					if jv1.debit != 0:
						debitline = ET.SubElement(lines,'DebitLine')
						recordid = ET.SubElement(debitline,'RecordID')
						recordid.text = str(jv1.idx)

						accountid = ET.SubElement(debitline,'AccountID')
						#accountid.text = str(jv1.account.strip())
						accountid.text = str(jv1.account[0:jv1.account.find('-')]).strip()
						#accountid.text = conta[0].account_number

						#Is this SI/DN or the JV ID
						sourcedocumentid = ET.SubElement(debitline,'SourceDocumentID')
						sourcedocumentid.text = str(jv1.voucher_no) #str(jv.name) #str(jvaccount.account)

						systementrydate = ET.SubElement(debitline,'SystemEntryDate')
						systementrydate.text = str(jv1.creation.strftime("%Y-%m-%dT%H:%M:%S"))	#Creation



						if jv.voucher_type == "Payment Entry":
							pagamentos = frappe.db.sql(""" select * from `tabPayment Entry` where company = %s and name = %s """,(empresa.name,jv1.voucher_no), as_dict=True)
							if pagamentos:
								if pagamentos[0].reference_no:
									description = ET.SubElement(debitline,'Description')
									description.text = str(pagamentos[0].reference_no.strip())									


						debitamount = ET.SubElement(debitline,'DebitAmount')
						debitamount.text = str("{0:.2f}".format(jv1.debit)) #str(jvaccount.debit)	

						#para cliente ou supplier
						#if jvaccount.party_type == "Customer":
						#	customerid.text = str(jvaccount.party)	

						#elif jvaccount.party_type == "Supplier":
						#	supplierid.text = str(jvaccount.party)	

					elif jv1.credit != 0:
						#CREDIT
						creditline = ET.SubElement(lines,'CreditLine')
						recordid = ET.SubElement(creditline,'RecordID')
						recordid.text = str(jv1.idx)

						accountid = ET.SubElement(creditline,'AccountID')
						#accountid.text = str(jv1.account.strip())
						accountid.text = str(jv1.account[0:jv1.account.find('-')]).strip()
						#accountid.text = conta[0].account_number

						sourcedocumentid = ET.SubElement(creditline,'SourceDocumentID')
						#JV NAME or SI/ASSETS .... needs to check first ...
						sourcedocumentid.text = str(jv1.voucher_no)
						#sourcedocumentid.text = str(jv.name) # Now as DEFAULT
						#str(jvaccount.account)

						systementrydate = ET.SubElement(creditline,'SystemEntryDate')
						systementrydate.text = str(jv1.creation.strftime("%Y-%m-%dT%H:%M:%S"))	#Creation

						if jv.voucher_type == "Payment Entry":
							pagamentos = frappe.db.sql(""" select * from `tabPayment Entry` where company = %s and name = %s """,(empresa.name,jv1.voucher_no), as_dict=True)
							if pagamentos:
								if pagamentos[0].reference_no:
									description = ET.SubElement(creditline,'Description')
									description.text = str(pagamentos[0].reference_no.strip())									


						creditamount = ET.SubElement(creditline,'CreditAmount')
						creditamount.text = str("{0:.2f}".format(jv1.credit)) #str(jvaccount.credit)	

						#para cliente ou supplier
						#if jvaccount.party_type == "Customer":
						#	customerid.text = str(jvaccount.party)	

						#elif jvaccount.party_type == "Supplier":
						#	supplierid.text = str(jvaccount.party)	

			'''
			for jv in jvs:
				print jv.name
				print jv.cheque_date	
				journal = ET.SubElement(generalledgerentries,'Journal')
				journalid = ET.SubElement(journal,'JournalID')
				journalid.text = str(jv.name)
		
				description = ET.SubElement(journal,'Description')
				if jv.remarks != None:
					description.text = str(jv.remarks.strip())
				#elif jv.cheque_no != None:
				#	description.text = str(jv.cheque_no.strip())
				#elif jv.remark != None:
				#	description.text = str(jv.remark.strip())


				#transaction

				transaction = ET.SubElement(journal,'Transaction')
				transactionid = ET.SubElement(transaction,'TransactionID')
				transactionid.text = str(jv.posting_date.strftime("%Y-%m-%d")) + "  " + str(jv.voucher_no)

				period = ET.SubElement(transaction,'Period')
				period.text = str(jv.modified.year)		#check date YEAR

				transactiondate = ET.SubElement(transaction,'TransactionDate')
				transactiondate.text = str(jv.posting_date)
				#if jv.cheque_date:
				#	transactiondate.text = str(jv.cheque_date)
				#else:
				#	transactiondate.text = str(jv.posting_date.strftime("%Y-%m-%d"))

				sourceid = ET.SubElement(transaction,'SourceID')
				if jv.owner.find("@"):
					sourceid.text = str(jv.owner[0:jv.owner.find("@")])	#Retirar o Email only names...
				else:
					sourceid.text = str(jv.owner)	#Retirar o Email only names...

				description = ET.SubElement(transaction,'Description')
				if jv.remarks != None:
					description.text = str(jv.remarks.strip())	

				docarchivalnumber = ET.SubElement(transaction,'DocArchivalNumber')
				#Sera o GL ou pode ser o jv.name !!!!
				#Pode ser o REFERENCE NUMBER

				transactiontype = ET.SubElement(transaction,'TransactionType')
				#jv.voucher_type
				transactiontype.text = "N"	# default para APP

				glpostingdate = ET.SubElement(transaction,'GLPostingDate')
				#glpostingdate.text = str(jv.posting_date.strftime("%Y-%m-%d")) + "T" + str(jv.posting_date.strftime("%H:%M:%S"))	#Posting date to JV
				glpostingdate.text = str(jv.posting_date.strftime("%Y-%m-%d"))


				if jv.party_type == "Sales Invoice":
					customerid = ET.SubElement(transaction,'CustomerID')
					customerid.text = jv.party

				elif jv.party_type == "Purchase Invoice":
					supplierid = ET.SubElement(transaction,'SupplierID')
					customerid.text = jv.party

				#lines
				lines = ET.SubElement(transaction,'Lines')
				jvaccounts = frappe.db.sql(""" select * from `tabJournal Entry Account` where parent = %s order by idx """,(jv.name), as_dict=True)

				for jvaccount in jvaccounts:
					#In case we need to get account_number instead
					#conta = frappe.db.sql(""" select * from `tabAccount` where name = %s and company = %s """,(jvaccount.account,empresa.name), as_dict=True)
					#accountid.text = conta[0].account_number

					#DEBIT
					if jvaccount.debit != 0:
						debitline = ET.SubElement(lines,'DebitLine')
						recordid = ET.SubElement(debitline,'RecordID')
						recordid.text = str(jvaccount.idx)

						accountid = ET.SubElement(debitline,'AccountID')
						accountid.text = str(jvaccount.account.strip())
						#accountid.text = conta[0].account_number

						#Is this SI/DN or the JV ID
						sourcedocumentid = ET.SubElement(debitline,'SourceDocumentID')
						sourcedocumentid.text = str(jv.name) #str(jvaccount.account)

						systementrydate = ET.SubElement(debitline,'SystemEntryDate')
						systementrydate.text = str(jvaccount.creation.strftime("%Y-%m-%dT%H:%M:%S"))	#Creation


						description = ET.SubElement(debitline,'Description')
						description.text = str(jvaccount.account.strip())	

						debitamount = ET.SubElement(debitline,'DebitAmount')
						debitamount.text = str("{0:.2f}".format(jvaccount.debit)) #str(jvaccount.debit)	

						#para cliente ou supplier
						if jvaccount.party_type == "Customer":
							customerid.text = str(jvaccount.party)	

						elif jvaccount.party_type == "Supplier":
							supplierid.text = str(jvaccount.party)	

					elif jvaccount.credit != 0:
						#CREDIT
						creditline = ET.SubElement(lines,'CreditLine')
						recordid = ET.SubElement(creditline,'RecordID')
						recordid.text = str(jvaccount.idx)

						accountid = ET.SubElement(creditline,'AccountID')
						accountid.text = str(jvaccount.account.strip())
						#accountid.text = conta[0].account_number

						sourcedocumentid = ET.SubElement(creditline,'SourceDocumentID')
						#JV NAME or SI/ASSETS .... needs to check first ...

						sourcedocumentid.text = str(jv.name) # Now as DEFAULT
						#str(jvaccount.account)

						systementrydate = ET.SubElement(creditline,'SystemEntryDate')
						systementrydate.text = str(jvaccount.creation.strftime("%Y-%m-%dT%H:%M:%S"))	#Creation

						description = ET.SubElement(creditline,'Description')
						description.text = str(jvaccount.account.strip())	

						creditamount = ET.SubElement(creditline,'CreditAmount')
						creditamount.text = str("{0:.2f}".format(jvaccount.credit)) #str(jvaccount.credit)	

						#para cliente ou supplier
						if jvaccount.party_type == "Customer":
							customerid.text = str(jvaccount.party)	

						elif jvaccount.party_type == "Supplier":
							supplierid.text = str(jvaccount.party)	

			'''	


	#END OF GeneralLEdgerEntries



	# ======================================



	####SourceDocuments
	sourcedocuments = None	

	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "F" or ficheiro_tipo[0:1].upper() == "S" or ficheiro_tipo[0:1].upper() == "Q":
		sourcedocuments = ET.SubElement(data,'SourceDocuments')

	#create Sales Invoices



		#SalesInvoices
		salesinvoices = ET.SubElement(sourcedocuments,'SalesInvoices')

		'''
		A data de criação do documento de venda [campo 4.1.4.7 - data do documento de venda (InvoiceDate) do SAF-T (AO)];
		ii. A data e hora da criação do documento de venda [campo 4.1.4.12 - data de gravação do documento (SystemEntryDate) do SAF-T (AO)];
		iii. O número do documento de venda [campo 4.1.4.1 - identificação única do documento de venda (InvoiceNo) do SAF-T (AO)];
		iv. O valor do documento de venda [campo 4.1.4.20.3 - total do documento com impostos (GrossTotal) do SAF-T (AO)];
		v. A assinatura gerada no documento anterior, do mesmo tipo e série de documento [campo 4.1.4.4 - chave do documento (Hash) do SAF-T (AO)].

		Para assinar [Registo1.txt = 2010-05-18;2010-05-18T11:22:19;FAC 001/14;3.12;]
		openssl dgst -sha1 -sign ChavePrivada.pem -out Registo1.sha1 Registo1.txt
		'''
		#Paid and Cancelled
		facturas = frappe.db.sql(""" select count(name), sum(rounded_total) from `tabSales Invoice` where company = %s and (status = 'Paid' or status = 'Cancelled' ) and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)


		print facturas
		print int(facturas[0]['count(name)'])


		numberofentries = ET.SubElement(salesinvoices,'NumberOfEntries')
		numberofentries.text = "0"
		numerodeentradas = 0
		totaldebit = ET.SubElement(salesinvoices,'TotalDebit')
		##### POR FAZER
		totalcredit = ET.SubElement(salesinvoices,'TotalCredit')

		####### POR FAZER
		#Facturas com PAID ou Cancelado nao precisa...
		# Paid and Cancelled
		facturas = frappe.db.sql(""" select count(name), sum(rounded_total) from `tabSales Invoice` where company = %s and (status = 'Paid' or status = 'Cancelled' ) and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

	#	if facturas[0].status != 'Paid' and facturas[0].status != 'Cancelled':
		if int(facturas[0]['count(name)']) !=0:
			if facturas[0]['sum(rounded_total)'] != 0:
				numberofentries.text = str(int(facturas[0]['count(name)']))
				numerodeentradas = int(facturas[0]['count(name)'])
				totaldebit.text = str("{0:.2f}".format(int(facturas[0]['sum(rounded_total)'])))
			else:
				totaldebit.text = "0.00"
		else:
			totaldebit.text = "0.00"

		#Creditos ou devolucoes
		facturas = frappe.db.sql(""" select count(name), sum(rounded_total) from `tabSales Invoice` where company = %s and status != 'Paid' and status != 'Cancelled' and status !='Draft' and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)
		if int(facturas[0]['count(name)']) !=0:
			#totalcredit.text = str(int(facturas[0]['sum(rounded_total)']))
			numberofentries.text = str(int(facturas[0]['count(name)']) + int(numerodeentradas))
			if facturas[0]['sum(rounded_total)'] != 0:
				totalcredit.text = str("{0:.2f}".format(int(facturas[0]['sum(rounded_total)'])))
			else:
				totalcredit.text = "0.00"

		else:
			totalcredit.text = "0.00"


	

		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	

		'''
		Gera primeiro o HASH e depois o sistema pega os files e apaga....

		'''
		#invoice para HASH
		facturas = frappe.db.sql(""" select * from `tabSales Invoice` where company = %s and (status = 'Paid' or status = 'Cancelled' or status = 'Return') and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		for factura in facturas:
			if chaveanterior == "":
				#1st record
				print 'primeiro registo'
				hashinfo = str(factura.posting_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";"
			else:
				print 'segundo registo'
				print chaveanterior
				hashinfo = str(factura.posting_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";" + str(chaveanterior)

			print fileregistocontador
			print str(factura.posting_date.strftime("%Y-%m-%d"))
			print str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S"))
			print str(factura.name)

			print 'HASH do SALESINVOICE ', hashinfo
			hashfile = open("/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt","wb")
			hashfile.write(hashinfo)

			fileregistocontador += 1	#contador para registo1, registo2 ....

	#		if fileregistocontador == 240:	
	#			return

	#	return
		exists = os.path.isfile("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")
		if exists:
			os.system("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh") # /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64)) 
		else:
			os.system("~/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")
	

		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	

		#invoice
		facturas = frappe.db.sql(""" select * from `tabSales Invoice` where company = %s and (status = 'Paid' or status = 'Cancelled' or status = 'Return') and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		for factura in facturas:
			print factura.name
			print factura.creation
			print factura.modified

			invoice = ET.SubElement(salesinvoices,'Invoice')

			invoiceno = ET.SubElement(invoice,'InvoiceNo')
			invoiceno.text = str(factura.name)

			#documentstatus
			documentstatus = ET.SubElement(invoice,'DocumentStatus')
			invoicestatus = ET.SubElement(documentstatus,'InvoiceStatus')
			if factura.status =="Paid" and factura.docstatus == 1:
				invoicestatus.text = "F"	#Facturado
			elif factura.status =="Cancelled" and factura.docstatus == 2:
				invoicestatus.text = "A"	#Anulado

			else:
				invoicestatus.text = "N"	#Normal


			invoicestatusdate = ET.SubElement(documentstatus,'InvoiceStatusDate')
			#Will be needed to add T between date and time!!!!!!!
			invoicestatusdate.text = factura.modified.strftime("%Y-%m-%dT%H:%M:%S")	#ultima change


			#Pode ser os Comments when deleted the Documents ....
			if factura.remarks != 'No Remarks' and factura.remarks != 'Sem Observações' and factura.remarks != None:
				reason = ET.SubElement(documentstatus,'Reason')
				reason.text = factura.remarks
			elif factura._comments != None:
				reason = ET.SubElement(documentstatus,'Reason')
				reason.text = factura._comments
		

			sourceid = ET.SubElement(documentstatus,'SourceID')
			#sourceid.text = factura.modified_by	#User

			if factura.modified_by.find("@"):
				#sourceid.text = str(factura.modified_by[0:factura.modified_by.find("@")])
				print frappe.get_doc('User',factura.modified_by)
				utilizador = frappe.get_doc('User',factura.modified_by)
				sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

			else:
				sourceid.text = str(factura.modified_by)


			sourcebilling = ET.SubElement(documentstatus,'SourceBilling')
			sourcebilling.text = "P"	#Default

			salesinvoicehash = ET.SubElement(invoice,'Hash')
			#salesinvoicehash.text = 0	#por rever...

			salesinvoicehashcontrol = ET.SubElement(invoice,'HashControl')
	#		salesinvoicehashcontrol.text = "1" 	#default ver 1 as per the certificate
			#"Nao validado pela AGT"	#default for now

			period = ET.SubElement(invoice,'Period')
			period.text = str(factura.posting_date.strftime("%m"))	#str(factura.modified.month)	#last modified month

			invoicedate = ET.SubElement(invoice,'InvoiceDate')
			invoicedate.text = factura.posting_date.strftime("%Y-%m-%d")	#posting date

			invoicetype = ET.SubElement(invoice,'InvoiceType')
			print 'NC ', factura.return_against
			if factura.is_pos == 1 and factura.status == 'Credit Note Issued':
				invoicetype.text = "NC"	#POS NC usually mistaken...
				salesinvoicehashcontrol.text = "1" + "NC" + "D " + str(factura.name)  	#default ver 1 as per the certificate
			if factura.is_pos == 1 :
				invoicetype.text = "FR"	#POS deve ser FR ou TV
				salesinvoicehashcontrol.text = "1" + "FR" + "D " + str(factura.name)  	#default ver 1 as per the certificate

			elif factura.return_against != None:
				invoicetype.text = "NC"	#Retorno / Credit Note
				salesinvoicehashcontrol.text = "1" + "NC" + "D " + str(factura.name)  	#default ver 1 as per the certificate
			else:
				invoicetype.text = "FT"	#default sales invoice
				salesinvoicehashcontrol.text = "1" + "FT" + "D " + str(factura.name)  	#default ver 1 as per the certificate


	
			#specialRegimes
			specialregimes = ET.SubElement(invoice,'SpecialRegimes')
			selfbillingindicator = ET.SubElement(specialregimes,'SelfBillingIndicator')
			selfbillingindicator.text = "0"	#default 

			cashvatschemeindicator = ET.SubElement(specialregimes,'CashVATSchemeIndicator')
			cashvatschemeindicator.text = "0"	#default 

			thirdpartiesbillingindicator = ET.SubElement(specialregimes,'ThirdPartiesBillingIndicator')
			thirdpartiesbillingindicator.text = "0"	#default 

			sourceid = ET.SubElement(invoice,'SourceID')
			#sourceid.text = factura.owner	#created by

			if factura.owner.find("@"):
				#sourceid.text = str(factura.owner[0:factura.owner.find("@")])
				print frappe.get_doc('User',factura.owner)
				utilizador = frappe.get_doc('User',factura.owner)
				sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

			else:
				sourceid.text = str(factura.owner)


			#eaccode = ET.SubElement(invoice,'EACCode')

			systementrydate = ET.SubElement(invoice,'SystemEntryDate')
			systementrydate.text = factura.creation.strftime("%Y-%m-%dT%H:%M:%S")	#creation date

			#transactions = ET.SubElement(invoice,'Transactions')

			entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='sales invoice' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)
			if entradasgl:
				for entradagl in entradasgl:
					print 'transactions ids'
					print entradagl
					transactionid = ET.SubElement(invoice,'TransactionID')
					transactionid.text = entradagl.name	#entrada GL;single invoice can generate more than 2GL

			customerid = ET.SubElement(invoice,'CustomerID')
			customerid.text = factura.customer	#cliente




			#shipto
			'''
			shipto = ET.SubElement(invoice,'ShipTo')
			deliveryid = ET.SubElement(shipto,'DeliveryID')
			deliverydate = ET.SubElement(shipto,'DeliveryDate')
			warehouseid = ET.SubElement(shipto,'WarehouseID')
			locationid = ET.SubElement(shipto,'LocationID')
			#address
			address = ET.SubElement(shipto,'Address')	
			#buildingnumber = ET.SubElement(address,'BuildingNumber')
			streetname = ET.SubElement(address,'StreetName')
			addressdetail = ET.SubElement(address,'AddressDetail')
			city = ET.SubElement(address,'City')
			postalcode = ET.SubElement(address,'PostalCode')
			province = ET.SubElement(address,'Province')
			country = ET.SubElement(address,'Country')
		
			###### END SHIP TO 
			###### START SHIP FROM 

			#shipfrom
			shipfrom = ET.SubElement(invoice,'ShipFrom')
			deliveryid = ET.SubElement(shipfrom,'DeliveryID')
			deliverydate = ET.SubElement(shipfrom,'DeliveryDate')
			warehouseid = ET.SubElement(shipfrom,'WarehouseID')
			locationid = ET.SubElement(shipfrom,'LocationID')
			#address
			address = ET.SubElement(shipfrom,'Address')
			#buildingnumber = ET.SubElement(address,'BuildingNumber')
			streetname = ET.SubElement(address,'StreetName')
			addressdetail = ET.SubElement(address,'AddressDetail')
			city = ET.SubElement(address,'City')
			postalcode = ET.SubElement(address,'PostalCode')
			province = ET.SubElement(address,'Province')
			country = ET.SubElement(address,'Country')
			'''

			#movementendtime = ET.SubElement(invoice,'MovementEndTime')
			#movementstarttime = ET.SubElement(invoice,'MovementStartTime')

			#line

			facturaitems = frappe.db.sql(""" select * from `tabSales Invoice Item` where parent = %s order by idx """,(factura.name), as_dict=True)
		
			for facturaitem in facturaitems:
				line = ET.SubElement(invoice,'Line')
				linenumber = ET.SubElement(line,'LineNumber')
				linenumber.text = str(facturaitem.idx)

				#SALES ORDER
				#orderreferences
				if facturaitem.sales_order:
					orderreferences = ET.SubElement(line,'OrderReferences')
					originatingon = ET.SubElement(orderreferences,'OriginatingON')
					orderdate = ET.SubElement(orderreferences,'OrderDate')

					originatingon.text = facturaitem.sales_order
					ordemvenda = frappe.db.sql(""" select * from `tabSales Order` where name = %s """,(facturaitem.sales_order), as_dict=True)
					orderdate.text = ordemvenda[0].transaction_date.strftime("%Y-%m-%d")



				productcode = ET.SubElement(line,'ProductCode')
				productcode.text = facturaitem.item_code

				productdescription = ET.SubElement(line,'ProductDescription')
				productdescription.text = facturaitem.item_name.strip()

				quantity = ET.SubElement(line,'Quantity')
				quantity.text = str("{0:.0f}".format(facturaitem.qty))	#str(facturaitem.qty)
				#str("{0:.0f}".format(d[10].qty))



				UnitOfMeasure = ET.SubElement(line,'UnitOfMeasure')
				UnitOfMeasure.text = facturaitem.uom

				unitprice = ET.SubElement(line,'UnitPrice')
				if facturaitem.rate:
					unitprice.text = str("{0:.2f}".format(facturaitem.rate))
				else:
					unitprice.text = "0.00"

				taxbase = ET.SubElement(line,'TaxBase')
				if facturaitem.net_rate:
					taxbase.text = str("{0:.2f}".format(facturaitem.net_rate))
				else:
					taxbase.text = "0.00"


				dn = frappe.db.sql(""" select * from `tabDelivery Note` where name = %s """,(facturaitem.delivery_note), as_dict=True)
				print 'DNnnnn'
				print dn
				if dn:
					taxpointdate = ET.SubElement(line,'TaxPointDate')
					taxpointdate.text = dn[0].posting_date.strftime("%Y-%m-%d")	#DN

				#Against .. in case of change or DN ?????
				#references
				if factura.return_against != None:
					references = ET.SubElement(line,'References')
					reference = ET.SubElement(references,'Reference')

					reference.text = factura.return_against

				#reason = ET.SubElement(references,'Reason')


				if facturaitem.description:
					description = ET.SubElement(line,'Description')
					description.text = facturaitem.description.strip()

				#productserialnumber
				if facturaitem.serial_no:
					productserialnumber = ET.SubElement(line,'ProductSerialNumber')
					serialnumber = ET.SubElement(productserialnumber,'SerialNumber')
					serialnumber.text = facturaitem.serial_no

				###If invoice was cancelled or deleted should not add...!!!!!
				if factura.status !="Cancelled" and factura.docstatus != 2:
					#debitamount = ET.SubElement(line,'DebitAmount')


					creditamount = ET.SubElement(line,'CreditAmount')
					creditamount.text = str("{0:.2f}".format(facturaitem.amount)) #str(facturaitem.amount)
					#POR VER SE TEM....

				#tax
				taxes = ET.SubElement(line,'Taxes')
			
				### TAX por PRODUTO OU SERVICO

				#procura no recibo pelo IS
				#recibos = frappe.db.sql(""" select * from `tabPayment Entry` where parent = %s """,(factura.name), as_dict=True)
				recibosreferencias = frappe.db.sql(""" select * from `tabPayment Entry Reference` where reference_doctype = 'sales invoice' and docstatus = 1 and reference_name = %s """,(factura.name), as_dict=True)
				print 'recibos refenrecias'
				print factura.name
				print recibosreferencias
				temiva = False
	#			if factura.name == 'FT19/0072':
	#				print 'TEM IPC'
	#				print factura.is_pos
	#				return
				
			
				#if facturaitem.imposto_de_consumo or factura.is_pos == 1 :	#Caso tem IPC or IVA or IS_POS
				if factura.is_pos == 0 :	#NOT IS_POS
					#if factura.name == 'SINV-19/06853':
					#	print 'ipc ou is pos'
					#	return
		
					if recibosreferencias:
						recibos = frappe.db.sql(""" select * from `tabPayment Entry` where name = %s """,(recibosreferencias[0].parent), as_dict=True)
						print 'recibos'
						print recibosreferencias[0].parent
						print recibos

						#entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibosreferencias[0].parent), as_dict=True)
						for reciboreferencia in recibosreferencias:
							entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,reciboreferencia.parent), as_dict=True)

							print 'entradasgl+++++'

							#print entradasgl


							if entradasgl:
								for entradagl in entradasgl:

									print entradagl.account
									print entradagl.credit_in_account_currency

									if "34710000" in entradagl.account:
										#imposto de selo
										tax = ET.SubElement(taxes,'Tax')
										taxtype = ET.SubElement(tax,'TaxType')

										taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
										taxcountryregion.text = "AO"


										taxtype.text = "IS"
										taxcode = ET.SubElement(tax,'TaxCode')
										taxcode.text = "NS"

										retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%selo' """,as_dict=True)
										print retn


										taxpercentage = ET.SubElement(tax,'TaxPercentage')
										taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) # str(retn[0].percentagem)		#por ir buscar

										taxamount = ET.SubElement(tax,'TaxAmount')
										#if entradagl.credit:
										#	taxamount.text = str(entradagl.credit)
										#else:
										taxamount.text = "0.00"

									elif "34210000" in entradagl.account:
										#imposto de producao e consumo IPC
										tax = ET.SubElement(taxes,'Tax')
										taxtype = ET.SubElement(tax,'TaxType')

										taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
										taxcountryregion.text = "AO"


										taxtype.text = "NS"
										taxcode = ET.SubElement(tax,'TaxCode')
										taxcode.text = "NS"

										retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'ipc' """,as_dict=True)
										print retn


										taxpercentage = ET.SubElement(tax,'TaxPercentage')
										taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

										taxamount = ET.SubElement(tax,'TaxAmount')
										#if entradagl.credit:
										#	taxamount.text = str(entradagl.credit)
										#else:
										taxamount.text = "0.00"


									'''
									elif "3422" in entradagl.account:	#34220000
										tax = ET.SubElement(taxes,'Tax')
										taxtype = ET.SubElement(tax,'TaxType')

										taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
										taxcountryregion.text = "AO"

										#IVA	ainda por rever
										#Aqui verifica se na ficha do ITEM diz que esta isento....
										taxtype.text = "IVA"
										taxcode = ET.SubElement(tax,'TaxCode')
										taxcode.text = "NOR"

									#else:
									#	taxtype.text = "NS"
									#	taxcode = ET.SubElement(tax,'TaxCode')
									#	taxcode.text = "NS"

										retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%acrescentado' """,as_dict=True)
										print retn


										taxpercentage = ET.SubElement(tax,'TaxPercentage')
										taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

										taxamount = ET.SubElement(tax,'TaxAmount')
										#if entradagl.credit:
										#	taxamount.text = str(entradagl.credit)
										#else:
										taxamount.text = "0.00"
			
									'''
									'''
									elif "34140000" in entradagl.account:
										tax = ET.SubElement(taxes,'Tax')
										taxtype = ET.SubElement(tax,'TaxType')

										taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
										taxcountryregion.text = "AO"

										#retencao na fonte
										taxtype.text = "NS"
										taxcode = ET.SubElement(tax,'TaxCode')
										taxcode.text = "NS"

										retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%fonte' """,as_dict=True)
										print retn


										taxpercentage = ET.SubElement(tax,'TaxPercentage')
										taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

										taxamount = ET.SubElement(tax,'TaxAmount')
										#if entradagl.debit:
										#	taxamount.text = str(entradagl.debit)
										#else:
										taxamount.text = "0.00"

									'''

								#return			
					#IVA
					entradasgliva =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='sales invoice' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)
					print 'factura ', factura.name
					#print entradasgliva
					#return
					for entradaglinva in entradasgliva:
						print entradaglinva.account
						#tem que verificar se o item tem ISENTA
						print facturaitem.item_code
						print facturaitem.isento_iva
						print facturaitem.motivo_isencao
						print "VVVVVVVVAAAA"
						#if facturaitem.item_code in "Leite para Crianças": return
						#if factura.name in 'SINV-00241': return

						if "3422" in entradaglinva.account:	#34220000
							if facturaitem.isento_iva == 1:
								#ISENTO
				
								temiva = False
								print 'IVA'
								tax = ET.SubElement(taxes,'Tax')
								taxtype = ET.SubElement(tax,'TaxType')

								taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
								taxcountryregion.text = "AO"

								#IVA	ainda por rever
								#Aqui verifica se na ficha do ITEM diz que esta isento....
								taxtype.text = "IVA"
								taxcode = ET.SubElement(tax,'TaxCode')
								taxcode.text = "ISE"

								retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
								print retn


								taxpercentage = ET.SubElement(tax,'TaxPercentage')
								#taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar
								taxpercentage.text = "0.00"

								taxamount = ET.SubElement(tax,'TaxAmount')
								#if entradagl.credit:
								#	taxamount.text = str(entradagl.credit)
								#else:
								taxamount.text = "0.00"

								print facturaitem.item_code
								print facturaitem.isento_iva
								print facturaitem.motivo_isencao

								#Busca a ISENCAO
								if facturaitem.motivo_isencao:
									taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
									#motivo = facturaitem.motivo_isento
									#print motivo
									#print motivo.find('-')
									taxexemptionreason.text = facturaitem.motivo_isencao[facturaitem.motivo_isencao.find('-')+1:len(facturaitem.motivo_isencao)] #"Regime Transitório"	#

									taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
									taxexemptioncode.text = facturaitem.motivo_isencao[0:facturaitem.motivo_isencao.find('-')-1] #"M00"


							else:
								temiva = True
								print 'IVA'
								tax = ET.SubElement(taxes,'Tax')
								taxtype = ET.SubElement(tax,'TaxType')

								taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
								taxcountryregion.text = "AO"

								#IVA	ainda por rever
								#Aqui verifica se na ficha do ITEM diz que esta isento....
								taxtype.text = "IVA"
								taxcode = ET.SubElement(tax,'TaxCode')
								taxcode.text = "NOR"

								retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
								print retn


								taxpercentage = ET.SubElement(tax,'TaxPercentage')
								taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

								taxamount = ET.SubElement(tax,'TaxAmount')
								#if entradagl.credit:
								#	taxamount.text = str(entradagl.credit)
								#else:
								taxamount.text = "0.00"

								taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
								taxexemptionreason.text = "0"	#

								taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
								taxexemptioncode.text = "0"


					#if factura.name == 'FAU-19/01539':
					#	return

				else:
						#caso POS or even bcs previous found nothing... 
			
					entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='sales invoice' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)
					#if factura.name == 'FT19/0061':
					#	print 'entradasgl'
					print entradasgl
					#	return

					if entradasgl:

						for entradagl in entradasgl:

							print entradagl.account
							print entradagl.credit_in_account_currency


							if "34710000" in entradagl.account:
								tax = ET.SubElement(taxes,'Tax')
								taxtype = ET.SubElement(tax,'TaxType')

								taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
								taxcountryregion.text = "AO"

								#imposto de selo
								taxtype.text = "IS"
								taxcode = ET.SubElement(tax,'TaxCode')
								taxcode.text = "NS"

								retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%selo' """,as_dict=True)
								print retn


								taxpercentage = ET.SubElement(tax,'TaxPercentage')
								taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

								taxamount = ET.SubElement(tax,'TaxAmount')
								#if entradagl.credit:
								#	taxamount.text = str(entradagl.credit)
								#else:
								taxamount.text = "0.00"

							elif "34210000" in entradagl.account:
								tax = ET.SubElement(taxes,'Tax')
								taxtype = ET.SubElement(tax,'TaxType')

								taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
								taxcountryregion.text = "AO"

								#imposto de producao e consumo IPC
								taxtype.text = "NS"
								taxcode = ET.SubElement(tax,'TaxCode')
								taxcode.text = "NS"

								retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'ipc' """,as_dict=True)
								print retn


								taxpercentage = ET.SubElement(tax,'TaxPercentage')
								taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

								taxamount = ET.SubElement(tax,'TaxAmount')
								#if entradagl.credit:
								#	taxamount.text = str(entradagl.credit)
								#else:
								taxamount.text = "0.00"





							'''
							elif "3422" in entradagl.account:	#34220000
								tax = ET.SubElement(taxes,'Tax')
								taxtype = ET.SubElement(tax,'TaxType')

								taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
								taxcountryregion.text = "AO"

								#IVA	ainda por rever
								taxtype.text = "IVA"
								taxcode = ET.SubElement(tax,'TaxCode')
								taxcode.text = "NOR"

							#else:
							#	taxtype.text = "NS"
							#	taxcode = ET.SubElement(tax,'TaxCode')
							#	taxcode.text = "NS"

								retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
								print retn


								taxpercentage = ET.SubElement(tax,'TaxPercentage')
								taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

								taxamount = ET.SubElement(tax,'TaxAmount')
								#if entradagl.credit:
								#	taxamount.text = str(entradagl.credit)
								#else:
								taxamount.text = "0.00"
							'''
							'''
							elif "34140000" in entradagl.account:
								tax = ET.SubElement(taxes,'Tax')
								taxtype = ET.SubElement(tax,'TaxType')

								taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
								taxcountryregion.text = "AO"

								#retencao na fonte
								taxtype.text = "NS"
								taxcode = ET.SubElement(tax,'TaxCode')
								taxcode.text = "NS"

								retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%fonte' """,as_dict=True)
								print retn


								taxpercentage = ET.SubElement(tax,'TaxPercentage')
								taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

								taxamount = ET.SubElement(tax,'TaxAmount')
								#if entradagl.debit:
								#	taxamount.text = str(entradagl.debit)
								#else:
								taxamount.text = "0.00"
							'''

					#IVA
					entradasgliva =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='sales invoice' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)
					print 'factura ', factura.name
					#print entradasgliva
					#print 'PARAAAAAAAA '
					#return	
					for entradaglinva in entradasgliva:
						print entradaglinva.account

						print facturaitem.item_code
						print facturaitem.isento_iva
						print facturaitem.motivo_isencao
						print "IIIIIIIIIVVVVV"	

						#if facturaitem.item_code in "Leite para Crianças": return
						#if factura.name == 'SINV-00241': return

						if "3422" in entradaglinva.account:	#34220000
							if facturaitem.isento_iva == 1:
								#ISENTO
				
								temiva = False
								print 'IVA'
								tax = ET.SubElement(taxes,'Tax')
								taxtype = ET.SubElement(tax,'TaxType')

								taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
								taxcountryregion.text = "AO"

								#IVA	ainda por rever
								#Aqui verifica se na ficha do ITEM diz que esta isento....
								taxtype.text = "IVA"
								taxcode = ET.SubElement(tax,'TaxCode')
								taxcode.text = "ISE"

								retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
								print retn


								taxpercentage = ET.SubElement(tax,'TaxPercentage')
								#taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar
								taxpercentage.text = "0.00"

								taxamount = ET.SubElement(tax,'TaxAmount')
								#if entradagl.credit:
								#	taxamount.text = str(entradagl.credit)
								#else:
								taxamount.text = "0.00"

								print facturaitem.item_code
								print facturaitem.isento_iva
								print facturaitem.motivo_isencao

								#Busca a ISENCAO
								if facturaitem.motivo_isencao:
									taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
									#motivo = facturaitem.motivo_isento
									#print motivo
									#print motivo.find('-')
									taxexemptionreason.text = facturaitem.motivo_isencao[facturaitem.motivo_isencao.find('-')+1:len(facturaitem.motivo_isencao)] #"Regime Transitório"	#

									taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
									taxexemptioncode.text = facturaitem.motivo_isencao[0:facturaitem.motivo_isencao.find('-')-1] #"M00"


							else:
								temiva = True
								print 'IVA'


								tax = ET.SubElement(taxes,'Tax')
								taxtype = ET.SubElement(tax,'TaxType')

								taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
								taxcountryregion.text = "AO"

								#IVA	ainda por rever
								#Aqui verifica se na ficha do ITEM diz que esta isento....
								taxtype.text = "IVA"
								taxcode = ET.SubElement(tax,'TaxCode')
								taxcode.text = "NOR"

							#else:
							#	taxtype.text = "NS"
							#	taxcode = ET.SubElement(tax,'TaxCode')
							#	taxcode.text = "NS"

								retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
								print retn


								taxpercentage = ET.SubElement(tax,'TaxPercentage')
								taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

								taxamount = ET.SubElement(tax,'TaxAmount')
								#if entradagl.credit:
								#	taxamount.text = str(entradagl.credit)
								#else:
								taxamount.text = "0.00"

								taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
								taxexemptionreason.text = "0"	#

								taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
								taxexemptioncode.text = "0"




					#if factura.name == 'FT19/0072':
					#	return
				'''
				if temiva == True:
					taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
					taxexemptionreason.text = "0"	#

					taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
					taxexemptioncode.text = "0"

				else:
					print facturaitem.item_code
					print facturaitem.isento_iva
					print facturaitem.motivo_isento

					#Busca a ISENCAO
					taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
					motivo = facturaitem.motivo_isento
					print motivo
					print motivo.find('-')
					taxexemptionreason.text = facturaitem.motivo_isento[facturaitem.motivo_isento.find('-')+1:len(facturaitem.motivo_isento)] #"Regime Transitório"	#

					taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
					taxexemptioncode.text = facturaitem.motivo_isento[0:facturaitem.motivo_isento.find('-')-1] #"M00"

				'''


				if factura.discount_amount:
					settlementamount = ET.SubElement(line,'SettlementAmount')
					settlementamount.text = str("{0:.2f}".format(factura.discount_amount))
					#if facturaitem.discount_amount:
					#	settlementamount.text = facturaitem.margin_rate_or_amount	#we can if % is added instead do the calcs...
				#else:
				#	settlementamount.text = "0.00"

				#customsinformation
				#customsinformation = ET.SubElement(line,'CustomsInformation')
				#arcno = ET.SubElement(customsinformation,'ARCNo')
				#iecamount = ET.SubElement(customsinformation,'IECAmount')



			#documenttotals
			documenttotals = ET.SubElement(invoice,'DocumentTotals')

			taxpayable = ET.SubElement(documenttotals,'TaxPayable')
			print 'factura Referencia'
			if factura.docstatus != 2:
				salestaxescharges = frappe.db.sql(""" select * from `tabSales Taxes and Charges` where parent = %s """,(factura.name),as_dict=True)
				print salestaxescharges

				if salestaxescharges: 
					print salestaxescharges[0].tax_amount
					taxpayable.text = str("{0:.2f}".format(salestaxescharges[0].tax_amount)) #str(salestaxescharges[0].tax_amount) 		#por ir buscar 
				else:
					taxpayable.text = "0.00" 		#por ir buscar 
			#if retencao.credit_in_account_currency:
			#	taxpayable.text = str(retencao.credit_in_account_currency) 		#por ir buscar 

			nettotal = ET.SubElement(documenttotals,'NetTotal')
			nettotal.text = str("{0:.2f}".format(factura.net_total)) #str(factura.net_total)		#Sem Impostos Total Factura

			grosstotal = ET.SubElement(documenttotals,'GrossTotal')
			if factura.rounded_total:
				grosstotal.text = str("{0:.2f}".format(factura.rounded_total)) #str(factura.rounded_total)		#Total Factura + impostos.... por ir buscar
			else:
				grosstotal.text = "0.00"

			####ONLY IF NOT AOA .... POR VERIFICAR
			#currency
			if factura.currency != "KZ":
				currency = ET.SubElement(documenttotals,'Currency')
				currencycode = ET.SubElement(currency,'CurrencyCode')

				currencycode.text = str(factura.currency)

				currencyamount = ET.SubElement(currency,'CurrencyAmount')
				currencyamount.text = str("{0:.2f}".format(factura.rounded_total))

				exchangerate = ET.SubElement(currency,'ExchangeRate')
				exchangerate.text = str("{0:.2f}".format(factura.conversion_rate))

			#settlement
			pagschedls = frappe.db.sql(""" select name, parent, payment_term, description, due_date, invoice_portion, payment_amount from `tabPayment Schedule` where parent = %s and docstatus = 1 """,(factura.name),as_dict=True)

			if pagschedls:
				for pagschedl in pagschedls:
					if pagschedl.payment_term:
						settlement = ET.SubElement(documenttotals,'Settlement')
						settlementdiscount = ET.SubElement(settlement,'SettlementDiscount')
						settlementdiscount.text = str(pagschedl.description)

						settlementamount = ET.SubElement(settlement,'SettlementAmount')
						settlementamount.text = str("{0:.2f}".format(pagschedl.payment_amount))

						settlementdate = ET.SubElement(settlement,'SettlementDate')
						settlementdate.text = str(pagschedl.due_date)

						paymentterms = ET.SubElement(settlement,'PaymentTerms')
						paymentterms.text = str(pagschedl.payment_term)

			#payment



			if recibosreferencias:
				recibos = frappe.db.sql(""" select * from `tabPayment Entry` where name = %s """,(recibosreferencias[0].parent), as_dict=True)
				print 'recibos'
				print recibosreferencias[0].parent
				print recibos

				for recibo in recibos:
					payment = ET.SubElement(documenttotals,'Payment')
					paymentmechanism = ET.SubElement(payment,'PaymentMechanism')				

					if "Transferência Bancária" in recibo.mode_of_payment:
						paymentmechanism.text = "TB"
					elif "Cash" in recibo.mode_of_payment:					
						paymentmechanism.text = "NU"

					elif "TPA" in recibo.mode_of_payment:					
						paymentmechanism.text = "CD"

					elif "Cheque Bancário".upper() in recibo.mode_of_payment:
						paymentmechanism.text = "CH"
					else:
						#did not found... search the Mode of payment TYPE
						modopagamento = frappe.get_doc("Mode of Payment",recibo.mode_of_payment)
						if modopagamento.type == 'Bank':
							paymentmechanism.text = "TB"
						elif modopagamento.type == 'Cash':
							paymentmechanism.text = "NU"

					paymentamount = ET.SubElement(payment,'PaymentAmount')
					paymentamount.text = str("{0:.2f}".format(recibo.paid_amount)) #str(recibo.paid_amount)

					paymentdate = ET.SubElement(payment,'PaymentDate')
					paymentdate.text = recibo.posting_date.strftime("%Y-%m-%d")

			#witholdingtax
			#withholdingtax = ET.SubElement(invoice,'WithholdingTax')

			if recibosreferencias:
				recibos = frappe.db.sql(""" select * from `tabPayment Entry` where name = %s """,(recibosreferencias[0].parent), as_dict=True)
				print 'recibos'
				print recibosreferencias[0].parent
				#print recibos

			#entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibosreferencias[0].parent), as_dict=True)
				for reciboreferencia in recibosreferencias:
					print reciboreferencia
					entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,reciboreferencia.parent), as_dict=True)
					#witholdingtax
					#withholdingtax = ET.SubElement(invoice,'WithholdingTax')

					print 'entradasgl'
					print entradasgl


					variasentradas = False
					if entradasgl:
						for entradagl in entradasgl:
							print 'conta ', entradagl.account
							if "34710000" in entradagl.account:
								#imposto selo
								if variasentradas == True:
									withholdingtax = ET.SubElement(invoice,'WithholdingTax')

								withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
								withholdingtaxtype.text = "IS"

								withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
								#withholdingtaxdescription.text = entradagl.account.strip()
								if entradagl.account.find('-'):
									withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find('-')+1:len(entradagl.account)]).strip()
								else:
									withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find(' ')+1:len(entradagl.account)]).strip()


								withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
								withholdingtaxamount.text = str("{0:.2f}".format(entradagl.credit)) #str(entradagl.credit)

							elif "34120000" in entradagl.account:
								#imposto industrial
								if variasentradas == True:
									withholdingtax = ET.SubElement(invoice,'WithholdingTax')

								withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
								withholdingtaxtype.text = "II"

								withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
								#withholdingtaxdescription.text = entradagl.account.strip()
								if entradagl.account.find('-'):
									withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find('-')+1:len(entradagl.account)]).strip()
								else:
									withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find(' ')+1:len(entradagl.account)]).strip()


								withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
								withholdingtaxamount.text = str("{0:.2f}".format(entradagl.credit_in_account_currency)) #str(entradagl.credit_in_account_currency)

							elif "34310000" in entradagl.account:
								#IRT
								if variasentradas == True:
									withholdingtax = ET.SubElement(invoice,'WithholdingTax')

								withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
								withholdingtaxtype.text = "IRT"

								withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
								#withholdingtaxdescription.text = entradagl.account.strip()
								if entradagl.account.find('-'):
									withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find('-')+1:len(entradagl.account)]).strip()
								else:
									withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find(' ')+1:len(entradagl.account)]).strip()


								withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
								withholdingtaxamount.text = str("{0:.2f}".format(entradagl.credit_in_account_currency)) #str(entradagl.credit_in_account_currency)

							variasentradas = True	#para garar varias entradas

						'''
						#IVA
						entradasgliva =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='sales invoice' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)
						print 'factura ', factura.name
						#print entradasgliva
						for entradaglinva in entradasgliva:
							print entradaglinva.account

							if "3422" in entradaglinva.account:	#34220000
								tax = ET.SubElement(taxes,'Tax')
								taxtype = ET.SubElement(tax,'TaxType')

								taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
								taxcountryregion.text = "AO"

								#IVA	ainda por rever
								#Aqui verifica se na ficha do ITEM diz que esta isento....
								taxtype.text = "IVA"
								taxcode = ET.SubElement(tax,'TaxCode')
								taxcode.text = "NOR"

							#else:
							#	taxtype.text = "NS"
							#	taxcode = ET.SubElement(tax,'TaxCode')
							#	taxcode.text = "NS"

								retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
								print retn


								taxpercentage = ET.SubElement(tax,'TaxPercentage')
								taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

								taxamount = ET.SubElement(tax,'TaxAmount')
								#if entradagl.credit:
								#	taxamount.text = str(entradagl.credit)
								#else:
								taxamount.text = "0.00"
						'''

			#HASH key to generate	
			#Invoicedate + Sytementrydate + InvoiceNo + Grosstotal
			'''
			if chaveanterior == "":
				#1st record
				print 'primeiro registo'
				hashinfo = str(factura.posting_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";"
			else:
				print 'segundo registo'
				print chaveanterior
				hashinfo = str(factura.posting_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";" + str(chaveanterior)


			print 'HASH do SALESINVOICE ', hashinfo
			hashfile = open("/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt","wb")
			hashfile.write(hashinfo)

			'''
			ficheirosha1  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".sha1"
			ficheirotxt  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt"
			ficheirob64  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".b64"

	#		myCMD = "openssl dgst -sha1 -sign /tmp/angolaer.cert/angolaerp-selfsigned-priv.pem -out /tmp/" +  ficheirosha1 + " /tmp/" + ficheirotxt + " > /tmp/resultado.txt"

	#		myCMD1 = " dgst -sha1 -sign /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem -out /tmp/" +  ficheirosha1 + " /tmp/" + ficheirotxt
	#		myCMD2 =  " /tmp/angolaerp.cert/privkey.pem -out /tmp/" +  ficheirosha1 + " /tmp/" + ficheirotxt

	#		print myCMD
	#		from subprocess import *
	#		import subprocess

	#		decrypted = call(myCMD,shell=True)
	#		print decrypted
	#		p = Popen(["./home/helio/pp1.py"], stdout=PIPE, stderr=PIPE)
			x = "echo -n " + hashinfo
			print x
	#		os.system("/tmp/angolaerp.cert2/bb3.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64)) 

			print "blablalbla"


	#		os.system("python /tmp/angolaerp.cert2/pp1.py")

	#		p = Popen("/tmp/angolaerp.cert2/bb1.sh", shell=True, stdout=PIPE, stderr=PIPE)
	#		p = Popen(["/tmp/angolaerp.cert2/bb1.sh","/tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem",str(ficheirosha1),str(ficheirotxt),str(ficheirob64)], shell=True, stdout=PIPE, stderr=PIPE)

	#		p = Popen(["/tmp/angolaerp.cert2/bb1.sh","/tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem",str(ficheirosha1),str(ficheirotxt),str(ficheirob64)],shell=True, stdout=PIPE, stderr=PIPE)

	#		with open('output','wb',0) as out:
	#			subprocess.run(["/tmp/angolaerp.cert2/bb1.sh","/tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem",str(ficheirosha1),str(ficheirotxt),str(ficheirob64)],shell=False, stdout=out, stderr=PIPE)


	#		p = Popen(['openssl dgst -sha1 -sign /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem -out ' + ficheirosha1 + ficheirotxt  ],shell=True, stdout=PIPE, stderr=PIPE)
	#		print 'ficheiro para executar'
			ddd = '/tmp/angolaerp.cert2/bb1.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem -out ' + ficheirosha1 + ficheirotxt + ficheirob64
			dd1 = "/bin/sh -c /usr/bin/openssl " #dgst -sha1 -sign /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem -out " #+ ficheirosha1 + ficheirotxt
			dd2 = '/tmp/angolaerp.cert2/bb.sh'
	#		print ddd
	#		p = Popen([dd1],shell=True, stdout=PIPE, stderr=PIPE)
	#		output, errors = p.communicate()
	#		p.wait()
			print 'Openssl Signing...'
	#		print output
	#		print errors

			#encoding

	#		p = Popen(['openssl enc -base64 -in ' + ficheirosha1 + ' -out ' + ficheirob64 + ' -A' ],shell=True, stdout=PIPE, stderr=PIPE)

	#		output, errors = p.communicate()
	#		p.wait()
	#		print 'Openssl Encoding...'
	#		print output
	#		print errors


	#		sts = call("/usr/bin/openssl dgst -sha1 -sign /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem -out /tmp/registo1.sha1 /tmp/registo1.txt", shell=True)

	#		print sts

	#		sts1 = call("/usr/bin/openssl enc -base64 -in /tmp/registo1.sha1 -out /tmp/registo1.b64 -A", shell=True)



	#		os.system("/tmp/angolaer.cert/bb1.sh " + myCMD1)	#execute

			#encoding base 64
			#ficheirosha1  = str(fileregisto) + str(fileregistocontador) + ".sha1"
		

			myCMD1 = 'openssl enc -base64 -in ' +  ficheirosha1 + ' -out ' + ficheirob64 + ' -a' #+ ' > /tmp/resultado.txt'

			print myCMD1
			print 'Openssl Encoding...'
			print ficheirosha1
			print ficheirob64

	#		os.system(myCMD1)	#Encondingi
	#		p = Popen([myCMD1], stdout=PIPE, stderr=PIPE)
	#		output, errors = p.communicate()
	#		p.wait()

	#		print output
	#		print errors

	
			hashfile.close()	#close previous ...
			#hashfile.close()	#close previous ...

			hashcriado = open(ficheirob64,'rb')	#open the file created to HASH
			print 'Hash criado'
			#print hashcriado.read()
	#		print hashcriado.read()
			chaveanterior = str(hashcriado.read())	#para usar no next record...
	#		print chaveanterior

			#verifica se tem HASH
			if factura.hash_erp:
				salesinvoicehash.text = str(factura.hash_erp)	#Hash created
			else:
				salesinvoicehash.text = str(chaveanterior)	#do System
		
			hashcriado.close()

			fileregistocontador += 1	#contador para registo1, registo2 ....


	#		if fileregistocontador == 4:
	#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64))
	#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem /tmp/registo1.sha1 /tmp/registo1.txt /tmp/registo1.b64")  
	#			return	
		
			'''
			In case we need to generate Hash for all records on the APP ... this will be done when SAFT export required
			A table Angolaerp_hash must be created with 
				Documenttype, DocumentNumber, Hash, Hashcontrol or Hashversion

			'''
		#Deve no fim apagar todos os regis* criados ....
		os.system("rm /tmp/registo* ")	#execute

	#	os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64)) 
	#	return
		#END OF SAlesInvoice



	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "A" or ficheiro_tipo[0:1].upper() == "Q":

		#create Purchase Invoices
		if sourcedocuments == None:
			sourcedocuments = ET.SubElement(data,'SourceDocuments')

		#BuyingInvoices
		purchaseinvoices = ET.SubElement(sourcedocuments,'PurchaseInvoices')
		#still need to filter per user request by MONTH or dates filter...
		#Default CURRENT MONTH

		#Debitos ou pagamentos
		facturas = frappe.db.sql(""" select count(name), sum(rounded_total) from `tabPurchase Invoice` where company = %s and (status = 'Paid' or status = 'Cancelled' ) and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)


		print facturas
		print int(facturas[0]['count(name)'])

	
		numberofentries = ET.SubElement(purchaseinvoices,'NumberOfEntries')
		numberofentries.text = "0"
		numerodeentradas = 0
		totaldebit = ET.SubElement(purchaseinvoices,'TotalDebit')
		##### POR FAZER
		totalcredit = ET.SubElement(purchaseinvoices,'TotalCredit')

		####### POR FAZER

		if int(facturas[0]['count(name)']) !=0:
			numberofentries.text = str(int(facturas[0]['count(name)']))
			numerodeentradas = int(facturas[0]['count(name)'])
			#Not need
			#totalcredit.text = str(int(facturas[0]['sum(rounded_total)']))
			if facturas[0]['sum(rounded_total)'] != 0:
				totalcredit.text = str("{0:.2f}".format(facturas[0]['sum(rounded_total)']))
			else:
				totalcredit.text = "0.00"

		else:
			totalcredit.text = "0.00"

	
		#DEBITO devolucoes
		facturas = frappe.db.sql(""" select count(name), sum(rounded_total) from `tabPurchase Invoice` where company = %s and (status = 'Return') and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)
		if int(facturas[0]['count(name)']) !=0:
			#totalcredit.text = str(int(facturas[0]['sum(rounded_total)']))
			#totaldebit.text = str("{0:.2f}".format(jvs[0]['sum(debit)']))
			numberofentries.text = str(int(facturas[0]['count(name)']) + int(numerodeentradas))
			if facturas[0]['sum(rounded_total)'] != 0:
				totaldebit.text = str("{0:.2f}".format(facturas[0]['sum(rounded_total)']))
			else:
				totaldebit.text = "0.00"
		else:
			totaldebit.text = "0.00"

	


		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	

		'''
		Gera primeiro o HASH e depois o sistema pega os files e apaga....

		'''
		#invoice para HASH
		facturas = frappe.db.sql(""" select * from `tabPurchase Invoice` where company = %s and (status = 'Paid' or status = 'Cancelled' or status = 'Return') and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		for factura in facturas:
			if chaveanterior == "":
				#1st record
				print 'primeiro registo'
				hashinfo = str(factura.posting_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";"
			else:
				print 'segundo registo'
				print chaveanterior
				hashinfo = str(factura.posting_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";" + str(chaveanterior)

			print fileregistocontador
			print str(factura.posting_date.strftime("%Y-%m-%d"))
			print str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S"))
			print str(factura.name)

			print 'HASH do SALESINVOICE ', hashinfo
			hashfile = open("/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt","wb")
			hashfile.write(hashinfo)

			fileregistocontador += 1	#contador para registo1, registo2 ....

	#		if fileregistocontador == 240:	
	#			return

	#	return
		exists = os.path.isfile("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")
		if exists:
			os.system("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh") # /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64)) 
		else:
			os.system("~/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")

		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	


		#invoice
		facturas = frappe.db.sql(""" select * from `tabPurchase Invoice` where company = %s and (status = 'Paid' or status = 'Cancelled' or status = 'Return') and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		for factura in facturas:
			print factura.name
			print factura.creation
			print factura.modified

			invoice = ET.SubElement(purchaseinvoices,'Invoice')

			invoiceno = ET.SubElement(invoice,'InvoiceNo')
			invoiceno.text = str(factura.name)

			#documentstatus
			documentstatus = ET.SubElement(invoice,'DocumentStatus')
			invoicestatus = ET.SubElement(documentstatus,'InvoiceStatus')
			if factura.status =="Paid" and factura.docstatus == 1:
				invoicestatus.text = "F"	#Facturado
			elif factura.status =="Cancelled" and factura.docstatus == 2:
				invoicestatus.text = "A"	#Anulado

			else:
				invoicestatus.text = "N"	#Normal


			invoicestatusdate = ET.SubElement(documentstatus,'InvoiceStatusDate')
			#Will be needed to add T between date and time!!!!!!!
			invoicestatusdate.text = factura.modified.strftime("%Y-%m-%dT%H:%M:%S")	#ultima change


			#Pode ser os Comments when deleted the Documents ....
			if factura.remarks != 'No Remarks' and factura.remarks != 'Sem Observações' and factura.remarks != None:
				reason = ET.SubElement(documentstatus,'Reason')
				reason.text = factura.remarks
			elif factura._comments != None:
				reason = ET.SubElement(documentstatus,'Reason')
				reason.text = factura._comments

			sourceid = ET.SubElement(documentstatus,'SourceID')
			#sourceid.text = factura.modified_by	#User
			if factura.modified_by.find("@"):
				#sourceid.text = str(factura.modified_by[0:factura.modified_by.find("@")])
				print frappe.get_doc('User',factura.modified_by)
				utilizador = frappe.get_doc('User',factura.modified_by)
				sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

			else:
				sourceid.text = str(factura.modified_by[0:factura.modified_by.find("@")])




			sourcebilling = ET.SubElement(documentstatus,'SourceBilling')
			sourcebilling.text = "P"	#Default

			salesinvoicehash = ET.SubElement(invoice,'Hash')
			#salesinvoicehash.text = 0	#por rever...

			salesinvoicehashcontrol = ET.SubElement(invoice,'HashControl')
			#salesinvoicehashcontrol.text = "Nao validado pela AGT"	#default for now

			period = ET.SubElement(invoice,'Period')
			period.text = str(factura.posting_date.strftime("%m"))	#str(factura.modified.month)	#last modified month

			invoicedate = ET.SubElement(invoice,'InvoiceDate')
			invoicedate.text = factura.posting_date.strftime("%Y-%m-%d")	#posting date

			invoicetype = ET.SubElement(invoice,'InvoiceType')
			print 'NC ', factura.return_against
			if factura.is_pos == 1:
				invoicetype.text = "FR"	#POS deve ser FR ou TV
				salesinvoicehashcontrol.text = "1" + "FR" + "D " + str(factura.name)  	#default ver 1 as per the certificate
			elif factura.return_against != None:
				invoicetype.text = "NC"	#Retorno / Credit Note
				salesinvoicehashcontrol.text = "1" + "NC" + "D " + str(factura.name)  	#default ver 1 as per the certificate

			else:
				invoicetype.text = "FT"	#default sales invoice
				salesinvoicehashcontrol.text = "1" + "FT" + "D " + str(factura.name)  	#default ver 1 as per the certificate

			'''
			#specialRegimes
			specialregimes = ET.SubElement(invoice,'SpecialRegimes')
			selfbillingindicator = ET.SubElement(specialregimes,'SelfBillingIndicator')
			selfbillingindicator.text = "0"	#default 

			cashvatschemeindicator = ET.SubElement(specialregimes,'CashVATSchemeIndicator')
			cashvatschemeindicator.text = "0"	#default 

			thirdpartiesbillingindicator = ET.SubElement(specialregimes,'ThirdPartiesBillingIndicator')
			thirdpartiesbillingindicator.text = "0"	#default 
			'''
			sourceid = ET.SubElement(invoice,'SourceID')
			#sourceid.text = factura.owner	#created by
			#sourceid.text = str(factura.owner[0:factura.owner.find("@")])
			if factura.owner.find("@"):
				#sourceid.text = str(factura.owner[0:factura.owner.find("@")])
				print frappe.get_doc('User',factura.owner)
				utilizador = frappe.get_doc('User',factura.owner)
				sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

			else:
				sourceid.text = str(factura.owner[0:factura.owner.find("@")])


			supplierid = ET.SubElement(invoice,'SupplierID')
			supplierid.text = factura.supplier	#Fornecedor

			'''
			eaccode = ET.SubElement(invoice,'EACCode')

			systementrydate = ET.SubElement(invoice,'SystemEntryDate')
			systementrydate.text = factura.creation.strftime("%Y-%m-%dT%H:%M:%S")	#creation date

			transactions = ET.SubElement(invoice,'Transactions')

			entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='purchase invoice' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)
			if entradasgl:
				for entradagl in entradasgl:
					print 'transactions ids'
					print entradagl
					transactionid = ET.SubElement(transactions,'TransactionID')
					transactionid.text = entradagl.name	#entrada GL;single invoice can generate more than 2GL



			#shipto
			shipto = ET.SubElement(invoice,'ShipTo')
			deliveryid = ET.SubElement(shipto,'DeliveryID')
			deliverydate = ET.SubElement(shipto,'DeliveryDate')
			warehouseid = ET.SubElement(shipto,'WarehouseID')
			locationid = ET.SubElement(shipto,'LocationID')
			#address
			address = ET.SubElement(shipto,'Address')	
			buildingnumber = ET.SubElement(address,'BuildingNumber')
			streetname = ET.SubElement(address,'StreetName')
			addressdetail = ET.SubElement(address,'AddressDetail')
			city = ET.SubElement(address,'City')
			postalcode = ET.SubElement(address,'PostalCode')
			province = ET.SubElement(address,'Province')
			country = ET.SubElement(address,'Country')
			#shipfrom
			shipfrom = ET.SubElement(invoice,'ShipFrom')
			deliveryid = ET.SubElement(shipfrom,'DeliveryID')
			deliverydate = ET.SubElement(shipfrom,'DeliveryDate')
			warehouseid = ET.SubElement(shipfrom,'WarehouseID')
			locationid = ET.SubElement(shipfrom,'LocationID')
			#address
			address = ET.SubElement(shipfrom,'Address')
			buildingnumber = ET.SubElement(address,'BuildingNumber')
			streetname = ET.SubElement(address,'StreetName')
			addressdetail = ET.SubElement(address,'AddressDetail')
			city = ET.SubElement(address,'City')
			postalcode = ET.SubElement(address,'PostalCode')
			province = ET.SubElement(address,'Province')
			country = ET.SubElement(address,'Country')

			movementendtime = ET.SubElement(invoice,'MovementEndTime')
			movementstarttime = ET.SubElement(invoice,'MovementStartTime')

			#line
			line = ET.SubElement(invoice,'Line')
			facturaitems = frappe.db.sql(""" select * from `tabPurchase Invoice Item` where parent = %s order by idx """,(factura.name), as_dict=True)
		
			for facturaitem in facturaitems:

				linenumber = ET.SubElement(line,'LineNumber')
				linenumber.text = str(facturaitem.idx)

				#SALES ORDER
				#orderreferences
				orderreferences = ET.SubElement(line,'OrderReferences')
				originatingon = ET.SubElement(orderreferences,'OriginatingON')
				orderdate = ET.SubElement(orderreferences,'OrderDate')
				if facturaitem.po_detail:
					ordemcompraitem = frappe.get_doc('Purchase Order Item', facturaitem.po_detail)
					originatingon.text = ordemcompraitem.parent
	
					ordemcompra = frappe.get_doc('Purchase Order Item', ordercompraitem.parent) #frappe.db.sql(""" select * from `tabPurchase Order` where name = %s """,(facturaitem.sales_order), as_dict=True)
					orderdate.text = ordemcompra.transaction_date.strftime("%Y-%m-%d")



				productcode = ET.SubElement(line,'ProductCode')
				productcode.text = facturaitem.item_code

				productdescription = ET.SubElement(line,'ProductDescription')
				productdescription.text = facturaitem.item_name

				quantity = ET.SubElement(line,'Quantity')
				quantity.text = str(facturaitem.qty)


				UnitOfMeasure = ET.SubElement(line,'UnitOfMeasure')
				UnitOfMeasure.text = facturaitem.uom

				unitprice = ET.SubElement(line,'UnitPrice')
				unitprice.text = str(facturaitem.rate)

				taxbase = ET.SubElement(line,'TaxBase')
				taxbase.text = str(facturaitem.net_rate)

				taxpointdate = ET.SubElement(line,'TaxPointDate')
				dn = frappe.db.sql(""" select * from `tabDelivery Note` where name = %s """,(facturaitem.delivery_note), as_dict=True)
				print 'DNnnnn'
				print dn
				if dn:
					taxpointdate.text = dn[0].posting_date.strftime("%Y-%m-%d")	#DN

				#Against .. in case of change or DN ?????
				#references
				references = ET.SubElement(line,'References')
				reference = ET.SubElement(references,'Reference')
				if factura.return_against != None:
					reference.text = factura.return_against

				reason = ET.SubElement(references,'Reason')

				description = ET.SubElement(line,'Description')
				description.text = facturaitem.item_description

				#productserialnumber
				productserialnumber = ET.SubElement(line,'ProductSerialNumber')
				serialnumber = ET.SubElement(productserialnumber,'SerialNumber')
				serialnumber.text = facturaitem.serial_no

				###If invoice was cancelled or deleted should not add...!!!!!
				if factura.status !="Cancelled" and factura.docstatus != 2:
					debitamount = ET.SubElement(line,'DebitAmount')
					debitamount.text = str(facturaitem.amount)

					creditamount = ET.SubElement(line,'CreditAmount')
					#POR VER SE TEM....

				#tax
				taxes = ET.SubElement(line,'Taxes')
			
				### TAX por PRODUTO OU SERVICO

				#procura no recibo pelo IS
				#recibos = frappe.db.sql(""" select * from `tabPayment Entry` where parent = %s """,(factura.name), as_dict=True)
				recibosreferencias = frappe.db.sql(""" select * from `tabPayment Entry Reference` where reference_doctype = 'sales invoice' and docstatus = 1 and reference_name = %s """,(factura.name), as_dict=True)
				print 'recibos refenrecias'
				print factura.name
				print recibosreferencias
				if factura.name == 'FT0029/18-1':
					print 'TEM IPC'
					print facturaitem.imposto_de_consumo
				

				if facturaitem.imposto_de_consumo:	#Caso tem IPC or IVA

					if recibosreferencias:
						recibos = frappe.db.sql(""" select * from `tabPayment Entry` where name = %s """,(recibosreferencias[0].parent), as_dict=True)
						print 'recibos'
						print recibosreferencias[0].parent
						print recibos

						entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibosreferencias[0].parent), as_dict=True)

						print 'entradasgl+++++'

						#print entradasgl
						#return


						if entradasgl:
							for entradagl in entradasgl:

								print entradagl.account
								print entradagl.credit_in_account_currency
								if "34210000" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#imposto de producao e consumo IPC
									taxtype.text = "NS"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NS"

									retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'ipc' """,as_dict=True)
									print retn


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									taxamount.text = str(entradagl.credit) 		


								elif "34710000" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#imposto de selo
									taxtype.text = "IS"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NS"

									retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%selo' """,as_dict=True)
									print retn


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									taxamount.text = str(entradagl.credit) 		


								elif "34140000" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#retencao na fonte
									taxtype.text = "NS"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NS"

									retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%fonte' """,as_dict=True)
									print retn


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									taxamount.text = str(entradagl.debit) 		



								elif "IVA" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#IVA	ainda por rever
									taxtype.text = "IVA"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NOR"

								#else:
								#	taxtype.text = "NS"
								#	taxcode = ET.SubElement(tax,'TaxCode')
								#	taxcode.text = "NS"


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									taxamount.text = str(entradagl.credit) 		
			
								#return			

				taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
				taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
				settlementamount = ET.SubElement(line,'SettlementAmount')

				#customsinformation
				customsinformation = ET.SubElement(line,'CustomsInformation')
				arcno = ET.SubElement(customsinformation,'ARCNo')
				iecamount = ET.SubElement(customsinformation,'IECAmount')


			'''
			#documenttotals
			documenttotals = ET.SubElement(invoice,'DocumentTotals')

			inputtax = ET.SubElement(documenttotals,'InputTax')	# IVA
			inputtax.text = "0.00"					#for now
			taxbase = ET.SubElement(documenttotals,'TaxBase')	# 
			taxbase.text = "0.00"					#for now

			grosstotal = ET.SubElement(documenttotals,'GrossTotal')
			if factura.rounded_total:
				grosstotal.text = str("{0:.2f}".format(factura.rounded_total))		#Total Factura + impostos.... por ir buscar
			else:
				grosstotal.text = "0.00"

			deductibletax = ET.SubElement(documenttotals,'DeductibleTax')
			deductiblepercentage = ET.SubElement(documenttotals,'DeductiblePercentage')
			if factura.currency != "KZ":
				currency = ET.SubElement(documenttotals,'Currency')
				currencycode = ET.SubElement(currency,'CurrencyCode')

				currencycode.text = str(factura.currency)

				currencyamount = ET.SubElement(currency,'CurrencyAmount')
				currencyamount.text = str("{0:.2f}".format(factura.rounded_total))

				exchangerate = ET.SubElement(currency,'ExchangeRate')
				exchangerate.text = str("{0:.2f}".format(factura.conversion_rate))


			#currencyamount = ET.SubElement(documenttotals,'CurrencyAmount')

			operationtype = ET.SubElement(documenttotals,'OperationType')
			#How to know if is CMN-compras nacional PSN-prestacao nacional PSN-prestacao estrangeiro OBN-outros bens ICN-investimento
			operationtype.text = "CMN"	#default ... 



			#HASH key to generate	
			#Invoicedate + Sytementrydate + InvoiceNo + Grosstotal

			ficheirosha1  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".sha1"
			ficheirotxt  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt"
			ficheirob64  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".b64"


	
			hashfile.close()	#close previous ...

			hashcriado = open(ficheirob64,'rb')	#open the file created to HASH
			print 'Hash criado'
			chaveanterior = str(hashcriado.read())	#para usar no next record...
			#verifica se tem HASH
			if factura.hash_erp:
				salesinvoicehash.text = str(factura.hash_erp)	#Hash created
			else:
				salesinvoicehash.text = str(chaveanterior)	#do System

		
			hashcriado.close()

			fileregistocontador += 1	#contador para registo1, registo2 ....


	#		if fileregistocontador == 4:
	#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64))
	#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem /tmp/registo1.sha1 /tmp/registo1.txt /tmp/registo1.b64")  
	#			return	
		
			'''
			In case we need to generate Hash for all records on the APP ... this will be done when SAFT export required
			A table Angolaerp_hash must be created with 
				Documenttype, DocumentNumber, Hash, Hashcontrol or Hashversion

			'''

			'''
			print 'factura Referencia'
			if factura.docstatus != 2:
				salestaxescharges = frappe.db.sql(""" select * from `tabSales Taxes and Charges` where parent = %s """,(factura.name),as_dict=True)
				print salestaxescharges

				if salestaxescharges: 
					print salestaxescharges[0].tax_amount
					taxpayable.text = str(salestaxescharges[0].tax_amount) 		#por ir buscar 


			#if retencao.credit_in_account_currency:
			#	taxpayable.text = str(retencao.credit_in_account_currency) 		#por ir buscar 

			nettotal = ET.SubElement(documenttotals,'NetTotal')
			nettotal.text = str(factura.net_total)		#Sem Impostos Total Factura

			####ONLY IF NOT AOA .... POR VERIFICAR
			#currency
			currency = ET.SubElement(documenttotals,'Currency')
			currencycode = ET.SubElement(currency,'CurrencyCode')

			currencyamount = ET.SubElement(currency,'CurrencyAmount')
			#currencyamount.text = str(factura.rounded_total)		#Total Factura + impostos.... por ir buscar

			exchangerate = ET.SubElement(currency,'ExchangeRate')

			#settlement
			settlement = ET.SubElement(documenttotals,'Settlement')
			settlementdiscount = ET.SubElement(settlement,'SettlementDiscount')
			settlementamount = ET.SubElement(settlement,'SettlementAmount')
			settlementdate = ET.SubElement(settlement,'SettlementDate')
			paymentterms = ET.SubElement(settlement,'PaymentTerms')

			#payment
			payment = ET.SubElement(documenttotals,'Payment')


			if recibosreferencias:
				recibos = frappe.db.sql(""" select * from `tabPayment Entry` where name = %s """,(recibosreferencias[0].parent), as_dict=True)
				print 'recibos'
				print recibosreferencias[0].parent
				print recibos

				for recibo in recibos:
					paymentmechanism = ET.SubElement(payment,'PaymentMechanism')				

					if "Transferência Bancária" in recibo.mode_of_payment:
						paymentmechanism.text = "TB"
					elif "Cash" in recibo.mode_of_payment:					
						paymentmechanism.text = "NU"

					elif "TPA" in recibo.mode_of_payment:					
						paymentmechanism.text = "CD"

					paymentamount = ET.SubElement(payment,'PaymentAmount')
					paymentamount.text = str(recibo.paid_amount)

					paymentdate = ET.SubElement(payment,'PaymentDate')
					paymentdate.text = recibo.posting_date.strftime("%Y-%m-%d")

			#witholdingtax
			withholdingtax = ET.SubElement(invoice,'WithholdingTax')

			if recibosreferencias:
				recibos = frappe.db.sql(""" select * from `tabPayment Entry` where name = %s """,(recibosreferencias[0].parent), as_dict=True)
				print 'recibos'
				print recibosreferencias[0].parent
				print recibos

				entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibosreferencias[0].parent), as_dict=True)

				print 'entradasgl'
				print entradasgl



				if entradasgl:
					for entradagl in entradasgl:


						print 'conta ', entradagl.account
						if "34710000" in entradagl.account:
							#imposto selo
							withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
							withholdingtaxtype.text = "IS"

							withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
							withholdingtaxdescription.text = entradagl.account

							withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
							withholdingtaxamount.text = str(entradagl.credit)

						elif "34120000" in entradagl.account:
							#imposto industrial
							withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
							withholdingtaxtype.text = "II"

							withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
							withholdingtaxdescription.text = entradagl.account

							withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
							withholdingtaxamount.text = str(entradagl.credit_in_account_currency)

						elif "34310000" in entradagl.account:
							#IRT
							withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
							withholdingtaxtype.text = "IRT"

							withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
							withholdingtaxdescription.text = entradagl.account

							withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
							withholdingtaxamount.text = str(entradagl.credit_in_account_currency)

			'''
		#Deve no fim apagar todos os regis* criados ....
		os.system("rm /tmp/registo* ")	#execute

		#END OF BuyingInvoices


	#create MovimentofGoods

	#MovementOfGoods
	if ficheiro_tipo[0:1].upper() == "I":
		if sourcedocuments == None:
			sourcedocuments = ET.SubElement(data,'SourceDocuments')

		#get delivery notes / items and count during the period.

		#guiasremessa = frappe.db.sql(""" select * from `tabDelivery Note` where company = %s and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		#primeirodiames = '2019-03-01'
		#ultimodiames = '2019-03-01'



		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	

		'''
		Gera primeiro o HASH e depois o sistema pega os files e apaga....

		'''
		#invoice para HASH
		facturas = frappe.db.sql(""" select * from `tabDelivery Note` where company = %s and docstatus <> 0 and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		for factura in facturas:
			if chaveanterior == "":
				#1st record
				print 'primeiro registo'
				hashinfo = str(factura.posting_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";"
			else:
				print 'segundo registo'
				print chaveanterior
				hashinfo = str(factura.posting_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";" + str(chaveanterior)

			print fileregistocontador
			print str(factura.posting_date.strftime("%Y-%m-%d"))
			print str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S"))
			print str(factura.name)

			print 'HASH do SALESINVOICE ', hashinfo
			hashfile = open("/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt","wb")
			hashfile.write(hashinfo)

			fileregistocontador += 1	#contador para registo1, registo2 ....

	#		if fileregistocontador == 240:	
	#			return

	#	return
		exists = os.path.isfile("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")
		if exists:
			os.system("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh") # /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64)) 
		else:
			os.system("~/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")

		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	


		guiasremessa = frappe.db.sql(""" select count(dn.name), sum(dni.qty) from `tabDelivery Note Item` dni join `tabDelivery Note` dn on dni.parent = dn.name where dn.company = %s and dn.docstatus <> 0 and dn.posting_date >= %s and dn.posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)


		print guiasremessa

		if int(guiasremessa[0]['count(dn.name)']) !=0:
			print 'num linhas ',guiasremessa[0]['count(dn.name)']
			movementofgoods = ET.SubElement(sourcedocuments,'MovementOfGoods')

			numberofmovementlines = ET.SubElement(movementofgoods,'NumberOfMovementLines')

			totalquantityissued = ET.SubElement(movementofgoods,'TotalQuantityIssued')

			numberofmovementlines.text = str(guiasremessa[0]['count(dn.name)'])

		#	guiasremessaitems = frappe.db.sql(""" select * from `tabDelivery Note Item` where parent = %s """,(guiasremessa.name), as_dict=True)



			print 'Qtys ',guiasremessa[0]['sum(dni.qty)']
			totalquantityissued.text = str("{0:.0f}".format(guiasremessa[0]['sum(dni.qty)'])) #str(guiasremessa[0]['sum(dni.qty)'])

		

			guiasremessa = frappe.db.sql(""" select * from `tabDelivery Note` where company = %s and docstatus <> 0 and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

			for guiaremessa in guiasremessa:
				stockmovement = ET.SubElement(movementofgoods,'StockMovement')
				documentnumber = ET.SubElement(stockmovement,'DocumentNumber')
				documentnumber.text = str(guiaremessa.name)

				#documentnumberunique = ET.SubElement(stockmovement,'DocumentNumberUnique')
				#documentnumberunique.text = 0	#default

				documentstatus = ET.SubElement(stockmovement,'DocumentStatus')
				movementstatus = ET.SubElement(documentstatus,'MovementStatus')
				if guiaremessa.status == 'Completed' and guiaremessa.docstatus == 1:
					#pago
					movementstatus.text = "F"
				elif guiaremessa.status == 'To bill' and (guiaremessa.docstatus == 1 or guiaremessa.docstatus == 2):
					#por pagar
					movementstatus.text = "N"
				elif guiaremessa.status == 'Cancelled' and guiaremessa.docstatus == 2:
					#cancelled
					movementstatus.text = "A"
				elif guiaremessa.status == 'Draft' and guiaremessa.docstatus == 0:
					#Draft
					movementstatus.text = "N"

				movementstatusdate = ET.SubElement(documentstatus,'MovementStatusDate')
				movementstatusdate.text = guiaremessa.modified.strftime("%Y-%m-%dT%H:%M:%S")

				#reason = ET.SubElement(documentstatus,'Reason')
				sourceid = ET.SubElement(documentstatus,'SourceID')
				#sourceid.text = guiaremessa.modified_by
				#sourceid.text = str(guiaremessa.modified_by[0:guiaremessa.modified_by.find("@")])
				if guiaremessa.modified_by.find("@"):
					#sourceid.text = str(guiaremessa.modified_by[0:guiaremessa.modified_by.find("@")])
					print frappe.get_doc('User',guiaremessa.modified_by)
					utilizador = frappe.get_doc('User',guiaremessa.modified_by)
					sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

				else:
					sourceid.text = str(guiaremessa.modified_by[0:guiaremessa.modified_by.find("@")])



				sourcebilling = ET.SubElement(documentstatus,'SourceBilling')
				sourcebilling.text = "P"	#default feito pela APP


				movementofgoodshash = ET.SubElement(stockmovement,'Hash')
				#movementofgoodshash.text = 0	#default nossa app nao precisa.

				movementofgoodshashcontrol = ET.SubElement(stockmovement,'HashControl')
				#movementofgoodshashcontrol.text = "Nao validado pela AGT"	#default for now


				period = ET.SubElement(stockmovement,'Period')
				period.text = str(guiaremessa.posting_date.strftime("%m"))	#str(guiaremessa.modified.month)	#last modified month

				movementdate = ET.SubElement(stockmovement,'MovementDate')
				movementdate.text = guiaremessa.modified.strftime("%Y-%m-%dT%H:%M:%S")

				movementtype = ET.SubElement(stockmovement,'MovementType')
				movementtype.text = "GR"	#default Delivery Note
				movementofgoodshashcontrol.text = "1" + "GR" + "D " + str(guiaremessa.name)  	#default ver 1 as per the certificate

				systementrydate = ET.SubElement(stockmovement,'SystemEntryDate')
				systementrydate.text = guiaremessa.creation.strftime("%Y-%m-%dT%H:%M:%S")

				#Get GL; TO CHECK as OURS GENS two or more GLs

				#transactionid = ET.SubElement(stockmovement,'TransactionID')

				#transactions = ET.SubElement(stockmovement,'Transactions')

				entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='delivery note' and company = %s and voucher_no = %s """,(empresa.name,guiaremessa.name), as_dict=True)
				if entradasgl:
					for entradagl in entradasgl:
						print 'transactions ids'
						print entradagl
						transactionid = ET.SubElement(stockmovement,'TransactionID')
						transactionid.text = entradagl.name	#entrada GL;single invoice can generate more than 2GL




				customerid = ET.SubElement(stockmovement,'CustomerID')
				cliente_endereco = angola.get_all_enderecos_a("Customer",guiaremessa.customer)
				customerid.text = guiaremessa.customer

				#supplierid = ET.SubElement(stockmovement,'SupplierID')
				#For now EMPTY

				sourceid = ET.SubElement(stockmovement,'SourceID')
				#sourceid.text = guiaremessa.owner
				#sourceid.text = str(guiaremessa.owner[0:guiaremessa.owner.find("@")])
				if guiaremessa.owner.find("@"):
					#sourceid.text = str(guiaremessa.owner[0:guiaremessa.owner.find("@")])
					print frappe.get_doc('User',guiaremessa.owner)
					utilizador = frappe.get_doc('User',guiaremessa.owner)
					sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

				else:
					sourceid.text = str(guiaremessa.owner[0:guiaremessa.owner.find("@")])


				#eaccode = ET.SubElement(stockmovement,'EACCode')
				#movementcomments = ET.SubElement(stockmovement,'MovementComments')

				if cliente_endereco:
					if cliente_endereco.address_line1:
						shipto = ET.SubElement(stockmovement,'ShipTo')
						#deliveryid = ET.SubElement(shipto,'DeliveryID')
						#deliverydate = ET.SubElement(shipto,'DeliveryDate')
						#warehouseid = ET.SubElement(shipto,'WarehouseID')
						#locationid = ET.SubElement(shipto,'LocationId')

						address = ET.SubElement(shipto,'Address')
						#buildingnumber = ET.SubElement(address,'BuildingNumber')
						streetname = ET.SubElement(address,'StreetName')

						streetname.text = cliente_endereco.address_line1

						addressdetail = ET.SubElement(address,'AddressDetail')
						#if cliente_endereco:
						addressdetail.text = cliente_endereco.address_line1

					
						if cliente_endereco.city:
							city = ET.SubElement(address,'City')
							city.text = cliente_endereco.city


						if cliente_endereco.pincode:
							postalcode = ET.SubElement(address,'PostalCode')
							postalcode.text = cliente_endereco.pincode

	
						if cliente_endereco.city:
							province = ET.SubElement(address,'Province')
							province.text = cliente_endereco.city

		
						if cliente_endereco.country:
							country = ET.SubElement(address,'Country')
							if cliente_endereco.country == 'Angola':
								country.text = "AO"
							else:
								country.text = cliente_endereco.country



				if cliente_endereco:
					if cliente_endereco.address_line1:
						shipfrom = ET.SubElement(stockmovement,'ShipFrom')
						#deliveryid = ET.SubElement(shipfrom,'DeliveryID')
						#deliverydate = ET.SubElement(shipfrom,'DeliveryDate')
						#warehouseid = ET.SubElement(shipfrom,'WarehouseID')
						#locationid = ET.SubElement(shipfrom,'LocationID')

						address = ET.SubElement(shipfrom,'Address')
						#buildingnumber = ET.SubElement(address,'BuildingNumber')
						streetname = ET.SubElement(address,'StreetName')
						streetname.text = cliente_endereco.address_line1

						addressdetail = ET.SubElement(address,'AddressDetail')
						#if cliente_endereco:
						addressdetail.text = cliente_endereco.address_line1


						if cliente_endereco.city:
							city = ET.SubElement(address,'City')
							city.text = cliente_endereco.city

	
						if cliente_endereco.pincode:
							postalcode = ET.SubElement(address,'PostalCode')
							postalcode.text = cliente_endereco.pincode

		
						if cliente_endereco.city:
							province = ET.SubElement(address,'Province')
							province.text = cliente_endereco.city

			
						if cliente_endereco.country:
							country = ET.SubElement(address,'Country')
							if cliente_endereco.country == 'Angola':
								country.text = "AO"
							else:
								country.text = cliente_endereco.country



				#movementendtime = ET.SubElement(stockmovement,'MovementEndTime')
				#movementstarttime = ET.SubElement(stockmovement,'MovementStartTime')
				#agtdoccodeid = ET.SubElement(stockmovement,'AGTDocCodeID')

				#Itens

				guiasremessaitems = frappe.db.sql(""" select * from `tabDelivery Note Item` where parent = %s order by idx """,(guiaremessa.name), as_dict=True)
				for guiaremessaitem in guiasremessaitems:
					line = ET.SubElement(stockmovement,'Line')

					linenumber = ET.SubElement(line,'LineNumber')
					linenumber.text = str(guiaremessaitem.idx)

					if guiaremessaitem.against_sales_order:
						orderreferences = ET.SubElement(line,'OrderReferences')
						originatingon = ET.SubElement(orderreferences,'OriginatingON')
						orderdate = ET.SubElement(orderreferences,'OrderDate')

						originatingon.text = guiaremessaitem.against_sales_order
						ordemvenda = frappe.db.sql(""" select * from `tabSales Order` where name = %s """,(guiaremessaitem.against_sales_order), as_dict=True)
						orderdate.text = ordemvenda[0].transaction_date.strftime("%Y-%m-%d")


					productcode = ET.SubElement(line,'ProductCode')
					productcode.text = guiaremessaitem.item_code

					productdescription = ET.SubElement(line,'ProductDescription')
					productdescription.text = guiaremessaitem.item_name.strip()

					quantity = ET.SubElement(line,'Quantity')

					quantity.text = str("{0:.0f}".format(guiaremessaitem.qty)) #str(guiaremessaitem.qty)

					unitofmeasure = ET.SubElement(line,'UnitOfMeasure')
					unitofmeasure.text = guiaremessaitem.uom

					unitprice = ET.SubElement(line,'UnitPrice')
					if guiaremessaitem.rate:
						unitprice.text = str("{0:.2f}".format(guiaremessaitem.rate))
					else:
						unitprice.text = "0.00"

					description = ET.SubElement(line,'Description')
					description.text = guiaremessaitem.description.strip()
					if guiaremessaitem.serial_no:
						productserialnumber = ET.SubElement(line,'ProductSerialNumber')
						serialnumber = ET.SubElement(productserialnumber,'SerialNumber')
						serialnumber.text = guiaremessaitem.serial_no

					#Sera que is o valor Valuation TAX or amount!!!
					#debitamount = ET.SubElement(line,'DebitAmount')
					#debitamount.text = "0.00"

					creditamount = ET.SubElement(line,'CreditAmount')
					#creditamount.text = "0.00"
					creditamount.text = str("{0:.2f}".format(guiaremessaitem.amount)) #str(guiaremessaitem.amount)

					#tax = ET.SubElement(line,'Tax')
					#taxtype = ET.SubElement(tax,'TaxType')
					#taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
					#taxcode = ET.SubElement(tax,'TaxCode')
					#taxpercentage = ET.SubElement(tax,'TaxPercentage')

					#IVA
					taxascharges =  frappe.db.sql(""" select * from `tabSales Taxes and Charges` where parenttype ='Delivery Note' and parent = %s """,(guiaremessa.name), as_dict=True)
				
					#entradasgliva =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='Delivery Note' and company = %s and voucher_no = %s """,(empresa.name,guiaremessa.name), as_dict=True)
					#if guiaremessa.name == 'DN-00004':
					#	print 'factura ', guiaremessa.name
					#	print entradasgliva
					#	return
				
					for taxacharge in taxascharges:
						print taxacharge.account

						if "3422" in taxacharge.account_head:	#34220000
							tax = ET.SubElement(line,'Tax')
							taxtype = ET.SubElement(tax,'TaxType')

							taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
							taxcountryregion.text = "AO"

							#IVA	ainda por rever
							#Aqui verifica se na ficha do ITEM diz que esta isento....
							taxtype.text = "IVA"
							taxcode = ET.SubElement(tax,'TaxCode')
							taxcode.text = "NOR"

						#else:
						#	taxtype.text = "NS"
						#	taxcode = ET.SubElement(tax,'TaxCode')
						#	taxcode.text = "NS"

							retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
							print retn


							taxpercentage = ET.SubElement(tax,'TaxPercentage')
							taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

							taxamount = ET.SubElement(tax,'TaxAmount')
							#if entradagl.credit:
							#	taxamount.text = str(entradagl.credit)
							#else:
							taxamount.text = "0.00"

				
					taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
					taxexemptionreason.text = "Regime Transitório"	#

					taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
					taxexemptioncode.text = "M00"


					#settlementamount = ET.SubElement(line,'SettlementAmount')

					#customsinformation
					#customsinformation = ET.SubElement(line,'CustomsInformation')
					#arcno = ET.SubElement(customsinformation,'ARCNo')
					#iecamount = ET.SubElement(customsinformation,'IECAmount')


				#documenttotals
				documenttotals = ET.SubElement(stockmovement,'DocumentTotals')
				taxpayable = ET.SubElement(documenttotals,'TaxPayable')
			
				print 'factura Referencia'
				if factura.docstatus != 2:
					salestaxescharges = frappe.db.sql(""" select * from `tabSales Taxes and Charges` where parent = %s """,(guiaremessa.name),as_dict=True)
					print salestaxescharges

					if salestaxescharges: 
						print salestaxescharges[0].tax_amount
						taxpayable.text = str("{0:.2f}".format(salestaxescharges[0].tax_amount)) #str(salestaxescharges[0].tax_amount) 		#por ir buscar 
					else:
						taxpayable.text = "0.00" 		#por ir buscar 
				#if retencao.credit_in_account_currency:
				#	taxpayable.text = str(retencao.credit_in_account_currency) 		#por ir buscar 

				nettotal = ET.SubElement(documenttotals,'NetTotal')
				nettotal.text = str("{0:.2f}".format(factura.net_total)) #str(factura.net_total)		#Sem Impostos Total Factura

				grosstotal = ET.SubElement(documenttotals,'GrossTotal')
				if factura.rounded_total:
					grosstotal.text = str("{0:.2f}".format(guiaremessa.rounded_total)) #str(factura.rounded_total)		#Total Factura + impostos.... por ir buscar
				else:
					grosstotal.text = "0.00"


				#currency if NOT AOA
				if guiaremessa.currency != "KZ":
					currency = ET.SubElement(documenttotals,'Currency')
					currencycode = ET.SubElement(currency,'CurrencyCode')

					currencycode.text = str(guiaremessa.currency)

					currencyamount = ET.SubElement(currency,'CurrencyAmount')
					currencyamount.text = str("{0:.2f}".format(guiaremessa.rounded_total))

					exchangerate = ET.SubElement(currency,'ExchangeRate')
					exchangerate.text = str("{0:.2f}".format(guiaremessa.conversion_rate))

				#currencyamount = ET.SubElement(currency,'CurrencyAmount')
				#exchangerate = ET.SubElement(currency,'ExchangeRate')


				#HASH key to generate	
				#Invoicedate + Sytementrydate + InvoiceNo + Grosstotal

				ficheirosha1  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".sha1"
				ficheirotxt  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt"
				ficheirob64  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".b64"


	
				hashfile.close()	#close previous ...

				hashcriado = open(ficheirob64,'rb')	#open the file created to HASH
				print 'Hash criado'
				chaveanterior = str(hashcriado.read())	#para usar no next record...

				movementofgoodshash.text = str(chaveanterior)	#Hash created
		
				hashcriado.close()

				fileregistocontador += 1	#contador para registo1, registo2 ....


		#		if fileregistocontador == 4:
		#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64))
		#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem /tmp/registo1.sha1 /tmp/registo1.txt /tmp/registo1.b64")  
		#			return	
		
				'''
				In case we need to generate Hash for all records on the APP ... this will be done when SAFT export required
				A table Angolaerp_hash must be created with 
					Documenttype, DocumentNumber, Hash, Hashcontrol or Hashversion

				'''
			#Deve no fim apagar todos os regis* criados ....
			os.system("rm /tmp/registo* ")	#execute



		#END OF MovementOfGoods



	#create WorkingDocuments...

	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "F" or ficheiro_tipo[0:1].upper() == "Q":

		#WorkingDocuments
		'''
			Campo Workdate, SystemEntryDate, DocumentNumber, GrossTotal, Last Hash from previous Doc.
		'''
		if sourcedocuments == None:
			sourcedocuments = ET.SubElement(data,'SourceDocuments')


		workingdocuments = ET.SubElement(sourcedocuments,'WorkingDocuments')

		numberofentries = ET.SubElement(workingdocuments,'NumberOfEntries')

		totaldebit = ET.SubElement(workingdocuments,'TotalDebit')


		#Debitos ou pagamentos
		facturas = frappe.db.sql(""" select count(name), sum(rounded_total) from `tabQuotation` where company = %s and docstatus <> 0 and transaction_date >= %s and transaction_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)


		print facturas
		print int(facturas[0]['count(name)'])


		##### POR FAZER
		totalcredit = ET.SubElement(workingdocuments,'TotalCredit')

		####### POR FAZER

		if int(facturas[0]['count(name)']) !=0:
			numberofentries.text = str(int(facturas[0]['count(name)']))
			totaldebit.text = str("{0:.2f}".format(int(facturas[0]['sum(rounded_total)'])))

		else:
			numberofentries.text = "0"
			totaldebit.text = "0.00"

		#Creditos ou devolucoes
		facturas = frappe.db.sql(""" select count(name), sum(rounded_total) from `tabQuotation` where company = %s and docstatus <> 0 and transaction_date >= %s and transaction_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)
		if int(facturas[0]['count(name)']) !=0:
			#totalcredit.text = str(int(facturas[0]['sum(rounded_total)']))
			if facturas[0]['sum(rounded_total)'] != 0:
				totalcredit.text = str("{0:.2f}".format(int(facturas[0]['sum(rounded_total)'])))
			else:
				totalcredit.text = "0.00"


		else:
			totalcredit.text = "0.00"


		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	

		'''
		Gera primeiro o HASH e depois o sistema pega os files e apaga....

		'''
		#invoice para HASH
		facturas = frappe.db.sql(""" select * from `tabQuotation` where company = %s and docstatus <> 0 and transaction_date >= %s and transaction_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		for factura in facturas:
			if chaveanterior == "":
				#1st record
				print 'primeiro registo'
				hashinfo = str(factura.transaction_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";"
			else:
				print 'segundo registo'
				print chaveanterior
				hashinfo = str(factura.transaction_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";" + str(chaveanterior)

			print fileregistocontador
			print str(factura.transaction_date.strftime("%Y-%m-%d"))
			print str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S"))
			print str(factura.name)

			print 'HASH do SALESINVOICE ', hashinfo
			hashfile = open("/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt","wb")
			hashfile.write(hashinfo)

			fileregistocontador += 1	#contador para registo1, registo2 ....

	#		if fileregistocontador == 240:	
	#			return

	#	return
		exists = os.path.isfile("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")
		if exists:
			os.system("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh") # /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64)) 
		else:
			os.system("~/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")

		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	



		#invoice
		facturas = frappe.db.sql(""" select * from `tabQuotation` where company = %s and docstatus <> 0 and transaction_date >= %s and transaction_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		for factura in facturas:
			print factura.name
			print factura.creation
			print factura.modified

			invoice = ET.SubElement(workingdocuments,'WorkDocument')

			invoiceno = ET.SubElement(invoice,'DocumentNumber')
			invoiceno.text = str(factura.name)

			#documentstatus
			documentstatus = ET.SubElement(invoice,'DocumentStatus')
			invoicestatus = ET.SubElement(documentstatus,'WorkStatus')
			if factura.status =="Paid" and factura.docstatus == 1:
				invoicestatus.text = "F"	#Facturado
			elif factura.status =="Cancelled" and factura.docstatus == 2:
				invoicestatus.text = "A"	#Anulado

			else:
				invoicestatus.text = "N"	#Normal


			invoicestatusdate = ET.SubElement(documentstatus,'WorkStatusDate')
			#Will be needed to add T between date and time!!!!!!!
			invoicestatusdate.text = factura.modified.strftime("%Y-%m-%dT%H:%M:%S")	#ultima change


			#Pode ser os Comments when deleted the Documents ....
			if factura.remarks != 'No Remarks' and factura.remarks != 'Sem Observações' and factura.remarks != None:
				reason = ET.SubElement(documentstatus,'Reason')
				reason.text = factura.remarks
			elif factura._comments != None:
				reason = ET.SubElement(documentstatus,'Reason')
				reason.text = factura._comments

			sourceid = ET.SubElement(documentstatus,'SourceID')
			#sourceid.text = factura.modified_by	#User
			#sourceid.text = str(factura.modified_by[0:factura.modified_by.find("@")])
			if factura.modified_by.find("@"):
				#sourceid.text = str(factura.modified_by[0:factura.modified_by.find("@")])
				print frappe.get_doc('User',factura.modified_by)
				utilizador = frappe.get_doc('User',factura.modified_by)
				sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

			else:
				sourceid.text = str(factura.modified_by[0:factura.modified_by.find("@")])


			sourcebilling = ET.SubElement(documentstatus,'SourceBilling')
			sourcebilling.text = "P"	#Default

			salesinvoicehash = ET.SubElement(invoice,'Hash')
			#salesinvoicehash.text = 0	#por rever...

			salesinvoicehashcontrol = ET.SubElement(invoice,'HashControl')
			#salesinvoicehashcontrol.text = "Nao validado pela AGT"	#default for now

			period = ET.SubElement(invoice,'Period')
			period.text = str(factura.transaction_date.strftime("%m"))	#str(factura.modified.month)	#last modified month

			invoicedate = ET.SubElement(invoice,'WorkDate')
			invoicedate.text = factura.transaction_date.strftime("%Y-%m-%d")	#posting date

			invoicetype = ET.SubElement(invoice,'WorkType')
			print 'NC ', factura.return_against
			#if factura.is_pos == 1:
			#	invoicetype.text = "FR"	#POS deve ser FR ou TV
			#elif factura.return_against != None:
			#	invoicetype.text = "NC"	#Retorno / Credit Note

			#else:
			invoicetype.text = "PF"	#default Proforma
			salesinvoicehashcontrol.text = "1" + "PF" + "D " + str(factura.name)  	#default ver 1 as per the certificate

			'''
			#specialRegimes
			specialregimes = ET.SubElement(invoice,'SpecialRegimes')
			selfbillingindicator = ET.SubElement(specialregimes,'SelfBillingIndicator')
			selfbillingindicator.text = "0"	#default 

			cashvatschemeindicator = ET.SubElement(specialregimes,'CashVATSchemeIndicator')
			cashvatschemeindicator.text = "0"	#default 

			thirdpartiesbillingindicator = ET.SubElement(specialregimes,'ThirdPartiesBillingIndicator')
			thirdpartiesbillingindicator.text = "0"	#default 
			'''

			sourceid = ET.SubElement(invoice,'SourceID')
			#sourceid.text = factura.owner	#created by
			#sourceid.text = str(factura.owner[0:factura.owner.find("@")])
			if factura.owner.find("@"):
				#sourceid.text = str(factura.owner[0:factura.owner.find("@")])
				print frappe.get_doc('User',factura.owner)
				utilizador = frappe.get_doc('User',factura.owner)
				sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

			else:
				sourceid.text = str(factura.owner[0:factura.owner.find("@")])


			#eaccode = ET.SubElement(invoice,'EACCode')

			systementrydate = ET.SubElement(invoice,'SystemEntryDate')
			systementrydate.text = factura.creation.strftime("%Y-%m-%dT%H:%M:%S")	#creation date

			#transactions = ET.SubElement(invoice,'Transactions')
			transactionid = ET.SubElement(invoice,'TransactionID')
			#transactionid.text = entradagl.name	#entrada GL;single invoice can generate more than 2GL

			'''
			entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='sales invoice' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)
			if entradasgl:
				for entradagl in entradasgl:
					print 'transactions ids'
					print entradagl
					transactionid = ET.SubElement(transactions,'TransactionID')
					transactionid.text = entradagl.name	#entrada GL;single invoice can generate more than 2GL
			'''
			customerid = ET.SubElement(invoice,'CustomerID')
			customerid.text = factura.customer	#cliente

			'''
			#shipto
			shipto = ET.SubElement(invoice,'ShipTo')
			deliveryid = ET.SubElement(shipto,'DeliveryID')
			deliverydate = ET.SubElement(shipto,'DeliveryDate')
			warehouseid = ET.SubElement(shipto,'WarehouseID')
			locationid = ET.SubElement(shipto,'LocationID')
			#address
			address = ET.SubElement(shipto,'Address')	
			buildingnumber = ET.SubElement(address,'BuildingNumber')
			streetname = ET.SubElement(address,'StreetName')
			addressdetail = ET.SubElement(address,'AddressDetail')
			city = ET.SubElement(address,'City')
			postalcode = ET.SubElement(address,'PostalCode')
			province = ET.SubElement(address,'Province')
			country = ET.SubElement(address,'Country')
			#shipfrom
			shipfrom = ET.SubElement(invoice,'ShipFrom')
			deliveryid = ET.SubElement(shipfrom,'DeliveryID')
			deliverydate = ET.SubElement(shipfrom,'DeliveryDate')
			warehouseid = ET.SubElement(shipfrom,'WarehouseID')
			locationid = ET.SubElement(shipfrom,'LocationID')
			#address
			address = ET.SubElement(shipfrom,'Address')
			buildingnumber = ET.SubElement(address,'BuildingNumber')
			streetname = ET.SubElement(address,'StreetName')
			addressdetail = ET.SubElement(address,'AddressDetail')
			city = ET.SubElement(address,'City')
			postalcode = ET.SubElement(address,'PostalCode')
			province = ET.SubElement(address,'Province')
			country = ET.SubElement(address,'Country')

			movementendtime = ET.SubElement(invoice,'MovementEndTime')
			movementstarttime = ET.SubElement(invoice,'MovementStartTime')
			'''

			#line
			line = ET.SubElement(invoice,'Line')
			facturaitems = frappe.db.sql(""" select * from `tabQuotation Item` where parent = %s order by idx """,(factura.name), as_dict=True)
		
			for facturaitem in facturaitems:

				linenumber = ET.SubElement(line,'LineNumber')
				linenumber.text = str(facturaitem.idx)

				#Quotation has no SO 
				#orderreferences
				#orderreferences = ET.SubElement(line,'OrderReferences')
				#originatingon = ET.SubElement(orderreferences,'OriginatingON')
				#orderdate = ET.SubElement(orderreferences,'OrderDate')
				#if facturaitem.sales_order:
				#	originatingon.text = facturaitem.sales_order
				#	ordemvenda = frappe.db.sql(""" select * from `tabSales Order` where name = %s """,(facturaitem.sales_order), as_dict=True)
				#	orderdate.text = ordemvenda[0].transaction_date.strftime("%Y-%m-%d")



				productcode = ET.SubElement(line,'ProductCode')
				productcode.text = facturaitem.item_code

				productdescription = ET.SubElement(line,'ProductDescription')
				productdescription.text = facturaitem.item_name.strip()

				quantity = ET.SubElement(line,'Quantity')
				quantity.text = str("{0:.0f}".format(facturaitem.qty)) #str(facturaitem.qty)


				UnitOfMeasure = ET.SubElement(line,'UnitOfMeasure')
				UnitOfMeasure.text = facturaitem.uom

				unitprice = ET.SubElement(line,'UnitPrice')
				if facturaitem.rate:
					unitprice.text = str("{0:.2f}".format(facturaitem.rate))
				else:
					unitprice.text = "0.00"

				taxbase = ET.SubElement(line,'TaxBase')
				if facturaitem.net_rate:
					taxbase.text = str("{0:.2f}".format(facturaitem.net_rate))
				else:
					taxbase.text = "0.00"


				dn = frappe.db.sql(""" select * from `tabDelivery Note` where name = %s """,(facturaitem.delivery_note), as_dict=True)
				print 'DNnnnn'
				print dn
				if dn:
					taxpointdate = ET.SubElement(line,'TaxPointDate')
					taxpointdate.text = dn[0].transaction_date.strftime("%Y-%m-%d")	#DN

				#Against .. in case of change or DN ?????
				#references
				if factura.return_against != None:
					references = ET.SubElement(line,'References')
					reference = ET.SubElement(references,'Reference')

					reference.text = factura.return_against

				#reason = ET.SubElement(references,'Reason')

				description = ET.SubElement(line,'Description')
				description.text = facturaitem.description.strip()

				#productserialnumber
				if facturaitem.serial_no:
					productserialnumber = ET.SubElement(line,'ProductSerialNumber')
					serialnumber = ET.SubElement(productserialnumber,'SerialNumber')
					serialnumber.text = facturaitem.serial_no

				###If invoice was cancelled or deleted should not add...!!!!!
				if factura.status !="Cancelled" and factura.docstatus != 2:
					#debitamount = ET.SubElement(line,'DebitAmount')


					creditamount = ET.SubElement(line,'CreditAmount')
					creditamount.text = str("{0:.2f}".format(facturaitem.amount)) #str(facturaitem.amount)
					#POR VER SE TEM....

				#tax
				taxes = ET.SubElement(line,'Taxes')
			
				### TAX por PRODUTO OU SERVICO

				#procura no recibo pelo IS
				#recibos = frappe.db.sql(""" select * from `tabPayment Entry` where parent = %s """,(factura.name), as_dict=True)
				recibosreferencias = frappe.db.sql(""" select * from `tabPayment Entry Reference` where reference_doctype = 'sales invoice' and docstatus = 1 and reference_name = %s """,(factura.name), as_dict=True)
				print 'recibos refenrecias'
				print factura.name
				print recibosreferencias
				

				if facturaitem.imposto_de_consumo:	#Caso tem IPC or IVA

					if recibosreferencias:
						recibos = frappe.db.sql(""" select * from `tabPayment Entry` where name = %s """,(recibosreferencias[0].parent), as_dict=True)
						print 'recibos'
						print recibosreferencias[0].parent
						print recibos

						entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibosreferencias[0].parent), as_dict=True)

						print 'entradasgl+++++'

						#print entradasgl
						#return


						if entradasgl:
							for entradagl in entradasgl:

								print entradagl.account
								print entradagl.credit_in_account_currency
								if "34210000" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#imposto de producao e consumo IPC
									taxtype.text = "NS"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NS"

									retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'ipc' """,as_dict=True)
									print retn


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									if entradagl.credit:
										taxamount.text = str(entradagl.credit)
									else:
										taxamount.text = "0.00"


								elif "34710000" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#imposto de selo
									taxtype.text = "IS"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NS"

									retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%selo' """,as_dict=True)
									print retn


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									if entradagl.credit:
										taxamount.text = str(entradagl.credit)
									else:
										taxamount.text = "0.00"


								elif "34140000" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#retencao na fonte
									taxtype.text = "NS"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NS"

									retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%fonte' """,as_dict=True)
									print retn


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									if entradagl.debit:
										taxamount.text = str(entradagl.debit)
									else:
										taxamount.text = "0.00"
	



								elif "IVA" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#IVA	ainda por rever
									taxtype.text = "IVA"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NOR"

								#else:
								#	taxtype.text = "NS"
								#	taxcode = ET.SubElement(tax,'TaxCode')
								#	taxcode.text = "NS"


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									if entradagl.credit:
										taxamount.text = str(entradagl.credit)
									else:
										taxamount.text = "0.00"

			
								#return			

				#IVA
				taxascharges =  frappe.db.sql(""" select * from `tabSales Taxes and Charges` where parenttype ='quotation' and parent = %s """,(factura.name), as_dict=True)

				#entradasgliva =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='quotation' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)
				print 'factura ', factura.name
				#print taxascharges
				#return
				for taxacharge in taxascharges:
					print taxacharge.account_head

					if "3422" in taxacharge.account_head:	#34220000
						tax = ET.SubElement(taxes,'Tax')
						taxtype = ET.SubElement(tax,'TaxType')

						taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
						taxcountryregion.text = "AO"

						#IVA	ainda por rever
						#Aqui verifica se na ficha do ITEM diz que esta isento....
						taxtype.text = "IVA"
						taxcode = ET.SubElement(tax,'TaxCode')
						taxcode.text = "NOR"

					#else:
					#	taxtype.text = "NS"
					#	taxcode = ET.SubElement(tax,'TaxCode')
					#	taxcode.text = "NS"

						retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
						print retn


						taxpercentage = ET.SubElement(tax,'TaxPercentage')
						taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

						taxamount = ET.SubElement(tax,'TaxAmount')
						#if entradagl.credit:
						#	taxamount.text = str(entradagl.credit)
						#else:
						taxamount.text = "0.00"

				taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
				taxexemptionreason.text = "Regime Transitório"	#

				taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
				taxexemptioncode.text = "M00"


				#settlementamount = ET.SubElement(line,'SettlementAmount')

				#customsinformation
				#customsinformation = ET.SubElement(line,'CustomsInformation')
				#arcno = ET.SubElement(customsinformation,'ARCNo')
				#iecamount = ET.SubElement(customsinformation,'IECAmount')



			#documenttotals
			documenttotals = ET.SubElement(invoice,'DocumentTotals')

			taxpayable = ET.SubElement(documenttotals,'TaxPayable')
			print 'factura Referencia'
			if factura.docstatus != 2:
				salestaxescharges = frappe.db.sql(""" select * from `tabSales Taxes and Charges` where parent = %s """,(factura.name),as_dict=True)
				print salestaxescharges

				if salestaxescharges: 
					print salestaxescharges[0].tax_amount
					taxpayable.text = str("{0:.2f}".format(salestaxescharges[0].tax_amount)) #str(salestaxescharges[0].tax_amount) 		#por ir buscar 
				else:
					taxpayable.text = "0.00" 		#por ir buscar 



			#if retencao.credit_in_account_currency:
			#	taxpayable.text = str(retencao.credit_in_account_currency) 		#por ir buscar 

			nettotal = ET.SubElement(documenttotals,'NetTotal')
			nettotal.text = str("{0:.2f}".format(factura.net_total)) #str(factura.net_total)		#Sem Impostos Total Factura

			grosstotal = ET.SubElement(documenttotals,'GrossTotal')
			if factura.rounded_total:
				grosstotal.text = str("{0:.2f}".format(factura.rounded_total)) #str(factura.rounded_total)		#Total Factura + impostos.... por ir buscar
			else:
				grosstotal.text = "0.00"

			####ONLY IF NOT AOA .... POR VERIFICAR
			#currency
			if factura.currency != "KZ":
				currency = ET.SubElement(documenttotals,'Currency')
				currencycode = ET.SubElement(currency,'CurrencyCode')

				currencycode.text = str(factura.currency)

				currencyamount = ET.SubElement(currency,'CurrencyAmount')
				currencyamount.text = str("{0:.2f}".format(factura.rounded_total))

				exchangerate = ET.SubElement(currency,'ExchangeRate')
				exchangerate.text = str("{0:.2f}".format(factura.conversion_rate))


			#currencyamount = ET.SubElement(currency,'CurrencyAmount')
			#currencyamount.text = str(factura.rounded_total)		#Total Factura + impostos.... por ir buscar

			#exchangerate = ET.SubElement(currency,'ExchangeRate')


			#HASH key to generate	
			#Invoicedate + Sytementrydate + InvoiceNo + Grosstotal

			ficheirosha1  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".sha1"
			ficheirotxt  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt"
			ficheirob64  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".b64"


	
			hashfile.close()	#close previous ...

			hashcriado = open(ficheirob64,'rb')	#open the file created to HASH
			print 'Hash criado'
			chaveanterior = str(hashcriado.read())	#para usar no next record...
			#verifica se tem HASH
			if factura.hash_erp:
				salesinvoicehash.text = str(factura.hash_erp)	#Hash created
			else:
				salesinvoicehash.text = str(chaveanterior)	#do System
		
			hashcriado.close()

			fileregistocontador += 1	#contador para registo1, registo2 ....


	#		if fileregistocontador == 4:
	#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64))
	#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem /tmp/registo1.sha1 /tmp/registo1.txt /tmp/registo1.b64")  
	#			return	
		
			'''
			In case we need to generate Hash for all records on the APP ... this will be done when SAFT export required
			A table Angolaerp_hash must be created with 
				Documenttype, DocumentNumber, Hash, Hashcontrol or Hashversion

			'''
		#Deve no fim apagar todos os regis* criados ....
		os.system("rm /tmp/registo* ")	#execute



	#### Purchase ORDER

	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "F" or ficheiro_tipo[0:1].upper() == "Q":

		#### Still need to update as Quotation already added numbers .... This should be the last to be ADDED for both Quotation and Purchase Order

		#numberofentries = ET.SubElement(workingdocuments,'NumberOfEntries')

		#totaldebit = ET.SubElement(workingdocuments,'TotalDebit')


		#Debitos ou pagamentos
		#facturas = frappe.db.sql(""" select count(name), sum(rounded_total) from `tabQuotation` where company = %s and (status = 'Paid' or status = 'Cancelled' ) and transaction_date >= %s and transaction_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)


		#print facturas
		#print int(facturas[0]['count(name)'])


		##### POR FAZER
		#totalcredit = ET.SubElement(workingdocuments,'TotalCredit')

		####### POR FAZER

		#if int(facturas[0]['count(name)']) !=0:
		#	numberofentries.text = str(int(facturas[0]['count(name)']))
		#	totaldebit.text = str(int(facturas[0]['sum(rounded_total)']))

		#Creditos ou devolucoes
		#facturas = frappe.db.sql(""" select count(name), sum(rounded_total) from `tabQuotation` where company = %s and (status = 'Return') and transaction_date >= %s and transaction_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)
		#if int(facturas[0]['count(name)']) !=0:
		#	totalcredit.text = str(int(facturas[0]['sum(rounded_total)']))


		'''
			PURCHASE ORDER
		'''


		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	

		'''
		Gera primeiro o HASH e depois o sistema pega os files e apaga....

		'''
		#invoice para HASH
		facturas = frappe.db.sql(""" select * from `tabPurchase Order` where company = %s and docstatus <> 0 and transaction_date >= %s and transaction_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		for factura in facturas:
			if chaveanterior == "":
				#1st record
				print 'primeiro registo'
				hashinfo = str(factura.transaction_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";"
			else:
				print 'segundo registo'
				print chaveanterior
				hashinfo = str(factura.transaction_date.strftime("%Y-%m-%d")) + ";" + str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S")) + ";" + str(factura.name) + ";" + str(factura.rounded_total) + ";" + str(chaveanterior)

			print fileregistocontador
			print str(factura.transaction_date.strftime("%Y-%m-%d"))
			print str(factura.creation.strftime("%Y-%m-%dT%H:%M:%S"))
			print str(factura.name)

			print 'HASH do SALESINVOICE ', hashinfo
			hashfile = open("/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt","wb")
			hashfile.write(hashinfo)

			fileregistocontador += 1	#contador para registo1, registo2 ....

	#		if fileregistocontador == 240:	
	#			return

	#	return
		exists = os.path.isfile("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")
		if exists:
			os.system("/home/frappe/frappe/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh") # /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64)) 
		else:
			os.system("~/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh")

		#Hash
		chaveanterior =""
		fileregisto = "registo"
		fileregistocontador = 1	




		#invoice
		facturas = frappe.db.sql(""" select * from `tabPurchase Order` where company = %s and docstatus <> 0 and transaction_date >= %s and transaction_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		print 'purchase orders'

		for factura in facturas:
			print factura.name
			print factura.creation
			print factura.modified

			invoice = ET.SubElement(workingdocuments,'WorkDocument')

			invoiceno = ET.SubElement(invoice,'DocumentNumber')
			invoiceno.text = str(factura.name)

			#documentstatus
			documentstatus = ET.SubElement(invoice,'DocumentStatus')
			invoicestatus = ET.SubElement(documentstatus,'WorkStatus')
			if factura.status =="Cancelled" and factura.docstatus == 2:
				invoicestatus.text = "A"	#Anulado

			else:
				invoicestatus.text = "N"	#Normal


			invoicestatusdate = ET.SubElement(documentstatus,'WorkStatusDate')
			#Will be needed to add T between date and time!!!!!!!
			invoicestatusdate.text = factura.modified.strftime("%Y-%m-%dT%H:%M:%S")	#ultima change


			#Pode ser os Comments when deleted the Documents ....
			if factura.remarks != 'No Remarks' and factura.remarks != 'Sem Observações' and factura.remarks != None:
				reason = ET.SubElement(documentstatus,'Reason')
				reason.text = factura.remarks
			elif factura._comments != None:
				reason = ET.SubElement(documentstatus,'Reason')
				reason.text = factura._comments

			sourceid = ET.SubElement(documentstatus,'SourceID')
			#sourceid.text = factura.modified_by	#User
			#sourceid.text = str(factura.modified_by[0:factura.modified_by.find("@")])
			if factura.modified_by.find("@"):
				#sourceid.text = str(factura.modified_by[0:factura.modified_by.find("@")])
				print frappe.get_doc('User',factura.modified_by)
				utilizador = frappe.get_doc('User',factura.modified_by)
				sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

			else:
				sourceid.text = str(factura.modified_by[0:factura.modified_by.find("@")])

			sourcebilling = ET.SubElement(documentstatus,'SourceBilling')
			sourcebilling.text = "P"	#Default

			salesinvoicehash = ET.SubElement(invoice,'Hash')
			#salesinvoicehash.text = 0	#por rever...

			salesinvoicehashcontrol = ET.SubElement(invoice,'HashControl')
			#salesinvoicehashcontrol.text = "Nao validado pela AGT"	#default for now

			period = ET.SubElement(invoice,'Period')
			period.text = str(factura.transaction_date.strftime("%m"))	#str(factura.modified.month)	#last modified month

			invoicedate = ET.SubElement(invoice,'WorkDate')
			invoicedate.text = factura.transaction_date.strftime("%Y-%m-%d")	#posting date

			invoicetype = ET.SubElement(invoice,'WorkType')
			print 'NC ', factura.return_against
			#if factura.is_pos == 1:
			#	invoicetype.text = "FR"	#POS deve ser FR ou TV
			#elif factura.return_against != None:
			#	invoicetype.text = "NC"	#Retorno / Credit Note

			#else:
			invoicetype.text = "PF"	#default Proforma
			salesinvoicehashcontrol.text = "1" + "PF" + "D " + str(factura.name)  	#default ver 1 as per the certificate

			'''
			#specialRegimes
			specialregimes = ET.SubElement(invoice,'SpecialRegimes')
			selfbillingindicator = ET.SubElement(specialregimes,'SelfBillingIndicator')
			selfbillingindicator.text = "0"	#default 

			cashvatschemeindicator = ET.SubElement(specialregimes,'CashVATSchemeIndicator')
			cashvatschemeindicator.text = "0"	#default 

			thirdpartiesbillingindicator = ET.SubElement(specialregimes,'ThirdPartiesBillingIndicator')
			thirdpartiesbillingindicator.text = "0"	#default 
			'''

			sourceid = ET.SubElement(invoice,'SourceID')
			#sourceid.text = factura.owner	#created by
			#sourceid.text = str(factura.owner[0:factura.owner.find("@")])
			if factura.owner.find("@"):
				#sourceid.text = str(factura.owner[0:factura.owner.find("@")])
				print frappe.get_doc('User',factura.owner)
				utilizador = frappe.get_doc('User',factura.owner)
				sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

			else:
				sourceid.text = str(factura.owner[0:factura.owner.find("@")])

			#eaccode = ET.SubElement(invoice,'EACCode')

			systementrydate = ET.SubElement(invoice,'SystemEntryDate')
			systementrydate.text = factura.creation.strftime("%Y-%m-%dT%H:%M:%S")	#creation date

			#transactions = ET.SubElement(invoice,'Transactions')
			transactionid = ET.SubElement(invoice,'TransactionID')
			#transactionid.text = entradagl.name	#entrada GL;single invoice can generate more than 2GL

			'''
			entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='sales invoice' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)
			if entradasgl:
				for entradagl in entradasgl:
					print 'transactions ids'
					print entradagl
					transactionid = ET.SubElement(transactions,'TransactionID')
					transactionid.text = entradagl.name	#entrada GL;single invoice can generate more than 2GL
			'''
			customerid = ET.SubElement(invoice,'CustomerID')
			customerid.text = factura.supplier	#cliente

			'''
			#shipto
			shipto = ET.SubElement(invoice,'ShipTo')
			deliveryid = ET.SubElement(shipto,'DeliveryID')
			deliverydate = ET.SubElement(shipto,'DeliveryDate')
			warehouseid = ET.SubElement(shipto,'WarehouseID')
			locationid = ET.SubElement(shipto,'LocationID')
			#address
			address = ET.SubElement(shipto,'Address')	
			buildingnumber = ET.SubElement(address,'BuildingNumber')
			streetname = ET.SubElement(address,'StreetName')
			addressdetail = ET.SubElement(address,'AddressDetail')
			city = ET.SubElement(address,'City')
			postalcode = ET.SubElement(address,'PostalCode')
			province = ET.SubElement(address,'Province')
			country = ET.SubElement(address,'Country')
			#shipfrom
			shipfrom = ET.SubElement(invoice,'ShipFrom')
			deliveryid = ET.SubElement(shipfrom,'DeliveryID')
			deliverydate = ET.SubElement(shipfrom,'DeliveryDate')
			warehouseid = ET.SubElement(shipfrom,'WarehouseID')
			locationid = ET.SubElement(shipfrom,'LocationID')
			#address
			address = ET.SubElement(shipfrom,'Address')
			buildingnumber = ET.SubElement(address,'BuildingNumber')
			streetname = ET.SubElement(address,'StreetName')
			addressdetail = ET.SubElement(address,'AddressDetail')
			city = ET.SubElement(address,'City')
			postalcode = ET.SubElement(address,'PostalCode')
			province = ET.SubElement(address,'Province')
			country = ET.SubElement(address,'Country')

			movementendtime = ET.SubElement(invoice,'MovementEndTime')
			movementstarttime = ET.SubElement(invoice,'MovementStartTime')
			'''

			#line
			line = ET.SubElement(invoice,'Line')
			facturaitems = frappe.db.sql(""" select * from `tabPurchase Order Item` where parent = %s order by idx """,(factura.name), as_dict=True)
		
			for facturaitem in facturaitems:

				linenumber = ET.SubElement(line,'LineNumber')
				linenumber.text = str(facturaitem.idx)

				#Quotation has no SO 
				#orderreferences
				if facturaitem.supplier_quotation:	#Pode ser ou tambem Material Request only...
					orderreferences = ET.SubElement(line,'OrderReferences')
					originatingon = ET.SubElement(orderreferences,'OriginatingON')
					orderdate = ET.SubElement(orderreferences,'OrderDate')

					originatingon.text = facturaitem.supplier_quotation
					ordemvenda = frappe.db.sql(""" select * from `tabSupplier Quotation` where name = %s """,(facturaitem.supplier_quotation), as_dict=True)
					orderdate.text = ordemvenda[0].transaction_date.strftime("%Y-%m-%d")
				elif facturaitem.material_request:	#Pode ser ou tambem Material Request only...
					orderreferences = ET.SubElement(line,'OrderReferences')
					originatingon = ET.SubElement(orderreferences,'OriginatingON')
					orderdate = ET.SubElement(orderreferences,'OrderDate')

					originatingon.text = facturaitem.material_request
					ordemvenda = frappe.db.sql(""" select * from `tabMaterial Request` where name = %s """,(facturaitem.material_request), as_dict=True)
					orderdate.text = ordemvenda[0].transaction_date.strftime("%Y-%m-%d")


				productcode = ET.SubElement(line,'ProductCode')
				productcode.text = facturaitem.item_code

				productdescription = ET.SubElement(line,'ProductDescription')
				productdescription.text = facturaitem.item_name.strip()

				quantity = ET.SubElement(line,'Quantity')
				quantity.text = str("{0:.0f}".format(facturaitem.qty)) #str(facturaitem.qty)


				UnitOfMeasure = ET.SubElement(line,'UnitOfMeasure')
				UnitOfMeasure.text = facturaitem.uom

				unitprice = ET.SubElement(line,'UnitPrice')
				if facturaitem.rate:
					unitprice.text = str("{0:.2f}".format(facturaitem.rate))
				else:
					unitprice.text = "0.00"

				taxbase = ET.SubElement(line,'TaxBase')
				if facturaitem.net_rate:
					taxbase.text = str("{0:.2f}".format(facturaitem.net_rate))
				else:
					taxbase.text = "0.00"


				dn = frappe.db.sql(""" select * from `tabDelivery Note` where name = %s """,(facturaitem.delivery_note), as_dict=True)
				print 'DNnnnn'
				print dn
				if dn:
					taxpointdate = ET.SubElement(line,'TaxPointDate')
					taxpointdate.text = dn[0].transaction_date.strftime("%Y-%m-%d")	#DN

				#Against .. in case of change or DN ?????
				#references
				if factura.return_against != None:
					references = ET.SubElement(line,'References')
					reference = ET.SubElement(references,'Reference')

					reference.text = factura.return_against

				#reason = ET.SubElement(references,'Reason')

				description = ET.SubElement(line,'Description')
				description.text = facturaitem.description.strip()

				#productserialnumber
				if facturaitem.serial_no:
					productserialnumber = ET.SubElement(line,'ProductSerialNumber')
					serialnumber = ET.SubElement(productserialnumber,'SerialNumber')
					serialnumber.text = facturaitem.serial_no

				###If invoice was cancelled or deleted should not add...!!!!!
				if factura.status !="Cancelled" and factura.docstatus != 2:
					#debitamount = ET.SubElement(line,'DebitAmount')


					creditamount = ET.SubElement(line,'CreditAmount')
					creditamount.text = str("{0:.2f}".format(facturaitem.amount)) #str(facturaitem.amount)
					#POR VER SE TEM....

				#tax
				taxes = ET.SubElement(line,'Taxes')
			
				### TAX por PRODUTO OU SERVICO

				#procura no recibo pelo IS
				#recibos = frappe.db.sql(""" select * from `tabPayment Entry` where parent = %s """,(factura.name), as_dict=True)
				recibosreferencias = frappe.db.sql(""" select * from `tabPayment Entry Reference` where reference_doctype = 'sales invoice' and docstatus = 1 and reference_name = %s """,(factura.name), as_dict=True)
				print 'recibos refenrecias'
				print factura.name
				print recibosreferencias
				#if factura.name == 'FT0029/18-1':
				#	print 'TEM IPC'
				#	print facturaitem.imposto_de_consumo
				

				if facturaitem.imposto_de_consumo:	#Caso tem IPC or IVA

					if recibosreferencias:
						recibos = frappe.db.sql(""" select * from `tabPayment Entry` where name = %s """,(recibosreferencias[0].parent), as_dict=True)
						print 'recibos'
						print recibosreferencias[0].parent
						print recibos

						entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibosreferencias[0].parent), as_dict=True)

						print 'entradasgl+++++'

						#print entradasgl
						#return


						if entradasgl:
							for entradagl in entradasgl:

								print entradagl.account
								print entradagl.credit_in_account_currency
								if "34210000" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#imposto de producao e consumo IPC
									taxtype.text = "NS"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NS"

									retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'ipc' """,as_dict=True)
									print retn


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									if entradagl.credit:
										taxamount.text = str(entradagl.credit)
									else:
										taxamount.text = "0.00"



								elif "34710000" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#imposto de selo
									taxtype.text = "IS"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NS"

									retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%selo' """,as_dict=True)
									print retn


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									if entradagl.credit:
										taxamount.text = str(entradagl.credit)
									else:
										taxamount.text = "0.00"



								elif "34140000" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#retencao na fonte
									taxtype.text = "NS"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NS"

									retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%fonte' """,as_dict=True)
									print retn


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									if entradagl.debit:
										taxamount.text = str(entradagl.debit)
									else:
										taxamount.text = "0.00"




								elif "IVA" in entradagl.account:
									tax = ET.SubElement(taxes,'Tax')
									taxtype = ET.SubElement(tax,'TaxType')

									taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
									taxcountryregion.text = "AO"

									#IVA	ainda por rever
									taxtype.text = "IVA"
									taxcode = ET.SubElement(tax,'TaxCode')
									taxcode.text = "NOR"

								#else:
								#	taxtype.text = "NS"
								#	taxcode = ET.SubElement(tax,'TaxCode')
								#	taxcode.text = "NS"


									taxpercentage = ET.SubElement(tax,'TaxPercentage')
									taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

									taxamount = ET.SubElement(tax,'TaxAmount')
									if entradagl.credit:
										taxamount.text = str(entradagl.credit)
									else:
										taxamount.text = "0.00"

			
								#return			

				#IVA
				taxascharges =  frappe.db.sql(""" select * from `tabPurchase Taxes and Charges` where parenttype ='purchase order' and parent = %s """,(factura.name), as_dict=True)

				#entradasgliva =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='sales invoice' and company = %s and voucher_no = %s """,(empresa.name,factura.name), as_dict=True)


				for taxacharge in taxascharges:
					print taxacharge.account_head

					if "3422" in taxacharge.account_head:	#34220000
						tax = ET.SubElement(taxes,'Tax')
						taxtype = ET.SubElement(tax,'TaxType')

						taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
						taxcountryregion.text = "AO"

						#IVA	ainda por rever
						#Aqui verifica se na ficha do ITEM diz que esta isento....
						taxtype.text = "IVA"
						taxcode = ET.SubElement(tax,'TaxCode')
						taxcode.text = "NOR"

					#else:
					#	taxtype.text = "NS"
					#	taxcode = ET.SubElement(tax,'TaxCode')
					#	taxcode.text = "NS"

						retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
						print retn


						taxpercentage = ET.SubElement(tax,'TaxPercentage')
						taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

						taxamount = ET.SubElement(tax,'TaxAmount')
						#if entradagl.credit:
						#	taxamount.text = str(entradagl.credit)
						#else:
						taxamount.text = "0.00"

				taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
				taxexemptionreason.text = "Regime Transitório"	#

				taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
				taxexemptioncode.text = "M00"


				#settlementamount = ET.SubElement(line,'SettlementAmount')

				#customsinformation
				#customsinformation = ET.SubElement(line,'CustomsInformation')
				#arcno = ET.SubElement(customsinformation,'ARCNo')
				#iecamount = ET.SubElement(customsinformation,'IECAmount')



			#documenttotals
			documenttotals = ET.SubElement(invoice,'DocumentTotals')

			taxpayable = ET.SubElement(documenttotals,'TaxPayable')
			print 'factura Referencia'
			if factura.docstatus != 2:
				salestaxescharges = frappe.db.sql(""" select * from `tabPurchase Taxes and Charges` where parent = %s """,(factura.name),as_dict=True)
				print salestaxescharges

				if salestaxescharges: 
					print salestaxescharges[0].tax_amount
					taxpayable.text = str("{0:.2f}".format(salestaxescharges[0].tax_amount)) #str(salestaxescharges[0].tax_amount) 		#por ir buscar 
				else:
					taxpayable.text = "0.00" 		#por ir buscar 



			#if retencao.credit_in_account_currency:
			#	taxpayable.text = str(retencao.credit_in_account_currency) 		#por ir buscar 

			nettotal = ET.SubElement(documenttotals,'NetTotal')
			nettotal.text = str("{0:.2f}".format(factura.net_total)) #str(factura.net_total)		#Sem Impostos Total Factura

			grosstotal = ET.SubElement(documenttotals,'GrossTotal')
			if factura.grand_total:
				grosstotal.text = str("{0:.2f}".format(factura.grand_total)) #str(factura.rounded_total)		#Total Factura + impostos.... por ir buscar
			else:
				grosstotal.text = "0.00"

			####ONLY IF NOT AOA .... POR VERIFICAR
			#currency
			if factura.currency != "KZ":
				currency = ET.SubElement(documenttotals,'Currency')
				currencycode = ET.SubElement(currency,'CurrencyCode')

				currencycode.text = str(factura.currency)

				currencyamount = ET.SubElement(currency,'CurrencyAmount')
				currencyamount.text = str("{0:.2f}".format(factura.rounded_total))

				exchangerate = ET.SubElement(currency,'ExchangeRate')
				exchangerate.text = str("{0:.2f}".format(factura.conversion_rate))


			#currencyamount = ET.SubElement(currency,'CurrencyAmount')
			#currencyamount.text = str(factura.rounded_total)		#Total Factura + impostos.... por ir buscar

			#exchangerate = ET.SubElement(currency,'ExchangeRate')



			#HASH key to generate	
			#Invoicedate + Sytementrydate + InvoiceNo + Grosstotal

			ficheirosha1  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".sha1"
			ficheirotxt  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt"
			ficheirob64  = "/tmp/" + str(fileregisto) + str(fileregistocontador) + ".b64"


	
			hashfile.close()	#close previous ...

			hashcriado = open(ficheirob64,'rb')	#open the file created to HASH
			print 'Hash criado'
			chaveanterior = str(hashcriado.read())	#para usar no next record...

			if factura.hash_erp:
				salesinvoicehash.text = str(factura.hash_erp)	#Hash created
			else:
				salesinvoicehash.text = str(chaveanterior)	#do System
		
			hashcriado.close()

			fileregistocontador += 1	#contador para registo1, registo2 ....


	#		if fileregistocontador == 4:
	#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem " + str(ficheirosha1) + " " + str(ficheirotxt) + " " + str(ficheirob64))
	#			os.system("/tmp/angolaerp.cert2/bb6.sh /tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem /tmp/registo1.sha1 /tmp/registo1.txt /tmp/registo1.b64")  
	#			return	
		
			'''
			In case we need to generate Hash for all records on the APP ... this will be done when SAFT export required
			A table Angolaerp_hash must be created with 
				Documenttype, DocumentNumber, Hash, Hashcontrol or Hashversion

			'''
		#Deve no fim apagar todos os regis* criados ....
		os.system("rm /tmp/registo* ")	#execute


		###END OF Purchase ORDER

	#END OF WORKINGDOCUMENTS

	
	if ficheiro_tipo[0:1].upper() == "I" or ficheiro_tipo[0:1].upper() == "F" or ficheiro_tipo[0:1].upper() == "R" or ficheiro_tipo[0:1].upper() == "Q":

		#create Payments

		#Payments
		if sourcedocuments == None:
			sourcedocuments = ET.SubElement(data,'SourceDocuments')

		payments = ET.SubElement(sourcedocuments,'Payments')

		#primeirodiames = '2019-03-01'
		#ultimodiames = '2019-03-01'

		pagamentos = frappe.db.sql(""" select count(name), sum(paid_amount) from `tabPayment Entry` where company = %s and docstatus <> 0 and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

		numberofentries = ET.SubElement(payments,'NumberOfEntries')
		numberofentries.text ="0"
		totaldebit = ET.SubElement(payments,'TotalDebit')
		totaldebit.text = "0.00"
		totalcredit = ET.SubElement(payments,'TotalCredit')
		totalcredit.text = "0.00"

		if int(pagamentos[0]['count(name)']) !=0:


			numberofentries.text = str(pagamentos[0]['count(name)'])


			totaldebit.text = str("{0:.2f}".format(pagamentos[0]['sum(paid_amount)'])) 



			pagamentos = frappe.db.sql(""" select * from `tabPayment Entry` where company = %s and docstatus <> 0 and posting_date >= %s and posting_date <= %s """,(empresa.name,primeirodiames,ultimodiames), as_dict=True)

			#payment

			for recibo in pagamentos:
				payment = ET.SubElement(payments,'Payment')
				paymentrefno = ET.SubElement(payment,'PaymentRefNo')
				paymentrefno.text = recibo.name

				period = ET.SubElement(payment,'Period')
				period.text = str(recibo.posting_date.strftime("%m"))	#str(recibo.modified.month)	#last modified month

				transactionid = ET.SubElement(payment,'TransactionID')
				#GLs created .... 
				entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibo.name), as_dict=True)

				print entradasgl
				if entradasgl:
					for entradagl in entradasgl:
						print entradagl.name
						transactionid.text = entradagl.name


				transactiondate = ET.SubElement(payment,'TransactionDate')
				transactiondate.text = recibo.posting_date.strftime("%Y-%m-%d")

				paymenttype = ET.SubElement(payment,'PaymentType')
				paymenttype.text = "RC"	#default SAFT

				if recibo.remarks != None:
					description = ET.SubElement(payment,'Description')
					description.text = recibo.remarks.strip()

				systemid = ET.SubElement(payment,'SystemID')
				systemid.text = recibo.name

				documentstatus = ET.SubElement(payment,'DocumentStatus')
				paymentstatus = ET.SubElement(documentstatus,'PaymentStatus')	
				if recibo.docstatus == 1:
					#pago
					paymentstatus.text = "N"
				elif recibo.docstatus == 2:
					#Canceled
					paymentstatus.text = "A"

				paymentstatusdate = ET.SubElement(documentstatus,'PaymentStatusDate')
				paymentstatusdate.text = recibo.modified.strftime("%Y-%m-%dT%H:%M:%S")

				#reason = ET.SubElement(documentstatus,'Reason')

				sourceid = ET.SubElement(documentstatus,'SourceID')
				#sourceid.text = recibo.owner
				#sourceid.text = str(recibo.owner[0:recibo.owner.find("@")])
				if recibo.owner.find("@"):
					#sourceid.text = str(recibo.owner[0:recibo.owner.find("@")])
					print frappe.get_doc('User',recibo.owner)
					utilizador = frappe.get_doc('User',recibo.owner)
					sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

				else:
					sourceid.text = str(recibo.owner[0:recibo.owner.find("@")])


				sourcepayment = ET.SubElement(documentstatus,'SourcePayment')
				sourcepayment.text = "P"	#default nossa APP

				paymentmethod = ET.SubElement(payment,'PaymentMethod')
				paymentmechanism = ET.SubElement(paymentmethod,'PaymentMechanism')
				modopagamento = frappe.get_doc("Mode of Payment",recibo.mode_of_payment)
				if modopagamento.type == "Cash" and ("TPA".upper() in modopagamento.mode_of_payment.upper() or "MULTICAIXA".upper() in modopagamento.mode_of_payment.upper()):
					paymentmechanism.text = "NU"

				elif modopagamento.type == "Bank" and "Cheque Bancário".upper() in modopagamento.mode_of_payment.upper():
					paymentmechanism.text = "CH"

				elif modopagamento.type == "Bank":
					paymentmechanism.text = "TB"

				elif modopagamento.type == "Cash":
					paymentmechanism.text = "NU"
				else:
					#did not found... search the Mode of payment TYPE
					modopagamento = frappe.get_doc("Mode of Payment",modopagamento.mode_of_payment)
					if modopagamento.type == 'Bank':
						paymentmechanism.text = "TB"
					elif modopagamento.type == 'Cash':
						paymentmechanism.text = "NU"


				#if "Transferência Bancária".upper() in recibo.mode_of_payment.upper():
				#	paymentmechanism.text = "TB"
				#elif "CASH".upper() in recibo.mode_of_payment.upper() or "monetário".upper() in recibo.mode_of_payment.upper():
				#	paymentmechanism.text = "NU"

				#elif "TPA".upper() in recibo.mode_of_payment.upper() or elif "MULTICAIXA".upper() in recibo.mode_of_payment.upper():					
				#	paymentmechanism.text = "CD"

				paymentamount = ET.SubElement(paymentmethod,'PaymentAmount')
				paymentamount.text = str("{0:.2f}".format(recibo.paid_amount)) #str(recibo.paid_amount) 

				paymentdate = ET.SubElement(paymentmethod,'PaymentDate')
				paymentdate.text = recibo.modified.strftime("%Y-%m-%d")

				sourceid = ET.SubElement(payment,'SourceID')
				#sourceid.text = recibo.owner
				#sourceid.text = str(recibo.owner[0:recibo.owner.find("@")])
				if recibo.owner.find("@"):
					#sourceid.text = str(recibo.owner[0:recibo.owner.find("@")])
					print frappe.get_doc('User',recibo.owner)
					utilizador = frappe.get_doc('User',recibo.owner)
					sourceid.text = str(utilizador.username)	#Retirar o Email only names... busca o username

				else:
					sourceid.text = str(recibo.owner[0:recibo.owner.find("@")])


				systementrydate = ET.SubElement(payment,'SystemEntryDate')
				systementrydate.text = recibo.posting_date.strftime("%Y-%m-%d")

				customerid = ET.SubElement(payment,'CustomerID')
				customerid.text = recibo.party


				#line
				recibosreferencias = frappe.db.sql(""" select * from `tabPayment Entry Reference` where parenttype = 'payment entry' and parent = %s order by idx """,(recibo.name), as_dict=True)

				print 'recibosreferencias'
				print recibosreferencias

				totaltaxaspagar = 0	#TaxPayable

				for reciboreferencia in recibosreferencias:
					line = ET.SubElement(payment,'Line')
					linenumber = ET.SubElement(line,'LineNumber')
					linenumber.text = str(reciboreferencia.idx)

					sourcedocumentid = ET.SubElement(line,'SourceDocumentID')
					originatingon = ET.SubElement(sourcedocumentid,'OriginatingON')
					originatingon.text = reciboreferencia.reference_name

					invoicedate = ET.SubElement(sourcedocumentid,'InvoiceDate')
					invoicedate.text = reciboreferencia.creation.strftime("%Y-%m-%dT%H:%M:%S")	#still need to know if should be postingdate from SL

					#description = ET.SubElement(sourcedocumentid,'Description')


					#procura no Sales Invoice 
					factura = frappe.db.sql(""" select * from `tabSales Invoice` where name = %s """,(reciboreferencia.reference_name), as_dict=True)
					if factura:
						if factura[0].discount_amount:
							settlementamount = ET.SubElement(line,'SettlementAmount')	#Desconto geral VALOR
							settlementamount.text = str(factura[0].discount_amount) 
	
					debitamount = ET.SubElement(line,'DebitAmount')
					debitamount.text = str("{0:.2f}".format(reciboreferencia.allocated_amount))
					#str(reciboreferencia.allocated_amount) 

					#creditamount = ET.SubElement(line,'CreditAmount')

					#tax
					#tax = ET.SubElement(line,'Tax')

					entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibo.name), as_dict=True)


					for entradagl in entradasgl:

						if "34710000" in entradagl.account:
							#imposto de selo
							tax = ET.SubElement(line,'Tax')
							taxtype = ET.SubElement(tax,'TaxType')

							taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
							taxcountryregion.text = "AO"

							taxtype.text = "IS"
							taxcode = ET.SubElement(tax,'TaxCode')
							taxcode.text = "ISE"

							retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%selo' """,as_dict=True)
							print retn


							taxpercentage = ET.SubElement(tax,'TaxPercentage')
							taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

							taxamount = ET.SubElement(tax,'TaxAmount')
							taxamount.text = "0.00"		 			#0 if percentagem exists

							taxexemptionreason = ET.SubElement(line,'TaxExemptionReason')
							taxexemptionreason.text = "Regime Transitório"

							taxexemptioncode = ET.SubElement(line,'TaxExemptionCode')
							taxexemptioncode.text = "M00"

						elif "IVA" in entradagl.account:
							#IVA	ainda por rever
							tax = ET.SubElement(line,'Tax')
							taxtype = ET.SubElement(tax,'TaxType')

							taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
							taxcountryregion.text = "AO"


							taxtype.text = "IVA"
							taxcode = ET.SubElement(tax,'TaxCode')
							taxcode.text = "NOR"

							taxpercentage = ET.SubElement(tax,'TaxPercentage')
							taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

							taxamount = ET.SubElement(tax,'TaxAmount')
							if entradagl.credit:
								taxamount.text = str(entradagl.credit)
							else:
								taxamount.text = "0.00"



						'''
						elif "34210000" in entradagl.account:
							#imposto de producao e consumo IPC
							tax = ET.SubElement(line,'Tax')

							taxtype = ET.SubElement(tax,'TaxType')

							taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
							taxcountryregion.text = "AO"

							taxtype.text = "NS"
							taxcode = ET.SubElement(tax,'TaxCode')
							taxcode.text = "NS"

							retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'ipc' """,as_dict=True)
							print retn


							taxpercentage = ET.SubElement(tax,'TaxPercentage')
							taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

							taxamount = ET.SubElement(tax,'TaxAmount')
							taxamount.text = str(entradagl.credit) 		


					
						elif "34140000" in entradagl.account:
							#retencao na fonte
							tax = ET.SubElement(line,'Tax')
							taxtype = ET.SubElement(tax,'TaxType')

							taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
							taxcountryregion.text = "AO"

							taxtype.text = "NS"
							taxcode = ET.SubElement(tax,'TaxCode')
							taxcode.text = "NS"

							retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  like '%%fonte' """,as_dict=True)
							print retn


							taxpercentage = ET.SubElement(tax,'TaxPercentage')
							taxpercentage.text = str(retn[0].percentagem)		#por ir buscar

							taxamount = ET.SubElement(tax,'TaxAmount')
							taxamount.text = str(entradagl.debit) 		

						'''


						#else:
						#	taxtype.text = "NS"
						#	taxcode = ET.SubElement(tax,'TaxCode')
						#	taxcode.text = "NS"

					#IVA
					entradasgliva =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='sales invoice' and company = %s and voucher_no = %s """,(empresa.name,recibo.name), as_dict=True)
					print 'factura ', recibo.name
					#print entradasgliva
					for entradaglinva in entradasgliva:
						print entradaglinva.account

						if "3422" in entradaglinva.account:	#34220000
							tax = ET.SubElement(taxes,'Tax')
							taxtype = ET.SubElement(tax,'TaxType')

							taxcountryregion = ET.SubElement(tax,'TaxCountryRegion')
							taxcountryregion.text = "AO"

							#IVA	ainda por rever
							#Aqui verifica se na ficha do ITEM diz que esta isento....
							taxtype.text = "IVA"
							taxcode = ET.SubElement(tax,'TaxCode')
							taxcode.text = "NOR"

						#else:
						#	taxtype.text = "NS"
						#	taxcode = ET.SubElement(tax,'TaxCode')
						#	taxcode.text = "NS"

							retn = frappe.db.sql(""" select * from `tabRetencoes` where docstatus = 0 and name  = 'iva' """,as_dict=True)
							print retn


							taxpercentage = ET.SubElement(tax,'TaxPercentage')
							taxpercentage.text = str("{0:.0f}".format(retn[0].percentagem)) #str(retn[0].percentagem)		#por ir buscar

							taxamount = ET.SubElement(tax,'TaxAmount')
							#if entradagl.credit:
							#	taxamount.text = str(entradagl.credit)
							#else:
							taxamount.text = "0.00"
			

				#documenttotals
				documenttotals = ET.SubElement(payment,'DocumentTotals')
	
				taxpayable = ET.SubElement(documenttotals,'TaxPayable')
				print 'Tax payable'
				pagamentotaxas = frappe.db.sql(""" select account,account_currency,debit,debit_in_account_currency,credit,credit_in_account_currency from `tabGL Entry` where company = %s and voucher_no = %s and account like %s """,(empresa.name,recibo.name,"34710000%"),as_dict=True)
				print pagamentotaxas
				#Ainda falta pegar o valor do IVA caso o mesmo tenha....
				if pagamentotaxas: 
					#print pagamentotaxas[0].amount
					if recibo.paid_to_account_currency !="KZ":
						#Eur, USD ....
						taxpayable.text = str("{0:.2f}".format(pagamentotaxas[0].credit_in_account_currency)) #str(entradagl.credit)
					else:
						taxpayable.text = str("{0:.2f}".format(pagamentotaxas[0].credit)) #str(entradagl.credit)	 	 
				else:
					taxpayable.text = "0.00" 		#por ir buscar 


				#Should it get from Each invoice the NETtotal and GrossTotal and do SUM
				nettotal = ET.SubElement(documenttotals,'NetTotal')
				nettotal.text = str("{0:.2f}".format(recibo.paid_amount)) #str(recibo.paid_amount)	#Paid amount...

				pagamentofinal = frappe.db.sql(""" select sum(debit), sum(debit_in_account_currency) from `tabGL Entry` where company = %s and voucher_no = %s """,(empresa.name,recibo.name), as_dict=True)
				if pagamentofinal[0]['sum(debit_in_account_currency)'] != None:
					print pagamentofinal[0]['sum(debit_in_account_currency)'] == None
					grosstotal = ET.SubElement(documenttotals,'GrossTotal')
			
					if recibo.paid_to_account_currency != "KZ":
						grosstotal.text = str("{0:.2f}".format(pagamentofinal[0]['sum(debit_in_account_currency)'])) #str(pagamentofinal[0]['sum(debit)'])	#Total Allocated Amount
					else:
						grosstotal.text = str("{0:.2f}".format(pagamentofinal[0]['sum(debit)'])) #str(pagamentofinal[0]['sum(debit)'])	#Total Allocated Amount

				#settlement
				#settlement = ET.SubElement(documenttotals,'Settlement')
				#settlementamount = ET.SubElement(settlement,'SettlementAmount')

				#currency
				if recibo.paid_to_account_currency != "KZ":
					currency = ET.SubElement(documenttotals,'Currency')
					currencycode = ET.SubElement(currency,'CurrencyCode')

					currencycode.text = str(recibo.paid_to_account_currency)

					currencyamount = ET.SubElement(currency,'CurrencyAmount')
					currencyamount.text = str("{0:.2f}".format(recibo.paid_amount))

					exchangerate = ET.SubElement(currency,'ExchangeRate')
					exchangerate.text = str("{0:.2f}".format(recibo.source_exchange_rate))

				#currencyamount = ET.SubElement(currency,'CurrencyAmount')
				#exchangerate = ET.SubElement(currency,'ExchangeRate')

				#witholdingtax
				#withholdingtax = ET.SubElement(payment,'WithholdingTax')

				'''
				if pagamentotaxas: 

					entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibosreferencias[0].parent), as_dict=True)

					for entradagl in entradasgl:

						if "34710000" in entradagl.account:
							#imposto selo
							withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
							withholdingtaxtype.text = "IS"

							withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
							withholdingtaxdescription.text = entradagl.account

							withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
							withholdingtaxamount.text = str(entradagl.credit)



						elif "34120000" in entradagl.account:
							#imposto industrial
							withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
							withholdingtaxtype.text = "II"

							withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
							withholdingtaxdescription.text = entradagl.account

							withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
							withholdingtaxamount.text = str(entradagl.credit)

						elif "34310000" in entradagl.account:
							#IRT
							withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
							withholdingtaxtype.text = "IRT"

							withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
							withholdingtaxdescription.text = entradagl.account

							withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
							withholdingtaxamount.text = str(entradagl.debit)

				'''

				if pagamentotaxas:
				#entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,recibosreferencias[0].parent), as_dict=True)
					for reciboreferencia in recibosreferencias:
						print reciboreferencia
						entradasgl =  frappe.db.sql(""" select * from `tabGL Entry` where voucher_type ='payment entry' and company = %s and voucher_no = %s """,(empresa.name,reciboreferencia.parent), as_dict=True)
						#witholdingtax
						#withholdingtax = ET.SubElement(invoice,'WithholdingTax')

						print 'entradasgl'
						print entradasgl


						variasentradas = False
						if entradasgl:
							for entradagl in entradasgl:
								print 'conta ', entradagl.account
								if "34710000" in entradagl.account:
									#imposto selo
									if variasentradas == True:
										withholdingtax = ET.SubElement(payment,'WithholdingTax')

									withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
									withholdingtaxtype.text = "IS"

									withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
									#withholdingtaxdescription.text = entradagl.account.strip()
									if entradagl.account.find('-'):
										withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find('-')+1:len(entradagl.account)]).strip()
									else:
										withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find(' ')+1:len(entradagl.account)]).strip()


									withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
									withholdingtaxamount.text = str("{0:.2f}".format(entradagl.credit)) #str(entradagl.credit)

								elif "34120000" in entradagl.account:
									#imposto industrial
									if variasentradas == True:
										withholdingtax = ET.SubElement(payment,'WithholdingTax')

									withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
									withholdingtaxtype.text = "II"

									withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
									#withholdingtaxdescription.text = entradagl.account.strip()
									if entradagl.account.find('-'):
										withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find('-')+1:len(entradagl.account)]).strip()
									else:
										withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find(' ')+1:len(entradagl.account)]).strip()

									withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
									withholdingtaxamount.text = str("{0:.2f}".format(entradagl.credit_in_account_currency)) #str(entradagl.credit_in_account_currency)

								elif "34310000" in entradagl.account:
									#IRT
									if variasentradas == True:
										withholdingtax = ET.SubElement(payment,'WithholdingTax')

									withholdingtaxtype = ET.SubElement(withholdingtax,'WithholdingTaxType')
									withholdingtaxtype.text = "IRT"

									withholdingtaxdescription = ET.SubElement(withholdingtax,'WithholdingTaxDescription')
									#withholdingtaxdescription.text = entradagl.account.strip()
									if entradagl.account.find('-'):
										withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find('-')+1:len(entradagl.account)]).strip()
									else:
										withholdingtaxdescription.text = str(entradagl.account[entradagl.account.find(' ')+1:len(entradagl.account)]).strip()


									withholdingtaxamount = ET.SubElement(withholdingtax,'WithholdingTaxAmount')
									withholdingtaxamount.text = str("{0:.2f}".format(entradagl.credit_in_account_currency)) #str(entradagl.credit_in_account_currency)

								variasentradas = True	#para garar varias entradas




		#END OF Payments



	###END PROCESSING 
	print 'Creating the File....'
	#record the data...	
	mydata = ET.tostring(data, 'utf-8')
	reparsed = minidom.parseString(mydata)
	

	#myfile = open("/tmp/" + nomeficheiro + ".xml","w")
	myfile = open(frappe.get_site_path('public','files') + "/" + nomeficheiro + ".xml","w")
	myfile.write(reparsed.toprettyxml(indent=" "))

	myfile.close()
	if usuario:
		print usuario
		print myfile.name[myfile.name.find('/files/'):len(myfile.name)]
		frappe.publish_realtime('msgprint', 'Terminou de processar SAFT-AO... <a href =' + myfile.name[myfile.name.find('/files/'):len(myfile.name)] + ">" + myfile.name[myfile.name.find('/files/'):len(myfile.name)] +"</a>", user=usuario)
	else:
		print "NAO TEM"
		print usuario

	print 'file created'
	print myfile.name
	if int(download_file) == 1:

		return myfile.name
		# write out response as a xlsx type
		#frappe.response['filename'] = myfile.name
		#frappe.response['filecontent'] = etree.parse(myfile) #minidom.parse(myfile)
		#frappe.response['type'] = 'binary'

	#END OF SAFT_AO
	



@frappe.whitelist()
def convert_csv_xml(ficheiro="csv_xml.csv", delimiter1 = None, site="http://127.0.0.1:8000"):

	#delimiter default , but added ;
	if delimiter1 == None:
		delimiter1 = str(u',').encode('utf-8') 
	if delimiter1 == ';':
		delimiter1 = str(u';').encode('utf-8') 	
	
	if not "tmp" in ficheiro:
		ficheiro = "/tmp/" + ficheiro	

	linhainicial = False
	colunas = []

	with open (ficheiro) as csvfile:
			readCSV = csv.reader(csvfile, delimiter = delimiter1)	

			for row in readCSV:
				if "DocType:" in row[0]:
					print row[1]	#Doctype name

				if "Column Name:" in row[0]:
					print len(row)	#Fields count
					for cols in row:	#Fields name print.
						print cols
						colunas.append(cols)
					#print row[1]	# 1st Fields...


				if linhainicial == True:	
					#Data starts here ....
#					print "Data starts here ...."
					for idx, cols in enumerate(row):
						#print idx
						#print cols
						print colunas[idx]
						print cols

				if "Start entering data below this line" in row[0]:
					print row
					linhainicial = True

			#testing ....
			convert_xml()



@frappe.whitelist()
def test_xs():
	from lxml import etree as ET
	from lxml.builder import ElementMaker

	NS_DC = "http://purl.org/dc/elements/1.1/"
	NS_OPF = "http://www.idpf.org/2007/opf"
	SCHEME = ET.QName(NS_OPF, 'scheme')
	FILE_AS = ET.QName(NS_OPF, "file-as")
	ROLE = ET.QName(NS_OPF, "role")
	opf = ElementMaker(namespace=NS_OPF, nsmap={"opf": NS_OPF, "dc": NS_DC})
	dc = ElementMaker(namespace=NS_DC)
#	validator = ET.RelaxNG(ET.parse("/tmp/opf-schema.xml"))

	tree = (
	    opf.package(
		{"unique-identifier": "uuid_id", "version": "2.0"},
		opf.metadata(
		    dc.identifier(
		        {SCHEME: "uuid", "id": "uuid_id"},
		        "d06a2234-67b4-40db-8f4a-136e52057101"),
		    dc.creator({FILE_AS: "Homes, A. M.", ROLE: "aut"}, "A. M. Homes"),
		    dc.title("My Book"),
		    dc.language("en"),
		),
		opf.manifest(
		    opf.item({"id": "foo", "href": "foo.pdf", "media-type": "foo"})
		),
		opf.spine(
		    {"toc": "uuid_id"},
		    opf.itemref({"idref": "uuid_id"}),
		),
		opf.guide(
		    opf.reference(
		        {"href": "cover.jpg", "title": "Cover", "type": "cover"})
		),
	    )
	)
#	validator.assertValid(tree)

	print(ET.tostring(tree, pretty_print=True).decode('utf-8'))


@frappe.whitelist()
def test_xsd():
	from lxml import etree
	from lxml.html import parse
	
	xxml = '/tmp/clientes.xml'
	for event, elem in ET.iterparse(xxml, events=('start','end','start-ns','end-ns')):

		print event
		print elem

@frappe.whitelist()
def validar_xml_xsd(xml_path, xsd_path):
	from lxml import etree

	xmlschema_doc = etree.parse(xsd_path)
	xmlschema = etree.XMLSchema(xmlschema_doc)

	xml_doc = etree.parse(xml_path)
	result = xmlschema.validate(xml_doc)

	print result




'''
@frappe.whitelist()
def verify_message(pem, msg, sig):
    f = open(pem,"r")
    pem1 = f.read()	
    cert = X509.load_cert(pem)	
    cert1 = X509.load_cert_string(pem1)
    pubkey = cert.get_pubkey()
    sig = sig.decode('base64')

    # Write a few files to disk for debugging purposes
    f = open("sig", "wb")
    f.write(sig)
    f.close()

#    f = open("msg", "w")
#    f.write(msg)
#    f.close()

    f = open("mypubkey.pem", "w")
    f.write(pubkey.get_rsa().as_pem())
    f.close()

    pubkey.reset_context(md='sha1')
    pubkey.verify_init()
    pubkey.verify_update(msg)
    return pubkey.verify_final(sig)

'''

@frappe.whitelist()
def assinar_ssl():


	datas = open("/tmp/registo1.txt","rb")
	data = datas.read()
	datas.close()
	#key_file = open("/tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem","rb")
	exists = os.path.isfile("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/angolaerp-selfsigned-priv.pem")
	if exists:
		key_file = open("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/angolaerp-selfsigned-priv.pem","rb")
	else:
		key_file = open("/tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem","rb")

	key = key_file.read()
#	key = key.encode('ascii')
	key_file.close()

	if key.startswith('-----BEGIN '):
		pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key)



	print data
	#data ='2019-04-24;2019-04-24T20:54:34;FAU-19/01516;1050.0;'
	message = _to_bytes(data, encoding='utf-8')
	sign = OpenSSL.crypto.sign(pkey, message, _to_bytes("sha1"))
	#print sign

	data_base64 = base64.b64encode(sign)
	print 'CODIGO xxxxxxx'
	print data_base64

@frappe.whitelist()
def assinar_ssl1(hashinfo):



	#key_file0 = open("/tmp/angolaerp.cert2/angolaerp-selfsigned-cert.pem","rb")
	exists = os.path.isfile("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/angolaerp-selfsigned-cert.pem")
	if exists:
		key_file0 = open("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/angolaerp-selfsigned-cert.pem","rb")
	else:
		key_file0 = open("/tmp/angolaerp.cert2/angolaerp-selfsigned-cert.pem","rb")
	key0 = key_file0.read()
#	key = key.encode('ascii')
	key_file0.close()


	#key_file = open("/tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem","rb")
	exists = os.path.isfile("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/angolaerp-selfsigned-priv.pem")
	if exists:
		key_file = open("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/angolaerp-selfsigned-priv.pem","rb")
	else:
		key_file = open("/tmp/angolaerp.cert2/angolaerp-selfsigned-priv.pem","rb")

	key = key_file.read()
#	key = key.encode('ascii')
	key_file.close()

	#key_file1 = open("/tmp/angolaerp.cert2/publickey.pem","rb")
	exists = os.path.isfile("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/publickey.pem")
	if exists:
		key_file1 = open("/home/frappe/frappe-bench/apps/angola_erp/angola_erp/util/publickey.pem","rb")
	else:
		key_file1 = open("/tmp/angolaerp.cert2/publickey.pem","rb")
	key1 = key_file1.read()

	key_file1.close()


	if key0.startswith('-----BEGIN '):	#cert
		pkey0 = crypto.load_certificate(crypto.FILETYPE_PEM, key0)

	if key.startswith('-----BEGIN '):
		pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key)

	if key1.startswith('-----BEGIN '):	#public
		pkey1 = crypto.load_publickey(crypto.FILETYPE_PEM, key1)



	#message = _to_bytes(hashinfo, encoding='utf-8')
	sign = OpenSSL.crypto.sign(pkey, hashinfo, _to_bytes("sha1"))
	#print sign

	data_base64 = base64.b64encode(sign)
	print 'CODIGO xxxxxxx'
	print data_base64

	print 'VERIFICAR CERTIFCATE......'
	verificar0 = OpenSSL.crypto.verify(pkey0,sign,hashinfo,_to_bytes("sha1"))
	if verificar0:
		print "CERTIFICATE VERIFICAO ERRADA"
	else:
		print "CERTIFICATE VERIFICAO OK"


	print 'VERIFICAR PUBLIC KEY......'
	x509 = OpenSSL.crypto.X509()
	x509.set_pubkey(pkey1)
	verificar1 = OpenSSL.crypto.verify(x509,sign,hashinfo,_to_bytes("sha1"))
	if verificar1:
		print "PUBLIC KEY VERIFICAO ERRADA"
	else:
		print "PUBLIC KEY VERIFICAO OK"

	return data_base64


'''
Eh9lq4L1+uw48J/Wf/dPVetijSFNimx0dQOI2b5huJyIoT0BMOG/kuxUFaNJ3wjZxd+UiI0Unclv1XgYzS9BKJ1PmxnxzZI7UKoKmP6XuUkBSDIvwiLmNYObvt3xrKYVVlAanZx3QRt+RsB7bA4tkR3Iz/oRlEGcUKzQpR8p2YM=
Eh9lq4L1+uw48J/Wf/dPVetijSFNimx0dQOI2b5huJyIoT0BMOG/kuxUFaNJ3wjZxd+UiI0Unclv1XgYzS9BKJ1PmxnxzZI7UKoKmP6XuUkBSDIvwiLmNYObvt3xrKYVVlAanZx3QRt+RsB7bA4tkR3Iz/oRlEGcUKzQpR8p2YM=
'''

'''

PEM = """-----BEGIN CERTIFICATE-----
MIICsDCCAhmgAwIBAgIJAJrZExFauz5pMA0GCSqGSIb3DQEBBQUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIEwpTb21lLVN0YXRlMSEwHwYDVQQKExhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMTMwMzA3MDkzNjQyWhcNMTgwMzA3MDkzNjQyWjBF
MQswCQYDVQQGEwJBVTETMBEGA1UECBMKU29tZS1TdGF0ZTEhMB8GA1UEChMYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKB
gQDRiW70Ea0CIrJmv9nwO0882mZ51ygAqQrQLfaYB2EUE5SRE99GaQbT9TsmcPK1
aG5ZDmazWRGBWe8UCL0W6fFrkg6Cb6VwFGqUSAsFhlT+XhOqAF9p3dfqu3S85zyY
7zJ5YIAMgDbd8/KmaqP8xn2aNY1cUxN/0HxOB4fz2/f/YQIDAQABo4GnMIGkMB0G
A1UdDgQWBBRj2EiZsFFFc4IbLHJa9CupE9ynbzB1BgNVHSMEbjBsgBRj2EiZsFFF
c4IbLHJa9CupE9ynb6FJpEcwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgTClNvbWUt
U3RhdGUxITAfBgNVBAoTGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZIIJAJrZExFa
uz5pMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEAip8XS5JX3hFG8wjZ
0FxqU/FLjSJkGrAscs16y7iq9YnUIfPt0Fha4a36vB5nG42vai10BtLgZEP/mifJ
DQXbDZA46G7gBiV9AvqtJWDNOfn7c34g23G9lxIEuU8ptLoyN+38TFdS+eWQDo/q
a/1IvCESUYYY43s+aOp6nbkDoGw=
-----END CERTIFICATE-----
"""

MSG = """
"""

SIG = """
FFOSR4UhPjheKN3hNAXIh/XL5OByp23+Gk+NRgonsZoI0eQHJn7nCEr/b1NbL/DP7UVL7o
nM6+RC1/yjiSi4J8wj4kqs19PY4ZGQXbnnDxutJoMfo+lhRA/H+jTPL5u8bs/d07ln0eHl
AzyOCxee3DRTxJKbmQewb48xhmou4jQ=
"""

'''
