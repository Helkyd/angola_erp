# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe import msgprint
from frappe.utils import getdate
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

def after_insert(doc,method):
	#Adds BI to Customer only after a change being made
	print "After Insert"
	frappe.db.set_value("Customer", doc.name, "bi", doc.bi)

