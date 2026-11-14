# APE 7 — Estimación de π mediante Monte Carlo

Práctica de Simulación con implementaciones equivalentes en Java y Python. Se generan puntos pseudoaleatorios para aproximar π y comparar estimación, error absoluto y tiempo de ejecución.

## Objetivos y alcance

- Ejecutar experimentos con 1 000, 10 000, 100 000 y 1 000 000 de puntos.
- Reproducir la misma secuencia en ambos lenguajes con los mismos parámetros.
- Mostrar una tabla por lenguaje en la terminal.
- Analizar precisión y rendimiento sin suponer que el error disminuye en cada muestra.

La versión actual no exporta CSV ni genera registros TXT. Tampoco requiere bibliotecas externas, base de datos o interfaz gráfica.

## Requisitos

| Herramienta | Requisito |
|---|---|
| Java | JDK 17 o posterior; deben estar disponibles `java` y `javac` |
| Python | Python 3.10 o posterior, mediante `python3` |
| Script conjunto | Bash 4 o posterior y `find`, como en el entorno Linux usado |
| IDE | Opcional; se incluye configuración de fuentes para VS Code |

No se necesita instalar NumPy, Pandas, Matplotlib, Maven ni Gradle.

## Ejecución rápida

Abre una terminal en la carpeta raíz `APE7`:

```bash
./ejecutar_ambos.sh
```

Si el archivo no tiene permiso de ejecución:

```bash
bash ejecutar_ambos.sh
```

El script comprueba las herramientas, compila todas las fuentes Java en `java/out`, ejecuta Java y después Python. Se detiene si encuentra un error. También puede invocarse mediante su ruta desde otra carpeta: resuelve la ubicación del proyecto automáticamente.

### Ejecutar Java por separado

Desde la raíz:

```bash
mkdir -p java/out
javac -encoding UTF-8 -d java/out $(find java/src/main/java -name '*.java')
java -cp java/out montecarlo.Main
```

`java/out` contiene archivos `.class` generados. Se edita el código de `src`, no esos archivos compilados. Después de modificar Java hay que volver a compilar; el script conjunto lo hace en cada ejecución.

### Ejecutar Python por separado

```bash
python3 python/main.py
```

## Modelo matemático

Se generan coordenadas en el cuadrado `[0,1) × [0,1)` y se cuenta un punto como interior del cuarto de círculo cuando:

```text
x² + y² ≤ 1
π estimado = 4.0 × Nc / N
Error absoluto = |π estimado − π de referencia|
```

`N` es el total de puntos y `Nc` el número de interiores. La razón de áreas es π/4. Java utiliza `Math.PI` y Python `math.pi` como referencia.

## Estructura del código

```text
APE7/
├── ejecutar_ambos.sh
├── README.md
├── PROMPT_ANALISIS_DECISIONES.md
├── GUION_EXPOSICION.md
├── java/
│   └── src/main/java/montecarlo/
│       ├── Main.java
│       ├── model/
│       │   ├── ConfiguracionExperimento.java
│       │   ├── GeneradorAleatorio.java
│       │   ├── GeneradorCongruencial.java
│       │   ├── EstimadorPi.java
│       │   └── ResultadoExperimento.java
│       ├── controller/ExperimentoController.java
│       └── view/ConsolaView.java
└── python/
    ├── main.py
    ├── model/
    │   ├── configuracion_experimento.py
    │   ├── generador_aleatorio.py
    │   ├── generador_congruencial.py
    │   ├── estimador_pi.py
    │   └── resultado_experimento.py
    ├── controller/experimento_controller.py
    └── view/consola_view.py
```


### Responsabilidades MVC

| Componente | Responsabilidad |
|---|---|
| `Main` / `main.py` | Definir muestras y semilla, construir componentes e iniciar el controlador |
| Configuración | Mantener N y semilla y validar sus restricciones |
| Contrato del generador | Declarar la operación que entrega el siguiente valor en `[0,1)` |
| Generador congruencial | Mantener y actualizar el estado pseudoaleatorio |
| Estimador | Generar puntos, contar interiores y calcular π y error |
| Resultado | Conservar los datos de cada experimento de forma inmutable |
| Controlador | Crear generadores, calentar, medir, reunir resultados y solicitar su presentación |
| Vista | Mostrar la tabla sin realizar el cálculo de la simulación |

## Decisiones de implementación

