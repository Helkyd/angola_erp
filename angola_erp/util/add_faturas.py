# -*- coding: utf-8 -*-
# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import sys
reload (sys)
sys.setdefaultencoding('utf8')



import frappe
from frappe import _
from frappe.utils import cint, random_string
from frappe.utils import cstr, flt, getdate
from frappe.utils import encode
from StringIO import StringIO
from frappeclient import FrappeClient
from datetime import datetime
import time
import csv 
import json


@frappe.whitelist()
def test_jentry():
	"""
		Pode ser apagado quando o check e Add to jentry estiver melhor ....
		Este usado para ver se o adding das contas funciona ...quando da o erro 417

	"""

	contasjv=[{u'account': u'729 -  Custos Com O Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'credit_in_account_currency': u'115264466',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'82070000 - Custo Com Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'debit_in_account_currency': u'115264466',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'729 -  Custos Com O Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'credit_in_account_currency': u'15677066',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'82070000 - Custo Com Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'debit_in_account_currency': u'15677066',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'729 -  Custos Com O Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'credit_in_account_currency': u'4770910',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'82070000 - Custo Com Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'debit_in_account_currency': u'4770910',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'729 -  Custos Com O Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'credit_in_account_currency': u'920500',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'82070000 - Custo Com Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'debit_in_account_currency': u'920500',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'729 -  Custos Com O Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'credit_in_account_currency': u'85684',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'82070000 - Custo Com Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'debit_in_account_currency': u'85684',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'729 -  Custos Com O Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'credit_in_account_currency': u'128055366',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'},
	{u'account': u'82070000 - Custo Com Pessoal - 2ms',
	u'account_currency': u'KZ',
	u'cost_center': u'Principal - 2ms',
	u'debit_in_account_currency': u'128055366',
	u'docstatus': 1,
	u'doctype': u'Journal Entry Account',
	u'exchange_rate': 1,
	u'is_advance': u'No'}]

	
	doc = frappe.get_doc({
		"posting_date" : "2012-06-20",
		"doctype" : "Journal Entry",
		"naming_series" : "JV-", 
		"voucher_type" : "Journal Entry",
		"company" : "2MS - Comercio e Representacoes, Lda",
		"accounts" : contasjv,
		"owner" : "administrator",
		"cheque_no" : "1111",
		"cheque_date" : "2012-06-20",
		"user_remark" : "olddescricao"

	})
	doc.insert()



