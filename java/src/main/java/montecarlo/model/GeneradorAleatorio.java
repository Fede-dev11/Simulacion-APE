package montecarlo.model;

public interface GeneradorAleatorio {
    /** Actualiza el estado y devuelve un valor finito en [0, 1). */
    double siguienteDouble();
}
