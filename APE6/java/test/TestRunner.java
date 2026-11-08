import java.math.BigInteger;
import java.util.List;
import model.ChiCuadrado;
import model.Configuracion;
import model.DatoGenerado;
import model.GeneradorLCG;
import model.KolmogorovSmirnov;
import model.ResultadoPrueba;

public final class TestRunner {
    private static int pruebas = 0;

    public static void main(String[] args) {
        pruebaSecuenciaManual();
        pruebaValidaciones();
        pruebaFrecuencias();
        pruebaKsManual();
        System.out.println("OK: " + pruebas + " verificaciones Java superadas");
    }

    private static void pruebaSecuenciaManual() {
        Configuracion c = new Configuracion(5, bi(1), bi(5), bi(3), bi(16), 2, 0.05);
        List<BigInteger> estados = new GeneradorLCG().generar(c).stream().map(DatoGenerado::estado).toList();
        comprobar(estados.equals(List.of(bi(8), bi(11), bi(10), bi(5), bi(12))), "secuencia manual");
    }

    private static void pruebaValidaciones() {
        esperarError(() -> new Configuracion(0, bi(1), bi(5), bi(3), bi(16), 2, 0.05).validar());
        esperarError(() -> new Configuracion(5, bi(16), bi(5), bi(3), bi(16), 2, 0.05).validar());
        esperarError(() -> new ChiCuadrado(2, 0.05).evaluar(List.of(0.1, 0.9)));
    }

    @SuppressWarnings("unchecked")
    private static void pruebaFrecuencias() {
        Configuracion c = new Configuracion(100, bi(12345), bi(1664525), bi(1013904223), bi(2).pow(32), 10, 0.05);
        List<Double> secuencia = new GeneradorLCG().generar(c).stream().map(DatoGenerado::valor).toList();
        ResultadoPrueba r = new ChiCuadrado(10, 0.05).evaluar(secuencia);
        int suma = ((List<model.Intervalo>) r.detalles().get("intervalos")).stream().mapToInt(model.Intervalo::observada).sum();
        comprobar(suma == 100, "suma de frecuencias");
    }

    private static void pruebaKsManual() {
        ResultadoPrueba r = new KolmogorovSmirnov(0.05).evaluar(List.of(0.1, 0.4, 0.8));
        comprobarCerca((double) r.detalles().get("d_mas"), 4.0 / 15.0, 1e-15, "D+");
        comprobarCerca((double) r.detalles().get("d_menos"), 2.0 / 15.0, 1e-15, "D-");
    }

    private static BigInteger bi(long valor) { return BigInteger.valueOf(valor); }

    private static void esperarError(Runnable accion) {
        try { accion.run(); } catch (IllegalArgumentException e) { pruebas++; return; }
        throw new AssertionError("Se esperaba IllegalArgumentException");
    }

    private static void comprobar(boolean condicion, String mensaje) {
        pruebas++;
        if (!condicion) throw new AssertionError(mensaje);
    }

    private static void comprobarCerca(double actual, double esperado, double tolerancia, String mensaje) {
        comprobar(Math.abs(actual - esperado) <= tolerancia, mensaje + ": " + actual);
    }
}
