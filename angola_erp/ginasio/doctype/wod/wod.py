# -*- coding: utf-8 -*-
# Copyright (c) 2017, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.website.website_generator import WebsiteGenerator
from frappe import _

class WOD(WebsiteGenerator):


	website = frappe._dict(
		page_title_field = "titulo",
		condition_field = "publish",
#		condition_field = "show_in_website",
#		template = "wod/templates/generators/wod_group.html",
#		template = "angola_erp/angola_erp/ginasio/doctype/wod1/templates/wod1.html",
		template = "www/wod.html",
		no_cache = 1
	)

#	website = frappe._dict(
#		template = "templates/generators/wod.html",
#		#template = "templates/wod.html",
#		condition_field = "publish",
#		page_title_field = "titulo",
#	)
	print 'PAGINA WEB'
	print website




	def get_context(self, context):
		print 'vim aqqqqqqqqqqqqqqqqqqqqqq'
		print 'vim aqqqqqqqqqqqqqqqqqqqqqq'
		print 'vim aqqqqqqqqqqqqqqqqqqqqqq'

#		context.show_search=True

		context.title = _("WODS")
		#context.parents = get_parent_item_groups(self.item_group)
		context.parents = [{'name': 'wods', 'title': _('All WODS') }]

		print context
		return context

	def validate(self):
		print self.docstatus
		print self.publish
		if not self.route:
			self.route = self.name

		if self.docstatus == 2:
			#cancela tambem o publish
			self.publish=0

	def before_cancel(self):
		print 'Antes cancelar'
		self.publish = 0




def get_list_context(context):
	context.title = _("Todos WODs")
	context.show_search=True
#	context.search_link = '/?data_do_wod'
#	context.introduction = _('Current Job Openings!!')
#	context.parents = [{'name': 'home', 'title': _('home') }]

#	print 'get list context'
#	print context

