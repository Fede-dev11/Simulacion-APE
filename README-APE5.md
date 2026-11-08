# Generador Congruencial Lineal en Python y Java

Proyecto de la práctica APE 5 de Simulación. Implementa el mismo Generador
Congruencial Lineal (LCG) en Python y Java, genera 10 000 valores con dos
semillas, guarda los resultados en CSV, compara ambas implementaciones y crea
gráficas de dispersión.

## 1. Requisitos previos

- Python 3.10 o posterior.
- Java JDK 17 o posterior.
- `pip`, el instalador de paquetes de Python.
- Bash para utilizar el script de ejecución completa.

Compruebe las versiones instaladas:

```bash
python3 --version
javac -version
java -version
```

## 2. Instalación

Abra una terminal en la carpeta principal del proyecto:

```bash
cd "U2 APE/APE5"
```

Se recomienda crear un entorno virtual para instalar Pillow sin afectar otros
proyectos:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

En Windows PowerShell, el entorno se activa con:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Ejecución completa

Con el entorno virtual activado, ejecute:

```bash
bash ejecutar.sh
```

El script realiza estas acciones:

1. Compila el proyecto Java.
2. Ejecuta Python con las semillas `12345` y `67890`.
3. Ejecuta Java con las mismas semillas.
4. Compara los 10 000 resultados de la semilla principal.
5. Crea la gráfica de Python y la gráfica de Java.

## 4. Ejecución por separado

### Python

```bash
PYTHONPATH=python/src python3 -m simulacion.main
python3 grafica.py
```

También se pueden cambiar las semillas, la cantidad y el directorio:

```bash
PYTHONPATH=python/src python3 -m simulacion.main \
  --seed 12345 --second-seed 99 --count 10000 \
  --output resultados_python
```

### Java

Compile el proyecto:

```bash
mkdir -p java/out
javac -d java/out $(find java/src -name '*.java')
```

Ejecútelo:

```bash
java -Djava.awt.headless=true -cp java/out simulacion.Main
```

Los argumentos opcionales se reciben en el orden `semilla1 semilla2 cantidad
directorio_salida`:

```bash
java -Djava.awt.headless=true -cp java/out simulacion.Main \
  12345 99 10000 resultados_java
```

### Comparación

Después de ejecutar ambos programas:

```bash
python3 comparar.py
```

Se crea `tabla_comparacion.csv`, que contiene los estados y valores normalizados
de ambos lenguajes, junto con una columna que indica si cada fila coincide.

## 5. Modelo matemático utilizado

El siguiente estado del LCG se calcula con:

```text
X(n+1) = (a × X(n) + c) mod m
```

El valor normalizado es:

```text
U(n) = X(n) / m
```

Parámetros de la práctica:

| Parámetro | Valor |
|---|---:|
| Multiplicador `a` | 1 664 525 |
| Incremento `c` | 1 013 904 223 |
| Módulo `m` | 2³² = 4 294 967 296 |
| Semilla principal | 12 345 |
| Segunda semilla | 67 890 |
| Valores por semilla | 10 000 |

La semilla representa `X(0)`. Por ello, la primera fila guardada corresponde a
`X(1)`. Los valores `U(n)` pertenecen al intervalo `[0, 1)`.

## 6. Análisis de los resultados

Los 10 000 estados generados por Python y Java para la semilla `12345`
coinciden exactamente. Esto confirma que las dos implementaciones aplican la
misma recurrencia y controlan correctamente la aritmética módulo `2³²`.

| Semilla | Media de U(n) | Varianza | Mínimo | Máximo | Correlación consecutiva |
|---:|---:|---:|---:|---:|---:|
| 12345 | 0,49876985 | 0,08301177 | 0,00005908 | 0,99992597 | -0,01531101 |
| 67890 | 0,50006664 | 0,08400996 | 0,00005914 | 0,99994938 | -0,00850072 |

Para una distribución uniforme continua en `[0, 1)`, la media teórica es `0,5`
y la varianza `1/12 ≈ 0,08333`. Los resultados obtenidos son cercanos a estos
valores. Las correlaciones consecutivas son pequeñas en la muestra observada.
Esto es evidencia descriptiva, pero no sustituye una batería completa de pruebas
estadísticas.

