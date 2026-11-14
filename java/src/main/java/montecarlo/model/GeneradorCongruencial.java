package montecarlo.model;

public final class GeneradorCongruencial implements GeneradorAleatorio {
    private static final long MODULO = 4_294_967_296L;
    private static final long MULTIPLICADOR = 1_664_525L;
    private static final long INCREMENTO = 1_013_904_223L;
    private long estado;

    public GeneradorCongruencial(long semilla) {
        if (semilla < 0 || semilla >= MODULO) {
            throw new IllegalArgumentException("La semilla debe cumplir 0 <= semilla < 2^32.");
        }
        estado = semilla;
    }

    @Override
    public double siguienteDouble() {
        estado = (MULTIPLICADOR * estado + INCREMENTO) % MODULO;
        return estado / (double) MODULO;
    }
}
