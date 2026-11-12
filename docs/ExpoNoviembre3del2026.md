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
Su menú desplegable permite alternar entre **Método de Bisección**,
**Método Regula Falsi** y **Análisis de Errores**, sin abrir ventanas
separadas. Los paneles y la lógica de cada cálculo se mantienen en módulos
específicos.

---

## 1. Método de bisección

### Idea matemática

El método busca una raíz de \(f(x)=0\) en un intervalo \([a,b]\). Para poder
comenzar, la función debe estar definida en un intervalo y presentar valores
con signos opuestos en sus extremos:

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
permitidas. Antes de validar el AST, `normalizar_expresion` convierte
notaciones como `2x`, `3(x+1)`, `(x+1)(x-1)`, `x^2`, `×`, `÷` y `π` a una
expresión equivalente con operadores explícitos. El resultado de cada
evaluación debe ser real y finito; si no, genera un error explícito.

#### `muestrear_funcion(funcion, x_min, x_max, muestras=400)`

Evalúa la función en puntos equidistantes del rango de exploración y devuelve
las coordenadas para dibujarla. Los puntos donde la función no está definida se
representan como huecos para evitar conectar regiones a través de una
discontinuidad. Esta operación solo prepara datos gráficos: no propone ni
selecciona extremos para el método.

#### `analizar_intervalos(funcion, x_min, x_max, muestras=400)`

Además de los datos de muestreo, detecta tramos consecutivos con cambio de
signo y devuelve sus extremos como candidatos para análisis programático. Una
muestra que coincide exactamente con una raíz también se toma en cuenta. Esta
función se conserva para el análisis numérico, pero la interfaz actual no
transfiere sus candidatos a los campos `a` y `b`.

El muestreo **no** demuestra continuidad ni garantiza detectar raíces fuera
del rango o raíces que toquen el eje sin cambiar de signo.

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
4. Comprueba el cambio de signo comparando si cada evaluación es negativa, en
   vez de multiplicar \(f(a)f(b)\). Esto evita un posible desbordamiento al
   formar el producto.
5. Calcula la estimación teórica y ejecuta las iteraciones. En cada paso guarda
   los extremos, el punto medio, sus evaluaciones y el error aproximado.
6. Detiene el cálculo si encuentra una raíz exacta o si el ancho del intervalo
   queda por debajo de la tolerancia. El error porcentual aproximado se reporta
   en la tabla como información adicional.
7. Devuelve la raíz, el residuo, las iteraciones y el criterio de paro.

El resultado es un diccionario que incluye la raíz, \(f(x_r)\), el número
efectivo y teórico de iteraciones, el criterio de paro y las filas de la tabla.

La tolerancia se aplica al ancho del intervalo, una magnitud expresada en las
mismas unidades que \(x\). `Ea (%)` se conserva en la tabla como indicador de
la variación relativa entre aproximaciones consecutivas, pero no se compara
directamente con esa tolerancia porque sus unidades e interpretaciones son
distintas.

#### `_resultado_extremo(...)`

Forma el resultado especial cuando `a` o `b` ya satisface \(f(x)=0\). Registra
cero iteraciones y conserva la estimación teórica.

#### `formatear_tabla(resultado)` y `_formatear_celda(valor)`

Convierten las filas numéricas en texto alineado mediante espacios
monoespaciados. La tabla conserva estas columnas:

`Iteración | xl | xu | xr | f(xl) | f(xu) | f(xr) | Ea (%)`

`_formatear_celda` se ocupa de mostrar valores ausentes y no finitos de forma
legible. La gráfica entrega `None` para los puntos donde la función no se
pudo evaluar, de modo que se representen como huecos sin depender de un
marcador numérico especial.

### Ejemplo para la exposición

Para \(f(x)=x^3-x-2\), intervalo \([1,2]\) y tolerancia \(10^{-6}\), el
resultado observado fue aproximadamente \(1.5213804245\). En ese ejemplo se
realizaron 20 iteraciones, igual que la estimación teórica.

---

## 2. Método Regula Falsi

Regula Falsi (falsa posición) conserva un intervalo cuyos extremos tienen
signos opuestos, pero estima la siguiente aproximación con la intersección de
la secante entre \((a,f(a))\) y \((b,f(b))\):

\[
c=a+(b-a)\frac{|f(a)|}{|f(a)|+|f(b)|}.
\]

La expresión equivalente se calcula con pesos normalizados para evitar
desbordamientos al sumar valores de función grandes. Después, se conserva el
subintervalo con cambio de signo. A diferencia de la bisección, la nueva
aproximación no tiene por qué ser el punto medio y un extremo puede permanecer
fijo durante varias iteraciones.

