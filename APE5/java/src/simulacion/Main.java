package simulacion;

import simulacion.controller.LCGController;
import simulacion.model.LinearCongruentialGenerator;
import simulacion.model.RandomValue;
import simulacion.view.ConsoleView;
import simulacion.view.Grafica;

import java.nio.file.Path;
import java.util.List;

public final class Main {
    private Main() { }

    public static void main(String[] args) throws Exception {
        long seed = args.length > 0 ? Long.parseLong(args[0]) : 12345L;
        long secondSeed = args.length > 1 ? Long.parseLong(args[1]) : 67890L;
        int count = args.length > 2 ? Integer.parseInt(args[2]) : 10_000;
        Path output = Path.of(args.length > 3 ? args[3] : "resultados_java");

        LCGController controller = new LCGController(
                new LinearCongruentialGenerator(), new ConsoleView());
        List<RandomValue> first = controller.run(seed, count, output, "semilla_" + seed);
        List<RandomValue> second = controller.run(secondSeed, count, output, "semilla_" + secondSeed);
        Grafica grafica = new Grafica();
        grafica.save(first, second, Path.of("graficas/grafica_java.png"));
    }
}
