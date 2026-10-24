# Simulación SIR en Java con visualización en NetLogo

Aplicación académica de consola que calcula una simulación discreta y estocástica SIR en Java, exporta una serie temporal CSV y permite reproducirla con agentes de colores y una gráfica en NetLogo.

**Java calcula; NetLogo visualiza.** La comunicación se realiza mediante un archivo, después de terminar la simulación Java. No hay conexión en tiempo real.


## Funcionalidades

- Población cerrada con estados susceptible, infectado y recuperado.
- Parámetros editables en Java y validación antes de simular.
- Infectados iniciales elegidos al azar sin duplicados.
- Un intento de contacto por infectado y paso, contagios y recuperaciones probabilísticos.
- Actualización simultánea de estados y comprobación de invariantes.
- Reproducibilidad mediante semilla explícita.
- Registro desde t=0 hasta T inclusive; T actualizaciones y T+1 observaciones.
- Exportación de un único CSV predeterminado: `resultados/resultados_java.csv`.
- Resumen por consola: parámetros, estado final, pico y su primer instante, duración y ruta.
- Vista NetLogo con círculos de colores, gráfica conjunta S/I/R, monitores, carga, reproducción/pausa y velocidad.

## Tecnologías y dependencias

| Tecnología | Uso | Requisito |
| --- | --- | --- |
| Java | Motor, modelo, configuración y escritura CSV | JDK 17 o superior para compilar; JVM 17 o superior para ejecutar el JAR |
| Maven | Compilación y empaquetado | Maven 3.9.x recomendado; verificado con 3.9.11 |
| Biblioteca estándar Java | Random, listas, archivos, UTF-8 y medición de tiempo | Incluida con Java; ninguna dependencia externa de ejecución para la aplicación |
| NetLogo | Interfaz, agentes representativos y gráfica | Modelo preparado para NetLogo 7.0.4 de escritorio |
| Extensión CSV de NetLogo | Importar el archivo generado por Java | Declarada mediante `extensions [csv]`; incluida en la instalación utilizada |

Los plugins Maven tienen versiones concretas: Clean 3.5.0, Resources 3.3.1, Compiler 3.15.0, Surefire 3.5.6 y JAR 3.5.1. La compilación usa `maven.compiler.release=17` y UTF-8. NetLogo se ejecuta por separado y no se añade como dependencia Maven del motor.

## Ejecutar en Linux

### 1. Comprobar el entorno

```bash
java -version
javac -version
mvn --version
```

Instala un JDK 17 o superior y Maven si no están disponibles. NetLogo debe estar instalado para utilizar la interfaz; no es necesario para ejecutar Java y obtener el CSV. La primera compilación Maven necesita acceso a sus repositorios, salvo que las dependencias y plugins ya estén almacenados en la caché local.

En este equipo `mvn` no está en PATH, pero existe esta distribución local:

```bash
/home/feder/.m2/wrapper/dists/apache-maven-3.9.11-bin/86516310/apache-maven-3.9.11/bin/mvn --version
```

Puedes usar la ruta completa en lugar de `mvn` en los comandos siguientes. Esa ruta pertenece a este equipo y no es un requisito portable del proyecto.

### 2. Compilar y generar el JAR

Desde la raíz del proyecto:

```bash
cd "/home/feder/Escritorio/UNL/QUINTO/Simulacion/Practica 4"
mvn clean package
```

En otro equipo, sustituye la ruta del `cd` por la ubicación donde guardaste el proyecto. El resultado es `target/sir-simulacion.jar`.

### 3. Ejecutar la simulación Java

```bash
java -jar target/sir-simulacion.jar
```

Se crea la carpeta `resultados` si no existe y se sobrescribe `resultados_java.csv`. El programa termina por sí solo, sin solicitar entrada interactiva. Si cambiaste el código o las constantes, recompila antes de ejecutar el JAR.

Otros argumentos disponibles:

```bash
java -jar target/sir-simulacion.jar --help
java -jar target/sir-simulacion.jar --salida resultados/resultados_java.csv
```

