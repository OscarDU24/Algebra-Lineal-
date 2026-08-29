
from sislineal import (
    leer_dimensiones,
    leer_metodo,
    construir_matriz_aumentada,
    imprimir_matriz,
    eliminacion_gauss_jordan,
    eliminacion_gauss,
    eliminacion_por_eliminacion,
    clasificar_sistema,
    sustitucion_hacia_atras,
    extraer_solucion_rref,
    verificar_solucion,
)

# Nombres descriptivos y funciones asociadas a cada método disponible.
METODOS = {
    "GAUSS_JORDAN": {
        "nombre": "Gauss-Jordan",
        "funcion": eliminacion_gauss_jordan,
        "usa_rref": True,
    },
    "GAUSS": {
        "nombre": "Gauss",
        "funcion": eliminacion_gauss,
        "usa_rref": False,
    },
    "ELIMINACION": {
        "nombre": "Eliminación (suma y resta de ecuaciones)",
        "funcion": eliminacion_por_eliminacion,
        "usa_rref": False,
    },
}


def main():
    print("=" * 60)
    print(" RESOLUCIÓN DE SISTEMAS DE ECUACIONES LINEALES Ax = b ")
    print("=" * 60)

    # --- 1. Entrada de datos ---
    m, n = leer_dimensiones()
    Ab = construir_matriz_aumentada(m, n)

    # Se guarda una copia del sistema original para la verificación posterior
    A_original = [fila[:n] for fila in Ab]
    b_original = [fila[n] for fila in Ab]

    imprimir_matriz(Ab, m, n, "Matriz aumentada inicial [A | b]:")

    # --- 2. Selección del método a utilizar ---
    clave_metodo = leer_metodo()
    metodo = METODOS[clave_metodo]

    # --- 3. Procesamiento: eliminación por filas según el método elegido ---
    print(f"\nResolviendo el sistema con el método: {metodo['nombre']}...")
    print("A continuación se muestra cada paso realizado.")
    Ab, columnas_pivote = metodo["funcion"](Ab, m, n)

    titulo_final = ("Matriz escalonada reducida final (RREF):" if metodo["usa_rref"]
                     else "Matriz escalonada final (REF):")
    imprimir_matriz(Ab, m, n, titulo_final)

    # --- 4. Clasificación del sistema ---
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

    # --- 5. Salida y verificación ---
    if clasificacion == "DETERMINADO":
        if metodo["usa_rref"]:
            x = extraer_solucion_rref(Ab, n)
        else:
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
