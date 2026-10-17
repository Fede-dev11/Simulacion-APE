# Simulación de modelos de crecimiento poblacional

Proyecto en Python para comparar cuatro modelos de crecimiento poblacional: determinístico, discreto, estocástico y continuo mediante el método de Euler. El programa muestra gráficas de crecimiento y decrecimiento a partir de un conjunto de datos de entrada.

> **Nota sobre el alcance:** el código incluido en este repositorio simula crecimiento poblacional. No contiene un modelo de atmósfera ni una predicción de lluvia.

## Tecnologías utilizadas

- **Python 3.10 o superior:** lenguaje de implementación.
- **NumPy:** operaciones numéricas, vectores de tiempo y generación de ruido aleatorio.
- **Matplotlib:** visualización comparativa de los resultados.

Se eligieron estas tecnologías porque permiten implementar las ecuaciones, manejar los arreglos numéricos y visualizar los resultados con una instalación sencilla.


## Decisiones tecnológicas y justificación

Las tecnologías se seleccionaron según las necesidades de la simulación y procurando que el proyecto fuera sencillo de instalar, ejecutar y modificar:

- **Python 3:** se eligió por su sintaxis clara y porque permite implementar directamente las ecuaciones matemáticas de los modelos.
- **NumPy:** se utiliza para generar vectores de tiempo, calcular el crecimiento exponencial y trabajar con arreglos numéricos. También permite generar el ruido aleatorio del modelo estocástico mediante `numpy.random.normal`.
- **Matplotlib:** se utiliza para representar en gráficas los resultados de los cuatro modelos y compararlos con los datos de entrada.
- **`venv` y `requirements.txt`:** se recomiendan para aislar las dependencias del proyecto y facilitar que otra persona pueda instalar las mismas bibliotecas.

## Decisiones de diseño y patrones utilizados

El código separa las responsabilidades en tres partes: modelos, controlador y vista. Esta organización facilita localizar los cálculos, coordinar la ejecución y cambiar la forma de presentar los resultados sin concentrar todo en un solo archivo.

### 1. Patrón Modelo–Vista–Controlador (MVC)

El proyecto sigue una organización inspirada en MVC:

- **Modelo (`modelo/`):** contiene la clase base `Modelo_Crecimiento` y los cuatro modelos que implementan el método `simular()`.
- **Controlador (`controller/controlador.py`):** calcula la tasa de crecimiento aproximada, prepara los parámetros, ejecuta los modelos y entrega los resultados a la vista.
- **Vista (`views/graficas.py`):** crea las gráficas y muestra las curvas, los datos de entrada, los títulos, las leyendas y la cuadrícula.

**¿Por qué se eligió?** Para separar los cálculos matemáticos de la coordinación del programa y de la presentación gráfica. Así, se puede modificar una gráfica sin tener que reescribir las ecuaciones de los modelos.

### 2. Estrategia (Strategy), aplicada a los modelos de simulación

Los modelos determinístico, discreto, estocástico y continuo comparten una interfaz: todos reciben parámetros comunes y ofrecen el método `simular()`. El controlador mantiene las clases de los modelos en `MODELOS` y los ejecuta de manera uniforme.

**¿Por qué se eligió?** Porque permite comparar distintos métodos de simulación sin escribir un flujo de ejecución diferente para cada uno. Si se incorpora otro modelo compatible con la misma interfaz, se puede añadir a la lista del controlador y reutilizar el proceso de comparación.

### 3. Herencia y polimorfismo

Las clases `Deterministico`, `Discreto`, `Estocastico` y `Continuo` heredan de `Modelo_Crecimiento` y cada una implementa su propia versión de `simular()`. El controlador puede tratarlas de la misma manera aunque cada una calcule la población de forma distinta.

**¿Por qué se eligieron?** La herencia permite reutilizar los parámetros comunes (`p0`, `r`, `tiempo`, `sigma` y `dt`), mientras que el polimorfismo permite ejecutar cada método con una llamada uniforme.

> **Aclaración:** el código actual no implementa una fábrica (*Factory*) explícita. Las clases de los modelos se enumeran directamente en `Controlador.MODELOS`; por ello, no se documenta Factory como un patrón implementado.

## Estructura del proyecto

```text
Practica2/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── modelo/
│   ├── basemodelo.py
│   ├── deterministico.py
│   ├── discreto.py
│   ├── estocastico.py
│   └── continuo.py
├── controller/
│   └── controlador.py
└── views/
    └── graficas.py
```

- `modelo/`: contiene la clase base y las implementaciones de los cuatro modelos.
- `controller/controlador.py`: calcula una tasa de crecimiento aproximada y coordina la ejecución de los modelos.
- `views/graficas.py`: genera las gráficas comparativas.
- `main.py`: punto de entrada del programa.

## Requisitos

- Python 3.10 o superior.
- `numpy`.
- `matplotlib`.

## Instalación y ejecución

Desde una terminal, sitúate en la carpeta raíz `Practica2`.

### Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

## Datos de entrada

En `main.py` se utiliza el arreglo:

```python
datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]
```

Puedes cambiar estos valores para ejecutar la comparación con otros datos. El controlador utiliza el primer valor como población inicial y estima la tasa de crecimiento a partir del primero y del último dato.

## Modelos implementados

1. **Determinístico:** usa la expresión exponencial `P(t) = P0 * exp(r*t)`.
2. **Discreto:** actualiza la población en períodos definidos.
3. **Estocástico:** añade ruido aleatorio con distribución normal, controlado por `sigma`.
4. **Continuo (Euler):** aproxima el crecimiento mediante pasos de tamaño `dt`.

