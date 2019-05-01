# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

#Helkyd
#Modified 13-02-2019

from __future__ import unicode_literals
import frappe, erpnext, json
from frappe import _, scrub, ValidationError
from frappe.utils import flt, comma_or, nowdate
from erpnext.accounts.utils import get_outstanding_invoices, get_account_currency, get_balance_on
from erpnext.accounts.party import get_party_account
from erpnext.accounts.doctype.journal_entry.journal_entry import get_default_bank_cash_account
from erpnext.setup.utils import get_exchange_rate
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.hr.doctype.expense_claim.expense_claim import update_reimbursed_amount
from erpnext.controllers.accounts_controller import AccountsController


import angola_erp
from angola_erp.util.cambios import cambios
from angola_erp.util.angola import get_lista_retencoes
from angola_erp.util.angola import get_taxa_retencao
from angola_erp.util.angola import get_taxa_ipc

from angola_erp.util.angola import cancel_gl_entry_fee

def setup_party_account_field(doc):
	doc.party_account_field = None
	doc.party_account = None
	doc.party_account_currency = None

	if doc.payment_type == "Receive":
		doc.party_account_field = "paid_from"
		doc.party_account = doc.paid_from
		doc.party_account_currency = doc.paid_from_account_currency

	elif doc.payment_type == "Pay":
		doc.party_account_field = "paid_to"
		doc.party_account = doc.paid_to
		doc.party_account_currency = doc.paid_to_account_currency



def validate(doc,method):
	print "VALIDAR PAGAMENTO !!!!"
	print "VALIDAR PAGAMENTO !!!!"
	print "VALIDAR PAGAMENTO !!!!"
	print "VALIDAR PAGAMENTO !!!!"

def on_submit(doc,method):
	print 'ENTRADA PAGAMENTO  - NO SUBMIT '
	print 'ENTRADA PAGAMENTO  - NO SUBMIT '
	print 'ENTRADA PAGAMENTO  - NO SUBMIT '


	#++++++++++ FEEs
	#Cancel GL 
	#Deve primeiro cancelar a GL entry feita para criar a Factura...
	tem_Educacao = False;
	tmp = frappe.get_single('Domain Settings')
	print('Dominios ', tmp)
	if tmp:
		for dominios in tmp.active_domains: # frappe.cache().get_value('active_domains',tmp):
			if dominios.domain == "Education":
				tem_Educacao = True;

	if tem_Educacao:
		print "TEM DOMINIO EDUCACAO SELECT"
		print "TEM DOMINIO EDUCACAO SELECT"
		for refs in doc.get("references"):
			print refs.reference_name
			factura = frappe.get_doc("Sales Invoice", refs.reference_name)
			print factura
			for prop in factura.get("propina"):
				print prop.propina
				cancel_gl_entry_fee(prop.propina)

				#Agora clear outstanding from Fees	
				frappe.db.set_value("Fees",prop.propina, "paid_amount", prop.valor)
				frappe.db.set_value("Fees",prop.propina, "outstanding_amount", 0)
				frappe.db.commit()
	
			
	#++++++++++ FEES

	global ipc_temp

	ipc_temp = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '3771%%'  """,(doc.company), as_dict=True)

	global ipc_

	ipc_ = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '3421%%'  """,(doc.company), as_dict=True)

	global is_temp

	is_temp = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '7531%%'  """,(doc.company), as_dict=True)

	global is_

	is_ = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '3471%%'  """,(doc.company), as_dict=True)


	#global iv_temp
	#iv_temp = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '3422%%'  """,(doc.company), as_dict=True)

	global iv_

	iv_ = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '3422%%'  """,(doc.company), as_dict=True)



	#Busca percentagem IPC e Imposto de Selo

	global retencoes_ipc

	retencoes_ipc = frappe.db.sql(""" SELECT name, descricao, percentagem, metade_do_valor, isencao, data_limite from `tabRetencoes` where name like 'ipc' """,as_dict=True)

	global retencoes_is

	retencoes_is = frappe.db.sql(""" SELECT name, descricao, percentagem, metade_do_valor, isencao, data_limite from `tabRetencoes` where name like 'imposto de selo' """,as_dict=True)


	global retencoes_iv

	retencoes_iv = frappe.db.sql(""" SELECT name, descricao, percentagem, metade_do_valor, isencao, data_limite from `tabRetencoes` where name like 'imposto valor acrescentado' or name like 'iva' """,as_dict=True)

	#Busca percentagem Imposto Industrial

	#NAO PRECISA DE TEMPORARIO......
	global ii_temp

	ii_temp = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '3419%%'  """,(doc.company), as_dict=True)

	global ii_
	#Imposto por conta
	ii_ = frappe.db.sql(""" select name, account_name, account_currency, company  from `tabAccount` where company = %s and name like '3412%%'  """,(doc.company), as_dict=True)

	#FIM Ainda por fazer

	global retencoes_ii

	retencoes_ii = frappe.db.sql(""" SELECT name, descricao, percentagem, metade_do_valor, isencao, data_limite from `tabRetencoes` where name like '%industrial%' """,as_dict=True)


	global valor_IPC
	global valor_IVA

	valor_IPC = 0
	valor_IVA = 0

	doc.setup_party_account_field()
	if doc.difference_amount:
		frappe.throw(_("Difference Amount must be zero"))
	make_gl_entries1(doc)
	#doc.update_outstanding_amounts()
	#doc.update_advance_paid()
	#doc.update_expense_claim()


