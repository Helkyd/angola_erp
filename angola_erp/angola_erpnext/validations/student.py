# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.desk.form.linked_with import get_linked_doctypes

def validate(doc, method):
	if not doc.cartao_numero:
		#add name to cartao numero
		doc.cartao_numero = doc.name