`--help` termina correctamente sin simular ni escribir archivos. `--salida` permite indicar otro destino, aunque el flujo normal del proyecto utiliza únicamente el nombre predeterminado. `--config` ya no existe. Los argumentos inválidos y los fallos de escritura se informan por stderr con código de salida distinto de cero; no se muestra un resumen de éxito si la exportación falla.

También se puede ejecutar `sir.Main` desde un IDE. Configura como directorio de trabajo la raíz del proyecto para mantener la ruta esperada del CSV.

### 4. Abrir NetLogo

Desde Archivo / Abrir de NetLogo, selecciona `netlogo/SIR_Java.nlogox`. Conserva `lector_csv.nls` y `vista_sir.nls` en esa misma carpeta; no los abras como modelos independientes. Si ya tenías el modelo abierto, ciérralo y vuelve a abrirlo para cargar la versión actualizada desde disco.

En este equipo también puedes iniciar NetLogo desde Linux con:

```bash
JAVA_HOME=/opt/netlogo/lib/runtime /opt/netlogo/netlogo-gui.sh "$PWD/netlogo/SIR_Java.nlogox"
```

La ruta corresponde a la instalación local; en otro equipo utiliza su lanzador o menú de aplicaciones. La interfaz gráfica requiere una sesión de escritorio disponible.

En el modelo:

1. Pulsa **Cargar CSV**.
2. Pulsa **Reproducir / Pausar** para comenzar y vuelve a pulsarlo para pausar.
3. Ajusta **velocidad** entre 1 y 20 pasos por segundo como ritmo objetivo.
4. Para volver a t=0, pausa y pulsa **Cargar CSV**.

Los únicos botones son Cargar CSV y Reproducir / Pausar. Cargar CSV también limpia la gráfica y devuelve la vista al inicio. Verde significa susceptible; rojo, infectado; azul, recuperado. Las tres curvas comparten gráfica y los monitores muestran los conteos de la fila actual. Al terminar el archivo, la reproducción se detiene.

La velocidad efectiva depende del equipo y del control general de velocidad de NetLogo. El deslizador modifica únicamente el ritmo de presentación; no cambia beta, gamma, los ticks del CSV ni los resultados calculados por Java.

## Parámetros y escenarios

Se editan en [ParametrosSimulacion.java](src/main/java/sir/model/ParametrosSimulacion.java). Valores actuales al documentar el proyecto:

```java
public static final int POBLACION = 100;
public static final int INFECTADOS_INICIALES = 8;
public static final double BETA = 0.30;
public static final double GAMMA = 0.10;
public static final int TIEMPO_SIMULACION = 100;
public static final long SEMILLA = 42L;
```

| Constante | Significado | Validación |
| --- | --- | --- |
| POBLACION | Número total de individuos | Positivo, representable como int |
| INFECTADOS_INICIALES | Personas infectadas al comenzar | Entre 0 y N |
| BETA | Probabilidad de contagio por contacto con susceptible | Finita y en [0,1] |
| GAMMA | Probabilidad de recuperación por infectado y paso | Finita y en [0,1] |
| TIEMPO_SIMULACION | Cantidad de actualizaciones | Entre 0 y 2147483646; T+1 debe caber en int |
| SEMILLA | Inicializa el generador pseudoaleatorio | Cualquier long, incluidos negativos |

Los recuperados iniciales son cero; los susceptibles son N-I0. El paso temporal vale una unidad abstracta y cada infectado realiza un intento de contacto por paso. Estas dos reglas no son parámetros adicionales. No se impone un máximo arbitrario de población, pero la memoria y la legibilidad de la vista limitan el tamaño práctico.

Escenarios sugeridos, manteniendo N=100, I0=8, T=100 y semilla=42:

| Escenario | BETA | GAMMA | Qué permite estudiar |
| --- | --- | --- | --- |
| Menor transmisión y mayor recuperación | 0.10 | 0.30 | Tendencia a una propagación más limitada |
| Referencia actual | 0.30 | 0.10 | Punto de comparación |
| Mayor transmisión y recuperación más lenta | 0.60 | 0.05 | Tendencia a una propagación más sostenida |

Son propuestas de experimentación, no conclusiones garantizadas ni escenarios ejecutados automáticamente. Para aislar el efecto de un parámetro, cambia solo ese parámetro y conserva el resto. Para estudiar variabilidad, repite manualmente con varias semillas. El uso de una misma semilla no garantiza las mismas llamadas aleatorias cuando cambian las condiciones del modelo.

