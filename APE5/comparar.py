import csv
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main() -> None:
    python_rows = read_rows(Path("resultados_python/semilla_12345.csv"))
    java_rows = read_rows(Path("resultados_java/semilla_12345.csv"))
    if len(python_rows) != len(java_rows):
        raise SystemExit("ERROR: las cantidades generadas son distintas")

    output = Path("tabla_comparacion.csv")
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(("n", "X_Python", "X_Java", "U_Python", "U_Java", "Coincide"))
        print(" n | X Python    | X Java      | ¿Coincide?")
        print("---+-------------+-------------+-----------")
        all_equal = True
        for index, (py, java) in enumerate(zip(python_rows, java_rows), start=1):
            equal = py["X_n"] == java["X_n"] and py["U_n"] == java["U_n"]
            all_equal &= equal
            writer.writerow((index, py["X_n"], java["X_n"], py["U_n"], java["U_n"], "Sí" if equal else "No"))
            if index <= 20:
                print(f"{index:2d} | {py['X_n']:>11} | {java['X_n']:>11} | {'Sí' if equal else 'No':>9}")

    print(f"\nResultado: {'todas las filas coinciden' if all_equal else 'hay diferencias'}.")
    print(f"Tabla completa: {output}")
    if not all_equal:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
