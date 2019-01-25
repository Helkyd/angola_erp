from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Ordem de Reparacao & Folha de Obra"),
			"items": [
				 {
				   "description": "Ordem de Reparacao", 
				   "name": "Ordem de Reparacao", 
				   "type": "doctype"
				  }, 

				{
				   "type": "doctype", 
				   "description": "Folha de Obras", 
				   "name": "Folha de Obras", 
				  },

			]
		},
		{
			"label": _("Configuracao"),
			"items": [
				 {
				   "description": "Marca Carros", 
				   "name": "Marca Carros", 
				   "type": "doctype"
				  }, 
				{
				   "type": "doctype", 
				   "description": "Veiculos", 
				   "name": "Veiculos", 
				  },

				 {
				   "description": "Avarias", 
				   "name": "Avarias", 
				   "type": "doctype"
				  }, 


			]
		},


	]
