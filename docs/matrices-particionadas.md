# Matrices particionadas y operaciones por bloques

La calculadora de matrices incluye una ventana dedicada para dividir matrices en
cuatro bloques y operar sobre ellos. Se abre desde **Operación especial →
Matrices Particionadas** en la calculadora matricial.

## Uso

1. Seleccione suma, multiplicación o inversa triangular superior.
2. Defina las dimensiones de cada matriz y los cortes horizontal (entre filas)
   y vertical (entre columnas). Cada corte debe quedar estrictamente dentro de
   la matriz; los cuatro bloques no tienen que ser del mismo tamaño.
3. Pulse **Generar editores**, ingrese los valores o cargue una matriz desde un
   archivo CSV. Se aceptan enteros, decimales y fracciones como `3/5`.
4. Pulse **Calcular**. El informe muestra la partición de entrada, cada bloque
   del resultado y la matriz final reensamblada.

En la operación de inversa, `A21` debe contener solo ceros y `A11` y `A22`
deben ser invertibles. La inversión de esos bloques usa el eliminador
Gauss-Jordan existente, que opera con tolerancia numérica y devuelve valores de
punto flotante.

## Lógica

La lógica independiente de la interfaz está en
`core/matriciales/particiones_logica.py`:

- `particionar_matriz` y `reensamblar_bloques` separan y reúnen matrices
  rectangulares.
- `suma_bloques` valida las dimensiones correspondientes y suma cada bloque.
- `multiplicacion_bloques` valida las dimensiones internas del producto y omite
  productos de bloques que sean completamente cero.
- `inversa_triangular_bloques` recibe una función de inversión y aplica la
  fórmula de la inversa de una matriz triangular superior por bloques.

Las entradas no conformables o los cortes inválidos producen `ValueError` con
un mensaje descriptivo. Las pruebas de regresión están en
`tests/test_particiones.py`.
