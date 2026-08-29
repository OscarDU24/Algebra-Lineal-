
def sustitucion_hacia_atras(Ab, n):
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = Ab[i][n]
        for j in range(i + 1, n):
            suma -= Ab[i][j] * x[j]
        x[i] = suma / Ab[i][i]
    return x


def extraer_solucion_rref(Ab, n):
    x = [0.0] * n
    for i in range(n):
        x[i] = Ab[i][n]
    return x
