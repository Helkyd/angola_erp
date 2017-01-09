# -*- coding: utf-8 -*-
# Copyright (c) 2015, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr, flt, getdate
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class CC_detalhes(Document):

	def autoname(self):
		print "cc detalhes ", self.numero_registo
		self.name = self.numero_registo
