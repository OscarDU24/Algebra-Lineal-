import random


# HERRAMIENTAS REUTILIZABLES (MODULARIDAD)


def leer_entero_seguro(mensaje):
    """Solicita un número al usuario de forma segura, evitando que el programa falle."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Entrada inválida. Por favor, ingrese un número entero.")

def imprimir_matriz(matriz):
    """Imprime cualquier matriz bidimensional con formato alineado."""
    for fila in matriz:
        # {:02d} fuerza 2 dígitos, equivalente al "D2" de C#
        print("\t".join(f"{elem:02d}" for elem in fila))
    print() # Salto de línea final


# LÓGICA DE LOS MÓDULOS


def modulo_busqueda():
    """Parte 1: Búsqueda dinámica en matriz."""
    print("\n=== Búsqueda de un valor en una matriz ===")
    filas = leer_entero_seguro("Ingrese el número de filas: ")
    columnas = leer_entero_seguro("Ingrese el número de columnas: ")

    # Llenar la matriz
    matriz = []
    print("\nIngrese los valores de la matriz:")
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(leer_entero_seguro(f"Elemento [{i},{j}]: "))
        matriz.append(fila)

    valor_buscado = leer_entero_seguro("\nIngrese el valor que desea buscar: ")
    encontrado = False

    # Buscar el valor
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == valor_buscado:
                print(f"El valor {valor_buscado} se encontró en la posición: fila {i}, columna {j}")
                encontrado = True

    if not encontrado:
        print(f"El valor {valor_buscado} no se encuentra en la matriz.")


def modulo_suma_pares():
    """Parte 2: Generación aleatoria y suma de pares en tiempo real."""
    print("\n=== Suma de elementos pares en una matriz 4x4 ===")
    
    # Generación de la matriz usando comprensión de listas
    matriz = [[random.randint(1, 100) for _ in range(4)] for _ in range(4)]

    print("\nMatriz generada:")
    imprimir_matriz(matriz)

    # Cálculo eficiente
    suma_pares = 0
    for fila in matriz:
        for elem in fila:
            if elem % 2 == 0:
                suma_pares += elem

    print(f"La suma de los elementos pares es: {suma_pares}")


def modulo_ordenamiento():
    """Parte 3: Aplanamiento y ordenamiento de una matriz 3x3."""
    print("\n=== Ordenamiento de una matriz 3x3 ===")
    
    matriz = []
    print("Ingrese los valores de la matriz (3x3):")
    for i in range(3):
        fila = []
        for j in range(3):
            fila.append(leer_entero_seguro(f"Elemento [{i},{j}]: "))
        matriz.append(fila)

    # 1. Aplanamiento optimizado usando comprensión de listas (Sin librerías extra)
    elementos = [elem for fila in matriz for elem in fila]

    # 2. Ordenamiento usando el método nativo (Timsort, muy rápido)
    elementos.sort()

    # 3. Reconstrucción de la matriz
    matriz_ordenada = []
    indice = 0
    for i in range(3):
        fila_nueva = []
        for j in range(3):
            fila_nueva.append(elementos[indice])
            indice += 1
        matriz_ordenada.append(fila_nueva)

    print("\nMatriz ordenada de menor a mayor:")
    imprimir_matriz(matriz_ordenada)



# MENÚ PRINCIPAL DEL PROYECTO


def menu_principal():
    while True:
        print("\n" + "="*30)
        print(" SISTEMA DE GESTIÓN DE MATRICES")
        print("="*30)
        print("1. Buscar valor en matriz")
        print("2. Sumar pares (Matriz aleatoria 4x4)")
        print("3. Ordenar matriz 3x3")
        print("4. Salir")
        
        opcion = leer_entero_seguro("Seleccione una opción: ")

        if opcion == 1:
            modulo_busqueda()
        elif opcion == 2:
            modulo_suma_pares()
        elif opcion == 3:
            modulo_ordenamiento()
        elif opcion == 4:
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Punto de entrada estándar en proyectos Python
if __name__ == "__main__":
    menu_principal()

    #Dios como odio subir cosas en GitHub