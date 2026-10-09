"""Operaciones matemáticas con matrices particionadas en bloques 2 x 2."""


_NOMBRES_BLOQUES = ("A11", "A12", "A21", "A22")


def _validar_matriz(matriz, nombre="La matriz"):
    if not isinstance(matriz, list) or not matriz:
        raise ValueError(f"{nombre} debe ser una lista de filas no vacía.")
    if any(not isinstance(fila, list) or not fila for fila in matriz):
        raise ValueError(f"{nombre} debe contener filas no vacías.")
    columnas = len(matriz[0])
    if any(len(fila) != columnas for fila in matriz):
        raise ValueError(f"{nombre} debe ser rectangular.")
    return len(matriz), columnas


def _validar_cortes(filas, columnas, fila_corte, col_corte):
    if not isinstance(fila_corte, int) or not 0 < fila_corte < filas:
        raise ValueError(
            f"El corte horizontal debe estar entre 1 y {filas - 1}."
        )
    if not isinstance(col_corte, int) or not 0 < col_corte < columnas:
        raise ValueError(
            f"El corte vertical debe estar entre 1 y {columnas - 1}."
        )


def _validar_bloques(bloques, nombre):
    if not isinstance(bloques, dict):
        raise ValueError(f"{nombre} debe ser un diccionario de bloques.")
    faltantes = [clave for clave in _NOMBRES_BLOQUES if clave not in bloques]
    if faltantes:
        raise ValueError(
            f"{nombre} debe contener los bloques: {', '.join(_NOMBRES_BLOQUES)}."
        )
    dimensiones = {
        clave: _validar_matriz(bloques[clave], f"{nombre}.{clave}")
        for clave in _NOMBRES_BLOQUES
    }
    a11 = dimensiones["A11"]
    a12 = dimensiones["A12"]
    a21 = dimensiones["A21"]
    a22 = dimensiones["A22"]
    if a11[0] != a12[0] or a21[0] != a22[0]:
        raise ValueError(f"Los bloques horizontales de {nombre} deben tener igual altura.")
    if a11[1] != a21[1] or a12[1] != a22[1]:
        raise ValueError(f"Los bloques verticales de {nombre} deben tener igual anchura.")
    return dimensiones


def particionar_matriz(A, fila_corte, col_corte):
    """Divide A en A11, A12, A21 y A22 según cortes internos."""
    filas, columnas = _validar_matriz(A, "La matriz A")
    _validar_cortes(filas, columnas, fila_corte, col_corte)
    return {
        "A11": [fila[:col_corte] for fila in A[:fila_corte]],
        "A12": [fila[col_corte:] for fila in A[:fila_corte]],
        "A21": [fila[:col_corte] for fila in A[fila_corte:]],
        "A22": [fila[col_corte:] for fila in A[fila_corte:]],
    }


def reensamblar_bloques(A_bloques):
    """Combina un arreglo 2 x 2 de bloques conformables en una matriz."""
    dimensiones = _validar_bloques(A_bloques, "Los bloques")
    if dimensiones["A11"][0] != dimensiones["A12"][0]:
        raise ValueError("A11 y A12 deben tener igual altura para reensamblar.")
    return [
        fila_izquierda + fila_derecha
        for bloque_izquierdo, bloque_derecho in (
            (A_bloques["A11"], A_bloques["A12"]),
            (A_bloques["A21"], A_bloques["A22"]),
        )
        for fila_izquierda, fila_derecha in zip(bloque_izquierdo, bloque_derecho)
    ]


def suma_bloques(A_bloques, B_bloques):
    """Suma dos matrices de bloques posición por posición."""
    dimensiones_a = _validar_bloques(A_bloques, "A")
    dimensiones_b = _validar_bloques(B_bloques, "B")
    resultado = {}
    for nombre in _NOMBRES_BLOQUES:
        if dimensiones_a[nombre] != dimensiones_b[nombre]:
            raise ValueError(
                f"Los bloques A.{nombre} y B.{nombre} deben tener las mismas dimensiones."
            )
        resultado[nombre] = [
            [valor_a + valor_b for valor_a, valor_b in zip(fila_a, fila_b)]
            for fila_a, fila_b in zip(A_bloques[nombre], B_bloques[nombre])
        ]
    return resultado


def _producto_matrices(A, B):
    filas_a, columnas_a = _validar_matriz(A, "La matriz izquierda")
    filas_b, columnas_b = _validar_matriz(B, "La matriz derecha")
    if columnas_a != filas_b:
        raise ValueError(
            "Las columnas de la matriz izquierda deben coincidir con las filas "
            "de la matriz derecha."
        )
    resultado = [[0 for _ in range(columnas_b)] for _ in range(filas_a)]
    for fila in range(filas_a):
        for indice in range(columnas_a):
            valor = A[fila][indice]
            if valor == 0:
                continue
            for columna in range(columnas_b):
                resultado[fila][columna] += valor * B[indice][columna]
    return resultado


