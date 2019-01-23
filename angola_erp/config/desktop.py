# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Angola ERPNext",
			"color": "grey",
			"icon": "/assets/angola_erp/images/angolaerp.svg",
			"type": "module",
			"label": _("Angola ERPNext")
		},

		{
			"module_name": "Gestao Residencial",
			"color": "grey",
			"icon": "/assets/angola_erp/images/hotel1.svg",
			"type": "module",
			"label": _("Gestao Residencial")
		},
		{
			"module_name": "Bar e Restaurante",
			"color": "grey",
			"icon": "/assets/angola_erp/images/rest.svg",
			"type": "module",
			"label": _("Bar e Restaurante")
		},
		{
			"module_name": "Transitario",
			"color": "grey",
			"icon": "octicon octicon-checklist",
			"type": "module",
			"label": _("Transitario")
		},
		{
			"module_name": "Advogados",
			"color": "blue",
			"icon": "octicon octicon-law",
			"type": "module",
			"label": _("Advogados")
		},
		{
			"module_name": "Ginasio",
			"color": "#7578f6",
			"icon": "/assets/angola_erp/images/gym.svg",
			"type": "module",
			"label": _("Ginasio")
		},
		{
			"module_name": "Oficinas",
			"color": "grey",
			"icon": "/assets/angola_erp/images/diagnostico.svg",
			"type": "module",
			"label": _("Oficinas")
		},
		{
			"module_name": "Contractos Rent",
			"color": "grey",
			"icon": "octicon octicon-checklist",
			"type": "module",
			"label": _("Contractos Rent")
		},

		{
		   "_doctype": "Folha de Obras", 
		   "color": "grey", 
		   "icon": "/assets/angola_erp/images/folhaobra.svg", 
		   "label": "Folha de Obras", 
		   "link": "List/Folha de Obras", 
		   "module_name": "Folha de Obras", 
		   "type": "link"
	        },
		{
		   "_doctype": "Ordem de Reparacao", 
		   "color": "grey", 
		   "icon": "/assets/angola_erp/images/ordemreparar.svg", 
		   "label": "Ordem de Reparacao", 
		   "link": "List/Ordem de Reparacao", 
		   "module_name": "Ordem de Reparacao", 
		   "type": "link"
		}


	]
