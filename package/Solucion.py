
def extraer_solucion(Ab, n):
    """
    Extrae el valor de cada variable directamente de la matriz reducida.
    Debe usarse solo cuando el sistema es Consistente Determinado
    (rango de A = n, con pivotes 1 en las columnas 0..n-1 y en orden).
    """
    x = [0.0] * n
    for i in range(n):
        x[i] = Ab[i][n]
    return x
