from __future__ import unicode_literals
import frappe

def execute():

	frappe.db.sql("""update tabReport set disabled=1 
		where name='createCustomReportinFrappePage' and module ='Angola ERPNext' """)

	frappe.db.sql("""update tabReport set disabled=1 
		where name='General Ledger 1' and module ='Angola ERPNext' """)

	frappe.db.sql("""update tabReport set disabled=1 
		where name='TESTES_GRID' and module ='Angola ERPNext' """)

	frappe.db.sql("""delete from `tabDocType` 
		where name='TestGRID' and module ='Angola ERPNext' """)


