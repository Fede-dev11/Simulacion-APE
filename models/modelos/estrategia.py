from abc import ABC, abstractmethod


class EstrategiaModelo(ABC):

    @abstractmethod
    def calcular(self, h, n, tf):
        pass