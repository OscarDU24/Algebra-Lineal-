# Exposición del jueves 15: determinantes y portada de HeyAlgb

Este documento resume dos partes del proyecto:

1. El cálculo de determinantes, sus métodos y el análisis previo de eficiencia.
2. La evolución de la portada y la adaptación de recursos visuales inspirados en
   una referencia HTML a widgets y dibujos nativos de Tkinter.

Las rutas citadas son relativas a la raíz del repositorio.

---

## 1. Módulo de determinantes

### 1.1 Organización y responsabilidades

La interfaz de determinantes se encuentra en
[`core/ui/vista_determinantes.py`](../core/ui/vista_determinantes.py), y la
implementación matemática principal en
[`core/determinantes/operaciones_determinantes.py`](../core/determinantes/operaciones_determinantes.py).
La vista recoge el orden y los valores de la matriz, deja elegir el formato y
el método, presenta la recomendación y muestra el procedimiento. El módulo de
lógica valida los datos, realiza el cálculo y produce el texto explicativo.

La matriz debe ser cuadrada, no vacía y numérica. La entrada se convierte a
`fractions.Fraction`, por lo que los cálculos racionales —incluidas las
fracciones introducidas como `1/3`— se conservan exactamente. El modo
«Decimales» solo cambia cómo se presenta el resultado; no cambia la aritmética
interna.

Por ejemplo, el valor introducido como `0.75` se normaliza como la fracción
exacta \(3/4\). Las entradas vacías o inválidas generan un error con la
coordenada de la celda, en vez de llegar silenciosamente a un cálculo parcial.

### 1.2 Métodos matemáticos

#### Cálculo directo para órdenes 1, 2 y 3

La opción «Automático» utiliza el procedimiento directo hasta orden 3:

- **1×1:** el determinante es el único elemento.
- **2×2:** para \(A=\begin{bmatrix}a&b\\c&d\end{bmatrix}\),
  \(\det(A)=ad-bc\).
- **3×3:** se aplica la regla de Sarrus, sumando los tres productos de las
  diagonales descendentes y restando los tres productos de las diagonales
  ascendentes.

El informe de Sarrus 3×3 muestra la operación simbólica, la sustitución de los
valores, los productos parciales y la resta final. De esta forma se pueden
seguir los signos y verificar de dónde sale el determinante.

#### Expansión por cofactores

La expansión recursiva se hace por la primera fila. Para cada elemento
\(a_{1j}\):

1. Se elimina la primera fila y la columna \(j\), formando el menor
   \(M_{1j}\).
2. Se calcula su determinante. En el caso 2×2 se muestra explícitamente
   \(ad-bc\); los órdenes superiores vuelven a expandirse recursivamente.
3. Se multiplica el menor por el elemento y por su signo posicional
   \((-1)^{1+j}\).
4. Se suman los aportes con sus signos.

En la salida se imprimen las submatrices y las cuentas intermedias. Es un
método pedagógico adecuado para matrices pequeñas, pero el número de
subproblemas crece factorialmente y no es conveniente para órdenes grandes.

#### LU con pivoteo parcial

La factorización implementada satisface \(P A=L U\):

- \(U\) parte de la matriz original y se transforma mediante eliminación
  gaussiana.
- Los multiplicadores usados para eliminar elementos se guardan en \(L\).
- En cada columna se elige como pivote el elemento de mayor valor absoluto
  entre las filas restantes.
- Si el pivote está en otra fila, se intercambian filas. Cada intercambio
  cambia el signo del determinante.

Una vez triangularizada la matriz:

\[
\det(A)=(-1)^s\prod_{i=1}^{n}u_{ii},
\]

donde \(s\) es el número de intercambios. Si una columna no tiene pivote
distinto de cero, la matriz es singular y el determinante es cero. El informe
incluye los intercambios, las eliminaciones, los estados de \(L\) y \(U\), la
diagonal y el producto final.

#### Sarrus extendido para 4×4

La regla clásica de Sarrus solo se aplica a 3×3. En el proyecto también hay
una extensión didáctica para 4×4 basada en tres etapas de permutación de
columnas:

1. Matriz original, con signo inicial positivo.
2. Intercambio de las columnas 2 y 3, con signo inicial negativo.
3. Sobre la segunda etapa, intercambio de las columnas 3 y 4, con signo
   inicial positivo.

En cada etapa se copian las tres primeras columnas a la derecha de la matriz
resultante y se calculan productos diagonales con signos alternados. El
procedimiento imprime la matriz extendida, los términos simbólicos, sus
sustituciones y el subtotal. La suma de los tres subtotales es el determinante.
La implementación contrasta este resultado con LU mediante pruebas para
matrices regulares y singulares.

Sarrus solo se ofrece en el selector cuando el orden es 3 o 4. Si se solicita
desde otro contexto, la lógica genera `ValueError` con el rango permitido.
Para órdenes mayores la interfaz muestra una advertencia.

### 1.3 Qué hace el análisis previo de eficiencia

