# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import utils 
import datetime 
from frappe.model.naming import make_autoname
import frappe.async
from frappe.utils import cstr
from frappe import _

from lxml import html
import requests


@frappe.whitelist()
def cambios(fonte):

	if fonte == 'BNA':
		page=requests.get('http://www.bna.ao/Servicos/cambios_table.aspx?idl=1')
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
	
	if fonte == 'BFA':
		if page.status_code == 200:
			page= requests.get('http://www.bfa.ao/Servicos/Cambios/Divisas.aspx?idl=1')
			tree = html.fromstring(page.content)
			i = 2 
			for tr in tree.xpath("//tr"):	

				if tr.xpath('//*[@id="usd"]/text()')[0].strip()=='USD': 
					moeda= tr.xpath('//*[@id="usd"]/text()')[0].strip()     #moeda USD
					moedacompra= tr.xpath('//tr[4]/td[1]/text()')[0].strip()	#Compra
					moedavenda= tr.xpath('//tr[4]/td[2]/text()')[0].strip()    #Venda

			print moeda
			print moedacompra
			print moedavenda

	return moedacompra, moedavenda


