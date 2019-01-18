from __future__ import unicode_literals
import frappe

def execute():

	ii = frappe.db.sql("""select name from `tabRetencoes` where name like '%industrial%' """)
	if len(ii) ==0:
		#Nao tem; must create
		doc = frappe.get_doc({
			"doctype" : "Retencoes",
			"descricao" : "Imposto Industrial", 
			"percentagem" : 2
		})
		doc.insert()

	#Accounting 3419 Imposto Industrial Temporario
	empresa_default = frappe.get_doc('Global Defaults').default_company
	if empresa_default:
		empresa_abbr = frappe.get_doc('Company', empresa_default).abbr
		iii = frappe.db.sql("""select name from `tabAccount` where name like '%3419%' and company = %s """,(empresa_default),as_dict=True)

		if len(iii) ==0:
			#Nao tem; must create
			dados = frappe.get_doc({
				"doctype": "Account",
				"report_type": "Balance Sheet",
				"owner": "administrator",
				"account_name": "34190000 - I Industrial - Pagamentos por Conta Temp.",
				"account_type": "Temporary",
				"freeze_account": "No",
				"root_type": "Asset",
				"docstatus": 0,
				"company": empresa_default,
				"is_group": 0,
				"tax_rate": 0.0,
				"account_currency": "KZ",
				"parent_account": "341 - Imposto Sobre Lucros" + " - " + empresa_abbr,
				"name": "34190000 - I Industrial - Pagamentos por Conta Temp.",
				"idx": 0,
				"docstatus": 0
			})
			dados.insert()


		
