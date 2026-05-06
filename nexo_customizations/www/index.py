import frappe
from frappe.www.login import get_context as core_login_context

from nexo_customizations.utils.branding import get_branding_context
from nexo_customizations.utils.website import get_logged_in_redirect

no_cache = True


def get_context(context):
	if frappe.session.user != "Guest":
		frappe.local.flags.redirect_location = get_logged_in_redirect()
		raise frappe.Redirect

	core_login_context(context)
	context.no_header = True
	context.body_class = "nexo-landing-page"
	context.nexo_branding = get_branding_context()
	context.title = context.nexo_branding.get("brand_name") or "NexoERP"