| Decisión | Motivo y efecto |
|---|---|
| Cuarto de círculo en cuadrado unidad | Simplifica las coordenadas y conserva la relación π/4 |
| Generador común implementado en ambos lenguajes | Evita depender de generadores predeterminados que podrían diferir |
| Semilla inicial 12345 | Permite reproducir los experimentos |
| Reinicio por cada N | Hace que cada muestra comience igual y no dependa de ejecuciones anteriores |
| Primero x y luego y | Conserva la misma asignación de números a coordenadas |
| Estado entero y módulo explícito | Mantiene la misma recurrencia entre lenguajes |
| `double` / `float` | Permite calcular coordenadas y proporciones con decimales |
| Configuración y resultado inmutables | Evita modificar parámetros o resultados una vez construidos |
| Puntos procesados individualmente | Evita almacenar hasta un millón de coordenadas |
| Tablas en consola | Permite revisar los resultados sin archivos de exportación |

### Generador reproducible

```text
estado siguiente = (1664525 × estado actual + 1013904223) mod 2^32
valor = estado siguiente / 4294967296.0
```

Se actualiza el estado antes de devolver el valor. Java usa `long` para que el producto intermedio quepa; Python utiliza enteros de precisión arbitraria. Compartir únicamente la semilla no garantiza reproducibilidad si el algoritmo es distinto.

El generador es una elección didáctica para esta práctica. Reproducir la secuencia no demuestra independencia ni calidad estadística perfecta. No se utiliza para criptografía.

### Validaciones y representación

N debe ser positivo y la semilla un entero en `[0, 2^32)`. En Python se rechazan también valores de tipo incorrecto, incluidos booleanos. La estimación se calcula con `4.0` para evitar división entera. La vista redondea los decimales mostrados; los cálculos conservan su precisión de coma flotante.

## Flujo de ejecución y medición

1. El punto de entrada crea cuatro configuraciones con la misma semilla.
2. El controlador realiza un calentamiento con el mayor N y un generador independiente.
3. Para cada tamaño crea otro generador con la semilla inicial.
4. Inicia el reloj y solicita la simulación.
5. El estimador genera cada par, evalúa la condición y calcula π y error.
6. El controlador detiene el reloj y construye el resultado con la duración.
7. La vista presenta los cuatro resultados.

Java mide con `System.nanoTime()` y convierte la diferencia a segundos. Python utiliza `time.perf_counter()`. El intervalo incluye generación, conteo y cálculo; excluye creación del generador, compilación, calentamiento e impresión.

La simulación tiene complejidad temporal O(N) y memoria adicional O(1). El controlador conserva una lista pequeña con un resultado por tamaño.

## Interpretación de la tabla

| Columna | Significado |
|---|---|
| N | Número total de puntos |
| Semilla | Estado inicial del generador |
| Nc | Puntos que cumplen la condición del círculo |
| π estimado | Aproximación mediante `4Nc/N` |
| Error absoluto | Distancia al valor de referencia de π |
| Tiempo | Duración de la simulación en segundos |

Con la semilla 12345, ambas implementaciones producen estos resultados reproducibles:

| N | Nc | π estimado | Error absoluto aproximado |
|---:|---:|---:|---:|
| 1 000 | 793 | 3.172000 | 0.030407346410 |
| 10 000 | 7 897 | 3.158800 | 0.017207346410 |
| 100 000 | 78 527 | 3.141080 | 0.000512653590 |
| 1 000 000 | 785 664 | 3.142656 | 0.001063346410 |

La mejor aproximación de estas muestras corresponde a 100 000 puntos. Los tiempos no son constantes: deben consultarse en cada ejecución. El informe contiene tiempos de una ejecución concreta, no promedios.

## Limitaciones y comprobaciones

- Más puntos no garantizan una reducción del error absoluto en cada caso.
- La relación teórica `1/√N` describe el error estándar bajo supuestos de independencia y varianza finita.
- Las muestras comparten un prefijo porque reinician la misma semilla; no son experimentos independientes entre tamaños.
- Un calentamiento y una medición por tamaño no eliminan la variabilidad del rendimiento.
- El resultado compara estas implementaciones; Python no utiliza vectorización ni se ejecuta en paralelo.
- La misma semilla reproduce la estimación, pero no el tiempo.

Se verificaron ejecución, conteos coincidentes, fórmulas y validaciones. Para una comprobación manual, ejecuta el script y compara las columnas N, semilla, Nc, π y error de ambas tablas. Para ampliar el estudio, usa múltiples semillas y repeticiones, reportando mediana y dispersión de los tiempos.



