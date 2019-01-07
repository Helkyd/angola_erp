from __future__ import unicode_literals
import frappe

def execute():

	frappe.db.sql("""update `tabPrint Format` set disabled=1 
		where name='fatura_6' and module ='Angola ERPNext' """)

	frappe.delete_doc("DocType","TestGRID")

	
