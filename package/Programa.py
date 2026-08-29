# ============================================================
# BLOQUE 1: FUNCIONES AUXILIARES DE ENTRADA Y VISUALIZACIÓN
# ============================================================

def leer_entero(mensaje):
    """Solicita al usuario un número entero, validando que sea correcto."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor <= 0:
                print("El valor debe ser un entero positivo. Intente de nuevo.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Debe ingresar un número entero.")


def leer_flotante(mensaje):
    """Solicita al usuario un número real (float), validando el formato."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Entrada inválida. Debe ingresar un número (ej: 2, -3.5, 0.25).")


def construir_matriz_aumentada(m, n):
    """
    Solicita al usuario, fila por fila, los coeficientes de A y el término
    independiente b, y arma la matriz aumentada Ab de tamaño m x (n+1).
    """
    Ab = []
    print("\nIngrese los coeficientes de cada ecuación (fila) y su término independiente b.")
    for i in range(m):
        print(f"\n--- Ecuación {i + 1} ---")
        fila = []
        for j in range(n):
            coef = leer_flotante(f"  Coeficiente de x{j + 1} (fila {i + 1}): ")
            fila.append(coef)
        b_i = leer_flotante(f"  Término independiente b{i + 1}: ")
        fila.append(b_i)
        Ab.append(fila)
    return Ab


def imprimir_matriz(Ab, m, n, titulo=""):
    """Imprime en pantalla la matriz aumentada Ab con formato alineado."""
    if titulo:
        print(f"\n{titulo}")
    for i in range(m):
        fila_texto = []
        for j in range(n):
            fila_texto.append(f"{Ab[i][j]:8.3f}")
        # separador visual entre A y b
        fila_texto.append("|")
        fila_texto.append(f"{Ab[i][n]:8.3f}")
        print("  ".join(fila_texto))
    print()


def copiar_matriz(Ab):
    """Devuelve una copia profunda (independiente) de la matriz Ab."""
    return [fila[:] for fila in Ab]


# ============================================================
# BLOQUE 2: ALGORITMO DE ELIMINACIÓN POR FILAS (GAUSS)
# ============================================================

def eliminacion_gaussiana(Ab, m, n, tolerancia=1e-9):
    """
    Aplica eliminación por filas (Gauss con pivoteo parcial) sobre la matriz
    aumentada Ab (m x n+1), llevándola a una forma escalonada por filas.
    Imprime la matriz después de cada paso representativo (cada pivote).
    Retorna: la matriz escalonada y la lista de columnas pivote encontradas.
    """
    fila_pivote = 0
    columnas_pivote = []
    paso = 1

    for col in range(n):
        if fila_pivote >= m:
            break

        # --- Búsqueda del mejor pivote (mayor valor absoluto) en la columna ---
        fila_max = fila_pivote
        for r in range(fila_pivote + 1, m):
            if abs(Ab[r][col]) > abs(Ab[fila_max][col]):
                fila_max = r

        # Si el pivote es prácticamente cero, esta columna no tiene pivote
        # (variable libre); se pasa a la siguiente columna.
        if abs(Ab[fila_max][col]) < tolerancia:
            continue

        # --- Intercambio de filas si es necesario ---
        if fila_max != fila_pivote:
            Ab[fila_pivote], Ab[fila_max] = Ab[fila_max], Ab[fila_pivote]

        # --- Eliminación de los elementos debajo del pivote ---
        for r in range(fila_pivote + 1, m):
            if abs(Ab[r][col]) > tolerancia:
                factor = Ab[r][col] / Ab[fila_pivote][col]
                for c in range(col, n + 1):
                    Ab[r][c] -= factor * Ab[fila_pivote][c]

        columnas_pivote.append(col)
        imprimir_matriz(Ab, m, n, f"Paso {paso}: pivote en columna x{col + 1} (fila {fila_pivote + 1})")
        paso += 1
        fila_pivote += 1

    return Ab, columnas_pivote


# ============================================================
# BLOQUE 3: CLASIFICACIÓN DEL SISTEMA
# ============================================================

def clasificar_sistema(Ab, m, n, columnas_pivote, tolerancia=1e-9):
    """
    Evalúa la matriz escalonada y determina si el sistema es:
      - Consistente Determinado (solución única)
      - Consistente Indeterminado (infinitas soluciones)
      - Inconsistente (sin solución)
    Retorna una cadena con la clasificación.
    """
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


# ============================================================
# BLOQUE 4: SOLUCIÓN DEL SISTEMA (SUSTITUCIÓN HACIA ATRÁS)
# ============================================================

