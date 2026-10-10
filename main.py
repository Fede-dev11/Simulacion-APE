from models.datos.lector_excel import datos_excel
from models.datos.validar_datos import validar_datos

from models.modelos.factory import crear_modelo

from models.calculador_clima import calcular

from models.visualizacion.graficas import (
    grafica_crecimiento_decrecimiento,
    grafica_comparacion
)

def main():

    ruta = "archivos/clima.xlsx"

    df = datos_excel(ruta)

    validar_datos(df)

    print("Datos válidos")

    print(df)

    modelo_original = crear_modelo("original")

    resultados_original = calcular(
        df,
        modelo_original
    )

    print("\n==========================================")
    print("RESULTADOS - MODELO ORIGINAL")
    print("==========================================")

    print(
        resultados_original[
            [
                "Hora",
                "Humedad",
                "Nubosidad",
                "Temperatura",
                "H",
                "N",
                "Tf",
                "Indice",
                "Clasificacion"
            ]
        ].to_string(index=False)
    )

    modelo_ajustado = crear_modelo("ajustado")

    resultados_ajustado = calcular(
        df,
        modelo_ajustado
    )

    print("\n==========================================")
    print("RESULTADOS - MODELO AJUSTADO")
    print("==========================================")

    print(
        resultados_ajustado[
            [
                "Hora",
                "Humedad",
                "Nubosidad",
                "Temperatura",
                "H",
                "N",
                "Tf",
                "Indice",
                "Clasificacion"
            ]
        ].to_string(index=False)
    )

    grafica_comparacion(
        resultados_original,
        resultados_ajustado
    )

    grafica_crecimiento_decrecimiento(
        resultados_original
    )

if __name__ == "__main__":
    main()