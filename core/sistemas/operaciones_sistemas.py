# ============================================================
# OPERACIONES - SISTEMAS DE ECUACIONES E INDEPENDENCIA LINEAL
# ============================================================

from fractions import Fraction

from core.determinantes.operaciones_determinantes import (
    determinante_lu_valor,
    _factorizar_lu,
    _formatear,
    _matriz_a_string,
    _validar_matriz,
)


def convertir_a_fraccion(valor):
    """Convierte una cadena o número a Fraction. Retorna None si hay error."""
    try:
        # Reemplazar comas por puntos por si el usuario escribe en formato latino.
        if isinstance(valor, str):
            valor = valor.replace(',', '.')
        return Fraction(valor)
    except (TypeError, ValueError, ZeroDivisionError):
        return None

def gauss_jordan(matriz, devolver_pasos=False):
    """
    Aplica el método de Gauss-Jordan con pivoteo parcial a una matriz dada.
    Retorna la matriz escalonada reducida y el número de pivotes.
    """
    # Crear una copia profunda para no alterar la original
    M = [[matriz[i][j] for j in range(len(matriz[0]))] for i in range(len(matriz))]
    filas = len(M)
    cols = len(M[0])
    pasos = []
    if devolver_pasos:
        pasos.append(("Matriz inicial", [fila[:] for fila in M]))

    def registrar_paso(descripcion):
        if devolver_pasos:
            pasos.append((descripcion, [fila[:] for fila in M]))
    
    pivotes_encontrados = 0
    fila_actual = 0
    
    for j in range(cols):
        if fila_actual >= filas:
            break
            
        # 1. Pivoteo Parcial: Buscar el mayor valor absoluto en la columna actual
        max_val = 0
        fila_max = fila_actual
        for i in range(fila_actual, filas):
            if abs(M[i][j]) > max_val:
                max_val = abs(M[i][j])
                fila_max = i
                
        if max_val == 0:
            continue # Toda la columna es cero por debajo de esta fila, pasamos a la siguiente
            
        # Intercambiar filas si es necesario
        if fila_max != fila_actual:
            M[fila_actual], M[fila_max] = M[fila_max], M[fila_actual]
            registrar_paso(
                f"Intercambiar F{fila_actual + 1} ↔ F{fila_max + 1}.",
            )
            
        # 2. Hacer el pivote igual a 1
        pivote = M[fila_actual][j]
        for k in range(cols):
            M[fila_actual][k] /= pivote
        registrar_paso(
            f"Normalizar F{fila_actual + 1}: dividir entre el pivote "
            f"{pivote} de la columna {j + 1}.",
        )
            
        # 3. Hacer ceros en el resto de la columna (arriba y abajo)
        for i in range(filas):
            if i != fila_actual:
                factor = M[i][j]
                if factor == 0:
                    continue
                for k in range(cols):
                    M[i][k] -= factor * M[fila_actual][k]
                registrar_paso(
                    f"Eliminar la entrada de F{i + 1}, columna {j + 1}: "
                    f"F{i + 1} <- F{i + 1} - ({factor})*F{fila_actual + 1}.",
                )
                    
        pivotes_encontrados += 1
        fila_actual += 1
        
    if devolver_pasos:
        return M, pivotes_encontrados, pasos
    return M, pivotes_encontrados


