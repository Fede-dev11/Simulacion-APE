import numpy as np
from modelo.basemodelo import Modelo_Crecimiento


class Discreto(Modelo_Crecimiento):
    nombre = "Discreto"

    def simular(self):
        poblacion = [self.p0]
        for _ in range(self.tiempo):
            actual = poblacion[-1]
            poblacion.append(actual + self.r * actual)
        return np.arange(self.tiempo + 1), np.array(poblacion)