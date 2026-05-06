# Provisioning automatizado de tenants

El repo incluye un script base en:

- `scripts/provision_tenant.sh`

## Objetivo
Automatizar:
- creación del site
- instalación de ERPNext y `nexo_customizations`
- aplicación de branding NexoERP
- defaults Nicaragua
- POS opcional
- DNS/Nginx/SSL de forma opcional y segura por variables de entorno

## Variables
Copia:
```bash
cp scripts/env.example .env.provisioning
```

Luego completa secretos y rutas.

## Ejemplo de uso
```bash
bash scripts/provision_tenant.sh cliente-demo "Cliente Demo Corp" CDC
```

## Notas
- no hardcodees tokens ni passwords en el script
- rota credenciales viejas de Name.com si alguna vez se expusieron
- usa el script como base y adáptalo al servidor real
