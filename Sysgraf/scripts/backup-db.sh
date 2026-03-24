#!/bin/bash
# =============================================================================
# backup-db.sh - PostgreSQL Backup Script for ERP Gráficas Expressas
# Requisitos: 15.1 (backups automáticos diários), 15.2 (restauração),
#             15.3 (registrar data/hora/status), 15.4 (30 dias de histórico),
#             15.5 (notificar admin em caso de falha)
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration (can be overridden via environment variables)
# ---------------------------------------------------------------------------
DB_HOST="${DB_HOST:-postgres}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-erp_grafica}"
DB_USER="${DB_USER:-erp_user}"
PGPASSWORD="${DB_PASSWORD:-erp_password_dev}"
export PGPASSWORD

BACKUP_DIR="${BACKUP_DIR:-/backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILENAME="erp_grafica_${TIMESTAMP}.sql.gz"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILENAME}"
LOG_FILE="${BACKUP_DIR}/backup.log"

# Admin notification (optional – set ADMIN_EMAIL to enable)
ADMIN_EMAIL="${ADMIN_EMAIL:-}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
log() {
  local level="$1"
  shift
  local msg="$*"
  local ts
  ts=$(date +"%Y-%m-%d %H:%M:%S")
  echo "[${ts}] [${level}] ${msg}" | tee -a "${LOG_FILE}"
}

notify_admin() {
  local subject="$1"
  local body="$2"
  if [[ -n "${ADMIN_EMAIL}" ]]; then
    if command -v mail &>/dev/null; then
      echo "${body}" | mail -s "${subject}" "${ADMIN_EMAIL}" || true
    else
      log "WARN" "mail command not available – cannot send email to ${ADMIN_EMAIL}"
    fi
  fi
  log "INFO" "Admin notification: ${subject} | ${body}"
}

record_backup_status() {
  local status="$1"
  local size_bytes="${2:-0}"
  local error_msg="${3:-}"
  local retention_until
  retention_until=$(date -d "+${RETENTION_DAYS} days" +"%Y-%m-%d %H:%M:%S" 2>/dev/null \
    || date -v "+${RETENTION_DAYS}d" +"%Y-%m-%d %H:%M:%S" 2>/dev/null \
    || echo "")

  psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
    -c "INSERT INTO backup_metadata (backup_name, backup_type, status, size_bytes, completed_at, error_message, retention_until)
        VALUES ('${BACKUP_FILENAME}', 'full', '${status}', ${size_bytes},
                CURRENT_TIMESTAMP,
                $([ -n "${error_msg}" ] && echo "'${error_msg}'" || echo "NULL"),
                $([ -n "${retention_until}" ] && echo "'${retention_until}'" || echo "NULL"));" \
    >> "${LOG_FILE}" 2>&1 || log "WARN" "Could not record backup metadata to database"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
mkdir -p "${BACKUP_DIR}"

log "INFO" "Starting backup: ${BACKUP_FILENAME}"
log "INFO" "Database: ${DB_NAME} @ ${DB_HOST}:${DB_PORT}"

# Record backup start
psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
  -c "INSERT INTO backup_metadata (backup_name, backup_type, status)
      VALUES ('${BACKUP_FILENAME}', 'full', 'running');" \
  >> "${LOG_FILE}" 2>&1 || log "WARN" "Could not record backup start to database"

# Perform pg_dump
if pg_dump \
    -h "${DB_HOST}" \
    -p "${DB_PORT}" \
    -U "${DB_USER}" \
    -d "${DB_NAME}" \
    --format=plain \
    --no-password \
    --verbose \
    2>>"${LOG_FILE}" \
  | gzip > "${BACKUP_PATH}"; then

  SIZE_BYTES=$(stat -c%s "${BACKUP_PATH}" 2>/dev/null || stat -f%z "${BACKUP_PATH}" 2>/dev/null || echo 0)
  log "INFO" "Backup completed successfully: ${BACKUP_PATH} (${SIZE_BYTES} bytes)"
  record_backup_status "success" "${SIZE_BYTES}"

else
  ERROR_MSG="pg_dump failed for ${BACKUP_FILENAME}"
  log "ERROR" "${ERROR_MSG}"
  record_backup_status "failed" "0" "${ERROR_MSG}"
  notify_admin "[ERP] Backup FAILED - ${TIMESTAMP}" \
    "Backup ${BACKUP_FILENAME} failed at $(date). Check ${LOG_FILE} for details."
  exit 1
fi

# ---------------------------------------------------------------------------
# Retention: remove backups older than RETENTION_DAYS
# ---------------------------------------------------------------------------
log "INFO" "Applying retention policy: keeping last ${RETENTION_DAYS} days"
find "${BACKUP_DIR}" -maxdepth 1 -name "erp_grafica_*.sql.gz" \
  -mtime "+${RETENTION_DAYS}" -type f | while read -r old_backup; do
  log "INFO" "Removing old backup: ${old_backup}"
  rm -f "${old_backup}"
done

# Log remaining backup count
BACKUP_COUNT=$(find "${BACKUP_DIR}" -maxdepth 1 -name "erp_grafica_*.sql.gz" -type f | wc -l)
log "INFO" "Retention cleanup done. Backups retained: ${BACKUP_COUNT}"

log "INFO" "Backup process finished successfully"
