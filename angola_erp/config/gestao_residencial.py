from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Atendimento"),
			"items": [
				 {
				   "description": "Contas Correntes", 
				   "name": "Contas Correntes", 
				   "type": "doctype"
				  }, 

				 {
				   "description": "Gestao de Quartos", 
				   "name": "Gestao de Quartos", 
				   "type": "doctype"
				  }, 

				 {
				   "description": "Quartos", 
				   "name": "Quartos", 
				   "type": "doctype"
				  }, 

				 {
				   "description": "Reservas", 
				   "name": "Reservas", 
				   "type": "doctype"
				  }, 
				 {
				   "description": "Tipo de Quartos", 
				   "name": "Tipo de Quartos", 
				   "type": "doctype"
				  }, 

			]
		},

		{
			"label": _("Configuracao"),
			"items": [

				 {
				   "description": "Alerta PBX Asterisk", 
				   "name": "Alerta PBX", 
				   "type": "doctype"

				  }, 


			]
		},


		{
			"label": _("Relatorios"),
			"items": [

				 {
				   "description": "Movimento dos Quartos", 
				   "name": "Movimento dos Quartos", 
				   "doctype": "Gestao de Quartos",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "Relatorio de Contas-Correntes por Cliente", 
				   "name": "Relatorio de Contas-Correntes por Cliente", 
				   "doctype": "Gestao de Quartos",
				   "type": "report",
				   "is_query_report": True
				  }, 
				 {
				   "description": "Reservas", 
				   "name": "Reservas", 
				   "doctype": "Reservas",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "Reservas Ativas ou Novas", 
				   "name": "Reservas Ativas ou Novas", 
				   "doctype": "Reservas",
				   "type": "report",
				   "is_query_report": True
				  }, 

			]
		},

	]
