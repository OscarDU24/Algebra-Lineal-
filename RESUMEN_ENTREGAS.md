# Resumen de entregas · HeyAlgb

Fecha: 2026-11-18.

Estado:
- Entregas 0 a 6: confirmadas en `main` (commit `a5997bf`).
- Entregas 7 a 10 (etapa final de UX): rama `pulido-ux-final`, **sin commit ni push**.

En las entregas 0 a 6 no se tocaron los cambios de otra persona en
`core/ui/vista_metodos_abiertos.py` y `core/ui/vista_grafica_biseccion.py`. En la
entrega 7 solo se cambió la interfaz de Métodos Abiertos (consola común y destino
x0/x1), sin tocar su lógica.
El detalle técnico y la verificación de cada entrega están en
[DIAGNOSTICO_AUDITORIA.md](DIAGNOSTICO_AUDITORIA.md).

| Entrega | Tema | Pruebas al terminar |
|---|---|---|
| 0 | Diagnóstico (sin cambios en el código) | 80 OK |
| 1 | Evaluador de expresiones: congelamiento y precisión | 92 OK |
| 2 | Exactitud con fracciones en Matrices individuales | 106 OK |
| 3 | Límites, sistemas numéricos y mensajes de error | 119 OK |
| 4 | Zoom en las consolas de resultados | 128 OK |
| 5 | Pulido de comportamiento y estabilidad | 136 OK |
| 6 | Documentación y licencias | 136 OK |
| 7 | Navegación coherente (Volver, X, aviso de cambios) | 151 OK (7–10) |
| 8 | Ayuda contextual y «Cargar ejemplo» | |
| 9 | Guía de bienvenida y preferencias | |
| 10 | Copiar, foco, errores por campo, audio y tamaño de ventanas | |

---

## Entrega 0 · Diagnóstico

**Añadido**
- `DIAGNOSTICO_AUDITORIA.md`: estado del repositorio, 6 problemas graves comprobados, plan del zoom y prioridades.

**Aplicado / eliminado:** nada. No se modificó ningún archivo de código.

---

## Entrega 1 · Evaluador de expresiones (congelamiento y precisión)

**Aplicado**
- `core/limites/operaciones_limites.py`: `sin`, `cos`, `sqrt`, `exp` y `log` usan ahora el módulo `math`. La reducción del ángulo pasa a hacerse con `math.remainder`, en tiempo constante.
  - **Antes:** `sin(1e300)` congelaba la aplicación, `sqrt(1e20)` daba `9.35e10` y `exp(50)` tenía un error del 9 %.
  - **Ahora:** todas dan el valor correcto al instante.

**Eliminado**
- Las series de Taylor y la raíz de Newton escritas a mano (`_seno`, `_coseno`, `_raiz_cuadrada`, `_exponencial`, `_logaritmo`). Se conservan los nombres de las funciones y los mensajes que ya existían.

**Añadido**
- `tests/test_evaluador_expresiones.py` (12 pruebas). Incluye una prueba, con límite de tiempo, de que `sin(1e300)` no congela la aplicación.

---

## Entrega 2 · Exactitud con fracciones (Matrices individuales)

**Aplicado**
- Con fracciones, la eliminación por filas, la clasificación, la verificación y la inversa comparan con `== 0` en lugar de usar una tolerancia de decimales: `core/lineal/eliminacion.py`, `clasificacion.py`, `verificacion.py` y `solucion.py`.
  - Un pivote `1/10¹⁰` ya no se trata como cero.
  - La inversa de una matriz de fracciones sale exacta.
- `core/lineal/conversiones.py`:
  - Nueva función `convertir_a_racional`, que lee `1/3`, `0.1` o `1e-3` como fracción exacta.
  - Nueva función `formatear_decimal`, que muestra hasta 6 decimales y nunca muestra «0» para un valor distinto de cero.
- `core/lineal/visualizacion.py`: el sistema equivalente usa el formato que eligió el usuario.
- `core/ui/vista_matriz.py`:
  - La entrada se lee como fracción exacta.
  - El modo «Fracciones» ya no aproxima: `0.0004` antes se mostraba como `0`.
  - Los pasos se escriben con paréntesis: `F2 = F2 / (2/3)`.

