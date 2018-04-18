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

from erpnext.stock.get_item_details import get_batch_qty

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
	totaldescontos_linha = 0

	percentagem = 0
	
	
	ii=0

	for x in lista_retencoes:
		if x.descricao =='Retencao na Fonte':
			print ('pertagem ', x.percentagem)
			retencaopercentagem = x.percentagem
		elif (x.descricao =='IPC') or (x.descricao =='Imposto de Consumo'):
			print ('IPC % ', x.percentagem)
			percentagem = x.percentagem


	for i in doc.get("items"):			
		if i.item_code != None:
			prod = frappe.db.sql("""SELECT item_code,imposto_de_consumo,retencao_na_fonte FROM `tabItem` WHERE item_code = %s """, i.item_code , as_dict=True)
			if prod[0].imposto_de_consumo ==1:
				print ("IMPOSTO CONSUMO")
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

			#BATCH Qty 
			if i.warehouse and i.item_code and i.batch_no:
				print 'BATCH NO verifica a QTD'
				print i.batch_no
				print i.warehouse
				print i.item_code
				print ('qtd atual ', i.actual_qty)
				print get_batch_qty(i.batch_no,i.warehouse,i.item_code)['actual_batch_qty']
				#print get_batch_qty(i.warehouse,i.item_code)['actual_batch_qty']
				#for xx in get_batch_qty(i.batch_no,i.warehouse,i.item_code)['actual_batch_qty']:
				#	print "LISTA BATCHES....."
				#	print xx

				i.actual_batch_qty = get_batch_qty(i.batch_no,i.warehouse,i.item_code)['actual_batch_qty']
				if i.actual_qty == 0:
					print 'ACTUAL QTY ZEROOOOOOOO'
					i.actual_qty = get_batch_qty(i.batch_no,i.warehouse,i.item_code)['actual_batch_qty']

	
			#Total Desconto Linha
			if i.margin_type == "Percentage":
				totaldescontos_linha += i.amount

	#Save retencao na INVoice 
	doc.total_retencao_na_fonte = totalgeralretencaofonte
	doc.base_retencao_fonte = totalbaseretencaofonte

	#Save Descontos linha
	doc.total_desconto_linha = totaldescontos_linha

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
								print percentagem
								print totaldespesas_noretencaofonte
								print despesas
								print totalgeralimpostoconsumo
								print ai.account_head

								ai.charge_type="Actual"
								#ai.tax_amount=despesas
								ai.tax_amount = despesas #totalgeralimpostoconsumo 
							else:
								ai.tax_amount = 0




				else:
					print ("CALCULA DESPESAS")
					if (ai.rate == 0) and (percentagem == 0) :
						percentagem = 5
					else:
						percentagem = ai.rate

					despesas = (ai.rate * totaldespesas_noretencaofonte)/100

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
			else:
				print "SEM DESPESAS MAS CALCULA IPC"
				print "SEM DESPESAS MAS CALCULA IPC"
				ai.charge_type = "Actual"
				ai.tax_amount = totalgeralimpostoconsumo




	print "VALOR POR EXTENSO"

	company_currency = erpnext.get_company_currency(doc.company)
	print company_currency
	if (company_currency =='KZ'):
		doc.in_words = num2words(doc.rounded_total, lang='pt_BR').title() + ' Kwanzas.'
	else:
		doc.in_words = money_in_words(doc.rounded_total, company_currency)



