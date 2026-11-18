# HeyAlgb · Calculadora de Álgebra Lineal

Aplicación de escritorio educativa para practicar operaciones con matrices, vectores,
sistemas de ecuaciones, determinantes, límites, sistemas numéricos y métodos numéricos.
Cada herramienta muestra el procedimiento paso a paso, además del resultado.

> **Antes de distribuir la aplicación** (ejecutable, ZIP o portafolio), revisa
> [docs/RECURSOS_Y_LICENCIAS.md](docs/RECURSOS_Y_LICENCIAS.md). Según sus metadatos,
> el audio y dos fuentes incluidas no pueden redistribuirse.

## Estudio de UI/UX

El diagnostico de experiencia de usuario, la comparacion con calculadoras educativas,
las referencias de accesibilidad y el plan de pruebas se encuentran en
[docs/estudio-ui-ux-heyalg.md](docs/estudio-ui-ux-heyalg.md).

Las propuestas que aun no han sido aprobadas para desarrollo se conservan en
[docs/pendientes-ui-ux.md](docs/pendientes-ui-ux.md).

## Evolución de la interfaz con el pasar del tiempo

La interfaz actual es resultado de una revisión visual realizada durante el desarrollo
del proyecto. La versión anterior utilizaba una presentación más clara y ornamental,
con una cabecera morada en el Dashboard, tarjetas con espacios reservados para las
imágenes de cada calculadora y una apariencia menos uniforme entre el menú y las
ventanas de trabajo.

La versión actual separa con mayor claridad dos contextos de uso:

- **Dashboard:** funciona como menú visual de entrada. Utiliza un fondo decorativo,
  tarjetas con iconos, tipografías registradas desde `core/assets/fonts` y una barra de
  estado que indica el módulo activo.
- **Calculadoras:** priorizan la captura y lectura de datos. Usan CustomTkinter, fondo
  oscuro, paneles delimitados, bordes de acento rojo, botones con funciones visualmente
  diferenciadas y consolas monoespaciadas para procedimientos y resultados.

Los cambios principales fueron:

- Sustitución de la paleta anterior por una base negro, blanco y rojo definida en
  `core/ui/tema.py`.
- Centralización de estilos para paneles, botones principales, botones secundarios,
  menús desplegables y consolas de resultado.
- Incorporación de fondos e iconos reales en el Dashboard mediante Pillow.
- Registro temporal de fuentes incluidas en el proyecto para reforzar la jerarquía
  visual del título, las tarjetas y el menú.
- Organización de las calculadoras en áreas diferenciadas de configuración, captura,
  acciones, procedimiento y resultado.
- Incorporación de vistas previas para matrices, vectores, ecuaciones matriciales y
  sistemas lineales, actualizadas mientras el usuario escribe.
- Unificación del flujo de ventanas: el Dashboard se oculta al abrir una calculadora,
  conserva la referencia de la ventana activa y vuelve a mostrarse al cerrarla.

El objetivo de estos cambios no fue solo modificar colores. La interfaz pasó de ser una
colección de formularios independientes a una herramienta educativa con una jerarquía
visual más consistente: primero se identifica el módulo, después se introducen los
datos, se revisa su representación y finalmente se consulta el procedimiento y el
resultado.

## Descripcion general

La aplicacion utiliza una ventana principal, llamada Dashboard, como punto de entrada
a los distintos modulos matematicos. Cada tarjeta del Dashboard abre una calculadora
especializada en una ventana independiente. De esta forma, los modulos conservan su
propia interfaz y logica, pero el usuario puede volver al menu principal sin cerrar
la aplicacion completa.

Los modulos disponibles son:

- Matrices individuales.
- Operaciones vectoriales.
- Ecuaciones matriciales (incluye Tabla de Intercambio, Flujo de Red y Matrices
  Particionadas).
- Ecuaciones lineales e independencia lineal.
- Calculo de limites.
- Sistemas numericos.
- Determinantes y factorización LU.
- Métodos numéricos: Bisección, Regula Falsi, Métodos Abiertos (Newton-Raphson y
  Secante) y Análisis de Errores. Se describen en
  [docs/ExpoNoviembre3del2026.md](docs/ExpoNoviembre3del2026.md).

### Resultados exactos y aproximaciones

