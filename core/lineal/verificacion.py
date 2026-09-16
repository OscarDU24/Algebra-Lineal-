
def verificar_solucion(matriz_original, solucion, tolerancia_verificacion=1e-5):
    filas = len(matriz_original)
    variables = len(solucion)
    for i in range(filas):
        suma = 0.0
        for j in range(variables):
            suma += matriz_original[i][j] * solucion[j]
        independiente = matriz_original[i][-1]
        if abs(suma - independiente) > tolerancia_verificacion:
            return False
    return True
