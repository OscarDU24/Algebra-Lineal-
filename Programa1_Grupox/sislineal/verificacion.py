
def verificar_solucion(A_original, b_original, x, m, n, tolerancia=1e-6):
    
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
