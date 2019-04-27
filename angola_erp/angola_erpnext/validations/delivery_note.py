# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint

import os 
from datetime import datetime

from subprocess import Popen, PIPE

import angola_erp.util.saft_ao

####
# Helkyd modified 27-04-2019
####

ultimoreghash = None


def validate(doc,method):
	'''
	#Check if the Item has a Stock Reconciliation after the date and time or NOT.
	#if there is a Stock Reconciliation then the Update would FAIL
	for dnd in doc.get("items"):
		sr = frappe.db.sql("""SELECT name FROM `tabStock Ledger Entry` 
			WHERE item_code = '%s' AND warehouse = '%s' AND voucher_type = 'Stock Reconciliation'
			AND posting_date > '%s'""" %(dnd.item_code, dnd.warehouse, doc.posting_date), as_list=1)
		if sr:
			frappe.throw(("There is a Reconciliation for Item \
			Code: {0} after the posting date").format(dnd.item_code))
		else:
			sr = frappe.db.sql("""SELECT name FROM `tabStock Ledger Entry` 
			WHERE item_code = '%s' AND warehouse = '%s' AND voucher_type = 'Stock Reconciliation'
			AND posting_date = '%s' AND posting_time >= '%s'""" \
			%(dnd.item_code, dnd.warehouse, doc.posting_date, doc.posting_time), as_list=1)
			if sr:
				frappe.throw(("There is a Reconciliation for Item \
				Code: {0} after the posting time").format(dnd.item_code))
			else:
				pass
	'''
	ultimodoc = frappe.db.sql(""" select max(name),creation,docstatus,hash_erp,hashcontrol_erp from `tabDelivery Note` where (docstatus = 1 or docstatus = 2)  and hash_erp <> '' """,as_dict=True)
	print 'VALIDARrrrrrrrrrrrrrrrrrr'
	print ultimodoc
	global ultimoreghash
	ultimoreghash = ultimodoc
	
def before_submit(doc, method):


	#HASH and HASH CONTROL...
	fileregisto = "registo"
	fileregistocontador = 1	#sera sempre aqui 

	#get the last doc generated 
	print 'verifica se ja tem o registo'
	print 'verifica se ja tem o registo' 
	print ultimoreghash

	if ultimoreghash:
		ultimodoc = ultimoreghash
	else:
		#ultimodoc = frappe.db.sql(""" select max(name),creation,modified,posting_date,hash_erp,hashcontrol_erp from `tabSales Invoice` """,as_dict=True)
		ultimodoc = frappe.db.sql(""" select name,creation,modified,posting_date,hash_erp,hashcontrol_erp from `tabDelivery Note` where creation = (select max(creation) from `tabSales Invoice`) """,as_dict=True)
		


	criado = datetime.strptime(doc.creation,'%Y-%m-%d %H:%M:%S.%f').strftime("%Y-%m-%dT%H:%M:%S") 
	
	print 'ULTIMO HASH.....'
	print ultimodoc
#	print ultimodoc[0].hash_erp
	if ultimodoc[0].hash_erp == "" or ultimodoc[0].hash_erp == None:
		#1st record
		print 'primeiro registo HASH'
		#print doc.posting_date.strftime("%Y-%m-%d")

		print doc.creation	
		print criado
		hashinfo = str(doc.posting_date) + ";" + str(criado) + ";" + str(doc.name) + ";" + str(doc.rounded_total) + ";"
	else:
		print 'segundo registo'
		#print chaveanterior
		hashinfo = str(doc.posting_date)  + ";" + str(criado) + ";" + str(doc.name) + ";" + str(doc.rounded_total) + ";" + str(ultimodoc[0].hash_erp)


#	hashfile = open("/tmp/" + str(fileregisto) + str(fileregistocontador) + ".txt","wb")
#	hashfile.write(hashinfo)

	#to generate the HASH
#	angola_erp.util.saft_ao.assinar_ssl()
	print "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
#	os.system("/usr/bin/python /tmp/angolaerp.cert2/assinar_ssl.py")	
	print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	print angola_erp.util.saft_ao.assinar_ssl1(hashinfo)
	 

#	p = Popen(["/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh"],shell=True, stdout=PIPE, stderr=PIPE)
#	p = Popen(["exec ~/frappe-bench/apps/angola_erp/angola_erp/util/hash_ao_erp.sh"],shell=True, stdout=PIPE, stderr=PIPE)
#	output, errors = p.communicate()
#	p.wait()
	print 'Openssl Signing...'
#	print output
#	print errors

#	hashfile.close()

	#Reads the file to save the HASH....
#	hashcriado = open('/tmp/registo1.b64','rb')	#open the file created to HASH
#	print 'Hash criado'
#	chaveanterior = str(hashcriado.read())	#para usar no next record...

	doc.hash_erp = str(angola_erp.util.saft_ao.assinar_ssl1(hashinfo))	#Hash created
	
#	hashcriado.close()
	
	#Deve no fim apagar todos os regis* criados ....
#	os.system("rm /tmp/registo* ")	#execute
	

