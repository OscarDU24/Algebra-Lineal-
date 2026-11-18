from core.lineal.exactitud import es_cero, es_matriz_exacta

TOLERANCIA = 1e-9


def clasificar_sistema(matriz_resultado, columnas_pivote):
    filas = len(matriz_resultado)
    columnas = len(matriz_resultado[0])
    variables = columnas - 1
    rango = len(columnas_pivote)
    # Con fracciones exactas, un coeficiente es nulo solo si vale exactamente 0.
    exacta = es_matriz_exacta(matriz_resultado)

    # Inconsistente: existe una fila 0 0 ... 0 | k, con k != 0
    for i in range(filas):
        coeficientes_nulos = all(
            es_cero(matriz_resultado[i][j], exacta, TOLERANCIA) for j in range(variables)
        )
        termino_no_nulo = not es_cero(matriz_resultado[i][-1], exacta, TOLERANCIA)
        if coeficientes_nulos and termino_no_nulo:
            return "Sistema Inconsistente"

    if rango == variables:
        return "Sistema Consistente Determinado"
    return "Sistema Consistente Indeterminado"
