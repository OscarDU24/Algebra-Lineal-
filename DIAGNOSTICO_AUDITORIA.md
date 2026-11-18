# Diagnóstico de auditoría · HeyAlgb

Fecha: 2026-11-18 · Rama: `main` (último commit `cc90831`) · Alcance: Paso 1 (diagnóstico, sin modificar código).

Convenciones de este documento:

- **[Comprobado]**: verificado ejecutando código o pruebas en esta sesión.
- **[Leído]**: confirmado leyendo el código; no se ejecutó.
- **[Documentado]**: afirmación de la documentación del repositorio que no se verificó o que contradice el código.
- **[Pendiente]**: requiere comprobación manual (por ejemplo, abrir la interfaz o probar en otro equipo).

Durante este diagnóstico **no se editó ningún archivo fuente ni se instalaron dependencias**. Las pruebas se ejecutaron con `-B` para no generar `__pycache__`. Los scripts de sondeo se guardaron fuera del repositorio.

---

## 0. Punto de partida

### Instrucciones del repositorio

- No hay `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md` ni configuración `.claude/`. Las únicas guías son `README.md`, `TODO.MD` y `docs/`.
- Los tres documentos de referencia solicitados existen y se leyeron:
  `docs/estudio-ui-ux-heyalg.md`, `docs/pendientes-ui-ux.md` y `docs/ExpoNoviembre3del2026.md`.
  También existen `docs/ExposicionDelJueves15.md`, `docs/calculadora-*.md`, `docs/matrices-particionadas.md`, `docs/operaciones-matriciales.md` y `docs/explicacion-logica-y-cambios.txt`; no se revisaron a fondo.

### Cambios sin commit de otro colaborador (se conservan)

`git status` muestra dos archivos modificados y no confirmados. **No se tocaron.**

| Archivo | Cambio en curso |
|---|---|
| `core/ui/vista_metodos_abiertos.py` | Selector «Usar el punto en: x0 / x1» para Secante; `on_x_selected` ahora escribe en el campo elegido; `mostrar_marcas_raices=True`. |
| `core/ui/vista_grafica_biseccion.py` | Texto «…como punto inicial en el método actual». |

Estos cambios afectan directamente a Métodos Abiertos; ver hallazgo **I-1**. Antes de modificar estos archivos conviene confirmar con el autor si el cambio está terminado.

---

## (a) Estado actual del repositorio

### a.1 Arquitectura, punto de entrada y ejecución

- **Entrada:** `main.py` crea una raíz `tk.Tk` (no `ctk.CTk`), instala el `AudioManager`, muestra `VistaInicio` (canvas + wipe con `after()`) y, al terminar, construye `Dashboard`. **[Leído]**
- **Dashboard** (`core/ui/dashboard.py`): Tkinter clásico sobre `Canvas`, 8 tarjetas, `withdraw()` al abrir un módulo, `deiconify()` y música del lobby al recibir `<Destroy>` de la ventana activa. Evita la doble apertura con `ventana_activa`. **[Leído]**
- **Calculadoras:** `CTkToplevel` hijas de la raíz: `VistaMatriz`, `VistaVector`, `VistaMatricial` (abre a su vez `VistaIntercambio`, `VistaFlujoRed` y `VistaParticiones`, esta última modal con `grab_set`), `VistaSistemas`, `VistaLimites`, `VistaSistemasNumericos`, `VistaDeterminantes` y `VistaMetodosNumericos`. Esta última funciona como contenedor de 4 `CTkFrame` (Bisección, Regula Falsi, Métodos Abiertos y Errores) que conservan su estado. **[Leído]**
- **Auxiliares:** `VistaGraficaBiseccion` (matplotlib embebido) y `teclado_matematico`. **[Leído]**
- **Ejecución:** `.\.venv\Scripts\python.exe main.py` (README). El `.venv` local existe y usa Python 3.13.5. **[Comprobado]**
- **Pruebas:** `python -m unittest discover -s tests` → **80 pruebas, OK** en 0.04 s. **[Comprobado]**
  `discover -s tests -t .` falla porque `tests/` no tiene `__init__.py`. No hay pytest.

### a.2 Dependencias y recursos

| Paquete (requirements.txt) | Uso real |
|---|---|
| customtkinter 6.0.0 | Todas las calculadoras. |
| Pillow 12.3.0 | Imágenes de inicio, Dashboard e iconos. |
| prettytable 3.18.0 | Solo `vista_matriz.py`. |
| pygame 2.6.1 | Solo `audio_manager.py` (mixer). |
| numpy | `operaciones_errores.py`, `verificacion_matriz.py`, `vista_errores.py`. |
| matplotlib | Solo `vista_grafica_biseccion.py`. |
| **scipy** | **No se importa en ningún archivo de `core/` ni `tests/`.** [Comprobado con grep] `ExpoNoviembre3del2026.md` afirma que SciPy ofrece una bisección para contrastar resultados. Esa afirmación está desactualizada o la integración se retiró. No se recomienda eliminar SciPy sin confirmarlo con el equipo. |

- El README afirma «No se utilizan NumPy, SciPy ni SymPy» y que «La aplicación no incluye todavía una suite automatizada de pruebas». **Ambas afirmaciones son falsas en el estado actual.** El README tampoco menciona los módulos de Determinantes ni Métodos Numéricos. **[Comprobado]**
- **Recursos:** 13 fuentes, 7 MP3 y 17 PNG/ICO en `core/assets/`. Las rutas se resuelven con `Path(__file__)`. **[Leído]**
- **Licencias [Pendiente, riesgo alto para distribución]:**
  - No hay archivos de licencia para fuentes, audio ni imágenes.
  - `HelveticaNowDisplay-Bold.ttf` es una familia comercial de Monotype. No debe distribuirse sin licencia.
  - Anton, Oswald, Archivo Black, Abril Fatface, Alfa Slab One, Playfair, League Spartan, Arsenal, Caprasimo y Tinos parecen fuentes de Google Fonts con licencia OFL o Apache. La OFL exige incluir el texto de la licencia.
  - Se desconoce el origen de `Democratica Bold`, `UltraCondensedSansSerif`, de los MP3 y de los avatares. Los avatares (`Liang_Amamiya.png`, `Oscar_Sakamoto.png`, `Diego_Kitagawa.png`, `Charly_Sakura.png`) usan apellidos de personajes de Persona 5. Hay que confirmar que son ilustraciones propias y no derivadas de arte oficial.

### a.3 Operaciones implementadas (según el código)

