from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Cadastro de Processo"),
			"items": [
				 {
				   "description": "Cadastro de Processo", 
				   "name": "Cadastro de Processo", 
				   "type": "doctype"
				  }, 


			]
		},
		{
			"label": _("Configuracao"),
			"items": [
				 {
				   "description": "Fases Processuais", 
				   "name": "Fases Processuais", 
				   "type": "doctype"
				  }, 
				 {
				   "description": "Localizacao Processo", 
				   "name": "Localizacao Processo", 
				   "type": "doctype"
				  }, 

				{
				   "type": "doctype", 
				   "description": "Tipo de Acoes", 
				   "name": "Tipo de Acoes", 
				  },

				 {
				   "description": "Tipo de Processo", 
				   "name": "Tipo de Processo", 
				   "type": "doctype"
				  }, 

				 {
				   "description": "Tipo de Recurso", 
				   "name": "Tipo de Recurso", 
				   "type": "doctype"
				  }, 

			]
		},


	]