@frappe.whitelist()
def check_jentry(empresa, usuario, senha,ficheiro="journalentry_dev.csv", site="http://127.0.0.1:8000"):

	if empresa is None:
		print "Nome da Empresa necessario"
		return
	elif usuario is None:
		print "Usuario e Senha necessario"
		return

	else:
		#cost center
		centrocusto = frappe.get_list("Company",filters=[['name','like', empresa]],fields=['cost_center'])


	"""
		bench execute --args "['Company name']"  angola_erp.util.add_faturas.add_jentry
	"""
	print "Ficheiro journalentry_dev.csv deve estar no /TMP"
	print "Ficheiro extraido do Primavera"
	print "Ter a certeza de Order by Ano, Mes, Dia, Diario, NumDiario, Descricao"
	print "Criar os Anos passados existentes no Ficheiro no ERPNext"

	print "Mudar o Usuario e a Senha para Importar"
	
	
	time.sleep(.1000)



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


	contador = 0

	#VERIFICA SE AS CONTAS EXISTEM... Antes de voltar a processar novamente ...

	client= FrappeClient(site,usuario,senha)
	if not "tmp" in ficheiro:
		ficheiro = "/tmp/" + ficheiro	

	#with open ('/tmp/journalentry_dev.csv') as csvfile:
	with open (ficheiro) as csvfile:
		readCSV = csv.reader(csvfile)
		print "Lendo o ficheiro...Verificando Contas"

		text_file = open('/tmp/criarcontas.txt', "w")

		for row in readCSV:
			if "Conta" in row[0]:
				print 'Inicio'
			elif row[0] == "\xef\xbb\xbfConta":
				print 'ainda falta'
			else:
				#print row
				if (len(row[0]) >1): #(row[0].strip() != "0"):
					#print row[1]
					#print row[2]
					if row[2] != 0 and int(row[2]) <= 12:

						conta = row[0]
						valoralt = row[11]
						descricao = row[10]
						natureza = row[12]
						#print row[34]
						#print 'datagravacao ', row[35]
						#print 'ana ', row[36]
						#print 'conta ', conta
						#print 'descricao ', descricao

						datagravacao = datetime.strptime(row[34],'%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')



						registomes = row[2] #Mes
						registodia = row[3] #Dia
						diario = row[4] #Diario
						numerodiario = row[5] #Numdiario
						registoano = row[35] #Ano
			

						try:
							#existe =  frappe.get_list("Account",filters=[['name', 'like',conta + '%']],fields=['name','company','is_group'])
							cc = conta + '%'
							existe = frappe.db.sql(""" SELECT name, company, is_group from `tabAccount` where name like %s and company like %s """,(cc,empresa),as_dict=True)

							existeano = frappe.db.sql(""" select year, year_start_date, year_end_date, disabled from `tabFiscal Year` where year = %s """,(registoano),as_dict=True)
							print 'ano ', existeano
							contador += 1
							print contador

							if existeano == []:

								dados = { 
									"year_start_date": registoano + "-01-01",
									"name": registoano,
									"year_end_date": registoano + "-12-31",
									#"companies":[],
									"doctype":"Fiscal Year", 										"disabled":0,
									"year": registoano,
									"owner":"Administrator",
									"docstatus":0
								}
								x = client.session.post(site +"/api/resource/Fiscal Year",data={"data":json.dumps(dados)})
								print dados
								print "++++ RESULTADO Ano Fiscal  +++++"
								print " resultado ", x
								if x.status_code == 200:
									#200
									print 'Anos Fiscal criado ', registoano
									frappe.db.commit()
									time.sleep(.800)		
										
								else:
									print x
									print "Ano Fiscal ", registoano, ' tem que ser criado!'
									return
							
	
							#print "CONTAS CONTAB"
							#print existe == []
							#print existe	


							if existe == []:

								print 'Conta ', conta, ' nao existe...tentar procura 3 digitos..'
								#Tenta criar a conta apartir dos 3 digitos
								#existe1 =  frappe.get_list("Account",filters=[['name', 'like',conta[0:3] + '%']],fields=['name','report_type','root_type','account_type','company','is_group'])

								conta0 = conta[0:3] + '%'
								existe1 = frappe.db.sql(""" SELECT name, report_type, root_type, account_type, company, is_group from `tabAccount` where name like %s and company like %s and is_group =1 """,(conta0,empresa),as_dict=True)

								if existe1 == []:
									conta0 = conta[0:2] + '%'
									existe1 = frappe.db.sql(""" SELECT name, report_type, root_type, account_type, company, is_group from `tabAccount` where name like %s and company like %s and is_group =1 """,(conta0,empresa),as_dict=True)

									#Raro nao existir 
									if existe1 == []:
										print 'Conta ', conta[0:2], ' nao existe. Tem que criar.'
										conta0 = conta[0:1] + ' -%' #Um digito apenas
										existe1 = frappe.db.sql(""" SELECT name, report_type, root_type, account_type, company, is_group from `tabAccount` where name like %s and company like %s and is_group =1 """,(conta0,empresa),as_dict=True)
										print conta0, ' ', existe1
										#print existe1[0]['name']
										if existe1 != []:
											conta1 = existe1[0]['name']
											conta1desc = conta1
											if conta1.count('-') >= 2:
												conta1desc = conta1[conta1.find('-')+1:len(conta1)]

											conta1desc = conta1desc[0:conta1desc.find('-')-1]

											dados = {
												"doctype": "Account",
												"report_type": existe1[0]['report_type'],
												"owner": "administrator",
												"account_name": conta[0:2] + ' - ' + conta1desc,
												"freeze_account": "No",
												"root_type": existe1[0]['root_type'],
												"docstatus": 0,
												"company": empresa,
												"is_group": 1,
												"tax_rate": 0.0,
												"account_currency": "KZ",
												"parent_account": existe1[0]['name'],
												"name": conta[0:2] + ' - ' + conta1desc,
												"idx": 0,
												"docstatus": 0
											}
											x = client.session.post(site + "/api/resource/Account",data={"data":json.dumps(dados)})
											print dados
											print "++++ RESULTADO Accounts conta 1 digitos  +++++"

											print " resultado ", x

											if x.status_code == 200:
												#200
												frappe.db.commit()
												print 'Registo salvo'
												registosalvo = True
												time.sleep(.800)
												#Tenta criar novamente
												conta0 = conta[0:2] + '%'
												existe1 = frappe.db.sql(""" SELECT name, report_type, root_type, account_type, company, is_group from `tabAccount` where name like %s and company like %s and is_group =1 """,(conta0,empresa),as_dict=True)
												print conta0, ' ', existe1
												print existe1[0]['name']

												
												#break

									
											else:

												print "Conta ou Grupo ", conta0, ' tem que ser criado!'
												return
											

									
									for contas in existe1:
										print 'contas 3 e 2'
										print contas
										if contas['company'] == empresa and contas['is_group'] == 1:
											if contas['name'].startswith(conta[0:2] + ' '):

												conta1 = contas['name']
												conta1desc = conta1
												if conta1.count('-') >= 2:
													conta1desc = conta1[conta1.find('-')+1:len(conta1)]

												conta1desc = conta1desc[0:conta1desc.find('-')-1]

												dados = {
													"doctype": "Account",
													"report_type": contas['report_type'],
													"owner": "administrator",
													"account_name": conta[0:3] + ' - ' + conta1desc,
													"freeze_account": "No",
													"root_type": contas['root_type'],
													"docstatus": 0,
													"company": empresa,
													"is_group": 1,
													"tax_rate": 0.0,
													"account_currency": "KZ",
													"parent_account": contas['name'],
													"name": conta[0:3] + ' - ' + conta1desc,
													"idx": 0,
													"docstatus": 0
												}
												x = client.session.post(site + "/api/resource/Account",data={"data":json.dumps(dados)})
												print dados
												print "++++ RESULTADO Accounts conta 2 digitos  +++++"

												print " resultado ", x

												if x.status_code == 200:
													#200
													frappe.db.commit()
													print 'Registo salvo'
													registosalvo = True
													#Tenta criar novamente
													conta0 = conta[0:3] + '%'
													existe1 = frappe.db.sql(""" SELECT name, report_type, root_type, account_type, company, is_group from `tabAccount` where name like %s and company like %s and is_group =1 """,(conta0,empresa),as_dict=True)

													time.sleep(.800)
													break

										
												else:

													print "Conta ou Grupo ", conta0, ' tem que ser criado!'
													return

								for contas in existe1:
							
									#print contas
									#print empresa
									if contas['company'] == empresa and contas['is_group'] == 1:
										conta1 = contas['name']
										conta1desc = conta1
										if conta1.count('-') >= 2:
											conta1desc = conta1[conta1.find('-')+1:len(conta1)]

										conta1desc = conta1desc[0:conta1desc.find('-')-1]
										print conta1desc
										print "conta ", conta



										registoerro = False
										if len(conta) == 3:
											dados = {
												"doctype": "Account",
												"report_type": contas['report_type'],
												"owner": "administrator",
												"account_name": conta + '00000 - ' + conta1desc,
												"freeze_account": "No",
												"root_type": contas['root_type'],
												"docstatus": 0,
												"company": empresa,
												"is_group": 0,
												"tax_rate": 0.0,
												"account_currency": "KZ",
												"parent_account": contas['name'],
												"name": conta + '00000 - ' + conta1desc,
												"idx": 0,
												"docstatus": 0
											}

										else:
											dados = {
												"doctype": "Account",
												"report_type": contas['report_type'],
												"owner": "administrator",
												"account_name": conta + ' - ' + conta1desc,
												"freeze_account": "No",
												"root_type": contas['root_type'],
												"docstatus": 0,
												"company": empresa,
												"is_group": 0,
												"tax_rate": 0.0,
												"account_currency": "KZ",
												"parent_account": contas['name'],
												"name": conta + ' - ' + conta1desc,
												"idx": 0,
												"docstatus": 0
											}

										print dados
										x = client.session.post(site + "/api/resource/Account",data={"data":json.dumps(dados)})
										print "++++ RESULTADO Accounts +++++"
										print "++++ RESULTADO Accounts  +++++"
										print "++++ RESULTADO Accounts  +++++"
										print "++++ RESULTADO Accounts  +++++"

										print " resultado ", x

										if x.status_code == 200:

											#200
											frappe.db.commit()
											print 'Registo salvo'
											registosalvo = True
											time.sleep(.800)

										elif x.status_code == 409:
											print 'Registo ja existe ....'
										else:
											print "ERRRO CONTA 1"
											print "Conta ", unicode(conta.strip()), " nao existe"
											registoerro = True		

											text_file.write("Conta " + unicode(conta.strip()) + " nao existe\n" )

										#break

							else:
								#Tem registos mas nao tem a conta
								registoerro = True
								#if conta == '48110000':
								#	print 'TEM REGISTOS mas nao tem CONTA ', conta
								for contas in existe:
									#if '48110000' in contas['name']:
									#	print contas['company']
									#	print contas['name']
									#	print empresa
									print 'EXISTE '
									print existe
									print 'conta ', conta
									if contas['company'] == empresa:
										if contas['is_group'] == 1 and len(conta) == 3:
											#conta 3 digitos add 00000
											print "cria a conta com 5 ZEROs!!!!!"
											#return
										else:
											conta1 = contas['name']
											conta1desc = conta1[conta1.find('-')+1:len(conta1)]
											conta1desc = conta1desc[0:conta1desc.find('-')-1]
										#print "CONTA EXISTE"
										#print conta1
										#print conta1desc

											registosalvo = True
											registoerro = False

									
						except frappe.DoesNotExistError:
							print "ERRRO CONTA 2"
							print "Conta ", unicode(conta.strip()), " nao existe"
							print existe.name == conta
							registoerro = True
							text_file.write("Conta " + unicode(conta.strip()) + " nao existe\n" )



						if registoerro == False:
							registoerro1 = True
							if registosalvo == False:
								for contas in existe:
									print existe
								
									#print contas['company']
									#print empresa
									if contas['company'] == empresa: #and contas['company'] == 1:
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
		print 'Ficheiro criado /tmp/criarcontas.txt ' 
		return




	print "TERMINOU DE VERIFICAR CONTAS E ANO FISCAL"


