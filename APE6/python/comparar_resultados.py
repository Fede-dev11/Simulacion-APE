import csv
from pathlib import Path

from views.graficas import VistaGraficas

BASE = Path(__file__).resolve().parents[1]
PYTHON = BASE / "python" / "resultados"
JAVA = BASE / "java" / "resultados"
TOLERANCIA_NORMALIZADOS = 1e-15
TOLERANCIA_ESTADISTICOS = 1e-12
TOLERANCIA_VALORES_P = 1e-12


def leer_csv(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def resultados_por_prueba(directorio: Path) -> dict[str, dict[str, str]]:
    return {fila["prueba"]: fila for fila in leer_csv(directorio / "resultados_pruebas.csv")}


def comparar_secuencias() -> tuple[bool, float, list[float]]:
    python = leer_csv(PYTHON / "secuencia.csv")
    java = leer_csv(JAVA / "secuencia.csv")
    if len(python) != len(java):
        return False, float("inf"), []
    estados_iguales = all(p["estado"] == j["estado"] for p, j in zip(python, java))
    diferencias = [abs(float(p["valor_normalizado"]) - float(j["valor_normalizado"])) for p, j in zip(python, java)]
    return estados_iguales, max(diferencias, default=0.0), [float(j["valor_normalizado"]) for j in java]


def main() -> None:
    estados_iguales, diferencia_maxima, secuencia_java = comparar_secuencias()
    py = resultados_por_prueba(PYTHON)
    ja = resultados_por_prueba(JAVA)
    chi_py, chi_ja = py["Chi-cuadrado"], ja["Chi-cuadrado"]
    ks_py, ks_ja = py["Kolmogorov-Smirnov"], ja["Kolmogorov-Smirnov"]

    fila = {
        "configuracion": "propuesta_base",
        "N": len(secuencia_java),
        "estados_coinciden": estados_iguales,
        "max_diferencia_normalizados": format(diferencia_maxima, ".17g"),
        "chi2_python": chi_py["estadistico"],
        "chi2_java": chi_ja["estadistico"],
        "gl": chi_py["gl"],
        "p_chi2_python": chi_py["valor_p"],
        "p_chi2_java": chi_ja["valor_p"],
        "decision_chi2_python": chi_py["decision"],
        "decision_chi2_java": chi_ja["decision"],
        "D_python": ks_py["estadistico"],
        "D_java": ks_ja["estadistico"],
        "p_ks_python": ks_py["valor_p"],
        "p_ks_java": ks_ja["valor_p"],
        "decision_ks_python": ks_py["decision"],
        "decision_ks_java": ks_ja["decision"],
    }
    ruta = BASE / "comparacion_resultados.csv"
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fila.keys())
        escritor.writeheader()
        escritor.writerow(fila)

    VistaGraficas().guardar(secuencia_java, 10, JAVA)
    errores = []
    if not estados_iguales: errores.append("los estados enteros no coinciden")
    if diferencia_maxima > TOLERANCIA_NORMALIZADOS: errores.append("los normalizados exceden la tolerancia")
    for nombre, a, b, tol in (
        ("chi2", chi_py["estadistico"], chi_ja["estadistico"], TOLERANCIA_ESTADISTICOS),
        ("p chi2", chi_py["valor_p"], chi_ja["valor_p"], TOLERANCIA_VALORES_P),
        ("D", ks_py["estadistico"], ks_ja["estadistico"], TOLERANCIA_ESTADISTICOS),
        ("p KS", ks_py["valor_p"], ks_ja["valor_p"], TOLERANCIA_VALORES_P),
    ):
        if abs(float(a) - float(b)) > tol: errores.append(f"{nombre} excede la tolerancia {tol}")
    if errores:
        raise AssertionError("; ".join(errores))

    print(f"Estados enteros idénticos: {estados_iguales} ({len(secuencia_java)} de {len(secuencia_java)})")
    print(f"Máxima diferencia normalizada: {diferencia_maxima:.3g}")
    print(f"Comparación aprobada con tolerancias: normalizados={TOLERANCIA_NORMALIZADOS:g}, "
          f"estadísticos={TOLERANCIA_ESTADISTICOS:g}, valores p={TOLERANCIA_VALORES_P:g}")
    print(f"Tabla: {ruta}")


if __name__ == "__main__":
    main()