Casos de control útiles: BETA=0 impide nuevos contagios; GAMMA=0 impide nuevas recuperaciones; I0=0 mantiene una población susceptible constante; T=0 produce solo la observación inicial.

Después de cada cambio: recompila, ejecuta Java y pulsa Cargar CSV en NetLogo. El historial cargado en NetLogo no se actualiza automáticamente cuando cambia el archivo en disco.

## Reglas del algoritmo

1. Crear individuos con identificadores 0 a N-1, inicialmente susceptibles.
2. Barajar un arreglo auxiliar de identificadores mediante Fisher-Yates completo y marcar los primeros I0 como infectados. La población conserva su orden original.
3. Contar y registrar el estado inicial.
4. En cada paso, copiar la lista actual en la lista siguiente.
5. Recorrer únicamente los infectados del estado actual, en orden de identificador.
6. Seleccionar un identificador entre los N. El contacto propio o con I/R consume el intento sin repetirlo.
7. Si el contacto era susceptible en el estado actual, sortear un uniforme y aplicar directamente `u < beta`.
8. Sortear siempre la recuperación del infectado y aplicar directamente `u < gamma`.
9. Aplicar la población siguiente, verificar invariantes y registrar el nuevo instante.
10. Terminar después de registrar T, sin producir una actualización adicional.

Todas las consultas se hacen sobre `actual` y las escrituras sobre `siguiente`. Un recién contagiado no transmite ni se recupera durante el mismo paso. Un infectado que se recupera al final sí pudo contagiar antes. Diferentes infectados pueden elegir al mismo susceptible; se consume cada sorteo, pero el individuo se cuenta una sola vez.

BETA y GAMMA se interpretan como probabilidades discretas conforme al pseudocódigo. No se convierten mediante exponenciales ni se resuelven ecuaciones diferenciales. Si desaparecen los infectados, el historial continúa hasta T con estados constantes.

Se usa un `Random` nuevo por ejecución y se comparte entre inicialización y evolución. Con iguales parámetros y semilla, dos ejecuciones nuevas producen el mismo historial y los mismos bytes CSV. La duración de cálculo puede variar.

## Arquitectura y decisiones de diseño

Separación por capas **inspirada en MVC**. El modelo y el motor están en Java, el controlador coordina simulación y exportación, y NetLogo presenta la vista. Es una integración por archivo entre dos programas; no existe un MVC con eventos de interfaz conectados al motor en tiempo real.

| Decisión o técnica aplicada | Motivo y efecto |
| --- | --- |
| Modelo separado del motor | Los datos y sus validaciones no dependen de los sorteos ni de archivos |
| Controlador y exportador en controller | Simplifica los paquetes conservando la coordinación y la escritura en clases distintas |
| Inyección por constructor | Main entrega el generador al motor y el motor/exportador al controlador; las dependencias quedan explícitas |
| Interfaz GeneradorAleatorio | El motor conoce las operaciones necesarias, sin depender directamente de java.util.Random |
| Adaptador GeneradorJava | Traduce el contrato propio a nextInt y nextDouble de Random |
| Enum EstadoSalud | Limita los estados válidos y evita textos inconsistentes |
| Records y copias defensivas | Protegen parámetros, individuos, registros e historial frente a cambios externos |
| Doble estado actual/siguiente | Evita que el orden del recorrido haga actuar a recién infectados dentro del mismo paso |
| CSV agregado | Mantiene una comunicación sencilla y verificable entre Java y NetLogo |
| Constantes Java | Centraliza los escenarios en una clase, a cambio de tener que recompilar |
| Una gráfica con tres series | Permite comparar S, I y R con el mismo tiempo y escala |
| Dos botones de vista | Reduce controles: Cargar CSV también sirve para volver al inicio |


La inicialización cuesta O(N). La simulación cuesta O(N·T) para T positivo, más O(N) inicial, y utiliza O(N+T) de memoria para población, estado siguiente e historial agregado. No conserva una población completa por instante. La vista ordena representantes y puede tener un coste diferente al del motor.

## Estructura y responsabilidades

