from fractions import Fraction
from .exactitud import es_cero, es_matriz_exacta, es_uno, matriz_a_fracciones
from .visualizacion import copiar_matriz

TOLERANCIA = 1e-9


def eliminacion_por_filas(matriz_original, modo="escalonado", formatear=None):
    """
    Realiza eliminación por filas sobre una matriz aumentada.

    Modos disponibles:
        - "escalonado": forma escalonada sin normalizar pivotes.
        - "gauss": forma escalonada con pivotes normalizados.
        - "gauss_jordan": forma escalonada reducida.

    El algoritmo funciona con matrices cuadradas y rectangulares.
    Las columnas que no poseen pivote corresponden a variables libres.

    ``formatear`` (opcional) convierte los factores de cada paso en texto, para
    que la descripción use el mismo formato que la vista (fracción o decimal).
    """

    # Con fracciones (y sin floats) se trabaja de forma exacta: un valor es cero
    # solo si es exactamente cero. Con floats se usa la tolerancia TOLERANCIA.
    is_fraction = es_matriz_exacta(matriz_original)
    matriz = (
        matriz_a_fracciones(matriz_original)
        if is_fraction
        else copiar_matriz(matriz_original)
    )

    filas = len(matriz)
    columnas = len(matriz[0])
    variables = columnas - 1

    def format_val(val):
        """Función auxiliar para formatear fracciones o decimales limpiamente."""
        if isinstance(val, Fraction):
            if val.denominator == 1:
                return str(val.numerator)
            return f"{val.numerator}/{val.denominator}"
        else:
            if isinstance(val, float) and abs(val - round(val)) < 1e-9:
                return str(int(round(val)))
            s = f"{val:.2f}"
            if "." in s:
                s = s.rstrip("0").rstrip(".")
            return s

    if formatear is not None:
        format_val = formatear

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
            # Fraction admite abs() y comparación exacta sin pasar por float.
            if abs(matriz[r][col]) > abs(matriz[fila_max][col]):
                fila_max = r

        # Si la columna no posee un pivote diferente de cero,
        # se pasa a la siguiente columna.
        if es_cero(matriz[fila_max][col], is_fraction, TOLERANCIA):
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

            # Eliminación únicamente debajo del pivote.
            for r in range(fila_pivote + 1, filas):

                if es_cero(matriz[r][col], is_fraction, TOLERANCIA):
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
                if es_cero(matriz[r][col], is_fraction, TOLERANCIA):
                    matriz[r][col] = Fraction(0) if is_fraction else 0.0

                pasos.append(
                    (
                        f"F{r + 1} = F{r + 1} - "
                        f"({format_val(factor)}) * F{fila_pivote + 1}",
                        copiar_matriz(matriz)
                    )
                )

        # =========================================================
        # MÉTODO DE GAUSS
        # =========================================================

        elif modo == "gauss":

            # Normalizar el pivote para convertirlo en 1.
            if not es_uno(valor_pivote, is_fraction, TOLERANCIA):

                for c in range(col, columnas):

                    matriz[fila_pivote][c] /= valor_pivote

                pasos.append(
                    (
                        f"F{fila_pivote + 1} = "
                        f"F{fila_pivote + 1} / "
                        f"({format_val(valor_pivote)})",
                        copiar_matriz(matriz)
                    )
                )

            # Eliminación únicamente debajo del pivote.
            for r in range(fila_pivote + 1, filas):

                factor = matriz[r][col]
                if es_cero(factor, is_fraction, TOLERANCIA):
                    continue

                for c in range(col, columnas):

                    matriz[r][c] -= (
                        factor *
                        matriz[fila_pivote][c]
                    )

                if es_cero(matriz[r][col], is_fraction, TOLERANCIA):
                    matriz[r][col] = Fraction(0) if is_fraction else 0.0

                pasos.append(
                    (
                        f"F{r + 1} = F{r + 1} - "
                        f"({format_val(factor)}) * F{fila_pivote + 1}",
                        copiar_matriz(matriz)
                    )
                )

        # =========================================================
        # MÉTODO DE GAUSS-JORDAN
        # =========================================================

        elif modo == "gauss_jordan":

            # Normalizar el pivote para convertirlo en 1.
            if not es_uno(valor_pivote, is_fraction, TOLERANCIA):

                for c in range(col, columnas):

                    matriz[fila_pivote][c] /= valor_pivote

                pasos.append(
                    (
                        f"F{fila_pivote + 1} = "
                        f"F{fila_pivote + 1} / "
                        f"({format_val(valor_pivote)})",
                        copiar_matriz(matriz)
                    )
                )

            # Eliminar el valor de la columna pivote en TODAS las demás filas.
            for r in range(filas):

                if r == fila_pivote:
                    continue

                factor = matriz[r][col]
                if es_cero(factor, is_fraction, TOLERANCIA):
                    continue

                for c in range(col, columnas):

                    matriz[r][c] -= (
                        factor *
                        matriz[fila_pivote][c]
                    )

                if es_cero(matriz[r][col], is_fraction, TOLERANCIA):
                    matriz[r][col] = Fraction(0) if is_fraction else 0.0

                pasos.append(
                    (
                        f"F{r + 1} = F{r + 1} - "
                        f"({format_val(factor)}) * F{fila_pivote + 1}",
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
            if es_cero(matriz[i][j], is_fraction, TOLERANCIA):
                matriz[i][j] = Fraction(0) if is_fraction else 0.0

    return matriz, pasos, columnas_pivote