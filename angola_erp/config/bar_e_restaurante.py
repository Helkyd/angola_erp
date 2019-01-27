from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Atendimento e Caixa"),
			"items": [
				 {
				   "description": "Atendimento Bar", 
				   "name": "Atendimento Bar", 
				   "type": "doctype"
				  }, 

				 {
				   "description": "Caixa de Registo", 
				   "name": "Caixa de Registo", 
				   "type": "doctype"
				  }, 

				 {
				   "description": "Mesas", 
				   "name": "Mesas", 
				   "type": "doctype"
				  }, 

			]
		},

		{
			"label": _("Relatorios"),
			"items": [

				 {
				   "description": "Mesas Ocupadas", 
				   "name": "Mesas Ocupadas", 
				   "doctype": "Atendimento Bar",
				   "type": "report",
				   "is_query_report": True
				  }, 

				 {
				   "description": "Relatorio de Mesas Faturadas", 
				   "name": "Relatorio de Mesas Faturadas", 
				   "doctype": "Atendimento Bar",
				   "type": "report",
				   "is_query_report": True
				  }, 
				 {
				   "description": "Relatorio do Caixa", 
				   "name": "Relatorio do Caixa", 
				   "doctype": "Caixa de Registo",
				   "type": "report",
				   "is_query_report": True
				  }, 

			]
		},

	]
