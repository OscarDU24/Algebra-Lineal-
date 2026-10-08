# Módulo de determinantes y factorización LU

El módulo se abre desde la tarjeta **Determinantes y Factorización LU** del
Dashboard. Permite calcular determinantes y resolver sistemas cuadrados
\(A x = b\). La interfaz está en `core/ui/vista_determinantes.py` y las
operaciones matemáticas integradas en
`core/determinantes/operaciones_determinantes.py`.

Los módulos reutilizables del prototipo también se conservaron en
`core/determinantes/`: `operacionesDeterminantes.py`,
`verificacionDeterminantes.py`, `cramerDeterminantes.py` y
`visualizacionDeterminantes.py`. La interfaz prototipo
`docs/Reciclar/ReciclarDeterminaantes/Main_Determinantes.py` permanece en la
carpeta de reciclaje; la aplicación principal usa
`core/ui/vista_determinantes.py`.

## Entrada y formato

- La matriz \(A\) debe ser cuadrada y no vacía.
- Cada elemento admite enteros, decimales y fracciones, por ejemplo `-2`,
  `0.75` o `3/4`.
- La resolución de sistemas requiere un vector \(b\) con una componente por
  cada fila de \(A\).
- El selector de salida permite mostrar fracciones o decimales. Los cálculos
  se hacen con `fractions.Fraction`, por lo que las entradas racionales se
  conservan exactamente durante las operaciones; el modo decimal solo cambia
  la presentación.
- La recomendación de eficiencia se actualiza cuando se completa una matriz
  válida. Para órdenes hasta 3 sugiere cofactores o Sarrus; para orden 4 sugiere
  LU, aunque cofactores sigue siendo viable; para orden 5 o superior recomienda
  fuertemente LU. Las cifras de operaciones que muestra el panel son
  estimaciones didácticas, no una medición del tiempo real de ejecución.

## Métodos disponibles

### Determinantes

- **Automático:** usa el procedimiento directo para matrices de orden 1, 2 y 3
  (caso 1x1, regla \(ad-bc\) y regla de Sarrus, respectivamente). Para órdenes
  mayores usa LU.
- **Cofactores:** expande recursivamente por la primera fila. Es útil para
  estudiar el procedimiento en matrices pequeñas; su costo crece rápidamente
  con el orden.
- **LU / Triangulación:** realiza eliminación gaussiana con pivoteo parcial.
  Los multiplicadores se guardan en \(L\), la matriz triangular resultante es
  \(U\), y se registra cada intercambio de filas.

Con pivoteo, la factorización satisface \(P A = L U\). El determinante se
calcula como

\[
\det(A) = (-1)^s \prod_{i=1}^{n} u_{ii},
\]

donde \(s\) es el número de intercambios de filas. Si no se encuentra un pivote
distinto de cero, la matriz es singular y el resultado es cero. El informe
muestra la matriz inicial, los intercambios y pasos de eliminación, \(L\), \(U\),
la diagonal, el signo y el determinante resultante.

### Resolver sistemas

- **Resolver sistema (LU):** calcula \(P A = L U\), reordena el vector como
  \(P b\), resuelve \(L y = P b\) por sustitución hacia adelante y luego
  \(U x = y\) por sustitución hacia atrás. Muestra las matrices \(L\) y \(U\),
  el vector intermedio \(y\) y cada componente de la solución.
- **Resolver sistema (Cramer):** conserva la alternativa del prototipo. Calcula
  el determinante principal y los determinantes de las matrices con una columna
  reemplazada por \(b\). Si el determinante principal es cero, informa que
  Cramer no permite obtener una solución única.

La factorización LU del módulo requiere una matriz no singular para resolver el
sistema; si \(A\) es singular, muestra un error en vez de presentar una solución
única inexistente.

## Pruebas

La suite `tests/test_determinantes.py` contiene pruebas de regresión para el
signo debido al pivoteo, la concordancia entre LU y cofactores, la solución con
permutación de filas, matrices singulares, recomendaciones por orden y
validación de entradas.

Desde la raíz del repositorio se puede ejecutar con:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_determinantes.py" -v
```

Estas pruebas no se importan ni ejecutan al abrir la aplicación; son una
herramienta de desarrollo para comprobar el comportamiento matemático y detectar
regresiones al modificar el módulo.
