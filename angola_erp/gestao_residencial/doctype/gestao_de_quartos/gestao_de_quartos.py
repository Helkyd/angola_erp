# -*- coding: utf-8 -*-
# Copyright (c) 2015, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime, timedelta
from frappe.utils import cstr, get_datetime, getdate, cint, get_datetime_str, flt
from frappe.model.document import Document
from frappe.model.naming import make_autoname

import erpnext
from erpnext.controllers.stock_controller import update_gl_entries_after
from erpnext.controllers.selling_controller import SellingController
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from erpnext.stock.get_item_details import get_pos_profile
from erpnext.accounts.utils import get_fiscal_year

#from erpnext.controllers.selling_controller import update_stock_ledger
#import erpnext.controllers.selling_controller



form_grid_templates = {
	"items": "templates/form_grid/gestao_quartos_list.html"
}

#class GestaodeQuartos(SalesInvoice):
class GestaodeQuartos(Document):

	def autoname(self):
		self.name = make_autoname(self.numero_quarto + '-' + '.#####')


	def validate(self):
		#super(GestaodeQuartos, self).validate()
		print "DOC STATUS"
		print self.name
		print self.docstatus
		self.Validar_Numero_Dias()
		self.Check_ContaCorrente()
		self.Sethoras_Quarto()
		self.Contas_Correntes()

		self.validate_debit_to_acc()
		self.validate_stocks()
		self.set_against_income_account()


	def Validar_Numero_Dias(self):
		if self.horas <= 0:
			validated=False
			frappe.throw(_("Horas/Dias tem que ser 1 ou mais."))

		elif self.hora_entrada == self.hora_saida:
			validated=False
			frappe.throw(_("Hora de Saida tem que sair diferente que Hora de Entrada."))


	def on_update(self):
		self.Quartos_Status()
		self.Reservas_Status()
		#self.valor_pago = self.total_servicos


	def Quartos_Status(self):

		# Change Quarto status 
		quarto = frappe.get_doc("Quartos", self.numero_quarto)
		
		if self.status_quarto == "Ocupado":
			quarto.status_quarto = "Ocupado"
		elif self.status_quarto == "Ativo":
			quarto.status_quarto = "Ocupado"
		elif self.status_quarto == "Livre":
			quarto.status_quarto = "Livre"
		elif self.status_quarto == "Fechado":
			quarto.status_quarto = "Livre"

		quarto.save()		

	def Reservas_Status(self):
		#Change Reservas status
		if (self.status_quarto == "Fechado") and  (self.reserva_numero != None) :
			reserva = frappe.get_doc("Reservas",self.reserva_numero)
			reserva.reservation_status = "Fechada"
			reserva.save()
			
			

	def Check_ContaCorrente(self):

		if (self.servico_pago_por=="Conta-Corrente"):
			self.nome_cliente = self.conta_corrente
			if (self.conta_corrente == "") or (self.conta_corrente == "nome do cliente"):
				validated= False
				frappe.throw(_("Nao foi selecionado o Cliente para Conta-Corrente."))