- **Matrices individuales, Sistemas y Determinantes** trabajan con
  `fractions.Fraction`. Valores como `1/3` o `0.1` se calculan de forma exacta, y un
  pivote se considera nulo solo si vale exactamente 0. El formato «Fracciones» muestra
  el valor exacto; el formato «Decimales» muestra hasta 6 decimales y usa notación
  científica antes que mostrar `0` para un valor que no es cero.
- Las herramientas que reciben datos en punto flotante (Flujo de Red, Leontief y
  algunas operaciones vectoriales) usan una tolerancia de `1e-9` y sus resultados
  son aproximados.
- **Límites** es una estimación numérica: evalúa f(x) en 12 puntos por lado cada vez
  más cercanos y muestra la tabla. Informa si la función tiende a un valor, si diverge
  a ±∞, si los límites laterales son distintos o si no se pudo determinar. No es una
  demostración simbólica.
- **Newton-Raphson y Secante** solo declaran convergencia por residuo cuando además
  verifican un cambio de signo cerca de la aproximación. Así, `exp(x)` no se reporta
  como si tuviera una raíz.
- **Sistemas numéricos** lee los números con `int` o `Decimal`, de modo que los enteros
  grandes, de hasta 300 dígitos, se convierten sin error.
- El evaluador de expresiones (`2x`, `x^2`, `sin(x)`, `sqrt(x)`, etc.) analiza el texto
  con `ast` y solo admite números, `x`, `pi`, `e`, las operaciones básicas y una lista
  cerrada de funciones. Nunca usa `eval` ni `exec`.

### Consolas de resultados y zoom

Los procedimientos y resultados aparecen en consolas monoespaciadas de solo lectura
(se puede seleccionar y copiar con Ctrl+C). Cada consola tiene su propio zoom, de 50 %
a 200 % en pasos de 10:

| Acción | Control |
|---|---|
| Aumentar | Ctrl + rueda hacia arriba, Ctrl + `+`, Ctrl + `+` del teclado numérico o botón `+` |
| Disminuir | Ctrl + rueda hacia abajo, Ctrl + `-`, Ctrl + `-` del teclado numérico o botón `−` |
| Restablecer a 100 % | Ctrl + `0` o clic en el porcentaje |

El zoom solo afecta a esa consola: no cambia las entradas ni otras ventanas, y no vuelve
a calcular. Se conserva mientras la ventana está abierta (también al cambiar de panel en
Métodos Numéricos) y vuelve a 100 % al cerrarla.

Sobre cada consola también están **Copiar resultados**, que copia todo el texto y
muestra «✓ Copiado» unos segundos, y **Limpiar resultados**, que borra solo la
consola. Ninguno de los dos recalcula ni cambia el zoom.

### Navegación, ayuda y ejemplos

- Cada calculadora tiene arriba una barra con **← Volver** (al menú, o a Ecuaciones
  matriciales desde Leontief, Flujo de Red y Particiones), **? Ayuda** y, donde aporta
  valor, **Cargar ejemplo**.
- «Volver» y la X de la ventana hacen lo mismo. Si el usuario escribió datos que siguen
  en pantalla, se pide confirmación; si no hay cambios, se sale sin preguntar.
- **? Ayuda** abre una sola ventana por herramienta. Explica para qué sirve, qué datos
  introducir, los formatos admitidos, un ejemplo, las restricciones, cómo leer la
  salida y los atajos de teclado. Se cierra con «Cerrar» o Esc. El contenido está en
  `core/ui/ayuda.py`.
- **Cargar ejemplo** llena los campos con un caso válido, pero no calcula. Si ya había
  otros datos, pide confirmación antes de reemplazarlos. Está disponible en Matrices,
  Sistemas, Límites, Sistemas numéricos, Determinantes, Bisección, Regula Falsi y
  Métodos Abiertos.
- Los botones de limpieza usan nombres consistentes: «Limpiar entradas», «Limpiar
  resultados» (en la consola) y «Limpiar todo» (Ecuaciones matriciales).
- Al pulsar Tab, el campo activo se resalta con un borde rojo. Si falta un dato o es
  inválido, el campo se marca en ámbar, recibe el foco y la consola explica el
  problema con «⚠».

### Bienvenida y preferencias

- La primera vez que aparece el Dashboard en cada sesión se muestra una guía de 4
  pasos (Anterior, Siguiente, Omitir, Finalizar y «No mostrar al iniciar»). Se puede
  abrir de nuevo desde **Ayuda › Guía de bienvenida** en el menú del Dashboard.
