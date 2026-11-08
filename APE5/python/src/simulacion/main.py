import argparse
from pathlib import Path

from simulacion.controller.lcg_controller import LCGController
from simulacion.model.linear_congruential_generator import LinearCongruentialGenerator
from simulacion.view.console_view import ConsoleView


def main() -> None:
    parser = argparse.ArgumentParser(description="Generador Congruencial Lineal")
    parser.add_argument("--seed", type=int, default=12345, help="semilla inicial")
    parser.add_argument("--second-seed", type=int, default=67890, help="semilla para comparar")
    parser.add_argument("--count", type=int, default=10_000, help="cantidad de valores")
    parser.add_argument("--output", type=Path, default=Path("resultados_python"))
    args = parser.parse_args()

    controller = LCGController(LinearCongruentialGenerator(), ConsoleView())
    controller.run(args.seed, args.count, args.output, f"semilla_{args.seed}")
    controller.run(args.second_seed, args.count, args.output, f"semilla_{args.second_seed}")


if __name__ == "__main__":
    main()
