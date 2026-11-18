
from core.lineal.exactitud import es_cero, es_matriz_exacta


def verificar_solucion(matriz_original, solucion, tolerancia_verificacion=1e-5):
    filas = len(matriz_original)
    variables = len(solucion)
    # Con datos exactos la comprobación es una igualdad; con floats, aproximada.
    exacta = es_matriz_exacta(matriz_original) and es_matriz_exacta([solucion])
    for i in range(filas):
        suma = 0
        for j in range(variables):
            suma += matriz_original[i][j] * solucion[j]
        independiente = matriz_original[i][-1]
        if not es_cero(suma - independiente, exacta, tolerancia_verificacion):
            return False
    return True
