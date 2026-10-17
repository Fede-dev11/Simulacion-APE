import matplotlib.pyplot as plt


class Vista:
    def comparar(self, resultados, datos, titulo):
        plt.figure(figsize=(9, 5))
        for nombre, (t, p) in resultados.items():
            plt.plot(t, p, label=nombre)
        if datos is not None:
            plt.scatter(range(len(datos)), datos, color="black",
                        label="Datos reales", zorder=5)
        plt.title(titulo)
        plt.xlabel("Tiempo")
        plt.ylabel("Población")
        plt.legend()
        plt.grid(True)

    def mostrar(self):
        plt.show()