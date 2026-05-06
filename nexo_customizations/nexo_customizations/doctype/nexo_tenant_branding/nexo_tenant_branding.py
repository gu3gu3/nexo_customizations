import frappe
from frappe.model.document import Document

from nexo_customizations.utils.branding import clear_branding_cache


class NexoTenantBranding(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		enabled: DF.Check
		footer_note: DF.SmallText | None
		hero_kicker: DF.Data | None
		hero_message: DF.SmallText | None
		hero_subtitle: DF.SmallText | None
		hero_title: DF.Data | None
		industry_variant: DF.Data | None
		login_subtitle: DF.SmallText | None
		login_title: DF.Data | None
		secondary_color: DF.Color | None
		tenant_display_name: DF.Data | None
		theme_variant: DF.Data | None
		whatsapp_message: DF.SmallText | None
		whatsapp_number: DF.Data | None

	# end: auto-generated types
	def validate(self):
		if self.whatsapp_number:
			self.whatsapp_number = "".join(ch for ch in self.whatsapp_number if ch.isdigit() or ch == "+")

	def on_update(self):
		clear_branding_cache()
