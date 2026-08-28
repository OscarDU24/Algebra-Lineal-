"""
UNIVERSIDAD AMERICANA
Facultad de Ingeniería y Arquitectura (FIA)
Asignatura: Álgebra Lineal (MTM0120)
Proyecto Integrador: Calculadora de Álgebra Lineal (Programa 1)

Autores: Liang Li Zuñiga Woo, Oscar Issac Duran Guadron, Diego Alexander Gomez Solis, Carlos Daniel Aguirre Molina
Carrera: Ingeniería en Sistemas de Información
Docente: Carlos Ivan Arguello Martinez
"""

from logica_matematica import (
    eliminacion_gaussiana,
    clasificar_sistema,
    sustitucion_hacia_atras,
    verificar_solucion
)
from validaciones import pedir_dimensiones_sistema, pedir_matriz_aumentada

def mostrar_portada():
    """Despliega la portada requerida por las normas de la universidad."""
    print("=" * 65)
    print("           UNIVERSIDAD AMERICANA - FIA")
    print("       Asignatura: Álgebra Lineal (MTM0120)")
    print("    PROYECTO INTEGRADOR: CALCULADORA DE ÁLGEBRA LINEAL")
    print("        Programa 1: Eliminación por Filas (Gauss)")
    print("=" * 65)

def imprimir_matriz(matriz):
    """
    Imprime la matriz aumentada formateada con barras verticales separando 
    los coeficientes del término independiente.
    """
    filas = len(matriz)
    columnas = len(matriz[0])
    
    for i in range(filas):
        print("  | ", end="")
        for j in range(columnas - 1):
            # Imprime cada coeficiente alineado en 8 espacios con 3 decimales
            print(f"{matriz[i][j]:8.3f} ", end="")
        # Barra separadora de la matriz aumentada [A|b]
        print(f"| {matriz[i][-1]:8.3f} |")
    print()

def main():
    mostrar_portada()
    
    # 1. Entrada de datos
    m, n = pedir_dimensiones_sistema()
    matriz_original = pedir_matriz_aumentada(m, n)
    
    # 2. Procesamiento: Eliminación Gaussiana y registro de pasos
    print("\n" + "=" * 65)
    print("PROCESO DE ELIMINACIÓN POR FILAS (PASO A PASO)")
    print("=" * 65)
    
    matriz_escalonada, pasos = eliminacion_gaussiana(matriz_original)
    
    for descripcion, est_matriz in pasos:
        print(f"\n👉 {descripcion}:")
        imprimir_matriz(est_matriz)
        
    # 3. Clasificación del Sistema
    clasificacion = clasificar_sistema(matriz_escalonada)
    
    print("=" * 65)
    print(f"RESULTADO: {clasificacion.upper()}")
    print("=" * 65)
    
    # 4. Salida y Verificación
    if clasificacion == "Sistema Consistente Determinado":
        soluciones = sustitucion_hacia_atras(matriz_escalonada)
        
        print("\n--- Solución Única Encontrada ---")
        for i, val in enumerate(soluciones):
            print(f"  x{i + 1} = {val:.4f}")
            
        # Comprobación automática
        es_correcta = verificar_solucion(matriz_original, soluciones)
        print("\n--- Verificación Automática en el Sistema Original ---")
        if es_correcta:
            print("Comprobación Exitosa: Todos los valores satisfacen las ecuaciones originales.")
        else:
            print("Advertencia: Hubo una discrepancia al sustituir los valores.")

    elif clasificacion == "Sistema Consistente Indeterminado":
        print("\n  El sistema tiene infinitas soluciones (variables libres).")
        print("  No es posible despejar una solución numérica única.")
        
    elif clasificacion == "Sistema Inconsistente":
        print("\n  El sistema no tiene solución.")
        print("  Se detectó una contradicción matemática (ej. 0 = k, con k ≠ 0).")

if __name__ == "__main__":
    main()