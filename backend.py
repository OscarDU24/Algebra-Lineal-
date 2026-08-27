#-------------------------------------------
# Backend
#-------------------------------------------

# Función para resolver con método de Gauss
# Toma la matriz como elemento y devuelve la matriz resuelta
def gauss(matrix):
    # Implementar código
    return matrix

# Ditto, pero con Gauss Jordan
def gauss_jordan(matrix):
    # Ditto
    return matrix

# Función de renderizado de la matriz
# Muestra cada uno de los elementos de la matriz organizados por filas y columnas
def render_matrix(matrix):
    for i in matrix:
            for j in i:
                print(j, end=' ')
            print()

# Función de creación de la matriz
# Devuelve una matriz de row x col
def create_matrix(row, col):
    return [[0] * row for _ in range(col)]

# Función de actualización del elemento
# Cambia el valor del elemento row x col de matrix
def update_cell(matrix, row, col, value):
    matrix[row][col] = value

# Función de entrada del usuario
# Registra la entrada del usuario y la valida
def int_input():
    while True:
        try:
            return int(input())
            break
        except ValueError:
             print(f"ERROR: Debe introducir un número entero válido: ", end="")
