import numpy as np
from modelo.basemodelo import Modelo_Crecimiento


class Deterministico(Modelo_Crecimiento):
    nombre = "Determinístico"

    def simular(self):
        t = np.linspace(0, self.tiempo, self.tiempo * 10 + 1)
        return t, self.p0 * np.exp(self.r * t)