# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe import msgprint
from frappe.model.document import Document
from frappe.utils import money_in_words, flt


@frappe.whitelist()
def make_earn_ded_table1(ddd):
	
	print "AAAAAAA"
	#	ddd.make_table1('Salary Component','earnings','Salary Detail')
	#	ddd.make_table1('Salary Component','deductions', 'Salary Detail')


	def make_table1(ddd, doct_name, tab_fname, tab_name):

		frappe.throw(_("Net pay cannot be negative"))
		list1 = frappe.db.sql("select name from `tab%s` where docstatus != 2" % doct_name)

		for li in list1:
			child = ddd.append(tab_fname, {})
			if(tab_fname == 'earnings' and li.abono == 1):
				child.salary_component = cstr(li[0])
				child.amount = 0
			elif(tab_fname == 'deductions' and li.desconto == 1):
				child.salary_component = cstr(li[0])
				child.amount = 0


	def validate(doc,method):

		check_edc(doc, method)
		doc.total_deduction = 0
		doc.total_ctc = 0
		doc.total_contribution = 0
		doc.total_earning = 0
		doc.net_pay = 0

		for d in doc.deductions:
			count = 0
			for e in doc.earnings:
				earn = frappe.get_doc("Salary Component", e.salary_component)
				if earn.only_for_deductions == 1:
					for ded in earn.deduction_contribution_formula:
						if ded.salary_component == d.salary_component:
							if count == 0:
								d.amount =0
								count += 1
							d.amount += (ded.percentage * e.amount)/100
			d.amount = round(d.amount, 0)
			doc.total_deduction += d.amount
	
		for e in doc.earnings:
			earn = frappe.get_doc("Salary Component", e.salary_component)
			if earn.only_for_deductions <> 1:
				doc.total_earning += flt(e.amount)

		for c in doc.contributions:
			c.amount = 0
			for e in doc.earnings:
				earn = frappe.get_doc("Salary Component", e.salary_component)
				if earn.only_for_deductions == 1:
					for cont in earn.deduction_contribution_formula:
						if cont.salary_component == c.salary_component:
							c.amount += cont.percentage * e.amount/100
			c.amount = round(c.amount, 0)
			doc.total_contribution += c.amount
		doc.net_pay = doc.total_earning - doc.total_deduction
		doc.total_ctc = doc.total_earning + doc.total_contribution
	
	def check_edc(doc,method):
		for e in doc.earnings:
			earn = frappe.get_doc("Salary Component", e.salary_component)
			if earn.abono <> 1:
				frappe.throw(("Only Earnings are allowed in Earning Table check row# \
					{0} where {1} is not an Earning").format(e.idx, e.salary_component))
				
		for d in doc.deductions:
			ded = frappe.get_doc("Salary Component", d.salary_component)
			if ded.desconto <> 1:
				frappe.throw(("Only Deductions are allowed in Deduction Table check row# \
					{0} where {1} is not a Deduction").format(d.idx, d.salary_component))
				

