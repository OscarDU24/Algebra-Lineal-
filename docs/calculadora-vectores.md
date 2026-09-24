# Calculadora de vectores

## 1. Proposito

La calculadora de vectores es una ventana educativa de la aplicacion de Algebra
Lineal. Permite introducir dos vectores de la misma dimension, seleccionar una
operacion y consultar tanto el resultado como la formula utilizada.

La ventana principal esta implementada en
`core/ui/vista_vector.py`. La interfaz recibe y valida los datos; la logica
matematica vive en `core/vectores/eliminacionVectores.py`, mientras que las
conversiones numericas estan en `core/vectores/conversionesVectores.py`.

La separacion se decidio para que las operaciones puedan probarse sin abrir
Tkinter y para evitar que las formulas queden mezcladas con la construccion de
botones y campos de entrada.

## 2. Como se abre y como se organiza

Desde el Dashboard se selecciona la tarjeta de operaciones vectoriales. El
Dashboard se oculta temporalmente y crea una ventana `VistaVector`, que es una
ventana secundaria (`CTkToplevel`). Al cerrarla, el Dashboard vuelve a mostrarse.

La vista tiene tres zonas:

1. **Configuracion superior:** dimension del vector, boton para generar entradas y
   boton para limpiarlas.
2. **Zona central:** campos de `u` y `v`, uno por componente, y una vista previa
   que se actualiza mientras se escribe.
3. **Zona inferior:** operacion, escalar opcional, formato numerico, boton de
   calculo y visor de resultados.

La dimension inicial es 3. El usuario puede cambiarla y pulsar **Generar
Vectores**. Al regenerar, se eliminan las entradas anteriores y se crean listas
nuevas con la dimension solicitada.

## 3. Representacion interna

Los vectores se representan como listas ordenadas de numeros `float`:

```text
u = [u1, u2, ..., un]
v = [v1, v2, ..., vn]
```

Los widgets de la interfaz no se envian directamente a la logica matematica. Los
metodos `obtener_vector_u()` y `obtener_vector_v()` recorren sus entradas, limpian
el texto, convierten cada valor y construyen una lista numerica.

Esta decision tiene dos ventajas:

- La logica matematica trabaja con datos simples y no depende de CustomTkinter.
- La validacion queda concentrada antes de ejecutar una formula.

## 4. Entradas aceptadas y conversiones

Cada componente puede escribirse como:

- Entero: `5`
- Decimal: `-3.2`
- Fraccion: `1/3`
- Cero o valores negativos: `0`, `-7`, `-1/2`

La funcion `convertir_a_decimal()` intenta primero interpretar la entrada con
`fractions.Fraction` y, si no puede, intenta convertirla a `float`. Si ambas
conversiones fallan, devuelve `None`.

Por tanto, las entradas vacias, textos como `abc` y expresiones matematicas como
`2+3` no son componentes validos. Tampoco se evalua codigo ni se aceptan
expresiones con variables.

Una fraccion como `1/3` se convierte internamente a un `float`. Esto simplifica
las operaciones y mantiene una implementacion basada en la biblioteca estandar,
sin NumPy, SciPy ni SymPy. La consecuencia es que el calculo se realiza con
aritmetica de punto flotante, no con fracciones simbolicas exactas.

### Formatos de salida

El selector permite elegir:

- **Fracciones:** convierte el resultado decimal a una fraccion reducida usando
  `Fraction(...).limit_denominator()`.
- **Decimales:** muestra dos cifras despues del punto mediante `f"{numero:.2f}"`.

El formato afecta principalmente a la presentacion, no cambia la operacion
interna. Por ejemplo, el resultado interno de una division puede ser
`0.333333...`, mientras que la salida puede verse como `1/3` o `0.33`.

## 5. Flujo de calculo

Cuando se pulsa **Calcular**, `accion_calcular()` realiza este flujo:

1. Lee el nombre de la operacion seleccionada.
2. Obtiene y convierte el vector `u`.
3. Obtiene y convierte el vector `v`.
4. Prepara una cabecera con los vectores capturados.
5. Llama a la funcion matematica correspondiente de `eliminacionVectores`.
6. Agrega la formula y el resultado al visor.
7. Si ocurre un `ValueError`, muestra el mensaje sin cerrar la ventana.

Un detalle importante: actualmente `accion_calcular()` obtiene **ambos vectores
antes de revisar que operacion se eligio**. Por eso, aunque una operacion use solo
`u` (por ejemplo, `Magnitud de u`), los campos de `v` tambien deben estar llenos y
ser validos.

## 6. Operaciones disponibles

### 6.1 Suma

Suma componente por componente:

$$
u + v = [u_1+v_1, u_2+v_2, \ldots, u_n+v_n]$$

Requiere que ambos vectores tengan la misma dimension.

### 6.2 Resta

Resta componente por componente:

$$
u - v = [u_1-v_1, u_2-v_2, \ldots, u_n-v_n]$$

