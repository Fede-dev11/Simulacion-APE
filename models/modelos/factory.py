from .modelo import ModeloOriginal, ModeloAjustado


def crear_modelo(tipo):

    if tipo == "original":
        return ModeloOriginal()

    if tipo == "ajustado":
        return ModeloAjustado()

    raise ValueError("Modelo no válido")