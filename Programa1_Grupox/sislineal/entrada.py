"""
Submódulo: sislineal.entrada
Funciones para solicitar y validar los datos ingresados por el usuario:
número de ecuaciones (m), número de variables (n) y la matriz aumentada
Ab de tamaño m x (n+1). El sistema puede ser cuadrado (m == n),
sobredeterminado (m > n) o subdeterminado (m < n); el método de
Gauss-Jordan implementado en este paquete funciona para los tres casos.
"""


def leer_entero(mensaje):
    """Solicita al usuario un número entero positivo, validando la entrada."""
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


def leer_dimensiones():
    """
    Solicita el número de ecuaciones (m) y el número de variables (n).
    No se exige que la matriz sea cuadrada: el sistema puede tener más
    ecuaciones que variables, más variables que ecuaciones, o la misma
    cantidad de ambas; en cualquier caso el método elegido y la
    clasificación posterior determinan el tipo de sistema.
    """
    m = leer_entero("\nIngrese el número de ecuaciones (m): ")
    n = leer_entero("Ingrese el número de variables (n): ")
    return m, n


def leer_metodo():
    """
    Muestra un menú y solicita al usuario el método con el que desea
    resolver el sistema de ecuaciones. Devuelve una cadena:
    "GAUSS_JORDAN", "GAUSS" o "ELIMINACION".
    """
    opciones = {
        "1": "GAUSS_JORDAN",
        "2": "GAUSS",
        "3": "ELIMINACION",
    }

    print("\n" + "-" * 60)
    print("Seleccione el método con el que desea resolver el sistema:")
    print("  1. Gauss-Jordan   (forma escalonada REDUCIDA por filas)")
    print("  2. Gauss          (forma escalonada + sustitución hacia atrás)")
    print("  3. Eliminación    (suma y resta de ecuaciones)")
    print("-" * 60)

    while True:
        opcion = input("Ingrese el número de la opción (1, 2 o 3): ").strip()
        if opcion in opciones:
            return opciones[opcion]
        print("Opción inválida. Debe ingresar 1, 2 o 3. Intente de nuevo.")


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
