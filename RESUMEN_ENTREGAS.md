# Resumen de entregas · HeyAlgb

Fecha: 2026-11-18 · Estado: **todo sin commit** en `main`.

No se tocaron los cambios sin commit de otra persona en
`core/ui/vista_metodos_abiertos.py` y `core/ui/vista_grafica_biseccion.py`.
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

## Decisiones que quedan para el equipo

- Reemplazar el audio y las dos fuentes comerciales.
- Añadir el texto de la licencia OFL junto a las fuentes.
- Decidir si se quitan `scipy` y el código que nadie usa.
- Integrar el zoom en Métodos Abiertos cuando se acuerden los cambios de la otra persona.
- Probar el teclado numérico y el escalado de Windows.
- Preparar un ejecutable, después de resolver las licencias.
- Confirmar el trabajo en git, dejando fuera los dos archivos de la otra persona.
