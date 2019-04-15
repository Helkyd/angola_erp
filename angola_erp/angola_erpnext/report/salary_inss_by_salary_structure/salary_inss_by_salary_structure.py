# Copyright (c) 2013, Helio de Jesus and contributors
# For license information, please see license.txt

# Modified: 09-04-2019


from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

global encargo_inss, inss_pessoal

def execute(filters=None):
	if not filters: filters = {}
	salary_slips = get_salary_slips(filters)
	columns, earning_types, ded_types = get_columns(salary_slips)
	ss_earning_map, ss_earning_map1 = get_ss_earning_map(salary_slips)
	ss_ded_map, ss_ded_map1 = get_ss_ded_map(salary_slips)

	sb_status = 0
	he_status = 0
	ftjss_status = 0
	fi_status = 0
	pa_status = 0
	pp_status = 0
	inss_status = 0
	


	data = []
	for ss in salary_slips:
		row = [ss.employee_name[0:ss.employee_name.find(' ')] + ' ' + ss.employee_name[ss.employee_name.rfind(' '):len(ss.employee_name)], ss.department, ss.designation
		]

		if (not ss.designation  == None and not ss.designation  == '') :
			#row += [ss.designation]
			columns[2] = columns[2].replace('-1','80')

		inss_pessoal = 0

		for e in earning_types:
#			if (ss_earning_map.get(ss.name, {}).get(e) != None and ss_earning_map.get(ss.name, {}).get(e) =='SB'):							
			row.append(ss_earning_map.get(ss.name, {}).get(e))

			print 'Abono'
			print ss_earning_map1.get(ss.name, {}).get(e)

			if (ss_earning_map1.get(ss.name, {}).get(e) == 'SB'):
			#SI = (SB + HE - PA + PP) - (FTJSS - FI )
			#('SB','HE','PA','PP','FTJSS','FI','IH','SDF','DU','ST','ABF','SA')
			#(SB + HE + PA + PP + IH + SDF + DU + ST) - (FTJSS - FTI1)

				encargo_inss = flt(ss_earning_map.get(ss.name, {}).get(e))

				sb_status = 0
				he_status = 0
				ftjss_status = 0
				fi_status = 0
				pa_status = 0
				pp_status = 0
				ih_status = 0
				du_status = 0
				st_status = 0
				sdf_status = 0 
				pat_status = 0
				aj_1_status = 0
				
				

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'SDF') and (sdf_status ==0):
			#SI = SB + HE - FTJSS - FI 
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))
				sdf_status  = 1

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'ST') and (st_status ==0):
			#SI = SB + HE - FTJSS - FI 
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))
				st_status  = 1

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'DU') and (du_status ==0):
			#SI = SB + HE - FTJSS - FI 
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))
				du_status  = 1

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'IH') and (ih_status ==0):
			#SI = SB + HE - FTJSS - FI 
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))
				ih_status  = 1

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'HE') and (he_status ==0):
			#SI = SB + HE - FTJSS - FI 
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))
				he_status = 1


			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'FTJSS') and (ftjss_status ==0):
			#SI = SB + HE - FTJSS - FI 
				encargo_inss = encargo_inss - flt(ss_earning_map.get(ss.name, {}).get(e))
				ftjss_status = 1

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'FI') and (fi_status ==0):
			#SI = SB + HE - FTJSS - FI 
				encargo_inss = encargo_inss - flt(ss_earning_map.get(ss.name, {}).get(e))
				fi_status = 1

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'PA') and (pa_status ==0):
			#SI = SB + HE - FTJSS - FI 
				pa_status = 1
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'PP') and (pp_status ==0):
			#SI = SB + HE - FTJSS - FI 
				pp_status = 1
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'SA') and (sa_status ==0):
			#SI = SB + HE - FTJSS - FI 
				sa_status = 1
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'PAT') and (pat_status ==0):
			#SI = SB + HE - FTJSS - FI 
				pat_status = 1
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))

			elif (ss_earning_map1.get(ss.name, {}).get(e) == 'AJ_1') and (aj_1_status ==0):
			#SI = SB + HE - FTJSS - FI 
				aj_1_status = 1
				encargo_inss = encargo_inss + flt(ss_earning_map.get(ss.name, {}).get(e))


		row += [ss.gross_pay]

		for d in ded_types:
#			if (ss_ded_map.get(ss.name, {}).get(d) != None and (frappe.db.get_value('Salary Component',{'name':d},'salary_component_abbr') !='INSS')):			
			row.append(ss_ded_map.get(ss.name, {}).get(d))

			inss_status = 0
			print 'DEscontos'
			print ss_ded_map1.get(ss.name, {}).get(d)
			if (ss_ded_map1.get(ss.name, {}).get(d) == 'INSS') and (inss_status ==0):
				inss_status = 1
				inss_pessoal = inss_pessoal + flt(ss_ded_map.get(ss.name, {}).get(d))
				print 'INSSS'
				print inss_pessoal

		row += [ss.total_deduction, ss.net_pay]
