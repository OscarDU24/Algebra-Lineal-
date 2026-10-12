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


def _expandir_cofactores_detallado(
    matriz, filas_origen, columnas_origen, formato, nivel=0, nombre_matriz="M"
):
    orden = len(matriz)
    prefijo = "  " * nivel
    if orden == 1:
        return matriz[0][0], [f"{prefijo}Determinante de 1 × 1: {_formatear(matriz[0][0], formato)}"]
    if orden == 2:
        a, b = matriz[0]
        c, d = matriz[1]
        primero = a * d
        segundo = b * c
        resultado = primero - segundo
        lineas = [
            f"{prefijo}Operación: det({nombre_matriz}) = "
            f"({_formatear(a, formato)} * {_formatear(d, formato)}) - "
            f"({_formatear(b, formato)} * {_formatear(c, formato)}) = "
            f"{_formatear(primero, formato)} - {_formatear(segundo, formato)} "
            f"= {_formatear(resultado, formato)}"
        ]
        return resultado, lineas

    aportes = []
    lineas = []
    for columna, valor in enumerate(matriz[0]):
        signo = 1 if columna % 2 == 0 else -1
        fila_original = filas_origen[0]
        columna_original = columnas_origen[columna]
        menor = [
            fila[:columna] + fila[columna + 1:]
            for fila in matriz[1:]
        ]
        filas_menor = filas_origen[1:]
        columnas_menor = (
            columnas_origen[:columna] + columnas_origen[columna + 1:]
        )
        lineas.append(
            f"{prefijo}Elemento a{fila_original + 1},{columna_original + 1} = "
            f"{_formatear(valor, formato)} (Signo: {'+1' if signo > 0 else '-1'})"
        )
        lineas.append(
            f"{prefijo}Submatriz M{fila_original + 1},{columna_original + 1}:"
        )
        lineas.extend(
            f"{prefijo}[ " + "   ".join(
                _formatear(elemento, formato) for elemento in fila
            ) + " ]"
            for fila in menor
        )
        determinante_menor, desarrollo_menor = _expandir_cofactores_detallado(
            menor,
            filas_menor,
            columnas_menor,
            formato,
            nivel + 1,
            f"M{fila_original + 1},{columna_original + 1}",
        )
        lineas.extend(desarrollo_menor)
        aporte = signo * valor * determinante_menor
        aportes.append(aporte)
        lineas.append(
            f"{prefijo}Aporte: {_formatear(valor, formato)} * "
            f"{'+1' if signo > 0 else '-1'} * "
            f"{_formatear(determinante_menor, formato)} = "
            f"{_formatear(aporte, formato)}"
        )
        lineas.append("")

    resultado = sum(aportes, Fraction(0))
    expresion_aportes = " ".join(
        ("+" if aporte >= 0 else "-")
        + f" {_formatear(abs(aporte), formato)}"
        for aporte in aportes
    ).lstrip("+ ")
    lineas.extend([
        f"{prefijo}Suma final de aportes: {expresion_aportes} = "
        f"{_formatear(resultado, formato)}",
    ])
    return resultado, lineas


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


def determinante_lu_valor(matriz):
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


def determinante_cofactores_a_string(matriz, formato="Decimales"):
    """Presenta la expansión por cofactores y el desarrollo de cada menor."""
    normalizada = _validar_matriz(matriz)
    determinante, desarrollo = _expandir_cofactores_detallado(
        normalizada,
        list(range(len(normalizada))),
        list(range(len(normalizada))),
        formato,
    )
    salida = [
        "MATRIZ A:",
        _matriz_a_string(normalizada, formato),
        "",
        "EXPANSIÓN POR COFACTORES DE LA PRIMERA FILA:",
    ]
    salida.extend(desarrollo)
    salida.extend(["", f"det(A) = {_formatear(determinante, formato)}"])
    return "\n".join(salida)


def _producto_diagonal_sarrus_4x4(
    matriz_extendida, columnas_ext, columnas_originales, ascendente
):
    nombres = []
    valores = []
    for fila in range(4):
        indice_columna = columnas_ext - fila if ascendente else columnas_ext + fila
        columna_original = columnas_originales[indice_columna]
        nombres.append(f"a{fila + 1}{columna_original + 1}")
        valores.append(matriz_extendida[fila][indice_columna])
    producto = Fraction(1)
    for valor in valores:
        producto *= valor
    return nombres, valores, producto


