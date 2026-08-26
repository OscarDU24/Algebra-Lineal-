# ==============================================================================
# MÓDULO DE ENTRADAS Y VISUALIZACIÓN (entradas.py)
# Propósito: Manejar la validación de datos del usuario y la impresión en consola.
# ==============================================================================

# ---------------------------------------------------------
# BLOQUE 1: VALIDACIÓN DE ENTRADAS NUMÉRICAS
# ---------------------------------------------------------
def leer_flotante_seguro(mensaje):
    """Solicita un número (entero o decimal) de forma segura mediante un ciclo."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número válido (ejemplo: 5, -2, 3.5).")

def leer_entero_positivo(mensaje):
    """Solicita estrictamente un entero mayor a cero."""
    while True:
        try:
            val = int(input(mensaje))
            if val > 0:
                return val
            print("Error: El valor debe ser mayor a 0.")
        except ValueError:
            print("Error: Ingrese un número entero válido.")

# ---------------------------------------------------------
# BLOQUE 2: VISUALIZACIÓN DE MATRICES
# ---------------------------------------------------------
def imprimir_matriz_aumentada(matriz, m, n):
    """
    Imprime la matriz aumentada [A|b].
    Itera sobre cada fila separando la matriz A del vector b con una barra vertical '|'.
    """
    for fila in matriz:
        # Formatea los coeficientes de A (todos los elementos excepto el último)
        coeficientes = "  ".join(f"{elem:8.3f}" for elem in fila[:-1])
        # Formatea el término independiente b (el último elemento de la fila)
        b_val = f"{fila[-1]:8.3f}"
        
        print(f"[ {coeficientes}  | {b_val} ]")
    print()