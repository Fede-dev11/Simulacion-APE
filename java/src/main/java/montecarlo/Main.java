package montecarlo;

import montecarlo.controller.ExperimentoController;
import montecarlo.model.ConfiguracionExperimento;
import montecarlo.model.EstimadorPi;
import montecarlo.model.GeneradorCongruencial;
import montecarlo.view.ConsolaView;
import java.util.List;

public final class Main {
    public static void main(String[] args) {
        long semilla = 12345L;
        var configuraciones = List.of(
                new ConfiguracionExperimento(1_000, semilla),
                new ConfiguracionExperimento(10_000, semilla),
                new ConfiguracionExperimento(100_000, semilla),
                new ConfiguracionExperimento(1_000_000, semilla));
        var controlador = new ExperimentoController(
                new EstimadorPi(), new ConsolaView(), GeneradorCongruencial::new);
        controlador.ejecutar(configuraciones);
    }
}