#			validated= False
#			frappe.throw(_("Modulo nao funcional de momento."))

		if (self.pagamento_por=="Conta-Corrente"):
			if (self.conta_corrente == "") or (self.conta_corrente == "nome do cliente"):
				validated= False
				frappe.throw(_("Nao foi selecionado o Cliente para Conta-Corrente."))


	def Sethoras_Quarto(self):
		
		if self.hora_diaria_noite == "Noite":			
			self.hora_saida= get_datetime(self.hora_entrada) + timedelta(hours=12)			
		elif self.hora_diaria_noite == "Diaria":
			self.hora_saida= get_datetime(self.hora_entrada) + timedelta(days=self.horas)
		elif self.hora_diaria_noite == "Hora":
			self.hora_saida = get_datetime(self.hora_entrada) + timedelta(hours=self.horas)

		print "DEPOIS DE CALCULAR"
		print self.hora_saida


	def Contas_Correntes(self):
				#aproveita criar ja o registo no Conta-correntes
		if (self.conta_corrente !="nome do cliente") and (self.conta_corrente !=None) and (self.status_quarto == "Fechado") and (self.conta_corrente_status == "Não Pago") :
			if (frappe.db.sql("""select cc_nome_cliente from `tabContas Correntes` WHERE cc_nome_cliente =%s """,self.conta_corrente, as_dict=False)) != ():
				#existe faz os calculos da divida
				print " CLIENTE JA EXISTE"
				ccorrente = frappe.get_doc("Contas Correntes", self.conta_corrente)
				print "CLIENTE"
				print ccorrente.name

				totalextra = 0

				cc_detalhes = frappe.new_doc("CC_detalhes")
				cc_detalhes.parent = ccorrente.name
				cc_detalhes.parentfield = "cc_table_detalhes"
				cc_detalhes.parenttype = "Contas Correntes"
					
				cc_detalhes.descricao_servico = self.name #extras.nome_servico
				cc_detalhes.name = self.name
				cc_detalhes.numero_registo = self.name
				cc_detalhes.total = self.total #extras.total_extra
				cc_detalhes.total_servicos = self.total_servicos #extras.total_extra
				cc_detalhes.data_registo = self.hora_entrada
				totalextra = totalextra + self.total_servicos  + self.total #extras.total_extra

				cc_detalhes.status_conta_corrente = "Não Pago"
				cc_detalhes.tipo = "Quarto"
				cc_detalhes.idx += 1	
					
				cc_detalhes.insert()

				print (ccorrente.cc_valor_divida + totalextra)
				ccorrente.cc_valor_divida = flt(ccorrente.cc_valor_divida) + totalextra
				#ccorrente.save()

			else:
				#novo
				print " CLIENTE NAO EXISTE"
				print self.conta_corrente
				ccorrente = frappe.new_doc("Contas Correntes")
				ccorrente.cc_nome_cliente = self.conta_corrente
				ccorrente.name = self.conta_corrente
				ccorrente.cc_status_conta_corrente = "Não Pago"
				ccorrente.insert()

				print "CONTAS CORRENTES FEITA !!!!!!"

				totalextra = 0

				cc_detalhes = frappe.new_doc("CC_detalhes")
				cc_detalhes.parent =ccorrente.name
				cc_detalhes.parentfield = "cc_table_detalhes"
				cc_detalhes.parenttype = "Contas Correntes"

					#print extras.nome_servico
				cc_detalhes.descricao_servico = self.name #extras.nome_servico
				cc_detalhes.name = self.name
				cc_detalhes.numero_registo = self.name
				cc_detalhes.total = self.total #extras.total_extra
				cc_detalhes.total_servicos = self.total_servicos #extras.total_extra
				cc_detalhes.data_registo = self.hora_entrada
				totalextra = totalextra + self.total_servicos  + self.total #extras.total_extra

				cc_detalhes.status_conta_corrente = "Não Pago"
				cc_detalhes.tipo = "Quarto"
				cc_detalhes.insert()

				ccorrente.cc_valor_divida = flt(ccorrente.cc_valor_divida) + totalextra

	def validate_debit_to_acc(self):
		account = frappe.db.get_value("Account", self.debit_to,
			["account_type", "report_type", "account_currency"], as_dict=True)

		if not account:
			frappe.throw(_("Debit To is required"))

		if account.report_type != "Balance Sheet":
			frappe.throw(_("Debit To account must be a Balance Sheet account"))

		if self.nome_cliente and account.account_type != "Receivable":
			frappe.throw(_("Debit To account must be a Receivable account"))

		#self.party_account_currency = account.account_currency

	def validate_stocks(self):
#		if cint(self.update_stock):
		print ("Validar os Stocks")
#		self.validate_dropship_item()
#		self.validate_item_code()
		self.validate_warehouse()
		self.actualiza_stock_corrente()
#		self.validate_delivery_note()

		self.update_stock_ledger()

	def set_against_income_account(self):
		"""Set against account for debit to account"""
		against_acc = []
		for d in self.get('servicos'):
			if d.income_account not in against_acc:
				against_acc.append(d.income_account)
		#return against_acc
		self.against_income_account = ','.join(against_acc)

	def actualiza_stock_corrente(self):
			print ("Atualizar Stocks")
			for d in self.get('servicos'):
				if d.servico_produto:
					bin = frappe.db.sql("select actual_qty from `tabBin` where item_code = %s", d.servico_produto, as_dict = 1)
					d.actual_qty = bin and flt(bin[0]['actual_qty']) or 0

	def validate_warehouse(self):
		pos_profile = get_pos_profile(self.company) or {}
		print (pos_profile)
		for d in self.get('servicos'):
			print (d.servico_produto)
			artigo = frappe.get_doc("Item", d.servico_produto)
			d.warehouse = pos_profile['warehouse'] or artigo.default_warehouse
			d.income_account = pos_profile['income_account'] or artigo.income_account
			d.cost_center = pos_profile['cost_center'] or artigo.selling_cost_center
