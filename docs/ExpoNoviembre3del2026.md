# Exposición: Métodos Numéricos — 3 de noviembre de 2026

Este documento sirve como guía para explicar el módulo de Métodos Numéricos
de HeyAlgb: cómo se organizan sus herramientas, qué hacen sus funciones y qué
significan los resultados que presenta la interfaz.

El módulo está separado en tres partes:

- **Interfaz:** recibe los datos y presenta los resultados.
- **Lógica numérica:** valida las entradas, calcula y construye los datos de
  salida.
- **Bibliotecas numéricas:** NumPy aporta operaciones de punto flotante y
  medidas de condicionamiento; SciPy ofrece una implementación independiente
  de la bisección para contrastar resultados.

La ventana unificada está en
[`core/ui/vista_metodos_numericos.py`](../core/ui/vista_metodos_numericos.py).
Su menú desplegable permite alternar entre **Método de Bisección** y
**Análisis de Errores**, sin abrir ventanas separadas. Los paneles y la lógica
de cada cálculo se mantienen en módulos específicos.

---

## 1. Método de bisección

### Idea matemática

El método busca una raíz de \(f(x)=0\) en un intervalo \([a,b]\). Para poder
comenzar, la función debe estar definida en ambos extremos y tener signos
opuestos:

\[
f(a)f(b)<0.
\]

Por el teorema del valor intermedio, si la función es continua en el intervalo,
existe al menos una raíz entre los extremos. En cada iteración se calcula el
punto medio:

\[
x_r=\frac{x_l+x_u}{2}.
\]

Se conserva la mitad del intervalo cuyos extremos todavía tienen signos
opuestos. Así, la longitud del intervalo se reduce aproximadamente a la mitad
en cada paso.

### Funciones principales

El código está en
[`core/metodos_numericos/biseccion.py`](../core/metodos_numericos/biseccion.py).

#### `_convertir_finito(valor, nombre)`

Convierte una entrada a número de punto flotante y verifica que sea finita.
Rechaza valores booleanos, textos que no representan números y valores como
`NaN` o infinito. Al centralizar esta validación, los extremos y la tolerancia
siguen las mismas reglas.

#### `_crear_funcion(funcion)`

Prepara la expresión ingresada por el usuario como una función evaluable de
\(x\). No ejecuta el texto como código Python. Primero lo analiza con el módulo
`ast` y luego reutiliza el evaluador seguro de
[`core/limites/operaciones_limites.py`](../core/limites/operaciones_limites.py).

El proceso limita la longitud y complejidad de la expresión, comprueba los
exponentes y delega al evaluador la lista de operaciones y funciones
permitidas. El resultado de cada evaluación debe ser real y finito; si no,
genera un error explícito.

#### `_iteraciones_teoricas(xl, xu, tolerancia)`

Calcula el número de iteraciones que teóricamente se necesitan para reducir el
ancho del intervalo hasta la tolerancia:

\[
n\geq\log_2\left(\frac{x_u-x_l}{\text{tol}}\right).
\]

La implementación usa la diferencia de logaritmos y redondea hacia arriba,
evitando formar directamente el cociente, que podría ser excesivamente grande.
Este valor sirve como estimación de referencia y como límite para proteger el
bucle.

#### `_error_aproximado_porcentual(actual, anterior)`

Calcula el cambio relativo entre dos aproximaciones consecutivas, expresado
como porcentaje:

\[
E_a=\left|\frac{x_r^{(i)}-x_r^{(i-1)}}{x_r^{(i)}}\right|100.
\]

En la primera iteración no hay una aproximación previa, por lo que la columna
`Ea (%)` comienza sin valor. También se maneja el caso de aproximación actual
igual a cero para evitar dividir entre cero.

#### `resolver_biseccion(funcion, a, b, tolerancia)`

Es la función coordinadora del algoritmo:

1. Valida que `a`, `b` y la tolerancia sean números finitos, que la tolerancia
   sea positiva y que \(a<b\).
2. Construye el evaluador seguro y calcula \(f(a)\) y \(f(b)\).
3. Si uno de los extremos ya es una raíz, retorna ese resultado sin iterar.
4. Comprueba el cambio de signo comparando los bits de signo de NumPy, en vez
   de multiplicar \(f(a)f(b)\). Esto evita un posible desbordamiento al formar
   el producto.