| Módulo (vista → lógica) | Operaciones | Aritmética |
|---|---|---|
| Matrices individuales `vista_matriz` → `core/lineal` | Sistemas `[A\|b]` por escalonado, Gauss y Gauss-Jordan; inversa | **float** con tolerancia 1e-9; «fracciones» solo como formato de salida |
| Vectores `vista_vector` → `core/vectores` | Operaciones básicas, geometría e independencia | Fraction/float según el formato |
| Ecuaciones matriciales `vista_matricial` → `core/matriciales`, `core/vectores` | A·u, propiedades, transpuesta, cA, inversa, Ax=b, Leontief, flujo de red y particiones | Mixta |
| Sistemas `vista_sistemas` → `core/sistemas` | Gauss-Jordan, Cramer, LU e independencia | **Fraction exacta** [Comprobado: singularidad, Cramer con D=0 y LU con intercambio funcionan] |
| Determinantes `vista_determinantes` → `operaciones_determinantes` | Determinante por varios métodos y LU | Fraction |
| Límites `vista_limites` → `core/limites` | Límite numérico (bilateral, izquierda o derecha, ±∞) | float, series propias |
| Sistemas numéricos `vista_numerica` → `core/sistemas_numericos` | Decimal ↔ base 2/8/16 y números romanos | float/int |
| Métodos numéricos → `core/metodos_numericos` | Bisección, Regula Falsi, Newton-Raphson, Secante, errores, propagación, truncamiento, punto flotante y Hilbert | float; Hilbert exacto con Fraction |

**Código muerto o duplicado [Comprobado con grep: nadie lo importa]:**
- `core/biseccion/biseccion.py`, que duplica la versión de `metodos_numericos`.
- `core/determinantes/{operacionesDeterminantes, cramerDeterminantes, visualizacionDeterminantes, verificacionDeterminantes}.py`, que suman unas 1 870 líneas y solo se importan entre sí.
- `core/lineal/entrada.py` y `core/matriciales/entradaMatriciales.py`, que leen datos por consola con `input()`.

### a.4 Separación cálculo / interfaz

En general se respeta: las vistas leen campos, llaman a la lógica y escriben texto. Hay tres excepciones:
- Las vistas `vista_matricial.py` (1056 líneas) y `vista_vector.py` (1166) contienen formateo y parte de la lógica de presentación.
- `core/limites/operaciones_limites.py` devuelve texto ya formateado, incluidos los mensajes de error. Por eso no se puede distinguir un error de un resultado sin analizar el texto.
- `audio_manager.reproducir_sonido_error` decide si hubo error según si el texto empieza con «error» o «advertencia».

### a.5 Pruebas y empaquetado

- Pruebas existentes: determinantes, métodos numéricos (Bisección, Regula Falsi, Newton, Secante, errores y Hilbert), particiones, sistemas, `vista_inicio` (sin Tk) y validación de `vista_matricial`.
- **Sin pruebas:** límites, el evaluador de expresiones con argumentos grandes, `core/lineal` (vista Matrices individuales), vectores, sistemas numéricos y Leontief o flujo de red.
- **Empaquetado:** no existe ningún `.spec`, script de compilación ni instrucciones. `.gitignore` ya ignora `build/` y `dist/`. Para PyInstaller habría que declarar `core/assets` como datos y verificar que `Path(__file__)` resuelve dentro del paquete. **[Pendiente]**

---

### a.6 Problemas confirmados

#### Bloqueantes (exactitud o congelamiento)

**B-1. Congelamiento total con trigonométricas de argumento grande. [Comprobado]**
- `core/limites/operaciones_limites.py:14-19`: `_reducir_angulo` resta 2π dentro de un `while`.
- Con `sin(1e300)` el bucle no termina nunca, porque `1e300 - 2π == 1e300`. El proceso quedó colgado hasta que lo cortó un `timeout` de 8 s. `_reducir_angulo(1e8)` tarda 0.4 s por evaluación.
- El evaluador es compartido: lo usan Bisección, Regula Falsi, Newton, Secante, Propagación, la gráfica (que hace 800 evaluaciones por actualización) y Límites. Todo corre en el hilo de Tk, así que una entrada como `sin(1e9x)` congela la ventana sin posibilidad de cancelar.

**B-2. `sqrt` y `exp` propios devuelven valores incorrectos. [Comprobado]**
- `_raiz_cuadrada` (`operaciones_limites.py:42-50`) hace solo 30 iteraciones de Newton empezando en `valor`:
  - `sqrt(1e20)` da `9.35e10` en lugar de `1e10`.
  - `sqrt(1e300)` da `9.3e290`.
- `_exponencial` (`:53-63`) trunca la serie a 60 términos: `exp(50)` tiene un **error relativo del 9.2 %**. `exp(20)` y `ln` son correctos.
- `sin(100)` tiene un error de 3e-14, que es aceptable.
- Decisión requerida: el README dice que Sistemas Numéricos no usa `math`, y Límites dice usar «únicamente Python estándar». `math` es biblioteca estándar. Hay que confirmar si existe una restricción académica de no usar `math`. Si no existe, la corrección es directa. Si existe, se deben implementar una reducción de argumento con `math.fmod` equivalente (o `Fraction`/`divmod`), una semilla por exponente y una reducción `exp(x) = exp(x/2^k)^(2^k)`.

**B-3. «Fracciones» en Matrices individuales muestra valores falsos. [Comprobado]**
- `core/lineal/conversiones.py:47` usa `Fraction(entrada).limit_denominator(1000)`:
  - `0.0004` se muestra como **`0`**.
  - `1/1001` se muestra como `1/1000`.
- La interfaz presenta esas aproximaciones como fracciones exactas. Además, `vista_matriz.py:282` convierte toda la entrada a `float` (`convertir_a_decimal`), así que el cálculo nunca es exacto aunque el usuario escriba `1/3`.

**B-4. Las rutas «exactas» con `Fraction` usan tolerancias de punto flotante. [Comprobado]**
- `core/lineal/eliminacion.py:4, 66-75, 107-126`: convierte el `Fraction` a float y compara con `1e-9`. Un pivote exacto `1/10^10` se considera cero. Con `[[1/10^10 | 1]]` no se detecta pivote, cuando `x = 10^10` es una solución válida. Esta función la usan `solucionMatriciales`, `flujo_red`, `intercambio`, `eliminacionVectores` y `lineal/solucion`.
- `core/lineal/solucion.py:6-29` (`invertir_matriz_gauss_jordan`) tiene dos problemas:
  1. Añade la identidad como `1.0/0.0`, de modo que **la inversa de una matriz de `Fraction` sale en `float`** (comprobado con `[[1,2],[3,4]]`).
  2. Rechaza como singular un pivote exacto `1/10^12`.
  Esta función la usa `particiones_gui.py:359`, que trabaja con `Fraction`.