def make_gl_entries1(doc, cancel=0, adv_adj=0):
	print('MAKE GL ENTRIES 1...')

	if doc.payment_type in ("Receive", "Pay") and not doc.get("party_account_field"):
		doc.setup_party_account_field()

	#Check if more than one payment ....



	gl_entries = []

	# 3771 (D) IPC to 3421 (C)
	#Tem que verificar Fact se tem IPC por pagar .... e qual o valor
	calculaIPC = False
	calculaIVA = False
	for d in doc.get("references"):
		if d.reference_doctype in ("Sales Invoice"):
			tempIPC = frappe.get_doc(d.reference_doctype, d.reference_name)
			print "Sales Invoice - TEMPIPC"
			print tempIPC.name
			print tempIPC.taxes_and_charges
			if tempIPC.taxes_and_charges:
				#check if IPC or IVA
				global valor_IPC
				global valor_IVA
				print doc.name
				print tempIPC.taxes_and_charges
				taxasencs = frappe.db.sql(""" select * from `tabSales Taxes and Charges` where parent = %s""",(doc.name),as_dict=True)
				print taxasencs
				for taxaenc in taxasencs:
					if "3422" in taxaenc.account_head:
						#IVA
						valor_IVA += tempIPC.total_taxes_and_charges
						calculaIVA = False
						calculaIPC = False
					else:
						valor_IPC += tempIPC.total_taxes_and_charges
						calculaIPC = True

	if calculaIPC and doc.party_type != _("Employee"):
		print "IPC EMPLOYEE"
		add_party_gl_entries1(doc, gl_entries)
		add_bank_gl_entries1(doc, gl_entries)

	if doc.party_type != _("Supplier") and doc.party_type != _("Employee") and doc.party_type != "Supplier":
		print "II EMPLOYEE"
		#Verify if isencao
		print retencoes_is[0].isencao
		print retencoes_is[0].descricao
		print retencoes_is[0].data_limite
		

		if retencoes_is[0].isencao == 0:
			# 3471 (C) IPC to 7531 (D)
			#IS always
			add_party_gl_entries2(doc, gl_entries)
			add_bank_gl_entries2(doc, gl_entries)
		elif retencoes_is[0].isencao == 1  and retencoes_is[0].data_limite.strftime("%Y-%m-%d") < frappe.utils.nowdate():
			print "expirou pode processar"
			print "expirou pode processar"
			# 3471 (C) IPC to 7531 (D)
			#IS always
			add_party_gl_entries2(doc, gl_entries)
			add_bank_gl_entries2(doc, gl_entries)


		#return
		#Imposto Industrial
		# 3412 (C) to 3419 (D)
		if retencoes_ii[0].isencao == 0:
			#somente if retencoes_is[0].isencao == 1
			if retencoes_is[0].isencao == 1 and retencoes_is[0].data_limite.strftime("%Y-%m-%d") > frappe.utils.nowdate():
				print "IMPOSTO INDUSTRIAL"
				print "IMPOSTO INDUSTRIAL"
				print "IMPOSTO INDUSTRIAL"
				print "IMPOSTO INDUSTRIAL"
				add_party_gl_entries3(doc, gl_entries)
				add_bank_gl_entries3(doc, gl_entries)


	#doc.add_deductions_gl_entries(gl_entries)
	#add_deductions_gl_entries(doc, gl_entries)

	print "make_gl_entries"
	print "make_gl_entries"
	print "make_gl_entries"
	print(gl_entries)
	make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj)



