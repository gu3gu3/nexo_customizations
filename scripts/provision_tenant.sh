#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ENV_FILE:-$SCRIPT_DIR/../.env.provisioning}"

if [[ -f "$ENV_FILE" ]]; then
	set -a
	# shellcheck disable=SC1090
	source "$ENV_FILE"
	set +a
fi

: "${BENCH_DIR:?Missing BENCH_DIR}"
: "${BENCH_USER:?Missing BENCH_USER}"
: "${DB_ROOT_PASSWORD:?Missing DB_ROOT_PASSWORD}"
: "${ADMIN_EMAIL:?Missing ADMIN_EMAIL}"
: "${PARENT_DOMAIN:?Missing PARENT_DOMAIN}"

TENANT_SLUG="${1:-}"
COMPANY_NAME="${2:-}"
COMPANY_ABBR="${3:-}"

if [[ -z "$TENANT_SLUG" ]]; then
	echo "Uso: $0 <tenant-slug> [company-name] [company-abbr]"
	exit 1
fi

if [[ -z "$COMPANY_NAME" ]]; then
	COMPANY_NAME="$(python3 - <<PY
slug = "$TENANT_SLUG".replace("-", " ").strip()
print(" ".join(word.capitalize() for word in slug.split()) + " Corp")
PY
)"
fi

if [[ -z "$COMPANY_ABBR" ]]; then
	COMPANY_ABBR="$(python3 - <<PY
slug = "$TENANT_SLUG".replace("-", "")
print((slug[:5] or "NEXO").upper())
PY
)"
fi

if [[ -n "${SITE_SUBDOMAIN:-}" ]]; then
	FULL_DOMAIN="${TENANT_SLUG}.${SITE_SUBDOMAIN}.${PARENT_DOMAIN}"
else
	FULL_DOMAIN="${TENANT_SLUG}.${PARENT_DOMAIN}"
fi

ADMIN_PASSWORD="$(python3 - <<PY
import secrets, string
alphabet = string.ascii_letters + string.digits + !@#%^*-_
print(Adm- + .join(secrets.choice(alphabet) for _ in range(18)))
PY
)"

run_bench() {
	sudo -u "$BENCH_USER" -H bash -lc "cd  && PATH=/home/$BENCH_USER/.local/bin:\$PATH $*"
}

if [[ "${ENABLE_DNS_AUTOMATION:-0}" == "1" ]]; then
	: "${NAMECOM_API_USER:?Missing NAMECOM_API_USER}"
	: "${NAMECOM_API_TOKEN:?Missing NAMECOM_API_TOKEN}"
	ANSWER="${PUBLIC_IP:-$(curl -s ifconfig.me)}"
	HOSTNAME_PART="$TENANT_SLUG${SITE_SUBDOMAIN:+.$SITE_SUBDOMAIN}"
	curl -s -u "$NAMECOM_API_USER:$NAMECOM_API_TOKEN" \
		-X POST "https://api.name.com/v4/domains/$PARENT_DOMAIN/records" \
		-H "Content-Type: application/json" \
		-d "{\"host\":\"$HOSTNAME_PART\",\"type\":\"A\",\"answer\":\"$ANSWER\",\"ttl\":300}" >/dev/null
	echo "DNS record created for $FULL_DOMAIN"
fi

run_bench "bench pip install -e apps/nexo_customizations"
run_bench "bench new-site  --mariadb-root-password  --admin-password "
run_bench "bench --site  install-app erpnext"
run_bench "bench --site  install-app nexo_customizations"
run_bench "bench --site  migrate"
run_bench "bench build --app nexo_customizations"
run_bench "bench --site  execute nexo_customizations.provisioning.provision_tenant --kwargs "company_name":"""
run_bench "bench --site  clear-cache"

if [[ "${APPLY_NGINX:-0}" == "1" ]]; then
	run_bench "bench setup nginx --yes"
	sudo cp "$BENCH_DIR/config/nginx.conf" /etc/nginx/conf.d/frappe-bench.conf
	sudo systemctl reload nginx
fi

if [[ "${ENABLE_SSL:-0}" == "1" ]]; then
	sudo certbot --nginx -d "$FULL_DOMAIN" --non-interactive --agree-tos -m "$ADMIN_EMAIL"
fi

echo "Provisioning completed"
echo "Site: https://$FULL_DOMAIN"
echo "User: Administrator"
echo "Password: $ADMIN_PASSWORD"