- En contraste, `core/sistemas/operaciones_sistemas.py` resuelve el mismo caso `1/10^13` correctamente. Es la referencia a seguir.
- Regla para la corrección: si todos los datos son `Fraction`, comparar `== 0`. Si son float, usar una tolerancia **relativa** a la escala de la columna y advertir que el resultado es aproximado.

**B-5. Límites: resultados numéricos presentados como límites. [Comprobado]** (`operaciones_limites.py:180-235`)
- `lim 1/x²` cuando x→0 se reporta como `100000000000000.02` en lugar de indicar que diverge a +∞.
- `lim x` cuando x→∞ se reporta como `1000000.00`.
- El resultado siempre se redondea a 2 decimales: `lim x²` cuando x→1e-5 se reporta como `0.00`.
- `lim 1/x` en 0 (bilateral) muestra un error genérico de «sintaxis o dominio» en lugar de indicar que los límites laterales difieren.
- `10**10**10` produce `ERROR INTERNO: (34, 'Result too large')`.
- Este evaluador no limita la profundidad ni los exponentes, a diferencia de `_crear_funcion`. No permite ejecutar código, porque `_evaluar_arbol` solo interpreta nodos conocidos, pero sí acepta cálculos costosos (B-1).

**B-6. Sistemas numéricos: enteros grandes convertidos con error. [Comprobado]**
- `operaciones_numericas.py:205` (`parsear_decimal`) hace `float(cadena)`. El número `999…9` de 30 dígitos se convierte a binario como si fuera `1000000000000000019884624838656`: el resultado termina en ceros cuando debería ser impar.
- Afecta a cualquier entero mayor que 2⁵³.
- Los números de 400 dígitos se rechazan como «no finitos», lo cual es una protección, pero el mensaje es engañoso.

#### Importantes (uso y estabilidad)

**I-1. Métodos Abiertos con el cambio en curso. [Leído]**
- Si el usuario elige `x1`, cambia a Newton y luego hace clic en la gráfica, el valor se escribe en `x1`, que está oculto. El usuario no ve ningún efecto. `destino_grafica_var` no se reinicia en `_cambiar_metodo`.
- `selector_destino_grafica.pack(side="left")` se vuelve a empaquetar al final de la fila, detrás de «Borrar» o «Forzar cálculo». El orden visual varía.
- La leyenda de la gráfica sigue diciendo `x0 = …` (`vista_grafica_biseccion.py:239`) aunque el destino sea `x1`.
- `ExpoNoviembre3del2026.md` dice que la gráfica de Métodos Abiertos **no** muestra marcadores. El cambio activa `mostrar_marcas_raices=True` (cruces de raíz candidata), y la documentación queda desactualizada.
- **[Documentado, no implementado]:** el contexto recibido indica que en Secante «el backend puede generar el segundo punto». `resolver_secante` exige ambos puntos y no existe ningún generador. Lo implementado es el selector manual x0/x1.

**I-2. Newton: criterio de convergencia por residuo absoluto. [Comprobado]**
- Con `exp(x)`, `x0 = 0` y «Forzar cálculo», el método reporta **«Convergió: Sí»** con la raíz `-18.99999…`, aunque `exp(x)` no tiene raíces. Basta con que `|f| ≤ 1e-8`.
- Con `x²` forzado, la «raíz» es `6.1e-5` (error 6000 veces mayor que la tolerancia).
- Sin forzar, el preanálisis detiene el cálculo en `x²` porque no detecta el cero tangencial. Esto está documentado como diseño.
- Propuesta: reportar «residuo pequeño, pero sin cambio de signo verificado» y diferenciar el estado; no se propone cambiar el algoritmo.

**I-3. Los mensajes de validación útiles se pierden. [Comprobado]**
- `biseccion.py:116-119` envuelve cualquier `ValueError` en el texto genérico «sintaxis u operaciones no permitidas».
- Por ejemplo, «Los exponentes deben ser constantes con valor absoluto ≤ 1000» o «La función es demasiado compleja» nunca llegan al estudiante.
- En `evaluar`, los dominios se reportan como «Error de valor numérico», por ejemplo en `sqrt(-1)` o `(-8)^(1/3)`.

**I-4. Ventanas secundarias de Ecuaciones matriciales. [Leído]**
- `vista_matricial.py:951-972` hace `self.withdraw()` **antes** de construir `VistaIntercambio`, `VistaFlujoRed` o `VistaParticiones`.
- Si el constructor falla, `accion_calcular` captura la excepción (`except Exception`, línea 1025) y escribe el error en una ventana oculta. Como el Dashboard también está oculto, **la aplicación queda sin ninguna ventana visible**.

**I-5. Consolas de resultados inconsistentes. [Leído]**
- Las de `vista_matricial.py:296`, `vista_flujo_red.py:67` y `vista_intercambio.py:80` **no definen fuente**. Usan la de CustomTkinter, que es proporcional, así que las matrices pierden la alineación. **[Pendiente: confirmar visualmente]**
- `vista_matriz` y `vista_vector` usan Courier New; el resto usa Consolas.
- Solo Bisección, Regula Falsi y Métodos Abiertos usan `wrap="none"`. En las demás, las filas largas se parten y descuadran.
- Casi todas son editables: el usuario puede escribir sobre el resultado. Solo `vista_matriz`, `vista_vector` y `texto_eficiencia` alternan a `disabled`.

**I-6. Cálculos síncronos en el hilo de Tk. [Leído]**
- No hay hilos en el proyecto, lo cual es correcto para casi todo.
- La gráfica muestrea dos veces (`muestrear_funcion` + `analizar_intervalos`, 800 evaluaciones) y, si `marcar_raices_reales` está activo, ejecuta bisecciones adicionales. Sumado a B-1, puede bloquear la interfaz.
- Recomendación: corregir B-1 antes de considerar hilos y reutilizar el muestreo. **No** se propone introducir hilos.

**I-7. Ciclo de vida. [Leído]**
- El wipe de `vista_inicio.py:836-839` encadena `after()` sin guardar los identificadores. Si se cierra la raíz durante el wipe (unos 200 ms), aparecen `TclError` en la consola. El impacto es bajo.
- `Dashboard._abrir_ventana` vuelve a lanzar la excepción tras restaurar el Dashboard. El usuario no ve ningún mensaje y la traza solo va a la consola.
- El historial no crece sin límite: cada consola se reescribe con `delete` + `insert`.
- **No se encontró doble ejecución peligrosa:** el Dashboard bloquea la doble apertura y los cálculos son síncronos.

