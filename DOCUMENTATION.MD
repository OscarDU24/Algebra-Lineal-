# Nombre
Matrices

# Descripcion
Programa de Matrices sencillo escrito en Python.

# Modulos
## 1. main.py
### Descripción
Script principal del programa. Su única función es la de llamar a la función para mostrar la pantalla principal, encontrada en el módulo *frontend.py*

## 2. frontend.py
### Descripción
Módulo encargado de la interfaz gráfica del programa. Contiene las pantallas para cada procedimiento, así como ciertas convenciones para decorados de la interfaz de texto.

### Funciones
- hr(): Dibuja una línea horizontal en la pantalla
- scr_render_matrix(matrix): Pantalla de renderizado de la matriz
- scr_reduce(matrix): Pantalla para reducción de matrices
- scr_create(matrix): Menú de creación de la matriz. Se ejecuta al inicio del programa.
- scr_update_cell(matrix, row, col): Menú para actualizar los datos en el elemento row x col de la matriz matrix.
- scr_select_cell(matrix): Menú para seleccionar un elemento de la matrix matriz. Conecta con la pantalla scr_update_cell().
- scr_main(): Pantalla principal del programa. Contiene el bucle principal.

## 3. backend.py
### Descripción
Contiene funciones relacionadas a la lógica interna del programa. Módulo usado principalmente por el módulo frontend.py.

### Funciones
- gauss(matrix): Toma como argumento una matriz y la devuelve reducida mediante el método de Gauss.
- gauss_jordan(matrix: Lo mismo que la anterior, pero con el método de Gauss Jordan.
- render_matrix(matrix): Dibuja la matriz especificada, elemento por elemento, separándolos por columnas
- create_matrix(row, col): Crea una matriz de row x col y la devuelve.
- update_cell(matrix, row, col, value): Cambia el valor del elemento row x col de la matriz matrix a value.
- int_input(): Versión acortada de int(input()), con validaciones y mensajes de error.
