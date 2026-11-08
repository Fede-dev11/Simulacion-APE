# APE 5: Generador Congruencial Lineal en Python y Java

## 1. Descripción

Este proyecto implementa el Generador Congruencial Lineal (LCG) solicitado en
la práctica de Simulación. Se desarrolló el mismo algoritmo en Python y Java
para comprobar que, con los mismos parámetros y semilla, ambos lenguajes
producen exactamente la misma secuencia.

Los programas generan archivos CSV. Después, `comparar.py` lee los CSV de ambos
lenguajes, compara sus 10 000 observaciones y crea una tabla conjunta. Finalmente,
`grafica.py` crea la gráfica de Python y Java crea su propia gráfica. Cada
imagen reúne las dos semillas, diferenciadas por color.

## 2. Fórmula y parámetros

```text
X(n+1) = (a × X(n) + c) mod m
U(n) = X(n) / m
```

| Parámetro | Valor |
|---|---:|
| Multiplicador `a` | 1 664 525 |
| Incremento `c` | 1 013 904 223 |
| Módulo `m` | 2³² = 4 294 967 296 |
| Semilla principal | 12 345 |
| Segunda semilla | 67 890 |
| Cantidad | 10 000 por semilla |

## 3. Arquitectura MVC

Los dos programas emplean Modelo-Vista-Controlador:

- **Modelo:** contiene el LCG, sus parámetros y genera la secuencia.
- **Vista:** presenta las primeras 20 observaciones, el período y la ruta del CSV.
- **Controlador:** solicita la secuencia, guarda el CSV y llama a la vista.
- **Main:** configura las dependencias y ejecuta las dos semillas.

```text
Main → Controlador → Modelo
          ↓            ↓
         CSV        Secuencia
          ↓
        Vista
```

## 4. Patrones de diseño utilizados

### MVC (Model-View-Controller)

Separa la lógica matemática, la presentación y la coordinación. Un cambio en
la salida no obliga a modificar el generador.

### Strategy

La generación se define mediante una abstracción: la clase abstracta
`NumberGenerator` en Python y la interfaz `NumberGenerator` en Java.
`LinearCongruentialGenerator` es la estrategia concreta. Así se puede agregar
otro generador sin cambiar la vista ni el flujo general.

### Inyección de dependencias por constructor

El controlador recibe el modelo y la vista en su constructor. Esto reduce el
acoplamiento y facilita sustituir o probar cada componente.

## 5. Estructura del proyecto

```text
APE5/
├── python/
│   └── src/simulacion/
│       ├── main.py
│       ├── model/
│       │   └── linear_congruential_generator.py
│       ├── view/
│       │   └── console_view.py
│       └── controller/
│           └── lcg_controller.py
├── java/
│   └── src/simulacion/
│       ├── Main.java
│       ├── model/
│       │   ├── NumberGenerator.java
│       │   ├── RandomValue.java
│       │   └── LinearCongruentialGenerator.java
│       ├── view/
│       │   ├── ConsoleView.java
│       │   └── Grafica.java
│       └── controller/
│           └── LCGController.java
├── comparar.py
├── grafica.py
├── ejecutar.sh
└── README.md
```

Al ejecutar se crean:

```text
resultados_python/
├── semilla_12345.csv
└── semilla_67890.csv
resultados_java/
├── semilla_12345.csv
└── semilla_67890.csv
tabla_comparacion.csv
graficas/
├── grafica_python.png
└── grafica_java.png
```

## 6. Requisitos

- Python 3.10 o posterior.
- JDK 17 o posterior.
- Terminal Bash para usar `ejecutar.sh`.
- Python requiere Pillow para la gráfica PNG (`pip install Pillow`).

```bash
python3 --version
javac -version
java -version
```

Los comandos siguientes se ejecutan desde la carpeta raíz `APE5`.

## 7. Ejecutar Python

Con valores predeterminados:

```bash
PYTHONPATH=python/src python3 -m simulacion.main
```

Con valores personalizados:

```bash
PYTHONPATH=python/src python3 -m simulacion.main \
  --seed 12345 --second-seed 99 --count 10000 \
  --output resultados_python
```

Esto crea un CSV para cada semilla dentro de `resultados_python`.

## 8. Compilar y ejecutar Java

Compilación:

```bash
mkdir -p java/out
javac -d java/out $(find java/src -name '*.java')
```

Ejecución predeterminada:

```bash
java -Djava.awt.headless=true -cp java/out simulacion.Main
```

Java acepta los argumentos `semilla1 semilla2 cantidad directorio_salida`:

```bash
java -Djava.awt.headless=true -cp java/out simulacion.Main 12345 99 10000 resultados_java
```

## 9. Ejecutar todo automáticamente

El método recomendado es:

```bash
bash ejecutar.sh
```

El script compila Java, ejecuta Python, ejecuta Java, compara sus CSV y genera
las dos gráficas de dispersión en PNG.

## 10. Comparar los resultados

Después de ejecutar ambos programas:

```bash
python3 comparar.py
```

El comparador lee:

```text
resultados_python/semilla_12345.csv
resultados_java/semilla_12345.csv
```

Muestra las primeras 20 filas y crea `tabla_comparacion.csv`:

| Columna | Significado |
|---|---|
| `n` | Número de observación |
| `X_Python` | Estado calculado por Python |
| `X_Java` | Estado calculado por Java |
| `U_Python` | Valor normalizado por Python |
| `U_Java` | Valor normalizado por Java |
| `Coincide` | Indica si ambos resultados son iguales |

La comparación termina con error si las cantidades son distintas o alguna fila
no coincide.

## 11. Generar las gráficas de dispersión

Después de generar los CSV se ejecuta:

```bash
python3 grafica.py
```

Se crean dos imágenes, una dibujada por cada lenguaje:

```text
graficas/grafica_python.png
graficas/grafica_java.png
```

Cada imagen contiene conjuntamente la semilla `12345` en azul y la semilla
`67890` en rojo. El eje horizontal representa la observación `n` y el vertical
el valor normalizado `U(n)`. Python usa sus CSV; Java dibuja desde las listas
generadas por su modelo.

## 12. Contenido de los CSV

Cada programa crea un CSV por semilla:

```text
n,X_n,U_n
```

- `n`: posición del número generado.
- `X_n`: estado entero del LCG.
- `U_n`: número normalizado en `[0, 1)`.

La primera fila corresponde a `X(1)`, calculado desde la semilla `X(0)`.

## 13. Análisis del período

El generador cumple las condiciones de Hull-Dobell porque:

- `c = 1013904223` es impar y coprimo con `2³²`.
- `a - 1 = 1664524` es divisible por 4.

Por ello, el período teórico máximo es:

```text
2³² = 4 294 967 296
```

No se recorren más de cuatro mil millones de valores; las condiciones
matemáticas permiten determinar el período directamente.
