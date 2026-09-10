from .visualizacion import copiar_matriz

TOLERANCIA = 1e-9


def eliminacion_por_filas(matriz_original, modo="escalonado"):
    """
    Realiza eliminación por filas sobre una matriz aumentada.

    Modos disponibles:
        - "escalonado": forma escalonada sin normalizar pivotes.
        - "gauss": forma escalonada con pivotes normalizados.
        - "gauss_jordan": forma escalonada reducida.

    El algoritmo funciona con matrices cuadradas y rectangulares.
    Las columnas que no poseen pivote corresponden a variables libres.
    """

    matriz = copiar_matriz(matriz_original)

    filas = len(matriz)
    columnas = len(matriz[0])
    variables = columnas - 1

    pasos = [
        ("Matriz aumentada inicial", copiar_matriz(matriz))
    ]

    columnas_pivote = []
    fila_pivote = 0

    # Recorremos las columnas correspondientes a las variables.
    for col in range(variables):

        # Si ya no existen filas disponibles para colocar
        # otro pivote, terminamos el proceso.
        if fila_pivote >= filas:
            break

        # ---------------------------------------------------------
        # BUSCAR EL MEJOR PIVOTE
        # ---------------------------------------------------------

        fila_max = fila_pivote

        for r in range(fila_pivote + 1, filas):

            if abs(matriz[r][col]) > abs(matriz[fila_max][col]):
                fila_max = r

        # Si la columna no posee un pivote diferente de cero,
        # se pasa a la siguiente columna.
        if abs(matriz[fila_max][col]) < TOLERANCIA:
            continue

        # ---------------------------------------------------------
        # INTERCAMBIO DE FILAS
        # ---------------------------------------------------------

        if fila_max != fila_pivote:

            matriz[fila_pivote], matriz[fila_max] = (
                matriz[fila_max],
                matriz[fila_pivote]
            )

            pasos.append(
                (
                    f"Intercambio de fila {fila_pivote + 1} "
                    f"con fila {fila_max + 1}",
                    copiar_matriz(matriz)
                )
            )

        valor_pivote = matriz[fila_pivote][col]

        # =========================================================
        # MÉTODO ESCALONADO
        # =========================================================

        if modo == "escalonado":

            # NO se normaliza el pivote.
            # Se conserva el valor original del pivote.

            # Eliminación únicamente debajo del pivote.
            for r in range(fila_pivote + 1, filas):

                if abs(matriz[r][col]) < TOLERANCIA:
                    continue

                factor = (
                    matriz[r][col] /
                    valor_pivote
                )

                for c in range(col, columnas):

                    matriz[r][c] -= (
                        factor *
                        matriz[fila_pivote][c]
                    )

                # Limpieza de errores numéricos.
                if abs(matriz[r][col]) < TOLERANCIA:
                    matriz[r][col] = 0.0

                pasos.append(
                    (
                        f"F{r + 1} = F{r + 1} - "
                        f"({factor:.4f}) * F{fila_pivote + 1}",
                        copiar_matriz(matriz)
                    )
                )

        # =========================================================
        # MÉTODO DE GAUSS
        # =========================================================

        elif modo == "gauss":

            # Normalizar el pivote para convertirlo en 1.
            if abs(valor_pivote - 1.0) > TOLERANCIA:

                for c in range(col, columnas):

                    matriz[fila_pivote][c] /= valor_pivote

                pasos.append(
                    (
                        f"F{fila_pivote + 1} = "
                        f"F{fila_pivote + 1} / "
                        f"{valor_pivote:.4f}",
                        copiar_matriz(matriz)
                    )
                )

            # Eliminación únicamente debajo del pivote.
            for r in range(fila_pivote + 1, filas):

                factor = matriz[r][col]

                if abs(factor) < TOLERANCIA:
                    continue

                for c in range(col, columnas):

                    matriz[r][c] -= (
                        factor *
                        matriz[fila_pivote][c]
                    )

                if abs(matriz[r][col]) < TOLERANCIA:
                    matriz[r][col] = 0.0

                pasos.append(
                    (
                        f"F{r + 1} = F{r + 1} - "
                        f"({factor:.4f}) * F{fila_pivote + 1}",
                        copiar_matriz(matriz)
                    )
                )

        # =========================================================
        # MÉTODO DE GAUSS-JORDAN
        # =========================================================

        elif modo == "gauss_jordan":

            # Normalizar el pivote para convertirlo en 1.
            if abs(valor_pivote - 1.0) > TOLERANCIA:

                for c in range(col, columnas):

                    matriz[fila_pivote][c] /= valor_pivote

                pasos.append(
                    (
                        f"F{fila_pivote + 1} = "
                        f"F{fila_pivote + 1} / "
                        f"{valor_pivote:.4f}",
                        copiar_matriz(matriz)
                    )
                )

            # Eliminar el valor de la columna pivote
            # en TODAS las demás filas.
            for r in range(filas):

                if r == fila_pivote:
                    continue

                factor = matriz[r][col]

                if abs(factor) < TOLERANCIA:
                    continue

                for c in range(col, columnas):

                    matriz[r][c] -= (
                        factor *
                        matriz[fila_pivote][c]
                    )

                if abs(matriz[r][col]) < TOLERANCIA:
                    matriz[r][col] = 0.0

                pasos.append(
                    (
                        f"F{r + 1} = F{r + 1} - "
                        f"({factor:.4f}) * F{fila_pivote + 1}",
                        copiar_matriz(matriz)
                    )
                )

        else:

            raise ValueError(
                f"Modo de eliminación no válido: {modo}"
            )

        # Registrar la columna como columna pivote.
        columnas_pivote.append(col)

        # Avanzar a la siguiente fila.
        fila_pivote += 1

    # -------------------------------------------------------------
    # LIMPIEZA DE ERRORES NUMÉRICOS
    # -------------------------------------------------------------

    for i in range(filas):

        for j in range(columnas):

            if abs(matriz[i][j]) < TOLERANCIA:
                matriz[i][j] = 0.0

    return matriz, pasos, columnas_pivote