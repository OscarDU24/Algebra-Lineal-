# ==========================================================
# LÓGICA MATEMÁTICA
# Contiene los algoritmos utilizados para resolver sistemas
# de ecuaciones lineales mediante eliminación de Gauss y
# Gauss-Jordan.
#
# Este archivo no contiene input() ni print(). Su función es
# recibir matrices, realizar cálculos y devolver resultados.
#
# No se utilizan NumPy, SciPy ni funciones de álgebra lineal.
# ==========================================================


# ==========================================================
# COPIAR MATRIZ
# Crea una copia independiente de una matriz para evitar
# modificar accidentalmente la matriz original.
# ==========================================================

def copiar_matriz(matriz):
    copia = []
    for fila in matriz:
        copia.append(fila.copy())
    return copia


# ==========================================================
# ELIMINACIÓN GAUSSIANA
# Convierte la matriz aumentada en una matriz escalonada.
# Se realizan operaciones elementales para obtener ceros
# debajo de cada pivote.
# ==========================================================

def eliminacion_gaussiana(matriz):
    matriz = copiar_matriz(matriz)
    filas = len(matriz)
    columnas = len(matriz[0])
    pasos = []
    pivote = 0
    for columna in range(columnas - 1):
        if pivote >= filas:
            break

        # --------------------------------------------------
        # BUSCAR UNA FILA PARA UTILIZAR COMO PIVOTE
        # --------------------------------------------------

        fila_pivote = pivote
        while (
            fila_pivote < filas
            and abs(matriz[fila_pivote][columna]) < 0.000001
        ):
            fila_pivote += 1
        if fila_pivote == filas:
            continue

        # --------------------------------------------------
        # INTERCAMBIAR FILAS SI ES NECESARIO
        # --------------------------------------------------

        if fila_pivote != pivote:
            matriz[pivote], matriz[fila_pivote] = (
                matriz[fila_pivote],
                matriz[pivote]
            )
            pasos.append((
                f"Intercambio de filas {pivote + 1} y "
                f"{fila_pivote + 1}",
                copiar_matriz(matriz)
            ))

        # --------------------------------------------------
        # ELIMINAR LOS ELEMENTOS DEBAJO DEL PIVOTE
        # --------------------------------------------------
        for fila in range(pivote + 1, filas):
            if abs(matriz[fila][columna]) > 0.000001:
                factor = (
                    matriz[fila][columna]
                    / matriz[pivote][columna]
                )
                for j in range(columna, columnas):
                    matriz[fila][j] -= (
                        factor * matriz[pivote][j]
                    )
                pasos.append((
                    f"F{fila + 1} = F{fila + 1} - "
                    f"({factor:.4f})F{pivote + 1}",
                    copiar_matriz(matriz)
                ))
        pivote += 1
    return matriz, pasos


# ==========================================================
# SUSTITUCIÓN HACIA ATRÁS
# Obtiene los valores de las variables a partir de una
# matriz escalonada cuando existe una solución única.
# ==========================================================

def sustitucion_hacia_atras(matriz):
    variables = len(matriz[0]) - 1
    solucion = [0] * variables
    for i in range(variables - 1, -1, -1):
        resultado = matriz[i][variables]
        for j in range(i + 1, variables):
            resultado -= matriz[i][j] * solucion[j]
        solucion[i] = resultado / matriz[i][i]
    return solucion


# ==========================================================
# ELIMINACIÓN GAUSS-JORDAN
# Convierte la matriz aumentada en una matriz escalonada
# reducida, eliminando los valores tanto debajo como encima
# de cada pivote.
# ==========================================================

