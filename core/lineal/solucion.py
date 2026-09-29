from fractions import Fraction

TOLERANCIA_INVERSA = 1e-10


def invertir_matriz_gauss_jordan(matriz):
    """Calcula la inversa de una matriz cuadrada mediante Gauss-Jordan."""
    if not matriz or any(len(fila) != len(matriz) for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada y no estar vacía.")

    dimension = len(matriz)
    aumentada = [
        list(fila) + [1.0 if fila_indice == columna else 0.0 for columna in range(dimension)]
        for fila_indice, fila in enumerate(matriz)
    ]

    for columna in range(dimension):
        fila_pivote = max(
            range(columna, dimension),
            key=lambda indice: abs(aumentada[indice][columna])
        )
        if abs(aumentada[fila_pivote][columna]) < TOLERANCIA_INVERSA:
            raise ValueError(
                "La matriz A no es invertible; no se puede calcular su inversa."
            )

        if fila_pivote != columna:
            aumentada[columna], aumentada[fila_pivote] = (
                aumentada[fila_pivote],
                aumentada[columna]
            )

        pivote = aumentada[columna][columna]
        aumentada[columna] = [valor / pivote for valor in aumentada[columna]]
        fila_pivote_normalizada = aumentada[columna][:]

        for indice_fila in range(dimension):
            if indice_fila == columna:
                continue
            factor = aumentada[indice_fila][columna]
            if abs(factor) < TOLERANCIA_INVERSA:
                aumentada[indice_fila][columna] = 0.0
                continue

            fila_actual = aumentada[indice_fila]
            fila_nueva = []
            for indice_elemento in range(len(fila_actual)):
                valor_nuevo = (
                    fila_actual[indice_elemento]
                    - factor * fila_pivote_normalizada[indice_elemento]
                )
                fila_nueva.append(valor_nuevo)
            aumentada[indice_fila] = fila_nueva

    return [fila[dimension:] for fila in aumentada]


def multiplicar_matriz_por_vector(matriz, vector):
    """Multiplica una matriz por un vector usando productos fila-columna."""
    if not matriz or any(len(fila) != len(vector) for fila in matriz):
        raise ValueError(
            "La cantidad de componentes del vector debe coincidir con las columnas de la matriz."
        )

    return [
        sum(valor * componente for valor, componente in zip(fila, vector))
        for fila in matriz
    ]


def resolver_sistema_por_inversa(matriz, vector_b):
    """Resuelve Ax=b calculando x=A^-1 b; requiere A cuadrada e invertible."""
    if len(matriz) != len(vector_b):
        raise ValueError("El vector b debe tener una componente por cada fila de A.")

    inversa = invertir_matriz_gauss_jordan(matriz)
    return multiplicar_matriz_por_vector(inversa, vector_b)


def enrutar_resolucion_matricial(
    matriz_A,
    vector_b=None,
    formato_fracciones=False,
    metodo="gauss_jordan"
):
    """Selecciona entre inversa de A (b=None) y resolución de Ax=b."""
    if vector_b is None:
        return {
            "modo": "matriz_pura",
            "matriz_inversa": invertir_matriz_gauss_jordan(matriz_A),
            "formato_fracciones": bool(formato_fracciones),
        }

    if not matriz_A or any(len(fila) != len(matriz_A[0]) for fila in matriz_A):
        raise ValueError("La matriz A debe ser rectangular y no estar vacía.")
    if len(matriz_A) != len(vector_b):
        raise ValueError("El vector b debe tener una componente por cada fila de A.")

    from core.lineal.clasificacion import clasificar_sistema
    from core.lineal.eliminacion import eliminacion_por_filas

    matriz_aumentada = [
        list(fila) + [vector_b[indice]]
        for indice, fila in enumerate(matriz_A)
    ]
    matriz_resultado, pasos, pivotes = eliminacion_por_filas(
        matriz_aumentada,
        modo=metodo
    )
    clasificacion = clasificar_sistema(matriz_resultado, pivotes)
    solucion = None
    pasos_despeje = []

    if clasificacion == "Sistema Consistente Determinado":
        cantidad_variables = len(matriz_A[0])
        if metodo == "gauss_jordan":
            solucion = extraer_solucion_rref(matriz_resultado, cantidad_variables)
        else:
            solucion, pasos_despeje = sustitucion_hacia_atras_detallada(
                matriz_resultado,
                cantidad_variables
            )

    return {
        "modo": "sistema",
        "matriz_aumentada": matriz_aumentada,
        "matriz_resultado": matriz_resultado,
        "pasos": pasos,
        "pivotes": pivotes,
        "clasificacion": clasificacion,
        "solucion": solucion,
        "pasos_despeje": pasos_despeje,
        "formato_fracciones": bool(formato_fracciones),
    }


def sustitucion_hacia_atras(matriz_ref, n):
    """Para el resultado de Gauss: despeja las variables de abajo hacia arriba."""
    is_fraction = any(isinstance(val, Fraction) for row in matriz_ref for val in row)
    
    x = [None] * n
    for i in range(n - 1, -1, -1):
        suma = matriz_ref[i][n]
        for j in range(i + 1, n):
            suma -= matriz_ref[i][j] * x[j]
        x[i] = suma / matriz_ref[i][i]
    return x


def sustitucion_hacia_atras_detallada(matriz_ref, n):
    """
    Resuelve el sistema por sustitución hacia atrás y genera una traza 
    explicativa del despeje paso a paso para la interfaz gráfica.
    Preserva fracciones exactas si la matriz contiene objetos Fraction.
    """
    is_fraction = any(isinstance(val, Fraction) for row in matriz_ref for val in row)
    
    x = [None] * n
    pasos_despeje = []
    
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

    for i in range(n - 1, -1, -1):
        pivote = matriz_ref[i][i]
        b_val = matriz_ref[i][n]
        
        # Iniciar la suma con el tipo correcto (Fraction o float)
        subst_suma = Fraction(0) if is_fraction else 0.0
        explicacion_subst = []
        
        for j in range(i + 1, n):
            coef = matriz_ref[i][j]
            term = coef * x[j]
            subst_suma += term
            
            is_zero = (coef == 0) if is_fraction else (abs(coef) <= 1e-9)
            if not is_zero:
                explicacion_subst.append(f"({format_val(coef)})*({format_val(x[j])})")
        
        x[i] = (b_val - subst_suma) / pivote
        
        str_despeje = f"Despejando x{i + 1} de la Ec. {i + 1}:\n"
        if explicacion_subst:
            subst_text = " + ".join(explicacion_subst)
            str_despeje += f"  {format_val(pivote)}*x{i + 1} + [{subst_text}] = {format_val(b_val)}\n"
        
        str_despeje += f"  x{i + 1} = ({format_val(b_val)} - ({format_val(subst_suma)})) / {format_val(pivote)} ==> x{i + 1} = {format_val(x[i])}"
        pasos_despeje.append(str_despeje)
        
    return x, pasos_despeje


def extraer_solucion_rref(matriz_rref, n):
    """Para el resultado de Gauss-Jordan: la solucion queda directa en la ultima columna."""
    return [matriz_rref[i][n] for i in range(n)]