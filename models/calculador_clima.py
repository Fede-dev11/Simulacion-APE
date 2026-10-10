def factor_temperatura(temperatura):

    if temperatura <= 10:
        return 1.00
    elif temperatura <= 12:
        return 0.90
    elif temperatura <= 14:
        return 0.80
    elif temperatura <= 16:
        return 0.70
    elif temperatura <= 18:
        return 0.60
    elif temperatura <= 20:
        return 0.50
    elif temperatura <= 22:
        return 0.40
    elif temperatura <= 24:
        return 0.30
    elif temperatura <= 26:
        return 0.20
    else:
        return 0.10


def clasificar_lluvia(indice):

    if indice < 0.40:
        return "Sin lluvia"
    elif indice < 0.60:
        return "Baja posibilidad"
    elif indice < 0.75:
        return "Lluvia probable"
    else:
        return "Lluvia"


def calcular(df, modelo):

    df = df.copy()

    df["H"] = df["Humedad"] / 100
    df["N"] = df["Nubosidad"] / 100

    df["Tf"] = df["Temperatura"].apply(
        factor_temperatura
    )

    df["Indice"] = df.apply(
        lambda fila: modelo.calcular(
            fila["H"],
            fila["N"],
            fila["Tf"]
        ),
        axis=1
    )

    df["Clasificacion"] = df["Indice"].apply(
        clasificar_lluvia
    )

    return df