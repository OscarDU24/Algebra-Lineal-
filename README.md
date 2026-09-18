# Calculadora de Algebra Lineal

Aplicacion de escritorio para practicar operaciones con matrices, vectores, sistemas de ecuaciones, limites y sistemas numericos.

## Descripcion general

La aplicacion utiliza una ventana principal, llamada Dashboard, como punto de entrada
a los distintos modulos matematicos. Cada tarjeta del Dashboard abre una calculadora
especializada en una ventana independiente. De esta forma, los modulos conservan su
propia interfaz y logica, pero el usuario puede volver al menu principal sin cerrar
la aplicacion completa.

Los modulos disponibles son:

- Matrices individuales.
- Operaciones vectoriales.
- Ecuaciones matriciales.
- Ecuaciones lineales e independencia lineal.
- Calculo de limites.
- Sistemas numericos.

### Tabla de intercambio de Leontief

La calculadora de ecuaciones matriciales incluye la opcion `Tabla de Intercambio`. Esta herramienta
resuelve el modelo abierto mediante el sistema:

```text
(I - A)X = D
```

En lugar de calcular explicitamente la inversa de `I - A`, construye la matriz
aumentada `[I - A | D]` y aplica eliminacion de Gauss-Jordan con listas de Python.
La salida muestra la matriz `I - A`, la matriz aumentada, los pasos de reduccion y
el vector de produccion `X`.

El modelo cerrado agrega el sector hogares como un sector endogeno. Para ello se
ingresan, ademas, los coeficientes de consumo de los hogares y los coeficientes de
ingreso generados por cada sector. La demanda externa se mantiene en los sectores
productivos y la demanda externa del sector hogares se toma como cero.

### Flujo de red

La calculadora de ecuaciones matriciales tambien incluye la opcion `Flujo de Red`. Cada rama se
define por un nodo origen y un nodo destino, y su variable de flujo es positiva en
ese sentido. Para cada nodo se plantea la ecuacion:

```text
salidas - entradas = balance externo
```

El programa construye la matriz de incidencia `C`, forma el sistema aumentado
`[C | b]` y aplica Gauss-Jordan. La salida identifica los pivotes, las ramas libres
y los flujos resultantes. Si los balances son incompatibles, informa que no existe
un flujo que satisfaga simultaneamente todas las ecuaciones.

## Requisitos

- Windows 10 u 11
- Python 3.13 de 64 bits
- Git

La aplicacion utiliza `ctypes` para registrar temporalmente las fuentes incluidas en `core/assets/fonts`, por lo que esta version esta preparada principalmente para Windows.

## Instalacion para colaboradores

Desde PowerShell, clona el repositorio y entra en la carpeta del proyecto:

```powershell
git clone URL_DEL_REPOSITORIO
cd Algebra-Lineal
```

Crea el entorno virtual con Python 3.13:

```powershell
py -3.13 -m venv .venv
```

Activa el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell impide la activacion, puedes continuar sin activarlo usando directamente el ejecutable del entorno.

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

### Por que se utiliza un entorno virtual

El entorno virtual `.venv` mantiene las dependencias de este proyecto separadas de
las instalaciones globales de Python. Esto evita conflictos entre versiones y permite
que cada colaborador trabaje con las versiones fijadas en `requirements.txt`.

El entorno debe crearse con una version de Python compatible con el proyecto. En
Windows se recomienda Python 3.13 de 64 bits. La carpeta `.venv` es local para cada
colaborador y no debe subirse al repositorio.

Ejecuta la aplicacion:

```powershell
python main.py
```

Sin activar el entorno virtual:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Flujo de navegacion entre calculadoras

El flujo de transicion es el siguiente:

1. `main.py` crea la ventana raiz de Tkinter y construye el `Dashboard`.
2. El Dashboard muestra una tarjeta para cada calculadora disponible.
3. Al seleccionar una tarjeta, el Dashboard actualiza la barra de estado y se oculta
	temporalmente mediante `withdraw()`.
4. El controlador importa y crea la vista correspondiente como una ventana secundaria
	(`Toplevel`). La importacion dentro del controlador permite cargar cada modulo al
	utilizarlo.
