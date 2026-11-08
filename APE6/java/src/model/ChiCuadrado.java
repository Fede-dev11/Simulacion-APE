package model;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.apache.commons.math3.special.Gamma;

public final class ChiCuadrado implements PruebaEstadistica {
    private final int k;
    private final double alfa;

    public ChiCuadrado(int k, double alfa) {
        this.k = k;
        this.alfa = alfa;
    }

    @Override
    public ResultadoPrueba evaluar(List<Double> secuencia) {
        if (secuencia.isEmpty()) throw new IllegalArgumentException("La secuencia no puede estar vacía");
        if (k <= 1) throw new IllegalArgumentException("k debe ser mayor que 1");
        double esperada = (double) secuencia.size() / k;
        if (esperada < 5.0) throw new IllegalArgumentException("E < 5: aumente N o reduzca k");

        int[] observadas = new int[k];
        for (double valor : secuencia) {
            if (valor < 0.0 || valor >= 1.0) throw new IllegalArgumentException("Los valores deben pertenecer a [0, 1)");
            observadas[Math.min((int) (valor * k), k - 1)]++;
        }

        double estadistico = 0.0;
        List<Intervalo> intervalos = new ArrayList<>(k);
        for (int i = 0; i < k; i++) {
            double contribucion = Math.pow(observadas[i] - esperada, 2) / esperada;
            estadistico += contribucion;
            intervalos.add(new Intervalo((double) i / k, (double) (i + 1) / k,
                    observadas[i], esperada, contribucion));
        }
        int gl = k - 1;
        double valorP = Gamma.regularizedGammaQ(gl / 2.0, estadistico / 2.0);
        Map<String, Object> detalles = new LinkedHashMap<>();
        detalles.put("grados_libertad", gl);
        detalles.put("intervalos", intervalos);
        return new ResultadoPrueba("Chi-cuadrado", estadistico, valorP,
                valorP < alfa ? "se rechaza H0" : "no se rechaza H0", detalles);
    }
}
