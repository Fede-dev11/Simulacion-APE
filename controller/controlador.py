from modelo.deterministico import Deterministico
from modelo.discreto import Discreto
from modelo.estocastico import Estocastico
from modelo.continuo import Continuo


class Controlador:
    MODELOS = [Deterministico, Discreto, Estocastico, Continuo]

    def __init__(self, vista):
        self.vista = vista

    def estimar_r(self, datos):
        return (datos[-1] / datos[0]) ** (1 / (len(datos) - 1)) - 1

    def _correr(self, p0, r, tiempo, sigma, dt):
        resultados = {}
        for Clase in self.MODELOS:
            modelo = Clase(p0, r, tiempo, sigma, dt)
            resultados[modelo.nombre] = modelo.simular()
        return resultados

    def ejecutar(self, datos, sigma=30, dt=0.1):
        p0, tiempo = datos[0], len(datos) - 1
        r = self.estimar_r(datos)

        self.vista.comparar(self._correr(p0, r, tiempo, sigma, dt),
                            datos, f"Crecimiento (r = {r:.3f})")
        self.vista.comparar(self._correr(p0, -r, tiempo, sigma, dt),
                            None, f"Decrecimiento (r = {-r:.3f})")
        self.vista.mostrar()