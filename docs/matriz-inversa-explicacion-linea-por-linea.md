# Matriz inversa: explicación línea por línea

## 1. Qué hace esta funcionalidad

La aplicación ofrece dos usos relacionados, pero distintos, de la matriz inversa:

- **Matriz pura (`A⁻¹`)**: recibe solamente `A` y calcula su inversa.
- **Sistema por inversa (`Ax=b`)**: recibe `A` y `b`, calcula `A⁻¹` y después obtiene `x=A⁻¹b`.

Ambos requieren que `A` sea cuadrada e invertible. Los métodos de eliminación normales (Escalonado, Gauss y Gauss-Jordan) continúan disponibles para sistemas que no cumplan esa condición.

La implementación se reparte entre:

- `core/lineal/solucion.py`: algoritmo de inversión, producto entre matrices y enrutamiento matemático.
- `core/ui/vista_matriz.py`: selector, checkbox, cuadrícula, presentación y conexión con el motor.

## 2. Tolerancia numérica

En `solucion.py` aparece:

```python
TOLERANCIA_INVERSA = 1e-10
```

Es un umbral para decidir si un pivote puede considerarse cero. Como los cálculos usan `float`, un resultado que matemáticamente sería cero puede aparecer como un residuo diminuto. La tolerancia evita tratar ese ruido como un pivote válido.

No se calcula el determinante de forma explícita. El algoritmo detecta la singularidad cuando no encuentra un pivote suficientemente distinto de cero.

## 3. `invertir_matriz_gauss_jordan`

La función implementa el proceso:

$$
[A \mid I] \longrightarrow [I \mid A^{-1}]
$$

### Firma y validación

```python
def invertir_matriz_gauss_jordan(matriz, devolver_pasos=False):
```

- `matriz` es `A`, representada como lista de filas.
- `devolver_pasos=False` mantiene una llamada sencilla que devuelve solo la inversa.
- Si se activa `devolver_pasos`, también devuelve la traza usada por la interfaz.

```python
if not matriz or any(len(fila) != len(matriz) for fila in matriz):
    raise ValueError("La matriz debe ser cuadrada y no estar vacía.")
```

Rechaza una matriz vacía o no cuadrada. La prueba compara la longitud de cada fila con el número de filas, por lo que `A` debe medir `n × n`.

### Construcción de `[A | I]`

```python
dimension = len(matriz)
```

Guarda `n`, el número de filas y columnas de `A`.

```python
aumentada = [
    list(fila) + [1.0 if fila_indice == columna else 0.0
                  for columna in range(dimension)]
    for fila_indice, fila in enumerate(matriz)
]
```

Para cada fila de `A`, agrega una fila correspondiente de la identidad:

- Cuando `fila_indice == columna`, agrega `1.0`.
- En las demás posiciones, agrega `0.0`.
- `list(fila)` crea una copia de la fila original para no modificar `A`.

Con `A=[[2,1],[1,1]]`, empieza así:

```text
[A | I] =
[ 2  1 | 1  0 ]
[ 1  1 | 0  1 ]
```

### Registro de pasos

```python
pasos = [({"tipo": "inicial"}, [fila[:] for fila in aumentada])]
```

Guarda la matriz aumentada inicial. Cada elemento de `pasos` es una pareja:

```text
(descripción estructurada de la operación, copia de la matriz resultante)
```

`fila[:]` copia cada fila para que las operaciones posteriores no alteren las instantáneas anteriores.

### Iteración y pivoteo parcial

```python
for columna in range(dimension):
```

Procesa una columna por cada pivote de la matriz.

```python
fila_pivote = max(
    range(columna, dimension),
    key=lambda indice: abs(aumentada[indice][columna])
)
```

Busca, entre la fila actual y las que están debajo, el elemento de mayor valor absoluto en la columna. Elegir un pivote grande reduce errores de redondeo y permite intercambiar filas si la posición diagonal contiene cero.

```python
if abs(aumentada[fila_pivote][columna]) < TOLERANCIA_INVERSA:
    raise ValueError(...)
```

Si incluso el mejor candidato es casi cero, la matriz no tiene inversa numéricamente estable. La interfaz convierte este `ValueError` en un mensaje comprensible.

```python
if fila_pivote != columna:
    aumentada[columna], aumentada[fila_pivote] = ...
```

Mueve el mejor pivote a la diagonal mediante un intercambio de filas. La operación se agrega a `pasos` junto con una copia de la matriz nueva, para que la interfaz pueda mostrarla.

### Normalizar el pivote

```python
pivote = aumentada[columna][columna]
aumentada[columna] = [valor / pivote for valor in aumentada[columna]]
```

Divide toda la fila pivote por su pivote. Así, el valor diagonal pasa a ser `1`.

```python
fila_pivote_normalizada = aumentada[columna][:]
```

Guarda una copia inmutable de la fila normalizada. Las eliminaciones de otras filas deben usar esta misma fila, no una fila que vaya cambiando.

El paso de normalización también se guarda en la traza.

