# -*- coding: utf-8 -*-
# Copyright (c) 2019, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from datetime import datetime, timedelta
from frappe.utils import cstr, get_datetime, getdate, cint, get_datetime_str



class Estacao(Document):

	def autoname(self):
		self.name = self.estacao_local