5. Calcula la estimación teórica y ejecuta las iteraciones. En cada paso guarda
   los extremos, el punto medio, sus evaluaciones y el error aproximado.
6. Detiene el cálculo si encuentra una raíz exacta, si el ancho del intervalo
   queda por debajo de la tolerancia o si el error porcentual queda por debajo
   del valor de tolerancia.
7. Calcula también una raíz con `scipy.optimize.bisect` y devuelve la
   diferencia absoluta entre ambos resultados.

El resultado es un diccionario que incluye la raíz, \(f(x_r)\), el número
efectivo y teórico de iteraciones, el criterio de paro, la comparación con
SciPy y las filas de la tabla.

**Nota sobre el criterio porcentual:** en la implementación se compara el
valor numérico de `Ea (%)` directamente con la tolerancia ingresada, aunque
`Ea` está expresado en porcentaje y la tolerancia también participa en el
criterio de ancho del intervalo. Son magnitudes con unidades e
interpretaciones distintas. Para explicar el resultado con rigor, conviene
indicar qué criterio detuvo esa ejecución; la estimación teórica está asociada
al criterio de ancho del intervalo.

#### `_resultado_extremo(...)`

Forma el resultado especial cuando `a` o `b` ya satisface \(f(x)=0\). Registra
cero iteraciones, conserva la estimación teórica y también solicita el
contraste de SciPy. Si SciPy no puede realizar esa comparación, informa el
fallo en lugar de devolver una comparación ficticia.

#### `formatear_tabla(resultado)` y `_formatear_celda(valor)`

Convierten las filas numéricas en texto alineado mediante espacios
monoespaciados. La tabla conserva estas columnas:

`Iteración | xl | xu | xr | f(xl) | f(xu) | f(xr) | Ea (%)`

`_formatear_celda` se ocupa de mostrar valores ausentes y no finitos de forma
legible.

### Ejemplo para la exposición

Para \(f(x)=x^3-x-2\), intervalo \([1,2]\) y tolerancia \(10^{-6}\), el
resultado observado fue aproximadamente \(1.5213804245\). En ese ejemplo se
realizaron 20 iteraciones, igual que la estimación teórica, y la raíz de SciPy
coincidió a la precisión mostrada. La coincidencia sirve como contraste de
implementaciones, no como demostración de que cualquier cálculo esté libre de
error.

---

## 2. Cálculo y propagación de errores

Las operaciones de esta sección viven en
[`core/metodos_numericos/operaciones_errores.py`](../core/metodos_numericos/operaciones_errores.py).
El principio común es validar los valores de entrada antes de calcular y
devolver resultados estructurados para que la interfaz decida cómo mostrarlos.

### `calcular_errores(valor_aproximado, valor_exacto)`

Calcula tres medidas:

\[
E_{\text{abs}}=|x_{\text{aprox}}-x_{\text{exacto}}|,
\qquad
E_{\text{rel}}=\frac{E_{\text{abs}}}{|x_{\text{exacto}}|},
\qquad
E_{\%}=100E_{\text{rel}}.
\]

El error absoluto conserva las unidades de la cantidad; los errores relativo y
porcentual permiten comparar escalas. Si el valor exacto es cero, el error
relativo y porcentual no están definidos salvo que ambos valores coincidan
(en cuyo caso el error es cero). El resultado lo expresa como `None`, y la
interfaz lo identifica como no definido.

**Ejemplo:** aproximado `9.8`, exacto `10`: error absoluto \(0.2\), relativo
\(0.02\), porcentual \(2\%\).

### `propagar_error(funcion, x, delta_x)`

Estima el efecto de una pequeña variación \(\Delta x\) sobre \(y=f(x)\). Usa la
aproximación diferencial:

\[
\Delta y\approx f'(x)\Delta x.
\]

La derivada se aproxima con diferencia central:

\[
f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}.
\]

El paso \(h\) se ajusta al tamaño de \(x\) usando la raíz cúbica del épsilon de
máquina de `float64`, un compromiso práctico para limitar errores de
truncamiento y redondeo en la diferencia. Luego compara la estimación
diferencial con el cambio finito \(f(x+\Delta x)-f(x)\). Si las evaluaciones o
los resultados no son finitos, la función notifica el error.

