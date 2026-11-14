package montecarlo.model;

/** Datos inmutables; el estimador entrega tiempo cero hasta que el controlador lo mide. */
public record ResultadoExperimento(int n, long semilla, int nc, double piEstimado,
                                   double errorAbsoluto, double tiempoSegundos) {
    public ResultadoExperimento conTiempo(double segundos) {
        return new ResultadoExperimento(n, semilla, nc, piEstimado, errorAbsoluto, segundos);
    }
}