#			d.save()
	

	def update_stock_ledger(self):
#		self.update_reserved_qty()

		sl_entries = []
		for d in self.get('servicos'): # self.get_item_list():
			if frappe.db.get_value("Item", d.servico_produto, "is_stock_item") == 1 and flt(d.quantidade):
				return_rate = 0
#				if cint(self.is_return) and self.return_against and self.docstatus==1:
#					return_rate = self.get_incoming_rate_for_sales_return(d.item_code, self.return_against)
				print (d.servico_produto)
				print ("doctstatus ", self.docstatus)
				if d.warehouse and self.docstatus==0:
						sl_entries.append(self.get_sl_entries(d, {
							"actual_qty": -1*flt(d.quantidade),
							"incoming_rate": return_rate
						}))

		print ("Upd stock SL ENTRIES")
		print (sl_entries)
#		self.make_sl_entries(sl_entries)


	def get_sl_entries(self, d, args):
		print ("produto ",d.get("servico_produto", None))
		print ("armazem ",d.get("warehouse", None))
		print ("hora ", self.hora_entrada)
		print ("fiscal ", get_fiscal_year(self.hora_entrada, company=self.company)[0])



		sl_dict = frappe._dict({
			"item_code": d.get("servico_produto", None),
			"warehouse": d.get("warehouse", None),
			"posting_date": self.hora_entrada,
			"posting_time": self.hora_entrada,
			'fiscal_year': get_fiscal_year(self.hora_entrada, company=self.company)[0],
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"voucher_detail_no": d.name,
			"actual_qty": (self.docstatus==1 and 1 or -1)*flt(d.get("stock_qty")),
			"stock_uom": frappe.db.get_value("Item", args.get("item_code") or d.get("servico_produto"), "stock_uom"),
			"incoming_rate": 0,
			"company": self.company,
#			"batch_no": cstr(d.get("batch_no")).strip(),
#			"serial_no": d.get("serial_no"),
#			"project": d.get("project"),
			"is_cancelled": self.docstatus==2 and "Yes" or "No"
		})

		sl_dict.update(args)
		print ("SL Dict")
		print (sl_dict)

		return sl_dict

	def make_sl_entries(self, sl_entries, is_amended=None, allow_negative_stock=False,
			via_landed_cost_voucher=False):
		from erpnext.stock.stock_ledger import make_sl_entries
		make_sl_entries(sl_entries, is_amended, allow_negative_stock, via_landed_cost_voucher)


	def make_gl_entries(self, repost_future_gle=True):
		if not self.grand_total:
			return
		gl_entries = self.get_gl_entries()

		if gl_entries:
			from erpnext.accounts.general_ledger import make_gl_entries

			# if POS and amount is written off, updating outstanding amt after posting all gl entries
			update_outstanding = "No" if (cint(self.is_pos) or self.write_off_account) else "Yes"

			make_gl_entries(gl_entries, cancel=(self.docstatus == 2),
				update_outstanding=update_outstanding, merge_entries=False)

			if update_outstanding == "No":
				from erpnext.accounts.doctype.gl_entry.gl_entry import update_outstanding_amt
				update_outstanding_amt(self.debit_to, "Customer", self.customer,
					self.doctype, self.return_against if cint(self.is_return) else self.name)

			if repost_future_gle and cint(self.update_stock) \
				and cint(frappe.defaults.get_global_default("auto_accounting_for_stock")):
					items, warehouses = self.get_items_and_warehouses()
					update_gl_entries_after(self.posting_date, self.posting_time, warehouses, items)
		elif self.docstatus == 2 and cint(self.update_stock) \
			and cint(frappe.defaults.get_global_default("auto_accounting_for_stock")):
				from erpnext.accounts.general_ledger import delete_gl_entries
				delete_gl_entries(voucher_type=self.doctype, voucher_no=self.name)

	def get_gl_entries(self, warehouse_account=None):
		from erpnext.accounts.general_ledger import merge_similar_entries

		gl_entries = []

		self.make_customer_gl_entry(gl_entries)

		self.make_tax_gl_entries(gl_entries)

		self.make_item_gl_entries(gl_entries)

		# merge gl entries before adding pos entries
		gl_entries = merge_similar_entries(gl_entries)

		self.make_pos_gl_entries(gl_entries)
		self.make_gle_for_change_amount(gl_entries)

		self.make_write_off_gl_entry(gl_entries)

		return gl_entries

	def make_customer_gl_entry(self, gl_entries):
		if self.grand_total:
			# Didnot use base_grand_total to book rounding loss gle
			grand_total_in_company_currency = flt(self.grand_total * self.conversion_rate,
				self.precision("grand_total"))

			gl_entries.append(
				self.get_gl_dict({
					"account": self.debit_to,
					"party_type": "Customer",
					"party": self.customer,
					"against": self.against_income_account,
					"debit": grand_total_in_company_currency,
					"debit_in_account_currency": grand_total_in_company_currency \
						if self.party_account_currency==self.company_currency else self.grand_total,
					"against_voucher": self.return_against if cint(self.is_return) else self.name,
					"against_voucher_type": self.doctype
				}, self.party_account_currency)
			)

	def make_tax_gl_entries(self, gl_entries):
		for tax in self.get("taxes"):
			if flt(tax.base_tax_amount_after_discount_amount):
				account_currency = get_account_currency(tax.account_head)
				gl_entries.append(
					self.get_gl_dict({
						"account": tax.account_head,
						"against": self.customer,
						"credit": flt(tax.base_tax_amount_after_discount_amount),
						"credit_in_account_currency": flt(tax.base_tax_amount_after_discount_amount) \
							if account_currency==self.company_currency else flt(tax.tax_amount_after_discount_amount),
						"cost_center": tax.cost_center
					}, account_currency)
				)

	def make_item_gl_entries(self, gl_entries):
		# income account gl entries
		for item in self.get("items"):
			if flt(item.base_net_amount):
				if item.is_fixed_asset:
					asset = frappe.get_doc("Asset", item.asset)

					fixed_asset_gl_entries = get_gl_entries_on_asset_disposal(asset, item.base_net_amount)
					for gle in fixed_asset_gl_entries:
						gle["against"] = self.customer
						gl_entries.append(self.get_gl_dict(gle))

					asset.db_set("disposal_date", self.posting_date)
					asset.set_status("Sold" if self.docstatus==1 else None)
				else:
					account_currency = get_account_currency(item.income_account)
					gl_entries.append(
						self.get_gl_dict({
							"account": item.income_account,
							"against": self.customer,
							"credit": item.base_net_amount,
							"credit_in_account_currency": item.base_net_amount \
								if account_currency==self.company_currency else item.net_amount,
							"cost_center": item.cost_center
						}, account_currency)
					)

		# expense account gl entries
		if cint(frappe.defaults.get_global_default("auto_accounting_for_stock")) \
				and cint(self.update_stock):
			gl_entries += super(SalesInvoice, self).get_gl_entries()

	def make_pos_gl_entries(self, gl_entries):
		if cint(self.is_pos):
			for payment_mode in self.payments:
				if payment_mode.amount:
					# POS, make payment entries
					gl_entries.append(
						self.get_gl_dict({
							"account": self.debit_to,
							"party_type": "Customer",
							"party": self.customer,
							"against": payment_mode.account,
							"credit": payment_mode.base_amount,
							"credit_in_account_currency": payment_mode.base_amount \
								if self.party_account_currency==self.company_currency \
								else payment_mode.amount,
							"against_voucher": self.return_against if cint(self.is_return) else self.name,
							"against_voucher_type": self.doctype,
						}, self.party_account_currency)
					)

					payment_mode_account_currency = get_account_currency(payment_mode.account)
					gl_entries.append(
						self.get_gl_dict({
							"account": payment_mode.account,
							"against": self.customer,
							"debit": payment_mode.base_amount,
							"debit_in_account_currency": payment_mode.base_amount \
								if payment_mode_account_currency==self.company_currency \
								else payment_mode.amount
						}, payment_mode_account_currency)
					)
				
	def make_gle_for_change_amount(self, gl_entries):
		if cint(self.is_pos) and self.change_amount:
			if self.account_for_change_amount:
				gl_entries.append(
					self.get_gl_dict({
						"account": self.debit_to,
						"party_type": "Customer",
						"party": self.customer,
						"against": self.account_for_change_amount,
						"debit": flt(self.base_change_amount),
						"debit_in_account_currency": flt(self.base_change_amount) \
							if self.party_account_currency==self.company_currency else flt(self.change_amount),
						"against_voucher": self.return_against if cint(self.is_return) else self.name,
						"against_voucher_type": self.doctype
					}, self.party_account_currency)
				)
				
				gl_entries.append(
					self.get_gl_dict({
						"account": self.account_for_change_amount,
						"against": self.customer,
						"credit": self.base_change_amount
					})
				)
			else:
				frappe.throw(_("Select change amount account"), title="Mandatory Field")
		
	def make_write_off_gl_entry(self, gl_entries):
		# write off entries, applicable if only pos
		if self.write_off_account and self.write_off_amount:
			write_off_account_currency = get_account_currency(self.write_off_account)
			default_cost_center = frappe.db.get_value('Company', self.company, 'cost_center')

			gl_entries.append(
				self.get_gl_dict({
					"account": self.debit_to,
					"party_type": "Customer",
					"party": self.customer,
					"against": self.write_off_account,
					"credit": self.base_write_off_amount,
					"credit_in_account_currency": self.base_write_off_amount \
						if self.party_account_currency==self.company_currency else self.write_off_amount,
					"against_voucher": self.return_against if cint(self.is_return) else self.name,
					"against_voucher_type": self.doctype
				}, self.party_account_currency)
			)
			gl_entries.append(
				self.get_gl_dict({
					"account": self.write_off_account,
					"against": self.customer,
					"debit": self.base_write_off_amount,
					"debit_in_account_currency": self.base_write_off_amount \
						if write_off_account_currency==self.company_currency else self.write_off_amount,
					"cost_center": self.write_off_cost_center or default_cost_center
				}, write_off_account_currency)
			)

