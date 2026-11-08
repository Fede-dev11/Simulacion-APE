# Validación estadística de números pseudoaleatorios

Proyecto académico de Simulación que genera números pseudoaleatorios mediante un
generador congruencial lineal (LCG), evalúa su compatibilidad con una distribución
uniforme y compara dos implementaciones equivalentes: Python y Java.

## Problemática

Los números producidos por un algoritmo son pseudoaleatorios: aunque visualmente
parezcan aleatorios, pueden contener sesgos o patrones que afecten los resultados de
una simulación. Por ello, antes de utilizarlos se debe comprobar si presentan el
comportamiento estadístico esperado.

Este proyecto estudia la uniformidad de una secuencia en el intervalo `[0,1)` con:

- **Chi-cuadrado**, que compara frecuencias observadas y esperadas en intervalos.
- **Kolmogorov-Smirnov (KS)**, que compara la distribución acumulada empírica con
  la acumulada uniforme teórica `F(x) = x`.

La hipótesis nula es que los valores siguen una distribución uniforme `U(0,1)`. Si
el valor p es menor que `alfa = 0.05`, se rechaza la hipótesis nula; en caso
contrario, no se rechaza. No rechazarla no demuestra que el generador sea realmente
aleatorio ni que sus valores sean independientes.

## Configuración utilizada

La ejecución base utiliza:

| Parámetro | Valor |
| --- | ---: |
| N | 10000 |
| Intervalos `k` | 10 |
| Nivel de significancia `alfa` | 0.05 |
| Semilla | 12345 |
| Multiplicador `a` | 1664525 |
| Incremento `c` | 1013904223 |
| Módulo `m` | `2^32` |

Los parámetros del LCG son una propuesta reproducible del proyecto, no valores
obligatorios de la guía. La secuencia se genera mediante:

```text
X(n+1) = (a * X(n) + c) mod m
U(n+1) = X(n+1) / m
```

La semilla es el estado inicial. El primer dato guardado corresponde a la primera
actualización del estado.

## Decisiones de diseño

### Arquitectura MVC

Se utilizó MVC para separar responsabilidades:

- `model`: configuración, generación y fórmulas estadísticas.
- `views`: presentación en consola y, en Python, creación de gráficas.
- `controller`: coordina la generación, las pruebas, la presentación y exportación.
- `storage`: guarda configuraciones, secuencias y resultados en CSV.

Esta separación permite revisar las fórmulas sin mezclarlas con mensajes de consola,
archivos o gráficas.

### Strategy

Chi-cuadrado y KS respetan un contrato común denominado `PruebaEstadistica`. Cada
prueba recibe una secuencia y devuelve un `ResultadoPrueba` con nombre, estadístico,
valor p, decisión y detalles. Esto permite agregar otra prueba sin modificar las ya
implementadas.

### SOLID e inyección de dependencias

Cada componente posee una responsabilidad concreta. El controlador recibe el
generador, las pruebas, las vistas y el exportador mediante su constructor. De esta
manera, el controlador coordina el proceso, pero no contiene fórmulas estadísticas.

### CSV en lugar de base de datos

Los resultados son reproducibles, pequeños y tabulares, por lo que se almacenan en
CSV. Esto facilita abrirlos en una hoja de cálculo y comparar Python con Java sin
introducir una base de datos innecesaria.

### Precisión y equivalencia entre lenguajes

- Java utiliza `BigInteger` para evitar desbordamientos en la operación del LCG.
- Python conserva naturalmente los estados como enteros de precisión arbitraria.
- Ambos calculan explícitamente Chi-cuadrado, `D+`, `D-` y `D`.
- Para KS ambos emplean el método bilateral asintótico evaluado en `sqrt(N) * D`.
- Los valores p se obtienen con SciPy en Python y Apache Commons Math en Java.
- Los estados enteros deben coincidir exactamente.
- La tolerancia es `1e-15` para normalizados y `1e-12` para estadísticos y valores p.

### Gráficas

Matplotlib genera el histograma y la comparación entre la acumulada empírica y
`F(x) = x`. Java calcula sus propios resultados; Python lee los CSV producidos por
Java y crea sus gráficas para no añadir una biblioteca gráfica adicional al proyecto
Java.

## Estructura general

```text
APE6/
├── README.md
├── comparacion_resultados.csv
├── python/
│   ├── main.py
│   ├── comparar_resultados.py
│   ├── requirements.txt
│   ├── model/
│   ├── views/
│   ├── controller/
│   ├── storage/
│   └── resultados/
└── java/
    ├── src/
    │   ├── Main.java
    │   ├── model/
    │   ├── views/
    │   ├── controller/
    │   └── storage/
    ├── test/
    ├── lib/
    └── resultados/
```

## Estructura de Python

```text
python/
├── main.py
├── comparar_resultados.py
├── requirements.txt
├── model/
│   ├── configuracion.py
│   ├── generador_lcg.py
│   ├── chi_cuadrado.py
│   ├── kolmogorov_smirnov.py
│   ├── prueba_estadistica.py
│   └── resultado_prueba.py
├── views/
│   ├── consola.py
│   └── graficas.py
├── controller/
│   └── controlador.py
├── storage/
│   └── exportador_csv.py
└── resultados/
    ├── configuracion.csv
    ├── secuencia.csv
    ├── frecuencias_chi_cuadrado.csv
    ├── resultados_pruebas.csv
    ├── versiones.txt
    ├── acumulada.png
    └── histograma.png
```

