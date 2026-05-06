from pathlib import Path

import frappe
from frappe.website.utils import clear_cache as clear_website_cache

THEME_NAME = "Nexo SaaS Base"
APP_NAME = "NexoERP"
COMPANY_NAME = "Nexo Contable"
LOGO_PATH = "/assets/nexo_customizations/images/logo.png"
FAVICON_PATH = "/assets/nexo_customizations/images/n-logo.png"
COLORS = {
	"Nexo Blue": "#1E5EFF",
	"Nexo Green": "#19C37D",
	"Nexo Ink": "#0F172A",
	"Nexo Mist": "#F7FAFC",
}


def after_install():
	ensure_colors()
	ensure_website_theme()
	apply_site_defaults()
	ensure_tenant_branding_defaults()
	clear_caches()


@frappe.whitelist()
def apply_site_defaults():
	website_settings = frappe.get_single("Website Settings")
	website_settings.home_page = "index"
	website_settings.website_theme = THEME_NAME
	website_settings.app_name = APP_NAME
	website_settings.app_logo = LOGO_PATH
	website_settings.favicon = FAVICON_PATH
	website_settings.disable_signup = 1
	website_settings.show_footer_on_login = 0
	website_settings.copyright = f"© {COMPANY_NAME}"
	website_settings.save(ignore_permissions=True)

	navbar_settings = frappe.get_single("Navbar Settings")
	navbar_settings.app_logo = LOGO_PATH
	navbar_settings.save(ignore_permissions=True)

	frappe.db.set_single_value("System Settings", "app_name", APP_NAME)


@frappe.whitelist()
def ensure_tenant_branding_defaults():
	if not frappe.db.exists("DocType", "Nexo Tenant Branding"):
		return

	doc = frappe.get_single("Nexo Tenant Branding")
	defaults = {
		"enabled": 1,
		"tenant_display_name": "Portal NexoERP",
		"hero_kicker": "ERP cloud para Nicaragua",
		"hero_title": "Administra tu operación con NexoERP.",
		"hero_subtitle": "Ingresa a NexoERP con una experiencia SaaS moderna, rápida y segura, operada por Nexo Contable.",
		"hero_message": "Contabilidad, facturación, compras, ventas y visibilidad financiera en una sola plataforma.",
		"login_title": "Accede a NexoERP",
		"login_subtitle": "Ingresa con tu correo y contraseña corporativa.",
		"secondary_color": COLORS["Nexo Green"],
		"whatsapp_number": "50500000000",
		"whatsapp_message": "Hola, necesito ayuda con NexoERP.",
		"footer_note": "Plataforma SaaS NexoERP operada por Nexo Contable.",
		"theme_variant": "base",
		"industry_variant": "",
	}

	legacy_values = {
		"tenant_display_name": {"Portal Nexo Contable"},
		"hero_kicker": {"ERP y contabilidad en la nube"},
		"hero_title": {"Tu operación contable en un portal moderno, rápido y seguro."},
		"hero_subtitle": {
			"Accede a ERPNext con una experiencia SaaS alineada a Nexo Contable.",
		},
		"hero_message": {"Administra tu operación, consulta tu información y recibe soporte desde un solo lugar."},
		"login_title": {"Ingresa a tu portal"},
		"login_subtitle": {"Usa tu correo y contraseña corporativa."},
		"whatsapp_message": {"Hola, necesito ayuda con mi portal Nexo Contable."},
		"footer_note": {"SaaS ERPNext operado por Nexo Contable."},
	}

	updated = False
	for fieldname, value in defaults.items():
		current_value = doc.get(fieldname)
		if not current_value or current_value in legacy_values.get(fieldname, set()):
			doc.set(fieldname, value)
			updated = True

	if updated:
		doc.save(ignore_permissions=True)


@frappe.whitelist()
def ensure_colors():
	for name, color in COLORS.items():
		if frappe.db.exists("Color", name):
			doc = frappe.get_doc("Color", name)
			doc.color = color
			doc.save(ignore_permissions=True)
		else:
			frappe.get_doc({"doctype": "Color", "name": name, "color": color}).insert(ignore_permissions=True)


@frappe.whitelist()
def ensure_website_theme():
	data = {
		"doctype": "Website Theme",
		"theme": THEME_NAME,
		"module": "Website",
		"custom": 1,
		"google_font": "Inter",
		"font_properties": "wght@300;400;500;600;700;800",
		"primary_color": "Nexo Blue",
		"text_color": "Nexo Ink",
		"dark_color": "Nexo Ink",
		"light_color": "Nexo Green",
		"background_color": "Nexo Mist",
		"button_rounded_corners": 1,
		"button_shadows": 0,
		"button_gradients": 0,
		"custom_overrides": "",
		"custom_scss": "",
		"js": "",
	}

	if frappe.db.exists("Website Theme", THEME_NAME):
		doc = frappe.get_doc("Website Theme", THEME_NAME)
		for key, value in data.items():
			if key != "doctype":
				doc.set(key, value)
	else:
		doc = frappe.get_doc(data)

	doc.save(ignore_permissions=True)
	patch_theme_file(doc.theme_url)



def patch_theme_file(theme_url):
	if not theme_url:
		return

	file_path = Path(frappe.utils.get_site_path("public", theme_url.lstrip("/")))
	if not file_path.exists():
		return

	content = file_path.read_text(encoding="utf-8-sig")
	content = content.replace(
		"@import\"frappe/public/css/fonts/inter/inter.css\";",
		"@import\"/assets/frappe/css/fonts/inter/inter.css\";",
	)
	file_path.write_text(content, encoding="utf-8")



def clear_caches():
	frappe.clear_cache()
	clear_website_cache()
