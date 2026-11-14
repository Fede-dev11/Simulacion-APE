package montecarlo.controller;

import montecarlo.model.ConfiguracionExperimento;
import montecarlo.model.EstimadorPi;
import montecarlo.model.GeneradorAleatorio;
import montecarlo.model.ResultadoExperimento;
import montecarlo.view.ConsolaView;
import java.util.ArrayList;
import java.util.List;
import java.util.function.LongFunction;

public final class ExperimentoController {
    private final EstimadorPi estimador;
    private final ConsolaView vista;
    private final LongFunction<GeneradorAleatorio> crearGenerador;

    public ExperimentoController(EstimadorPi estimador, ConsolaView vista,
                                 LongFunction<GeneradorAleatorio> crearGenerador) {
        this.estimador = estimador;
        this.vista = vista;
        this.crearGenerador = crearGenerador;
    }

    public List<ResultadoExperimento> ejecutar(List<ConfiguracionExperimento> configuraciones) {
        if (configuraciones.isEmpty()) {
            throw new IllegalArgumentException("Debe existir al menos una configuración.");
        }

        // Una simulación con la muestra mayor calienta la JVM sin consumir
        // los generadores que se usarán en los experimentos medidos.
        var calentamiento = configuraciones.stream()
                .max(java.util.Comparator.comparingInt(ConfiguracionExperimento::n))
                .orElseThrow();
        estimador.estimar(calentamiento, crearGenerador.apply(calentamiento.semilla()));

        var resultados = new ArrayList<ResultadoExperimento>();
        for (var configuracion : configuraciones) {
            var generador = crearGenerador.apply(configuracion.semilla());
            long inicio = System.nanoTime();
            var resultado = estimador.estimar(configuracion, generador);
            long duracion = System.nanoTime() - inicio;
            resultados.add(resultado.conTiempo(duracion / 1_000_000_000.0));
        }
        var salida = List.copyOf(resultados);
        vista.mostrarResultados(salida);
        return salida;
    }
}
