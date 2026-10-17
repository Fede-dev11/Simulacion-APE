import numpy as np
from modelo.basemodelo import Modelo_Crecimiento


class Estocastico(Modelo_Crecimiento):
    nombre = "Estocástico"

    def simular(self):
        poblacion = [self.p0]
        for _ in range(self.tiempo):
            actual = poblacion[-1]
            ruido = np.random.normal(0, self.sigma)
            nueva = max(0, actual + self.r * actual + ruido)
            poblacion.append(nueva)
        return np.arange(self.tiempo + 1), np.array(poblacion)