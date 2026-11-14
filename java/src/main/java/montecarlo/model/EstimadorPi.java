package montecarlo.model;

public final class EstimadorPi {
    public ResultadoExperimento estimar(ConfiguracionExperimento configuracion,
                                       GeneradorAleatorio generador) {
        int nc = 0;
        for (int i = 0; i < configuracion.n(); i++) {
            double x = generador.siguienteDouble();
            double y = generador.siguienteDouble();
            if (x * x + y * y <= 1.0) {
                nc++;
            }
        }
        double piEstimado = 4.0 * nc / configuracion.n();
        double errorAbsoluto = Math.abs(piEstimado - Math.PI);
        return new ResultadoExperimento(
                configuracion.n(), configuracion.semilla(), nc, piEstimado, errorAbsoluto, 0.0);
    }
}
