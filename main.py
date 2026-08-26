# ==============================================================================
# MÓDULO PRINCIPAL (main.py)
# Propósito: Orquestar la ejecución del programa llamando a los otros módulos.
# ==============================================================================

# ---------------------------------------------------------
# BLOQUE 1: IMPORTACIÓN DE MÓDULOS
# ---------------------------------------------------------
import entradas as ent
import resolucion as res

def main():
    # ---------------------------------------------------------
    # BLOQUE 2: MENÚ DE INICIO Y CAPTURA DE DIMENSIONES
    # ---------------------------------------------------------
    print("=" * 60)
    print(" RESOLUCIÓN Y CLASIFICACIÓN DE SISTEMAS DE ECUACIONES (Ax=b)")
    print("=" * 60 + "\n")

    m = ent.leer_entero_positivo("Ingrese el número de ecuaciones (m): ")
    n = ent.leer_entero_positivo("Ingrese el número de variables (n): ")

    # ---------------------------------------------------------
    # BLOQUE 3: CAPTURA DE LA MATRIZ AUMENTADA
    # ---------------------------------------------------------
    matriz_aumentada = []
    print("\n--- INGRESO DE COEFICIENTES DE LA MATRIZ AUMENTADA [A|b] ---")
    
    for i in range(m):
        print(f"\n--- Ecuación {i + 1} ---")
        fila = []
        for j in range(n):
            fila.append(ent.leer_flotante_seguro(f"Ingrese coeficiente A[{i+1},{j+1}]: "))
        fila.append(ent.leer_flotante_seguro(f"Ingrese término independiente b[{i+1}]: "))
        matriz_aumentada.append(fila)

    # ---------------------------------------------------------
    # BLOQUE 4: PROCESAMIENTO MATEMÁTICO (CORE)
    # ---------------------------------------------------------
    solucion, tipo_sistema = res.eliminacion_gaussiana(matriz_aumentada, m, n)

    # ---------------------------------------------------------
    # BLOQUE 5: PRESENTACIÓN Y VERIFICACIÓN DE RESULTADOS
    # ---------------------------------------------------------
    if tipo_sistema == "Determinado" and solucion is not None:
        print("VALOR NUMÉRICO DE LAS VARIABLES HALLADAS:")
        print("-" * 40)
        for j in range(n):
            print(f"  x_{j + 1} = {solucion[j]:.4f}")
        print("-" * 40 + "\n")

        res.verificar_solucion(matriz_aumentada, solucion, m, n)

# ---------------------------------------------------------
# BLOQUE 6: PUNTO DE ENTRADA 
# ---------------------------------------------------------
if __name__ == "__main__":
    main()