**Ejemplo:** para \(f(x)=x^2\), \(x=2\), \(\Delta x=0.01\), la aproximación es
cerca de `0.04`, mientras que el cambio finito es `0.0401`. La diferencia
muestra el efecto de ignorar términos de orden superior a \(\Delta x\).

### `simular_truncamiento_redondeo(valor, decimales)`

Compara dos maneras de reducir la cantidad de decimales:

- **Truncamiento:** corta las cifras posteriores, hacia cero.
- **Redondeo:** ajusta la última cifra conservada según la regla de mitad hacia
  arriba.

La función usa `Decimal` para controlar la cuantización decimal y devuelve los
valores truncado y redondeado, además del error absoluto producido por cada
uno. Se rechazan cantidades de decimales negativas o que no sean enteros.

**Ejemplo:** con `3.146` y dos decimales, el truncamiento da `3.14` y el
redondeo `3.15`.

### `demostrar_punto_flotante()`

Reúne ejemplos reproducibles de la representación IEEE-754:

- Calcula `0.1 + 0.2` y comprueba si es exactamente igual a `0.3`.
- Consulta `numpy.finfo(float).eps`, la separación entre `1.0` y el siguiente
  número `float64` representable.
- Simula overflow y underflow con `numpy.float32` dentro de `numpy.errstate`,
  para que el comportamiento esperado no genere avisos que interrumpan la
  demostración.
- Retorna el menor valor normal de `float32`.

En la ejecución observada, `0.1 + 0.2` produjo
`0.30000000000000004`, el épsilon `float64` fue aproximadamente
\(2.22\times10^{-16}\), y las simulaciones dieron infinito y cero,
respectivamente. Esto ilustra que los números decimales generalmente se
representan mediante aproximaciones binarias finitas.

---

## 3. Comparación exacta y de punto flotante con matrices

El complemento está en
[`core/metodos_numericos/verificacion_matriz.py`](../core/metodos_numericos/verificacion_matriz.py).
Conecta el contenido de métodos numéricos con el Gauss-Jordan estudiado en
álgebra lineal.

### `parsear_matriz(texto)`

Lee una matriz escrita en filas: saltos de línea separan filas y espacios
separan elementos. Convierte cada entrada a `fractions.Fraction`, por lo que
admite notación entera, decimal o fraccionaria, como `1/2`. Rechaza entradas
inválidas y matrices que no sean cuadradas.

### `matriz_hilbert(orden=5)`

Construye una matriz de Hilbert usando fracciones exactas:

\[
H_{ij}=\frac{1}{i+j-1},\quad i,j=1,\ldots,n.
\]

Es una familia clásica de matrices cada vez peor condicionadas al aumentar su
orden. Esto la hace útil para observar cómo pequeños errores de redondeo
pueden influir en los cálculos numéricos.

### `comparar_inversas(matriz)`

Compara tres resultados y varias medidas:

1. Convierte la matriz a fracciones exactas y aplica el Gauss-Jordan del
   proyecto sobre la matriz aumentada \([A\mid I]\).
2. Convierte la misma matriz a `float64` y vuelve a aplicar el Gauss-Jordan.
3. Calcula una inversa de referencia con `numpy.linalg.inv` y el número de
   condición con `numpy.linalg.cond`.
4. Compara las inversas de punto flotante con la inversa exacta convertida a
   `float64`, y calcula los errores absoluto y relativo.
5. Calcula el residuo máximo de \(A A^{-1}-I\). Un residuo pequeño indica que
   el producto se acerca a la identidad, pero debe interpretarse junto con el
   condicionamiento.

La salida incluye ambas inversas calculadas por Gauss-Jordan, la inversa de
NumPy y las medidas de error, residuo y condición. Una matriz singular o una
operación que produzca valores no finitos genera un error explícito.

**Ejemplo didáctico:** en la matriz de Hilbert 5×5 se observó un número de
condición cercano a `476607`. La diferencia absoluta entre la inversa exacta y
la obtenida por Gauss-Jordan en `float64` fue cercana a
\(1.27\times10^{-7}\), mientras que el residuo máximo fue aproximadamente
\(6.30\times10^{-12}\). El residuo pequeño no elimina el efecto del
condicionamiento: las medidas responden preguntas diferentes.

