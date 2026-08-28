"""
UNIVERSIDAD AMERICANA
Facultad de Ingeniería y Arquitectura (FIA)
Proyecto Integrador: Calculadora de Álgebra Lineal
Módulo: Validaciones (Entradas del Usuario)
Descripción: Funciones para validar y capturar los datos ingresados desde la consola.
"""

def leer_entero_positivo(mensaje):
    """
    Solicita un número entero estrictamente mayor a 0.
    Garantiza que el usuario ingrese dimensiones válidas para la matriz.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if valor > 0:
                return valor
            else:
                print("Error: El valor debe ser un número entero mayor que 0.")
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

def leer_flotante(mensaje):
    """
    Solicita un número real (flotante) aceptando enteros, decimales y negativos.
    Maneja el error si el usuario escribe letras o caracteres no válidos.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            return float(entrada)
        except ValueError:
            print("   Error: Debe ingresar un número válido (ej. 5, -3.2, 0).")

def pedir_dimensiones_sistema():
    """Pide al usuario el número de ecuaciones (filas) y de variables (columnas)."""
    print("\n--- 1. Dimensiones del Sistema ---")
    filas = leer_entero_positivo("Ingrese el número de ecuaciones (m): ")
    columnas = leer_entero_positivo("Ingrese el número de variables (n): ")
    return filas, columnas

def pedir_matriz_aumentada(filas, columnas):
    """
    Pide al usuario los coeficientes y el término independiente de cada ecuación.
    Retorna la matriz aumentada como una lista de listas.
    """
    print("\n--- 2. Ingreso de Coeficientes y Términos Independientes ---")
    matriz = []
    
    for i in range(filas):
        print(f"\nEcuación {i + 1}:")
        fila = []
        # Pedir coeficientes de las variables
        for j in range(columnas):
            coef = leer_flotante(f"  Coeficiente de x{j + 1}: ")
            fila.append(coef)
        
        # Pedir el término independiente (b)
        indep = leer_flotante(f"  Término independiente (b{i + 1}): ")
        fila.append(indep)
        
        matriz.append(fila)
        
    return matriz