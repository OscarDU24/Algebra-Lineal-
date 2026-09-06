
from lineal import (
    leer_dimensiones,
    construir_matriz_aumentada,
    leer_metodo,
    imprimir_matriz,
    eliminacion_por_filas,
    clasificar_sistema,
    sustitucion_hacia_atras,
    extraer_solucion_rref,
    verificar_solucion,
)


def mostrar_portada():
    print("=" * 65)
    print("      UNIVERSIDAD AMERICANA - FIA - ALGEBRA LINEAL")
    print("   CALCULADORA DE SISTEMAS DE ECUACIONES LINEALES")
    print("        Metodo: Gauss o Gauss-Jordan")
    print("=" * 65)


def resolver_un_sistema():
    # --- 1. Entrada de datos ---
    m, n = leer_dimensiones()
    matriz_original = construir_matriz_aumentada(m, n)
    modo = leer_metodo()

    imprimir_matriz(matriz_original, "\nMatriz aumentada inicial [A | b]:")

    # --- 2. Procesamiento: eliminacion por filas, paso a paso ---
    print("\n" + "=" * 65)
    print("PROCESO DE ELIMINACION POR FILAS")
    print("=" * 65)
    matriz_resultado, pasos, columnas_pivote = eliminacion_por_filas(matriz_original, modo)
    for descripcion, matriz_paso in pasos[1:]:
        imprimir_matriz(matriz_paso, f"\n>> {descripcion}:")

    titulo_final = "Matriz escalonada reducida:" if modo == "gauss_jordan" else "Matriz escalonada:"
    imprimir_matriz(matriz_resultado, f"\n{titulo_final}")

    # --- 3. Clasificacion del sistema ---
    clasificacion = clasificar_sistema(matriz_resultado, columnas_pivote)
    print("\n" + "=" * 65)
    print(f"RESULTADO: {clasificacion.upper()}")
    print("=" * 65)

    # --- 4. Solucion y verificacion ---
    if clasificacion == "Sistema Consistente Determinado":
        if modo == "gauss_jordan":
            x = extraer_solucion_rref(matriz_resultado, n)
        else:
            x = sustitucion_hacia_atras(matriz_resultado, n)

        print("\n--- Solucion unica ---")
        for i in range(n):
            print(f"  x{i + 1} = {x[i]:.6f}")

        es_correcta = verificar_solucion(matriz_original, x)
        print("\n--- Verificacion en el sistema original ---")
        if es_correcta:
            print("Comprobacion exitosa: la solucion satisface todas las ecuaciones.")
        else:
            print("Advertencia: la solucion no pudo ser verificada correctamente.")

    elif clasificacion == "Sistema Consistente Indeterminado":
        print("\nEl sistema tiene infinitas soluciones (existen variables libres).")
        print(f"Variables con pivote (dependientes): {[f'x{c + 1}' for c in columnas_pivote]}")

    else:  # Sistema Inconsistente
        print("\nEl sistema no tiene solucion.")
        print("Se detecto una contradiccion del tipo 0 = k, con k distinto de cero.")


def main():
    mostrar_portada()
    while True:
        resolver_un_sistema()
        print("\n" + "-" * 65)
        de_nuevo = input("Desea resolver otro sistema? (s/n): ").strip().lower()
        if de_nuevo != "s":
            print("\nFin del programa.")
            break


if __name__ == "__main__":
    main()
