#!/bin/bash
# Compilation des programmes COBOL batch avec GnuCOBOL
# Les programmes DB2 et CICS ne sont pas compilables localement
# (necessitent le precompilateur DB2 et le traducteur CICS)

set -e

BATCH_DIR="/app/01-batch/cobol"
BIN_DIR="/app/bin"
DATA_DIR="/app/01-batch/data"

echo "=== Compilation des programmes batch ==="

for src in "$BATCH_DIR"/*.cbl; do
    pgm=$(basename "$src" .cbl)

    # PJ14CPT, PJ14PRO, PJ14REG sont des sous-programmes (pas de STOP RUN)
    if [[ "$pgm" == PJ14CPT || "$pgm" == PJ14PRO || "$pgm" == PJ14REG ]]; then
        echo "  [MODULE] $pgm"
        cobc -m "$src" -o "$BIN_DIR/$pgm.so" 2>&1 || echo "  SKIP $pgm (erreur compilation)"
        continue
    fi

    echo "  [EXEC]   $pgm"
    cobc -x "$src" -o "$BIN_DIR/$pgm" 2>&1 || echo "  SKIP $pgm (erreur compilation)"
done

echo "=== Compilation terminee ==="
ls -la "$BIN_DIR"/

echo "=== Creation des fichiers indexes ==="
cd "$DATA_DIR"
rm -f *.ix *.ix.*
"$BIN_DIR/MKINDEX" 2>&1 || echo "  ERREUR creation index"
echo "=== Index crees ==="
