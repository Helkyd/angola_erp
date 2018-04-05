# -*- coding: utf-8 -*-
# Copyright (c) 2018, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.utils import cstr

from frappe import _, throw, msgprint
from frappe.utils import nowdate, encode

from frappe.model.document import Document

import csv 
import json
from angola_erp.angola_erpnext.validations.sms_settings import send_sms


import sys
reload(sys)
sys.setdefaultencoding('utf8')


@frappe.whitelist()
def aoa_sms_numbers():


	unitel='92'
	unitel1 = '93'
	unitel2 = '94'

	pre_inicio = 1
	inicio = 1000000
	fim = 9999999
	contador = inicio

	sms_txt = 'AngolaERP Gestão de Serviços Integrados. Visite o nosso website https://angolaerp.co.ao'

	text_file = open('/tmp/numeros_sms.txt', "w")

	while contador != fim:
		contador += 1
		print(contador)
		#print(unitel,contador);
		numerofinal = unitel + str(contador)
		numerofinal1 = unitel1 + str(contador)
		numerofinal2 = unitel2 + str(contador)
		#print ('92 ',numerofinal);
		#print ('93 ',numerofinal1);
		#print ('94 ',numerofinal2);

		text_file.write(numerofinal + "\n" )
		text_file.write(numerofinal1 + "\n" )
		text_file.write(numerofinal2 + "\n" )

	text_file.close()
	print ('TERMINOU DE GERAR!!!!!!')

	ficheiro = '/tmp/numeros_sms.txt'
	lerficheiro = open (ficheiro,'r')
	for line in lerficheiro:
		print 'Enviando para ',line;
		send_sms(line,sms_txt,'angolaerp')


	print ('TERMINOU de LER e Enviar SMS')

	
	#send_sms('923534109',sms_txt,'angolaerp')


