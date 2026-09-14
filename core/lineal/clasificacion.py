TOLERANCIA = 1e-9


def clasificar_sistema(matriz_resultado, columnas_pivote):
    filas = len(matriz_resultado)
    columnas = len(matriz_resultado[0])
    variables = columnas - 1
    rango = len(columnas_pivote)

    # Inconsistente: existe una fila 0 0 ... 0 | k, con k != 0
    for i in range(filas):
        coeficientes_nulos = all(abs(matriz_resultado[i][j]) < TOLERANCIA for j in range(variables))
        termino_no_nulo = abs(matriz_resultado[i][-1]) > TOLERANCIA
        if coeficientes_nulos and termino_no_nulo:
            return "Sistema Inconsistente"

    if rango == variables:
        return "Sistema Consistente Determinado"
    return "Sistema Consistente Indeterminado"
