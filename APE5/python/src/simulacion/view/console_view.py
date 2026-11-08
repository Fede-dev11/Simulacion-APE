from pathlib import Path


class ConsoleView:
    def show_header(self, seed: int, count: int) -> None:
        print(f"\nLCG: semilla={seed}, cantidad={count}")
        print(" n |          X(n) |             U(n)")
        print("---+---------------+-----------------")

    def show_rows(self, sequence: list[tuple[int, float]], limit: int = 20) -> None:
        for index, (state, value) in enumerate(sequence[:limit], start=1):
            print(f"{index:2d} | {state:13d} | {value:.10f}")

    def show_period(self, period: int, full_period: bool) -> None:
        status = "cumplen" if full_period else "no cumplen"
        print(f"\nLos parámetros {status} Hull-Dobell.")
        if full_period:
            print(f"Período teórico máximo: {period} (= 2^32).")

    def show_file(self, csv_path: Path) -> None:
        print(f"CSV: {csv_path}")