def update_outstanding_amounts(doc):
	doc.set_missing_ref_details(force=True)


def update_advance_paid(doc):
	if doc.payment_type in ("Receive", "Pay") and doc.party:
		for d in doc.get("references"):
			if d.allocated_amount \
				and d.reference_doctype in ("Sales Order", "Purchase Order", "Employee Advance"):
					frappe.get_doc(d.reference_doctype, d.reference_name).set_total_advance_paid()


def update_expense_claim(doc):
	if doc.payment_type in ("Pay") and doc.party:
		for d in doc.get("references"):
			if d.reference_doctype=="Expense Claim" and d.reference_name:
				doc = frappe.get_doc("Expense Claim", d.reference_name)
				update_reimbursed_amount(doc)



def add_party_gl_entries1(doc, gl_entries):
	#Modificado para incluir IPC 3771 para 3421

	print "VERIFICA SE TEM IPC TEMP"
	print "VERIFICA SE TEM IPC TEMP"
	if ipc_temp:
		print "TEM IPC TEMP"
		print "TEM IPC TEMP"
		print "TEM IPC TEMP"

		#if doc.payment_type=="Receive":
		#	against_account = doc.paid_to
		#else:
		#	against_account = doc.paid_from


		party_gl_dict = doc.get_gl_dict({
			"account": ipc_[0].name,
			#"party_type": doc.party_type,
			#"party": doc.party,
			#"against": against_account,
			"account_currency": ipc_[0].account_currency
		})

		dr_or_cr = "credit" #if doc.party_type in ["Customer", "Student"] else "debit"

		allocated_amount_in_company_currency = 0

		gle = party_gl_dict.copy()
		for d in doc.get("references"):
#			gle = party_gl_dict.copy()

#			gle.update({
#				"against_voucher_type": d.reference_doctype,
#				"against_voucher": d.reference_name
#			})
			print "IPC "
			tempIPC = frappe.get_doc(d.reference_doctype, d.reference_name)
			print tempIPC.total_taxes_and_charges
			if tempIPC.total_taxes_and_charges:	#<>0
				if d.outstanding_amount == 0:
					print "POE O IPC"
					print tempIPC.total_taxes_and_charges
	#				valor_IPC = tempIPC.total_taxes_and_charges
	#				print valor_IPC
					print (flt(tempIPC.total_taxes_and_charges) * flt(d.exchange_rate),doc.precision("paid_amount"))
					allocated_amount_in_company_currency += tempIPC.total_taxes_and_charges # (flt(tempIPC.total_taxes_and_charges) * flt(d.exchange_rate),doc.precision("paid_amount"))

					#print (flt(flt(d.allocated_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_ipc[0].percentagem) / 100
					#allocated_amount_in_company_currency = (flt(flt(d.allocated_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_ipc[0].percentagem) / 100

#					gle.update({
#						dr_or_cr + "_in_account_currency": tempIPC.total_taxes_and_charges,
#						dr_or_cr: allocated_amount_in_company_currency
#					})

#					gl_entries.append(gle)
				else:
					global valor_IPC

					valor_IPC = 0
		#Update
		gle.update({
			dr_or_cr + "_in_account_currency": tempIPC.total_taxes_and_charges,
			dr_or_cr: allocated_amount_in_company_currency
		})

		gl_entries.append(gle)


#		if doc.unallocated_amount:
#			base_unallocated_amount = base_unallocated_amount = doc.unallocated_amount * \
#				(doc.source_exchange_rate if doc.payment_type=="Receive" else doc.target_exchange_rate)

#			gle = party_gl_dict.copy()

#			gle.update({
#				dr_or_cr + "_in_account_currency": doc.unallocated_amount,
#				dr_or_cr: base_unallocated_amount
#			})

#			gl_entries.append(gle)