**Eliminado**
- `limit_denominator(1000)`, que mostraba aproximaciones como si fueran fracciones exactas.
- La identidad en decimales dentro de la inversa cuando la entrada es exacta.

**Añadido**
- `core/lineal/exactitud.py`: reglas comunes para decidir si un cálculo es exacto o aproximado.
- `tests/test_lineal_exactitud.py` (16 pruebas).

---

## Entrega 3 · Límites, sistemas numéricos y mensajes de error

**Aplicado**
- **Límites** (`operaciones_limites.py`, `calcular_limite` reescrita):
  - Usa la misma validación segura de expresiones que Métodos Numéricos, así que admite `2x` y `x^2`.
  - El punto puede escribirse como `inf`, `-inf`, `∞` o `pi/2`.
  - Muestra una tabla de 12 aproximaciones por lado.
  - Informa si la función tiende a un valor, si diverge a +∞ o −∞, si los límites laterales son distintos, si no está definida o si no se estabiliza.
  - El resultado se rotula siempre como «estimación numérica».
  - Ejemplo: `1/x²` en 0 antes daba `1e14`; ahora da `+∞`.
- **Mensajes de error** (`metodos_numericos/biseccion.py`): se conserva la causa concreta, por ejemplo «`sin` es una función: escríbala con paréntesis», «raíz cuadrada de un negativo» o «división entre cero».
- **Sistemas numéricos** (`operaciones_numericas.py`):
  - Los números se leen como `int` o `Decimal`, sin pasar por decimales aproximados.
  - Los enteros grandes, de hasta 300 dígitos, se convierten sin error.
- Se corrigieron los acentos de los mensajes de dominio.
- Tres pruebas que ya existían se ajustaron a los mensajes nuevos, más específicos.

**Eliminado**
- `_aproximar_limite` y el redondeo del resultado a 2 decimales.
- El mensaje genérico «sintaxis u operaciones no permitidas» como única respuesta.
- El mensaje «ERROR INTERNO» con texto técnico; ahora el detalle va a un registro interno (`logging`).

**Añadido**
- `tests/test_limites_y_bases.py` (13 pruebas).

---

## Entrega 4 · Zoom en las consolas de resultados

**Aplicado**
- 19 consolas en 13 vistas pasan a ser de solo lectura y monoespaciadas, con zoom propio:
  - Matrices individuales, Vectores, Ecuaciones matriciales, Leontief, Flujo de red y Particiones.
  - Sistemas, Límites, Sistemas numéricos y Determinantes (2 consolas).
  - Bisección, Regula Falsi y Errores (5 consolas).
- Ecuaciones matriciales, Leontief y Flujo de red dejan de usar una fuente proporcional.
- Las consolas que muestran matrices o tablas ya no parten las líneas y tienen barra horizontal.

**Añadido**
- `core/ui/zoom_resultados.py`:
  - Zoom de 50 a 200 % en pasos de 10.
  - Controles: Ctrl + rueda, Ctrl + `+` / `-` / `0`, el teclado numérico y los botones `− / % / +`.
  - Sin atajos que afecten al resto de la aplicación.
  - Conserva la posición de lectura.
- `tests/test_zoom_resultados.py` (9 pruebas con una ventana real).

**Pendiente**
- Métodos Abiertos, que tiene cambios sin commit de otra persona.
- Probar el teclado numérico y el escalado de Windows a mano.

---

## Entrega 5 · Pulido de comportamiento y estabilidad

**Aplicado**
- **Newton y Secante** (`newton_raphson.py`, `metodo_secante.py`):
  - Solo declaran convergencia por residuo si además verifican un cambio de signo cerca del resultado. Así, `exp(x)` ya no aparece con una «raíz» en −19.
  - «Raíz exacta en x0» se reserva para cuando f(x0) vale exactamente 0.
- **Ecuaciones matriciales** (`vista_matricial.py`):
  - Si Leontief, Flujo de red o Particiones fallan al abrirse, la ventana ya no queda oculta.
  - Los errores inesperados muestran un mensaje claro y el detalle va a un registro interno.
  - La consola ocupa todo el ancho de la ventana.
- **Matrices individuales:** los pasos usan el formato elegido, Decimales o Fracciones. Para ello se añadió un parámetro opcional `formatear` en `eliminacion.py` y `solucion.py`.
- **Inicio** (`vista_inicio.py`): las tareas programadas de la transición se cancelan si se cierra la aplicación a mitad.
- **Dashboard** (`dashboard.py`): el título queda unificado como «HeyAlgb · Álgebra Lineal».

