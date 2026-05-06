import frappe


@frappe.whitelist()
def setup_pos_for_company(company_name: str, company_abbr: str | None = None):
	company = frappe.get_doc("Company", company_name)
	company_abbr = company_abbr or company.abbr

	_enable_retail_domain_if_available()
	warehouse = _get_or_create_warehouse(company_name, company_abbr)
	mode_of_payment = _get_or_create_mode_of_payment(company_name)
	pos_profile = _get_or_create_pos_profile(company, warehouse, mode_of_payment)
	frappe.db.commit()
	return {"pos_profile": pos_profile.name, "warehouse": warehouse, "mode_of_payment": mode_of_payment}



def _enable_retail_domain_if_available():
	meta = frappe.get_meta("Domain Settings")
	if not meta.has_field("retail"):
		return

	doc = frappe.get_single("Domain Settings")
	if not cint_safe(doc.get("retail")):
		doc.set("retail", 1)
		doc.save(ignore_permissions=True)



def _get_or_create_warehouse(company_name: str, company_abbr: str):
	warehouse_name = f"Almacén Principal - {company_abbr}"
	if frappe.db.exists("Warehouse", warehouse_name):
		return warehouse_name

	warehouse = frappe.get_doc(
		{
			"doctype": "Warehouse",
			"warehouse_name": "Almacén Principal",
			"company": company_name,
		}
	)
	warehouse.insert(ignore_permissions=True)
	return warehouse.name



def _get_or_create_mode_of_payment(company_name: str):
	mode_of_payment = "Efectivo"
	if not frappe.db.exists("Mode of Payment", mode_of_payment):
		frappe.get_doc(
			{
				"doctype": "Mode of Payment",
				"mode_of_payment": mode_of_payment,
				"type": "Cash",
			}
		).insert(ignore_permissions=True)

	mop = frappe.get_doc("Mode of Payment", mode_of_payment)
	if not any((row.company == company_name) for row in mop.accounts):
		default_account = _find_cash_or_bank_account(company_name) or _find_income_account(company_name)
		if default_account:
			mop.append("accounts", {"company": company_name, "default_account": default_account})
			mop.save(ignore_permissions=True)

	return mode_of_payment



def _get_or_create_pos_profile(company, warehouse, mode_of_payment):
	profile_name = f"Punto de Venta - {company.abbr}"
	if frappe.db.exists("POS Profile", profile_name):
		return frappe.get_doc("POS Profile", profile_name)

	pos_profile = frappe.get_doc(
		{
			"doctype": "POS Profile",
			"name": profile_name,
			"company": company.name,
			"currency": company.default_currency or "NIO",
			"warehouse": warehouse,
			"selling_price_list": _get_selling_price_list(company.default_currency or "NIO"),
			"customer_group": _get_customer_group(),
			"territory": _get_territory(),
			"income_account": _find_income_account(company.name),
			"expense_account": _find_expense_account(company.name),
			"write_off_account": company.write_off_account or _find_expense_account(company.name),
			"write_off_cost_center": company.cost_center or _find_cost_center(company.name),
			"payments": [{"mode_of_payment": mode_of_payment, "default": 1}],
		}
	)
	pos_profile.insert(ignore_permissions=True)
	return pos_profile



def _get_selling_price_list(currency: str):
	price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
	if price_list:
		return price_list

	price_list = frappe.db.get_value("Price List", {"selling": 1, "currency": currency}, "name")
	if price_list:
		return price_list

	price_list = frappe.db.get_value("Price List", {"selling": 1}, "name")
	if price_list:
		return price_list

	frappe.throw("No existe un Price List de venta para configurar el POS Profile.")



def _get_customer_group():
	return frappe.db.get_value("Customer Group", {"is_group": 0}, "name")



def _get_territory():
	return frappe.db.get_value("Territory", {"is_group": 0}, "name")



def _find_income_account(company_name: str):
	return frappe.db.get_value(
		"Account",
		{"company": company_name, "root_type": "Income", "is_group": 0, "disabled": 0},
		"name",
		order_by="name asc",
	)



def _find_expense_account(company_name: str):
	return frappe.db.get_value(
		"Account",
		{"company": company_name, "root_type": "Expense", "is_group": 0, "disabled": 0},
		"name",
		order_by="name asc",
	)



def _find_cash_or_bank_account(company_name: str):
	return frappe.db.get_value(
		"Account",
		{"company": company_name, "account_type": ["in", ["Cash", "Bank"]], "is_group": 0, "disabled": 0},
		"name",
		order_by="name asc",
	)



def _find_cost_center(company_name: str):
	return frappe.db.get_value(
		"Cost Center",
		{"company": company_name, "is_group": 0, "disabled": 0},
		"name",
		order_by="name asc",
	)



def cint_safe(value):
	return int(value or 0)
