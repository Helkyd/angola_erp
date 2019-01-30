from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Aluguer"),
			"items": [
				 {
				   "description": "Contractos Rent", 
				   "name": "Contractos Rent", 
				   "type": "doctype",
				  }, 

				{
				   "type": "doctype", 
				   "description": "Ficha Tecnica da Viatura", 
				   "name": "Ficha Tecnica da Viatura", 
				  },
				 {
				   "description": _("Vehicle"), 
				   "name": "Vehicle", 
				   "type": "doctype"
				  }, 


			]
		},
		{
			"label": _("Configuracao"),
			"items": [
				 {
				   "description": "Estacao", 
				   "name": "Estacao", 
				   "type": "doctype"
				  }, 
				{
				   "type": "doctype", 
				   "description": "Tarifas", 
				   "name": "Tarifas", 
				  },

				 {
				   "description": "Servico de Motorista", 
				   "name": "Servico de Motorista", 
				   "type": "doctype"
				  }, 


			]
		},


	]
