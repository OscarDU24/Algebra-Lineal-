"""
Implementa el método de GAUSS-JORDAN sin usar NumPy, SciPy ni funciones de álgebra lineal de math.

"""

from Visualizacion import imprimir_matriz


def eliminacion_gauss_jordan(Ab, m, n, tolerancia=1e-9):
    
    fila_pivote = 0
    columnas_pivote = []
    paso = 1

    for col in range(n):
        if fila_pivote >= m:
            break

        # --- Búsqueda del mejor pivote (mayor valor absoluto) en la columna ---
        fila_max = fila_pivote
        for r in range(fila_pivote + 1, m):
            if abs(Ab[r][col]) > abs(Ab[fila_max][col]):
                fila_max = r

        # Si el pivote es prácticamente cero, la columna no tiene pivote
        # (variable libre); se pasa a la siguiente columna.
        if abs(Ab[fila_max][col]) < tolerancia:
            continue

        # --- Intercambio de filas si es necesario (se muestra el resultado) ---
        if fila_max != fila_pivote:
            Ab[fila_pivote], Ab[fila_max] = Ab[fila_max], Ab[fila_pivote]
            print(f"\n>> Paso {paso}.a: se intercambia la fila {fila_pivote + 1} "
                  f"con la fila {fila_max + 1} (mejor pivote disponible).")
            imprimir_matriz(Ab, m, n)

        # --- Normalización: se divide toda la fila pivote entre el pivote ---
        valor_pivote = Ab[fila_pivote][col]
        for c in range(col, n + 1):
            Ab[fila_pivote][c] /= valor_pivote
        print(f"\n>> Paso {paso}.b: se normaliza la fila {fila_pivote + 1} "
              f"dividiendo entre {valor_pivote:.4f} (pivote de x{col + 1} = 1).")
        imprimir_matriz(Ab, m, n)

        # --- Eliminación en TODAS las demás filas (arriba y abajo) ---
        hubo_eliminacion = False
        for r in range(m):
            if r != fila_pivote and abs(Ab[r][col]) > tolerancia:
                factor = Ab[r][col]
                for c in range(col, n + 1):
                    Ab[r][c] -= factor * Ab[fila_pivote][c]
                hubo_eliminacion = True

        if hubo_eliminacion:
            print(f"\n>> Paso {paso}.c: se elimina x{col + 1} en el resto de "
                  f"las filas usando la fila {fila_pivote + 1} como pivote.")
            imprimir_matriz(Ab, m, n)

        columnas_pivote.append(col)
        paso += 1
        fila_pivote += 1

    return Ab, columnas_pivote
