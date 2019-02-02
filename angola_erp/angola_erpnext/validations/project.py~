# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

from frappe.utils import flt, getdate, get_url
from frappe import _

from frappe.model.document import Document



def validate(doc,method):

	check_tasks(doc,method)

def check_tasks(doc,method):
	"""check tasks for opened """
	print doc.name
	if doc.status == "Completed":
		tarefaaberta = frappe.db.sql("""select count(status) from tabTask where (status='Open' or status='Working' or status='Pending Review') and project=%s """,doc.name)
		print "Tarefas Projeto ", tarefaaberta
		if tarefaaberta[0][0] >=1:
			validation = False
			frappe.msgprint("Não pode fechar o Projecto sem terminar as Tarefas", raise_exception = 1)

