#!/usr/bin/env bash
set -euo pipefail

# Resolver la ruta permite ejecutar el script desde cualquier carpeta.
proyecto_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd -- "$proyecto_dir"

for comando in javac java python3; do
    if ! command -v "$comando" > /dev/null 2>&1; then
        printf 'Falta el comando requerido: %s\n' "$comando" >&2
        exit 1
    fi
done

mkdir -p java/out
mapfile -d '' fuentes < <(find java/src/main/java -name '*.java' -print0)
javac -encoding UTF-8 -d java/out "${fuentes[@]}"

printf '\n=== JAVA ===\n'
java -cp java/out montecarlo.Main

printf '\n=== PYTHON ===\n'
python3 python/main.py
