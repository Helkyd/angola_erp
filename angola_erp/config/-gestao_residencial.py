# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [


		{
                    "type": "doctype",
                    "name": "Gestao de Quartos",
                    "description": _("Gestao de Quartos... ")
                },
		{
                    "type": "doctype",
                    "name": "Quartos",
                    "description": _("Lista de Quartos...")
                },
		{
                    "type": "doctype",
                    "name": "Tipo de Quartos",
                    "description": _("Tipo de Quartos...")
                },
		{
                    "type": "doctype",
                    "name": "RESERVAS",
                    "description": _("Reservas dos Quartos...")
                },
	]
