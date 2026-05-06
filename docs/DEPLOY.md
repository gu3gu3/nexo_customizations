# Deploy de nexo_customizations a producción

## 1. Prerrequisitos
- Bench productivo con Frappe/ERPNext v15
- Acceso SSH al servidor
- Git instalado
- Repo accesible desde el servidor

## 2. Obtener la app
```bash
cd /home/frappe/frappe-bench
bench get-app https://github.com/gu3gu3/nexo_customizations.git
```

Si ya existe:
```bash
cd /home/frappe/frappe-bench/apps/nexo_customizations
git pull origin main
```

## 3. Instalar dependencias Python de la app
```bash
cd /home/frappe/frappe-bench
bench pip install -e apps/nexo_customizations
```

## 4. Instalar en el site
```bash
bench --site TU_SITE install-app nexo_customizations
```

## 5. Migrar y compilar assets
```bash
bench --site TU_SITE migrate
bench build --app nexo_customizations
```

## 6. Aplicar branding y defaults
```bash
bench --site TU_SITE execute nexo_customizations.install.ensure_colors
bench --site TU_SITE execute nexo_customizations.install.ensure_website_theme
bench --site TU_SITE execute nexo_customizations.install.apply_site_defaults
bench --site TU_SITE execute nexo_customizations.install.ensure_tenant_branding_defaults
bench --site TU_SITE clear-cache
```

## 7. Reiniciar servicios
```bash
bench restart
```

## 8. Validaciones
Revisar:
- `https://tu-dominio/`
- `https://tu-dominio/login`
- `https://tu-dominio/app`

Validar:
- nombre NexoERP
- logo y favicon correctos
- landing branded
- login branded

## 9. Nuevos tenants
Para cada tenant nuevo:
```bash
bench --site NUEVO_SITE install-app nexo_customizations
bench pip install -e apps/nexo_customizations
bench --site NUEVO_SITE migrate
bench build --app nexo_customizations
bench --site NUEVO_SITE execute nexo_customizations.install.ensure_colors
bench --site NUEVO_SITE execute nexo_customizations.install.ensure_website_theme
bench --site NUEVO_SITE execute nexo_customizations.install.apply_site_defaults
bench --site NUEVO_SITE execute nexo_customizations.install.ensure_tenant_branding_defaults
bench --site NUEVO_SITE clear-cache
```
