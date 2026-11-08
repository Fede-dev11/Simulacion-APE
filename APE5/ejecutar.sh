#!/usr/bin/env bash
set -euo pipefail

mkdir -p java/out
javac -d java/out $(find java/src -name '*.java')
PYTHONPATH=python/src python3 -m simulacion.main --output resultados_python
java -Djava.awt.headless=true -cp java/out simulacion.Main 12345 67890 10000 resultados_java
python3 comparar.py
python3 grafica.py
