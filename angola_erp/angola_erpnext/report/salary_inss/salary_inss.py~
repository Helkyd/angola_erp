# Copyright (c) 2013, Helio de Jesus and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

global encargo_inss

def execute(filters=None):
	if not filters: filters = {}
	salary_slips = get_salary_slips(filters)
	columns, earning_types, ded_types = get_columns(salary_slips)
	ss_earning_map, ss_earning_map1 = get_ss_earning_map(salary_slips)
	ss_ded_map = get_ss_ded_map(salary_slips)

	sb_status = 0
	he_status = 0
	ftjss_status = 0
	fi_status = 0
	pa_status = 0
	pp_status = 0


	data = []
	for ss in salary_slips:
		row = [ss.name, ss.employee_name, 
			ss.company, ss.start_date, ss.end_date]

		for e in earning_types:
			row.append(ss_earning_map.get(ss.name, {}).get(e))

			if (ss_earning_map1.get(ss.name, {}).get(e) == 'SB'):
			#SI = (SB + HE - PA + PP) - (FTJSS - FI )
				encargo_inss = flt(ss_earning_map.get(ss.name, {}).get(e))

				sb_status = 0
				he_status = 0
				ftjss_status = 0
				fi_status = 0
				pa_status = 0
				pp_status = 0

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

			

		row += [ss.gross_pay]

		for d in ded_types:
			row.append(ss_ded_map.get(ss.name, {}).get(d))

		row += [ss.total_deduction, ss.net_pay]


		encargo_inss = (encargo_inss * 0.08)		
		row += [encargo_inss]

		data.append(row)

	return columns, data

def get_columns(salary_slips):
	columns = [
		_("Salary Slip ID") + ":Link/Salary Slip:150", _("Employee Name") + "::140",
		_("Company") + ":Link/Company:120", _("Start Date") + "::80", _("End Date") + "::80" 
	]

	salary_components = {_("Earning"): [], _("Deduction"): []}

	for component in frappe.db.sql("""select distinct sd.salary_component, sc.type
		from `tabSalary Detail` sd, `tabSalary Component` sc
		where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s) order by sd.idx""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1):
		salary_components[_(component.type)].append(component.salary_component)

	print salary_components
	columns = columns + [(e + ":Currency:120") for e in salary_components[_("Earning")]] + \
		[_("Gross Pay") + ":Currency:120"] + [(d + ":Currency:120") for d in salary_components[_("Deduction")]] + \
		[_("Total Deduction") + ":Currency:120", _("Net Pay") + ":Currency:120",_("INSS %8") + ":Currency:120"]

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
	ss_deductions = frappe.db.sql("""select parent, salary_component, amount
		from `tabSalary Detail` where parent in (%s) order by idx""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_ded_map = {}
	for d in ss_deductions:
		ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_ded_map[d.parent][d.salary_component] = flt(d.amount)

	return ss_ded_map