La implementación está en
[`core/metodos_numericos/regla_falsa.py`](../core/metodos_numericos/regla_falsa.py)
y reutiliza el evaluador algebraico seguro del módulo de Bisección. Requiere
un intervalo ordenado con extremos finitos, una tolerancia porcentual positiva
y un máximo entero de iteraciones entre 1 y 100000. Si un extremo es una raíz,
el resultado se informa sin iterar; si no hay cambio de signo, la función
rechaza el intervalo.

La tolerancia está definida como el **error relativo aproximado porcentual**
entre dos valores consecutivos:

\[
E_a=\left|\frac{c_i-c_{i-1}}{c_i}\right|100.
\]

No se compara la tolerancia con \(|f(c)|\), porque este residuo tiene unidades
de función y no representa el mismo criterio. La primera iteración no tiene
un error aproximado previo. Si el cálculo alcanza la tolerancia, encuentra
una raíz exacta o deja de avanzar por precisión, cada estado queda indicado.
Al agotarse las iteraciones, se conserva la última aproximación como dato
diagnóstico, pero `raiz` permanece vacío y `convergio` es falso: no se presenta
como solución convergida.

`resolver_regla_falsa` devuelve los estados, el criterio, la aproximación y
una tabla estructurada con `Iteración`, `a`, `b`, `f(a)`, `f(b)`, `c`, `f(c)`,
`Reemplazo` y `Ea (%)`. La vista
[`core/ui/vista_regla_falsa.py`](../core/ui/vista_regla_falsa.py) presenta
estos resultados en una consola monoespaciada, permite ingresar los extremos
manualmente y utiliza el teclado matemático compartido.

**Ejemplo:** para \(f(x)=e^{-x}-x\), intervalo \([0,1]\) y tolerancia
\(0.00001\%\), la implementación alcanza aproximadamente
\(0.5671432915\) en 9 iteraciones. Con \(f(x)=x^{10}-1\), intervalo \([0,2]\)
y 100 iteraciones, Regula Falsi no alcanza esa tolerancia; el sistema informa
la no convergencia en vez de etiquetar la última aproximación como raíz.

---

## 3. Métodos Abiertos: Newton-Raphson y Secante

El menú principal **Métodos Abiertos** presenta ambos algoritmos dentro del
mismo panel y permite alternar entre ellos con botones de opción. La función,
la tolerancia y el máximo de iteraciones son comunes; Newton usa un valor
inicial `x0`, mientras Secante solicita dos (`x0`, `x1`).

### Newton-Raphson

El método de Newton-Raphson aproxima la raíz de una ecuación no lineal
mediante una recta tangente. Si \(x_n\) es la aproximación actual, la siguiente
aproximación es

\[
 x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.
\]

La implementación en
[`core/metodos_numericos/newton_raphson.py`](../core/metodos_numericos/newton_raphson.py)
acepta una función \(f(x)\) y un valor inicial \(x_0\). La interfaz no solicita
la derivada: el método la aproxima automáticamente con diferencia central:

\[
 f'(x)\approx\frac{f(x+h)-f(x-h)}{2h},\qquad h=10^{-5}\max(1,|x|).
\]

La lógica sigue criterios explícitos de parada: si el residuo \(|f(x_n)|\) cae
por debajo de la tolerancia o el cambio entre aproximaciones
\(|x_{n+1}-x_n|\) es menor que la tolerancia, se detiene el proceso. Si la
pendiente se hace cero o infinita, la función informa el problema y no intenta
continuar con una iteración inválida.

La salida de Newton incluye la raíz aproximada, el criterio de paro y la tabla
de iteraciones.
Además, en cada iteración expone el cálculo de la diferencia central: el paso
`h`, los puntos `x_n+h` y `x_n-h`, las evaluaciones de la función en ambos
puntos, la resta del numerador, el divisor `2h` y el valor resultante de
`f'(x_n)`. Así se puede seguir el origen de cada pendiente usada en la fórmula
de Newton, no solo consultar el valor final.

El evaluador admite `sin`/`sen`, `cos`, `tan`/`tg`, y también las funciones
recíprocas `csc`/`cosec`/`cosecante`, `sec`/`secante` y
`cot`/`cotg`/`cotan`/`cotangente`. Estas últimas se definen como
\(1/\sin(x)\), \(1/\cos(x)\) y \(\cos(x)/\sin(x)\), respectivamente; si el
denominador está próximo a cero, se informa que la función no está definida.