### Eliminar el resto de la columna

```python
for indice_fila in range(dimension):
    if indice_fila == columna:
        continue
```

Recorre todas las filas, excepto la fila pivote. Gauss-Jordan elimina valores tanto debajo como encima del pivote.

```python
factor = aumentada[indice_fila][columna]
```

Obtiene cuánto de la fila pivote debe restarse para anular la entrada de esa fila.

```python
if abs(factor) < TOLERANCIA_INVERSA:
    aumentada[indice_fila][columna] = 0.0
    continue
```

Si el factor es prácticamente cero, normaliza ese pequeño residuo a cero y evita una operación innecesaria.

```python
fila_actual = aumentada[indice_fila]
fila_nueva = []
for indice_elemento in range(len(fila_actual)):
    valor_nuevo = (
        fila_actual[indice_elemento]
        - factor * fila_pivote_normalizada[indice_elemento]
    )
    fila_nueva.append(valor_nuevo)
aumentada[indice_fila] = fila_nueva
```

Construye una fila completamente nueva con la operación elemental:

$$
F_i \leftarrow F_i - (factor)F_{pivote}
$$

Se conserva la fila pivote en `fila_pivote_normalizada` y no se reemplaza la fila actual hasta haber calculado todos sus componentes. La nueva matriz queda almacenada en la traza.

### Extraer y devolver la inversa

```python
inversa = [fila[dimension:] for fila in aumentada]
```

Al terminar, la parte izquierda es la identidad. Por eso, las columnas a la derecha de `dimension` forman `A⁻¹`.

```python
if devolver_pasos:
    return inversa, pasos
return inversa
```

El motor puede usarse de dos maneras:

- Solicitar solamente `A⁻¹`.
- Solicitar `A⁻¹` y todos los pasos para presentarlos en la interfaz.

## 4. Multiplicar matrices

La función auxiliar `multiplicar_matrices(matriz_a, matriz_b)` se usa para:

- Calcular `A⁻¹ · b`, convirtiendo `b` en matriz columna.
- Comprobar `A · A⁻¹`.

Primero valida que las matrices existan, que sean rectangulares y que las columnas de `A` coincidan con las filas de `B`.

```python
for fila_a in range(filas_a):
    fila_resultado = []
    for columna_b in range(columnas_b):
        suma = 0.0
        for indice in range(columnas_a):
            suma += matriz_a[fila_a][indice] * matriz_b[indice][columna_b]
        fila_resultado.append(suma)
    resultado.append(fila_resultado)
```

Los tres bucles implementan el producto fila por columna:

$$
(AB)_{ij}=\sum_k A_{ik}B_{kj}
$$

No se usa NumPy ni otra biblioteca de cálculo.

## 5. Enrutador matemático

```python
def enrutar_resolucion_matricial(
    matriz_A,
    vector_b=None,
    formato_fracciones=False,
    metodo="gauss_jordan"
):
```

Esta función decide qué flujo matemático ejecutar:

- `vector_b is None`: modo matriz pura, devuelve `A⁻¹` y los pasos.
- `vector_b` contiene valores: sistema `Ax=b`, resuelto con el método elegido.

En la rama de matriz pura:

```python
matriz_inversa, pasos = invertir_matriz_gauss_jordan(
    matriz_A,
    devolver_pasos=True
)
```

Solicita la inversa y su traza. Devuelve ambas en un diccionario para que la vista no tenga que volver a calcularlas.

En la rama de sistema, el enrutador crea `[A|b]`, llama a la eliminación por filas y devuelve matriz reducida, pivotes, clasificación y solución cuando existe. Esta rama conserva los métodos tradicionales.

`formato_fracciones` viaja en el resultado para registrar la selección de presentación; la conversión visual concreta la realiza `VistaMatriz`.

## 6. Selector y checkbox en `VistaMatriz`

El selector incluye **Matriz pura (A⁻¹)** junto con los métodos de sistema. Al cambiar el método:

- En un método de sistema, la cuadrícula contiene `n` coeficientes y una columna TI para `b`.
- En matriz pura, la cuadrícula contiene solo las `n` columnas de `A`.
- Al entrar en matriz pura aparece el checkbox **Incluir términos independientes (b)**.

`BooleanVar(value=False)` guarda el estado del checkbox. Su callback `al_cambiar_inclusion_b()`:

1. Lee los valores actuales de `A`.
2. Actualiza el texto del botón.
3. Vuelve a generar la cuadrícula con o sin la columna `b`.
4. Restaura en las nuevas celdas los valores de `A` que ya estaban escritos.

`actualizar_previsualizacion()` muestra `[A|b]` y el encabezado `Ax=b` cuando `b` está activo. Sin checkbox, presenta solamente `A`.

## 7. Flujo de `accion_resolver`

La función primero lee el método y el formato seleccionado. Si está en matriz pura, valida que `m=n` antes de leer los datos.

Después `obtener_matriz_desde_gui()` convierte las entradas a valores numéricos. En la rama de matriz pura:

