# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
# Helkyd V7.0.58

from __future__ import unicode_literals
import frappe

from frappe.utils import cstr, flt, getdate, get_url
from frappe.model.naming import make_autoname
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from erpnext.hr.utils import set_employee_name

import frappe.model
import frappe.utils

@frappe.whitelist()
def make_earn_ded_table(dt):
	make_table(dt,'Salary Component','earnings','Salary Detail')
	dt.make_table(dt,'Salary Component','deductions', 'Salary Detail')

@frappe.whitelist()
def make_table(dt, doct_name, tab_fname, tab_name):

	list1 = frappe.db.sql("select name,abono,desconto from `tab%s` where docstatus != 2" % doct_name)
	for li in list1:
		if(tab_fname == 'earnings' and li[1] == 1):
			child = dt.append(tab_fname, {})
			child.salary_component = cstr(li[0])
			child.amount = 0
		elif(tab_fname == 'deductions' and li[2] == 1):
			child = dt.append(tab_fname, {})
			child.salary_component = cstr(li[0])
			child.amount = 0


