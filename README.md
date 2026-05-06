# Nexo Customizations

App Frappe/ERPNext para branding reusable de **NexoERP** y automatización base de onboarding para ERPNext v15.

## Incluye
- landing SaaS branded en `/`
- login branded en `/login`
- theme base `Nexo SaaS Base`
- logo y favicon NexoERP
- configuración base por tenant con `Nexo Tenant Branding`
- defaults para Nicaragua
- bootstrap opcional de POS por compañía
- DocType `Onboarding Request`
- helper para crear Web Form de onboarding
- script seguro de aprovisionamiento de tenants

## Compatibilidad
- Frappe `v15`
- ERPNext `v15`

## Instalación rápida
```bash
cd /home/frappe/frappe-bench
bench get-app https://github.com/gu3gu3/nexo_customizations.git
bench pip install -e apps/nexo_customizations
bench --site TU_SITE install-app nexo_customizations
bench --site TU_SITE migrate
bench build --app nexo_customizations
```

## Aplicar branding base
```bash
bench --site TU_SITE execute nexo_customizations.install.ensure_colors
bench --site TU_SITE execute nexo_customizations.install.ensure_website_theme
bench --site TU_SITE execute nexo_customizations.install.apply_site_defaults
bench --site TU_SITE execute nexo_customizations.install.ensure_tenant_branding_defaults
bench --site TU_SITE clear-cache
bench restart
```

## Provisionar defaults Nicaragua + POS
```bash
bench --site TU_SITE execute nexo_customizations.provisioning.provision_tenant --kwargs company_name:Cliente Demo Corp
```

## Crear Web Form de onboarding
```bash
bench --site TU_SITE execute nexo_customizations.onboarding.ensure_onboarding_web_form
```

Ruta resultante por defecto:
- `/solicitud-onboarding`

## Si `bench get-app` dice que la app ya existe
No sobrescribas a ciegas. Revisa primero:

```bash
cd /home/frappe/frappe-bench/apps/nexo_customizations
git status
git remote -v
```

Si ya está conectada a este repo:
```bash
git pull origin main
cd /home/frappe/frappe-bench
bench pip install -e apps/nexo_customizations
bench --site TU_SITE migrate
bench build --app nexo_customizations
bench --site TU_SITE clear-cache
bench restart
```

## Documentación
- `docs/DEPLOY.md`
- `docs/PROVISIONING.md`

## License
MIT
