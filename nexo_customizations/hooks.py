app_name = "nexo_customizations"
app_title = "Nexo Customizations"
app_publisher = "Nexo Contable"
app_description = "Nexo Contable SaaS customizations"
app_email = "soporte@nexo-contable.com"
app_license = "mit"

web_include_css = ["nexo_website.bundle.css"]
web_include_js = ["nexo_website.bundle.js"]

after_install = "nexo_customizations.install.after_install"
after_migrate = "nexo_customizations.install.after_migrate"
get_website_user_home_page = "nexo_customizations.utils.website.get_home_page"

update_website_context = [
	"nexo_customizations.utils.branding.update_website_context",
]

doc_events = {
	"Nexo Tenant Branding": {
		"on_update": "nexo_customizations.utils.branding.clear_branding_cache",
	},
	"Website Settings": {
		"on_update": "nexo_customizations.utils.branding.clear_branding_cache",
	},
}

fixtures = [
	{
		"dt": "Color",
		"filters": [["name", "in", ["Nexo Blue", "Nexo Green", "Nexo Ink", "Nexo Mist"]]],
	}
]
