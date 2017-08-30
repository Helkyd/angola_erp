# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint

import angola_erp
from angola_erp.util.cambios import cambios
from angola_erp.util.angola import get_lista_retencoes
from angola_erp.util.angola import get_taxa_retencao
from angola_erp.util.angola import get_taxa_ipc


import erpnext

from frappe.utils import money_in_words, flt
from frappe.utils import cstr, getdate, date_diff
## from erpnext.setup.utils import get_company_currency
from num2words import num2words


def validate(doc,method):

	taxavenda= cambios("BNA")
	lista_retencoes = get_lista_retencoes()
	lista_retencao = get_taxa_retencao()
	lista_impostos = get_taxa_ipc()

	temretencao = False 
	temimpostoconsumo = False 
	retencaofonte =0
	retencaopercentagem =0
	totalpararetencao = 0
	totalgeralimpostoconsumo = 0
	totalgeralretencaofonte = 0
	totalbaseretencaofonte = 0
	retencaofonteDESC = ""
	totalservicos_retencaofonte =0
	totaldespesas_noretencaofonte =0

	
	
	ii=0

	for x in lista_retencoes:
		if x.descricao =='Retencao na Fonte':
			print ('pertagem ', x.percentagem)
			retencaopercentagem = x.percentagem

	for i in doc.get("items"):			

		prod = frappe.db.sql("""SELECT item_code,imposto_de_consumo,retencao_na_fonte FROM `tabItem` WHERE item_code = %s """, i.item_code , as_dict=True)
		if prod[0].imposto_de_consumo ==1:
			print ("IMPOSTO CONSUMO")
			if i.imposto_de_consumo == 0:
				i.imposto_de_consumo = (i.amount * 10) / 100
				
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

	#Calcula_despesas Ticked
	iii=0
	print ("Despesas")
	for ai in doc.get("taxes"):
		if ai.parent == doc.name and ai.charge_type !="":
			if ai.calcula_despesas:
				if totaldespesas_noretencaofonte ==0:
					#recalcula
					print ("RECALCULA")
					percentagem=ai.rate 
					for aii in doc.get("items"):
						if aii.parent == doc.name:
							prod = frappe.db.sql("""SELECT item_code,imposto_de_consumo,retencao_na_fonte FROM `tabItem` WHERE item_code = %s """, aii.item_code , as_dict=True)					

							#if (iii==0){iii=0}
							
							if prod[0].imposto_de_consumo == 1:

								if aii.imposto_de_consumo == 0:
									print ""
								
								if aii.retencao_na_fonte == 1:
										
									totalgeralretencaofonte +=  (aii.amount * retencaopercentagem) / 100
									totalbaseretencaofonte += aii.amount
									totalservicos_retencaofonte += totalbaseretencaofonte

								totalgeralimpostoconsumo += aii.imposto_de_consumo					


								despesas = (percentagem * totaldespesas_noretencaofonte)/100
								ai.charge_type="Actual"
								ai.tax_amount=despesas



				else:
					print ("CALCULA DESPESAS")
					despesas = (ai.rate * totaldespesas_noretencaofonte)/100

					ai.charge_type = "Actual"
					ai.tax_amount = despesas




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



