import os
from pathlib import Path

_CACHE_MATPLOTLIB = Path(__file__).resolve().parents[1] / ".matplotlib"
_CACHE_MATPLOTLIB.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_CACHE_MATPLOTLIB))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class VistaGraficas:
    def guardar(self, secuencia: list[float], k: int, directorio: Path) -> list[Path]:
        directorio.mkdir(parents=True, exist_ok=True)
        ordenada = sorted(secuencia)
        n = len(ordenada)

        fig, ax = plt.subplots()
        ax.step(ordenada, [i / n for i in range(1, n + 1)], where="post", label="F empírica")
        ax.plot([0, 1], [0, 1], "--", label="F(x) = x")
        ax.set(xlabel="x", ylabel="F(x)", title="Acumulada empírica y uniforme teórica")
        ax.grid(alpha=0.3)
        ax.legend()
        ruta_acumulada = directorio / "acumulada.png"
        fig.savefig(ruta_acumulada, dpi=150, bbox_inches="tight")
        plt.close(fig)

        fig, ax = plt.subplots()
        ax.hist(secuencia, bins=k, range=(0, 1), edgecolor="black")
        ax.axhline(n / k, color="red", linestyle="--", label="Frecuencia esperada")
        ax.set(xlabel="Intervalo", ylabel="Frecuencia", title="Histograma de la secuencia")
        ax.legend()
        ruta_histograma = directorio / "histograma.png"
        fig.savefig(ruta_histograma, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return [ruta_acumulada, ruta_histograma]

