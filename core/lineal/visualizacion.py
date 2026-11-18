
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
            print(f"{fila[j]:9.2f} ", end="")
            print(f"| {fila[-1]:9.2f} |")


def imprimir_sistema_ecuaciones(matriz, formatear=None):
    """Genera una representación visual en texto del sistema de ecuaciones algebraicas.

    ``formatear`` convierte cada número en texto; por omisión usa dos decimales.
    Con fracciones exactas, un coeficiente se omite solo si vale exactamente 0.
    """
    from core.lineal.exactitud import es_cero, es_matriz_exacta

    if formatear is None:
        def formatear(valor):
            return f"{valor:.2f}"

    exacta = es_matriz_exacta(matriz)
    m = len(matriz)
    n = len(matriz[0]) - 1
    lineas = []
    for i in range(m):
        terminos = []
        for j in range(n):
            coef = matriz[i][j]
            if not es_cero(coef, exacta, 1e-9):
                signo = "+" if coef > 0 and terminos else ("-" if coef < 0 else "")
                val = abs(coef)
                str_coef = formatear(val) if val != 1 else ""
                terminos.append(f"{signo} {str_coef}x{j+1}".strip())
        eq_str = " ".join(terminos) if terminos else "0"
        lineas.append(f"{eq_str} = {formatear(matriz[i][-1])}")
    return "\n".join(lineas)