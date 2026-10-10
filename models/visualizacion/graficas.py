import matplotlib.pyplot as plt

def grafica_crecimiento_decrecimiento(resultados):

    resultados = resultados.copy()

    resultados["Cambio"] = resultados["Indice"].diff()

    datos = resultados.iloc[1:].copy()

    horas = datos["Hora"].astype(str)
    cambios = datos["Cambio"]

    etiquetas = []

    for cambio in cambios:
        if cambio > 0:
            etiquetas.append("Crecimiento")
        elif cambio < 0:
            etiquetas.append("Decrecimiento")
        else:
            etiquetas.append("Sin cambio")

    plt.figure(figsize=(10, 5))

    plt.axhline(
        0,
        linestyle="--",
        label="Sin cambio"
    )

    plt.plot(
        horas,
        cambios,
        marker="o",
        label="Δ Índice"
    )

    plt.xlabel("Hora")
    plt.ylabel("Cambio del índice (ΔI)")
    plt.title("Crecimiento y decrecimiento del índice de lluvia")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

    print("\nAnálisis de crecimiento y decrecimiento:")

    for hora, cambio, estado in zip(horas, cambios, etiquetas):

        print(
            f"{hora}: "
            f"ΔI = {cambio:.3f} -> {estado}"
        )


def grafica_comparacion(resultados_original, resultados_ajustado):


    horas = resultados_original["Hora"].astype(str)

    indice_original = resultados_original["Indice"]
    indice_ajustado = resultados_ajustado["Indice"]

    plt.figure(figsize=(10, 5))

    plt.plot(
        horas,
        indice_original,
        marker="o",
        label="Modelo original"
    )

    plt.plot(
        horas,
        indice_ajustado,
        marker="s",
        linestyle="--",
        label="Modelo ajustado"
    )

    # Umbrales del modelo
    plt.axhline(
        0.75,
        linestyle="--",
        label="Umbral: Lluvia"
    )

    plt.axhline(
        0.60,
        linestyle="--",
        label="Umbral: Lluvia probable"
    )

    plt.axhline(
        0.40,
        linestyle="--",
        label="Umbral: Baja posibilidad"
    )

    plt.xlabel("Hora")
    plt.ylabel("Índice")
    plt.title("Comparación: modelo original vs modelo ajustado")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()