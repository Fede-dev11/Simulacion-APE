import numpy as np
from modelo.basemodelo import Modelo_Crecimiento


class Continuo(Modelo_Crecimiento):
    nombre = "Continuo (Euler)"

    def simular(self):
        t = np.arange(0, self.tiempo + self.dt, self.dt)
        poblacion = [self.p0]
        for _ in range(len(t) - 1):
            actual = poblacion[-1]
            poblacion.append(actual + self.dt * self.r * actual)
        return t, np.array(poblacion)