Tambien requiere dimensiones iguales.

### 6.3 Multiplicacion por escalar

Lee el escalar del campo adicional y multiplica `u`:

$$
c u = [cu_1, cu_2, \ldots, cu_n]$$

El escalar acepta los mismos formatos que un componente: enteros, decimales y
fracciones. Si el campo esta vacio o es invalido, se informa el error.

### 6.4 Producto punto

Devuelve un numero:

$$
u \cdot v = u_1v_1 + u_2v_2 + \cdots + u_nv_n$$

La interfaz muestra cada producto y la suma final. Los vectores deben tener la
misma dimension.
|
### 6.5 Magnitud

Calcula la longitud euclidiana del vector:

$$
\|u\| = \sqrt{u_1^2 + u_2^2 + \cdots + u_n^2}
$$

Existe una opcion separada para la magnitud de `u` y para la magnitud de `v`.

### 6.6 Normalizacion

Divide cada componente entre la magnitud:

$$
\hat{u} = \frac{u}{\|u\|}
$$

No se puede normalizar el vector cero. El proyecto usa
`TOLERANCIA = 1e-9` para tratar como cero una magnitud suficientemente pequena y
evitar divisiones inestables.

### 6.7 Producto cruz

El producto cruz esta restringido a vectores de tres componentes:

$$
u \times v = [u_2v_3-u_3v_2,\; u_3v_1-u_1v_3,\; u_1v_2-u_2v_1]$$

La funcion rechaza cualquier dimension diferente de 3. El resultado es un vector
perpendicular a los dos vectores de entrada, salvo las consideraciones usuales
cuando los vectores son paralelos o alguno es cero.

### 6.8 Angulo entre vectores

Usa la relacion:

$$
\cos(\theta) = \frac{u \cdot v}{\|u\|\|v\|}
$$

El resultado se muestra en grados. La implementacion limita el valor del coseno
al intervalo `[-1, 1]` para evitar errores numericos cerca de los extremos.

No se puede calcular el angulo si alguno de los vectores es cero. La implementacion
actual calcula la aproximacion del angulo dentro de `eliminacionVectores.py`; no
usa una dependencia externa de algebra o trigonometria.

### 6.9 Proyeccion de `u` sobre `v`

Calcula la proyeccion ortogonal:

$$
\operatorname{proj}_v(u) = \frac{u \cdot v}{\|v\|^2}v
$$

No se puede proyectar sobre el vector cero porque el denominador seria cero.

### 6.10 Distancia entre `u` y `v`

Calcula la distancia euclidiana como la magnitud de la diferencia:

$$
d(u,v) = \|u-v\|
$$

Requiere vectores de la misma dimension.

## 7. Validaciones y mensajes de error

La dimension debe ser un entero estrictamente positivo. Si se escribe `0`, un
numero negativo, un decimal o texto, no se generan los campos y se muestra un
mensaje de error.

Cada componente se valida individualmente. Una entrada vacia produce un mensaje
que identifica el componente, por ejemplo `La componente u2 esta vacia.`. Un valor
no interpretable produce un mensaje que incluye el texto recibido.

Las operaciones binarias comprueban que ambas listas tengan la misma longitud.
Esta validacion evita combinar elementos de espacios distintos y se realiza en la
capa matematica, no solo en la interfaz.

Los casos especiales principales son:

| Caso | Respuesta |
| --- | --- |
| Dimension no positiva | No se generan vectores |
| Componente vacio | Error de entrada con el indice |
| Texto no numerico | Error de entrada |
| Dimensiones distintas | `ValueError` de dimensiones |
| Normalizacion del vector cero | Error por magnitud nula |
| Angulo con vector cero | Error por magnitud nula |
| Proyeccion sobre vector cero | Error por denominador nulo |
| Producto cruz no tridimensional | Error: solo esta definido en R3 |
| Escalar vacio o invalido | Error de escalar |

## 8. Por que se eligio este diseño

### Separacion entre interfaz y calculo

La ventana se ocupa de capturar, convertir y presentar. El modulo de operaciones
se ocupa de formulas, dimensiones y excepciones matematicas. Asi se puede probar
una funcion con listas como `[[1, 2], [3, 4]]` sin crear una ventana grafica.

### Listas de Python

Para una calculadora educativa de dimensiones pequenas, las listas hacen visible
la relacion entre la teoria y el codigo. Ademas, evitan agregar dependencias
pesadas y permiten mostrar facilmente los pasos en texto.

### Una ventana para dos vectores

La interfaz se centra en las operaciones basicas entre `u` y `v`. La dimension se
puede cambiar, pero la estructura mantiene dos vectores para que las operaciones
sean faciles de comparar visualmente.

### Vista previa

La vista previa no calcula resultados. Solo refleja lo que el usuario esta
escribiendo, usando `_` para campos vacios. Esto permite detectar rapidamente si
se genero la dimension correcta sin mezclar datos incompletos con el calculo real.

### Salida explicativa