def eliminacion_gauss_jordan(matriz):
    matriz = copiar_matriz(matriz)
    filas = len(matriz)
    columnas = len(matriz[0])
    pasos = []
    pivote = 0

    for columna in range(columnas - 1):
        if pivote >= filas:
            break
        # --------------------------------------------------
        # BUSCAR FILA PARA EL PIVOTE
        # --------------------------------------------------

        fila_pivote = pivote
        while (
            fila_pivote < filas
            and abs(matriz[fila_pivote][columna]) < 0.000001
        ):
            fila_pivote += 1
        if fila_pivote == filas:
            continue

        # --------------------------------------------------
        # INTERCAMBIAR FILAS
        # --------------------------------------------------

        if fila_pivote != pivote:
            matriz[pivote], matriz[fila_pivote] = (
                matriz[fila_pivote],
                matriz[pivote]
            )
            pasos.append((
                f"Intercambio de filas {pivote + 1} y "
                f"{fila_pivote + 1}",
                copiar_matriz(matriz)
            ))

        # --------------------------------------------------
        # CONVERTIR EL PIVOTE EN UNO
        # --------------------------------------------------

        valor_pivote = matriz[pivote][columna]
        for j in range(columnas):
            matriz[pivote][j] /= valor_pivote
        pasos.append((
            f"F{pivote + 1} = F{pivote + 1} / "
            f"{valor_pivote:.4f}",
            copiar_matriz(matriz)
        ))
        # --------------------------------------------------
        # ELIMINAR LOS VALORES ENCIMA Y DEBAJO DEL PIVOTE
        # --------------------------------------------------

        for fila in range(filas):
            if fila != pivote:
                if abs(matriz[fila][columna]) > 0.000001:
                    factor = matriz[fila][columna]
                    for j in range(columnas):
                        matriz[fila][j] -= (
                            factor * matriz[pivote][j]
                        )
                    pasos.append((
                        f"F{fila + 1} = F{fila + 1} - "
                        f"({factor:.4f})F{pivote + 1}",
                        copiar_matriz(matriz)
                    ))
        pivote += 1
    return matriz, pasos


# ==========================================================
# CLASIFICAR SISTEMA
# Determina si el sistema posee solución única, infinitas
# soluciones o ninguna solución.
#
# Un sistema es inconsistente cuando aparece una fila:
#
# 0 0 0 | k
#
# donde k es diferente de cero.
# ==========================================================

def clasificar_sistema(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    variables = columnas - 1
    rango = 0

    for i in range(filas):
        tiene_coeficiente = False
        for j in range(variables):
            if abs(matriz[i][j]) > 0.000001:
                tiene_coeficiente = True
                break

        # --------------------------------------------------
        # DETECTAR SISTEMA INCONSISTENTE
        # --------------------------------------------------

        if not tiene_coeficiente:
            if abs(matriz[i][variables]) > 0.000001:
                return "Sistema Inconsistente"
        else:
            rango += 1

    # ------------------------------------------------------
    # SOLUCIÓN ÚNICA
    # ------------------------------------------------------
    if rango == variables:
        return "Sistema Consistente Determinado"

    # ------------------------------------------------------
    # INFINITAS SOLUCIONES
    # ------------------------------------------------------
    return "Sistema Consistente Indeterminado"


# ==========================================================
# OBTENER SOLUCIÓN MEDIANTE GAUSS
# Utiliza sustitución hacia atrás después de obtener la
# matriz escalonada.
# ==========================================================

def obtener_solucion_gauss(matriz):
    clasificacion = clasificar_sistema(matriz)
    if clasificacion != "Sistema Consistente Determinado":
        return None
    return sustitucion_hacia_atras(matriz)


# ==========================================================
# OBTENER SOLUCIÓN MEDIANTE GAUSS-JORDAN
# Obtiene directamente los valores de las variables desde
# la última columna de la matriz reducida.
# ==========================================================

def obtener_solucion_gauss_jordan(matriz):
    clasificacion = clasificar_sistema(matriz)
    if clasificacion != "Sistema Consistente Determinado":
        return None
    variables = len(matriz[0]) - 1
    solucion = []
    for i in range(variables):
        solucion.append(matriz[i][variables])
    return solucion


# ==========================================================
# VERIFICAR SOLUCIÓN
# Sustituye automáticamente las soluciones obtenidas en el
# sistema original para comprobar que las igualdades se
# cumplen.
# ==========================================================

def verificar_solucion(matriz_original, solucion):
    variables = len(solucion)
    for i in range(len(matriz_original)):
        resultado = 0
        for j in range(variables):
            resultado += (
                matriz_original[i][j] * solucion[j]
            )
        independiente = matriz_original[i][variables]
        if abs(resultado - independiente) > 0.000001:
            return False
    return True