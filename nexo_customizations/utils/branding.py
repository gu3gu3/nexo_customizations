from urllib.parse import quote

import frappe
from frappe.website.utils import clear_cache as clear_website_cache

CACHE_KEY = "nexo_branding_context"

DEFAULTS = {
	"enabled": 1,
	"brand_name": "NexoERP",
	"portal_name": "Portal NexoERP",
	"logo_url": "/assets/nexo_customizations/images/logo.png",
	"favicon_url": "/assets/nexo_customizations/images/n-logo.png",
	"main_site_url": "https://nexo-contable.com",
	"company_name": "Nexo Contable",
	"primary_color": "#1E5EFF",
	"secondary_color": "#19C37D",
	"ink_color": "#0F172A",
	"soft_color": "#F7FAFC",
	"hero_kicker": "ERP cloud para Nicaragua",
	"hero_title": "Administra tu operación con NexoERP.",
	"hero_subtitle": "Ingresa a NexoERP con una experiencia SaaS moderna, rápida y segura, operada por Nexo Contable.",
	"hero_message": "Contabilidad, facturación, compras, ventas y visibilidad financiera en una sola plataforma.",
	"login_title": "Accede a NexoERP",
	"login_subtitle": "Ingresa con tu correo y contraseña corporativa.",
	"whatsapp_number": "50500000000",
	"whatsapp_message": "Hola, necesito ayuda con NexoERP.",
	"footer_note": "Plataforma SaaS NexoERP operada por Nexo Contable.",
}

DEFAULT_BENEFITS = [
	{
		"title": "Operación centralizada",
		"description": "Contabilidad, ventas, compras e inventario en una sola interfaz.",
	},
	{
		"title": "Acceso seguro",
		"description": "Ingreso rápido, branding consistente y experiencia profesional para cada cliente.",
	},
	{
		"title": "Soporte ágil",
		"description": "Acompañamiento directo de Nexo Contable vía WhatsApp y mesa operativa.",
	},
]

DEFAULT_HIGHLIGHTS = [
	"Acceso 24/7 desde navegador",
	"Implementación operada por Nexo Contable",
	"Diseño ligero y responsive",
]

DEFAULT_STATS = [
	{"label": "Acceso", "value": "24/7"},
	{"label": "Branding", "value": "NexoERP"},
	{"label": "Soporte", "value": "WhatsApp"},
]


def _site_cache_key():
	site = getattr(frappe.local, "site", "default")
	return f"{CACHE_KEY}:{site}"


def _build_whatsapp_url(number, message):
	digits = "".join(ch for ch in (number or "") if ch.isdigit())
	if not digits:
		return ""
	url = f"https://wa.me/{digits}"
	if message:
		url += f"?text={quote(message)}"
	return url


def _load_tenant_settings():
	if not frappe.db.exists("DocType", "Nexo Tenant Branding"):
		return {}

	doc = frappe.get_single("Nexo Tenant Branding")
	return {
		"enabled": int(doc.enabled or 0),
		"portal_name": doc.tenant_display_name or DEFAULTS["portal_name"],
		"hero_kicker": doc.hero_kicker or DEFAULTS["hero_kicker"],
		"hero_title": doc.hero_title or DEFAULTS["hero_title"],
		"hero_subtitle": doc.hero_subtitle or DEFAULTS["hero_subtitle"],
		"hero_message": doc.hero_message or DEFAULTS["hero_message"],
		"login_title": doc.login_title or DEFAULTS["login_title"],
		"login_subtitle": doc.login_subtitle or DEFAULTS["login_subtitle"],
		"secondary_color": doc.secondary_color or DEFAULTS["secondary_color"],
		"whatsapp_number": doc.whatsapp_number or DEFAULTS["whatsapp_number"],
		"whatsapp_message": doc.whatsapp_message or DEFAULTS["whatsapp_message"],
		"footer_note": doc.footer_note or DEFAULTS["footer_note"],
		"theme_variant": doc.theme_variant or "base",
		"industry_variant": doc.industry_variant or "",
	}


def get_branding_context():
	def _build():
		data = DEFAULTS.copy()
		data.update(_load_tenant_settings())
		data["whatsapp_url"] = _build_whatsapp_url(data.get("whatsapp_number"), data.get("whatsapp_message"))
		data["benefits"] = DEFAULT_BENEFITS
		data["highlights"] = DEFAULT_HIGHLIGHTS
		data["stats"] = DEFAULT_STATS
		data["footer_links"] = [
			{"label": "Sitio Nexo Contable", "url": data["main_site_url"]},
			{"label": "WhatsApp", "url": data["whatsapp_url"]},
			{"label": "Ingresar", "url": "/login"},
		]
		return data

	if getattr(frappe.local, "dev_server", False):
		return _build()

	return frappe.cache.get_value(_site_cache_key(), _build)


def update_website_context(context):
	context.nexo_branding = get_branding_context()
	return context


def clear_branding_cache(*args, **kwargs):
	frappe.cache.delete_value(_site_cache_key())
	frappe.clear_cache()
	clear_website_cache()
