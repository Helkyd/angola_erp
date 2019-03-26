# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt

# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import frappe
from frappe import utils 
import datetime
from datetime import timedelta
from frappe.utils import get_datetime_str, formatdate, nowdate, getdate, cint
from frappe.model.naming import make_autoname
import frappe.async
from frappe.utils import cstr
from frappe import _
from frappe.model.naming import make_autoname
import frappe.async

from frappe.model.document import Document

from lxml import html
import requests

global actualizarqnd	#Should be everyday or Once per month
global actualizardia	#Select the day to update
global fontecambio	#BNA (default) or BFA	

@frappe.whitelist()
def cambios(fonte):

	if not fonte:
		frappe.throw("A fonte tem que ser BNA, BFA ou BIC.")

	#if no cambio on currency exchange continues otherwise use the already exchange rate
	temcambio = frappe.db.sql(""" select name,from_currency,to_currency,date,exchange_rate from `tabCurrency Exchange` where to_currency='kz' and from_currency='USD' and date=(select max(date) from `tabCurrency Exchange`) ;""",as_dict=True)

	print "Cambios - Cambios"
	print temcambio == []
	#print temcambio[0]['exchange_rate']
	if not temcambio == []:
		if not temcambio[0]['exchange_rate'] == None :
			moedacompra = 0
			moedavenda = temcambio[0]['exchange_rate']
			return moedacompra, moedavenda

	if fonte.upper() == 'BNA':
		try:
			page=requests.get('http://www.bna.ao/Servicos/cambios_table.aspx?idl=1')
		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0

		#print page
		if page.status_code == 200:
			tree = html.fromstring(page.content)

			i = 2
			for tr in tree.xpath("//tr"):
				#print tree.xpath('//tr['+ str(i) + ']') == []

				if tree.xpath('//tr['+ str(i) + ']') != []:
					print "meoda ", tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0]
					#print tr.xpath(tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0].strip()) == '  USD'
					if tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0] == 'USD': 
						moeda= tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0]     #moeda USD
						if (tree.xpath('//tr['+ str(i) +']/td[2]/text()') != []):
							moedacompra= tr.xpath('//tr['+ str(i) +']/td[2]/text()')[0]	#Compra
						else:
							moedacompra = 0
						if (tree.xpath('//tr['+ str(i) +']/td[3]/text()') != []):
							moedavenda= tr.xpath('//tr['+ str(i) +']/td[3]/text()')[0]    #Venda
						else:
							moedavenda = 0
					i += 1

			print moeda
			print moedacompra
			print moedavenda
			
			return moedacompra, moedavenda
	
	if fonte.upper() == 'BIC':
		try:
			page=requests.get('http://www.bancobic.ao/Servicos/Cambios/Cambios.aspx?ctype=D')
		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0

		#print page
		if page.status_code == 200:
			tree = html.fromstring(page.content)

			i = 2
			for tr in tree.xpath("//tr"):
				#print tree.xpath('//tr['+ str(i) + ']') == []

				if tree.xpath('//tr['+ str(i) + ']') != []:
					print "meoda ", tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0]
					#print tr.xpath(tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0].strip()) == '  USD'
					if tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0] == 'USD': 
						moeda= tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0]     #moeda USD
						moedacompra= tr.xpath('//tr['+ str(i) +']/td[2]/text()')[0]	#Compra
						moedavenda= tr.xpath('//tr['+ str(i) +']/td[3]/text()')[0]    #Venda
					i += 1

			print moeda
			print moedacompra
			print moedavenda
			
			return moedacompra, moedavenda

	if fonte.upper() == 'BFA':
		try:
			page= requests.get('http://www.bfa.ao/Servicos/Cambios/Divisas.aspx?idl=1')
		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0

		if page.status_code == 200:

			tree = html.fromstring(page.content)
			i = 1 
			moedacompraUSD = 0
			moedavendaUSD = 0
			for tr in tree.xpath("//tr"):	

				#print (tr.xpath('//tr['+ str(i) +']//*[@headers]/text()'))
				moeda=""
				moedacompra =0
				moedavenda = 0
				for tt in tr.xpath('//tr['+ str(i) +']//*[@headers]/text()'):
					print (tt.strip())
					if tt.strip()== 'USD':
						moeda = tt.strip()
					elif moeda== "":
						moeda = tt.strip()
					else:
						#Compra e Venda
						if moedacompra == 0:
							moedacompra = tt.strip()
							if moeda =='USD':
								moedacompraUSD = moedacompra
								#print ("dolares")

							print ("compra")
						elif moedavenda == 0:
							moedavenda = tt.strip()
							if moeda =='USD':
								moedavendaUSD = moedavenda
								#print ("dolares")

							print ("venda")
				
				i +=1
				print ("=============")	



			print moeda
			print moedacompra
			print moedavenda

			return moedacompraUSD, moedavendaUSD