**I-8. Registro de diagnóstico. [Leído]**
- Todo el diagnóstico usa `print()`. Si la aplicación se lanza con `pythonw` o como ejecutable empaquetado, esa información se pierde.
- Cuatro `except Exception` muestran `str(error)` en crudo: `vista_matricial.py:1025`, `vista_sistemas.py:314`, `operaciones_limites.py:234` y `biseccion/biseccion.py` (código muerto).

**I-9. Documentación desactualizada. [Comprobado]**
- README: menciona NumPy, SciPy y la ausencia de pruebas; omite dos módulos; su comando de `py_compile` solo cubre 8 de los 22 archivos de `core/ui`.
- `ExpoNoviembre3del2026.md`: menciona SciPy y la ausencia de marcadores en Métodos Abiertos.

#### Acabado visual (resumen; detalle en la sección c)

- Títulos de ventana distintos: `main.py` usa «HeyAlgb · Álgebra Lineal» y el Dashboard lo reemplaza por «Calculadora de Álgebra Lineal - FIA UAM».
- Fuentes codificadas en cada vista: Segoe UI, Impact y Arial, aunque existen `FUENTE_*` en `tema.py`.
- `tema.py` no define colores para los estados de foco, deshabilitado y error.

### a.7 Riesgos no verificables en esta sesión

- **No se abrió la interfaz gráfica.** Quedan sin verificar con capturas: la apariencia, el escalado de Windows (125 %/150 %), la resolución mínima y el audio.
- Pendientes de verificar con un teclado físico: la ruta de `<MouseWheel>` en Windows con Tk 8.6 (si el evento llega al widget bajo el puntero o al que tiene el foco), los keysyms de `+` en un teclado español (`plus`) frente a uno estadounidense (`equal` + Shift) y `KP_Add`.
- Las licencias de los recursos (a.2).
- Comportamiento de `pygame.mixer` en equipos sin dispositivo de audio. El código contempla el fallo y cae en silencio.

---

## (b) Plan exacto del zoom

### b.1 Inventario de consolas de resultados [Leído]

Todas son `ctk.CTkTextbox` con texto plano: **sin tags, imágenes ni fórmulas renderizadas**. La gráfica de matplotlib queda fuera del alcance.

| # | Archivo:línea | Atributo | Fuente actual | wrap | Solo lectura |
|---|---|---|---|---|---|
| 1 | `vista_matriz.py:164` | `txt_resultados` | Courier New 12 | char | Sí |
| 2 | `vista_vector.py:258` | `txt_resultados` | Courier New 12 | char | Sí |
| 3 | `vista_matricial.py:296` | `texto_resultado` | **ninguna** | char | No |
| 4 | `vista_intercambio.py:80` | `texto_resultado` | **ninguna** | char | No |
| 5 | `vista_flujo_red.py:67` | `texto_resultado` | **ninguna** | char | No |
| 6 | `particiones_gui.py:132` | `texto_resultado` | Consolas 12 | char | No |
| 7 | `vista_sistemas.py:267` | `texto_resultado` | Consolas 14 | char | No |
| 8 | `vista_limites.py:106` | `texto_resultado` | Consolas 14 | char | No |
| 9 | `vista_numerica.py:246` | `texto_resultado` | Consolas 14 | char | No |
| 10 | `vista_determinantes.py:135` | `texto_resultado` | Consolas 12 | char | No |
| 11 | `vista_determinantes.py:98` | `texto_eficiencia` | Consolas 12 | char | Sí |
| 12 | `vista_biseccion.py:118` | `texto_salida` | Consolas 11 | none | No |
| 13 | `vista_regla_falsa.py:117` | `texto_salida` | Consolas 11 | none | No |
| 14 | `vista_metodos_abiertos.py:163` | `texto_salida` | Consolas 11 | none | No |
| 15 | `vista_errores.py:50` | `_crear_salida` (5 pestañas) | Consolas 12 | char | No |

Quedan **fuera** del zoom:
- Las previsualizaciones de entrada (`txt_previsualizacion` en vista_matriz, vector, matricial y sistemas): son representación de entrada, no resultados.
- La entrada de matriz de `vista_errores.py:168`.
- La gráfica de matplotlib.

### b.2 Componente común propuesto

Se propone un archivo nuevo, `core/ui/zoom_resultados.py`, con un helper y una clase:

```text
ZoomConsola(textbox, controles_master=None, base=None)
  - Toma la fuente base una sola vez (familia, tamaño, peso) y crea un CTkFont propio.
  - nivel: entero en {50, 60, …, 200}; 100 = tamaño base de ESA consola.
  - tamaño = max(1, round(base * nivel / 100)), calculado siempre desde la base,
    nunca desde el tamaño anterior, para no acumular errores.
  - aumentar(), disminuir(), restablecer(), establecer(nivel)
  - destruir(): quita bindings y callbacks (se llama en <Destroy> del textbox).

crear_controles_zoom(master, zoom) -> CTkFrame con [−] [100 %] [+]
  - Clic en el porcentaje equivale a restablecer.
  - Los botones se deshabilitan en los límites; el texto muestra siempre el nivel aplicado.
  - Usa estilo_boton_secundario() de tema.py y no crea colores nuevos.
```

Y un helper de escritura `escribir_consola(textbox, texto)`: pone `state="normal"`, borra, inserta, vuelve a `state="disabled"` y conserva la posición de lectura cuando el contenido no cambia.