def _sarrus_4x4_etapa(
    matriz, orden_columnas, signo_etapa, numero, descripcion, formato
):
    columnas_extendidas = orden_columnas + orden_columnas[:3]
    matriz_extendida = [
        [fila[columna] for columna in columnas_extendidas]
        for fila in matriz
    ]
    terminos = []
    for ascendente in (False, True):
        inicios = range(3, 7) if ascendente else range(4)
        for indice, inicio in enumerate(inicios):
            nombres, valores, producto = _producto_diagonal_sarrus_4x4(
                matriz_extendida, inicio, columnas_extendidas, ascendente
            )
            signo = signo_etapa * (1 if indice % 2 == 0 else -1)
            terminos.append((nombres, valores, producto, signo))

    subtotal = sum(
        (signo * producto for _, _, producto, signo in terminos),
        Fraction(0),
    )
    expresion = " ".join(
        f"{'+' if signo > 0 else '−'} ({' * '.join(nombres)})"
        for nombres, _, _, signo in terminos
    )
    sustitucion = " ".join(
        f"{'+' if signo > 0 else '−'} "
        f"({' x '.join(_formatear(valor, formato) for valor in valores)})"
        for _, valores, _, signo in terminos
    )
    productos = " ".join(
        f"{'+' if signo > 0 else '−'} ({_formatear(producto, formato)})"
        for _, _, producto, signo in terminos
    )
    prefijo = f"ETAPA {numero} ({'+' if signo_etapa > 0 else '−'}):"
    salida = [
        prefijo,
        f"Permutación aplicada: {descripcion}",
        "Matriz extendida:",
        _matriz_a_string(matriz_extendida, formato),
        f"Operación: {expresion}",
        f"Sustitución: {sustitucion}",
        f"Sumas parciales: {productos}",
        f"Resultado de la etapa: {_formatear(subtotal, formato)}",
    ]
    return salida, subtotal


def determinante_sarrus_a_string(matriz, formato="Decimales"):
    """Explica Sarrus para 3x3 y su extensión por permutaciones para 4x4."""
    normalizada = _validar_matriz(matriz)
    orden = len(normalizada)
    if orden not in (3, 4):
        raise ValueError(
            "La Regla de Sarrus solo está soportada para matrices 3 × 3 y 4 × 4."
        )

    salida = ["MATRIZ A:", _matriz_a_string(normalizada, formato), ""]
    if orden == 3:
        diagonales_positivas = (
            ((0, 0), (1, 1), (2, 2)),
            ((1, 0), (2, 1), (0, 2)),
            ((2, 0), (0, 1), (1, 2)),
        )
        diagonales_negativas = (
            ((2, 0), (1, 1), (0, 2)),
            ((0, 0), (2, 1), (1, 2)),
            ((1, 0), (0, 1), (2, 2)),
        )

        def datos_diagonales(diagonales):
            expresion = []
            sustitucion = []
            productos = []
            for coordenadas in diagonales:
                valores = [
                    normalizada[fila][columna]
                    for fila, columna in coordenadas
                ]
                expresion.append(
                    "*".join(
                        f"a{fila + 1}{columna + 1}"
                        for fila, columna in coordenadas
                    )
                )
                sustitucion.append(
                    "x".join(_formatear(valor, formato) for valor in valores)
                )
                producto = Fraction(1)
                for valor in valores:
                    producto *= valor
                productos.append(producto)
            return expresion, sustitucion, productos

        op_pos, sub_pos, prod_pos = datos_diagonales(diagonales_positivas)
        op_neg, sub_neg, prod_neg = datos_diagonales(diagonales_negativas)
        suma_positiva = sum(prod_pos, Fraction(0))
        suma_negativa = sum(prod_neg, Fraction(0))
        determinante = suma_positiva - suma_negativa
        salida.extend([
            "Regla de Sarrus:",
            f"Operación: ({' + '.join(op_pos)}) - ({' + '.join(op_neg)})",
            f"Sustitución: ({' + '.join(sub_pos)}) - ({' + '.join(sub_neg)})",
            "Sumas parciales: ("
            + " + ".join(_formatear(valor, formato) for valor in prod_pos)
            + ") - ("
            + " + ".join(_formatear(valor, formato) for valor in prod_neg)
            + ")",
            f"Resultado: {_formatear(suma_positiva, formato)} - "
            f"{_formatear(suma_negativa, formato)} = "
            f"{_formatear(determinante, formato)}",
            f"RESULTADO: det(A) = {_formatear(determinante, formato)}",
        ])
        return "\n".join(salida)

    etapas = (
        ((0, 1, 2, 3), 1, "ninguna; matriz original"),
        ((0, 2, 1, 3), -1, "C2 ↔ C3"),
        ((0, 2, 3, 1), 1, "C3 ↔ C4 sobre la etapa 2"),
    )
    subtotales = []
    for numero, (orden_columnas, signo, descripcion) in enumerate(etapas, start=1):
        if numero > 1:
            salida.append("")
        texto_etapa, subtotal = _sarrus_4x4_etapa(
            normalizada, orden_columnas, signo, numero, descripcion, formato
        )
        salida.extend(texto_etapa)
        subtotales.append(subtotal)

    determinante = sum(subtotales, Fraction(0))
    salida.extend([
        "",
        "Suma de resultados parciales: "
        + " + ".join(_formatear(valor, formato) for valor in subtotales),
        f"RESULTADO: det(A) = {_formatear(determinante, formato)}",
    ])
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
        return determinante_sarrus_a_string(normalizada, formato)
    return "\n".join(salida)
