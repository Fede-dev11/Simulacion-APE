package simulacion.model;

import java.util.ArrayList;
import java.util.List;

public final class LinearCongruentialGenerator implements NumberGenerator {
    public static final long MULTIPLIER = 1_664_525L;
    public static final long INCREMENT = 1_013_904_223L;
    public static final long MODULUS = 1L << 32;
    private static final long MASK = MODULUS - 1;

    @Override
    public List<RandomValue> generate(long seed, int count) {
        if (count < 0) throw new IllegalArgumentException("La cantidad no puede ser negativa");
        List<RandomValue> sequence = new ArrayList<>(count);
        long state = seed & MASK;
        for (int i = 0; i < count; i++) {
            // The mask is equivalent to mod 2^32 and avoids signed-int problems.
            state = (MULTIPLIER * state + INCREMENT) & MASK;
            sequence.add(new RandomValue(state, (double) state / MODULUS));
        }
        return sequence;
    }

    public boolean hasFullPeriod() {
        return INCREMENT % 2 == 1 && (MULTIPLIER - 1) % 4 == 0;
    }
}