- **Fuente y DPI:** `CTkTextbox` ya aplica `_apply_font_scaling` y re-renderiza mediante el callback `add_size_configure_callback` cuando cambia el tamaño de un `CTkFont` (`customtkinter/.../ctk_textbox.py:69-71, 195-197`). Basta con cambiar `CTkFont.configure(size=…)`. El escalado DPI de CustomTkinter se respeta automáticamente y **no** se toca `set_widget_scaling`.
- **Alineación:** todas las consolas con zoom se fijan en una familia monoespaciada única (`FUENTE_RESULTADOS = "Consolas"`, ya presente en `tema.py`), con el tamaño base actual de cada una. Corrige I-5 para #3, #4 y #5. Como no hay tags ni fuentes múltiples, un solo `CTkFont` por consola escala todo el contenido de forma uniforme. Se verificará con una matriz y una tabla de iteraciones a 50 % y 200 %.
- **Desplazamiento:** las consolas que muestran matrices o tablas pasan a `wrap="none"`. `CTkTextbox` muestra la barra horizontal sola cuando `xview() != (0, 1)`. Para conservar la posición de lectura, antes del cambio se guarda el índice `textbox.index("@0,0")` y la fracción `xview()[0]`, y después se restauran con `yview(indice)` y `xview_moveto(fraccion)`.
- **Bindings (solo en el widget, nunca `bind_all`):** sobre `textbox._textbox` (el `tk.Text` interno) y sobre el marco de la consola:
  - `<Control-MouseWheel>`, que devuelve `"break"` para que no lo procese el scroll de CTk ni el `bind_all` de `CTkScrollableFrame`.
  - `<Control-plus>`, `<Control-equal>` (teclado estadounidense) y `<Control-KP_Add>`.
  - `<Control-minus>` y `<Control-KP_Subtract>`.
  - `<Control-0>` y `<Control-KP_0>` / `<Control-KP_Insert>`.
  - La rueda sin Ctrl conserva el desplazamiento normal.
  - Para que el teclado funcione en consolas de solo lectura: `takefocus=1` y `focus_set()` al hacer clic. Ctrl+C sigue copiando la selección.
- **Persistencia:**
  - El nivel se guarda **por consola y mientras exista la ventana**.
  - En Métodos Numéricos, los paneles se conservan al cambiar de operación (`vista_metodos_numericos.py:67-88`), así que **el zoom se conserva al cambiar de panel** dentro de la misma ventana.
  - Al cerrar la calculadora se pierde.
  - No se guarda en disco en esta entrega.
- **Sin recálculo:** el zoom solo cambia la fuente. No llama a la lógica ni toca el historial.

### b.3 Archivos a modificar

- **Nuevo:** `core/ui/zoom_resultados.py`.
- **Adaptar, una línea de creación y la barra de controles en cada uno:** `vista_matriz.py`, `vista_vector.py`, `vista_matricial.py`, `vista_intercambio.py`, `vista_flujo_red.py`, `particiones_gui.py`, `vista_sistemas.py`, `vista_limites.py`, `vista_numerica.py`, `vista_determinantes.py`, `vista_biseccion.py`, `vista_regla_falsa.py`, `vista_errores.py`.
- `vista_metodos_abiertos.py`: **solo después de acordar con el autor** los cambios sin commit (I-1).
- Las funciones `mostrar_resultado` y `_mostrar` de cada vista se redirigen a `escribir_consola` para obtener la consola de solo lectura.
- **Nuevo:** `tests/test_zoom_resultados.py`.

### b.4 Pruebas y criterios de aceptación

Automáticas (unittest, con una raíz Tk oculta; se omiten si no hay pantalla):
- Los límites: 50 % y 200 % no se exceden; seis pulsaciones de `+` desde 150 % terminan en 200 %.
- `100 → 110 → 100` restituye exactamente el tamaño base (sin deriva).
- `Ctrl-0` restablece.
- El texto y la posición `@0,0` se conservan tras el zoom.
- El estado `disabled` se mantiene después de escribir.
- Ningún binding nuevo en `bind_all`; destruir la consola elimina sus callbacks.

Manuales (lista de aceptación):
- Ctrl + rueda solo actúa con el puntero sobre la consola; fuera de ella, el resto de la ventana no cambia.
- Las teclas `+` del teclado principal (español y estadounidense) y del teclado numérico funcionan.
- La matriz 4×4 y la tabla de Newton mantienen columnas y delimitadores alineados a 50 %, 100 % y 200 %.
- Aparece la barra horizontal a 200 %.
- La prueba se repite con el escalado de Windows al 100 % y 150 %.
- Entradas, Dashboard y otras ventanas no cambian de tamaño.

---

## (c) Mejoras priorizadas

### c.1 Bloqueantes de exactitud o ejecución

| ID | Cambio | Archivos | Depende de |
|---|---|---|---|
| B-1 | Reducción de argumento en tiempo constante y rechazo de argumentos con magnitud mayor que un límite documentado | `operaciones_limites.py` | Decisión sobre `math` |
| B-2 | `sqrt` y `exp` correctos en todo el rango de float | `operaciones_limites.py` | Decisión sobre `math` |
| B-5 | Límites: detectar divergencia o crecimiento, informar «límites laterales distintos», precisión de salida razonable y mismas restricciones de AST que `_crear_funcion` | `operaciones_limites.py`, `vista_limites.py` | B-1 |
| B-4 | Comparaciones exactas para `Fraction` y tolerancia relativa para float; identidad en `Fraction` cuando la entrada es exacta | `lineal/eliminacion.py`, `lineal/solucion.py` | — |
| B-3 | Matrices individuales: aceptar entrada exacta (`Fraction`) y no presentar aproximaciones como fracciones | `lineal/conversiones.py`, `vista_matriz.py` | B-4 |
| B-6 | Enteros sin pasar por float (`int`/`Decimal`) y mensaje claro al exceder el límite | `operaciones_numericas.py` | — |

Cada corrección incluirá pruebas de regresión con los casos de este documento.

### c.2 Importantes de uso y estabilidad

1. I-3: propagar el mensaje específico de validación y nombrar el dominio violado («raíz de número negativo», «log de no positivo»).
2. I-2: Newton y Secante con un estado diferenciado cuando la convergencia es solo por residuo, sin verificar cambio de signo.
3. I-4: construir la ventana secundaria **antes** de ocultar `VistaMatricial` y restaurarla si falla. Mensajes amigables en lugar de `str(error)` crudo, con un registro técnico mediante `logging` hacia un archivo de diagnóstico.
4. I-1: coordinar con el autor el selector x0/x1 (reiniciar el destino al cambiar a Newton, posición fija del selector, leyenda dinámica) y actualizar `ExpoNoviembre3del2026.md`.
5. I-6: reutilizar el muestreo de la gráfica (una sola pasada).
6. I-7: guardar y cancelar los identificadores `after()` del wipe.

### c.3 Acabado visual y distribución

- Usar `FUENTE_RESULTADOS` y añadir constantes para la fuente de controles y títulos en `tema.py`, en lugar de Segoe UI, Impact y Arial codificadas.
- Definir en `tema.py` los colores de foco, deshabilitado y error (sin crear una paleta paralela: variantes de `ACENTO` y `FONDO_PANEL`).
- Unificar el título de la raíz.
- Consolas de solo lectura y monoespaciadas (llega con el zoom).
- Revisar el ajuste en 1366×768 y con escalado del 150 %. Hoy hay geometrías fijas entre 980×780 y 1120×850 con mínimos de 760–850 px. **[Pendiente de captura]**
- Botón «Volver al menú» y estados Listo / Error, que ya figuran en `pendientes-ui-ux.md`. Solo si el equipo lo aprueba.

