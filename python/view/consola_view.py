from model.resultado_experimento import ResultadoExperimento


class ConsolaView:
    def mostrar_resultados(self, resultados: list[ResultadoExperimento]) -> None:
        print("Estimación de π mediante Monte Carlo — Python, paso 2")
        print("Una ejecución medida por tamaño, después de un calentamiento.")
        print(f"{'N':>10} {'Semilla':>10} {'Nc':>10} {'π estimado':>16} "
              f"{'Error absoluto':>16} {'Tiempo Python (s)':>18}")
        for r in resultados:
            print(f"{r.n:10d} {r.semilla:10d} {r.nc:10d} {r.pi_estimado:16.12f} "
                  f"{r.error_absoluto:16.12f} {r.tiempo_segundos:18.9f}")
