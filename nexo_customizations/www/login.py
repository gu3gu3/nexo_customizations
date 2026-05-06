from frappe.www.login import get_context as core_login_context

from nexo_customizations.utils.branding import get_branding_context

no_cache = True


def get_context(context):
	core_login_context(context)
	context.no_header = True
	context.body_class = "nexo-auth-page"
	context.nexo_branding = get_branding_context()
	context.title = context.nexo_branding.get("brand_name") or "NexoERP"