**Caso guía:** para \(f(x)=x^3-x-2\), derivada \(f'(x)=3x^2-1\), valor inicial
\(x_0=1.5\) y tolerancia \(10^{-8}\), el algoritmo reproduce la progresión
analítica esperada: la raíz aproximada se estabiliza en torno a
\(1.521379707\), con convergencia rápida y sin indeterminaciones.

### Método de la Secante

La secante aproxima la pendiente mediante dos puntos consecutivos de la
función, sin calcular una derivada. Su iteración es

\[
x_{n+1}=x_n-\frac{f(x_n)(x_n-x_{n-1})}
{f(x_n)-f(x_{n-1})}.
\]

El backend está en
[`core/metodos_numericos/metodo_secante.py`](../core/metodos_numericos/metodo_secante.py).
Valida ambos puntos iniciales, la tolerancia y el máximo de iteraciones;
reporta un error si el denominador se anula o no es finito. En cada paso guarda
las dos aproximaciones, sus valores de función, la nueva aproximación, el
cambio absoluto y el residuo. La interfaz presenta además el desarrollo de la
fórmula y una tabla de iteraciones. La Secante no requiere cambio de signo, y
puede divergir o estancarse según los valores iniciales.

**Caso de prueba:** para \(f(x)=x^3-x-2\), con `x0 = 1`, `x1 = 2` y tolerancia
\(10^{-8}\), converge en 6 iteraciones a aproximadamente `1.52137970798`.

---

## 4. Cálculo y propagación de errores

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

## 5. Comparación exacta y de punto flotante con matrices

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

## 6. Cómo se conecta con la interfaz

La vista principal es
[`core/ui/vista_metodos_numericos.py`](../core/ui/vista_metodos_numericos.py).
`VistaMetodosNumericos` crea una ventana secundaria, oculta el Dashboard y
presenta un `CTkComboBox` con las áreas del módulo. Al cambiar la opción,
`cambiar_operacion` oculta el panel anterior y muestra el elegido. Los paneles
se conservan una vez creados, por lo que cambiar de menú no obliga a reconstruir
las entradas ni descarta los valores.

[`core/ui/vista_biseccion.py`](../core/ui/vista_biseccion.py) solicita la
función, los extremos manuales `a` y `b`, y la tolerancia. El botón
**Explorar gráfica** abre
[`core/ui/vista_grafica_biseccion.py`](../core/ui/vista_grafica_biseccion.py),
donde se ajusta por separado el rango mínimo y máximo de visualización. Ambas
ventanas comparten la función, pero el rango de la gráfica no determina ni
rellena los extremos del cálculo. El usuario inspecciona la curva y escribe
`a` y `b` explícitamente antes de pulsar **Biseccionar**. La salida presenta la
raíz, el residuo y la tabla de iteraciones. El botón **Borrar** limpia las
entradas.

La demostración inicial usa \(x^2-x-1=0\), `a = 1`, `b = 2` y tolerancia
`10^-6`. Son valores de ejemplo; los extremos siguen siendo editables y la
gráfica no los cambia.

[`core/ui/vista_regla_falsa.py`](../core/ui/vista_regla_falsa.py) recoge la
función, los extremos manuales, la tolerancia de `Ea (%)` y el máximo de
iteraciones. El botón **Resolver** llama a `resolver_regla_falsa`; la salida
distingue una raíz convergida de una última aproximación no convergida.
También usa la entrada algebraica y el teclado matemático compartido. El
ejemplo inicial es \(e^{-x}-x=0\), con `a = 0` y `b = 1`.

El explorador gráfico se comparte entre Bisección y Regula Falsi: cada panel
abre la misma ventana con su función enlazada. Al cambiar de método, se cierra
el teclado y el explorador auxiliares del panel anterior; los datos ingresados
en los paneles se conservan.

El panel **Métodos Abiertos** también abre el explorador con su función actual.
En Newton-Raphson, la ventana
marca los intervalos donde el muestreo observa un cambio de signo o un cero
muestreado e informa cuántas raíces candidatas encontró. En esta vista se puede
hacer clic en un punto de la curva para usar su coordenada `x` como nuevo `x0`.
La gráfica de Métodos Abiertos no muestra marcadores de raíces ni un mensaje
de estado debajo de la gráfica. La cantidad de raíces candidatas sigue siendo
una estimación interna: el muestreo puede omitir raíces tangenciales o muy
cercanas; un cambio de signo garantiza una raíz solo cuando la función es
continua en el intervalo. El punto elegido orienta el método, pero no garantiza
que Newton-Raphson converja.

Antes de iterar, Newton-Raphson analiza el rango visualizado más recientemente
(inicialmente `[-10, 10]`). Si no encuentra cambios de signo ni ceros
muestreados, detiene el método con cero iteraciones y muestra una advertencia.
Esto solo indica que no detectó candidatas en ese rango: no demuestra que la
función carezca de raíces reales fuera de él ni descarta raíces que el muestreo
no haya detectado. Se puede ampliar el rango desde la gráfica o pulsar
**Forzar cálculo** para intentar Newton con el `x0` elegido.

Los campos de función de Bisección, Regula Falsi, del explorador gráfico y de
Propagación incluyen un **teclado matemático**. También admiten escritura
directa en notación algebraica: por ejemplo, `2x`, `x^2`, `(x+1)(x-1)` y
`sin(x)`.
La tecla `xʸ` o el carácter `^` activa el modo exponente: las cifras aparecen
como superíndices visuales (por ejemplo, `x²`) y se convierten internamente a
una potencia antes de evaluarse. `Finalizar exp.` regresa al modo normal; al
escribir `+` o `-` después de un exponente simple, el modo también termina para
que el operador quede fuera de la potencia. Use paréntesis para expresiones
como `x^(2+1)`. El teclado inserta los operadores y funciones en el campo
activo; no incorpora SymPy ni ejecuta el texto ingresado. La normalización
mantiene la evaluación restringida al AST y a las funciones permitidas por el
backend.

En Regula Falsi, el máximo de iteraciones se valida como un entero. Si el campo
está vacío, la interfaz informa que debe ingresarse ese valor; no expone el
mensaje interno de conversión de Python. La tolerancia también tiene una
validación explícita de número finito positivo.

[`core/ui/vista_errores.py`](../core/ui/vista_errores.py) organiza las
herramientas en cinco pestañas:

1. **Errores:** valor aproximado y valor exacto.
2. **Propagación:** función, punto de evaluación \(x\) e incertidumbre
   \(\Delta x\).
3. **Truncamiento y redondeo.**
4. **Punto flotante.**
5. **Gauss-Jordan:** verificación de inversas.

Los callbacks `calcular_errores`, `calcular_propagacion`,
`calcular_redondeo`, `demostrar_float` y `calcular_verificacion` enlazan los
controles con sus funciones de backend. `cargar_hilbert` introduce una matriz
de Hilbert 5×5 de ejemplo y ejecuta su comparación. Las salidas se imprimen en
cajas de texto monoespaciadas para alinear tablas y matrices.

Al cerrar la ventana contenedora se destruye únicamente esa ventana y se
restaura el Dashboard.

---

## 7. Guion breve sugerido

1. **Presentar la organización:** una tarjeta y una ventana para las
   herramientas de métodos numéricos, con un selector para cambiar de área.
2. **Explicar bisección:** ingresar una función, abrir el explorador gráfico y
   ajustar su rango visual. A partir de la curva, elegir y escribir
   manualmente `a` y `b`; después observar el punto medio, la reducción del
   intervalo y la tabla. La gráfica orienta, pero no decide los extremos ni
   garantiza continuidad.
3. **Comparar con Regula Falsi:** usar un intervalo con cambio de signo y
   observar cómo la secante estima `c`. Distinguir la convergencia real de la
   detención por máximo de iteraciones o por pérdida de precisión.
4. **Distinguir los errores:** absoluto mide diferencia en las unidades
   originales; relativo y porcentual comparan la diferencia con el valor de
   referencia.
5. **Demostrar propagación:** comparar \(f'(x)\Delta x\) con el cambio finito
   calculado para \(f(x+\Delta x)-f(x)\).
6. **Mostrar representación finita:** `0.1 + 0.2`, épsilon, overflow y
   underflow explican por qué la computadora no representa todos los reales
   exactamente.
7. **Relacionar con álgebra lineal:** comparar la inversa exacta y la
   aproximada, observar el residuo y el número de condición de Hilbert.
8. **Cerrar con la idea central:** un resultado numérico se entiende mejor
   junto con sus criterios de paro, precisión, errores y estabilidad.

## Archivos de referencia

- [`core/metodos_numericos/biseccion.py`](../core/metodos_numericos/biseccion.py)
- [`core/metodos_numericos/regla_falsa.py`](../core/metodos_numericos/regla_falsa.py)
- [`core/metodos_numericos/operaciones_errores.py`](../core/metodos_numericos/operaciones_errores.py)
- [`core/metodos_numericos/verificacion_matriz.py`](../core/metodos_numericos/verificacion_matriz.py)
- [`core/ui/vista_metodos_numericos.py`](../core/ui/vista_metodos_numericos.py)
- [`core/ui/vista_biseccion.py`](../core/ui/vista_biseccion.py)
- [`core/ui/vista_regla_falsa.py`](../core/ui/vista_regla_falsa.py)
- [`core/ui/vista_errores.py`](../core/ui/vista_errores.py)
