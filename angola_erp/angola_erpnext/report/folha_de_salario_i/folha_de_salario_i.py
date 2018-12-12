# Copyright (c) 2013, Helio de Jesus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.utils import nowdate, cstr, flt, cint, now, getdate
from frappe import throw, _
from frappe.utils import formatdate, encode

def execute(filters=None):


	if not filters: filters = {}
	salary_slips = get_salary_slips(filters)
	columns, earning_types, ded_types = get_columns(salary_slips)
	ss_earning_map = get_ss_earning_map(salary_slips)
	ss_ded_map = get_ss_ded_map(salary_slips)


	data = []
	for ss in salary_slips:
		#Somente o primeiro e ultimo nome ....dd[dd.rfind(' '):len(dd)]
		row = [ss.employee_name[0:ss.employee_name.find(' ')] + ' ' + ss.employee_name[ss.employee_name.rfind(' '):len(ss.employee_name)], ss.department, ss.designation
			]
#		if (not ss.department == None and not ss.department == ''):
			#row += [ss.department]

#			columns[1] = columns[1].replace('-1','80')
		if (not ss.designation  == None and not ss.designation  == '') :
			#row += [ss.designation]
			columns[2] = columns[2].replace('-1','80')

#		print 'ver colunas'
		outros_abonos = 0
		print earning_types
		for e in earning_types:
			row.append(ss_earning_map.get(ss.name, {}).get(e))
			print 'earning type ', e
			print 	ss_earning_map.get(ss.name, {}).get(e)
			if (ss_earning_map.get(ss.name, {}).get(e) != None and e !='Salario Base'):
				outros_abonos += ss_earning_map.get(ss.name, {}).get(e)

#		print 'OUTROS ', outros
#		if outros:
		row += [outros_abonos]	
		row += [ss.gross_pay]
		
		outros_descontos = 0
		for d in ded_types:
			row.append(ss_ded_map.get(ss.name, {}).get(d))
			if (ss_ded_map.get(ss.name, {}).get(d) != None and (frappe.db.get_value('Salary Component',{'name':d},'salary_component_abbr') !='INSS') and (frappe.db.get_value('Salary Component',{'name':d},'salary_component_abbr') !='IRT')):
				outros_descontos += ss_ded_map.get(ss.name, {}).get(d)

		row += [outros_descontos]	
		row += [ss.total_deduction, ss.net_pay]

		data.append(row)

	return columns, data

def get_columns(salary_slips):
	columns = [
		_("Employee Name") + ":Data:150", 
		_("Department") + ":Link/Department:-1", _("Designation") + ":Link/Designation:-1"
		
	]

	salary_components = {_("Earning"): [], _("Deduction"): []}
	salary_components1 = {_("Earning"): [], _("Deduction"): []}

	for component in frappe.db.sql("""select distinct sd.salary_component, sc.type, sc.salary_component_abbr
		from `tabSalary Detail` sd, `tabSalary Component` sc
		where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s) order by sd.idx, sd.abbr """ %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1):
		print 'COMPONENT SALAR'
		print component.salary_component.encode('utf-8')
		salary_components[_(component.type)].append(component.salary_component)
		salary_components1[_(component.type)].append(component.salary_component_abbr)

	print salary_components
	print salary_components1
#	for e in salary_components[_("Earning")]:
#		print frappe.db.get_value('Salary Component',{'name':e},'salary_component_abbr' if e !='Salario Base' else 'salary_component')


	columns = columns + [(frappe.db.get_value('Salary Component',{'name':e},'salary_component_abbr' if e !='Salario Base' else 'salary_component') + (":Currency:120" if e =='Salario Base' else ":Currency:-1")) for e in salary_components[_("Earning")]] + \
		[_("Outras") + ":Currency:120"] + \
		[_("T. Remuneracoes") + ":Currency:120"] + [(frappe.db.get_value('Salary Component',{'name':d},'salary_component_abbr') + ":Currency:120") for d in salary_components[_("Deduction")]] + \
		[_("Outros Descontos") + ":Currency:120"] + \
		[_("Total Deduction") + ":Currency:120", _("Net Pay") + ":Currency:120"]

	print 'COLUNAS'	
	print columns
	print columns[3][1]

	return columns, salary_components[_("Earning")], salary_components[_("Deduction")]

def get_salary_slips(filters):
	print "DATAS"
	print filters.get("date_range")[0]
	print filters.get("date_range")[1]

	filters.update({"from_date": filters.get("date_range")[0], "to_date":filters.get("date_range")[1]})
	conditions, filters = get_conditions(filters)
	salary_slips = frappe.db.sql("""select * from `tabSalary Slip` where docstatus = 1 and salario_iliquido !=0 %s
		order by employee_name""" % conditions, filters, as_dict=1)

	if not salary_slips:
		frappe.throw(_("No salary slip found between {0} and {1}").format(
			filters.get("from_date"), filters.get("to_date")))
	return salary_slips

def get_conditions(filters):
	conditions = ""
	if filters.get("date_range"): conditions += " and start_date >= %(from_date)s"
	if filters.get("date_range"): conditions += " and end_date <= %(to_date)s"
	if filters.get("company"): conditions += " and company = %(company)s"
	if filters.get("employee"): conditions += " and employee = %(employee)s"

	return conditions, filters

def get_ss_earning_map(salary_slips):
	ss_earnings = frappe.db.sql("""select parent, salary_component, amount
		from `tabSalary Detail` where parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_earning_map = {}
	for d in ss_earnings:
		ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_earning_map[d.parent][d.salary_component] = flt(d.amount)

	return ss_earning_map

def get_ss_ded_map(salary_slips):
	ss_deductions = frappe.db.sql("""select parent, salary_component, amount
		from `tabSalary Detail` where parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_ded_map = {}
	for d in ss_deductions:
		ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_ded_map[d.parent][d.salary_component] = flt(d.amount)

	return ss_ded_map