def add_bank_gl_entries1(doc, gl_entries):
	#if doc.payment_type in ("Pay", "Internal Transfer"):
	#	gl_entries.append(
	#		doc.get_gl_dict({
	#			"account": doc.paid_from,
	#			"account_currency": doc.paid_from_account_currency,
	#			"against": doc.party if doc.payment_type=="Pay" else doc.paid_to,
	#			"credit_in_account_currency": doc.paid_amount,
	#			"credit": doc.base_paid_amount
	#		})
	#	)

	print "add_bank_gl_entries1"
	print "BANK GL"
	print "BANK GL"
	print valor_IPC

	if doc.payment_type in ("Receive", "Internal Transfer"):
		gl_entries.append(
			doc.get_gl_dict({
				"account": ipc_temp[0].name,
				"account_currency": ipc_temp[0].account_currency,
				#"against": doc.party if doc.payment_type=="Receive" else doc.paid_from,
				"debit_in_account_currency": valor_IPC,
				"debit": valor_IPC
			})
		)

#Imposto de Selo
def add_party_gl_entries2(doc, gl_entries):

	print "add_party_gl_entries2"
	print "VERIFICA SE TEM IS TEMP"
	print "VERIFICA SE TEM IS TEMP"
	centro_custo = frappe.get_value("Company",doc.company,"cost_center")

	if is_temp:
		print "TEM IS TEMP"
		print "TEM IS TEMP"
		print "TEM IS TEMP"
		print centro_custo
		#if doc.payment_type=="Receive":
		#	against_account = doc.paid_to
		#else:
		#	against_account = doc.paid_from


		party_gl_dict = doc.get_gl_dict({
			"account": is_[0].name,
			#"party_type": doc.party_type,
			#"party": doc.party,
			"against": is_temp[0].name,
			"account_currency": is_[0].account_currency,
			"cost_center": centro_custo
		})

		dr_or_cr = "credit" #if doc.party_type in ["Customer", "Student"] else "debit"

		allocated_amount_in_company_currency = 0

		gle = party_gl_dict.copy()
	
		#References for Sales Invoice or Fees
		for d in doc.get("references"):
