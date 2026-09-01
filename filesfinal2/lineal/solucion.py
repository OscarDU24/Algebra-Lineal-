
def sustitucion_hacia_atras(matriz_ref, n):
    """Para el resultado de Gauss: despeja las variables de abajo hacia arriba."""
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = matriz_ref[i][n]
        for j in range(i + 1, n):
            suma -= matriz_ref[i][j] * x[j]
        x[i] = suma / matriz_ref[i][i]
    return x


def sustitucion_hacia_atras_detallada(matriz_ref, n):
    """
    Resuelve el sistema por sustitución hacia atrás y genera una traza 
    textual explicativa del despeje paso a paso para la interfaz gráfica.
    """
    x = [0.0] * n
    pasos_despeje = []
    
    for i in range(n - 1, -1, -1):
        pivote = matriz_ref[i][i]
        b_val = matriz_ref[i][n]
        
        suma = 0.0
        explicacion_subst = []
        
        for j in range(i + 1, n):
            coef = matriz_ref[i][j]
            suma += coef * x[j]
            if abs(coef) > 1e-9:
                explicacion_subst.append(f"({coef:.4f})*({x[j]:.4f})")
        
        x[i] = (b_val - suma) / pivote
        
        str_despeje = f"Despejando x{i + 1} de la Ec. {i + 1}:\n"
        if explicacion_subst:
            subst_text = " + ".join(explicacion_subst)
            str_despeje += f"  {pivote:.4f}*x{i + 1} + [{subst_text}] = {b_val:.4f}\n"
        
        str_despeje += f"  x{i + 1} = ({b_val:.4f} - ({suma:.4f})) / {pivote:.4f} ==> x{i + 1} = {x[i]:.6f}"
        pasos_despeje.append(str_despeje)
        
    return x, pasos_despeje


def extraer_solucion_rref(matriz_rref, n):
    """Para el resultado de Gauss-Jordan: la solucion queda directa en la ultima columna."""
    return [matriz_rref[i][n] for i in range(n)]