@frappe.whitelist()
def mode_of_payment(company):
	return frappe.db.sql(""" select mpa.default_account, mpa.parent, mp.type as type from `tabMode of Payment Account` mpa,
		 `tabMode of Payment` mp where mpa.parent = mp.name and mpa.company = %(company)s""", {'company': company}, as_dict=True)


@frappe.whitelist()
def lista_clientes():

	return frappe.db.sql("""select name from `tabCustomer` """, as_dict=False)


@frappe.whitelist()
def quartos_reservados():

	return frappe.db.sql("""select name,numero_quarto,check_in,reservation_status from `tabReservas` where reservation_status = 'Nova' """, as_dict=True)



@frappe.whitelist()
def atualiza_ccorrente(cliente,recibo):

	print cliente
	print recibo
	for ccorrente1 in frappe.db.sql("""SELECT name,numero_registo,parent,status_conta_corrente from `tabCC_detalhes` where numero_registo = %s and parent = %s """, (recibo,cliente), as_dict=True):
		print ccorrente1.name
		print "CAMPOS !!!!!"

		reset_idx = frappe.get_doc("CC_detalhes",ccorrente1.name)
		reset_idx.status_conta_corrente = "Pago"
		reset_idx.save()


@frappe.whitelist()
def debit_to_acc(company):
	print frappe.db.sql("""select name from `tabAccount` where account_type='Receivable' and is_group=0 and company = %s """,company, as_dict=False)
	return frappe.db.sql("""select name from `tabAccount` where account_type='Receivable' and is_group=0 and company = %s """,company, as_dict=False)



@frappe.whitelist()
def get_perfil_pos():

	pos_profile = get_pos_profile(doc.company) or {}

	return {
#		'doc': doc,
#		'default_customer': pos_profile.get('customer'),
#		'items': get_items_list(pos_profile),
#		'customers': get_customers_list(pos_profile),
#		'serial_no_data': get_serial_no_data(pos_profile, doc.company),
#		'batch_no_data': get_batch_no_data(),
#		'tax_data': get_item_tax_data(),
#		'price_list_data': get_price_list_data(doc.selling_price_list),
#		'bin_data': get_bin_data(pos_profile),
#		'pricing_rules': get_pricing_rule_data(doc),
#		'print_template': print_template,
		'pos_profile': pos_profile
#		'meta': get_meta()
	}