**Eliminado**
- Ocultar Ecuaciones matriciales *antes* de crear la ventana secundaria.
- Mostrar al estudiante el texto técnico de los errores (`str(error)`).

**Añadido**
- `tests/test_pulido.py` (8 pruebas).

---

## Entrega 6 · Documentación y licencias

**Añadido**
- `docs/RECURSOS_Y_LICENCIAS.md`: inventario elaborado leyendo los metadatos de cada archivo.
  - El audio está etiquetado como música y sonidos de sistema de Persona 5: no distribuible.
  - HelveticaNow (Monotype) y Democratica (Emigre) son fuentes comerciales.
  - Las otras 10 fuentes son SIL OFL 1.1 y falta incluir el texto de la licencia.
  - El origen de las imágenes está sin documentar.
  - `Arsenal-Bold.ttf`, `Bordes.png` y `HeyAlgbICON.png` no se usan.

**Aplicado**
- `README.md`:
  - Aviso de licencias y módulos completos.
  - Secciones «Resultados exactos y aproximaciones» y «Consolas de resultados y zoom».
  - Tabla de dependencias con su uso real.
  - Comandos para ejecutar las pruebas y `compileall`.
- `docs/ExpoNoviembre3del2026.md`: corrección sobre SciPy, Métodos Abiertos en el menú, mensajes específicos y la verificación de cambio de signo.

**Eliminado (en la documentación)**
- Las afirmaciones falsas «no se usan NumPy ni SciPy», «no hay pruebas automatizadas» y «SciPy contrasta la bisección».

---

---

## Etapa final de UX (entregas 7 a 10) · rama `pulido-ux-final`

Alcance: solo experiencia de usuario. Los módulos matemáticos (`core/lineal`,
`limites`, `metodos_numericos`, `sistemas`, `sistemas_numericos`, `determinantes`,
`matriciales` y `vectores`) no tienen ningún cambio respecto de `main`.

### Entrega 7 · Navegación coherente

**Añadido**
- `core/ui/navegacion.py`, con `instalar_navegacion`:
  - Barra con «← Volver», «? Ayuda» y «Cargar ejemplo».
  - «Volver» y la X usan el mismo camino.
  - `GuardiaCambios` pide confirmación solo si el usuario escribió datos que siguen en pantalla.
  - Borde de foco en los campos.
  - Ajuste del tamaño de la ventana a su contenido.
- Instalado en las 11 ventanas de calculadora. Leontief, Flujo de Red y Particiones vuelven a Ecuaciones matriciales.

**Aplicado**
- Al volver se cierra la ayuda abierta, y la ventana de Métodos Numéricos también cierra sus auxiliares (gráfica y teclado), como antes.
- Las tareas `after()` nuevas se cancelan al destruir la ventana.

### Entrega 8 · Ayuda contextual y ejemplos

**Añadido**
- `core/ui/ayuda.py`: contenido de las 15 herramientas (para qué sirve, datos, formatos verificados contra el código, ejemplo, restricciones, salida y atajos).
  - Una sola ventana de ayuda por herramienta, que se cierra con «Cerrar» o Esc.
  - Funciona sobre ventanas modales (Particiones).
- «Cargar ejemplo» en Matrices, Sistemas, Límites, Sistemas numéricos, Determinantes, Bisección, Regula Falsi y Métodos Abiertos.
  - No calcula.
  - Pide confirmación si hay otros datos.
  - Usa la misma validación que el ingreso manual.
- Los resultados de los ejemplos se comprobaron con el código: (2, 3, −1), det = 24 y 45.75 → 101101.11.

**Aplicado (solo nombres de botones)**
- «Limpiar Valores» / «Borrar» → «Limpiar entradas».
- «Limpiar Consola» y «Limpiar Resultados» (Límites, Sistemas) → «Limpiar entradas»; ahora limpian los campos, porque la consola ya tiene su propio «Limpiar resultados».
- Ecuaciones matriciales: «Limpiar» → «Limpiar todo».

### Entrega 9 · Bienvenida y preferencias