@frappe.whitelist()
def atualizar_cambios():
	#This will run every day to update Cambios
	qnd_correrfonte = frappe.get_value('Atualizacao Cambios',None,'fonte_do_cambio')
	qnd_correr = frappe.get_value('Atualizacao Cambios',None,'atualizar_quando')
	qnd_correrdia = frappe.get_value('Atualizacao Cambios',None,'actualizar_dia_mes')

	diahoje = datetime.datetime.today()
	
	if (qnd_correrfonte == 'BNA') or (qnd_correrfonte == 'BFA') or (qnd_correrfonte == 'BIC'):
		print qnd_correrfonte, " selecionando"
		print qnd_correr
		print qnd_correrdia
		if qnd_correr == 'Todos os Dias':
			#executa o update
			mensagem = update_cambios(qnd_correrfonte)
		elif qnd_correr == 'Inicio de cada Mes':
			#verifica o dia ...

			if qnd_correrdia == diahoje.day:
				#executa o update
				mensagem = update_cambios(qnd_correrfonte)
			
	#return mensagem


@frappe.whitelist()
def update_cambios(fonte):
	#Re-done ...

	#Get the list of rates from BNA / BFA
	#Get list of Currency; if listed updates the rate
	tree=""
	mensagemretorno= ""
	bna_bfa=0 # for BNA and 1 for BFA 2 for BIC	

	if not fonte:
		frappe.throw("A fonte tem que ser BNA, BFA ou BIC.")

	if fonte.upper() == 'BNA':
		bna_bfa=0
		try:
			print "BNA sites !!!"
			page=requests.get('http://www.bna.ao/Servicos/cambios_table.aspx?idl=1')
			if page.status_code == 200:
				tree = html.fromstring(page.content)

		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0

	if fonte.upper() == 'BFA':
		bna_bfa=1
		try:
			print "BFA sites !!!"
			page= requests.get('http://www.bfa.ao/Servicos/Cambios/Divisas.aspx?idl=1')
			if page.status_code == 200:
				tree = html.fromstring(page.content)

		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0

	if fonte.upper() == 'BIC':
		bna_bfa=2
		try:
			print "BIC sites !!!"
			page= requests.get('http://www.bancobic.ao/Servicos/Cambios/Cambios.aspx?ctype=D')
			if page.status_code == 200:
				tree = html.fromstring(page.content)

		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0


	#Espera resposta de dos dois sites...	
	print "Ja tem resposta dos sites !!!"	
	if tree is not None: #page.status_code == 200:
		#tree = html.fromstring(page.content)

		bna_i = 2
		bfa_i = 1
		bic_i = 2
	
		if bna_bfa==0:
			print "Banco para Cambiais BNA" 
			fontecambio = "BNA"
		elif bna_bfa ==1: 

			print "Banco para Cambiais BFA" 
			fontecambio = "BFA"
		else:
			print "Banco para Cambiais BIC" 
			fontecambio = "BIC"

		for tr in tree.xpath("//tr"):
			#BNA
			if bna_bfa==0:
				if tree.xpath('//tr['+ str(bna_i) + ']') != []:
					print "moeda BNA ", tr.xpath('//tr['+ str(bna_i) +']/td[1]/text()')[0]

					moeda= tr.xpath('//tr['+ str(bna_i) +']/td[1]/text()')[0]     #moeda 

					if (tree.xpath('//tr['+ str(bna_i) +']/td[2]/text()') != []):
						moedacompra= tr.xpath('//tr['+ str(bna_i) +']/td[2]/text()')[0]	#Compra
					else:
						moedacompra= 0

					if (tree.xpath('//tr['+ str(bna_i) +']/td[3]/text()') != []):
						moedavenda= tr.xpath('//tr['+ str(bna_i) +']/td[3]/text()')[0]    #Venda
					else:
						moedavenda = 0

					
				bna_i +=1

			#BIC
			if bna_bfa==2:
				if tree.xpath('//tr['+ str(bic_i) + ']') != []:
					print "moeda BIC ", tr.xpath('//tr['+ str(bic_i) +']/td[1]/text()')[0]
					moeda= tr.xpath('//tr['+ str(bic_i) +']/td[1]/text()')[0]     #moeda 
					if (tree.xpath('//tr['+ str(bic_i) +']/td[2]/text()') != []):
						moedacompra= tr.xpath('//tr['+ str(bic_i) +']/td[2]/text()')[0]	#Compra
					else:
						moedacompra = 0

					if (tree.xpath('//tr['+ str(bic_i) +']/td[3]/text()') != []):
						moedavenda= tr.xpath('//tr['+ str(bic_i) +']/td[3]/text()')[0]    #Venda
					else:
						moedavenda = 0
					
				bic_i +=1

			#BFA
			if bna_bfa==1:
				moeda=""
				moedacompra =0
				moedavenda = 0
				for tt in tr.xpath('//tr['+ str(bfa_i) +']//*[@headers]/text()'):
					print 'BFA'
					print (tt.strip())
					if tt.strip()== 'USD':
						moeda = tt.strip()
					elif moeda== "":
						print 'nao tem nada'
						moeda = tt.strip()
					else:
						#Compra e Venda
						if moedacompra == 0:
							moedacompra = tt.strip()
							#if moeda =='USD':
							moedacompraUSD = moedacompra
								#print ("dolares")

							print ("compra")
						elif moedavenda == 0:
							moedavenda = tt.strip()
							#if moeda =='USD':
							moedavendaUSD = moedavenda
								#print ("dolares")

							print ("venda")
				
				bfa_i +=1
			print ("DONE =============")	
				
			#Geral

			cambios_ = frappe.db.sql(""" select name,from_currency,to_currency,max(date),exchange_rate from `tabCurrency Exchange` where to_currency='kz' and from_currency=%s ;""",(moeda),as_dict=True)

			print "moeda ", moeda
			print cambios_[0]['max(date)']
			print formatdate(get_datetime_str(frappe.utils.nowdate()),"YYY-MM-dd")
			print formatdate(cambios_[0]['max(date)'],"YYYY-MM-dd") == formatdate(get_datetime_str(frappe.utils.nowdate()),"YYY-MM-dd")


			if type(moedavenda) ==str:
				#BFA uses , instead of .
				moedavenda = moedavenda.replace(",",".")
				moedavenda = float(moedavenda)
			elif moedacompra ==0 and moedavenda == 0:
				#BIC or others with ,	
				print moedacompraUSD
				print moedavendaUSD
				moedavenda = moedavendaUSD
				moedacompra = moedacompraUSD
				print moedavenda, moedacompra
				print type(moedavenda)	
				moedavenda = moedavenda.replace(",",".")
			else:
				#something else
				print 'what to do !!!'	

			if (cambios_[0].to_currency != None):
	#						print "NAO Tem cambios "

	#					if (len(cambios_) >0):
				if formatdate(cambios_[0]['max(date)'],"YYYY-MM-dd") == formatdate(get_datetime_str(frappe.utils.nowdate()),"YYY-MM-dd"):
				#if (cambios_[-0].date == frappe.utils.nowdate()):
					print "Ja foi atualizado hoje ...."
					mensagemretorno= moeda + " Nao tem atualizacao hoje .... " + '\r' + '\n ' + mensagemretorno

				else:
					print "Tem cambios ", cambios_
					#Just add or should check if value changed...!!!

					for reg in cambios_:
						print " cambio ", reg.exchange_rate
						print " cambio ", moedavenda
						if (reg.exchange_rate <> moedavenda):	
							print "Cambios diferentes...."
							#add new record
							cambios_novo = frappe.get_doc({
								"doctype": "Currency Exchange",
								"from_currency": str(moeda),
								"to_currency": "KZ",
								"exchange_rate": moedavenda,
								"date": frappe.utils.nowdate()
								
								

	#										"name":'{0}-{1}-{2}'.format(formatdate(get_datetime_str(frappe.utils.nowdate()), "yyyy-MM-dd"),"USD", "KZ")


							})

							cambios_novo.insert()
							ddd = make_autoname(cambios_novo.name + '.###')
							frappe.db.sql("INSERT into tabCommunication  (name,docstatus,seen,unread_notification_sent,subject,reference_name,reference_doctype,sent_or_received,content,communication_type,creation,modified) values (%s,0,0,0,'Atualizacao do Cambio ',%s,'Currency Exchange','Sent', %s  ,'Comment',%s,%s) ",(ddd,cambios_novo.name,str(fontecambio),frappe.utils.now(),frappe.utils.now()))

							cambios_novo._comments = str(fontecambio) 

							cambios_novo.save()

							mensagemretorno= moeda + " Actualizacao feita hoje .... " + '\r' + '\n ' + mensagemretorno
							

	return mensagemretorno		





