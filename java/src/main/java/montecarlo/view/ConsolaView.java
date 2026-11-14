package montecarlo.view;

import montecarlo.model.ResultadoExperimento;
import java.util.List;
import java.util.Locale;

public final class ConsolaView {
    public void mostrarResultados(List<ResultadoExperimento> resultados) {
        System.out.println("Estimación de π mediante Monte Carlo — Java, paso 3");
        System.out.println("Una ejecución medida por tamaño, después de un calentamiento.");
        System.out.printf("%10s %10s %10s %16s %16s %16s%n",
                "N", "Semilla", "Nc", "π estimado", "Error absoluto", "Tiempo Java (s)");
        for (var resultado : resultados) {
            System.out.printf(Locale.ROOT, "%10d %10d %10d %16.12f %16.12f %16.9f%n",
                    resultado.n(), resultado.semilla(), resultado.nc(), resultado.piEstimado(),
                    resultado.errorAbsoluto(), resultado.tiempoSegundos());
        }
    }
}