def sustitucion_hacia_atras(Ab, n):
    """
    Calcula el valor de cada variable mediante sustitución hacia atrás.
    Solo debe usarse cuando el sistema es Consistente Determinado
    (rango de A = n, filas pivote ordenadas en las primeras n filas
    y en las columnas 0..n-1).
    """
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = Ab[i][n]
        for j in range(i + 1, n):
            suma -= Ab[i][j] * x[j]
        x[i] = suma / Ab[i][i]
    return x


# ============================================================
# BLOQUE 5: VERIFICACIÓN DE LA SOLUCIÓN
# ============================================================

def verificar_solucion(A_original, b_original, x, m, n, tolerancia=1e-6):
    """
    Sustituye los valores de x en el sistema ORIGINAL (antes de la
    eliminación) y comprueba que A*x sea igual a b, mostrando cada
    ecuación evaluada.
    """
    print("\n--- Verificación de la solución (sustitución en el sistema original) ---")
    todo_correcto = True
    for i in range(m):
        suma = 0.0
        terminos = []
        for j in range(n):
            suma += A_original[i][j] * x[j]
            terminos.append(f"({A_original[i][j]:.3f})({x[j]:.3f})")
        diferencia = abs(suma - b_original[i])
        correcto = diferencia < tolerancia
        todo_correcto = todo_correcto and correcto
        estado = "OK" if correcto else "ERROR"
        print(f"Ecuación {i + 1}: {' + '.join(terminos)} = {suma:.3f}  "
              f"(esperado {b_original[i]:.3f}) -> {estado}")
    if todo_correcto:
        print("\nLa solución satisface todas las ecuaciones del sistema original.")
    else:
        print("\nAdvertencia: existen diferencias numéricas al verificar la solución.")


# ============================================================
# BLOQUE 6: PROGRAMA PRINCIPAL
# ============================================================

def main():
    print("=" * 60)
    print(" RESOLUCIÓN DE SISTEMAS DE ECUACIONES LINEALES Ax = b ")
    print(" Método de Eliminación por Filas (Gauss)              ")
    print("=" * 60)

    # --- 1. Entrada de datos ---
    m = leer_entero("\nIngrese el número de ecuaciones (m): ")
    n = leer_entero("Ingrese el número de variables (n): ")

    Ab = construir_matriz_aumentada(m, n)

    # Se guarda una copia del sistema original para la verificación posterior
    A_original = [fila[:n] for fila in Ab]
    b_original = [fila[n] for fila in Ab]

    imprimir_matriz(Ab, m, n, "Matriz aumentada inicial [A | b]:")

    # --- 2. Procesamiento: eliminación por filas ---
    print("Iniciando proceso de eliminación por filas...")
    Ab, columnas_pivote = eliminacion_gaussiana(Ab, m, n)

    imprimir_matriz(Ab, m, n, "Matriz escalonada final:")

    # --- 3. Clasificación del sistema ---
    clasificacion = clasificar_sistema(Ab, m, n, columnas_pivote)

    print("=" * 60)
    if clasificacion == "INCONSISTENTE":
        print("CLASIFICACIÓN: Sistema Inconsistente -> Sin Solución")
        print("(Se encontró una fila de la forma 0 0 ... 0 | k, con k != 0)")
    elif clasificacion == "DETERMINADO":
        print("CLASIFICACIÓN: Sistema Consistente Determinado -> Solución Única")
    else:
        print("CLASIFICACIÓN: Sistema Consistente Indeterminado -> Infinitas Soluciones")
    print("=" * 60)

    # --- 4. Salida y verificación ---
    if clasificacion == "DETERMINADO":
        x = sustitucion_hacia_atras(Ab, n)
        print("\nValores de las variables:")
        for i in range(n):
            print(f"  x{i + 1} = {x[i]:.4f}")

        verificar_solucion(A_original, b_original, x, m, n)

    elif clasificacion == "INDETERMINADO":
        print("\nEl sistema tiene infinitas soluciones; no se despliega un valor")
        print("numérico único por variable. Las variables asociadas a columnas")
        print("sin pivote son libres y pueden tomar cualquier valor real.")
        print(f"Columnas con pivote (variables dependientes): "
              f"{[f'x{c + 1}' for c in columnas_pivote]}")

    else:  # INCONSISTENTE
        print("\nEl sistema no tiene solución; no es posible calcular valores")
        print("numéricos para las variables ni realizar la verificación.")

    print("\nFin del programa.")


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================
if __name__ == "__main__":
    main()
