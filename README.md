# Nexo Customizations

App Frappe/ERPNext para branding reusable de **NexoERP** sobre ERPNext v15.

Incluye:
- landing SaaS branded en `/`
- login branded en `/login`
- theme base `Nexo SaaS Base`
- logo y favicon NexoERP
- configuración base por tenant con `Nexo Tenant Branding`
- fixtures versionables (`Color`, `Website Theme`)

## Compatibilidad
- Frappe `v15`
- ERPNext `v15`

## Instalación rápida
Desde un bench existente:

```bash
cd /home/frappe/frappe-bench
bench get-app https://github.com/gu3gu3/nexo_customizations.git
bench --site TU_SITE install-app nexo_customizations
bench pip install -e apps/nexo_customizations
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

## Sitios y rutas
Después de instalar:
- `/` → landing branded NexoERP
- `/login` → login branded NexoERP
- `/app` → Desk con nombre y logo NexoERP

## Estructura relevante
```text
nexo_customizations/
├── hooks.py
├── install.py
├── fixtures/
├── public/
│   ├── images/
│   ├── js/
│   └── scss/
├── templates/nexo/
├── utils/
└── www/
```

## Desarrollo local
```bash
cd /workspace/bench
bench --site erp.localhost install-app nexo_customizations
bench --site erp.localhost migrate
bench build --app nexo_customizations
bench start
```

## Producción
Ver guía detallada en:
- `docs/DEPLOY.md`

## License
MIT
