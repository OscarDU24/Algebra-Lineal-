# ============================================================
# OPERACIONES - SISTEMAS DE ECUACIONES E INDEPENDENCIA LINEAL
# ============================================================

from fractions import Fraction

def convertir_a_fraccion(valor):
    """Convierte una cadena o número a Fraction. Retorna None si hay error."""
    try:
        # Reemplazar comas por puntos por si el usuario escribe en formato latino
        if isinstance(valor, str):
            valor = valor.replace(',', '.')
        return Fraction(valor)
    except ValueError:
        return None

def gauss_jordan(matriz):
    """
    Aplica el método de Gauss-Jordan con pivoteo parcial a una matriz dada.
    Retorna la matriz escalonada reducida y el número de pivotes.
    """
    # Crear una copia profunda para no alterar la original
    M = [[matriz[i][j] for j in range(len(matriz[0]))] for i in range(len(matriz))]
    filas = len(M)
    cols = len(M[0])
    
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
            
        # 2. Hacer el pivote igual a 1
        pivote = M[fila_actual][j]
        for k in range(cols):
            M[fila_actual][k] /= pivote
            
        # 3. Hacer ceros en el resto de la columna (arriba y abajo)
        for i in range(filas):
            if i != fila_actual:
                factor = M[i][j]
                for k in range(cols):
                    M[i][k] -= factor * M[fila_actual][k]
                    
        pivotes_encontrados += 1
        fila_actual += 1
        
    return M, pivotes_encontrados

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