
from .visualizacion import imprimir_matriz


def eliminacion_gauss(Ab, m, n, tolerancia=1e-9):

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

        # --- Eliminación SOLO debajo del pivote (no se toca lo de arriba) ---
        hubo_eliminacion = False
        for r in range(fila_pivote + 1, m):
            if abs(Ab[r][col]) > tolerancia:
                factor = Ab[r][col] / Ab[fila_pivote][col]
                for c in range(col, n + 1):
                    Ab[r][c] -= factor * Ab[fila_pivote][c]
                hubo_eliminacion = True

        if hubo_eliminacion:
            print(f"\n>> Paso {paso}.b: se elimina x{col + 1} debajo de la fila "
                  f"{fila_pivote + 1} (fila pivote), sin modificar el pivote.")
            imprimir_matriz(Ab, m, n)

        columnas_pivote.append(col)
        paso += 1
        fila_pivote += 1

    return Ab, columnas_pivote
