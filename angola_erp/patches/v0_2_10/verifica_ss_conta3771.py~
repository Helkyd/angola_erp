from __future__ import unicode_literals
import frappe

def execute():

	empresa_default = frappe.get_doc('Global Defaults').default_company
	print(empresa_default)
	if empresa_default:
		empresa_abbr = frappe.get_doc('Company', empresa_default).abbr		

		#Accounting 3771 Imposto Consumo Temporario
		iii = frappe.db.sql("""select name from `tabAccount` where name like '3771%%' and company = %s """,(empresa_default),as_dict=True)
		print(iii)
		if len(iii) == 0:
			#Nao tem; must create
			dados = frappe.get_doc({
				"doctype": "Account",
				"report_type": "Balance Sheet",
				"owner": "administrator",
				"account_name": "37710000 - IPC Transitorio",
				"account_type": "Temporary",
				"freeze_account": "No",
				"root_type": "Asset",
				"docstatus": 0,
				"company": empresa_default,
				"is_group": 0,
				"tax_rate": 0.0,
				"account_currency": "KZ",
				"parent_account": "377 - Contas Transitorias" + " - " + empresa_abbr,
				"name": "37710000 - IPC Transitorio",
				"idx": 0,
				"docstatus": 0
			})
			dados.insert()

		ii = frappe.db.sql("""select name from `tabCost Center` where name like '%Seguranca Social%' """)
		if len(ii) == 0:
			#Nao tem; must create
			doc = frappe.get_doc({
				"doctype" : "Cost Center",
				"cost_center_name" : "Seguranca Social", 
				"company" : empresa_default
			})
			doc.insert()


		
