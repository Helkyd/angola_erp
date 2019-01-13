# -*- coding: utf-8 -*-
# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt

#Date Changed: 12/01/2019

from __future__ import unicode_literals

from frappe.model.document import Document
import frappe.model
import frappe
from frappe.utils import nowdate, cstr, flt, cint, now, getdate
from frappe import throw, _
from frappe.utils import formatdate, encode
from frappe.model.naming import make_autoname
from frappe.model.mapper import get_mapped_doc

from frappe.email.doctype.email_group.email_group import add_subscribers

@frappe.whitelist()
def check_caixa_aberto():

	if (frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)) != ():
		print "AAAAAAAA"
		return frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)
	elif (frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Em Curso' """, as_dict=False)) != ():
		return frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Em Curso' """, as_dict=False)
		print "BBBBBBBBB"
		print frappe.db.sql("""select name from `tabCaixa de Registo` WHERE status_caixa ='Aberto' """, as_dict=False)	

@frappe.whitelist()
def caixa_movimentos_in(start,caixa,fecho):

		total_tpa = 0
		total_ccorrente = 0
		total_caixa = 0
		recalcula = False
		for d in  frappe.db.sql("""select hora_atendimento, name,total_servicos,pagamento_por, status_atendimento, bar_tender, company from `tabAtendimento Bar` where status_atendimento ='Fechado' and hora_atendimento >= %(start)s and hora_atendimento <= %(end)s """, {"start": start,"end": frappe.utils.now()	}, as_dict=True):
			
			print "MOVIMENTOS BAR RESTAURANTE +++++++++++++++++++++++++++++++"
			ddd = make_autoname('MOV-' + '.#####')
			if len(frappe.db.sql("SELECT name,descricao_movimento from tabMovimentos_Caixa WHERE descricao_movimento=%(mov)s""",{"mov":d.name}, as_dict=True))==0:
				frappe.db.sql("INSERT into tabMovimentos_Caixa (name, docstatus, parent, parenttype, parentfield, tipo_pagamento, descricao_movimento, valor_pago, hora_atendimento, creation, modified, usuario_movimentos, company) values (%s,0,%s,'Caixa de Registo','movimentos_caixa',%s,%s,%s,%s,%s,%s,%s,%s) ",(ddd, caixa, d.pagamento_por ,d.name, d.total_servicos, d.hora_atendimento, frappe.utils.now(), frappe.utils.now(),d.bar_tender,d.company))
				total_caixa = d.total_servicos+total_caixa
				if (d.pagamento_por == "TPA"):
					total_tpa = d.total_servicos+total_tpa
				
				if (d.pagamento_por == "Conta-Corrente"):
					total_ccorrente = d.total_servicos+total_ccorrente
			else:
				#Recalcula o Caixa ....
				recalcula = True
				total_caixa = d.total_servicos+total_caixa
				if (d.pagamento_por == "TPA"):
					total_tpa = d.total_servicos+total_tpa
				
				if (d.pagamento_por == "Conta-Corrente"):
					total_ccorrente = d.total_servicos+total_ccorrente

		print "Abre Caixa"
		print total_caixa
		reser = frappe.get_doc("Caixa de Registo",caixa)
		if (total_caixa > 1) and (reser.amount_caixa == 0):
			if (recalcula == False):
				reser.amount_caixa = total_caixa+reser.amount_caixa
				reser.amount_tpa = total_tpa+reser.amount_tpa
				reser.amount_conta_corrente = total_ccorrente+reser.amount_conta_corrente
			else:
				reser.amount_caixa = total_caixa
				reser.amount_tpa = total_tpa
				reser.amount_conta_corrente = total_ccorrente

			reser.status_caixa='Em Curso'
			reser.save()
		elif (total_caixa > 1) and (reser.amount_caixa >= 0):
			if (recalcula == False):
				reser.amount_caixa = total_caixa+reser.amount_caixa
				reser.amount_tpa = total_tpa+reser.amount_tpa
				reser.amount_conta_corrente = total_ccorrente+reser.amount_conta_corrente
			else:
				reser.amount_caixa = total_caixa
				reser.amount_tpa = total_tpa
				reser.amount_conta_corrente = total_ccorrente

			reser.save()

		print fecho
		print reser.status_caixa
		if (fecho==2):
			reser.status_caixa='Fechado'
			reser.save()

		

		return total_caixa



@frappe.whitelist()
def get_taxa_ipc():
	#IPC to temp account 37710000

	#locate account 37710000 instead of 34210000
	j= frappe.db.sql(""" select name, description, account_head, parent  from `tabSales Taxes and Charges` where account_head like '3771%' and parenttype ='Sales Taxes and Charges Template' """,as_dict=True)

	print " LISTA TAXE IPC conta 3771"
	print j	

	return j

@frappe.whitelist()
def get_taxa_ipc_1():
	#Original

	#locate account 34210000
	j= frappe.db.sql(""" select name, description, account_head, parent  from `tabSales Taxes and Charges` where account_head like '3421%' and parenttype ='Sales Taxes and Charges Template' """,as_dict=True)

	print " LISTA TAXE IPC conta 3421"
	print j	

	return j


@frappe.whitelist()
def get_contab_taxa_retencao(empresa,fornclien = 'Supplier'):
	#locate account 34130000 or plano contif 2.80.20.20.30 - Ret Fonte a Pagar - Imposto Industrial
	print (empresa).encode('utf-8')
	if (empresa):
		if (fornclien == 'Supplier'):
			j= frappe.db.sql(""" select name, account_name from `tabAccount` where company = %s and account_name like '3413%%'  """,(empresa),as_dict=True)
			print " LISTA CONTAB TAXA RETENCAO conta 3413"
		else:
			j= frappe.db.sql(""" select name, account_name from `tabAccount` where company = %s and account_name like '3414%%'  """,(empresa),as_dict=True)
			print " LISTA CONTAB TAXA RETENCAO conta 3414"
		print j	

		# ****************** Still missing aqui qual a conta para o cliente e para fornecedor
		if (j==[]):
			#Plano CONTIF
			j= frappe.db.sql(""" select name, account_name from `tabAccount` where company = %s and account_name like '2.80.20.20.30%%' """,(empresa),as_dict=True)

			print " LISTA CONTAB TAXA RETENCAO conta 2.80.20.20.20"
			print j	

	return j if (j) else None

@frappe.whitelist()
def get_compras_taxa_retencao():
	#locate account 34130000 or plano contif 2.80.20.20.30 - Ret Fonte a Pagar - Imposto Industrial

	j= frappe.db.sql(""" select name, description, account_head, parent  from `tabPurchase Taxes and Charges` where account_head like '3413%' and parenttype ='Purchase Taxes and Charges Template' """,as_dict=True)

	print " LISTA COMPRA TAXA RETENCAO conta 3413"
	print j	
	if (j==[]):
		#Plano CONTIF
		j= frappe.db.sql(""" select name, description, account_head, parent  from `tabPurchase Taxes and Charges` where account_head like '2.80.20.20.30%' and parenttype ='Purchase Taxes and Charges Template' """,as_dict=True)

		print " LISTA COMPRA TAXA RETENCAO conta 2.80.20.20.20"
		print j	

	return j

@frappe.whitelist()
def get_vendas_taxa_retencao():
	#locate account 34140000 por liquidar pelo Cliente
	j= frappe.db.sql(""" select name, description, account_head, parent  from `tabSales Taxes and Charges` where account_head like '3414%' and parenttype ='Sales Taxes and Charges Template' """,as_dict=True)

	print " LISTA TAXA RETENCAO conta 3414"
	print j	
	if (j==[]):
		#Plano CONTIF
		j= frappe.db.sql(""" select name, description, account_head, parent  from `tabSales Taxes and Charges` where account_head like '2.80.20.20.30%' and parenttype ='Sales Taxes and Charges Template' """,as_dict=True)

		print " LISTA COMPRA TAXA RETENCAO conta 2.80.20.20.20"
		print j	

	return j

@frappe.whitelist()
def get_taxa_retencao():
	# POR REMOVER MAIS TARDE  **********************
	#locate account 34130000

	#Account 3413 ou 3414
	j= frappe.db.sql(""" select name, description, account_head, parent  from `tabSales Taxes and Charges` where account_head like '3413%' and parenttype ='Sales Taxes and Charges Template' """,as_dict=True)

	print " LISTA TAXA RETENCAO conta 3413"
	print j	
	if (j==[]):
		#Plano CONTIF
		j= frappe.db.sql(""" select name, description, account_head, parent  from `tabSales Taxes and Charges` where account_head like '2.80.20.20.30%' and parenttype ='Sales Taxes and Charges Template' """,as_dict=True)

		print " LISTA COMPRA TAXA RETENCAO conta 2.80.20.20.20"
		print j	

	return j

@frappe.whitelist()
def get_lista_retencoes():
	j= frappe.db.sql(""" SELECT name, descricao, percentagem, metade_do_valor from `tabRetencoes` """,as_dict=True)

	print " LISTA RETENCOES"
	print j	
	return j



@frappe.whitelist()
def get_lista_taxas_vendas():
	j= frappe.db.sql(""" select name, description  from `tabSales Taxes and Charges` """,as_dict=True)

	print " LISTA TAXES e CHARGES"
	print j	
	return j


@frappe.whitelist()
def get_supplier_retencao(fornecedor,fornclien = 'Supplier'):
	"""
		Looks for Supplier otherwise for Customer
	"""
	if (fornclien == 'Supplier'):
		j= frappe.db.sql(""" select name,que_retencao,retencao_na_fonte from `tabSupplier` where retencao_na_fonte=1 and name = %s """,fornecedor,as_dict=True)
	else:
		j= frappe.db.sql(""" select name,que_retencao,retencao_na_fonte from `tabCustomer` where retencao_na_fonte=1 and name = %s """,fornecedor,as_dict=True)


	print (fornclien," com RETENCAO")
	print j	
	return j





# 
# convert number to words 
# 
def in_words_pt(integer, in_million=True): 
	""" 
	Returns string in words for the given integer. 
	""" 
	n=int(integer) 
 	known = {0: 'zero', 1: 'um', 2: 'dois', 3: 'três', 4: 'quarto', 5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'novo', 10: 'dez', 11: 'onze', 12: 'doze', 13: 'treze', 14: 'catorze', 15: 'quinze', 16: 'dezaseis', 17: 'dezasete', 18: 'dezoito',
19: 'dezanove', 20: 'vinte', 30: 'trinta', 40: 'quarenta', 50: 'cinquenta', 60: 'sessenta', 70: 'setenta', 80: 'oitenta', 90: 'noventa'} 


	def psn(n, known, xpsn): 
		import sys; 
		if n in known: return known[n] 
		bestguess, remainder = str(n), 0 

 
		if n<=20: 
			webnotes.errprint(sys.stderr) 
			webnotes.errprint(n) 
			webnotes.errprint("Como isto aconteceu?") 
			assert 0 
		elif n < 100: 
			bestguess= xpsn((n//10)*10, known, xpsn) + '-' + xpsn(n%10, known, xpsn) 
			return bestguess 
		elif n < 1000: 
			bestguess= xpsn(n//100, known, xpsn) + ' ' + 'cem' 
			remainder = n%100 
		else: 
			if in_million: 
				if n < 1000000: 
					bestguess= xpsn(n//1000, known, xpsn) + ' ' + 'mil' 
					remainder = n%1000 
				elif n < 1000000000: 
					bestguess= xpsn(n//1000000, known, xpsn) + ' ' + 'milhões' 
					remainder = n%1000000 
				else: 
					bestguess= xpsn(n//1000000000, known, xpsn) + ' ' + 'bilhões' 
					remainder = n%1000000000 
			else: 
				if n < 100000: 
					bestguess= xpsn(n//1000, known, xpsn) + ' ' + 'mil' 
					remainder = n%1000 
				elif n < 10000000: 
					bestguess= xpsn(n//100000, known, xpsn) + ' ' + 'cem mil' 
					remainder = n%100000 
				else: 
					bestguess= xpsn(n//10000000, known, xpsn) + ' ' + 'dez milhões' 
					remainder = n%10000000 
		if remainder: 
			if remainder >= 100: 
				comma = ',' 
			else: 
				comma = '' 
			return bestguess + comma + ' ' + xpsn(remainder, known, xpsn) 
		else: 
			return bestguess 


	return psn(n, known, psn) 

@frappe.whitelist()
def get_sample_data():

	return frappe.db.sql("""select * from `tabJournal Entry` """, as_dict=False)

@frappe.whitelist()
def get_escola_ginasio():

	#print frappe.db.get_value("Modulo Ginasio",None,"mod_escola_ginasio")
	print frappe.get_value("Modulo Ginasio",None,"mod_escola_ginasio")
	return frappe.get_value("Modulo Ginasio",None,"mod_escola_ginasio")
	#return frappe.db.get_value("Modulo Ginasio",None,"mod_escola_ginasio")


@frappe.whitelist()
def get_escola_config():


	print frappe.get_value("School Settings",None,"current_academic_year")
	print frappe.get_value("School Settings",None,"current_academic_term")
	return frappe.get_value("School Settings",None,"current_academic_year"), frappe.get_value("School Settings",None,"current_academic_term")

@frappe.whitelist()
def get_cursos(programa):
	return frappe.db.sql('''select course, course_name from `tabProgram Course` where parent = %s''', (programa), as_dict=1)


@frappe.whitelist()
def set_fee_pago(propina,fatura):

	pago = frappe.get_doc('Fees',propina)
	print 'propina paga'
	print pago.outstanding_amount
	
	factura = frappe.get_doc('Sales Invoice',fatura) #self.format_as_links(ss.name)[0]

	if pago.outstanding_amount:
		#PAID
		if pago.grand_total:
			frappe.db.set_value("Fees", propina, "paid_amount", pago.grand_total)
		else:
			frappe.db.set_value("Fees", propina, "paid_amount", pago.total_amount)
		frappe.db.set_value("Fees", propina, "outstanding_amount", 0)
		frappe.db.set_value("Fees", propina, "sales_invoice", fatura)
#		pago.paid_amount = pago.total_amount
#		pago.outstanding_amount = 0
#		pago.save()




@frappe.whitelist()
def get_programa_enroll(aluno):

	print frappe.model.frappe.get_all('Program Enrollment',filters={'student':aluno},fields=['name','student_name','program'])

	print ('segundo ')

	print frappe.db.sql(""" select p.name,p.student,p.student_name,p.program, f.parent,f.fee_structure,f.amount from `tabProgram Fee` f JOIN `tabProgram Enrollment` p on f.parent = p.name where p.student = %s; """, (aluno),as_dict=False)

	return frappe.db.sql(""" select p.name,p.student,p.student_name,p.program, f.parent,f.fee_structure,f.amount from `tabProgram Fee` f JOIN `tabProgram Enrollment` p on f.parent = p.name where p.student = %s; """, (aluno),as_dict=True)



@frappe.whitelist()
def estudante_enroll(source_name):
	"""Creates a Student Record and returns a Program Enrollment.

	:param source_name: Student Applicant.
	"""
	frappe.publish_realtime('enroll_student_progress', {"progress": [1, 4]}, user=frappe.session.user)
	student = get_mapped_doc("Student Applicant", source_name,
		{"Student Applicant": {
			"doctype": "Student",
			"field_map": {
				"name": "student_applicant"
			}
		}}, ignore_permissions=True)

	student.save()

	frappe.db.set_value('Student',student.name,'_user_tags',student.title[0])
	frappe.db.commit()


	#Cria Customer	
	cliente = get_mapped_doc("Student Applicant", source_name,
		{"Student Applicant": {
			"doctype": "Customer",
			"field_map": {
				"name": "student_applicant"
			}
		}}, ignore_permissions=True)

	cliente.customer_name = student.title
	cliente.customer_group = 'Individual'
	cliente.territory = 'Angola'
	cliente.language = 'pt'
	print "ALUNO GENDER"
	print _(student.gender)

	cliente.save()

	frappe.db.set_value('Customer',cliente.name,'_user_tags',student.title[0])
	frappe.db.commit()
	

	contacto = frappe.new_doc("Contact")
	contacto.name = student.title
	contacto.first_name = student.first_name	
	contacto.middle_name = student.middle_name	
	contacto.last_name = student.last_name	
	contacto.gender = student.gender
	contacto.email_id = student.student_email_id
	contacto.mobile_no = student.student_mobile_number
	#contacto.parent

	contacto.status = 'Passive'
	contacto.save()


	contacto_link = frappe.new_doc('Dynamic Link')
	contacto_link.parent = contacto.name
	contacto_link.parentfield ='links'
	contacto_link.parenttype ='Contact'
	contacto_link.link_title = student.title
	contacto_link.link_doctype ='Customer'
	contacto_link.link_name = student.title

	contacto_link.save()


	program_enrollment = frappe.new_doc("Program Enrollment")
	program_enrollment.student = student.name
	program_enrollment.student_name = student.title
	program_enrollment.program = frappe.db.get_value("Student Applicant", source_name, "program")
	frappe.publish_realtime('enroll_student_progress', {"progress": [4, 4]}, user=frappe.session.user)	
	return program_enrollment


@frappe.whitelist()
def update_email_group(doctype, name):
	if not frappe.db.exists("Email Group", name):
		email_group = frappe.new_doc("Email Group")
		email_group.title = name
		email_group.save()
	email_list = []
	students = []
	if doctype == "Student Group":
		students = get_student_group_students(name)
	for stud in students:
		email = frappe.db.get_value("Student", stud.student, "student_email_id")
		print email
		if email:
			email_list.append(email)	
	add_subscribers(name, email_list)

@frappe.whitelist()
def get_student_group_students(student_group, include_inactive=0):
	"""Returns List of student, student_name in Student Group.

	:param student_group: Student Group.
	"""
	if include_inactive:
		students = frappe.get_list("Student Group Student", fields=["student", "student_name"] ,
			filters={"parent": student_group}, order_by= "group_roll_number")
	else:
		students = frappe.get_list("Student Group Student", fields=["student", "student_name"] ,
			filters={"parent": student_group, "active": 1}, order_by= "group_roll_number")
	return students

@frappe.whitelist()
def css_per_user(username=frappe.session.user):
	""" Should load the CSS created on app theme  per user
	
	:param username: currently logged or logging.
	"""

	print 'css per user ', username

	#should look for user folder with CSS and load if not use starndard CSS
	#assets/css/username/.css
	
	#assets/angola_erp/css/erpnext/bootstrap.css
	
	"""	body {
		  font-family: "Helvetica Neue", Helvetica, Arial, "Open Sans", sans-serif;
		  font-size: 10px;
		  line-height: 1.42857143;
		  color: #36414c;
		  background-color: #ff5858;
		}
	"""		
	#script = open ("./assets/angola_erp/js/carregarCSS.js","r")
	#script_content = script.read()

	#script.close()

	#js.exec(script_content)
	

@frappe.whitelist()
def get_versao_erp():
	""" Due to School renamed to Education ....
	
	"""

	print frappe.get_attr("erpnext"+".__version__")

	return frappe.get_attr("erpnext"+".__version__")

@frappe.whitelist()
def cancel_gl_entry_fee(fee_number):
	"""Cancel the GL Entry made by FEE... ONLY if user makes SALES INVOICE LATER FOR ALL GROUP OF Fees...

	:param fee_number.
	"""

	print "Cancela GL ENTRY NO FEE"
	print "Cancela GL ENTRY NO FEE"
	frappe.db.sql('''UPDATE `tabGL Entry` set docstatus = 2 where voucher_no = %s''', (fee_number), as_dict=1)

	print "APAGA GL ENTRY NO FEE"
	print "APAGA GL ENTRY NO FEE"
	frappe.db.sql('''DELETE from `tabGL Entry` where voucher_no = %s''', (fee_number), as_dict=1)


@frappe.whitelist()
def get_dominios_activos():
	"""Returns Active domains .... 

	:param .
	"""

	print "DOMINIOS ACTIVOS"
	print "DOMINIOS ACTIVOS"
	print "DOMINIOS ACTIVOS"
	print "DOMINIOS ACTIVOS"
	tmp = frappe.get_single('Domain Settings')
	
	return frappe.cache().get_value('active_domains',tmp)



