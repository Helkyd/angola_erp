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
from datetime import datetime
import csv 
import json


@frappe.whitelist()
def add_jentry(empresa):

	if empresa is None:
		print "Nome da Empresa necessario"
		return
	else:
		#cost center
		centrocusto = frappe.get_list("Company",filters=[['name','like', empresa]],fields=['cost_center'])


	"""
		bench execute --args "['Company name']"  angola_erp.util.add_faturas.add_jentry
	"""
	print "Ficheiro journalentry_dev.csv deve estar no /TMP"
	print "Ficheiro extraido do Primavera"
	print "Ter a certeza de Order by Ano, Mes, Dia, NumDiario"
	print "Criar os Anos passados existentes no Ficheiro no ERPNext"
	
	print "Conta, ValorAlt, Descricao, Natureza, Datagravacao"
	print "Mudar o IP do Servidor"
	print "Mudar o Usuario e a Senha para Importar"
	
	




	conta = 0
	contas1 = {}
	contas2 = {}
	contasJV = []

	olddescricao = ""
	oldregistodia = "" #Dia
	olddiario = "" #Diario
	oldnumerodiario = "" #Numdiario
	
	registosalvo = False
	registoerro = False


	#VERIFICA SE AS CONTAS EXISTEM... Antes de voltar a processar novamente ...

	with open ('/tmp/journalentry_dev.csv') as csvfile:
		readCSV = csv.reader(csvfile)
		print "Lendo o ficheiro...Verificando Contas"

		text_file = open('/tmp/criarcontas.txt', "w")

		for row in readCSV:
			if "Conta" in row[0]:
				print 'Inicio'
			elif row[0] == "\xef\xbb\xbfConta":
				print 'ainda falta'
			else:

				if (len(row[0]) >1): #(row[0].strip() != "0"):
					if row[2] != 0 and int(row[2]) <= 12:

						conta = row[0]
						valoralt = row[1]
						descricao = row[10]
						natureza = row[12]
						datagravacao = datetime.strptime(row[34],'%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')



						registomes = row[2] #Mes
						registodia = row[3] #Dia
						diario = row[4] #Diario
						numerodiario = row[5] #Numdiario
						registoano = row[35] #Ano
			

						try:
							existe =  frappe.get_list("Account",filters=[['name', 'like',conta + '%']],fields=['name','company'])
							print "CONTAS CONTAB"
							print existe == []
							#print existe	
							if existe == []:

								print "ERRRO CONTA 1"
								print "Conta ", unicode(conta.strip()), " nao existe"
								registoerro = True							
								text_file.write("Conta " + unicode(conta.strip()) + " nao existe\n" )
									
						except frappe.DoesNotExistError:
							print "ERRRO CONTA 2"
							print "Conta ", unicode(conta.strip()), " nao existe"
							print existe.name == conta
							registoerro = True
							text_file.write("Conta " + unicode(conta.strip()) + " nao existe\n" )



						if registoerro == False:
							registoerro1 = True
							for contas in existe:
						
								#print contas['company']
								#print empresa
								if contas['company'] == empresa:
									#print "Lancamento no file"
									#print contas['name']
									conta = contas['name']
									registoerro1 = False

							if registoerro1 == True:

								print "ERRRO CONTA 3"
								print "Conta ", unicode(conta.strip()), " nao existe"
								registoerro = True
								text_file.write("Conta " + unicode(conta.strip()) + " nao existe")
							

	if registoerro == True:
		text_file.close()
		return

	client= FrappeClient("http://127.0.0.1:8000","administrator","123")
	with open ('/tmp/journalentry_dev.csv') as csvfile:
		readCSV = csv.reader(csvfile)
		print "Lendo o ficheiro..."

		for row in readCSV:
			#print row
			#print "======="
			#print row[0]
			if "Conta" in row[0]:
				print 'Inicio'
			elif row[0] == "\xef\xbb\xbfConta":
				print 'ainda falta'
			else:
				print row[0]
				print row[2] != 0
				print int(row[2]) <= 12
				print 'dia ', row[3] #DIA
				print 'diario ', row[4] #DIARIO
				print 'numdiario ', row[5] #NumDiario
				print 'ano ', row[35] #Ano

				if (len(row[0]) >1): #(row[0].strip() != "0"):
					if row[2] != 0 and int(row[2]) <= 12:

						conta = row[0]
						valoralt = row[1]
						descricao = row[10]
						natureza = row[12]
						datagravacao = datetime.strptime(row[34],'%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')



						registomes = row[2] #Mes
						registodia = row[3] #Dia
						diario = row[4] #Diario
						numerodiario = row[5] #Numdiario
						registoano = row[35] #Ano

						print "Registo a processar ===="
						print 'conta', conta
						print 'valor ', valoralt
						print 'descricao ', descricao
						print 'NumDiario ', numerodiario

						print datagravacao
					

						try:
							existe =  frappe.get_list("Account",filters=[['name', 'like',conta + '%']],fields=['name','company'])
							print "CONTAS CONTAB"
							print existe == []
							print existe	
							if existe == []:

								print "ERRRO CONTA"
								print "ERRRO CONTA"
								print "ERRRO CONTA"
								print "Conta ", unicode(conta.strip()), " nao existe"
								registoerro = True
								
								break
										
						except frappe.DoesNotExistError:
							print "ERRRO CONTA"
							print "ERRRO CONTA"
							print "ERRRO CONTA"
							print "Conta ", unicode(conta.strip()), " nao existe"
							print existe.name == conta
							registoerro = True
							break


						"""
							{"posting_date":"2018-01-01","doctype":"Journal Entry", "naming_series":"JV-", "voucher_type":"Journal Ent
	    ...: ry","company":"2MS - Comercio e Representacoes, Lda", "accounts":[{"is_advance":"No","cost_center":"Principal -
	    ...:  2ms","account":"75214300 - Conservação E Reparação - Equipamento - 2ms","against_account":"43120000-Depositos 
	    ...: A Ordem - Moeda Nacional Banco 1 - 2ms","doctype":"Journal Entry Account","debit_in_account_currency":50.0,"acc
	    ...: ount_currency":"KZ","exchange_rate":1,"docstatus":1},{"is_advance":"No","cost_center":"Principal - 2ms","accoun
	    ...: t":"43120000-Depositos A Ordem - Moeda Nacional Banco 1 - 2ms","against_account":"75214300 - Conservação E Repa
	    ...: ração - Equipamento - 2ms","doctype":"Journal Entry Account","credit_in_account_currency":50.0,"account_currenc
	    ...: y":"KZ","exchange_rate":1,"docstatus":1}], "owner":"administrator", "user_remark":"Daily Sales 1st Sep 2015", "
	    ...: remark":"Daily Sales Posting 1st Sep 2015", "docstatus":1}


						"""
						registoerro = True
						for contas in existe:
							
							#print contas['company']
							#print empresa
							if contas['company'] == empresa:
								#print "Lancamento no file"
								#print contas['name']
								conta = contas['name']
								registoerro = False

						if registoerro == True:
	
							print "ERRRO CONTA"
							print "ERRRO CONTA"
							print "ERRRO CONTA"
							print "Conta ", unicode(conta.strip()), " nao existe"
							break

						if natureza == "D":
							print 'NATUREZA D'
							contas1 = {
									"is_advance": "No", 
									"cost_center": centrocusto[0]['cost_center'],
									"account": conta,
									"doctype": "Journal Entry Account", 									"debit_in_account_currency": valoralt, 
									"account_currency": "KZ",
									"exchange_rate": 1,
									"docstatus": 1
								}
							#print contas1
						elif natureza == "C":
							print 'NATUREZA C'
							contas2 = {
									"is_advance": "No",
									"cost_center": centrocusto[0]['cost_center'],
									"account": conta,
									"doctype":"Journal Entry Account", 									"credit_in_account_currency": valoralt,
									"account_currency": "KZ",
									"exchange_rate": 1,
									"docstatus": 1
								}
							#print contas2



							"""
							dados = {
								"posting_date": frappe.util.nowdate(),
								"doctype": "Journal Entry", 
								"naming_series": "JV-", 
								"voucher_type": "Journal Entry", 
								"company": empresa, 
								"accounts":[
								{
									"is_advance": "No", 
									"cost_center": centrocusto,
									"account": "75214300 - Conservação E Reparação - Equipamento - 2ms",
									"against_account": "43120000-Depositos", 
									"doctype": "Journal Entry Account", 									"debit_in_account_currency": 50.0, 
									"account_currency": "KZ",
									"exchange_rate": 1,
									"docstatus": 1
								},
								{
									"is_advance": "No",
									"cost_center": centrocusto,
									"account": "43120000-Depositos",
									"against_account": "75214300",
									"doctype":"Journal Entry Account", 									"credit_in_account_currency": 50.0,
									"account_currency": "KZ",
									"exchange_rate": 1,
									"docstatus": 1
								}],
								"owner": "administrator", 
								"user_remark":"Daily Sales 1st Sep 2015",
								"remark": "Daily Sales Posting 1st Sep 2015", 
								"docstatus": 1	
							}
	
							"""
						if olddiario == "" and oldnumerodiario == "":
						#if olddescricao == "":
							print "Primeira volta"
							olddescricao = descricao
							oldregistodia = registodia
							oldnumerodiario = numerodiario
							olddiario = diario

							print contas1
							print contas2
							if contas1:					
								#Debito
								contasJV.append(contas1)
								contas1 ={}
							elif contas2:
								#Credito
								contasJV.append(contas2)				
								contas2 = {}

						elif diario != olddiario or numerodiario != oldnumerodiario:
						#elif descricao != olddescricao:
							#Novo registo
							print "Novo Registo =========="
							print "DEVE SALVAR O REGISTO E INICIAR NOVO"

							dados = {
								"posting_date": datagravacao,
								"doctype": "Journal Entry", 
								"naming_series": "JV-", 
								"voucher_type": "Journal Entry", 
								"company": empresa,
								"accounts": contasJV, 
								"owner": "administrator", 
								"cheque_no": 'dia ' + olddiario + ' diario ' + oldnumerodiario,
								"cheque_date": datagravacao,
								"user_remark": olddescricao + ' dia ' + olddiario + ' diario ' + oldnumerodiario + ' dated ' + datagravacao,
								"remark": "Reference #" + olddiario + numerodiario + ' dated ' + datagravacao, 
								"docstatus": 1	
							}

							print "CONTAS JV ------"
							print contasJV
						
							print "REGISTO ++++++++"
							print dados
							olddescricao = descricao
							oldregistodia = registodia
							oldnumerodiario = numerodiario
							olddiario = diario

							registosalvo = True


							x = client.session.post("http://127.0.0.1:8000/api/resource/Journal Entry",data={"data":json.dumps(dados)})
							print "++++ RESULTADO +++++"
							print "++++ RESULTADO +++++"
							print "++++ RESULTADO +++++"
							print "++++ RESULTADO +++++"

							print " resultado ", x


							contasJV = []
							print "DEPOIS REGISTO "
							print contas1
							print contas2

							if contas1:					
								#Debito
								contasJV.append(contas1)
								contas1 ={}
							elif contas2:
								#Credito
								contasJV.append(contas2)				
								contas2 = {}


					
						else:
							print "Continua Registo ======="
							print "ACRESCENTA AO REGISTO ..."
							print contas1
							print "credito"
							print contas2

							if contas1:					
								#Debito
								contasJV.append(contas1)
								contas1 ={}
							elif contas2:
								#Credito
								contasJV.append(contas2)				
								contas2 = {}

							registosalvo = False


						#print "DADOS PARA CRIAR "
						#print dados
						#print contas1
						#print contas2



						"""	
						x = client.session.post("http://127.0.0.1:8000/api/resource/Sales Invoice",data={"data":json.dumps(doc)})
						"""

	if registosalvo == False and registoerro == False:
		print "PRECISA SALVAR O ULTIMO REGISTO ======="
		print "PRECISA SALVAR O ULTIMO REGISTO ======="
		print "PRECISA SALVAR O ULTIMO REGISTO ======="
		print "PRECISA SALVAR O ULTIMO REGISTO ======="

		dados = {
			"posting_date": datagravacao,
			"doctype": "Journal Entry", 
			"naming_series": "JV-", 
			"voucher_type": "Journal Entry", 
			"company": empresa,
			"accounts": contasJV, 
			"owner": "administrator", 
			"user_remark": 'dia ' + olddiario + ' diario ' + oldnumerodiario + ' dated ' + datagravacao,
			"cheque_no": 'dia ' + olddiario + ' diario ' + oldnumerodiario,
			"cheque_date": datagravacao,
			"remark": "Reference #" + olddiario + oldnumerodiario + ' dated ' + datagravacao, 
			"docstatus": 1	
		}

		print "REGISTO ++++++++"
		print dados
		olddescricao = descricao
		oldregistodia = registodia
		oldnumerodiario = numerodiario
		olddiario = diario

		registosalvo = True		
		x = client.session.post("http://127.0.0.1:8000/api/resource/Journal Entry",data={"data":json.dumps(dados)})

		print "++++ RESULTADO +++++"
		print "++++ RESULTADO +++++"
		print "++++ RESULTADO +++++"
		print "++++ RESULTADO +++++"

		print "RESULTADO ", x

	#client.logout()


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
