

def leer_flotante_seguro(mensaje):
    """Solicita un número (entero o decimal) al usuario de forma segura."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número válido (ejemplo: 5, -2, 3.5).")

def leer_entero_positivo(mensaje):
    """Solicita un entero positivo al usuario."""
    while True:
        try:
            val = int(input(mensaje))
            if val > 0:
                return val
            print("Error: El valor debe ser mayor a 0.")
        except ValueError:
            print("Error: Ingrese un número entero válido.")

def imprimir_matriz_aumentada(matriz, m, n):
    """Muestra la matriz aumentada [A|b] con formato visual limpio."""
    for fila in matriz:
        coeficientes = "  ".join(f"{elem:8.3f}" for elem in fila[:-1])
        b_val = f"{fila[-1]:8.3f}"
        print(f"[ {coeficientes}  | {b_val} ]")
    print()