#			gle = party_gl_dict.copy()
#			gle.update({
#				"against_voucher_type": d.reference_doctype,
#				"against_voucher": d.reference_name
#			})
			print "IPC "
			print "valor Pago ", doc.paid_amount
			print doc.received_amount
			print (flt(flt(d.allocated_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_is[0].percentagem) / 100
			print (flt(flt(doc.paid_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_is[0].percentagem) / 100
			allocated_amount_in_company_currency = (flt(flt(doc.paid_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_is[0].percentagem) / 100
			#allocated_amount_in_company_currency += (flt(flt(d.allocated_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_is[0].percentagem) / 100

		
		gle.update({
			dr_or_cr + "_in_account_currency": (doc.paid_amount * retencoes_is[0].percentagem) / 100,
			dr_or_cr: allocated_amount_in_company_currency
		})

		gl_entries.append(gle)

#		if doc.unallocated_amount:
#			base_unallocated_amount = base_unallocated_amount = doc.unallocated_amount * \
#				(doc.source_exchange_rate if doc.payment_type=="Receive" else doc.target_exchange_rate)

#			gle = party_gl_dict.copy()

#			gle.update({
#				dr_or_cr + "_in_account_currency": doc.unallocated_amount,
#				dr_or_cr: base_unallocated_amount
#			})

#			gl_entries.append(gle)

def add_bank_gl_entries2(doc, gl_entries):
	print "ADD BANK GL ENTRIES 2"
	centro_custo = frappe.get_value("Company",doc.company,"cost_center")

	#if doc.payment_type in ("Pay", "Internal Transfer"):
	#	gl_entries.append(
	#		doc.get_gl_dict({
	#			"account": doc.paid_from,
	#			"account_currency": doc.paid_from_account_currency,
	#			"against": doc.party if doc.payment_type=="Pay" else doc.paid_to,
	#			"credit_in_account_currency": doc.paid_amount,
	#			"credit": doc.base_paid_amount
	#		})
	#	)
	if doc.payment_type in ("Receive", "Internal Transfer"):
		gl_entries.append(
			doc.get_gl_dict({
				"account": is_temp[0].name,
				"account_currency": is_temp[0].account_currency,
				"against": is_[0].name,
				"debit_in_account_currency": (doc.received_amount * retencoes_is[0].percentagem) / 100,
				"debit": (doc.base_received_amount * retencoes_is[0].percentagem) / 100,
				"cost_center": centro_custo
			})
		)


#Imposto Industrial
def add_party_gl_entries3(doc, gl_entries):

	print "add_party_gl_entries3"
	print "VERIFICA SE TEM IIndustrial TEMP"
	print "VERIFICA SE TEM IIndustrial TEMP"
	centro_custo = frappe.get_value("Company",doc.company,"cost_center")

	if ii_temp:
		print "TEM IIndustrial TEMP"
		print "TEM IIndustrial TEMP"
		print "TEM IIndustrial TEMP"

		#if doc.payment_type=="Receive":
		#	against_account = doc.paid_to
		#else:
		#	against_account = doc.paid_from


		party_gl_dict = doc.get_gl_dict({
			"account": ii_[0].name,
			#"party_type": doc.party_type,
			#"party": doc.party,
			"against": ii_temp[0].name,
			"account_currency": ii_[0].account_currency,
			"cost_center": centro_custo
		})

		dr_or_cr = "credit" #if doc.party_type in ["Customer", "Student"] else "debit"

		allocated_amount_in_company_currency = 0

		gle = party_gl_dict.copy()
		for d in doc.get("references"):
#			gle = party_gl_dict.copy()
#			gle.update({
#				"against_voucher_type": d.reference_doctype,
#				"against_voucher": d.reference_name
#			})
			print "IPC "
			print "valor Pago ", doc.paid_amount
			print doc.received_amount
			print (flt(flt(d.allocated_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_ii[0].percentagem) / 100
			print (flt(flt(doc.paid_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_ii[0].percentagem) / 100
			allocated_amount_in_company_currency = (flt(flt(doc.paid_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_ii[0].percentagem) / 100
			#allocated_amount_in_company_currency += (flt(flt(d.allocated_amount) * flt(d.exchange_rate),doc.precision("paid_amount")) * retencoes_is[0].percentagem) / 100

		gle.update({
			dr_or_cr + "_in_account_currency": (doc.paid_amount * retencoes_ii[0].percentagem) / 100,
			dr_or_cr: allocated_amount_in_company_currency
		})

		gl_entries.append(gle)

#		if doc.unallocated_amount:
#			base_unallocated_amount = base_unallocated_amount = doc.unallocated_amount * \
#				(doc.source_exchange_rate if doc.payment_type=="Receive" else doc.target_exchange_rate)

#			gle = party_gl_dict.copy()

#			gle.update({
#				dr_or_cr + "_in_account_currency": doc.unallocated_amount,
#				dr_or_cr: base_unallocated_amount
#			})

#			gl_entries.append(gle)

def add_bank_gl_entries3(doc, gl_entries):
	print "ADD BANK GL ENTRIES 3...."
	centro_custo = frappe.get_value("Company",doc.company,"cost_center")

	#if doc.payment_type in ("Pay", "Internal Transfer"):
	#	gl_entries.append(
	#		doc.get_gl_dict({
	#			"account": doc.paid_from,
	#			"account_currency": doc.paid_from_account_currency,
	#			"against": doc.party if doc.payment_type=="Pay" else doc.paid_to,
	#			"credit_in_account_currency": doc.paid_amount,
	#			"credit": doc.base_paid_amount
	#		})
	#	)
	if doc.payment_type in ("Receive", "Internal Transfer"):
		gl_entries.append(
			doc.get_gl_dict({
				"account": ii_temp[0].name,
				"account_currency": ii_temp[0].account_currency,
				"against": ii_[0].name,
				"debit_in_account_currency": (doc.received_amount * retencoes_ii[0].percentagem) / 100,
				"debit": (doc.base_received_amount * retencoes_ii[0].percentagem) / 100,
				"cost_center": centro_custo
			})
		)

def add_deductions_gl_entries(doc, gl_entries):

	print "add_deductions_gl_entries"
	print "add_deductions_gl_entries"
	print "add_deductions_gl_entries"

	for d in doc.get("deductions"):
		if d.amount:
			account_currency = get_account_currency(d.account)
			if account_currency != doc.company_currency:
				frappe.throw(_("Currency for {0} must be {1}").format(d.account, doc.company_currency))

			gl_entries.append(
				doc.get_gl_dict({
					"account": d.account,
					"account_currency": account_currency,
					"against": doc.party or doc.paid_from,
					"debit_in_account_currency": d.amount,
					"debit": d.amount,
					"cost_center": d.cost_center
				})
			)

#===========