@frappe.whitelist()
def update_cambios_(fonte):

	# TO BE DELETED **************************

	#Get the list of rates from BNA / BFA
	#Get list of Currency; if listed updates the rate
	
	
	if not fonte:
		frappe.throw("A fonte tem que ser BNA ou BFA.")

	if fonte.upper() == 'BNA':
		try:
			page=requests.get('http://www.bna.ao/Servicos/cambios_table.aspx?idl=1')
		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0

	if fonte.upper() == 'BFA':
		try:
			page= requests.get('http://www.bfa.ao/Servicos/Cambios/Divisas.aspx?idl=1')
		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0

		#print page
	if page.status_code == 200:
		tree = html.fromstring(page.content)

		i = 2
		#BNA
		if fonte.upper() == 'BNA':
			for tr in tree.xpath("//tr"):
				#print tree.xpath('//tr['+ str(i) + ']') == []

				if tree.xpath('//tr['+ str(i) + ']') != []:
					print "meoda BNA ", tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0]
					#print tr.xpath(tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0].strip()) == '  USD'

					moeda= tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0]     #moeda 
					moedacompra= tr.xpath('//tr['+ str(i) +']/td[2]/text()')[0]	#Compra
					moedavenda= tr.xpath('//tr['+ str(i) +']/td[3]/text()')[0]    #Venda

					cambios_ = frappe.db.sql(""" select name,from_currency,to_currency,max(date),exchange_rate from `tabCurrency Exchange` where to_currency='kz' and from_currency=%s ;""",(moeda),as_dict=True)

					print "moeda ", moeda
					print cambios_[0]['max(date)']
					print formatdate(get_datetime_str(frappe.utils.nowdate()),"YYY-MM-dd")
					print formatdate(cambios_[0]['max(date)'],"YYYY-MM-dd") == formatdate(get_datetime_str(frappe.utils.nowdate()),"YYY-MM-dd")
					if (cambios_[0].to_currency != None):
