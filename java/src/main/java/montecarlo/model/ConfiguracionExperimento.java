package montecarlo.model;

/** Parámetros inmutables de una simulación. */
public record ConfiguracionExperimento(int n, long semilla) {
    public ConfiguracionExperimento {
        if (n <= 0) {
            throw new IllegalArgumentException("N debe ser positivo.");
        }
        if (semilla < 0 || semilla >= 4_294_967_296L) {
            throw new IllegalArgumentException("La semilla debe cumplir 0 <= semilla < 2^32.");
        }
    }
}
