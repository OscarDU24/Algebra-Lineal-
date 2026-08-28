"""
UNIVERSIDAD AMERICANA
Facultad de Ingeniería y Arquitectura (FIA)
Proyecto Integrador: Calculadora de Álgebra Lineal
Módulo: Lógica Matemática (Modelo)
Descripción: Contiene los algoritmos de Eliminación Gaussiana, sustitución hacia atrás,
clasificación de sistemas y verificación. Sin interacciones de consola.
"""

# Tolerancia para evitar errores de precisión de punto flotante
TOLERANCIA = 1e-9

def copiar_matriz(matriz):
    """Crea una copia profunda de la matriz para no alterar la original."""
    return [fila[:] for fila in matriz]

def eliminacion_gaussiana(matriz_original):
    """
    Realiza el método de Eliminación por Filas (Gauss Clásico) haciendo
    ceros solo debajo del pivote.
    Retorna la matriz escalonada y una lista con el registro de los pasos.
    """
    matriz = copiar_matriz(matriz_original)
    filas = len(matriz)
    columnas = len(matriz[0])
    pasos = [] # Aquí guardaremos la "historia" de los cálculos

    pasos.append(("Matriz inicial", copiar_matriz(matriz)))

    # Recorremos las columnas para pivotear
    for i in range(min(filas, columnas - 1)):
        # 1. Pivoteo Parcial (buscar el mayor valor absoluto en la columna)
        fila_max = i
        for k in range(i + 1, filas):
            if abs(matriz[k][i]) > abs(matriz[fila_max][i]):
                fila_max = k

        # Si el pivote máximo es prácticamente 0, pasamos a la siguiente columna
        if abs(matriz[fila_max][i]) < TOLERANCIA:
            continue

        # Intercambiar filas si es necesario
        if i != fila_max:
            matriz[i], matriz[fila_max] = matriz[fila_max], matriz[i]
            pasos.append((f"Intercambio de Fila {i+1} con Fila {fila_max+1}", copiar_matriz(matriz)))

        # 2. Hacer el pivote igual a 1 (simplifica los cálculos)
        pivote = matriz[i][i]
        for j in range(i, columnas):
            matriz[i][j] /= pivote
        pasos.append((f"Fila {i+1} dividida entre {pivote:.4g} (Pivote = 1)", copiar_matriz(matriz)))

        # 3. Hacer ceros DEBAJO del pivote (Gauss)
        for k in range(i + 1, filas):
            factor = matriz[k][i]
            if abs(factor) > TOLERANCIA:
                for j in range(i, columnas):
                    matriz[k][j] -= factor * matriz[i][j]
                pasos.append((f"Fila {k+1} - ({factor:.4g}) * Fila {i+1}", copiar_matriz(matriz)))

    return matriz, pasos

def clasificar_sistema(matriz_escalonada):
    """
    Evalúa la matriz escalonada para determinar el tipo de sistema.
    Retorna un string con la clasificación.
    """
    filas = len(matriz_escalonada)
    columnas = len(matriz_escalonada[0])
    incognitas = columnas - 1

    # Revisar si hay Inconsistencias (Fila de ceros igualada a una constante distinta de cero)
    for i in range(filas):
        todo_cero = all(abs(matriz_escalonada[i][j]) < TOLERANCIA for j in range(incognitas))
        termino_indep_no_cero = abs(matriz_escalonada[i][-1]) > TOLERANCIA
        if todo_cero and termino_indep_no_cero:
            return "Sistema Inconsistente"

    # Contar filas no nulas (para comparar el rango con el número de variables)
    filas_no_nulas = 0
    for i in range(filas):
        if not all(abs(matriz_escalonada[i][j]) < TOLERANCIA for j in range(columnas)):
            filas_no_nulas += 1

    if filas_no_nulas < incognitas:
        return "Sistema Consistente Indeterminado"
    else:
        return "Sistema Consistente Determinado"

def sustitucion_hacia_atras(matriz_escalonada):
    """
    Resuelve un Sistema Consistente Determinado.
    Empieza desde la última variable y va sustituyendo hacia arriba.
    Retorna una lista con los valores de las incógnitas.
    """
    filas = len(matriz_escalonada)
    columnas = len(matriz_escalonada[0])
    incognitas = columnas - 1
    soluciones = [0.0] * incognitas

    # Recorrer de abajo hacia arriba (desde la última variable hasta la primera)
    for i in range(incognitas - 1, -1, -1):
        suma = 0.0
        # Sumar los productos de las variables ya conocidas por sus coeficientes
        for j in range(i + 1, incognitas):
            suma += matriz_escalonada[i][j] * soluciones[j]
        
        # Despejar la variable actual (nota: no dividimos porque el pivote ya es 1)
        soluciones[i] = matriz_escalonada[i][-1] - suma

    return soluciones

def verificar_solucion(matriz_original, soluciones):
    """
    Sustituye los valores de las variables en el sistema original.
    Retorna True si todas las ecuaciones se cumplen, False de lo contrario.
    """
    if not soluciones:
        return False

    filas = len(matriz_original)
    incognitas = len(soluciones)
    # Tolerancia ligeramente mayor por acumulación de redondeos al sustituir
    tolerancia_comprobacion = 1e-5 

    for i in range(filas):
        suma = 0.0
        for j in range(incognitas):
            suma += matriz_original[i][j] * soluciones[j]
        
        termino_independiente = matriz_original[i][-1]
        
        if abs(suma - termino_independiente) > tolerancia_comprobacion:
            return False # Falló en al menos una ecuación
            
    return True