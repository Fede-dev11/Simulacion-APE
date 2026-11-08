package simulacion.controller;

import simulacion.model.LinearCongruentialGenerator;
import simulacion.model.RandomValue;
import simulacion.view.ConsoleView;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;

public final class LCGController {
    private final LinearCongruentialGenerator model;
    private final ConsoleView view;

    public LCGController(LinearCongruentialGenerator model, ConsoleView view) {
        this.model = model;
        this.view = view;
    }

    public List<RandomValue> run(long seed, int count, Path outputDir, String name) throws IOException {
        List<RandomValue> sequence = model.generate(seed, count);
        Files.createDirectories(outputDir);
        Path csv = outputDir.resolve(name + ".csv");
        writeCsv(csv, sequence);
        view.show(seed, count, sequence, model.hasFullPeriod(),
                LinearCongruentialGenerator.MODULUS, csv);
        return sequence;
    }

    private static void writeCsv(Path path, List<RandomValue> sequence) throws IOException {
        StringBuilder text = new StringBuilder("n,X_n,U_n\n");
        for (int i = 0; i < sequence.size(); i++) {
            RandomValue value = sequence.get(i);
            text.append(String.format(Locale.US, "%d,%d,%.12f%n", i + 1, value.state(), value.normalized()));
        }
        Files.writeString(path, text);
    }

}