Cada vez que se modifica una celda, la vista intenta leer la matriz completa.
Mientras falten datos o exista una entrada inválida, el panel solicita
completarla y, si el orden excede 4, recuerda que Sarrus no está disponible.
Con una matriz válida, llama a `analizar_eficiencia_determinante` y muestra:

- El orden de la matriz.
- Una estimación didáctica del crecimiento de cofactores: \(O(n!)\). Hasta
  orden 20 se muestra \(n!\) como cifra; para órdenes mayores se conserva la
  expresión simbólica.
- Una estimación para LU de aproximadamente
  \(\lfloor 2n^3/3\rfloor+n\), identificada como \(O(n^3)\).
- Una recomendación textual y el nombre del método recomendado.

Los umbrales son:

| Orden | Recomendación |
|---|---|
| \(n\leq3\) | Cofactores; el texto indica que Cofactores o Sarrus tienen un costo práctico parecido para estos tamaños. |
| \(n=4\) | LU / Triangulación; cofactores todavía es viable. |
| \(n\geq5\) | LU / Triangulación, con advertencia fuerte por el crecimiento factorial de cofactores. |

Estas cifras comparan el crecimiento teórico aproximado, no miden el tiempo
real de ejecución ni consideran el hardware. Son orientación para escoger un
método, no una predicción de duración exacta. La recomendación depende del
orden de la matriz; no inspecciona patrones numéricos como ceros, sparsidad o
singularidad para escoger otro método.

**Importante: recomendación y modo «Automático» no son exactamente lo mismo.**
El análisis recomienda cofactores para órdenes 1 a 3 porque es un algoritmo
simple y didáctico (y menciona Sarrus para 3×3). En cambio, al pulsar Calcular
con «Automático», la vista despacha a cálculo directo hasta 3×3 y a LU para
órdenes mayores. Por ello, para 3×3 la ejecución directa usa Sarrus, aunque el
panel de recomendación devuelva «Cofactores» como sugerencia general.

### 1.4 Pruebas

[`tests/test_determinantes.py`](../tests/test_determinantes.py) verifica,
entre otros casos:

- Conversión exacta y rechazo de entradas inválidas.
- Recomendaciones en varios órdenes.
- Consistencia entre LU, cofactores y Sarrus extendido.
- Signo por intercambio de filas y matrices singulares.
- Desglose detallado de Sarrus 3×3, Sarrus extendido 4×4 y cofactores.

---

## 2. Interfaz de inicio y adaptación de la referencia HTML

### 2.1 HTML como referencia, no como componente ejecutado

La referencia HTML se analizó como guía visual y de comportamiento: estilo
Persona 5, letras con aspecto de recorte, selección oblicua, colores de alto
contraste y transición de entrada. La aplicación no carga ni ejecuta ese HTML,
JavaScript o CSS dentro de la ventana. Los efectos se recrearon con las
herramientas disponibles en la aplicación: `tk.Canvas`, Tkinter,
CustomTkinter y Pillow.

Esta adaptación conserva el carácter visual de la referencia, pero no pretende
ser una reproducción pixel a pixel del navegador. Las coordenadas y los tamaños
se calculan en relación con las dimensiones actuales de la ventana.

### 2.2 Composición y recursos gráficos

La implementación está en
[`core/ui/vista_inicio.py`](../core/ui/vista_inicio.py). La portada usa un
`tk.Canvas` que ocupa la ventana y coloca sobre él fondo, logotipos, textos,
créditos y controles dibujados:

- `FondoMAIN.png` es el fondo decorativo. Pillow lo ajusta con `ImageOps.fit`
  en modo *cover*: mantiene la proporción, llena el Canvas y recorta el
  excedente alrededor del centro.
- `HeyAlgbLogoBlanco.png` es el logo principal, escalado con Pillow según el
  tamaño disponible.
- `UAMICON.png` se presenta como identidad institucional junto a un texto
  limpio de Facultad.
- Los retratos de los integrantes se cargan en RGBA para conservar la
  transparencia, se reducen con Pillow y se colocan en la zona de créditos.

El orden de creación y elevación de elementos del Canvas determina las capas:
el fondo permanece detrás y los textos, botones y elementos decorativos se
dibujan por encima. Para evitar el parpadeo de imágenes grandes al arrancar, el
logo principal, el de UAM y los retratos comienzan con una imagen transparente
de 1×1. El primer redibujado real se realiza cuando el Canvas ya tiene
dimensiones suficientes.

### 2.3 Fuentes locales

La clase mantiene una lista de fuentes locales bajo `core/assets/fonts/`.
En Windows registra las disponibles en el proceso mediante
`AddFontResourceExW` y las retira al destruir el marco de inicio. Pillow carga
esas fuentes por archivo para renderizar glifos. Si falta un archivo, se
advierte y la lista de fuentes utilizables se limita a las disponibles.

La portada combina tipografías de alto impacto para el estilo del menú con
Helvetica Now Display Bold para el texto institucional. Los PNG y los TTF son
recursos locales del proyecto: no hay dependencia de una fuente remota ni de
un navegador.

### 2.4 Efecto «ransom note»

