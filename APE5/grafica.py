import csv
from pathlib import Path

from PIL import Image, ImageDraw


WIDTH, HEIGHT, MARGIN = 1100, 550, 70


def read_values(path: Path) -> list[float]:
    with path.open(encoding="utf-8") as file:
        return [float(row["U_n"]) for row in csv.DictReader(file)]


def draw_series(draw: ImageDraw.ImageDraw, values: list[float], color: tuple[int, int, int]) -> None:
    plot_width, plot_height = WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN
    denominator = max(1, len(values) - 1)
    for index, value in enumerate(values):
        x = MARGIN + round(index * plot_width / denominator)
        y = HEIGHT - MARGIN - round(value * plot_height)
        draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=color)


def main() -> None:
    first = read_values(Path("resultados_python/semilla_12345.csv"))
    second = read_values(Path("resultados_python/semilla_67890.csv"))
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    for division in range(6):
        y = MARGIN + division * (HEIGHT - 2 * MARGIN) // 5
        draw.line((MARGIN, y, WIDTH - MARGIN, y), fill=(220, 220, 220))
        draw.text((30, y - 7), f"{1 - division / 5:.1f}", fill="black")
    draw.line((MARGIN, MARGIN, MARGIN, HEIGHT - MARGIN), fill="black", width=2)
    draw.line((MARGIN, HEIGHT - MARGIN, WIDTH - MARGIN, HEIGHT - MARGIN), fill="black", width=2)
    draw_series(draw, first, (37, 99, 235))
    draw_series(draw, second, (220, 38, 38))
    draw.text((WIDTH // 2 - 100, 20), "Grafica de dispersion - Python", fill="black")
    draw.text((WIDTH // 2 - 75, HEIGHT - 30), "Numero de observacion n", fill="black")
    draw.text((MARGIN, 45), "U(n)", fill="black")
    draw.rectangle((WIDTH - 275, 20, WIDTH - 260, 35), fill=(37, 99, 235))
    draw.text((WIDTH - 255, 20), "Semilla 12345", fill="black")
    draw.rectangle((WIDTH - 150, 20, WIDTH - 135, 35), fill=(220, 38, 38))
    draw.text((WIDTH - 130, 20), "Semilla 67890", fill="black")
    output = Path("graficas/grafica_python.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    print(f"Gráfica conjunta de Python: {output}")


if __name__ == "__main__":
    main()
