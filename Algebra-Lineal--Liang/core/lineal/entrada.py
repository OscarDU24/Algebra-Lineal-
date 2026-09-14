
def leer_entero_positivo(mensaje):
    """Pide un numero entero estrictamente mayor que cero, validando la entrada."""
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if valor > 0:
                return valor
            print("Error: el valor debe ser un entero mayor que 0.")
        except ValueError:
            print("Error: debe ingresar un numero entero valido.")


def leer_flotante(mensaje):
    """Pide un numero real, aceptando enteros, decimales y negativos."""
    while True:
        entrada = input(mensaje).strip()
        try:
            return float(entrada)
        except ValueError:
            print("Error: debe ingresar un numero valido (ej. 5, -3.2, 0.25).")


def leer_dimensiones():
    """Solicita el numero de ecuaciones (m) y el numero de variables (n)."""
    print("\n--- 1. Dimensiones del sistema ---")
    m = leer_entero_positivo("Ingrese el numero de ecuaciones (m): ")
    n = leer_entero_positivo("Ingrese el numero de variables (n): ")
    return m, n


def construir_matriz_aumentada(m, n):
    """
    Solicita fila por fila los coeficientes de A y el termino independiente b,
    y arma la matriz aumentada Ab de tamano m x (n+1).
    """
    print("\n--- 2. Ingreso de coeficientes y terminos independientes ---")
    matriz = []
    for i in range(m):
        print(f"\nEcuacion {i + 1}:")
        fila = []
        for j in range(n):
            coef = leer_flotante(f"  Coeficiente de x{j + 1}: ")
            fila.append(coef)
        indep = leer_flotante(f"  Termino independiente b{i + 1}: ")
        fila.append(indep)
        matriz.append(fila)
    return matriz


def leer_metodo():
    """
    Muestra un menu y solicita al usuario el metodo de eliminacion
    por filas a utilizar. Devuelve "gauss" o "gauss_jordan".
    """
    print("\n" + "-" * 60)
    print("Seleccione el metodo de eliminacion por filas a utilizar:")
    print("  1. Gauss           (forma escalonada + sustitucion hacia atras)")
    print("  2. Gauss-Jordan    (forma escalonada reducida, solucion directa)")
    print("-" * 60)
    while True:
        opcion = input("Ingrese 1 o 2: ").strip()
        if opcion == "1":
            return "gauss"
        if opcion == "2":
            return "gauss_jordan"
        print("Opcion invalida. Intente de nuevo.")
