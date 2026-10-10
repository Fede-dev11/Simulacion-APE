from .estrategia import EstrategiaModelo


class ModeloOriginal(EstrategiaModelo):

    def calcular(self, h, n, tf):
        return 0.5 * h + 0.3 * n + 0.2 * tf


class ModeloAjustado(EstrategiaModelo):

    def calcular(self, h, n, tf):
        return 0.45 * h + 0.35 * n + 0.20 * tf