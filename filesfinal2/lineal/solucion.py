
def sustitucion_hacia_atras(matriz_ref, n):
    """Para el resultado de Gauss: despeja las variables de abajo hacia arriba."""
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = matriz_ref[i][n]
        for j in range(i + 1, n):
            suma -= matriz_ref[i][j] * x[j]
        x[i] = suma / matriz_ref[i][i]
    return x


def extraer_solucion_rref(matriz_rref, n):
    """Para el resultado de Gauss-Jordan: la solucion queda directa en la ultima columna."""
    return [matriz_rref[i][n] for i in range(n)]
