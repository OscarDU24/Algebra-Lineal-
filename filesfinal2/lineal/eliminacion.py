
from .visualizacion import copiar_matriz

TOLERANCIA = 1e-9


def eliminacion_por_filas(matriz_original, modo="gauss"):
    """
    Aplica eliminacion por filas sobre la matriz aumentada.
    """
    matriz = copiar_matriz(matriz_original)
    filas = len(matriz)
    columnas = len(matriz[0])
    variables = columnas - 1

    pasos = [("Matriz aumentada inicial", copiar_matriz(matriz))]
    columnas_pivote = []
    fila_pivote = 0

    for col in range(variables):
        if fila_pivote >= filas:
            break

        # Pivoteo parcial: se busca, desde fila_pivote hacia abajo,
        # la fila con mayor valor absoluto en la columna actual.
        fila_max = fila_pivote
        for r in range(fila_pivote + 1, filas):
            if abs(matriz[r][col]) > abs(matriz[fila_max][col]):
                fila_max = r











        # Si el mejor candidato es practicamente cero, esa columna
        # no tiene pivote (variable libre): se pasa a la siguiente.
        if abs(matriz[fila_max][col]) < TOLERANCIA:
            continue

        # Intercambio de filas si el pivote no esta ya arriba.
        if fila_max != fila_pivote:
            matriz[fila_pivote], matriz[fila_max] = matriz[fila_max], matriz[fila_pivote]
            pasos.append((
                f"Intercambio de fila {fila_pivote + 1} con fila {fila_max + 1}",
                copiar_matriz(matriz)
            ))

        if modo == "gauss_jordan":
            # (Gauss-Jordan) Se normaliza la fila pivote dividiendo
            # entre el valor del pivote, para que quede en 1.
            valor_pivote = matriz[fila_pivote][col]
            for c in range(col, columnas):
                matriz[fila_pivote][c] /= valor_pivote
            pasos.append((
                f"F{fila_pivote + 1} = F{fila_pivote + 1} / {valor_pivote:.4f}",
                copiar_matriz(matriz)
            ))

            # Eliminacion en TODAS las demas filas (arriba y abajo).
            for r in range(filas):
                if r != fila_pivote and abs(matriz[r][col]) > TOLERANCIA:
                    factor = matriz[r][col]
                    for c in range(col, columnas):
                        matriz[r][c] -= factor * matriz[fila_pivote][c]
                    pasos.append((
                        f"F{r + 1} = F{r + 1} - ({factor:.4f}) * F{fila_pivote + 1}",
                        copiar_matriz(matriz)
                    ))
        else:
            # (Gauss) Eliminacion SOLO debajo del pivote.
            for r in range(fila_pivote + 1, filas):
                if abs(matriz[r][col]) > TOLERANCIA:
                    factor = matriz[r][col] / matriz[fila_pivote][col]
                    for c in range(col, columnas):
                        matriz[r][c] -= factor * matriz[fila_pivote][c]
                    pasos.append((
                        f"F{r + 1} = F{r + 1} - ({factor:.4f}) * F{fila_pivote + 1}",
                        copiar_matriz(matriz)
                    ))

        columnas_pivote.append(col)
        fila_pivote += 1

    return matriz, pasos, columnas_pivote
