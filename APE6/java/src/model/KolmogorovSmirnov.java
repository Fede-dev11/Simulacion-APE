package model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.apache.commons.math3.stat.inference.KolmogorovSmirnovTest;

public final class KolmogorovSmirnov implements PruebaEstadistica {
    private final double alfa;

    public KolmogorovSmirnov(double alfa) {
        this.alfa = alfa;
    }

    @Override
    public ResultadoPrueba evaluar(List<Double> secuencia) {
        if (secuencia.isEmpty()) throw new IllegalArgumentException("La secuencia no puede estar vacía");
        List<Double> ordenada = new ArrayList<>(secuencia);
        Collections.sort(ordenada);
        int n = ordenada.size();
        double dMas = 0.0;
        double dMenos = 0.0;
        for (int indice = 1; indice <= n; indice++) {
            double valor = ordenada.get(indice - 1);
            if (valor < 0.0 || valor > 1.0) throw new IllegalArgumentException("Los valores deben pertenecer a [0, 1]");
            dMas = Math.max(dMas, (double) indice / n - valor);
            dMenos = Math.max(dMenos, valor - (double) (indice - 1) / n);
        }
        double estadistico = Math.max(dMas, dMenos);
        KolmogorovSmirnovTest distribucion = new KolmogorovSmirnovTest();
        double cdf = distribucion.ksSum(Math.sqrt(n) * estadistico, 1e-20, 100_000);
        double valorP = 1.0 - cdf;
        Map<String, Object> detalles = new LinkedHashMap<>();
        detalles.put("d_mas", dMas);
        detalles.put("d_menos", dMenos);
        detalles.put("n", n);
        return new ResultadoPrueba("Kolmogorov-Smirnov", estadistico, valorP,
                valorP < alfa ? "se rechaza H0" : "no se rechaza H0", detalles);
    }
}
