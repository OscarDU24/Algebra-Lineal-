import os
import backend as b

#-------------------------------------------
# Frontend
#-------------------------------------------

# Hr: Linea horizontal dibujada para decoración
def hr():
    print("-" * 64)

# Pantalla de muestra de la matriz: Renderiza todos los elementos de la matriz
def scr_render_matrix(matrix):
    os.system("clear")
    hr()
    print("Mostrando la matriz...")
    hr()
    b.render_matrix(matrix)
    hr()
    print("Pulse Enter para continuar...", end="")
    input()

# Pantalla de muestra de la matriz: Renderiza todos los elementos de la matriz
def scr_reduce(matrix):
    os.system("clear")
    hr()
    print("Reducir la matriz")
    hr()
    b.render_matrix(matrix)
    hr()
    print("1. Por Gauss")
    print("2. Por Gauss Jordan")
    print("3. Cancelar")
    hr()
    
    print("Seleccione un número: ", end="")
    while True:
        opcion = b.int_input()
        if opcion == 1:
            matrix = b.gauss(matrix)
            break
        if opcion == 2:
            matrix = b.gauss_jordan(matrix)
            break
        if opcion == 3:
            return
            break
        else:
            print("Error: Entrada inválida: ", end="")
    os.system("clear")
    hr()
    print("Matriz reducida")
    hr()
    print("Pulse enter para continuar...", end="")
    input()

# Pantalla de creación de la matriz: Configuración inicial del programa
def scr_create_matrix():
    hr()
    print("Creación de la matriz")
    hr()
    print("Introduzca el número de filas: ", end="")
    while True:
        row = b.int_input()
        if row > 0:
            break
        else:
            print("Error: Número de filas inválido: Intente de nuevo: ", end="")

    hr()
    print("Introduzca el número de columnas: ", end="")
    while True:
        col = b.int_input()
        if col > 0:
            break
        else:
            print("Error: Número de columnas inválido. Intente de nuevo:", end="")


    return b.create_matrix(row, col)

# Menú de actualización de elementos: Modifica el valor del elemento row x col de una matriz 
def scr_update_cell(matrix, row, col):
    os.system("clear")
    hr()
    print("Actualizando datos del elemento")
    hr()
    print("Introduzca el valor nuevo: ", end="")
    val = b.int_input() # Input del usuario
    b.update_cell(matrix, row, col, val)

# Menú de selección de elementos: Selecciona un elemento por columna y por fila
def scr_select_cell(matrix):
    while True:
        try:
            os.system("clear")
            hr()
            print("Selección de un elemento")
            hr()
            print("Introduzca el número de fila: ", end="")
            row = b.int_input()
            hr()
            print("Introduzca el número de columna: ", end="")
            col = b.int_input()
            matrix[row][col]
            break
        except IndexError:
            hr()
            print("Error: El elemento especificado no es válido.")
            hr()
            print("Pulse enter para continuar...", end="")
            input()

    # Bucle principal
    while True:
        os.system("clear")
        hr()
        print(f"Elemento {col}x{row} seleccionado (Valor: {matrix[row][col]})")

        hr()
        print("1. Actualizar datos del elemento")
        print("2. Cancelar")

        hr()
        print("Ingrese un número de opción: ", end="")
        opcion = b.int_input()
        if opcion == 1:
            scr_update_cell(matrix, row, col) # Cambiar a menú de actualización de elementos
        if opcion == 2:
            break

#  Menú de opciones: Menú principal del programa
def scr_main():
    os.system("clear") 
    matrix = scr_create_matrix() # Primero crear la matriz

    while True:
        # Bucle principal
        os.system("clear")
        hr()
        print("Opciones")
        hr()
        print("1. Ver toda la matriz")
        print("2. Seleccionar un elemento")
        print("3. Reducir la matriz")
        print("4. Salir")
        hr()
        print("Ingrese un número de opción: ", end='')

        # Input del usuario
        opcion = b.int_input()
        if opcion == 1:
            scr_render_matrix(matrix)
        elif opcion == 2:
            scr_select_cell(matrix)
        elif opcion == 3:
            scr_reduce(matrix)
        elif opcion == 4:
            break
        else:
            print("La opción introducida no existe")
