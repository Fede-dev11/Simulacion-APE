package model;

import java.math.BigInteger;

public record Configuracion(
        int n, BigInteger semilla, BigInteger a, BigInteger c, BigInteger m, int k, double alfa) {

    public static Configuracion propuesta() {
        return new Configuracion(
                10_000,
                BigInteger.valueOf(12_345),
                BigInteger.valueOf(1_664_525),
                BigInteger.valueOf(1_013_904_223),
                BigInteger.valueOf(2).pow(32),
                10,
                0.05);
    }

    public void validar() {
        if (n <= 0) throw new IllegalArgumentException("N debe ser positivo");
        if (m.compareTo(BigInteger.ONE) <= 0) throw new IllegalArgumentException("m debe ser mayor que 1");
        if (k <= 1) throw new IllegalArgumentException("k debe ser mayor que 1");
        validarRango("semilla", semilla);
        validarRango("a", a);
        validarRango("c", c);
        if (!(alfa > 0.0 && alfa < 1.0)) throw new IllegalArgumentException("alfa debe estar entre 0 y 1");
    }

    private void validarRango(String nombre, BigInteger valor) {
        if (valor == null || valor.signum() < 0 || valor.compareTo(m) >= 0) {
            throw new IllegalArgumentException(nombre + " debe cumplir 0 <= " + nombre + " < m");
        }
    }
}