```python
incluir_b = self.incluir_b_variable.get()
n = int(self.entry_n.get())
matriz_a = [fila[:n] for fila in matriz_original]
vector_b = [fila[n] for fila in matriz_original] if incluir_b else None
```

- `matriz_a` toma las primeras `n` columnas.
- Si el checkbox está activo, la última columna se separa como `vector_b`.
- Si está desmarcado, `vector_b` queda como `None`.

Luego se pide la inversa y la traza:

```python
resultado = enrutar_resolucion_matricial(
    matriz_a,
    vector_b=None,
    formato_fracciones=formato_fracciones
)
```

La inversa se calcula una sola vez. Si había vector `b`, la vista lo convierte a matriz columna y calcula:

```python
producto_solucion = multiplicar_matrices(
    resultado["matriz_inversa"],
    vector_b_columna
)
```

El resultado se transforma de nuevo en una lista para presentarlo como `x`. Independientemente del checkbox, también se calcula `A·A⁻¹` para mostrar la comprobación.

Si no está en matriz pura, se separan los coeficientes y el término independiente de la cuadrícula `[A|b]`, y se envían al enrutador con el método seleccionado. Así el flujo tradicional continúa separado del cálculo de la inversa.

## 8. Presentación del reporte

`mostrar_matriz_inversa()` recibe:

- `A` y `A⁻¹`.
- La lista `pasos` devuelta por el motor.
- El producto de verificación `A·A⁻¹`.
- Opcionalmente, `b`, el vector solución y `A⁻¹b`.
- El formato activo.

`_descripcion_paso_inversa()` traduce cada operación estructurada a texto:

| Tipo de paso | Texto mostrado |
| --- | --- |
| `inicial` | Matriz aumentada inicial `[A | I]` |
| `intercambio` | `F1 ↔ F2` |
| `normalizar` | `F1 = F1 / pivote` |
| `eliminar` | `F2 = F2 - (factor) * F1` |

Para cada paso, `_matriz_aumentada_inversa_a_string()` muestra las mitades izquierda y derecha de la matriz aumentada. El resultado final incluye `A⁻¹` y la comprobación de identidad.

Cuando `b` está marcado, se añade además:

1. El vector `b` como columna.
2. La fórmula `x=A⁻¹·b`.
3. El cálculo de cada componente `xi` como producto fila por columna.
4. El vector solución `x`.
5. El producto matricial representado como columna.

### Fracciones y decimales

`_formatear_valor()` consulta el formato seleccionado:

- En **Fracciones**, usa `Fraction` mediante `conversiones.convertir_a_fraccion()`.
- En **Decimales**, muestra el valor redondeado a dos cifras y elimina ceros finales innecesarios.

Los cálculos internos de esta ruta usan listas y `float`; el selector afecta la presentación. Por ello la comprobación de `A·A⁻¹` puede mostrar una identidad visualmente redondeada aunque internamente existan residuos de punto flotante muy pequeños.

## 9. Ejemplo del modo `Ax=b` con inversa

Sean:

```text
A = [2  0]
    [0  4]

b = [6, 8]ᵀ
```

Se activa **Matriz pura (A⁻¹)** y se marca **Incluir términos independientes (b)**. La interfaz construye `[A|b]`, separa `A` de `b` al calcular y obtiene:

```text
A⁻¹ = [1/2   0  ]
      [0     1/4]

x = A⁻¹b = [3, 2]ᵀ
```

Al desmarcar el checkbox, la cuadrícula solo recibe los cuatro coeficientes de `A` y el reporte termina en la inversa y su comprobación.

## 10. Errores y límites

- **`A` no cuadrada:** el modo matriz pura exige `m=n`; se rechaza antes de leer celdas.
- **`A` singular:** Gauss-Jordan no encuentra un pivote válido y el visor informa que `A` no tiene inversa.
- **Entrada vacía o no numérica:** `obtener_matriz_desde_gui()` identifica la posición problemática.
- **Modo sistema:** puede trabajar con los métodos de eliminación aunque el sistema no sea cuadrado o tenga soluciones infinitas/incompatibles.
- **Precisión:** el motor usa punto flotante y una tolerancia de `1e-10` para detectar pivotes nulos; no calcula determinantes simbólicos.

## 11. Cómo probar la funcionalidad

1. Abrir **Operaciones Básicas de Matrices**.
2. Elegir **Matriz pura (A⁻¹)**.
3. Dejar el checkbox desmarcado para obtener solamente `A⁻¹`, o marcarlo para crear `[A|b]` y resolver `Ax=b`.
4. Elegir Fracciones o Decimales y pulsar el botón de cálculo.
5. Verificar en el reporte los pasos `[A|I]`, la inversa y `A·A⁻¹`; con `b` activo, comprobar también `A⁻¹b`.

Para comprobar el caso singular, puede introducirse:

```text
A = [1  2]
    [2  4]
```

La función debe informar que no existe inversa. La implementación es Python puro; no utiliza NumPy.
