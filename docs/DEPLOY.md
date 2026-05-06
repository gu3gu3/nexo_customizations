# Deploy de nexo_customizations a producción

## 1. Obtener la app
```bash
cd /home/frappe/frappe-bench
bench get-app https://github.com/gu3gu3/nexo_customizations.git
```

Si la carpeta ya existe, no la sobreescribas sin revisar. Mejor:
```bash
cd /home/frappe/frappe-bench/apps/nexo_customizations
git status
git remote -v
```

## 2. Instalar dependencias Python de la app
```bash
cd /home/frappe/frappe-bench
bench pip install -e apps/nexo_customizations
```

## 3. Instalar en el site
```bash
bench --site TU_SITE install-app nexo_customizations
```

## 4. Migrar y compilar assets
```bash
bench --site TU_SITE migrate
bench build --app nexo_customizations
```

## 5. Aplicar branding y defaults
```bash
bench --site TU_SITE execute nexo_customizations.install.ensure_colors
bench --site TU_SITE execute nexo_customizations.install.ensure_website_theme
bench --site TU_SITE execute nexo_customizations.install.apply_site_defaults
bench --site TU_SITE execute nexo_customizations.install.ensure_tenant_branding_defaults
bench --site TU_SITE clear-cache
```

## 6. Provisionar compañía Nicaragua y POS
```bash
bench --site TU_SITE execute nexo_customizations.provisioning.provision_tenant --kwargs company_name:Cliente Demo Corp
```

## 7. Crear Web Form de onboarding si aplica
```bash
bench --site TU_SITE execute nexo_customizations.onboarding.ensure_onboarding_web_form
```

## 8. Reiniciar servicios
```bash
bench restart
```

## 9. Validaciones
Revisar:
- `https://tu-dominio/`
- `https://tu-dominio/login`
- `https://tu-dominio/app`
- `https://tu-dominio/solicitud-onboarding` si habilitaste onboarding
