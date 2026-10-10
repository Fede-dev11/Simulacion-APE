import pandas as pd


COLUMNAS_REQUERIDAS = [
    "Hora",
    "Humedad",
    "Nubosidad",
    "Temperatura"
]


def validar_columnas(df):
    faltantes = [
        columna
        for columna in COLUMNAS_REQUERIDAS
        if columna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            f"Faltan las columnas: {faltantes}"
        )


def validar_valores(df):
    for columna in ["Humedad", "Nubosidad", "Temperatura"]:
        if df[columna].isnull().any():
            raise ValueError(
                f"Hay valores vacíos en {columna}."
            )

        if not pd.api.types.is_numeric_dtype(df[columna]):
            raise ValueError(
                f"La columna {columna} debe contener números."
            )

    if not df["Humedad"].between(0, 100).all():
        raise ValueError(
            "La humedad debe estar entre 0 y 100."
        )

    if not df["Nubosidad"].between(0, 100).all():
        raise ValueError(
            "La nubosidad debe estar entre 0 y 100."
        )


def validar_datos(df):
    validar_columnas(df)
    validar_valores(df)