### c.4 Lanzamiento y documentación

- README: corregir dependencias, módulos, cómo ejecutar las pruebas (`python -m unittest discover -s tests`) y el comando de verificación.
- Inventario de licencias de recursos. Antes de distribuir, sustituir `HelveticaNowDisplay` si no hay licencia y confirmar el origen de audio y avatares.
- Decidir con el equipo si se eliminan el código muerto (a.3) y `scipy`.
- Empaquetado (PyInstaller): solo después de lo anterior.

### c.5 Dependencias entre cambios

```text
Decisión sobre math ─► B-1 + B-2 ─► B-5 ─► I-3
B-4 ─► B-3
Acuerdo con autor de I-1 ─► zoom en vista_metodos_abiertos
Zoom (helper) ─► consolas de solo lectura y fuente monoespaciada (I-5)
Licencias ─► empaquetado
```

---

## Primera entrega de implementación recomendada

**Entrega 1: evaluador de expresiones seguro y preciso (B-1 y B-2) con pruebas de regresión.**

Se recomienda empezar aquí porque es el único problema que **congela la aplicación** y porque el evaluador es compartido por siete herramientas, incluidas todas las de Métodos Numéricos que se presentarán. El cambio queda contenido en `core/limites/operaciones_limites.py` más un archivo de pruebas. No toca la interfaz ni los archivos con cambios sin commit, y se puede verificar por completo con unittest.

Contenido:
1. Reducción de argumento trigonométrica en tiempo constante y un límite explícito de magnitud con un mensaje para el estudiante.
2. `sqrt` y `exp` correctos en todo el rango de float.
3. Pruebas comparando con valores de referencia y una prueba con límite de tiempo para `sin(1e300)`.

**Decisión necesaria antes de empezar:** ¿se permite usar el módulo `math` de la biblioteca estándar en el motor matemático, o existe una restricción académica que obliga a implementar las funciones a mano?

Entregas siguientes sugeridas: (2) B-4 + B-3, exactitud de `Fraction`; (3) B-5 + B-6 + I-3; (4) zoom; (5) pulido visual y documentación.

---

## Estado de implementación

### Entrega 1 — B-1 y B-2 (2026-11-18) · completada, sin commit

- **Decisión:** se autorizó usar `math` de la biblioteca estándar.
- `core/limites/operaciones_limites.py`:
  - `sin`, `cos`, `sqrt`, `exp` y `log` delegan en `math`.
  - `_reducir_angulo` usa `math.remainder` y se ejecuta en tiempo constante.
  - Los argumentos trigonométricos no finitos producen `ValueError`.
  - `exp` desbordado devuelve `inf`, como antes, y Métodos Numéricos lo sigue reportando como «resultado no finito».
  - `PI` y `E` provienen de `math`; sus valores no cambian.
  - Se conservan los nombres de funciones, la tolerancia de indefinición de `tan`, `sec`, `csc` y `cot`, y los mensajes existentes.
- **Pruebas nuevas:** `tests/test_evaluador_expresiones.py` (12 casos). Una de ellas lanza `sin(1e300)` en un subproceso con límite de tiempo.
- **Verificación [Comprobado]:**
  - Suite completa: **92 pruebas OK**.
  - `sqrt(1e20)` = `1e10`; `exp(50)` con error relativo 0; `sin(1e300)` responde al instante.
  - Con la versión anterior del archivo, las pruebas nuevas se quedan colgadas, que es el defecto que corrige esta entrega.
- **Sin cambios todavía:** B-5 (cómo se presentan los límites); el resto de bloqueantes sigue pendiente.

### Entrega 2 — B-4 y B-3 (2026-11-18) · completada, sin commit

- **Regla común:** el nuevo `core/lineal/exactitud.py` define cuándo un cálculo es exacto: hay al menos un `Fraction` y ningún `float`. En modo exacto, los enteros se convierten a `Fraction` y un valor es cero solo si vale `0`. Con floats se conserva la tolerancia anterior (1e-9 en eliminación y 1e-10 en la inversa).
- **B-4:**
  - `eliminacion.py`, `clasificacion.py`, `verificacion.py`: comparaciones exactas en lugar de `abs(float(...)) < 1e-9`.
  - `solucion.py`:
    - `invertir_matriz_gauss_jordan` usa una identidad racional y comparaciones exactas, así que la inversa de una matriz de fracciones sale en `Fraction`.
    - `multiplicar_matrices` ya no fuerza `float`.
  - Las matrices solo de enteros siguen en punto flotante; así lo esperan `particiones` y sus pruebas.
- **B-3 (`vista_matriz.py` + `conversiones.py`):**
  - La entrada se lee con `convertir_a_racional`: `1/3`, `0.1` y `1e-3` quedan exactos, y `1/0`, `inf` y `nan` se rechazan.
  - El modo Fracciones ya no usa `limit_denominator(1000)`.
  - El modo Decimales muestra hasta 6 decimales y usa notación científica antes que mostrar `0` para un valor no nulo.
  - El sistema equivalente de Gauss usa el formato elegido.
  - La división de fila se escribe `F2 = F2 / (2/3)`.
- **Pruebas nuevas:** `tests/test_lineal_exactitud.py` (16 casos).
- **Verificación [Comprobado]:**
  - Suite completa: **106 pruebas OK**.
  - Se ejecutó `VistaMatriz` con una raíz Tk oculta y estos casos:
    - `0.0004x + y = 1, x + y = 2` → `x = 2500/2499`.
    - Inversa de `[[1,2],[3,4]]` exacta, con `A·A⁻¹ = I`.
    - `x/10¹⁰ + y = 1, y = 2` → determinado, `x = -10¹⁰`. Antes se declaraba sin pivote.
- **Cambios visibles para el usuario:**
  - El modo Decimales pasa de 2 a 6 decimales.
  - Las descripciones de pasos de la eliminación muestran fracciones exactas aunque se elija Decimales; esto queda pendiente para el pulido.
- **No incluido:** las vistas que usan `core/lineal` con floats (flujo de red, Leontief, combinación lineal de vectores) mantienen su tolerancia absoluta. Cambiarla a una tolerancia relativa queda pendiente.

### Entrega 3 — B-5, B-6 e I-3 (2026-11-18) · completada, sin commit