### `matriz_a_texto(matriz, formato="fracciones")`

Formatea matrices para la salida monoespaciada. El modo predeterminado presenta
fracciones; el modo `"decimales"` muestra aproximaciones decimales. Solo cambia
la presentación, no vuelve a calcular la inversa.

### Validadores y utilidades internas

- `_validar_matriz(matriz)` comprueba que la entrada sea cuadrada y convierte
  sus elementos a `Fraction`.
- `_formatear_fraccion(valor)` imprime enteros sin denominador y fracciones
  con numerador y denominador.
- `_residuo_maximo(matriz, inversa)` calcula
  \(\max|A A^{-1}-I|\) usando NumPy.

---

## 4. Cómo se conecta con la interfaz

La vista principal es
[`core/ui/vista_metodos_numericos.py`](../core/ui/vista_metodos_numericos.py).
`VistaMetodosNumericos` crea una ventana secundaria, oculta el Dashboard y
presenta un `CTkComboBox` con las dos áreas del módulo. Al cambiar la opción,
`cambiar_operacion` oculta el panel anterior y muestra el elegido. Los paneles
se conservan una vez creados, por lo que cambiar de menú no obliga a reconstruir
las entradas ni descarta los valores.

[`core/ui/vista_biseccion.py`](../core/ui/vista_biseccion.py) recoge la
función, los extremos y la tolerancia. Su callback `calcular` invoca
`resolver_biseccion`, muestra los errores de validación y presenta la tabla y
la comparación con SciPy. `borrar` limpia los campos.

[`core/ui/vista_errores.py`](../core/ui/vista_errores.py) organiza las
herramientas en cuatro pestañas:

1. Errores y propagación.
2. Truncamiento y redondeo.
3. Punto flotante.
4. Verificación de matrices con Gauss-Jordan.

Los callbacks `calcular_errores`, `calcular_propagacion`,
`calcular_redondeo`, `demostrar_float` y `calcular_verificacion` enlazan los
controles con sus funciones de backend. `cargar_hilbert` introduce una matriz
de Hilbert 5×5 de ejemplo y ejecuta su comparación. Las salidas se imprimen en
cajas de texto monoespaciadas para alinear tablas y matrices.

Al cerrar la ventana contenedora se destruye únicamente esa ventana y se
restaura el Dashboard.

---

## 5. Guion breve sugerido

1. **Presentar la organización:** una tarjeta y una ventana para las
   herramientas de métodos numéricos, con un selector para cambiar de área.
2. **Explicar bisección:** cambio de signo, punto medio, reducción del
   intervalo, tolerancia, tabla de iteraciones y contraste con SciPy.
3. **Distinguir los errores:** absoluto mide diferencia en las unidades
   originales; relativo y porcentual comparan la diferencia con el valor de
   referencia.
4. **Demostrar propagación:** comparar \(f'(x)\Delta x\) con el cambio finito
   calculado para \(f(x+\Delta x)-f(x)\).
5. **Mostrar representación finita:** `0.1 + 0.2`, épsilon, overflow y
   underflow explican por qué la computadora no representa todos los reales
   exactamente.
6. **Relacionar con álgebra lineal:** comparar la inversa exacta y la
   aproximada, observar el residuo y el número de condición de Hilbert.
7. **Cerrar con la idea central:** un resultado numérico se entiende mejor
   junto con sus criterios de paro, precisión, errores y estabilidad.

## Archivos de referencia

- [`core/metodos_numericos/biseccion.py`](../core/metodos_numericos/biseccion.py)
- [`core/metodos_numericos/operaciones_errores.py`](../core/metodos_numericos/operaciones_errores.py)
- [`core/metodos_numericos/verificacion_matriz.py`](../core/metodos_numericos/verificacion_matriz.py)
- [`core/ui/vista_metodos_numericos.py`](../core/ui/vista_metodos_numericos.py)
- [`core/ui/vista_biseccion.py`](../core/ui/vista_biseccion.py)
- [`core/ui/vista_errores.py`](../core/ui/vista_errores.py)
