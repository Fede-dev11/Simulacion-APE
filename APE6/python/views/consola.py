from model.configuracion import Configuracion
from model.generador_lcg import DatoGenerado
from model.resultado_prueba import ResultadoPrueba


class VistaConsola:
    def mostrar_configuracion(self, config: Configuracion) -> None:
        print("\nConfiguración propuesta (no obligatoria en la guía)")
        print(
            f"N={config.n}, semilla={config.semilla}, a={config.a}, "
            f"c={config.c}, m={config.m}, k={config.k}, alfa={config.alfa}"
        )
        print("Las validaciones de rango no garantizan un buen período del LCG.")

    def mostrar_secuencia(self, datos: list[DatoGenerado], limite: int = 20) -> None:
        print("\nSecuencia generada")
        if len(datos) > limite:
            print(f"Salida abreviada: se muestran los primeros {limite} de {len(datos)} valores.")
        print("índice\testado\tvalor")
        for dato in datos[:limite]:
            print(f"{dato.indice}\t{dato.estado}\t{dato.valor:.17g}")

    def mostrar_resultado(self, resultado: ResultadoPrueba) -> None:
        print(f"\n{resultado.nombre}")
        if resultado.nombre == "Chi-cuadrado":
            print("intervalo\tobservada\tesperada\tcontribución")
            for fila in resultado.detalles["intervalos"]:
                cierre = "]" if fila["superior"] == 1 else ")"
                print(
                    f"[{fila['inferior']:.1f}, {fila['superior']:.1f}{cierre}\t"
                    f"{fila['observada']}\t\t{fila['esperada']:.3f}\t\t"
                    f"{fila['contribucion']:.8f}"
                )
            print(f"χ²={resultado.estadistico:.12g}")
            print(f"gl={resultado.detalles['grados_libertad']}")
        else:
            print(f"D+={resultado.detalles['d_mas']:.12g}")
            print(f"D-={resultado.detalles['d_menos']:.12g}")
            print(f"D={resultado.estadistico:.12g}")
        print(f"valor p={resultado.valor_p:.12g}")
        print(f"decisión: {resultado.decision}")

    def mostrar_archivos(self, archivos: list[str]) -> None:
        print("\nArchivos generados:")
        for archivo in archivos:
            print(f"- {archivo}")

