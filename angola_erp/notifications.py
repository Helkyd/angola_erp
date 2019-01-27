
# Copyright (c) 2016, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

def get_notification_config():
	return { "for_doctype":
		{
			"Atendimento Bar": {"status_atendimento": "Ocupado"},
			"Mesas": {"status_mesa": "Ocupada"},
			"Gestao de Quartos": {"status_quarto": "Ocupado"},
			"Reservas": {"reservation_status": "Nova"},
			"Ficha de Processo": {"status_process":['in',"Aberto,Em Curso"]},
			"Folha de Obras": {"fo_status": ['in','Aberta, Em Curso']},
			"Ordem de Reparacao": {"or_status": ['in','Aberta, Em Curso']},
			"Ficha Tecnica da Viatura": {"status_viatura": ['in','Alugada']},
			"Contractos Rent": {"status_contracto": ['in','Activo']}

		}
	}