El visor muestra los vectores de entrada, la formula y el resultado. La finalidad
no es actuar como una caja negra: el usuario debe poder relacionar la salida con
la formula de algebra lineal que selecciono.

## 9. Que no hace esta calculadora

Para evitar confusiones:

- No resuelve sistemas `Ax = b` desde esta ventana.
- No calcula transpuestas de matrices desde esta ventana.
- No trabaja con matrices como entrada principal.
- No realiza algebra simbolica ni conserva fracciones exactas durante todo el
  calculo.
- No acepta expresiones como `sqrt(2)`, `2+3` o `sin(1)` en los campos.
- No necesita que la dimension sea 2 o 3, excepto para el producto cruz, que exige
  dimension 3.

Las operaciones con matrices, transposicion, ecuaciones matriciales y sistemas
pertenecen a `core/ui/vista_matricial.py` y a los modulos dentro de
`core/matriciales/`. La funcion `vectores_a_matriz()` existe en el modulo de
operaciones vectoriales para convertir una ecuacion vectorial a una matriz
ampliada, pero no es una opcion del selector actual de `VistaVector`.

## 10. Como probarla manualmente

### Prueba basica

1. Abrir **Productos entre Matrices (Vectores)** desde el Dashboard.
2. Mantener dimension `3` y pulsar **Generar Vectores**.
3. Introducir `u = [1, 2, 3]` y `v = [4, 5, 6]`.
4. Seleccionar **Suma** y pulsar **Calcular**.
5. Comprobar que el resultado sea `[5, 7, 9]`.

### Prueba de fracciones

Introducir `1/2`, `-3/4` y `2` en los componentes. Seleccionar **Fracciones** y
comprobar que los resultados se presenten como fracciones reducidas cuando la
conversion sea representable con la aproximacion utilizada.

### Prueba de dimension invalida

Probar `0`, `-2`, `2.5` y texto en el campo de dimension. La ventana debe conservarse
abierta y mostrar el error sin crear una estructura parcial.

### Pruebas de casos especiales

- Producto cruz con dimension 2: debe rechazarse.
- Normalizar `[0, 0, 0]`: debe rechazarse.
- Proyectar sobre `[0, 0, 0]`: debe rechazarse.
- Angulo con un vector cero: debe rechazarse.
- Suma con un campo vacio: debe identificar el componente faltante.
- Magnitud de `u` con `v` vacio: actualmente tambien falla, porque la accion
  principal valida ambos vectores antes de seleccionar la rama.

## 11. Como probar la logica sin interfaz

Desde la raiz del proyecto puede ejecutarse una prueba directa:

```powershell
.\.venv\Scripts\python.exe -c "from core.vectores import eliminacionVectores as ev; assert ev.sumar_vectores([1,2,3],[4,5,6]) == [5,7,9]; print('Prueba correcta')"
```

Tambien se pueden probar los casos que deben fallar:

```powershell
.\.venv\Scripts\python.exe -c "from core.vectores import eliminacionVectores as ev; 
try:
    ev.normalizar_vector([0,0,0])
except ValueError as error:
    print(error)"
```

La primera prueba valida el resultado. La segunda valida que el error esperado
se convierta en un mensaje controlado por la interfaz.

## 12. Mantenimiento y ampliaciones futuras

Para agregar una operacion nueva se recomienda seguir este orden:

1. Implementar la formula en `core/vectores/eliminacionVectores.py`.
2. Validar alli las dimensiones y los casos matematicamente imposibles.
3. Agregar el texto de la operacion al `CTkComboBox` de `VistaVector`.
4. Agregar una rama en `accion_calcular()`.
5. Mostrar formula, datos de entrada y resultado usando los formateadores actuales.
6. Probar primero la funcion con listas y despues el flujo grafico.

Si una operacion necesita datos distintos de `u`, `v` o un escalar, conviene
ampliar la interfaz antes de reutilizar campos de forma ambigua. Por ejemplo, una
operacion matricial no debe incorporarse a esta ventana sin agregar entradas y
validaciones para matrices; debe vivir en `VistaMatricial`.

Una mejora futura razonable seria validar solo los vectores que necesita cada
operacion. Eso permitiria calcular la magnitud de `u` aunque `v` este vacio, sin
cambiar las formulas ni la representacion interna.

## 13. Archivos relacionados

- `core/ui/vista_vector.py`: interfaz, entradas, selector, previsualizacion y salida.
- `core/vectores/eliminacionVectores.py`: operaciones matematicas y validaciones.
- `core/vectores/conversionesVectores.py`: conversion entre texto, decimal y fraccion.
- `core/vectores/constantesVectores.py`: tolerancia numerica.
- `core/vectores/entradaVectores.py`: entrada por consola reutilizable para pruebas o
  flujos no graficos.
- `core/vectores/utilidadesVectores.py`: copia independiente de vectores.
- `core/ui/dashboard.py`: apertura y cierre de la ventana desde el Dashboard.
