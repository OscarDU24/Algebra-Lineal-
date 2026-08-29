
from .visualizacion import imprimir_matriz


def eliminacion_por_eliminacion(Ab, m, n, tolerancia=1e-9):

    fila_pivote = 0
    columnas_pivote = []
    paso = 1

    for col in range(n):
        if fila_pivote >= m:
            break


        if abs(Ab[fila_pivote][col]) < tolerancia:
            fila_encontrada = None
            for r in range(fila_pivote + 1, m):
                if abs(Ab[r][col]) > tolerancia:
                    fila_encontrada = r
                    break
            if fila_encontrada is None:
                # No hay ninguna ecuación con esta variable; es libre.
                continue
            Ab[fila_pivote], Ab[fila_encontrada] = Ab[fila_encontrada], Ab[fila_pivote]
            print(f"\n>> Paso {paso}.a: se reordena la ecuación {fila_encontrada + 1} "
                  f"hacia la posición {fila_pivote + 1} (tenía x{col + 1} = 0).")
            imprimir_matriz(Ab, m, n)

        hubo_eliminacion = False
        for r in range(fila_pivote + 1, m):
            if abs(Ab[r][col]) > tolerancia:
                factor = Ab[r][col] / Ab[fila_pivote][col]
                operacion = "resta" if factor > 0 else "suma"
                print(f"\n>> Paso {paso}.b: para eliminar x{col + 1} de la ecuación "
                      f"{r + 1}, se multiplica la ecuación {fila_pivote + 1} por "
                      f"{factor:.4f} y se {operacion} de la ecuación {r + 1}.")
                for c in range(col, n + 1):
                    Ab[r][c] -= factor * Ab[fila_pivote][c]
                hubo_eliminacion = True

        if hubo_eliminacion:
            imprimir_matriz(Ab, m, n)

        columnas_pivote.append(col)
        paso += 1
        fila_pivote += 1

    return Ab, columnas_pivote
