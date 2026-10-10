import pandas as pd
from pathlib import Path


def datos_excel(ruta):
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    if ruta.suffix.lower() not in [".xlsx", ".xls"]:
        raise ValueError(
            f"El archivo {ruta} no es un archivo Excel válido."
        )

    return pd.read_excel(ruta)