- `main.py`: construye los componentes e inicia la ejecución.
- `configuracion.py`: contiene y valida los parámetros.
- `generador_lcg.py`: genera estados enteros y valores normalizados.
- `chi_cuadrado.py`: calcula intervalos, frecuencias, estadístico y valor p.
- `kolmogorov_smirnov.py`: calcula `D+`, `D-`, `D` y valor p.
- `consola.py`: muestra parámetros, secuencia abreviada y resultados.
- `graficas.py`: crea el histograma y la gráfica de acumuladas.
- `controlador.py`: coordina el caso de uso sin implementar fórmulas.
- `exportador_csv.py`: guarda los datos con precisión suficiente para compararlos.
- `comparar_resultados.py`: compara los CSV de Python y Java y genera la tabla final.

## Estructura de Java

```text
java/
├── src/
│   ├── Main.java
│   ├── model/
│   │   ├── Configuracion.java
│   │   ├── DatoGenerado.java
│   │   ├── GeneradorLCG.java
│   │   ├── ChiCuadrado.java
│   │   ├── KolmogorovSmirnov.java
│   │   ├── PruebaEstadistica.java
│   │   ├── ResultadoPrueba.java
│   │   └── Intervalo.java
│   ├── views/
│   │   └── VistaConsola.java
│   ├── controller/
│   │   └── Controlador.java
│   └── storage/
│       └── ExportadorCSV.java
├── test/
│   └── TestRunner.java
├── lib/
│   └── commons-math3-3.6.1.jar
└── resultados/
    ├── configuracion.csv
    ├── secuencia.csv
    ├── frecuencias_chi_cuadrado.csv
    ├── resultados_pruebas.csv
    ├── versiones.txt
    ├── acumulada.png
    └── histograma.png
```

- `Main.java`: conecta los componentes e inicia el programa.
- `Configuracion.java`: almacena y valida los parámetros.
- `GeneradorLCG.java`: usa `BigInteger` y genera la secuencia.
- `ChiCuadrado.java` y `KolmogorovSmirnov.java`: realizan los cálculos.
- `PruebaEstadistica.java`: define el contrato Strategy.
- `VistaConsola.java`: presenta los datos y resultados.
- `Controlador.java`: coordina la ejecución.
- `ExportadorCSV.java`: exporta los mismos campos que Python.
- `TestRunner.java`: verifica la secuencia manual, validaciones, frecuencias y KS.

## Requisitos en Linux

### Python

- Linux de 64 bits.
- Python 3.11 o superior; el proyecto fue verificado con Python 3.14.4.
- Módulo `venv` de Python.
- Acceso a Internet solo durante la instalación inicial de dependencias.
- SciPy 1.16.3 y Matplotlib 3.10.7, instalados desde `requirements.txt`.

En Debian o Ubuntu se pueden instalar los requisitos del sistema con:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

### Java

- JDK 17 o superior; el proyecto fue verificado con Java 24.
- No se necesita Maven ni Gradle.
- Apache Commons Math 3.6.1 ya está incluido en `java/lib`.

En Debian o Ubuntu se puede instalar el JDK con:

```bash
sudo apt update
sudo apt install openjdk-17-jdk
```

Para comprobar las instalaciones:

```bash
python3 --version
javac -version
java -version
```

## Ejecución en Linux

Todos los comandos siguientes parten desde una terminal Linux.

### 1. Preparar y ejecutar Python

Entrar en la carpeta Python:

```bash
cd "/home/feder/Escritorio/UNL/QUINTO/Simulacion/U2 APE/APE6/python"
```

Crear el entorno virtual e instalar las dependencias la primera vez:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Ejecutar el programa:

```bash
.venv/bin/python main.py
```

Los CSV y las gráficas se crearán o actualizarán en `python/resultados`.

### 2. Compilar y ejecutar Java

Entrar en la carpeta Java:

```bash
cd "/home/feder/Escritorio/UNL/QUINTO/Simulacion/U2 APE/APE6/java"
```

Crear la carpeta de compilación y compilar:

```bash
mkdir -p out
javac -cp lib/commons-math3-3.6.1.jar -d out src/Main.java src/model/*.java src/views/*.java src/storage/*.java src/controller/*.java
```

Ejecutar Java:

```bash
java -cp out:lib/commons-math3-3.6.1.jar Main
```

Los CSV se crearán o actualizarán en `java/resultados`.

### 3. Ejecutar las verificaciones Java

Desde la carpeta `java`:

```bash
javac -cp out:lib/commons-math3-3.6.1.jar -d out test/TestRunner.java
java -cp out:lib/commons-math3-3.6.1.jar TestRunner
```

El resultado esperado es:

```text
OK: 7 verificaciones Java superadas
```

### 4. Comparar Python y Java

Primero deben haberse ejecutado los dos programas. Después, entrar en Python y
ejecutar el comparador:

```bash
cd "/home/feder/Escritorio/UNL/QUINTO/Simulacion/U2 APE/APE6/python"
.venv/bin/python comparar_resultados.py
```

El comparador:

1. Lee las dos secuencias CSV.
2. Compara los 10000 estados enteros.
3. Compara normalizados, estadísticos y valores p con tolerancias explícitas.
4. Genera las gráficas correspondientes a Java.
5. Crea `comparacion_resultados.csv` en la raíz del proyecto.

La salida esperada incluye:

```text
Estados enteros idénticos: True (10000 de 10000)
Máxima diferencia normalizada: 0
Comparación aprobada con tolerancias: normalizados=1e-15, estadísticos=1e-12, valores p=1e-12
```

## Resultados y documentación

- `comparacion_resultados.csv` contiene la comparación completa entre lenguajes.
- Cada carpeta `resultados` conserva configuración, secuencia, frecuencias,
  resultados, versiones y gráficas.

La tabla de la guía menciona «pi estimado» y «Error», pero el procedimiento resumido
no explica esa actividad; por ello no se implementó una estimación de pi. Las pruebas
de rachas, poker, seriales y baterías completas tampoco forman parte del alcance.
