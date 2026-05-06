import frappe

from nexo_customizations.install import (
	apply_site_defaults,
	ensure_colors,
	ensure_tenant_branding_defaults,
	ensure_website_theme,
)
from nexo_customizations.pos_setup import setup_pos_for_company
from nexo_customizations.setup_nicaragua_defaults import setup_defaults


@frappe.whitelist()
def provision_tenant(company_name: str, company_abbr: str | None = None, setup_pos: int = 1):
	ensure_colors()
	ensure_website_theme()
	apply_site_defaults()
	ensure_tenant_branding_defaults()
	setup_defaults(company_name, company_abbr)
	pos_result = None
	if int(setup_pos or 0):
		pos_result = setup_pos_for_company(company_name, company_abbr)
	frappe.clear_cache()
	return {"company": company_name, "company_abbr": company_abbr, "pos": pos_result}
