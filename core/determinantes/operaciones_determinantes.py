"""Cálculo exacto de determinantes y sistemas lineales mediante listas y Fraction."""

from fractions import Fraction

from core.matriciales import conversionesMatriciales as conv


def convertir_entrada(valor):
    """Interpreta enteros, decimales y fracciones introducidos por el usuario."""
    try:
        return Fraction(str(valor).strip())
    except (ValueError, TypeError, ZeroDivisionError) as error:
        raise ValueError(f"El valor '{valor}' no es un número válido.") from error


def _validar_matriz(matriz):
    if not isinstance(matriz, (list, tuple)) or not matriz:
        raise ValueError("La matriz debe ser cuadrada y no estar vacía.")
    orden = len(matriz)
    if any(not isinstance(fila, (list, tuple)) or len(fila) != orden for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada.")

    resultado = []
    for indice_fila, fila in enumerate(matriz):
        try:
            resultado.append([
                valor if isinstance(valor, Fraction) else Fraction(str(valor))
                for valor in fila
            ])
        except (ValueError, TypeError, ZeroDivisionError) as error:
            raise ValueError(
                f"La fila {indice_fila + 1} contiene un valor no numérico."
            ) from error
    return resultado


def _formatear(valor, formato):
    if formato == "Fracciones":
        return conv.convertir_a_fraccion(valor)
    try:
        numero = float(valor)
    except OverflowError:
        return conv.convertir_a_fraccion(valor)
    if abs(numero) < 1e-12:
        numero = 0.0
    if numero.is_integer():
        return str(int(numero))
    return f"{numero:.6f}".rstrip("0").rstrip(".")


def _matriz_a_string(matriz, formato):
    return "\n".join(
        "[ " + "   ".join(_formatear(valor, formato) for valor in fila) + " ]"
        for fila in matriz
    )


def _determinante_cofactores(matriz):
    orden = len(matriz)
    if orden == 1:
        return matriz[0][0]
    if orden == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

    resultado = Fraction(0)
    for columna, valor in enumerate(matriz[0]):
        if valor == 0:
            continue
        menor = [
            fila[:columna] + fila[columna + 1:]
            for fila in matriz[1:]
        ]
        resultado += (-1 if columna % 2 else 1) * valor * _determinante_cofactores(menor)
    return resultado


def analizar_eficiencia_determinante(matriz):
    """Compara el crecimiento factorial de cofactores con el costo cúbico de LU."""
    normalizada = _validar_matriz(matriz)
    orden = len(normalizada)

    if orden <= 20:
        operaciones_cofactores = 1
        for factor in range(2, orden + 1):
            operaciones_cofactores *= factor
        estimacion_cofactores = f"~{operaciones_cofactores:,}"
    else:
        estimacion_cofactores = f"~{orden}!"

    operaciones_lu = (2 * orden ** 3) // 3 + orden
    if orden <= 3:
        recomendado = "Cofactores"
        recomendacion = (
            "Cofactores o Sarrus: para este tamaño, la diferencia de rendimiento "
            "es insignificante."
        )
    elif orden == 4:
        recomendado = "LU / Triangulación"
        recomendacion = (
            "Se recomienda LU por rendimiento; Cofactores sigue siendo viable."
        )
    else:
        recomendado = "LU / Triangulación"
        recomendacion = (
            "SE RECOMIENDA FUERTEMENTE LU. Cofactores crece factorialmente y "
            "resulta inviable para este orden."
        )

    texto = "\n".join([
        f"ANÁLISIS PREVIO DE EFICIENCIA ({orden} × {orden})",
        f"Cofactores: {estimacion_cofactores} operaciones aproximadas (O(n!)).",
        f"LU / triangulación: ~{operaciones_lu:,} operaciones (O(n³)).",
        f"RECOMENDACIÓN: {recomendacion}",
    ])
    return texto, recomendado


def _factorizar_lu(matriz):
    """Devuelve P, L, U y los pasos de eliminación para P·A = L·U."""
    orden = len(matriz)
    superior = [fila[:] for fila in matriz]
    inferior = [
        [Fraction(int(fila == columna)) for columna in range(orden)]
        for fila in range(orden)
    ]
    permutacion = list(range(orden))
    intercambios = 0
    pasos = []
    singular = False

    for columna in range(orden):
        fila_pivote = max(
            range(columna, orden),
            key=lambda fila: abs(superior[fila][columna]),
        )
        if superior[fila_pivote][columna] == 0:
            singular = True
            pasos.append((f"Columna {columna + 1}: no hay pivote distinto de cero; "
                          "la matriz es singular.", [fila[:] for fila in inferior],
                          [fila[:] for fila in superior]))
            continue

        if fila_pivote != columna:
            superior[columna], superior[fila_pivote] = (
                superior[fila_pivote],
                superior[columna],
            )
            permutacion[columna], permutacion[fila_pivote] = (
                permutacion[fila_pivote],
                permutacion[columna],
            )
            for indice in range(columna):
                inferior[columna][indice], inferior[fila_pivote][indice] = (
                    inferior[fila_pivote][indice],
                    inferior[columna][indice],
                )
            intercambios += 1
            pasos.append((
                f"Intercambiar F{columna + 1} ↔ F{fila_pivote + 1} "
                f"(intercambio {intercambios}; cambia el signo).",
                [fila[:] for fila in inferior],
                [fila[:] for fila in superior],
            ))

        pivote = superior[columna][columna]
        eliminaciones = []
        for fila in range(columna + 1, orden):
            multiplicador = superior[fila][columna] / pivote
            inferior[fila][columna] = multiplicador
            superior[fila][columna] = Fraction(0)
            for indice in range(columna + 1, orden):
                superior[fila][indice] -= multiplicador * superior[columna][indice]
            eliminaciones.append(
                f"m{fila + 1},{columna + 1} = "
                f"{_formatear(multiplicador, 'Fracciones')}; "
                f"F{fila + 1} ← F{fila + 1} − "
                f"m{fila + 1},{columna + 1}·F{columna + 1}"
            )
        if eliminaciones:
            pasos.append((
                f"Eliminación en la columna {columna + 1}: "
                + "; ".join(eliminaciones) + ".",
                [fila_actual[:] for fila_actual in inferior],
                [fila_actual[:] for fila_actual in superior],
            ))

    return inferior, superior, permutacion, intercambios, pasos, singular


def _determinante_lu_valor(matriz):
    _, superior, _, intercambios, _, singular = _factorizar_lu(matriz)
    if singular:
        return Fraction(0)
    producto = Fraction(1)
    for indice in range(len(superior)):
        producto *= superior[indice][indice]
    return (-1 if intercambios % 2 else 1) * producto


def determinante_lu_a_string(matriz, formato="Decimales"):
    """Explica la eliminación con pivoteo parcial y evalúa det(A) mediante LU."""
    normalizada = _validar_matriz(matriz)
    inferior, superior, permutacion, intercambios, pasos, singular = (
        _factorizar_lu(normalizada)
    )
    salida = [
        "MATRIZ INICIAL A:",
        _matriz_a_string(normalizada, formato),
        "",
        "Factorización con pivoteo parcial: P·A = L·U",
        "Cada multiplicador de eliminación se almacena en L.",
    ]
    for descripcion, matriz_l, matriz_u in pasos:
        salida.extend([
            f">> {descripcion}",
            "U:",
            _matriz_a_string(matriz_u, formato),
            "L:",
            _matriz_a_string(matriz_l, formato),
            "",
        ])

    diagonal = [superior[indice][indice] for indice in range(len(superior))]
    producto = Fraction(1)
    for valor in diagonal:
        producto *= valor
    signo = -1 if intercambios % 2 else 1
    determinante = Fraction(0) if singular else signo * producto
    salida.extend([
        "MATRIZ L FINAL:",
        _matriz_a_string(inferior, formato),
        "",
        "MATRIZ U FINAL:",
        _matriz_a_string(superior, formato),
        "",
        "Permutación de filas: " + ", ".join(str(fila + 1) for fila in permutacion),
        f"Intercambios de filas: {intercambios}",
        f"Factor de signo: (-1)^{intercambios} = {signo}",
        "Diagonal de U: " + " × ".join(_formatear(valor, formato) for valor in diagonal),
        f"Producto de la diagonal: {_formatear(producto, formato)}",
        "",
        "det(A) = factor de signo × producto de la diagonal de U",
        f"det(A) = {signo} × {_formatear(producto, formato)}",
        f"RESULTADO: det(A) = {_formatear(determinante, formato)}",
    ])
    return "\n".join(salida)


def resolver_sistema_cramer_a_string(matriz_A, vector_b, formato="Decimales"):
    """Conserva la alternativa Cramer del prototipo con cálculo racional exacto."""
    matriz = _validar_matriz(matriz_A)
    if not isinstance(vector_b, (list, tuple)) or len(vector_b) != len(matriz):
        raise ValueError("El vector b debe tener una componente por cada fila de A.")
    try:
        vector = [
            valor if isinstance(valor, Fraction) else Fraction(str(valor))
            for valor in vector_b
        ]
    except (ValueError, TypeError, ZeroDivisionError) as error:
        raise ValueError("El vector b contiene un valor no numérico.") from error

    determinante_principal = _determinante_lu_valor(matriz)
    salida = [
        "RESOLUCIÓN DEL SISTEMA Ax = b MEDIANTE LA REGLA DE CRAMER",
        "Matriz A:",
        _matriz_a_string(matriz, formato),
        "Vector b: [ " + "   ".join(_formatear(valor, formato) for valor in vector) + " ]",
        "",
        f"D = det(A) = {_formatear(determinante_principal, formato)}",
        "",
    ]
    if determinante_principal == 0:
        salida.append(
            "D = 0; la Regla de Cramer no permite obtener una solución única."
        )
        return "\n".join(salida)

    soluciones = []
    for columna in range(len(matriz)):
        matriz_cramer = [fila[:] for fila in matriz]
        for fila in range(len(matriz)):
            matriz_cramer[fila][columna] = vector[fila]
        determinante_columna = _determinante_lu_valor(matriz_cramer)
        solucion = determinante_columna / determinante_principal
        soluciones.append(solucion)
        salida.extend([
            f"Matriz A{columna + 1} (columna {columna + 1} reemplazada por b):",
            _matriz_a_string(matriz_cramer, formato),
            f"D{columna + 1} = det(A{columna + 1}) = "
            f"{_formatear(determinante_columna, formato)}",
            f"x{columna + 1} = D{columna + 1} / D = "
            f"{_formatear(determinante_columna, formato)} / "
            f"{_formatear(determinante_principal, formato)} = "
            f"{_formatear(solucion, formato)}",
            "",
        ])
    salida.extend([
        "SOLUCIÓN:",
        "[ " + "   ".join(_formatear(valor, formato) for valor in soluciones) + " ]",
    ])
    return "\n".join(salida)


def resolver_sistema_lu_a_string(matriz_A, vector_b, formato="Decimales"):
    """Resuelve Ax=b con pivoteo parcial y muestra sustituciones Ly=Pb y Ux=y."""
    matriz = _validar_matriz(matriz_A)
    if not isinstance(vector_b, (list, tuple)) or len(vector_b) != len(matriz):
        raise ValueError("El vector b debe tener una componente por cada fila de A.")
    try:
        vector = [
            valor if isinstance(valor, Fraction) else Fraction(str(valor))
            for valor in vector_b
        ]
    except (ValueError, TypeError, ZeroDivisionError) as error:
        raise ValueError("El vector b contiene un valor no numérico.") from error

    inferior, superior, permutacion, intercambios, _, singular = (
        _factorizar_lu(matriz)
    )
    if singular:
        raise ValueError(
            "La matriz A es singular; la factorización LU no permite obtener "
            "una solución única."
        )

    permutado = [vector[indice] for indice in permutacion]
    y = []
    salida = [
        "RESOLUCIÓN DEL SISTEMA Ax = b MEDIANTE FACTORIZACIÓN LU",
        "P·A = L·U; por tanto, L·y = P·b y U·x = y.",
        "",
        "Matriz A:",
        _matriz_a_string(matriz, formato),
        "Vector b: [ " + "   ".join(_formatear(valor, formato) for valor in vector) + " ]",
        f"Intercambios de filas: {intercambios}",
        "",
        "MATRIZ L:",
        _matriz_a_string(inferior, formato),
        "",
        "MATRIZ U:",
        _matriz_a_string(superior, formato),
    ]
    if permutacion != list(range(len(matriz))):
        salida.append(
            "Vector permutado P·b: [ "
            + "   ".join(_formatear(valor, formato) for valor in permutado)
            + " ]"
        )

    salida.extend(["", "SUSTITUCIÓN HACIA ADELANTE: L·y = P·b"])
    for fila in range(len(matriz)):
        conocidos = sum(
            inferior[fila][columna] * y[columna]
            for columna in range(fila)
        )
        y_fila = permutado[fila] - conocidos
        y.append(y_fila)
        salida.append(
            f"y{fila + 1} = "
            f"{_formatear(permutado[fila], formato)} − "
            f"{_formatear(conocidos, formato)} = "
            f"{_formatear(y_fila, formato)}"
        )

    x = [Fraction(0) for _ in matriz]
    salida.extend(["", "SUSTITUCIÓN HACIA ATRÁS: U·x = y"])
    for fila in range(len(matriz) - 1, -1, -1):
        conocidos = sum(
            superior[fila][columna] * x[columna]
            for columna in range(fila + 1, len(matriz))
        )
        x[fila] = (y[fila] - conocidos) / superior[fila][fila]
        salida.append(
            f"x{fila + 1} = "
            f"({_formatear(y[fila], formato)} − {_formatear(conocidos, formato)}) "
            f"/ {_formatear(superior[fila][fila], formato)} = "
            f"{_formatear(x[fila], formato)}"
        )

    salida.extend([
        "",
        "SOLUCIÓN:",
        "[ " + "   ".join(_formatear(valor, formato) for valor in x) + " ]",
    ])
    return "\n".join(salida)


def determinante_cofactores_a_string(matriz, formato="Decimales"):
    """Presenta la expansión por la primera fila y su resultado recursivo."""
    normalizada = _validar_matriz(matriz)
    salida = [
        "MATRIZ A:",
        _matriz_a_string(normalizada, formato),
        "",
        "EXPANSIÓN POR COFACTORES DE LA PRIMERA FILA:",
    ]
    aportes = []
    for columna, valor in enumerate(normalizada[0]):
        menor = [
            fila[:columna] + fila[columna + 1:]
            for fila in normalizada[1:]
        ]
        det_menor = _determinante_cofactores(menor) if menor else Fraction(1)
        signo = -1 if columna % 2 else 1
        aporte = signo * valor * det_menor
        aportes.append(aporte)
        salida.append(
            f"a1,{columna + 1}: signo {signo:+d}; "
            f"det(M1,{columna + 1}) = {_formatear(det_menor, formato)}; "
            f"aporte = {_formatear(valor, formato)} × {signo:+d} × "
            f"{_formatear(det_menor, formato)} = {_formatear(aporte, formato)}"
        )
    determinante = sum(aportes, Fraction(0))
    salida.extend(["", f"det(A) = {_formatear(determinante, formato)}"])
    return "\n".join(salida)


def determinante_directo_a_string(matriz, formato="Decimales"):
    """Calcula los casos 1x1, 2x2 y 3x3 con su procedimiento elemental."""
    normalizada = _validar_matriz(matriz)
    orden = len(normalizada)
    if orden > 3:
        raise ValueError("El cálculo directo solo está disponible hasta orden 3.")
    salida = ["MATRIZ A:", _matriz_a_string(normalizada, formato), ""]
    if orden == 1:
        resultado = normalizada[0][0]
        salida.extend(["det(A) = a₁₁", f"det(A) = {_formatear(resultado, formato)}"])
    elif orden == 2:
        a, b = normalizada[0]
        c, d = normalizada[1]
        primero = a * d
        segundo = b * c
        resultado = primero - segundo
        salida.extend([
            "Regla ad − bc:",
            f"det(A) = ({_formatear(a, formato)} × {_formatear(d, formato)}) − "
            f"({_formatear(b, formato)} × {_formatear(c, formato)})",
            f"det(A) = {_formatear(primero, formato)} − "
            f"{_formatear(segundo, formato)} = {_formatear(resultado, formato)}",
            f"RESULTADO: det(A) = {_formatear(resultado, formato)}",
        ])
    else:
        a, b, c = normalizada[0]
        d, e, f = normalizada[1]
        g, h, i = normalizada[2]
        positivas = (a * e * i, b * f * g, c * d * h)
        negativas = (c * e * g, b * d * i, a * f * h)
        resultado = sum(positivas, Fraction(0)) - sum(negativas, Fraction(0))
        salida.extend([
            "Regla de Sarrus:",
            "Diagonales positivas: " + " + ".join(
                _formatear(valor, formato) for valor in positivas
            ) + f" = {_formatear(sum(positivas, Fraction(0)), formato)}",
            "Diagonales negativas: " + " + ".join(
                _formatear(valor, formato) for valor in negativas
            ) + f" = {_formatear(sum(negativas, Fraction(0)), formato)}",
            f"RESULTADO: det(A) = {_formatear(resultado, formato)}",
        ])
    return "\n".join(salida)
