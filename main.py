from controller.controlador import Controlador
from views.graficas import Vista

datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]

if __name__ == "__main__":
    Controlador(Vista()).ejecutar(datos)