- **I-3 (`metodos_numericos/biseccion.py`, `_crear_funcion`):**
  - Los mensajes de validación ya no se reemplazan por el genérico. Ejemplos:
    - «`sin` es una función: escríbala con paréntesis».
    - «El nombre `y` no está permitido; use x, pi o e».
    - Límite de exponentes.
    - «error de sintaxis».
    - «estructura incompleta».
  - Los errores de dominio explican el motivo: raíz cuadrada de un negativo, logaritmo de un número no positivo, división entre cero, resultado complejo o valor demasiado grande.
  - Se corrigieron los acentos de esos mensajes en `operaciones_limites.py`.
- **B-5 (`limites/operaciones_limites.py`, `calcular_limite`):**
  - La expresión pasa por la misma validación AST que Métodos Numéricos y admite la misma notación (`2x`, `x^2`). El punto acepta `inf`, `-inf`, `∞` y expresiones como `pi/2`.
  - Se evalúan 12 puntos por lado, con paso relativo a `max(1, |c|)`, y se muestran en una tabla junto con `f(c)`.
  - Cada lado se clasifica en una de cinco categorías:
    - valor;
    - +∞ / -∞, cuando el valor crece por encima de 10⁶ y al menos se multiplica por 10 en los últimos pasos;
    - no definida;
    - no se estabiliza.
  - La estimación toma el tramo estable más cercano antes de que aparezca la cancelación numérica. Cuando la convergencia es lenta y geométrica, se extrapola con Aitken (`sqrt(x)` → 0⁺).
  - En modo bilateral se informa «el límite NO existe: los límites laterales son distintos» mostrando ambos laterales.
  - El resultado se muestra con 6 cifras significativas y siempre se rotula como estimación numérica.
  - Los errores inesperados se registran con `logging` (`heyalgb.limites`) y el estudiante ve un mensaje claro, sin traza técnica.
- **B-6 (`sistemas_numericos/operaciones_numericas.py`):**
  - `parsear_decimal` devuelve `int` o `Decimal` exactos, sin pasar por `float`.
  - Admite hasta 300 dígitos enteros y 300 decimales, con un mensaje claro al superar el límite.
  - `convertir_decimal_a_base` amplía la precisión de `Decimal` para todos los dígitos, incluida la de `abs()`.
- **Pruebas:**
  - Nuevas: `tests/test_limites_y_bases.py` (13 casos).
  - Tres expectativas existentes se ajustaron al mensaje específico nuevo: `test_metodos_numericos.py`, líneas 171 y 238, y `test_evaluador_expresiones.py`.
- **Verificación [Comprobado]:**
  - Suite completa: **119 pruebas OK**.
  - En `VistaLimites` (raíz Tk oculta): `abs(x)/x` → «NO existe, izquierda ≈ -1, derecha ≈ 1»; `1/x²` → `+∞`; `sin` → mensaje con paréntesis.
  - En `VistaSistemasNumericos`: 30 nueves → binario exacto; `1e400` → «demasiado grande».
- **Casos conocidos:**
  - `ln(x)` cuando x→0⁺ se informa como «no se estabiliza», porque crece demasiado lento para considerarlo divergente.
  - `1/x` cuando x→±∞ se informa como `≈ 1e-12 (muy cercano a 0; el límite podría ser 0)`.
  - Las dos respuestas son honestas, pero no son simbólicas.
- **No incluido:** `convertir_a_decimal` (de otra base a decimal) sigue sumando la parte fraccionaria con `float`.

### Entrega 4 — Zoom de resultados (2026-11-18) · completada, sin commit

- **Nuevo componente:** `core/ui/zoom_resultados.py`.
  - `ZoomConsola`: un `CTkFont` propio por consola; nivel entre 50 y 200 % en pasos de 10; el tamaño se calcula siempre desde la base, así que no acumula redondeos.
  - `crear_consola_resultados`: consola monoespaciada (`FUENTE_RESULTADOS`) de solo lectura, con los botones «−», «N %» (restablece) y «+».
  - `escribir_consola`: reemplaza el contenido de la consola.
- **Atajos:** Ctrl + rueda, Ctrl + `+` / `=` / `KP_Add`, Ctrl + `-` / `KP_Subtract` y Ctrl + `0` / `KP_0`.
  - Se instalan solo en el `tk.Text` de cada consola y devuelven `"break"` para no desplazar el texto ni otros marcos. Ningún atajo usa `bind_all`.
  - Al hacer clic en la consola, esta recibe el foco, así que los atajos y Ctrl+C funcionan aunque sea de solo lectura.
- **Posición de lectura:** se conservan la primera línea visible (`@0,0`) y el desplazamiento horizontal.
- **Persistencia:** el nivel dura mientras exista la consola. En Métodos Numéricos se conserva al cambiar de panel (comprobado: 150 % antes y después del cambio). Al cerrar la ventana vuelve a 100 %. No se guarda en disco.
- **Integrado en 13 vistas, 19 consolas:**
  - Matrices individuales, Vectores, Ecuaciones matriciales, Leontief, Flujo de red y Particiones.
  - Sistemas, Límites, Sistemas numéricos y Determinantes (2 consolas).
  - Bisección, Regula Falsi y Errores (5 pestañas).
  - Todas quedan de solo lectura. Las 3 que usaban fuente proporcional (I-5) ahora son monoespaciadas.
  - `wrap="none"` en matrices y tablas; `"word"` en Límites, Sistemas numéricos, la eficiencia de Determinantes y las pestañas de texto de Errores.
- **Pendiente: `vista_metodos_abiertos.py` no se integró** porque tiene cambios sin commit de otro colaborador (I-1). Es un cambio de 6 líneas, igual al de Bisección, cuando se acuerde.
- **Verificación [Comprobado]:**
  - Suite completa: **128 pruebas OK**. Incluye `tests/test_zoom_resultados.py`, que crea una ventana Tk real fuera de la pantalla y prueba:
    - límites y deriva del tamaño;
    - botones;
    - Ctrl con `+`, `=`, `-` y `0`;
    - la rueda con y sin Ctrl;
    - la posición de lectura;
    - la ausencia de atajos globales.
  - Las 13 vistas se construyeron, se escribió en sus 19 consolas y se aplicó zoom sin errores.
  - Capturas de Matrices individuales a 100 %, 200 % y 50 %: las columnas y delimitadores permanecen alineados.
- **[Pendiente de verificación manual]:**
  - Teclas del teclado numérico: Tk en Windows no puede sintetizarlas (`keycode 0`); los atajos están registrados, pero falta probarlos con un teclado físico.
  - Escalado de Windows al 125 % y al 150 %.
