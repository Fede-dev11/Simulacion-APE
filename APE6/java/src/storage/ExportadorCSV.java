package storage;

import java.io.BufferedWriter;
import java.io.IOException;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import model.Configuracion;
import model.DatoGenerado;
import model.Intervalo;
import model.ResultadoPrueba;

public final class ExportadorCSV {
    private final Path directorio;

    public ExportadorCSV(Path directorio) {
        this.directorio = directorio;
    }

    public List<Path> exportar(Configuracion config, List<DatoGenerado> datos,
            List<ResultadoPrueba> resultados) throws IOException {
        Files.createDirectories(directorio);
        List<Path> rutas = new ArrayList<>();
        rutas.add(exportarConfiguracion(config));
        rutas.add(exportarSecuencia(datos, config.m()));
        rutas.add(exportarFrecuencias(resultados.get(0)));
        rutas.add(exportarResultados(resultados));
        rutas.add(exportarVersiones());
        return rutas;
    }

    private Path exportarConfiguracion(Configuracion c) throws IOException {
        Path ruta = directorio.resolve("configuracion.csv");
        try (BufferedWriter w = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            w.write("parametro,valor\n");
            w.write("n," + c.n() + "\nsemilla," + c.semilla() + "\na," + c.a() + "\nc," + c.c()
                    + "\nm," + c.m() + "\nk," + c.k() + "\nalfa," + c.alfa() + "\n");
        }
        return ruta;
    }

    private Path exportarSecuencia(List<DatoGenerado> datos, BigInteger m) throws IOException {
        Path ruta = directorio.resolve("secuencia.csv");
        try (BufferedWriter w = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            w.write("indice,estado,valor_normalizado\n");
            for (DatoGenerado d : datos) {
                // La fracción decimal se deriva del mismo estado entero exportado.
                w.write(d.indice() + "," + d.estado() + "," + Double.toString(d.valor()) + "\n");
            }
        }
        return ruta;
    }

    @SuppressWarnings("unchecked")
    private Path exportarFrecuencias(ResultadoPrueba resultado) throws IOException {
        Path ruta = directorio.resolve("frecuencias_chi_cuadrado.csv");
        try (BufferedWriter w = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            w.write("inferior,superior,observada,esperada,contribucion\n");
            for (Intervalo f : (List<Intervalo>) resultado.detalles().get("intervalos")) {
                w.write(f.inferior() + "," + f.superior() + "," + f.observada() + ","
                        + f.esperada() + "," + f.contribucion() + "\n");
            }
        }
        return ruta;
    }

    private Path exportarResultados(List<ResultadoPrueba> resultados) throws IOException {
        Path ruta = directorio.resolve("resultados_pruebas.csv");
        try (BufferedWriter w = Files.newBufferedWriter(ruta, StandardCharsets.UTF_8)) {
            w.write("prueba,estadistico,valor_p,decision,d_mas,d_menos,gl\n");
            for (ResultadoPrueba r : resultados) {
                w.write(r.nombre() + "," + r.estadistico() + "," + r.valorP() + "," + r.decision() + ","
                        + r.detalles().getOrDefault("d_mas", "") + ","
                        + r.detalles().getOrDefault("d_menos", "") + ","
                        + r.detalles().getOrDefault("grados_libertad", "") + "\n");
            }
        }
        return ruta;
    }

    private Path exportarVersiones() throws IOException {
        Path ruta = directorio.resolve("versiones.txt");
        Files.writeString(ruta,
                "Java " + System.getProperty("java.version") + "\nApache Commons Math 3.6.1\n"
                + "Chi-cuadrado: Gamma.regularizedGammaQ(gl/2, estadistico/2)\n"
                + "KS bilateral asintótico: 1 - KolmogorovSmirnovTest.ksSum(sqrt(N)*D)\n",
                StandardCharsets.UTF_8);
        return ruta;
    }
}
