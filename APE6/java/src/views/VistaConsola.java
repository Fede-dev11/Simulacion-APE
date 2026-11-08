package views;

import java.util.List;
import model.Configuracion;
import model.DatoGenerado;
import model.Intervalo;
import model.ResultadoPrueba;

public final class VistaConsola {
    public void mostrarConfiguracion(Configuracion c) {
        System.out.println("\nConfiguración propuesta (no obligatoria en la guía)");
        System.out.printf("N=%d, semilla=%s, a=%s, c=%s, m=%s, k=%d, alfa=%s%n",
                c.n(), c.semilla(), c.a(), c.c(), c.m(), c.k(), c.alfa());
        System.out.println("Las validaciones de rango no garantizan un buen período del LCG.");
    }

    public void mostrarSecuencia(List<DatoGenerado> datos, int limite) {
        System.out.println("\nSecuencia generada");
        if (datos.size() > limite) System.out.printf("Salida abreviada: primeros %d de %d valores.%n", limite, datos.size());
        System.out.println("índice\testado\tvalor");
        datos.stream().limit(limite).forEach(d ->
                System.out.printf("%d\t%s\t%.17g%n", d.indice(), d.estado(), d.valor()));
    }

    @SuppressWarnings("unchecked")
    public void mostrarResultado(ResultadoPrueba resultado) {
        System.out.println("\n" + resultado.nombre());
        if (resultado.nombre().equals("Chi-cuadrado")) {
            System.out.println("intervalo\tobservada\tesperada\tcontribución");
            for (Intervalo fila : (List<Intervalo>) resultado.detalles().get("intervalos")) {
                String cierre = fila.superior() == 1.0 ? "]" : ")";
                System.out.printf("[%.1f, %.1f%s\t%d\t\t%.3f\t\t%.8f%n", fila.inferior(), fila.superior(), cierre,
                        fila.observada(), fila.esperada(), fila.contribucion());
            }
            System.out.printf("χ²=%.12g%n", resultado.estadistico());
            System.out.println("gl=" + resultado.detalles().get("grados_libertad"));
        } else {
            System.out.printf("D+=%.12g%nD-=%.12g%nD=%.12g%n",
                    resultado.detalles().get("d_mas"), resultado.detalles().get("d_menos"), resultado.estadistico());
        }
        System.out.printf("valor p=%.12g%ndecisión: %s%n", resultado.valorP(), resultado.decision());
    }
}
