class Modelo_Crecimiento:
    nombre =""

    def __init__(self, p0, r, tiempo, sigma=0, dt=0.1):
        self.p0= p0
        self.r = r
        self.tiempo = tiempo
        self.sigma = sigma
        self.dt = dt

    def simular(self):
        raise NotImplementedError