La función `_dibujar_texto_ransom` crea una imagen Pillow por cada carácter:

1. Elige una fuente de la lista disponible y le asigna un tamaño levemente
   variable.
2. Dibuja el carácter sobre un pequeño lienzo, opcionalmente con un recuadro
   de color.
3. Lo rota unos grados y usa el ancho real del sprite resultante para
   posicionar el siguiente carácter sin superposición.
4. Convierte el sprite en `ImageTk.PhotoImage` y lo coloca como imagen dentro
   del Canvas.

El subtítulo de la portada usa esta técnica para obtener irregularidad y
dinamismo. Los nombres de los integrantes también usan sprites de letras. El
texto de la Facultad se mantiene intencionalmente fuera del efecto: se dibuja
como un único texto nativo de Canvas, uniforme y en Helvetica Now Display Bold.

En los botones, las palabras se capitalizan alternadamente (por ejemplo,
`InIcIaR` y `AyUdA`) y sus letras se vuelven sprites con variación de tamaño y
rotación. El procedimiento se comparte con los demás textos para mantener
legibilidad y aprovechar el mismo cálculo de anchos.

### 2.5 Botones de Canvas e interacción

Los botones no son widgets `Button`: cada uno es un grupo de elementos del
Canvas asociado a un tag. El grupo incluye:

- Un trapecio de fondo, cuyo color depende de la acción.
- Un respaldo blanco y un detalle rojo que se muestran en hover.
- Una insignia poligonal con el número `1` o `2`.
- El texto construido carácter por carácter.

Los eventos `<Enter>`, `<Leave>` y `<Button-1>` se enlazan al tag de cada
opción. Al entrar:

- El conjunto cambia a su estado activo, se invierten los colores de la
  insignia y se activa el contraste del texto.
- El conjunto se desplaza horizontalmente para dar sensación de *hop*.
- Se reproduce el efecto de cursor.

Al salir del grupo, la vista confirma que el puntero ya no esté sobre otra
parte del mismo tag antes de restaurar el estado, evitando que el hover
parpadee al moverse entre el trapecio, el número y los glifos. El clic en
«Iniciar» reproduce una transición diagonal antes de invocar el callback que
abre el Dashboard; «Ayuda» abre su ventana correspondiente. También se
conservan las teclas de navegación y los atajos numéricos.

El fondo de las palabras ransom se dibuja usando Canvas; por ello, el orden de
capas de los polígonos se controla explícitamente para que queden detrás del
bloque del botón y no tapen el texto.

### 2.6 Controles CustomTkinter y sonido

La portada mezcla deliberadamente tecnologías: Canvas de Tkinter permite
control geométrico fino sobre el fondo, sprites y polígonos; el interruptor
de música y la ventana de ayuda usan CustomTkinter. El cambio de música sigue
delegándose al `AudioManager`, que centraliza música y efectos.

El efecto de cursor se reproduce cuando se entra a una opción nueva, no con
cada movimiento dentro del mismo botón. La música de inicio, su interruptor y
la llamada al Dashboard siguen conectados a los objetos de la aplicación.

### 2.7 Créditos e integrantes

Los retratos se relacionan con sus nombres de equipo mediante
`VistaInicio.INTEGRANTES`:

| Nombre mostrado | Archivo de imagen |
|---|---|
| Liang Woo | `Liang_Amamiya.png` |
| Óscar Durán | `Oscar_Sakamoto.png` |
| Diego Gómez | `Diego_Kitagawa.png` |
| Carlos Aguirre | `Charly_Sakura.png` |

Las imágenes provistas con esos nombres se conservan en la carpeta de assets,
con alpha, y se acomodan en tarjetas dentro de la franja de créditos. Esta
relación centralizada ayuda a mantener orden y nombre alineados si luego se
actualiza el diseño.

### 2.8 Verificación de portada

[`tests/test_vista_inicio.py`](../tests/test_vista_inicio.py) comprueba el
orden y los nombres de los créditos y el recorte centrado del fondo en modo
cover. Durante el desarrollo también se comprobaron en ejecución el
redimensionado del Canvas, el tamaño inicial seguro de los iconos, el estado de
hover, el desplazamiento, el sonido y la transición de inicio.

---

## Resumen para la exposición

- La lógica de determinantes conserva aritmética racional exacta y presenta
  procedimientos, no solo resultados.
- Cofactores es claro para aprender, Sarrus resuelve 3×3 y tiene una extensión
  específica y limitada a 4×4, y LU es la opción escalable para órdenes mayores.
- El análisis previo compara órdenes de crecimiento para orientar al usuario.
  La opción «Automático» usa una regla de ejecución definida en la interfaz y
  puede no coincidir literalmente con el nombre recomendado.
- La portada no incrusta HTML. Reinterpreta su lenguaje visual con Canvas,
  Pillow, fuentes locales y eventos Tkinter, manteniendo en CustomTkinter los
  controles que ya pertenecen a ese toolkit.
- Los recursos gráficos de equipo e institución se integran como assets
  locales, con escalado y transparencia adecuados para el redimensionado.
