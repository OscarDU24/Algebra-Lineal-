# resolucion.py
from entradas import imprimir_matriz_aumentada

def eliminacion_gaussiana(matriz_orig, m, n):
    """Aplica eliminación por filas ordenada sobre la matriz aumentada [A|b]."""
    matriz = [fila[:] for fila in matriz_orig]
    
    print("\n--- MATRIZ AUMENTADA INICIAL [A|b] ---")
    imprimir_matriz_aumentada(matriz, m, n)

    fila_pivote = 0
    tol = 1e-9  

    for col in range(n):
        if fila_pivote >= m:
            break

        max_fila = fila_pivote
        for i in range(fila_pivote + 1, m):
            if abs(matriz[i][col]) > abs(matriz[max_fila][col]):
                max_fila = i

        if abs(matriz[max_fila][col]) < tol:
            continue

        if max_fila != fila_pivote:
            matriz[fila_pivote], matriz[max_fila] = matriz[max_fila], matriz[fila_pivote]
            print(f"Paso: Intercambiar Fila {fila_pivote + 1} con Fila {max_fila + 1}")
            imprimir_matriz_aumentada(matriz, m, n)

        pivote = matriz[fila_pivote][col]
        matriz[fila_pivote] = [elem / pivote for elem in matriz[fila_pivote]]
        print(f"Paso: Normalizar Fila {fila_pivote + 1} (Dividir entre {pivote:.3f})")
        imprimir_matriz_aumentada(matriz, m, n)

        hizo_cambios = False
        for i in range(m):
            if i != fila_pivote and abs(matriz[i][col]) > tol:
                factor = matriz[i][col]
                matriz[i] = [matriz[i][j] - factor * matriz[fila_pivote][j] for j in range(n + 1)]
                hizo_cambios = True

        if hizo_cambios:
            print(f"Paso: Eliminación de la columna {col + 1}")
            imprimir_matriz_aumentada(matriz, m, n)

        fila_pivote += 1

    for i in range(m):
        for j in range(n + 1):
            if abs(matriz[i][j]) < tol:
                matriz[i][j] = 0.0

    return clasificar_sistema(matriz, m, n)

def clasificar_sistema(matriz, m, n):
    """Sub-función para evaluar y clasificar la matriz resultante."""
    tol = 1e-9
    inconsistente = False
    filas_no_cero = 0

    for i in range(m):
        es_fila_cero_A = all(abs(matriz[i][j]) < tol for j in range(n))
        b_cero = abs(matriz[i][n]) < tol

        if es_fila_cero_A and not b_cero:
            inconsistente = True
            break
        elif not es_fila_cero_A:
            filas_no_cero += 1

    print("-" * 60)
    print("CLASIFICACIÓN DEL SISTEMA:")
    print("-" * 60)

    if inconsistente:
        print("-> Sistema Inconsistente: Sin Solución.\n")
        return None, "Inconsistente"
    elif filas_no_cero < n:
        print("-> Sistema Consistente Indeterminado: Presenta Infinitas Soluciones.\n")
        return None, "Indeterminado"
    else:
        print("-> Sistema Consistente Determinado: Presenta Solución Única.\n")
        solucion = [matriz[i][n] for i in range(n)]
        return solucion, "Determinado"

def verificar_solucion(matriz_original, solucion, m, n):
    """Comprueba automáticamente la solución obtenida."""
    print("=" * 60)
    print("VERIFICACIÓN AUTOMÁTICA DE LA SOLUCIÓN")
    print("=" * 60)
    tol = 1e-6
    todas_correctas = True

    for i in range(m):
        suma_lhs = sum(matriz_original[i][j] * solucion[j] for j in range(n))
        b_esperado = matriz_original[i][n]
        cumple = abs(suma_lhs - b_esperado) < tol

        print(f"Ecuación {i + 1}:")
        print(f"  Calculado: {suma_lhs:.3f} | Esperado: {b_esperado:.3f} | Estado: {'✓' if cumple else '✗'}\n")
        if not cumple: todas_correctas = False

    if todas_correctas:
        print(">> ÉXITO: Todos los valores satisfacen el sistema original.\n")