import frappe

WEB_FORM_NAME = "solicitud-de-onboarding"
WEB_FORM_ROUTE = "solicitud-onboarding"


@frappe.whitelist()
def ensure_onboarding_web_form():
	if not frappe.db.exists("DocType", "Onboarding Request"):
		frappe.throw("El DocType Onboarding Request no existe en este site.")

	fields = []
	for df in frappe.get_meta("Onboarding Request").fields:
		if df.fieldtype in {"Section Break", "Column Break", "Tab Break", "Fold", "HTML", "Table"}:
			continue
		fields.append(
			{
				"fieldname": df.fieldname,
				"label": df.label,
				"fieldtype": df.fieldtype,
				"options": df.options,
				"reqd": df.reqd,
				"default": df.default,
				"read_only": df.read_only,
				"hidden": df.hidden,
			}
		)

	payload = {
		"title": "Solicitud de Onboarding",
		"route": WEB_FORM_ROUTE,
		"doc_type": "Onboarding Request",
		"published": 1,
		"login_required": 0,
		"allow_edit": 0,
		"allow_multiple": 0,
		"show_list": 0,
		"show_attachments": 1,
		"success_message": "¡Gracias por tu solicitud! Hemos recibido tu información y pronto nos pondremos en contacto.",
	}

	if frappe.db.exists("Web Form", WEB_FORM_NAME):
		web_form = frappe.get_doc("Web Form", WEB_FORM_NAME)
		for key, value in payload.items():
			web_form.set(key, value)
		web_form.set("web_form_fields", [])
		for field in fields:
			web_form.append("web_form_fields", field)
		web_form.save(ignore_permissions=True)
	else:
		web_form = frappe.get_doc({"doctype": "Web Form", "name": WEB_FORM_NAME, **payload, "web_form_fields": fields})
		web_form.insert(ignore_permissions=True)

	frappe.db.commit()
	return {"web_form": web_form.name, "route": web_form.route}