**Añadido**
- `core/ui/bienvenida.py`: guía de 4 pasos con Anterior, Siguiente, Omitir, Finalizar, «No mostrar al iniciar», Esc y flechas.
  - Se programa 300 ms después de crear el Dashboard, sin interferir con la portada.
  - Se abre de nuevo desde el menú Ayuda.
- `core/ui/preferencias.py`: archivo `%APPDATA%\HeyAlgb\preferencias.json` (o `HEYALGB_CONFIG_DIR`).
  - Escritura atómica.
  - Si el archivo falta o está dañado, se usan los valores predeterminados y se registra un aviso.
- Menú Ayuda del Dashboard: «Guía de bienvenida» y «Cómo usar HeyAlgb y atajos de teclado».

### Entrega 10 · Comodidad y accesibilidad

**Añadido / aplicado**
- **Consolas:**
  - «Copiar resultados», con el aviso «✓ Copiado» o «Nada que copiar» durante 1.8 s y sin ventana modal.
  - «Limpiar resultados».
  - Etiqueta «Zoom (clic en % = 100 %)».
  - Copiar y limpiar no cambian el zoom ni recalculan.
- **Métodos Abiertos:** usa la consola común. Al cambiar a Newton, el destino del clic en la gráfica vuelve a x0 (antes podía escribir en el campo oculto x1).
- **Errores por campo:**
  - Límites: el campo vacío recibe el foco, se marca en ámbar y la consola muestra un mensaje con «⚠».
  - Matrices: la casilla vacía o inválida recibe el foco y se marca.
  - Los colores nuevos `COLOR_FOCO` y `COLOR_ADVERTENCIA` están en `tema.py`.
- **Dashboard:**
  - Las tarjetas se alcanzan con Tab, muestran un borde rojo y se abren con Enter.
  - Nuevo control «Efectos de sonido» (`AudioManager.establecer_efectos_habilitados`).
  - La música y los efectos se guardan en las preferencias, también desde la portada.
- **Tamaño de ventanas:** se agrandan hasta su contenido sin pasar del tamaño de la pantalla. A 100 % de escala, Sistemas, Sistemas numéricos y Determinantes recortaban controles. Las consolas de Determinantes y Sistemas numéricos piden menos altura mínima.

**No añadido (con motivo)**
- **Separar «resultado» y «procedimiento» al copiar:** el texto no tiene una marca fiable para hacerlo.
- **Botón Cancelar:** no hay cálculos cancelables; todos son síncronos y no se introdujeron hilos.
- **Bloqueo de pulsaciones repetidas:** como el cálculo es síncrono, un doble clic solo repite el mismo cálculo; no hay estados intermedios que corromper.

**Pruebas añadidas**
- `tests/test_ux_navegacion.py` (15 casos): preferencias (archivo ausente, dañado o con tipos incorrectos, y ubicación fuera del repositorio), contenido completo de la ayuda, ejemplos contra el código, Volver con y sin cambios, teclas de navegación, ayuda única, Cargar ejemplo, error por campo, copiar y limpiar sin afectar el zoom, recorrido de la bienvenida y silencio de efectos.

### Pendientes y hallazgos para el equipo

- **Escalado de Windows al 150 %:** en una pantalla de 1080 p, el contenido de la mayoría de las ventanas mide más que el alto disponible. Las áreas de datos ya tienen scroll, pero los controles inferiores pueden quedar fuera. Resolverlo requiere poner el contenido de cada vista en un contenedor con desplazamiento: es un cambio mayor, que se propone como tarea aparte.
- **Sin probar a mano:** lector de pantalla, teclado numérico y las ventanas de confirmación con un usuario real.
- **Sin límite de dimensiones:** ninguna calculadora limita el tamaño máximo de las matrices (n grande crea muchísimos campos). No es un fallo matemático; se documenta y no se cambió.

## Decisiones que quedan para el equipo

- Reemplazar el audio y las dos fuentes comerciales.
- Añadir el texto de la licencia OFL junto a las fuentes.
- Decidir si se quitan `scipy` y el código que nadie usa.
- Integrar el zoom en Métodos Abiertos cuando se acuerden los cambios de la otra persona.
- Probar el teclado numérico y el escalado de Windows.
- Preparar un ejecutable, después de resolver las licencias.
- Confirmar el trabajo en git, dejando fuera los dos archivos de la otra persona.
