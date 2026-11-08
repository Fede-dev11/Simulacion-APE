package model;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.MathContext;
import java.util.ArrayList;
import java.util.List;

public final class GeneradorLCG {
    private static final MathContext PRECISION = MathContext.DECIMAL128;

    public List<DatoGenerado> generar(Configuracion config) {
        config.validar();
        BigInteger estado = config.semilla();
        List<DatoGenerado> datos = new ArrayList<>(config.n());
        BigDecimal modulo = new BigDecimal(config.m());
        for (int indice = 1; indice <= config.n(); indice++) {
            estado = config.a().multiply(estado).add(config.c()).mod(config.m());
            double valor = new BigDecimal(estado).divide(modulo, PRECISION).doubleValue();
            datos.add(new DatoGenerado(indice, estado, valor));
        }
        return datos;
    }
}