5. Al cerrar la calculadora, su metodo `al_cerrar()` vuelve a mostrar el Dashboard con
	`deiconify()` y destruye solamente la ventana secundaria.
6. Al elegir `Archivo > Salir`, se desregistran las fuentes temporales y se cierra la
	ventana principal junto con la aplicacion.

Este patron se aplica a las vistas de matrices, vectores, ecuaciones matriciales,
sistemas, limites y sistemas numericos. La referencia al Dashboard se guarda en cada
vista secundaria como `master_dashboard`, lo que permite regresar al menu sin crear
una segunda ventana principal.

## Estructura del proyecto

```text
main.py                 Punto de entrada de la aplicacion
requirements.txt        Dependencias y versiones fijadas
core/
  ui/                   Dashboard y ventanas de cada calculadora
  vectores/             Operaciones, conversiones y validaciones vectoriales
  lineal/               Eliminacion y resolucion de sistemas lineales
  matriciales/          Operaciones con matrices y ecuaciones matriciales
  limites/              Operaciones relacionadas con limites
  sistemas/             Operaciones con sistemas
  sistemas_numericos/   Conversiones y operaciones entre bases numericas
  assets/               Fondos e imagenes de la interfaz
```

La interfaz se mantiene separada de la logica matematica. Por ejemplo, `vista_vector.py`
se encarga de recibir datos y mostrar resultados, mientras que los modulos dentro de
`core/vectores/` realizan las conversiones y operaciones. Esta separacion facilita
probar o reutilizar la logica sin depender directamente de los widgets.

## Mejoras recientes del modulo de vectores

- Las fracciones se convierten con `fractions.Fraction`, evitando el uso incorrecto
  de `rstrip("/1")` y reduciendo correctamente valores como `0.1` a `1/10`.
- Las entradas aceptan enteros, decimales, negativos y fracciones como `1/3`.
- Los denominadores cero se validan sin cerrar la aplicacion.
- La tolerancia numerica se centralizo en `constantesVectores.py`.
- La copia de vectores se reutiliza desde `utilidadesVectores.py`.
- Las operaciones basicas utilizan comprensiones, `zip()` y `sum()` manteniendo la
  restriccion de utilizar Python estandar, sin NumPy ni SciPy.

## Configuracion en VS Code

Selecciona como interprete de Python:

```text
.venv\\Scripts\\python.exe
```

Despues ejecuta `main.py`.

## Dependencias

Las versiones utilizadas estan fijadas en `requirements.txt` para que todos los colaboradores instalen el mismo conjunto de paquetes.

Dependencias principales:

- `customtkinter`: controles visuales de las calculadoras.
- `Pillow`: carga y visualizacion de recursos graficos.
- `prettytable`: presentacion tabular de algunos resultados.

Las operaciones vectoriales, matriciales y de limites implementadas para la actividad
utilizan listas, ciclos, condicionales, `ast` y funciones propias de Python estandar,
sin NumPy, SciPy, SymPy ni funciones avanzadas de `math`.

## Recursos incluidos

- `core/assets/Bordes.png`: fondo decorativo.
- `core/assets/fonts/`: fuentes utilizadas por la interfaz.

Las fuentes deben conservarse junto con el proyecto. Antes de redistribuir la aplicacion, verifica que sus licencias permitan incluirlas.

## Estado del entorno

No se debe subir `.venv`, `__pycache__` ni archivos `.pyc`. Cada colaborador debe crear su propio entorno virtual local.

## Solucion de problemas frecuentes

### PowerShell no permite activar el entorno

La aplicacion puede ejecutarse directamente con el interprete del entorno virtual:

```powershell
.\.venv\Scripts\python.exe main.py
```

Tambien se puede seleccionar `.venv\Scripts\python.exe` como interprete de Python
en VS Code.

### No se muestran las fuentes o el fondo

Los recursos se cargan desde `core/assets`. Se debe conservar esa carpeta dentro del
proyecto. El registro temporal de fuentes se realiza principalmente en Windows; si
una fuente no puede registrarse, la interfaz utiliza fuentes de respaldo.
