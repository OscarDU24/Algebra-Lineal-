#Hacer un programa que te permita crear matrices de cualquier tamaño e ingresar y consultar datos 

print("Bienvenido al programa de creacion y consulta de matrices.")

def mostrar_menu():
    print("Seleccione una opción:")
    print("1. Crear matriz")
    print("2. Consultar matriz")
    print("3. Mostrar matriz")
    print("4. Salir")

def programa_matrices():
    matriz = []

    while True:
        mostrar_menu()
        opcion = input("Seleccione la opción: ")
        
        if opcion == "1":
            # Validación estricta para el número de filas
            while True:
                try:
                    filas = int(input("Ingrese el número de filas: "))
                    if filas <= 0:
                        print("Error: El número de filas debe ser mayor a 0.")
                        continue
                    break # Si pasa la validación, salimos de este while
                except ValueError:
                    print("Error: Ingrese un número entero válido (no se permiten letras ni espacios vacíos).")

            # Validación estricta para el número de columnas
            while True:
                try:
                    columnas = int(input("Ingrese el número de columnas: "))
                    if columnas <= 0:
                        print("Error: El número de columnas debe ser mayor a 0.")
                        continue
                    break # Si pasa la validación, salimos de este while
                except ValueError:
                    print("Error: Ingrese un número entero válido (no se permiten letras ni espacios vacíos).")

            # Crear matriz vacía y llenar con los valores ingresados por el usuario con validación
            matriz = []
            print("--- LLENANDO LA MATRIZ ---")
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    # Validación para que al llenar la celda tampoco se acepten letras
                    while True:
                        try:
                            valor = int(input(f"Ingrese el valor entero para la posición ({i}, {j}): "))
                            fila.append(valor)
                            break
                        except ValueError:
                            print("Error: Ingrese un número entero válido (no se permiten letras).")
                matriz.append(fila)
            print("¡Matriz creada exitosamente!")

        elif opcion == "2":
            if not matriz:
                print("No hay matriz creada. Por favor, cree una matriz primero.")
            else:
                print("\nMatriz actual:")
                for fila in matriz:
                    print(fila)
                
                print("Ingrese la posición que desea consultar:")
                try:
                    x = int(input("Ingrese la fila: "))
                    y = int(input("Ingrese la columna: "))
                    
                    # Validar que la posición esté dentro de los límites
                    if 0 <= x < len(matriz) and 0 <= y < len(matriz[0]):
                        print(f"El valor en la posición ({x}, {y}) es: {matriz[x][y]}")
                    else:
                        print("Error: La posición está fuera de los límites de la matriz.")
                except ValueError:
                    print("Por favor, ingrese un número entero válido para las coordenadas.")

        elif opcion == "3":
            if not matriz:
                print("No hay matriz creada. Por favor, cree una matriz primero.")
            else:
                print("\nMatriz actual:")
                for fila in matriz:
                    print(fila)

        elif opcion == "4":
            print("¡Gracias por usar el programa! Hasta luego.")
            break
        
        else:
            print("Opción inválida. Por favor, seleccione un número del 1 al 4.")

    programa_matrices()