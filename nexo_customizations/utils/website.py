import frappe


def get_home_page(user):
	if not user or user == "Guest":
		return "index"

	user_type = frappe.db.get_value("User", user, "user_type")
	if user_type == "Website User":
		return (frappe.db.get_single_value("Portal Settings", "default_portal_home") or "me").strip("/")

	return None



def get_logged_in_redirect():
	if frappe.session.user == "Guest":
		return None

	if frappe.session.data.user_type == "Website User":
		return "/" + get_home_page(frappe.session.user)

	return "/app"
