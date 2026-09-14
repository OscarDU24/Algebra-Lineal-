from fractions import Fraction
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

    # Detectar si estamos trabajando con fracciones
    is_fraction = any(isinstance(val, Fraction) for row in matriz for val in row)

    def format_val(val):
        """Función auxiliar para formatear fracciones o decimales limpiamente."""
        if isinstance(val, Fraction):
            if val.denominator == 1:
                return str(val.numerator)
            return f"{val.numerator}/{val.denominator}"
        else:
            if isinstance(val, float) and abs(val - round(val)) < 1e-9:
                return str(int(round(val)))
            s = f"{val:.4f}"
            if "." in s:
                s = s.rstrip("0").rstrip(".")
            return s

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
            # Comparación segura considerando Fracciones o Floats
            val_r = abs(matriz[r][col]) if not is_fraction else abs(float(matriz[r][col]))
            val_max = abs(matriz[fila_max][col]) if not is_fraction else abs(float(matriz[fila_max][col]))
            if val_r > val_max:
                fila_max = r

        # Si la columna no posee un pivote diferente de cero,
        # se pasa a la siguiente columna.
        val_piv_check = abs(matriz[fila_max][col]) if not is_fraction else abs(float(matriz[fila_max][col]))
        if val_piv_check < TOLERANCIA:
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

                val_check = abs(matriz[r][col]) if not is_fraction else abs(float(matriz[r][col]))
                if val_check < TOLERANCIA:
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
                val_clean = abs(matriz[r][col]) if not is_fraction else abs(float(matriz[r][col]))
                if val_clean < TOLERANCIA:
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
            val_piv_num = float(valor_pivote) if is_fraction else valor_pivote
            if abs(val_piv_num - 1.0) > TOLERANCIA:

                for c in range(col, columnas):

                    matriz[fila_pivote][c] /= valor_pivote

                pasos.append(
                    (
                        f"F{fila_pivote + 1} = "
                        f"F{fila_pivote + 1} / "
                        f"{format_val(valor_pivote)}",
                        copiar_matriz(matriz)
                    )
                )

            # Eliminación únicamente debajo del pivote.
            for r in range(fila_pivote + 1, filas):

                factor = matriz[r][col]
                fact_num = float(factor) if is_fraction else factor

                if abs(fact_num) < TOLERANCIA:
                    continue

                for c in range(col, columnas):

                    matriz[r][c] -= (
                        factor *
                        matriz[fila_pivote][c]
                    )

                val_clean = abs(matriz[r][col]) if not is_fraction else abs(float(matriz[r][col]))
                if val_clean < TOLERANCIA:
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
            val_piv_num = float(valor_pivote) if is_fraction else valor_pivote
            if abs(val_piv_num - 1.0) > TOLERANCIA:

                for c in range(col, columnas):

                    matriz[fila_pivote][c] /= valor_pivote

                pasos.append(
                    (
                        f"F{fila_pivote + 1} = "
                        f"F{fila_pivote + 1} / "
                        f"{format_val(valor_pivote)}",
                        copiar_matriz(matriz)
                    )
                )

            # Eliminar el valor de la columna pivote en TODAS las demás filas.
            for r in range(filas):

                if r == fila_pivote:
                    continue

                factor = matriz[r][col]
                fact_num = float(factor) if is_fraction else factor

                if abs(fact_num) < TOLERANCIA:
                    continue

                for c in range(col, columnas):

                    matriz[r][c] -= (
                        factor *
                        matriz[fila_pivote][c]
                    )

                val_clean = abs(matriz[r][col]) if not is_fraction else abs(float(matriz[r][col]))
                if val_clean < TOLERANCIA:
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
            val_clean = abs(matriz[i][j]) if not is_fraction else abs(float(matriz[i][j]))
            if val_clean < TOLERANCIA:
                matriz[i][j] = Fraction(0) if is_fraction else 0.0

    return matriz, pasos, columnas_pivote