- En el Dashboard, «Música de fondo» y «Efectos de sonido» activan o silencian el audio
  de forma independiente.
- Las preferencias se guardan en `%APPDATA%\HeyAlgb\preferencias.json`, nunca dentro
  del repositorio. Si el archivo falta o está dañado, la aplicación inicia con los
  valores predeterminados. Para pruebas se puede usar otra carpeta con la variable de
  entorno `HEYALGB_CONFIG_DIR`.

Las calculadoras se abren desde el Dashboard en ventanas secundarias. Mientras el
usuario captura datos, las vistas de matrices, vectores, ecuaciones matriciales y
sistemas muestran una previsualización de la estructura que se está construyendo.

### Previsualizaciones

- **Matrices individuales:** muestra la matriz aumentada `[A | b]` mientras se capturan
  los coeficientes.
- **Operaciones vectoriales:** muestra los vectores `u` y `v` con sus componentes actuales.
- **Ecuaciones matriciales:** muestra la estructura `A`, `X` y `B` de la ecuación `AX = B`.
- **Sistemas lineales:** muestra las ecuaciones con sus variables, términos independientes
  y bordes visuales `┌`, `│` y `└`.

Las previsualizaciones se actualizan con cada cambio de los campos y utilizan `_` para
representar valores todavía vacíos.

### Sistemas numéricos

El conversor incluye dos operaciones:

- **Decimal → otra base:** convierte a binario, octal o hexadecimal mediante divisiones
  sucesivas para la parte entera y multiplicaciones sucesivas para la parte fraccionaria.
  Al final muestra los residuos en orden inverso para formar el resultado.
- **Otra base → Decimal:** convierte desde binario, octal o hexadecimal mediante
  descomposición polinómica. La salida muestra los términos con potencias de la base,
  sus valores calculados y la suma final.

Estas conversiones están implementadas con Python estándar, sin NumPy, SciPy, SymPy ni
`math`.

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

1. `main.py` crea la ventana raiz de Tkinter y muestra la pantalla de inicio
   (`vista_inicio.py`). Al elegir «INICIAR» (clic, tecla 1 o Enter), una transición roja y blanca da paso al
   `Dashboard`.
2. El Dashboard muestra una tarjeta para cada calculadora disponible.
3. Al seleccionar una tarjeta, el Dashboard actualiza la barra de estado y se oculta
  temporalmente mediante `withdraw()`.
4. El controlador importa y crea la vista correspondiente como una ventana secundaria
  (`Toplevel`). La importacion dentro del controlador permite cargar cada modulo al
  utilizarlo.
5. El Dashboard conserva una referencia a la ventana activa. Esto evita abrir dos
   calculadoras por una doble pulsacion y evita que la destruccion de un widget interno
   se confunda con el cierre de la ventana completa.
6. Al cerrar la calculadora, su metodo `al_cerrar()` vuelve a mostrar el Dashboard con
   `deiconify()` y destruye solamente la ventana secundaria.
7. Al elegir `Archivo > Salir`, se desregistran las fuentes temporales y se cierra la
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
  ui/                   Inicio, Dashboard, ventanas de cada calculadora, tema y audio
  vectores/             Operaciones, conversiones y validaciones vectoriales
  lineal/               Eliminacion y resolucion de sistemas lineales (exacta con Fraction)
  matriciales/          Operaciones con matrices y ecuaciones matriciales
  limites/              Estimacion numerica de limites y evaluador seguro de expresiones
  sistemas/             Gauss-Jordan, Cramer, LU e independencia lineal
  sistemas_numericos/   Conversiones y operaciones entre bases numericas
  determinantes/        Determinantes y factorizacion LU
  metodos_numericos/    Biseccion, Regula Falsi, Newton-Raphson, Secante y errores
  assets/               Fondos, iconos, fuentes y audio (ver docs/RECURSOS_Y_LICENCIAS.md)
