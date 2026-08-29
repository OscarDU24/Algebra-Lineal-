"""
Funciones para solicitar y validar los datos ingresados por el usuario
(número de ecuaciones, número de variables y la matriz aumentada Ab).
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
