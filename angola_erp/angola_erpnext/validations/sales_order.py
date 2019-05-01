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

from frappe.utils import money_in_words, flt, cint
from frappe.utils import cstr, getdate, date_diff
## from erpnext.setup.utils import get_company_currency
from num2words import num2words

from erpnext.stock.get_item_details import get_batch_qty

####
# Helkyd modified 09-01-2019
####

def validate(doc,method):
	
	print "+VALIDAR SALES INVOICE+"
	print "+VALIDAR SALES INVOICE+"
	print "+VALIDAR SALES INVOICE+"
	print "+VALIDAR SALES INVOICE+"
	print "+VALIDAR SALES INVOICE+"

	taxavenda= cambios("BNA")
	lista_retencoes = get_lista_retencoes()
	lista_retencao = get_taxa_retencao()
	lista_impostos = get_taxa_ipc()

	lista_iva = get_taxa_iva()

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

	impostoselotransit = []
	totalimpostoselotrans = 0
	impostoselotranspercentagem = 0
	metadedovalor = False

	percentagem = 0
	
	
	ii=0

	numISelo = 0	#contador Imposto de Selo

	for x in lista_retencoes:
		if x.descricao =='Retencao na Fonte':
			print ('pertagem ', x.percentagem)
			retencaopercentagem = x.percentagem
		elif (x.descricao =='IPC') or (x.descricao =='Imposto de Consumo'):
			print ('IPC % ', x.percentagem)
			percentagem = x.percentagem
		elif ('Imposto de Selo' in x.descricao):

			print ('Imposto de Selo % ', x.percentagem)
			print (x.descricao)
			print ('metade '), x.metade_do_valor
			impostoselotransit.append([x.descricao, x.percentagem, x.metade_do_valor])

			#impostoselotranspercentagem = x.percentagem
			#if (x.metade_do_valor):
			#	metadedovalor = True	
		elif (x.descricao.upper() =='IVA'.upper()) or ("Imposto Valor Acrescentado".upper() == x.descricao.upper() or 'Acrescentado'.upper() in x.descricao.upper()):
			print ('IVA % ', x.percentagem)
			percentagem = x.percentagem





	for i in doc.get("items"):			
		if i.item_code != None:
			prod = frappe.db.sql("""SELECT item_code,imposto_de_consumo,retencao_na_fonte,imposto_de_selo,que_imposto_de_selo FROM `tabItem` WHERE item_code = %s """, i.item_code , as_dict=True)
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

			if prod[0].imposto_de_selo ==1:
				print ("IMPOSTO DE SELO TRANS")
				print ("IMPOSTO DE SELO TRANS")
				for x1 in impostoselotransit:
					print 'loop no imposto selo'
					print x1
					print x1[0]
					print x1[1]
					print x1[2]
					if x1[0] == prod[0].que_imposto_de_selo:
						print 'Imposto CORRETO!!!!!'
						print 'Imposto CORRETO!!!!!'
						print 'Imposto CORRETO!!!!!'

						if x1[2] == 1:	#metade do valor TRUE
							print 'METADE DO VALOR!!!'
							metadedovalor = True
						else:
							metadedovalor = False

						impostoselotranspercentagem = x1[1]
						
						print (flt(i.amount) * x1[1])
						print ('Selo % ',((i.amount * impostoselotranspercentagem) / 100))
						break
				print 'continua....'
				print metadedovalor
				#i.retencao_na_fonte = (i.amount * retencaopercentagem) / 100
				if (metadedovalor):
					totalimpostoselotrans += ((i.amount/2) * impostoselotranspercentagem) / 100
					i.imposto_de_selo_trans = ((i.amount/2) * impostoselotranspercentagem) / 100
				else:
					totalimpostoselotrans += (i.amount * impostoselotranspercentagem) / 100
					i.imposto_de_selo_trans = (i.amount * impostoselotranspercentagem) / 100
				print totalimpostoselotrans


			totalgeralimpostoconsumo += i.imposto_de_consumo					
			totalgeralretencaofonte +=  i.retencao_na_fonte


			#Total Desconto Linha
			if i.margin_type == "Percentage":
				totaldescontos_linha += i.amount

	#Save retencao na INVoice 
	doc.total_retencao_na_fonte = totalgeralretencaofonte
	doc.base_retencao_fonte = totalbaseretencaofonte

	#Save Descontos linha
	doc.total_desconto_linha = totaldescontos_linha

	#Save Imposto de Selo Trans
	doc.total_imposto_selo_trans = totalimpostoselotrans

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
				ai.total = totalgeralimpostoconsumo + doc.net_total




	print "VALOR POR EXTENSO"

	print totalgeralimpostoconsumo

	#Save Total Taxes and Charges if IPC exists
	if totalgeralimpostoconsumo:
		doc.base_total_taxes_and_charges = totalgeralimpostoconsumo
		doc.total_taxes_and_charges = totalgeralimpostoconsumo
	
		doc.grand_total = totalgeralimpostoconsumo + doc.net_total
		doc.rounded_total = doc.grand_total
		doc.base_grand_total = doc.grand_total
		doc.base_rounded_total = doc.grand_total
		doc.outstanding_amount = doc.grand_total

	company_currency = erpnext.get_company_currency(doc.company)
	print company_currency
	if (company_currency =='KZ'):
		doc.in_words = num2words(doc.rounded_total, lang='pt_BR').title() + ' Kwanzas.'
	else:
		doc.in_words = money_in_words(doc.rounded_total, company_currency)


def before_submit(doc,method):

	#Fees to be paid by Sales Invoice
	for prop_ in doc.get("propina"):
		frappe.db.set_value("Fees",prop_.propina, "sales_invoice", doc.name)
		#frappe.db.set_value("Fees",prop_.propina, "outstanding_amount", 0)
		frappe.db.commit()