def invertir_matriz_a_string(matriz, formato="Decimales"):
    """Invierte una matriz cuadrada con Gauss-Jordan y expone la reducción."""
    if not isinstance(matriz, (list, tuple)) or not matriz:
        raise ValueError("La matriz debe ser cuadrada y no estar vacía.")
    orden = len(matriz)
    if any(not isinstance(fila, (list, tuple)) or len(fila) != orden for fila in matriz):
        raise ValueError("Solo las matrices cuadradas tienen inversa.")
    try:
        matriz_exacta = [
            [
                valor if isinstance(valor, Fraction) else Fraction(str(valor))
                for valor in fila
            ]
            for fila in matriz
        ]
    except (ValueError, TypeError, ZeroDivisionError) as error:
        raise ValueError("La matriz contiene valores no numéricos.") from error

    identidad = [
        [Fraction(int(fila == columna)) for columna in range(orden)]
        for fila in range(orden)
    ]
    aumentada = [
        fila[:] + identidad[indice][:]
        for indice, fila in enumerate(matriz_exacta)
    ]
    reducida, _, pasos = gauss_jordan(aumentada, devolver_pasos=True)
    izquierda = [fila[:orden] for fila in reducida]
    identidad_reducida = [
        [Fraction(int(fila == columna)) for columna in range(orden)]
        for fila in range(orden)
    ]
    if izquierda != identidad_reducida:
        raise ValueError("La matriz es singular y no posee inversa.")

    def formatear(valor):
        if formato == "Fracciones":
            return str(valor.numerator) if valor.denominator == 1 else str(valor)
        decimal = f"{float(valor):.6f}".rstrip("0").rstrip(".")
        return decimal if decimal not in ("-0", "") else "0"

    def matriz_a_string(valores):
        return "\n".join(
            "[ " + "   ".join(formatear(valor) for valor in fila) + " ]"
            for fila in valores
        )

    salida = [
        "INVERSA DE UNA MATRIZ POR GAUSS-JORDAN",
        "",
        "Matriz aumentada inicial [A | I]:",
        matriz_a_string(aumentada),
        "",
    ]
    for descripcion, matriz_paso in pasos[1:]:
        salida.extend([
            f">> {descripcion}",
            matriz_a_string(matriz_paso),
            "",
        ])

    inversa = [fila[orden:] for fila in reducida]
    salida.extend([
        "La reducción produjo [I | A⁻¹].",
        "",
        "MATRIZ INVERSA A⁻¹:",
        matriz_a_string(inversa),
    ])
    return "\n".join(salida)


def resolver_sistema(matriz_A, vector_b):
    """
    Resuelve el sistema Ax = b analizando la matriz aumentada.
    Retorna un texto formateado con el resultado para la consola.
    """
    filas = len(matriz_A)
    cols_A = len(matriz_A[0])
    
    # Construir matriz aumentada [A | b]
    matriz_aumentada = []
    for i in range(filas):
        fila = list(matriz_A[i]) + [vector_b[i]]
        matriz_aumentada.append(fila)
        
    M_reducida, pivotes_A = gauss_jordan(matriz_A)
    M_aum_reducida, pivotes_Aum = gauss_jordan(matriz_aumentada)
    
    # Análisis por Rouché-Capelli
    salida = ["--- ANÁLISIS DEL SISTEMA (Ax = b) ---", ""]
    
    if pivotes_A < pivotes_Aum:
        salida.append("Resultado: SISTEMA INCOMPATIBLE")
        salida.append("El sistema no tiene solución (las ecuaciones son contradictorias).")
    elif pivotes_A == cols_A:
        salida.append("Resultado: SISTEMA COMPATIBLE DETERMINADO")
        salida.append("El sistema tiene una SOLUCIÓN ÚNICA:")
        for i in range(cols_A):
            salida.append(f"x{i+1} = {M_aum_reducida[i][-1]}")
    else:
        salida.append("Resultado: SISTEMA COMPATIBLE INDETERMINADO")
        salida.append("El sistema tiene INFINITAS SOLUCIONES.")
        salida.append(f"Variables principales: {pivotes_A}")
        salida.append(f"Variables libres: {cols_A - pivotes_A}")
        
    return "\n".join(salida)


def resolver_sistema_cramer_a_string(matriz_A, vector_b, formato="Decimales"):
    """Resuelve un sistema cuadrado mediante la regla de Cramer."""
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

    determinante_principal = determinante_lu_valor(matriz)
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
        determinante_columna = determinante_lu_valor(matriz_cramer)
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
    """Resuelve Ax=b por LU, sustitución hacia adelante y hacia atrás."""
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


def evaluar_independencia(matriz_vectores):
    """
    Evalúa la independencia lineal de un conjunto de vectores (columnas).
    """
    filas = len(matriz_vectores)
    cols = len(matriz_vectores[0]) # Número de vectores
    
    M_reducida, pivotes = gauss_jordan(matriz_vectores)
    
    salida = ["--- ANÁLISIS DE INDEPENDENCIA LINEAL ---", ""]
    salida.append(f"Dimensión del espacio (filas): {filas}")
    salida.append(f"Cantidad de vectores analizados: {cols}")
    salida.append(f"Número de pivotes encontrados: {pivotes}")
    salida.append("")
    
    if pivotes == cols:
        salida.append("Resultado: Los vectores son LINEALMENTE INDEPENDIENTES.")
        salida.append("Ninguno de los vectores se puede escribir como combinación lineal de los demás.")
    else:
        salida.append("Resultado: Los vectores son LINEALMENTE DEPENDIENTES.")
        salida.append(f"Al menos {cols - pivotes} vector(es) es combinación lineal del resto.")
        
    return "\n".join(salida)