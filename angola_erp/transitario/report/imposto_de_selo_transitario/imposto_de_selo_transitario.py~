# Copyright (c) 2013, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import msgprint, _


def execute(filters=None):
	return _execute(filters)

def _execute(filters, additional_table_columns=None, additional_query_columns=None):
	if not filters: filters = frappe._dict({})

	invoice_list = get_invoices(filters, additional_query_columns)

	print 'Invoice List'
	print invoice_list
	print additional_query_columns
	columns = get_columns(invoice_list, additional_table_columns)

	if not invoice_list:
		msgprint(_("No record found"))
		return columns, invoice_list

	company_currency = frappe.db.get_value("Company", filters.get("company"), "default_currency")

	mes2_ = 0


	data = []
	for inv in invoice_list:

		#acrescenta o mes corrente ....
		if inv.Mes == 1: mes2_ = 'Janeiro'
		if inv.Mes == 2: mes2_ = 'Fevereiro'
		if inv.Mes == 3: mes2_ = 'Marco'
		if inv.Mes == 4: mes2_ = 'Abril'
		if inv.Mes == 5: mes2_ = 'Maio'
		if inv.Mes == 6: mes2_ = 'Junho'
		if inv.Mes == 7: mes2_ = 'Julho'
		if inv.Mes == 8: mes2_ = 'Agosto'
		if inv.Mes == 9: mes2_ = 'Setembro'
		if inv.Mes == 10: mes2_ = 'Outubro'
		if inv.Mes == 11: mes2_ = 'Novembro'
		if inv.Mes == 12: mes2_ = 'Dezembro'

		#print mes2_.encode('utf-8') 
		

		row = [
			inv.Ano, mes2_ , inv.Total, inv.Selo
		]

		if additional_query_columns:
			for col in additional_query_columns:
				row.append(inv.get(col))


		# total tax, grand total, outstanding amount & rounded total
		row += [inv.Total]

		data.append(row)

	return columns, data

def get_columns(invoice_list, additional_table_columns):
	"""return columns based on filters"""
	columns = [
		_("Ano") + "::80", _("Mes") + "::80"
	]

	columns = columns + [_("Total") + ":Currency/currency:120"] + [_("Imp. Selo 1%") + ":Currency/currency:120"]

	return columns

def get_conditions(filters):
	conditions = ""

	if filters.get("company"): conditions += " and company=%(company)s"

	if filters.get("from_date"): conditions += " and posting_date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and posting_date <= %(to_date)s"


	return conditions

def get_invoices(filters, additional_query_columns):
	if additional_query_columns:
		additional_query_columns = ', ' + ', '.join(additional_query_columns)

	conditions = get_conditions(filters)
	return frappe.db.sql(""" select year(posting_date) as Ano, month(posting_date) as Mes, sum(base_grand_total) as Total, sum(base_grand_total*1/100) as Selo from `tabSales Invoice` where docstatus =1 and outstanding_amount = 0 %s group by month(posting_date) order by year(posting_date), month(posting_date)""".format(additional_query_columns or '') %
		conditions, filters, as_dict=1)	


