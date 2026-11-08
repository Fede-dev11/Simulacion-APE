import controller.Controlador;
import java.nio.file.Path;
import java.util.List;
import model.ChiCuadrado;
import model.Configuracion;
import model.GeneradorLCG;
import model.KolmogorovSmirnov;
import storage.ExportadorCSV;
import views.VistaConsola;

public final class Main {
    public static void main(String[] args) throws Exception {
        Configuracion config = Configuracion.propuesta();
        Controlador controlador = new Controlador(
                new GeneradorLCG(),
                List.of(new ChiCuadrado(config.k(), config.alfa()), new KolmogorovSmirnov(config.alfa())),
                new VistaConsola(),
                new ExportadorCSV(Path.of("resultados")));
        controlador.ejecutar(config);
    }
}