@frappe.whitelist()
def add_jentry(empresa, usuario, senha, ficheiro="journalentry_dev.csv", site="http://127.0.0.1:8000"):


	if empresa is None:
		print "Nome da Empresa necessario"
		return
	elif usuario is None:
		print "Usuario e Senha necessario"
		return

	else:
		#cost center
		centrocusto = frappe.get_list("Company",filters=[['name','like', empresa]],fields=['cost_center'])


	"""
		bench execute --args "['Company name']"  angola_erp.util.add_faturas.add_jentry
	"""
	print "Ficheiro journalentry_dev.csv deve estar no /TMP"
	print "Ficheiro extraido do Primavera"
	print "Ter a certeza de Order by Ano, Mes, Dia, Diario, NumDiario, Descricao"
	print "Criar os Anos passados existentes no Ficheiro no ERPNext"

	print "Mudar o Usuario e a Senha para Importar"
	
	
	time.sleep(.1000)



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

	registoerro1 = False

	clientediversos = frappe.db.sql(""" SELECT name from `tabCustomer` where name like 'diversos' """,as_dict=True)

	client= FrappeClient(site,usuario,senha)
	if not "tmp" in ficheiro:
		ficheiro = "/tmp/" + ficheiro	
	

	with open (ficheiro) as csvfile:
		readCSV = csv.reader(csvfile)
		print "Lendo o ficheiro..."
		
		text_file = open(ficheiro[0:ficheiro.find('_')+1] + 'movimentos_error.txt', "w")

		for row in readCSV:
			#print row
			#print "======="
			#print row[0]
			if "Conta" in row[0]:
				print 'Inicio'
			elif row[0] == "\xef\xbb\xbfConta":
				print 'ainda falta'
			else:
				#print row[0]
				#print row[2] != 0
				#print int(row[2]) <= 12

				if (len(row[0]) >1): #(row[0].strip() != "0"):
					if int(row[2]) != 0 and int(row[2]) <= 12: 
						if int(row[5]) > 1 and row[1] != 0:

							conta = row[0]
							valoralt = row[11]
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
								#existe =  frappe.get_list("Account",filters=[['name', 'like',conta + '%']],fields=['name','company'])
								cc = conta + '%'
								existe = frappe.db.sql(""" SELECT name, company, is_group from `tabAccount` where name like %s and company like %s """,(cc,empresa),as_dict=True)
								#print "CONTAS CONTAB"
								#print existe == []
								#print existe	
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


							registoerro = True
							for contas in existe:
							
								#print contas['company']
								#print empresa
								if contas['company'] == empresa:
									#print "Lancamento no file"
									#print contas['name']
									conta = contas['name'] #.encode('utf-8')
									registoerro = False

							if registoerro == True:
	
								print "ERRRO CONTA"
								print "ERRRO CONTA"
								print "ERRRO CONTA"
								print "Conta ", unicode(conta.strip()), " nao existe"
								break

							if natureza == "D":
								#print 'NATUREZA D'
								if conta.startswith('31121000'):
									contas1 = {
											"is_advance": "No", 
											"cost_center": centrocusto[0]['cost_center'],
											"account": conta,
											"doctype": "Journal Entry Account", 									"debit_in_account_currency": valoralt, 
											"account_currency": "KZ",
											"exchange_rate": 1,
											"docstatus": 1,
											"party_type": "Customer",
											"party": clientediversos[0]['name'] 
										}
								else:
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
								if conta.startswith('31121000'):
									contas2 = {
											"is_advance": "No",
											"cost_center": centrocusto[0]['cost_center'],
											"account": conta,
											"doctype":"Journal Entry Account", 									"credit_in_account_currency": valoralt,
											"account_currency": "KZ",
											"exchange_rate": 1,
											"docstatus": 1,
											"party_type": "Customer",
											"party": clientediversos[0]['name']
										}
								else:
									contas2 = {
											"is_advance": "No",
											"cost_center": centrocusto[0]['cost_center'],
											"account": conta,
											"doctype":"Journal Entry Account", 									"credit_in_account_currency": valoralt,
											"account_currency": "KZ",
											"exchange_rate": 1,
											"docstatus": 1
										}


								print conta #.encode('utf-8')
								print unicode(contas2).decode('utf-8')



							if olddiario == "" and oldnumerodiario == "":
							#if olddescricao == "":
								print "Primeira volta"
								olddescricao = descricao
								oldregistodia = registodia
								oldnumerodiario = numerodiario
								olddiario = diario
								olddatagravacao = datagravacao

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
									"posting_date": olddatagravacao,
									"doctype": "Journal Entry", 
									"naming_series": "JV-", 
									"voucher_type": "Journal Entry", 
									"company": empresa,
									"accounts": contasJV, 
									"owner": "administrator", 
									"cheque_no": 'dia ' + olddiario + ' diario ' + oldnumerodiario,
									"cheque_date": datagravacao,
									"user_remark": olddescricao + ' dia ' + olddiario + ' diario ' + oldnumerodiario + ' dated ' + olddatagravacao,
									"remark": "Reference #" + olddiario + oldnumerodiario + ' dated ' + olddatagravacao, 
									"docstatus": 1	
								}

								#moved down
								#olddescricao = descricao
								#oldregistodia = registodia
								#oldnumerodiario = numerodiario
								#olddiario = diario

								registosalvo = True

								#If conta1 = conta2 CANCEL add... conta deb and cre cannot be the same...
								#print "CONTAS JV"
								#print contasJV
								
								#print 'debito ', contas1
								#print 'credito ', contas2
								#print contas1 == contas2
								conta00 = ''
								conta00tipo = ''
								conta00valor = 0
								contasiguais = False

								
								#caso count reg >=2 and count conta >=2 deb e cred na mesma conta...
								#caso recordcount - countcontas = 1 entao cred e deb na mesma conta...
								
								d = {}
								registos = 0
								
								for elem in contasJV:
									registos += 1
									print "VERIFICA DUPLICADOS!!!!"
									#print elem
									#print elem['account']
									#print "D Elem"
									#print d.items()
									#print d.has_key([elem['account'], elem['credit_in_account_currency']])
									#print d.has_key([elem['account'], elem['debit_in_account_currency']])
									acrescenta = True
									if d != {}:
										#print elem['account']
										#print "tipo ", d.items()[0][0][0]
										#print d.items()[0][0][1]

										for c in d.items():
											#print 'dentro ', c[0][0]
											#print c[0][1]
											
											if c[0][0] == elem['account']:
												print 'conta +1'
												print c[0][1]
												if 'credit_in_account_currency' in elem:
											
													print elem['credit_in_account_currency']
													if  elem['credit_in_account_currency'] == c[0][1]:
														d[elem['account'], elem['credit_in_account_currency']] += 1
													else:
														d[elem['account'], elem['credit_in_account_currency']] = 1
													acrescenta = False
													break

												elif 'debit_in_account_currency' in elem:
													#print 'DEBITO'
													#print elem['account']
													print elem['debit_in_account_currency']
													#print c[0][1]
													if  elem['debit_in_account_currency'] == c[0][1]: 
														d[elem['account'], elem['debit_in_account_currency']] += 1
													else:
														d[elem['account'], elem['debit_in_account_currency']] = 1
													acrescenta = False
													break

												#contaduplicada[conta[0][0]] = contaduplicada[conta[0][0]] + 1
												
												#break

										
										if acrescenta == True:
											print 'acrescenta'
											#print elem
											if 'debit_in_account_currency' in elem:
												#if  elem['debit_in_account_currency'] == d.items()[0][0][1]: 
												d[elem['account'], elem['debit_in_account_currency']] = 1
													#else:
													#	d[elem['account'], elem['debit_in_account_currency']] = 1
											elif 'credit_in_account_currency' in elem:
												#if  elem['credit_in_account_currency'] == d.items()[0][0][1]: 
												d[elem['account'], elem['credit_in_account_currency']] = 1

											#contaduplicada[conta[0][0]] = 1

										#print "novo for"
										#print d.items()
										
										"""
										if elem['account'] in d.items()[0][0][0]:
											print "Conta +1"			
											if 'credit_in_account_currency' in elem:
											
												print elem['credit_in_account_currency']
												if elem['credit_in_account_currency'] in d.items()[0][0][1]:
													if  elem['credit_in_account_currency'] == d.items()[0][0][1]:
														d[elem['account'], elem['credit_in_account_currency']] += 1
													else: 
														d[elem['account'], elem['credit_in_account_currency']] = 1
												else:
													d[elem['account'], elem['credit_in_account_currency']] = 1

											elif 'debit_in_account_currency' in elem:
												print elem['account']
												print elem['debit_in_account_currency']
												if elem['debit_in_account_currency'] in d.items()[0][0][1]:
													print d.items()[0][0][1]
													#print d[elem['account'], elem['debit_in_account_currency']]

													if  elem['debit_in_account_currency'] == d.items()[0][0][1]: 
														d[elem['account'], elem['debit_in_account_currency']] += 1
													else:
														d[elem['account'], elem['debit_in_account_currency']] = 1
												else:
													d[elem['account'], elem['debit_in_account_currency']] = 1
										elif elem['account'] in d.items()[0][0]:
											print "Conta +2"			
											return
											if 'credit_in_account_currency' in elem:
												print elem['credit_in_account_currency']
												d[elem['account'], elem['credit_in_account_currency']] = 1

											elif 'debit_in_account_currency' in elem:
												print elem['debit_in_account_currency']
												d[elem['account'], elem['debit_in_account_currency']] = 1
										elif type(d) == list:
											print "lista"
											return
										#	print d[0][0][0]
										#	if elem['account'] in d[0][0][0]:
										#		print "Conta List 1"			
										#		if 'credit_in_account_currency' in elem:
											
										#			print elem['credit_in_account_currency']
										#			if elem['credit_in_account_currency'] in d[0][0][1]:
										#				d[elem['account'], elem['credit_in_account_currency']] += 1
										#			else:
										#				d[elem['account'], elem['credit_in_account_currency']] = 1

										#		elif 'debit_in_account_currency' in elem:
										#			print elem['debit_in_account_currency']
										#			if elem['debit_in_account_currency'] in d[0][0][1]:
										#				d[elem['account'], elem['debit_in_account_currency']] += 1
										#			else:
										#				d[elem['account'], elem['debit_in_account_currency']] = 1

										else:
											if 'credit_in_account_currency' in elem:
												print elem['credit_in_account_currency']
												d[elem['account'], elem['credit_in_account_currency']] = 1
											elif 'debit_in_account_currency' in elem:
												print elem['debit_in_account_currency']
												d[elem['account'], elem['debit_in_account_currency']] = 1


										print "========"
										print d.items()
										"""

									elif d == {}:
										#d[elem['account']] = 1
										print "Conta 1"
										if 'credit_in_account_currency' in elem:
											#print elem['credit_in_account_currency']
											d[elem['account'], elem['credit_in_account_currency']] = 1
										elif 'debit_in_account_currency' in elem:
											#print elem['debit_in_account_currency']
											d[elem['account'], elem['debit_in_account_currency']] = 1

								#print "Conta 1 ", d.items()

										
								print "RESULTADO DUPLICADOS"
								print ([x for x, y in d.items() if y >1])
								if int(d.items()[0][1]) > 1:

									if (registos - int(d.items()[0][1]) == 1) or (registos == int(d.items()[0][1])):

										#print d.items()
										#print registos
										#print int(d.items()[0][1])
										if (registos == int(d.items()[0][1])):
											print "Contas iguais"
											contasiguais = True
										#return
								else:
									#Para os casos 4 registos com 3 contas iguais mais valores diferentes ...
									print "REGISTOs por verificar!!!!!"
									#print d.items()
									#print registos
									contaduplicada = {}
									acrescenta = True
									for conta in d.items():
										#print conta
										#print 'conta ', conta[0][0]
										#print d.items()[0]
										if contasiguais == True:
											print "Saindo do loop Conta d.ITEMS"
											print contaduplicada
											break
										elif contaduplicada != {}:
											#print 'reg dupl ',contaduplicada.items()
											for c in contaduplicada.items():
												#print 'dentro ', c[0]
												if c[0] == conta[0][0]:
													#print 'xxxxxx'
													contaduplicada[conta[0][0]] = contaduplicada[conta[0][0]] + 1
													acrescenta = False
													if int(contaduplicada[conta[0][0]]) == 2:
														print "ESTE TEM QUE PARAR 2 vezes"
														print "ESTE TEM QUE PARAR 2 vezes"
														print "Nao deve salvar o registo!!!"
														print registos
														print contaduplicada[c[0]]


													elif int(contaduplicada[conta[0][0]]) >= 3:
														if registos == contaduplicada[c[0]]:
															print "ESTE TEM QUE PARAR 3 ou mais !!!!!"
															print "ESTE TEM QUE PARAR 3 ou mais !!!!!"
															print "ESTE TEM QUE PARAR 3 ou mais !!!!!"
															print contaduplicada[c[0]]

															print registos

															contasiguais = True
															break
														#return
													#return
											
											if acrescenta == True:
												#print 'acrescenta'
												contaduplicada[conta[0][0]] = 1
										#if conta[0][0] in contaduplicada.items():
										#	print "depois"
										#	contaduplicada[conta[0][0]] += 1
										else:
											print "inicio"

											contaduplicada[conta[0][0]] = 1
											print contaduplicada[conta[0][0]]

										#print 'conta dup', contaduplicada.items()



								if contasiguais == False:

									x = client.session.post(site + "/api/resource/Journal Entry",data={"data":json.dumps(dados)})
									print "++++ RESULTADO +++++"

									print " resultado ", x.status_code
									if x.status_code == 200:
										print 'salvo'
										print olddiario, ' ', oldnumerodiario, ' ', olddescricao
										print olddatagravacao
										time.sleep(.500)
									elif x.status_code == 417:
										print 'Verifique Ano Fiscal Ou Debito e Credito na mesma conta!'

										print 'diario ', olddiario
										print 'numdiario ', oldnumerodiario
										print 'descricao ', olddescricao
										print 'datagravacao ', olddatagravacao

										print "CONTAS JV ------"
										print contasJV
						
										print "REGISTO ++++++++"
										print dados

										#Salva o erro no File ...e Continua
										registoerro1 = True
										text_file.write(empresa + "\n")
										text_file.write("Diario " + unicode(olddiario.strip()) + "\n NumeroDiario " + unicode(oldnumerodiario.strip()) + "\n Descricao " + unicode(olddescricao.strip()) + "\n")
										#print contasJV
										for tmp in contasJV:
											text_file.write(tmp['account'] + "\n")
											if 'debit_in_account_currency' in tmp:
												text_file.write(tmp['debit_in_account_currency'] + "\n")
											else:
												text_file.write(tmp['credit_in_account_currency'] + "\n")
											text_file.write("\n")	

										#return Retirado por enquanto... deu erro mas pode continuar a importar.
									else:
										print 'diario ', diario
										print 'numdiario ', numerodiario
										print 'descricao ', descricao

										print "CONTAS JV ------"
										print contasJV
						
										print "REGISTO ++++++++"
										print dados

										return


									contasJV = []
									#print "DEPOIS REGISTO "
									#print contas1
									#print contas2
								else:
									registoerro1 = True
									text_file.write(empresa + "\n")
									text_file.write("Diario " + unicode(olddiario.strip()) + "\n NumeroDiario " + unicode(oldnumerodiario.strip()) + "\n Descricao " + unicode(olddescricao.strip()) + "\n")
									print contasJV
									for tmp in contasJV:
										text_file.write(tmp['account'] + "\n")
										if 'debit_in_account_currency' in tmp:
											text_file.write(tmp['debit_in_account_currency'] + "\n")
										else:
											text_file.write(tmp['credit_in_account_currency'] + "\n")
										text_file.write("\n")	
									#text_file.write(contasJV) Por ver como passar
									#text_file.write("\n\n")



								if contas1:					
									#Debito
									contasJV.append(contas1)
									contas1 ={}
								elif contas2:
									#Credito
									contasJV.append(contas2)				
									contas2 = {}


								#novos values nos old
								olddescricao = descricao
								oldregistodia = registodia
								oldnumerodiario = numerodiario
								olddiario = diario

	
							else:
								print "Continua Registo ======="
								print "ACRESCENTA AO REGISTO ..."
								#print contas1
								#print "credito"
								#print contas2

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
		x = client.session.post(site + "/api/resource/Journal Entry",data={"data":json.dumps(dados)})

		print "++++ RESULTADO +++++"

		print " resultado ", x.status_code
		if x.status_code == 200:
			print 'salvo'
			print " resultado ", x.status_code
			print diario, ' ', numerodiario, ' ', descricao
			print datagravacao

		else:
			print 'diario ', diario
			print 'numdiario ', numerodiario
			print 'descricao ', descricao

			return

	if registoerro1 == True:
		text_file.close()
		print 'Ficheiro criado /tmp/movimentos_error.txt ' 
		return



	print "FIM DO LANCAMENTO DOS DADOS PRIMAVERA NO ERPNext"

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
