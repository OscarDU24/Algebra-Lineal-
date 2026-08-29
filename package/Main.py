"""
PROGRAMA 1: Resolución de Sistemas de Ecuaciones Lineales
            mediante el Método de GAUSS-JORDAN (sin NumPy/SciPy/math)
============================================================
"""

from Entrada import leer_entero, construir_matriz_aumentada
from Visualizacion import imprimir_matriz
from Eliminacion import eliminacion_gauss_jordan
from Clasificacion import clasificar_sistema
from Solucion import extraer_solucion
from Verificacion import verificar_solucion


def main():
    print("=" * 60)
    print(" RESOLUCIÓN DE SISTEMAS DE ECUACIONES LINEALES ")
    print(" Método de Gauss-Jordan                                ")
    print("=" * 60)

    # --- 1. Entrada de datos ---
    m = leer_entero("\nIngrese el número de ecuaciones (m): ")
    n = leer_entero("Ingrese el número de variables (n): ")

    Ab = construir_matriz_aumentada(m, n)

    # Se guarda una copia del sistema original para la verificación posterior
    A_original = [fila[:n] for fila in Ab]
    b_original = [fila[n] for fila in Ab]

    imprimir_matriz(Ab, m, n, "Matriz aumentada inicial [A | b]:")

    # --- 2. Procesamiento: eliminación por filas (Gauss-Jordan) ---
    print("Iniciando proceso de eliminación por filas (método Gauss-Jordan)...")
    print("A continuación se muestra cada paso hasta llegar a la forma")
    print("escalonada reducida por filas.")
    Ab, columnas_pivote = eliminacion_gauss_jordan(Ab, m, n)

    imprimir_matriz(Ab, m, n, "Matriz escalonada reducida final :")

    # --- 3. Clasificación del sistema ---
    clasificacion = clasificar_sistema(Ab, m, n, columnas_pivote)

    print("=" * 60)
    if clasificacion == "INCONSISTENTE":
        print("CLASIFICACIÓN: Sistema Inconsistente -> Sin Solución")
        print("(Se encontró una fila de la forma 0 0 ... 0 | k, con k != 0)")
    elif clasificacion == "DETERMINADO":
        print("CLASIFICACIÓN: Sistema Consistente Determinado -> Solución Única")
    else:
        print("CLASIFICACIÓN: Sistema Consistente Indeterminado -> Infinitas Soluciones")
    print("=" * 60)

    # --- 4. Salida y verificación ---
    if clasificacion == "DETERMINADO":
        x = extraer_solucion(Ab, n)
        print("\nValores de las variables:")
        for i in range(n):
            print(f"  x{i + 1} = {x[i]:.4f}")

        verificar_solucion(A_original, b_original, x, m, n)

    elif clasificacion == "INDETERMINADO":
        print("\nEl sistema tiene infinitas soluciones; no se despliega un valor")
        print("numérico único por variable. Las variables asociadas a columnas")
        print("sin pivote son libres y pueden tomar cualquier valor real.")
        print(f"Columnas con pivote (variables dependientes): "
              f"{[f'x{c + 1}' for c in columnas_pivote]}")

    else:  # INCONSISTENTE
        print("\nEl sistema no tiene solución; no es posible calcular valores")
        print("numéricos para las variables ni realizar la verificación.")

    print("\nFin del programa.")


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================
if __name__ == "__main__":
    main()
