
def copiar_matriz(matriz):
    """Devuelve una copia independiente (profunda) de la matriz."""
    return [fila[:] for fila in matriz]


def imprimir_matriz(matriz, titulo=""):
    """Imprime la matriz aumentada [A|b] con una barra separando A de b."""
    if titulo:
        print(f"\n{titulo}")
    columnas = len(matriz[0])
    for fila in matriz:
        print("  | ", end="")
        for j in range(columnas - 1):
            print(f"{fila[j]:9.4f} ", end="")
        print(f"| {fila[-1]:9.4f} |")
