# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt


from lxml import html
import requests



def cambios(fonte):

	if fonte == 'BNA':
		page=requests.get('http://www.bna.ao/Servicos/cambios_table.aspx?idl=1')
		#page= requests.get('http://www.bfa.ao/Servicos/Cambios/Divisas.aspx?idl=1')

		tree = html.fromstring(page.content)

		x=0
		for tr in tree.xpath("//tr"):
		
			if tr.xpath('//tr[3]/td[1]/text()')[0] == 'USD': 
				moeda= tr.xpath("//tr[3]/td[1]/text()")[0]     #moeda USD
				moedacompra= tr.xpath("//tr[3]/td[2]/text()")[0]	#Compra
				moedavenda= tr.xpath("//tr[3]/td[3]/text()")[0]    #Venda
				x += 1

		print moeda
		print moedacompra
		print moedavenda
	
	if fonte == 'BFA':
		page= requests.get('http://www.bfa.ao/Servicos/Cambios/Divisas.aspx?idl=1')

		tree = html.fromstring(page.content)

		x=0
		for tr in tree.xpath("//tr"):	

			if tr.xpath('//*[@id="usd"]/text()')[0] == 'usd': 
				print "AQUIIIIIII"
				print tr.xpath('//*[@id="usd"')
				moeda= tr.xpath('//*[@id="usd"]/text()')[0]     #moeda USD
				moedacompra= tr.xpath('//tr[4]/td[1]/text()')[0]	#Compra
				moedavenda= tr.xpath('//tr[4]/td[2]/text()')[0]    #Venda
				x += 1

		print moeda
		print moedacompra
		print moedavenda


