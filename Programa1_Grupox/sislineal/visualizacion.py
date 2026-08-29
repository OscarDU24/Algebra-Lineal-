
def imprimir_matriz(Ab, m, n, titulo=""):
    """Imprime en pantalla la matriz aumentada Ab con formato alineado."""
    if titulo:
        print(f"\n{titulo}")
    for i in range(m):
        fila_texto = []
        for j in range(n):
            fila_texto.append(f"{Ab[i][j]:8.3f}")
        fila_texto.append("|")
        fila_texto.append(f"{Ab[i][n]:8.3f}")
        print("  ".join(fila_texto))
    print()


def copiar_matriz(Ab):
    """Devuelve una copia profunda (independiente) de la matriz Ab."""
    return [fila[:] for fila in Ab]
