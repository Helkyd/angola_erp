# -*- coding: utf-8 -*-
# Copyright (c) 2017, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
import os

class AppTheme(Document):
	def validate(self):
		#self.validate_if_customizable()
		self.validate_colors()

	def on_update(self):
		print 'on update'
		#print self.custom
		print frappe.local.conf.get('developer_mode')
		print (frappe.flags.in_import or frappe.flags.in_test)

		#if (not self.custom
		#	and frappe.local.conf.get('developer_mode')
		#	and not (frappe.flags.in_import or frappe.flags.in_test)):

		self.export_doc()

		#self.clear_cache_if_current_theme()

	def is_standard_and_not_valid_user(self):
		return (not self.custom
			and not frappe.local.conf.get('developer_mode')
			and not (frappe.flags.in_import or frappe.flags.in_test))

	def on_trash(self):
		if self.is_standard_and_not_valid_user():
			frappe.throw(_("You are not allowed to delete a standard Website Theme"),
				frappe.PermissionError)
		print 'Apagar tambem o CSS'
		file1 = './assets/angola_erp/css/erpnext/' + self.username + '_bootstrap.css'
		print file1
		os.remove(file1)


	def validate_if_customizable(self):
		if self.is_standard_and_not_valid_user():
			frappe.throw(_("Please Duplicate this Website Theme to customize."))

	def validate_colors(self):
		if (self.top_bar_color or self.top_bar_text_color) and \
			self.top_bar_color==self.top_bar_text_color:
				frappe.throw(_("Top Bar Color and Text Color are the same. They should be have good contrast to be readable."))


	def export_doc(self):
		"""Export to CSS file under 'assets/angola_erp/css/erpnext/' + frappe.session.user + '_bootstrap.css' """
		print ('export doc')
		""" 
			body {
			  font-family: "Helvetica Neue", Helvetica, Arial, "Open Sans", sans-serif;
			  font-size: 10px;
			  line-height: 1.42857143;
			  color: #36414c;
			  background-color: #ff5858;
			}
		"""
		print self.css
		print self.background_color

		body_css =' body { font-family: "Helvetica Neue", Helvetica, Arial, "Open Sans", sans-serif; font-size: ' + self.font_size + '; line-height: 1.42857143; color: #36414c; background-color: ' + self.background_color + ';}'
			


		#novo_css = self.css + '\n' + body_css
		novo_css = body_css

		print ('novo css ',novo_css)
	
		print 'body css'
		print body_css

		#Cria o file ...even if exists overwrite it..
		file1 = './assets/angola_erp/css/erpnext/' + self.username + '_bootstrap.css' #?ver=1510070115.0'
		print file1
		f = open(file1,'w')
		f.write(novo_css)
		f.close()



	def clear_cache_if_current_theme(self):
		website_settings = frappe.get_doc("Website Settings", "Website Settings")
		if getattr(website_settings, "website_theme", None) == self.name:
			website_settings.clear_cache()

	def use_theme(self):
		print ('use theme !!!')
		use_theme(self.name)

@frappe.whitelist()
def use_theme(theme):
	website_settings = frappe.get_doc("Website Settings", "Website Settings")
	website_settings.website_theme = theme
	website_settings.ignore_validate = True
	website_settings.save()

def add_website_theme(context):
	bootstrap = frappe.get_hooks("bootstrap")[0]
	bootstrap = [bootstrap]
	context.theme = frappe._dict()
	print ('add website theme ',context.disable_website_theme)
	if not context.disable_website_theme:
		website_theme = get_active_theme()
		context.theme = website_theme and website_theme.as_dict() or frappe._dict()

		if website_theme:
			if website_theme.bootstrap:
				bootstrap.append(website_theme.bootstrap)

			context.web_include_css = context.web_include_css + ["website_theme.css"]

	context.web_include_css = bootstrap + context.web_include_css

def get_active_theme():
	website_theme = frappe.db.get_value("Website Settings", "Website Settings", "website_theme")
	if website_theme:
		try:
			return frappe.get_doc("Website Theme", website_theme)
		except frappe.DoesNotExistError:
			pass