- **Detalle de diseño observado (pulido):** en Ecuaciones matriciales, la consola ocupa solo el ancho de las columnas de la barra de acciones (cuadrícula de `frame_inferior` sin peso). El problema es anterior al zoom. **Resuelto en la entrega 5.**

### Entrega 5 — Pulido de comportamiento y estabilidad (2026-11-18) · completada, sin commit

- **I-2 · Newton y Secante** (`newton_raphson.py`, `metodo_secante.py`):
  - Con residuo ≤ tolerancia, `verificar_cambio_de_signo` comprueba que f se anule o cambie de signo en [x ± h] o [x ± 10h], con h igual al último paso.
  - Si no hay cambio de signo, el resultado ya no se declara convergido y se explica: «posible raíz múltiple o función que solo se acerca a 0».
  - Ejemplo: `exp(x)` forzado → «Convergió: No» (antes: raíz en -19).
  - Las raíces simples no cambian.
  - Newton ya no dice «Raíz exacta en x0» cuando solo se cumple la tolerancia; ahora es «Tolerancia por residuo alcanzada en x0».
  - No se tocó `vista_metodos_abiertos.py`: la vista ya muestra «Convergió: No» y «Última aproximación (no convergida)» a partir del resultado.
- **I-4 · Ecuaciones matriciales** (`vista_matricial.py`):
  - `_abrir_secundaria` construye Leontief, Flujo de red o Particiones y solo después oculta la ventana. Si la construcción falla, la ventana sigue visible, el fallo se registra con `logging` (`heyalgb.ui.matricial`) y se muestra un mensaje claro.
  - El `except Exception` de «Calcular» ya no muestra `str(error)` crudo.
  - La consola ocupa todo el ancho (columna 6 con peso).
- **I-7 · Inicio** (`vista_inicio.py`): los identificadores del wipe y del redimensionado se guardan y se cancelan al destruir el inicio.
- **Título:** el Dashboard usa el mismo título que `main.py`, «HeyAlgb · Álgebra Lineal».
- **Matrices individuales:** las descripciones de los pasos y la sustitución hacia atrás usan el formato elegido. Para ello, `eliminacion_por_filas`, `enrutar_resolucion_matricial` y `sustitucion_hacia_atras_detallada` aceptan un parámetro opcional `formatear`. Ejemplo: `F2 = F2 / (1.666667)` en Decimales y `F2 = F2 / (5/3)` en Fracciones.
- **Pruebas:** `tests/test_pulido.py` (8 casos, uno con Tk real).
- **Verificación [Comprobado]:**
  - Suite completa: **136 pruebas OK**.
  - Las 13 vistas siguen construyéndose con sus consolas.
  - Captura de Ecuaciones matriciales con la consola a ancho completo.
  - `VistaMatriz` en ambos formatos con el sistema `3x + y = 1, x + 2y = 0` → `x = 2/5, y = -1/5`.
- **Sin cambios:**
  - Estados de foco y deshabilitado en `tema.py`, fuentes codificadas en las vistas, navegación con teclado y botón «Volver al menú». Requieren decisión del equipo (`pendientes-ui-ux.md`) o pruebas con usuarios.
  - Métodos Abiertos (I-1).
  - Documentación y licencias (entrega 6).

### Entrega 6 — Documentación y licencias (2026-11-18) · completada, sin commit

- **Nuevo `docs/RECURSOS_Y_LICENCIAS.md`:** inventario elaborado a partir de los metadatos incrustados en los archivos y del uso real en el código. **[Comprobado]**
  - **Audio:** `BackgroundMusic.mp3` tiene la etiqueta ID3 «Beneath the Mask -rain- · Lyn · PERSONA5 ORIGINAL SOUNDTRACK». Los 6 efectos llevan nombres de flujo internos de un banco de sonidos (`system#172 (cancel)`, `system#177 (cursor)`, …). No hay ninguna licencia que los cubra: **no son distribuibles**.
  - **Fuentes comerciales:**
    - `HelveticaNowDisplay-Bold.ttf`: «Copyright © 2019 Monotype Imaging Inc. All rights reserved».
    - `Democratica Bold.ttf`: «Copyright (C) 1993 Emigre Graphics», sin licencia incrustada.
  - **Por confirmar:** `UltraCondensedSansSerif.ttf` (Manfred Klein, 2004, sin licencia incrustada), las imágenes (ninguna tiene metadatos de autoría), los avatares y el logotipo de la UAM.
  - **SIL OFL 1.1:** las otras 10 fuentes. Falta incluir `OFL.txt`.
  - **Sin uso en el código:** `Arsenal-Bold.ttf`, `Bordes.png` y `HeyAlgbICON.png`.
  - **Dependencias:** licencias leídas de su `METADATA` instalado. pygame es LGPL.
- **`README.md`:**
  - Nombre HeyAlgb y aviso de licencias al inicio.
  - Módulos completos (Determinantes, Métodos Numéricos y las herramientas de Ecuaciones matriciales).
  - Secciones «Resultados exactos y aproximaciones» y «Consolas de resultados y zoom».
  - Flujo de inicio con `vista_inicio.py`.
  - Estructura y vistas actualizadas.
  - Tabla de dependencias con su uso real. Se corrigió «no se usan NumPy ni SciPy» y se aclaró que `scipy` no se importa.
  - Comando de pruebas (`python -m unittest discover -s tests`), `compileall` para todo el código y nota sobre `logging`.
  - Hallazgos de licencias.
- **`docs/ExpoNoviembre3del2026.md`:**
  - Corregida la afirmación sobre SciPy.
  - El menú ahora incluye Métodos Abiertos.
  - Mensajes específicos del evaluador.
  - Verificación de cambio de signo en Newton y Secante (con el ejemplo \(e^{-19}=5.6\times10^{-9}\), comprobado).
  - **No se cambió** la descripción de los marcadores de la gráfica de Métodos Abiertos: describe el código confirmado, y el cambio sin commit del colaborador la modifica (I-1).
- **Verificación [Comprobado]:**
  - `python -m unittest discover -s tests` → **136 OK**.
  - `python -m compileall -q main.py core` → código de salida 0.
- **No incluido:**
  - Sustituir el audio o las fuentes (requiere decisión y recursos del equipo).
  - Crear `OFL.txt` (conviene copiar el texto oficial de cada familia).
  - Eliminar `scipy` o el código muerto (decisión del equipo).
  - Empaquetado con PyInstaller (después de resolver las licencias).