def _bloque_es_cero(bloque):
    return all(valor == 0 for fila in bloque for valor in fila)


def multiplicacion_bloques(A_bloques, B_bloques):
    """Multiplica arreglos de bloques 2 x 2, omitiendo bloques cero."""
    dimensiones_a = _validar_bloques(A_bloques, "A")
    dimensiones_b = _validar_bloques(B_bloques, "B")

    # Las columnas de cada bloque de A deben conformar con la fila de bloques de B.
    for bloque_a, bloque_b in (("A11", "A11"), ("A21", "A11"),
                               ("A12", "A21"), ("A22", "A21")):
        columna_a = dimensiones_a[bloque_a][1]
        fila_b = dimensiones_b[bloque_b][0]
        if columna_a != fila_b:
            raise ValueError(
                "La partición interna no es conformable: las anchuras de bloques "
                f"de A deben coincidir con las alturas de bloques de B "
                f"({bloque_a}: {columna_a}, {bloque_b}: {fila_b})."
            )

    bloques_a = (
        (A_bloques["A11"], A_bloques["A12"]),
        (A_bloques["A21"], A_bloques["A22"]),
    )
    bloques_b = (
        (B_bloques["A11"], B_bloques["A12"]),
        (B_bloques["A21"], B_bloques["A22"]),
    )
    resultado = {}
    for fila_bloques in range(2):
        for columna_bloques in range(2):
            productos = []
            for indice_bloques in range(2):
                bloque_a = bloques_a[fila_bloques][indice_bloques]
                bloque_b = bloques_b[indice_bloques][columna_bloques]
                if _bloque_es_cero(bloque_a) or _bloque_es_cero(bloque_b):
                    continue
                productos.append(_producto_matrices(bloque_a, bloque_b))

            nombre = f"A{fila_bloques + 1}{columna_bloques + 1}"
            if not productos:
                alto = dimensiones_a[f"A{fila_bloques + 1}1"][0]
                ancho = dimensiones_b[f"A1{columna_bloques + 1}"][1]
                resultado[nombre] = [[0 for _ in range(ancho)] for _ in range(alto)]
                continue

            alto = len(productos[0])
            ancho = len(productos[0][0])
            suma = [[0 for _ in range(ancho)] for _ in range(alto)]
            for producto in productos:
                if len(producto) != alto or len(producto[0]) != ancho:
                    raise ValueError(
                        "Los productos parciales de un bloque no tienen dimensiones conformables."
                    )
                for fila in range(alto):
                    for columna in range(ancho):
                        suma[fila][columna] += producto[fila][columna]
            resultado[nombre] = suma
    _validar_bloques(resultado, "El resultado")
    return resultado


def _producto_matrices_compatible(A, B):
    """Producto matricial local para la fórmula de inversión por bloques."""
    return _producto_matrices(A, B)


def inversa_triangular_bloques(A11, A12, A22, funcion_inversa_externa):
    """Invierte una matriz triangular superior por bloques."""
    if not callable(funcion_inversa_externa):
        raise ValueError("Debe proporcionar una función externa para invertir los bloques.")
    filas_11, columnas_11 = _validar_matriz(A11, "A11")
    filas_12, columnas_12 = _validar_matriz(A12, "A12")
    filas_22, columnas_22 = _validar_matriz(A22, "A22")
    if filas_11 != columnas_11 or filas_22 != columnas_22:
        raise ValueError("A11 y A22 deben ser matrices cuadradas.")
    if columnas_11 != filas_12 or columnas_22 != columnas_12:
        raise ValueError("A12 debe tener tantas filas como A11 y columnas como A22.")

    inversa_11 = funcion_inversa_externa(A11)
    inversa_22 = funcion_inversa_externa(A22)
    filas_i11, columnas_i11 = _validar_matriz(inversa_11, "La inversa de A11")
    filas_i22, columnas_i22 = _validar_matriz(inversa_22, "La inversa de A22")
    if (filas_i11, columnas_i11) != (filas_11, columnas_11):
        raise ValueError("La función de inversión devolvió una inversa inválida para A11.")
    if (filas_i22, columnas_i22) != (filas_22, columnas_22):
        raise ValueError("La función de inversión devolvió una inversa inválida para A22.")

    producto = _producto_matrices_compatible(
        _producto_matrices_compatible(inversa_11, A12),
        inversa_22,
    )
    inversa_12 = [[-valor for valor in fila] for fila in producto]
    inversa_21 = [[0 for _ in range(columnas_i11)] for _ in range(filas_i22)]
    resultado = {
        "A11": inversa_11,
        "A12": inversa_12,
        "A21": inversa_21,
        "A22": inversa_22,
    }
    _validar_bloques(resultado, "La inversa")
    return resultado
