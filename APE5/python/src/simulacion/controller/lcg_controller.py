import csv
from pathlib import Path

from simulacion.model.linear_congruential_generator import LinearCongruentialGenerator
from simulacion.view.console_view import ConsoleView


class LCGController:
    def __init__(self, model: LinearCongruentialGenerator, view: ConsoleView) -> None:
        self.model = model
        self.view = view

    def run(self, seed: int, count: int, output_dir: Path, name: str) -> list[tuple[int, float]]:
        sequence = self.model.generate(seed, count)
        output_dir.mkdir(parents=True, exist_ok=True)
        csv_path = output_dir / f"{name}.csv"
        self._write_csv(csv_path, sequence)
        self.view.show_header(seed, count)
        self.view.show_rows(sequence)
        self.view.show_period(self.model.parameters.modulus, self.model.has_full_period())
        self.view.show_file(csv_path)
        return sequence

    @staticmethod
    def _write_csv(path: Path, sequence: list[tuple[int, float]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(("n", "X_n", "U_n"))
            for index, (state, value) in enumerate(sequence, start=1):
                writer.writerow((index, state, f"{value:.12f}"))