#						print "NAO Tem cambios "

#					if (len(cambios_) >0):
						if formatdate(cambios_[0]['max(date)'],"YYYY-MM-dd") == formatdate(get_datetime_str(frappe.utils.nowdate()),"YYY-MM-dd"):
						#if (cambios_[-0].date == frappe.utils.nowdate()):
							print "Ja foi atualizado hoje ...."
						else:
							print "Tem cambios ", cambios_
							#Just add or should check if value changed...!!!

							for reg in cambios_:
								print " cambio ", reg.exchange_rate
								if (reg.exchange_rate <> moedavenda):	
									print "Cambios diferentes...."
									#add new record
									cambios_novo = frappe.get_doc({
										"doctype": "Currency Exchange",
										"from_currency": str(moeda),
										"to_currency": "KZ",
										"exchange_rate": moedavenda,
										"date": frappe.utils.nowdate()
#										"name":'{0}-{1}-{2}'.format(formatdate(get_datetime_str(frappe.utils.nowdate()), "yyyy-MM-dd"),"USD", "KZ")


									})

									cambios_novo.insert()

					

					if tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0] == 'USD': 
						moeda= tr.xpath('//tr['+ str(i) +']/td[1]/text()')[0]     #moeda USD
						moedacompra= tr.xpath('//tr['+ str(i) +']/td[2]/text()')[0]	#Compra
						moedavenda= tr.xpath('//tr['+ str(i) +']/td[3]/text()')[0]    #Venda
					i += 1

			print moeda
			print moedacompra
			print moedavenda
			
	#			return moedacompra, moedavenda
	

		if fonte.upper() == 'BFA':

			tree = html.fromstring(page.content)
			i = 1 
			moedacompraUSD = 0
			moedavendaUSD = 0
			for tr in tree.xpath("//tr"):	

				#print (tr.xpath('//tr['+ str(i) +']//*[@headers]/text()'))
				moeda=""
				moedacompra =0
				moedavenda = 0
				for tt in tr.xpath('//tr['+ str(i) +']//*[@headers]/text()'):
					print (tt.strip())
					if tt.strip()== 'USD':
						moeda = tt.strip()
					elif moeda== "":
						moeda = tt.strip()
					else:
						#Compra e Venda
						if moedacompra == 0:
							moedacompra = tt.strip()
							if moeda =='USD':
								moedacompraUSD = moedacompra
								#print ("dolares")

							print ("compra")
						elif moedavenda == 0:
							moedavenda = tt.strip()
							if moeda =='USD':
								moedavendaUSD = moedavenda
								#print ("dolares")

							print ("venda")
				
				i +=1
				print ("=============")	



			print moeda
			print moedacompra
			print moedavenda
			print "Actualizacao na tabela ainda por implementar ....."

#			return moedacompra, moedavenda


@frappe.whitelist()
def cambios_local(moeda):

	print("CAMBIOS....")
#	print(frappe.model.frappe.get_all('Currency Exchange',filters={'from_currency':moeda,'docstatus':0},fields=['from_currency','date','exchange_rate']))
	cambiolocal = frappe.model.frappe.get_all('Currency Exchange',filters={'from_currency':moeda,'docstatus':0,'date':frappe.utils.nowdate()},fields=['from_currency','date','exchange_rate'])

	print(cambiolocal)
	return cambiolocal
