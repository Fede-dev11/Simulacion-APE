package simulacion.view;

import simulacion.model.RandomValue;
import java.nio.file.Path;
import java.util.List;

public final class ConsoleView {
    public void show(long seed, int count, List<RandomValue> values, boolean fullPeriod,
                     long period, Path csv) {
        System.out.printf("%nLCG: semilla=%d, cantidad=%d%n", seed, count);
        System.out.println(" n |          X(n) |             U(n)");
        System.out.println("---+---------------+-----------------");
        for (int i = 0; i < Math.min(20, values.size()); i++) {
            RandomValue value = values.get(i);
            System.out.printf("%2d | %13d | %.10f%n", i + 1, value.state(), value.normalized());
        }
        System.out.printf("%nLos parámetros %s Hull-Dobell.%n", fullPeriod ? "cumplen" : "no cumplen");
        if (fullPeriod) System.out.printf("Período teórico máximo: %d (= 2^32).%n", period);
        System.out.println("CSV: " + csv);
    }
}
