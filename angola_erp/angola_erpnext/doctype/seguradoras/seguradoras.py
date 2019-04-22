# -*- coding: utf-8 -*-
# Copyright (c) 2019, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import cstr, flt, getdate
from frappe.model.naming import make_autoname


class Seguradoras(Document):

	def autoname(self):

		self.name = self.nome_da_seguradora