```text
.
├── pom.xml
├── .gitignore
├── README.md
├── docs/
│   ├── EXPLICACION_Y_EXPOSICION.docx
│   └── PROMPTS_DEL_PROYECTO.docx
├── src/main/java/sir/
│   ├── Main.java
│   ├── model/
│   │   ├── EstadoSalud.java
│   │   ├── Individuo.java
│   │   ├── ParametrosSimulacion.java
│   │   ├── Poblacion.java
│   │   ├── RegistroPaso.java
│   │   └── ResultadoSimulacion.java
│   ├── simulation/MotorSimulacionSIR.java
│   ├── random/
│   │   ├── GeneradorAleatorio.java
│   │   └── GeneradorJava.java
│   └── controller/
│       ├── SimulacionController.java
│       └── ExportadorCSV.java
├── netlogo/
│   ├── SIR_Java.nlogox
│   ├── lector_csv.nls
│   └── vista_sir.nls
├── resultados/resultados_java.csv       # Generado al ejecutar
└── target/sir-simulacion.jar            # Generado al compilar
```


| Archivo o clase | Responsabilidad |
| --- | --- |
| Main | Lee argumentos, compone dependencias y presenta el resumen |
| ParametrosSimulacion | Constantes, datos de parámetros y validación |
| EstadoSalud / Individuo | Estados permitidos e identidad/estado de cada persona |
| Poblacion | Colección ordenada, conteos y validación de transiciones |
| RegistroPaso / ResultadoSimulacion | Una observación y el historial completo protegido |
| MotorSimulacionSIR | Inicialización y evolución del SIR |
| GeneradorAleatorio / GeneradorJava | Contrato de sorteos y adaptación de Random |
| SimulacionController | Solicita cálculo y después exportación |
| ExportadorCSV | Crea carpetas y escribe cabecera y filas |
| SIR_Java.nlogox | Widgets y composición del modelo NetLogo |
| lector_csv.nls | Importación, validación e índice de lectura |
| vista_sir.nls | Representantes visuales, colores, puntos de gráfica y temporizador |

## Contrato CSV y comunicación

```csv
tiempo,susceptibles,infectados,recuperados
0,92,8,0
```

La fila mostrada corresponde a los valores actuales. El CSV es UTF-8 sin BOM, separado por comas, sin índice extra ni comentarios. Con T=100 contiene 101 filas de datos y cabecera: 102 líneas. Se cierra mediante try-with-resources y sobrescribe la ejecución anterior.

El lector NetLogo usa `csv:from-file`. Comprueba cabecera, estructura, enteros no negativos, secuencia temporal, población constante y transiciones agregadas compatibles con el modelo. Deduce N y el horizonte del archivo. Una carga inválida no reemplaza un historial válido ya cargado.

La vista crea un círculo por individuo, comprueba que cada color coincida con S/I/R, y agrega un punto por serie para cada registro. `timer` regula los segundos de reproducción; `ticks` conserva el tiempo del CSV. El deslizador tiene nombre visible y variable `velocidad`, iguales para evitar la diferencia de carga entre GUI y ejecución sin ventana.

El CSV no exporta identidades, posiciones ni contactos. Las curvas son las de Java, pero la selección de círculos que cambian de color y su posición son representativas. No se reconstruye quién contagió a quién ni se afirma que sea una simulación SIR independiente en NetLogo.

## Problemas frecuentes

- **mvn: command not found:** instala Maven, usa el Maven del IDE o la ruta local indicada. No hay `mvnw` dentro de este proyecto.
- **JAR no encontrado:** compila desde la raíz; `target` es una carpeta generada.
- **Cambios de parámetros sin efecto:** recompila antes de ejecutar. Revisa la primera fila del CSV.
- **NetLogo no encuentra el CSV:** ejecuta Java desde la raíz y conserva las carpetas `netlogo` y `resultados` como hermanas.
- **Vista anterior o variable velocidad no definida:** vuelve a abrir el modelo actualizado; conserva `display` y `variable` del deslizador como `velocidad`. No abras un `.nls` como modelo independiente.
- **No se ve el nuevo escenario:** pausa y pulsa Cargar CSV; el historial anterior permanece en memoria hasta recargar.

