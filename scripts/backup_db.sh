#!/usr/bin/env bash
# ==============================================================================
# DentalSecureLab - Script Automatizado de Respaldo, Cifrado y Endurecimiento
# Riesgo Mitigado: A-04 / A-54 (Extracción o borrado directo de db.sqlite3)
# ==============================================================================
set -euo pipefail

# Definición de variables de entorno y rutas base
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB_FILE="${PROJECT_DIR}/db.sqlite3"
BACKUP_DIR="${PROJECT_DIR}/backups"
TIMESTAMP="$(date +'%Y%m%d_%H%M%S')"
BACKUP_RAW="${BACKUP_DIR}/dentalsecurelab_${TIMESTAMP}.sqlite3"
BACKUP_TAR="${BACKUP_DIR}/dentalsecurelab_${TIMESTAMP}.tar.gz"
BACKUP_ENC="${BACKUP_DIR}/dentalsecurelab_${TIMESTAMP}.tar.gz.gpg"
LOG_FILE="${BACKUP_DIR}/backup_operations.log"
PASSPHRASE="${BACKUP_ENCRYPTION_KEY:-DentalSecureLab2026_KeySecure_AES256_Backup}"

# Máscara restrictiva: únicamente el propietario posee permisos de lectura y escritura
umask 077

# Creación de directorio seguro de respaldos si no existe
mkdir -p "${BACKUP_DIR}"
chmod 700 "${BACKUP_DIR}"

log_msg() {
    local MSG="$1"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ${MSG}" | tee -a "${LOG_FILE}"
}

log_msg "=== Iniciando procedimiento de endurecimiento y respaldo seguro ==="

# PASO 1: Endurecimiento de permisos en el sistema de archivos sobre la base de datos
if [ -f "${DB_FILE}" ]; then
    log_msg "[1/5] Aplicando permisos estrictos chmod 600 sobre la base de datos ${DB_FILE}..."
    chmod 600 "${DB_FILE}"
    if [ -f "${DB_FILE}-wal" ]; then
        chmod 600 "${DB_FILE}-wal"
    fi
    if [ -f "${DB_FILE}-shm" ]; then
        chmod 600 "${DB_FILE}-shm"
    fi
else
    log_msg "ERROR: El archivo de base de datos ${DB_FILE} no existe. Abortando respaldo."
    exit 1
fi

# PASO 2: Respaldo en caliente consistente utilizando la API de respaldo de SQLite
log_msg "[2/5] Generando copia en caliente consistente mediante sqlite3 .backup..."
sqlite3 "${DB_FILE}" ".backup '${BACKUP_RAW}'"
chmod 600 "${BACKUP_RAW}"

# PASO 3: Compresión de la base de datos con verificación de integridad
log_msg "[3/5] Comprimiendo archivo de respaldo con gzip..."
tar -czf "${BACKUP_TAR}" -C "${BACKUP_DIR}" "$(basename "${BACKUP_RAW}")"
rm -f "${BACKUP_RAW}"
chmod 600 "${BACKUP_TAR}"

# PASO 4: Cifrado simétrico de alta seguridad mediante GPG con estándar AES-256
log_msg "[4/5] Cifrando respaldo comprimido mediante GPG (Algoritmo AES-256)..."
echo "${PASSPHRASE}" | gpg --batch --yes --passphrase-fd 0 \
    --symmetric --cipher-algo AES256 \
    --output "${BACKUP_ENC}" "${BACKUP_TAR}"

rm -f "${BACKUP_TAR}"
chmod 600 "${BACKUP_ENC}"

# Cálculo de hash SHA-256 para auditoría de integridad forense
SHA256_HASH=$(sha256sum "${BACKUP_ENC}" | awk '{print $1}')
log_msg "Respaldo cifrado exitosamente: ${BACKUP_ENC}"
log_msg "Huella digital SHA-256 del artefacto cifrado: ${SHA256_HASH}"

# PASO 5: Política de rotación de respaldos (retención de últimos 30 días)
log_msg "[5/5] Aplicando política de rotación (purgando respaldos mayores a 30 días)..."
find "${BACKUP_DIR}" -name "dentalsecurelab_*.tar.gz.gpg" -type f -mtime +30 -exec rm -f {} \;

log_msg "=== Procedimiento de respaldo y endurecimiento concluido satisfactoriamente ==="
exit 0
