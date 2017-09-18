# -*- coding: utf-8 -*-
# Copyright (c) 2017, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.website.website_generator import WebsiteGenerator
from frappe import _

class WOD(WebsiteGenerator):
	website = frappe._dict(
		template = "templates/generators/wod.html",
		condition_field = "publish",
		page_title_field = "titulo",
	)

	def validate(self):
		print self.docstatus
		print self.publish
		if self.docstatus == 2:
			#cancela tambem o publish
			self.publish=0

	def before_cancel(self):
		print 'Antes cancelar'
		self.publish = 0


	def get_context(self, context):
		# show breadcrumbs
		context.parents = [{'name': 'titulo', 'title': _('All WODS') }]

def get_list_context(context):
	context.title = _("WODS da Semana?")
	context.introduction = _('Current WODS!!')