Cambiar la semilla modifica la secuencia, mientras que repetir una semilla
reproduce exactamente los mismos valores. El período máximo es `2³²` porque el
incremento es coprimo con el módulo y `a - 1` es divisible por 4, cumpliendo las
condiciones de Hull-Dobell.

## 7. Organización del proyecto

```text
APE5/
├── python/src/simulacion/
│   ├── main.py
│   ├── model/
│   │   └── linear_congruential_generator.py
│   ├── controller/
│   │   └── lcg_controller.py
│   └── view/
│       └── console_view.py
├── java/src/simulacion/
│   ├── Main.java
│   ├── model/
│   │   ├── NumberGenerator.java
│   │   ├── RandomValue.java
│   │   └── LinearCongruentialGenerator.java
│   ├── controller/
│   │   └── LCGController.java
│   └── view/
│       ├── ConsoleView.java
│       └── Grafica.java
├── comparar.py
├── grafica.py
├── ejecutar.sh
├── requirements.txt
├── INFORME_APE5.html
├── INFORME_APE5.docx
├── INFORME_APE5.pdf
└── README.md
```

## 8. Función de los archivos

- **`main.py` y `Main.java`:** configuran y ejecutan las dos semillas.
- **`LinearCongruentialGenerator`:** implementa la fórmula del LCG y comprueba
  las condiciones del período.
- **`NumberGenerator`:** define la estrategia común de generación.
- **`LCGController`:** coordina generación, exportación CSV y presentación.
- **`ConsoleView`:** muestra las primeras 20 observaciones y el período.
- **`Grafica.java`:** crea la gráfica conjunta de las dos semillas de Java.
- **`grafica.py`:** crea la gráfica conjunta desde los CSV de Python.
- **`comparar.py`:** compara los CSV de Python y Java.
- **`ejecutar.sh`:** automatiza compilación, ejecución, comparación y gráficas.
- **`requirements.txt`:** declara Pillow, usado para la gráfica de Python.

## 9. Patrones y organización de diseño empleados

1. **MVC:** el modelo realiza el cálculo, la vista presenta los resultados y el
   controlador coordina el proceso.
2. **Strategy:** `NumberGenerator` define el contrato y
   `LinearCongruentialGenerator` implementa la estrategia concreta. Esto permite
   incorporar otro generador sin cambiar el controlador.
3. **Inyección de dependencias:** el modelo y la vista se entregan al controlador
   mediante su constructor, reduciendo el acoplamiento.
4. **Separación de responsabilidades:** generación, presentación, exportación,
   comparación y gráficas se encuentran en componentes distintos.

## 10. Archivos generados

- `resultados_python/semilla_12345.csv`
- `resultados_python/semilla_67890.csv`
- `resultados_java/semilla_12345.csv`
- `resultados_java/semilla_67890.csv`
- `tabla_comparacion.csv`
- `graficas/grafica_python.png`
- `graficas/grafica_java.png`

En cada gráfica, la semilla `12345` aparece en azul y la semilla `67890` en
rojo. El eje horizontal representa `n` y el vertical representa `U(n)`.

## 11. Solución de problemas frecuentes

- **No se encuentra Pillow:** active `.venv` y ejecute
  `python -m pip install -r requirements.txt`.
- **No se encuentra el módulo `simulacion`:** ejecute Python desde la raíz con
  `PYTHONPATH=python/src`.
- **Java no encuentra `simulacion.Main`:** compile primero con `javac -d
  java/out ...` y use `-cp java/out`.
- **Error gráfico de Java en Linux:** conserve la opción
  `-Djava.awt.headless=true`.
- **No existen los CSV para comparar:** ejecute primero Python y Java o use
  `bash ejecutar.sh`.
- **Los resultados no coinciden:** compruebe que ambos programas usen iguales
  parámetros, semilla y cantidad.

## 12. Dependencias

Pillow es la única biblioteca externa de Python y está declarada en
`requirements.txt`. `csv`, `argparse`, `pathlib` y `abc` pertenecen a la
biblioteca estándar. Java utiliza únicamente clases incluidas en el JDK.

Para salir del entorno virtual:

```bash
deactivate
```
