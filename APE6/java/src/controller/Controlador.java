package controller;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;
import model.Configuracion;
import model.DatoGenerado;
import model.GeneradorLCG;
import model.PruebaEstadistica;
import model.ResultadoPrueba;
import storage.ExportadorCSV;
import views.VistaConsola;

public final class Controlador {
    private final GeneradorLCG generador;
    private final List<PruebaEstadistica> pruebas;
    private final VistaConsola vista;
    private final ExportadorCSV exportador;

    public Controlador(GeneradorLCG generador, List<PruebaEstadistica> pruebas,
            VistaConsola vista, ExportadorCSV exportador) {
        this.generador = generador;
        this.pruebas = pruebas;
        this.vista = vista;
        this.exportador = exportador;
    }

    public List<Path> ejecutar(Configuracion config) throws IOException {
        List<DatoGenerado> datos = generador.generar(config);
        List<Double> secuencia = datos.stream().map(DatoGenerado::valor).toList();
        List<ResultadoPrueba> resultados = pruebas.stream().map(p -> p.evaluar(secuencia)).toList();
        vista.mostrarConfiguracion(config);
        vista.mostrarSecuencia(datos, 20);
        resultados.forEach(vista::mostrarResultado);
        List<Path> rutas = exportador.exportar(config, datos, resultados);
        System.out.println("\nArchivos generados:");
        rutas.forEach(ruta -> System.out.println("- " + ruta));
        return rutas;
    }
}
