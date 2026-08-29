
def clasificar_sistema(Ab, m, n, columnas_pivote, tolerancia=1e-9):

    rango_A = len(columnas_pivote)

    # Se revisa si existe una fila del tipo 0 0 ... 0 | k, con k != 0
    for i in range(m):
        coeficientes_nulos = all(abs(Ab[i][j]) < tolerancia for j in range(n))
        termino_no_nulo = abs(Ab[i][n]) > tolerancia
        if coeficientes_nulos and termino_no_nulo:
            return "INCONSISTENTE"

    if rango_A == n:
        return "DETERMINADO"
    else:
        return "INDETERMINADO"
