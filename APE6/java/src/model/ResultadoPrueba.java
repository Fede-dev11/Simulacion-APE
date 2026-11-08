package model;

import java.util.Map;

public record ResultadoPrueba(
        String nombre, double estadistico, double valorP, String decision, Map<String, Object> detalles) {}
