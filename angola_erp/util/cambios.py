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

from frappe.model.document import Document

from lxml import html
import requests

global actualizarqnd	#Should be everyday or Once per month
global actualizardia	#Select the day to update
global fontecambio	#BNA (default) or BFA	

@frappe.whitelist()
def cambios(fonte):

	if not fonte:
		frappe.throw("A fonte tem que ser BNA ou BFA.")


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
def update_cambios(fonte):
	#Re-done ...

	#Get the list of rates from BNA / BFA
	#Get list of Currency; if listed updates the rate
	tree=""
	mensagemretorno= ""
	bna_bfa=0 # for BNA and 1 for BFA	

	if not fonte:
		frappe.throw("A fonte tem que ser BNA ou BFA.")

	if fonte.upper() == 'BNA':
		bna_bfa=0
		try:
			page=requests.get('http://www.bna.ao/Servicos/cambios_table.aspx?idl=1')
			if page.status_code == 200:
				tree = html.fromstring(page.content)

		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0

	if fonte.upper() == 'BFA':
		bna_bfa=1
		try:
			page= requests.get('http://www.bfa.ao/Servicos/Cambios/Divisas.aspx?idl=1')
			if page.status_code == 200:
				tree = html.fromstring(page.content)

		except Exception, e:
			if frappe.message_log: frappe.message_log.pop()
			return 0,0

	#Espera resposta de dos dois sites...		
	if tree is not None: #page.status_code == 200:
		#tree = html.fromstring(page.content)

		bna_i = 2
		bfa_i = 1
		if bna_bfa==0:
			print "Banco para Cambiais BNA" 
		else:
			print "Banco para Cambiais BFA" 


		for tr in tree.xpath("//tr"):
			#BNA
			if bna_bfa==0:
				if tree.xpath('//tr['+ str(bna_i) + ']') != []:
					print "meoda BNA ", tr.xpath('//tr['+ str(bna_i) +']/td[1]/text()')[0]
					moeda= tr.xpath('//tr['+ str(bna_i) +']/td[1]/text()')[0]     #moeda 
					moedacompra= tr.xpath('//tr['+ str(bna_i) +']/td[2]/text()')[0]	#Compra
					moedavenda= tr.xpath('//tr['+ str(bna_i) +']/td[3]/text()')[0]    #Venda
					
				bna_i +=1
			#BFA
			if bna_bfa==1:
				moeda=""
				moedacompra =0
				moedavenda = 0
				for tt in tr.xpath('//tr['+ str(bfa_i) +']//*[@headers]/text()'):
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
							mensagemretorno= moeda + " Actualizacao feita hoje .... " + '\r' + '\n ' + mensagemretorno

	return mensagemretorno		
