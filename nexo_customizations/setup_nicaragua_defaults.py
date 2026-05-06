import frappe
from frappe.utils import getdate, nowdate


@frappe.whitelist()
def setup_defaults(company_name: str, company_abbr: str | None = None):
	company_abbr = company_abbr or company_name[:5].upper()
	company = ensure_company(company_name, company_abbr)
	ensure_fiscal_year(company.name)
	ensure_global_defaults(company.name, company.default_currency or "NIO")
	frappe.db.commit()
	return {
		"company": company.name,
		"abbr": company.abbr,
		"currency": company.default_currency,
	}



def ensure_company(company_name: str, company_abbr: str):
	if frappe.db.exists("Company", company_name):
		return frappe.get_doc("Company", company_name)

	company = frappe.get_doc(
		{
			"doctype": "Company",
			"company_name": company_name,
			"abbr": company_abbr,
			"country": "Nicaragua",
			"default_currency": "NIO",
		}
	)
	company.insert(ignore_permissions=True)
	return company



def ensure_fiscal_year(company_name: str):
	today = getdate(nowdate())
	year = today.year
	fiscal_year_name = f"FY{year}"

	if frappe.db.exists("Fiscal Year", fiscal_year_name):
		fy = frappe.get_doc("Fiscal Year", fiscal_year_name)
		if not any(row.company == company_name for row in fy.companies):
			fy.append("companies", {"company": company_name})
			fy.save(ignore_permissions=True)
		return fy

	fy = frappe.get_doc(
		{
			"doctype": "Fiscal Year",
			"year": str(year),
			"year_start_date": f"{year}-01-01",
			"year_end_date": f"{year}-12-31",
			"companies": [{"company": company_name}],
		}
	)
	fy.insert(ignore_permissions=True)
	return fy



def ensure_global_defaults(company_name: str, currency: str):
	frappe.db.set_single_value("Global Defaults", "default_company", company_name)
	if currency:
		frappe.db.set_single_value("Global Defaults", "default_currency", currency)