#		if inss_status == 1:
		print inss_pessoal
		print encargo_inss
		if inss_pessoal == 0: encargo_inss = 0
		encargo_inss = (encargo_inss * 0.08)			
		inss_pessoal = (inss_pessoal + encargo_inss)
#		else:
#			encargo_inss = 0
#			inss_pessoal = 0

		row += [encargo_inss]
		row += [inss_pessoal]

		data.append(row)

	return columns, data

def get_columns(salary_slips):
	columns = [
		_("Employee Name") + "::140", 
		_("Department") + ":Link/Department:-1", _("Designation") + ":Link/Designation:-1"		
	]

	salary_components = {_("Earning"): [], _("Deduction"): []}
	salary_components1 = {_("Earning"): [], _("Deduction"): []}	

	for component in frappe.db.sql("""select distinct sd.salary_component, sc.type, sc.salary_component_abbr
		from `tabSalary Detail` sd, `tabSalary Component` sc
		where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s) order by sd.idx, sd.abbr""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1):
		#salary_components[_(component.type)].append(component.salary_component)

		print 'COMPONENT SALAR'
		print component.salary_component
		salary_components[_(component.type)].append(component.salary_component)
		salary_components1[_(component.type)].append(component.salary_component_abbr)
	
	print 'Component salarial'
	print salary_components
	print salary_components1


	#columns = columns + [('Rem. Adicional' if frappe.db.get_value('Salary Component',{'name':e},'salary_component_abbr') =='ST' else frappe.db.get_value('Salary Component',{'name':e},'salary_component_abbr' if e !='Salario Base' else 'salary_component') + (":Currency:120" if (e =='Salario Base' or frappe.db.get_value('Salary Component',{'name':e},'salary_component_abbr') == 'ST') else ":Currency:-1")) for e in salary_components[_("Earning")]] + \
	columns = columns + [(frappe.db.get_value('Salary Component',{'name':e},'salary_component_abbr' if e !='Salario Base' else 'salary_component') + (":Currency:120" if (e =='Salario Base' or frappe.db.get_value('Salary Component',{'name':e},'salary_component_abbr') == 'ST') else ":Currency:-1")).replace('ST','Rem. Adicional') for e in salary_components[_("Earning")]] + \
		[_("Gross Pay") + ":Currency:120"] + [(frappe.db.get_value('Salary Component',{'name':d},'salary_component_abbr') + ":Currency:120" if frappe.db.get_value('Salary Component',{'name':d},'salary_component_abbr') =='INSS' else ":Currency:-1") for d in salary_components[_("Deduction")]] + \
		[_("Total Deduction") + ":Currency:-1", _("Net Pay") + ":Currency:120",_("INSS %8") + ":Currency:120", _("Total a Pagar") + ":Currency:120"   ]
	"""

	columns = columns + [(frappe.db.get_value('Salary Component',{'name':e},'salary_component_abbr' if e !='Salario Base' else 'salary_component') + (":Currency:120" if e =='Salario Base' else ":Currency:-1")) for e in salary_components[_("Earning")]] + \
		[_("Outras") + ":Currency:120"] + \
		[_("T. Remuneracoes") + ":Currency:120"] + [(frappe.db.get_value('Salary Component',{'name':d},'salary_component_abbr') + ":Currency:120") for d in salary_components[_("Deduction")]] + \
		[_("Outros Descontos") + ":Currency:120"] + \
		[_("Total Deduction") + ":Currency:120", _("Net Pay") + ":Currency:120"]
	"""

	print 'COLUNAS'	
	print columns
	print columns[3][1]




	return columns, salary_components[_("Earning")], salary_components[_("Deduction")]

def get_salary_slips(filters):
	filters.update({"from_date": filters.get("date_range")[0], "to_date":filters.get("date_range")[1]})
	conditions, filters = get_conditions(filters)
	salary_slips = frappe.db.sql("""select * from `tabSalary Slip` where docstatus = 1 %s
		order by employee""" % conditions, filters, as_dict=1)

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
	if filters.get("salary_structure"): conditions += " and salary_structure = %(salary_structure)s"

	return conditions, filters

def get_ss_earning_map(salary_slips):
	ss_earnings = frappe.db.sql("""select parent, abbr, salary_component, amount
		from `tabSalary Detail` where parent in (%s) order by idx""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_earning_map = {}
	ss_earning_map1 = {}

	for d in ss_earnings:
		ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_earning_map[d.parent][d.salary_component] = flt(d.amount)

		ss_earning_map1.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_earning_map1[d.parent][d.salary_component] = d.abbr



	return ss_earning_map, ss_earning_map1

def get_ss_ded_map(salary_slips):
	ss_deductions = frappe.db.sql("""select parent, abbr, salary_component, amount
		from `tabSalary Detail` where parent in (%s) order by idx""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_ded_map = {}
	ss_ded_map1 = {}

	for d in ss_deductions:
		ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_ded_map[d.parent][d.salary_component] = flt(d.amount)

		ss_ded_map1.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_ded_map1[d.parent][d.salary_component] = d.abbr

	return ss_ded_map, ss_ded_map1