tests/                  Pruebas automatizadas (unittest)
docs/                   Estudios de UI/UX, guias de exposicion y documentacion de modulos
```

La interfaz se mantiene separada de la logica matematica. Por ejemplo, `vista_vector.py`
se encarga de recibir datos y mostrar resultados, mientras que los modulos dentro de
`core/vectores/` realizan las conversiones y operaciones. Esta separacion facilita
probar o reutilizar la logica sin depender directamente de los widgets.

Vistas principales dentro de `core/ui/`:

- `dashboard.py`: menú principal, tarjetas, navegación y control de la ventana activa.
- `vista_matriz.py`: resolución de sistemas de ecuaciones lineales con matriz aumentada.
- `vista_vector.py`: operaciones entre vectores y conversiones de formato.
- `vista_matricial.py`: productos matriz-vector, operaciones matriciales, ecuaciones
  matriciales, tabla de intercambio y flujo de red.
- `vista_sistemas.py`: sistemas `Ax = b` e independencia lineal.
- `vista_limites.py`: evaluación de límites y continuidad.
- `vista_numerica.py`: conversión entre bases numéricas y procedimiento detallado.
- `vista_determinantes.py`: determinantes (Sarrus, cofactores, LU) y evaluación previa
  de eficiencia.
- `vista_metodos_numericos.py`: contenedor de Bisección (`vista_biseccion.py`), Regula
  Falsi (`vista_regla_falsa.py`), Métodos Abiertos (`vista_metodos_abiertos.py`) y
  Análisis de Errores (`vista_errores.py`), con el explorador gráfico
  `vista_grafica_biseccion.py` y el teclado matemático `teclado_matematico.py`.
- `vista_inicio.py`: pantalla de inicio, créditos y ayuda.
- `tema.py`: colores y estilos compartidos; `zoom_resultados.py`: consolas de
  resultados con zoom; `audio_manager.py`: música y efectos (si `pygame` o el
  dispositivo de audio fallan, la aplicación sigue en silencio).

## Características de las operaciones vectoriales

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

Dependencias y uso real en el código:

| Paquete | Se usa en |
|---|---|
| `customtkinter` | Controles visuales de las calculadoras |
| `Pillow` | Fondos, iconos e imágenes del inicio y del Dashboard |
| `prettytable` | Tablas de Matrices individuales (`vista_matriz.py`) |
| `pygame` | Música y efectos de sonido (`audio_manager.py`) |
| `numpy` | Análisis de Errores: épsilon, overflow/underflow, número de condición e inversa de referencia (`operaciones_errores.py`, `verificacion_matriz.py`) |
| `matplotlib` | Explorador gráfico de Métodos Numéricos (`vista_grafica_biseccion.py`) |
| `scipy` | Figura en `requirements.txt`, pero **hoy no se importa en ningún módulo** |

La lógica de álgebra lineal, límites y sistemas numéricos usa Python estándar: listas,
`ast`, `fractions.Fraction`, `decimal.Decimal` y `math`. No se usa SymPy. NumPy se
limita a la sección de Análisis de Errores, donde sirve para contrastar el punto
flotante con el cálculo exacto.

## Verificación rápida

Ejecuta la suite de pruebas desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Las pruebas cubren determinantes, sistemas, particiones, la exactitud de `core/lineal`,
límites, sistemas numéricos, el evaluador de expresiones, los métodos numéricos y el
zoom de las consolas. Algunas pruebas crean ventanas de Tk fuera de la pantalla y
requieren un escritorio de Windows activo; sin pantalla se omiten.

Para comprobar solamente que todo el código compila:

```powershell
.\.venv\Scripts\python.exe -m compileall -q main.py core
```

Los mensajes técnicos de errores inesperados se envían al módulo `logging` (registros
`heyalgb.*`), no a la ventana. El estudiante ve un mensaje claro.

## Recursos incluidos

- `core/assets/BordesFinales.png`: fondo decorativo principal del Dashboard.
- `core/assets/*ICON.png` y `*CON.png`: iconos de las calculadoras del Dashboard.
- `core/assets/fonts/`: fuentes utilizadas por la interfaz.

- `core/assets/SoundEffects/`: música y efectos de sonido.

Las fuentes deben conservarse junto con el proyecto. El inventario completo, con la
licencia o el origen que declara cada archivo, está en
[docs/RECURSOS_Y_LICENCIAS.md](docs/RECURSOS_Y_LICENCIAS.md). Hallazgos principales:

- El audio está etiquetado como parte de la banda sonora y los sonidos de sistema de
  Persona 5.
- `HelveticaNowDisplay-Bold.ttf` (Monotype) y `Democratica Bold.ttf` (Emigre) son
  fuentes comerciales.
- Las demás fuentes son SIL OFL 1.1 y requieren incluir el texto de la licencia.

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
