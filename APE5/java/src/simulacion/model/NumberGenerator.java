package simulacion.model;

import java.util.List;

// Strategy: the controller depends on this abstraction, not on a specific generator.
public interface NumberGenerator {
    List<RandomValue> generate(long seed, int count);
}
