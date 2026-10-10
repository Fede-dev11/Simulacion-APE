# Modelo matemático de posibilidad de lluvia

Proyecto en Python que lee datos meteorológicos desde Excel, valida la información, calcula un índice de posibilidad de lluvia con dos versiones del modelo y presenta gráficas para comparar los resultados y observar los cambios del índice durante el día.

## 1. Requisitos previos

- Python 3.10 o una versión posterior.
- `pip`, el instalador de paquetes de Python.
- El archivo de datos `archivos/clima.xlsx`, que se incluye en el proyecto.
- Para ver las gráficas, un entorno gráfico de escritorio. En un servidor sin interfaz gráfica se debe configurar Matplotlib para guardar las figuras en archivos en lugar de mostrarlas.

## 2. Instalación

Abra una terminal y entre en la carpeta del proyecto, es decir, donde está `main.py`:

```bash
cd modelo_comportamiento_atm
```

### Linux 

Se recomienda crear un entorno virtual para instalar las dependencias sin afectar otros proyectos:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si el comando para crear el entorno virtual indica que falta `venv`, instale el paquete correspondiente a su versión de Python (por ejemplo, `python3-venv`) y vuelva a ejecutar el comando.

## 3. Ejecución

Desde la carpeta principal del proyecto y con el entorno virtual activado, ejecute:

```bash
python main.py
```

El programa leerá `archivos/clima.xlsx`, comprobará los datos, imprimirá en la terminal los resultados del modelo original y del ajustado, y abrirá dos gráficas. Cierre cada ventana de gráfica para continuar con la siguiente.

La ruta del Excel está definida en `main.py` como `archivos/clima.xlsx`. Si cambia el nombre o la ubicación del archivo, actualice esa ruta.

## 4. Formato de los datos de entrada

El archivo Excel debe contener una hoja con estas columnas, respetando sus nombres:

| Columna | Descripción | Formato esperado |
|---|---|---|
| `Hora` | Hora de la medición | Texto u hora de Excel |
| `Humedad` | Humedad relativa | Número de 0 a 100 |
| `Nubosidad` | Nubosidad | Número de 0 a 100 |
| `Temperatura` | Temperatura en grados Celsius | Número |

El validador comprueba que existan las cuatro columnas, que humedad y nubosidad sean valores numéricos entre 0 y 100 y que no falten valores en las columnas meteorológicas. Si los datos no cumplen estas condiciones, el programa genera un error explicativo.

## 5. Modelo matemático utilizado

Primero se normalizan la humedad y la nubosidad dividiéndolas para 100:

- `H = Humedad / 100`
- `N = Nubosidad / 100`

La temperatura se transforma en un factor `Tf` de acuerdo con los intervalos establecidos en `models/calculador_clima.py`:

| Temperatura | Tf |
|---|---:|
| Menor o igual a 10 °C | 1.00 |
| Mayor que 10 y hasta 12 °C | 0.90 |
| Mayor que 12 y hasta 14 °C | 0.80 |
| Mayor que 14 y hasta 16 °C | 0.70 |
| Mayor que 16 y hasta 18 °C | 0.60 |
| Mayor que 18 y hasta 20 °C | 0.50 |
| Mayor que 20 y hasta 22 °C | 0.40 |
| Mayor que 22 y hasta 24 °C | 0.30 |
| Mayor que 24 y hasta 26 °C | 0.20 |
| Mayor que 26 °C | 0.10 |

### Modelo original

```text
I = 0.50 * H + 0.30 * N + 0.20 * Tf
```

### Modelo ajustado

```text
I = 0.45 * H + 0.35 * N + 0.20 * Tf
```

En el modelo ajustado se reduce el peso de la humedad de 0.50 a 0.45 y se aumenta el de la nubosidad de 0.30 a 0.35. El peso de la temperatura se mantiene en 0.20. Los coeficientes de cada modelo suman 1.

### Clasificación del índice

| Índice I | Clasificación |
|---|---|
| `I < 0.40` | Sin lluvia |
| `0.40 <= I < 0.60` | Baja posibilidad |
| `0.60 <= I < 0.75` | Lluvia probable |
| `I >= 0.75` | Lluvia |

Estas categorías son las reglas didácticas del ejercicio y no equivalen a probabilidades meteorológicas calibradas.

## 6. Organización del proyecto

```text
modelo_comportamiento_atm/
├── main.py
├── requirements.txt
├── README.md
├── archivos/
│   └── clima.xlsx
└── models/
    ├── calculador_clima.py
    ├── datos/
    │   ├── lector_excel.py
    │   └── validar_datos.py
    ├── modelos/
    │   ├── estrategia.py
    │   ├── modelo.py
    │   └── factory.py
    └── visualizacion/
        └── graficas.py
```

### Función de los archivos

- **`main.py`**: coordina la lectura, validación, cálculo, impresión de tablas y generación de gráficas.
- **`models/datos/lector_excel.py`**: abre el archivo Excel con pandas.
- **`models/datos/validar_datos.py`**: comprueba columnas, tipos y rangos de los datos.
- **`models/calculador_clima.py`**: normaliza humedad y nubosidad, calcula `Tf`, obtiene el índice y asigna la clasificación.
- **`models/modelos/estrategia.py`**: define una interfaz común para los modelos.
- **`models/modelos/modelo.py`**: contiene las fórmulas del modelo original y del ajustado.
- **`models/modelos/factory.py`**: crea el modelo solicitado (`original` o `ajustado`).
- **`models/visualizacion/graficas.py`**: dibuja la comparación de índices y los cambios entre mediciones consecutivas.
- **`archivos/clima.xlsx`**: contiene las observaciones meteorológicas de entrada.

## 7. Patrones y organización de diseño empleados

1. **Strategy (Estrategia):** `EstrategiaModelo` define el método `calcular()`. `ModeloOriginal` y `ModeloAjustado` implementan ese método con fórmulas diferentes. Así se puede cambiar de modelo sin reescribir el cálculo general.
2. **Factory (Fábrica simple):** `crear_modelo()` centraliza la creación del modelo según el texto recibido (`original` o `ajustado`). Si se solicita un tipo desconocido, genera un `ValueError`.
3. **Separación de responsabilidades / modularidad:** la lectura, validación, cálculo, definición de modelos y visualización están en módulos distintos. Esto facilita mantener, probar y modificar el programa.
4. **Validación de datos:** antes de realizar cálculos se revisan las columnas obligatorias y los rangos de humedad y nubosidad, evitando procesar entradas incorrectas conocidas.

## 8. Gráficas generadas

- **Comparación del modelo original y ajustado:** muestra el índice de ambos modelos en cada hora e incluye líneas de referencia en 0.40, 0.60 y 0.75.
- **Crecimiento y decrecimiento:** muestra la diferencia entre el índice de una medición y el de la medición anterior (`ΔI`). Un valor positivo indica crecimiento, uno negativo indica decrecimiento y cero indica que no hubo cambio.

La gráfica de crecimiento/decrecimiento usa los resultados del modelo original. Además, compara mediciones consecutivas del archivo; no estima una tasa continua entre ellas.

## 9. Dependencias

Las bibliotecas externas necesarias se encuentran en `requirements.txt`. Los módulos `abc` y `pathlib` forman parte de la biblioteca estándar de Python y no requieren instalación adicional.
