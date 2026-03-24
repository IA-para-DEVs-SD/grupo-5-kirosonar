#!/bin/bash
# =============================================================================
# restore-db.sh - PostgreSQL Restore Script for ERP Gráficas Expressas
# Requisito 15.2: THE Sistema SHALL permitir restaurar dados a partir de um backup
# =============================================================================

set -euo pipefail

DB_HOST="${DB_HOST:-postgres}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-erp_grafica}"
DB_USER="${DB_USER:-erp_user}"
PGPASSWORD="${DB_PASSWORD:-erp_password_dev}"
export PGPASSWORD

BACKUP_DIR="${BACKUP_DIR:-/backups}"
LOG_FILE="${BACKUP_DIR}/restore.log"

log() {
  local level="$1"; shift
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] [${level}] $*" | tee -a "${LOG_FILE}"
}

usage() {
  echo "Usage: $0 <backup_file>"
  echo "  backup_file: path to a .sql.gz backup file"
  echo ""
  echo "Available backups:"
  find "${BACKUP_DIR}" -maxdepth 1 -name "erp_grafica_*.sql.gz" -type f | sort
  exit 1
}

BACKUP_FILE="${1:-}"
[[ -z "${BACKUP_FILE}" ]] && usage
[[ ! -f "${BACKUP_FILE}" ]] && { log "ERROR" "File not found: ${BACKUP_FILE}"; exit 1; }

log "INFO" "Starting restore from: ${BACKUP_FILE}"
log "WARN" "This will DROP and recreate the database ${DB_NAME}. Press Ctrl+C within 5 seconds to abort."
sleep 5

# Drop and recreate database
psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres \
  -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='${DB_NAME}' AND pid <> pg_backend_pid();" \
  >> "${LOG_FILE}" 2>&1

psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres \
  -c "DROP DATABASE IF EXISTS ${DB_NAME};" >> "${LOG_FILE}" 2>&1

psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d postgres \
  -c "CREATE DATABASE ${DB_NAME};" >> "${LOG_FILE}" 2>&1

# Restore
if gunzip -c "${BACKUP_FILE}" | psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
    >> "${LOG_FILE}" 2>&1; then
  log "INFO" "Restore completed successfully from ${BACKUP_FILE}"
else
  log "ERROR" "Restore failed from ${BACKUP_FILE}"
  exit 1
fi
