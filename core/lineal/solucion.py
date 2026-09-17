from fractions import Fraction

def sustitucion_hacia_atras(matriz_ref, n):
    """Para el resultado de Gauss: despeja las variables de abajo hacia arriba."""
    is_fraction = any(isinstance(val, Fraction) for row in matriz_ref for val in row)
    
    x = [None] * n
    for i in range(n - 1, -1, -1):
        suma = matriz_ref[i][n]
        for j in range(i + 1, n):
            suma -= matriz_ref[i][j] * x[j]
        x[i] = suma / matriz_ref[i][i]
    return x


def sustitucion_hacia_atras_detallada(matriz_ref, n):
    """
    Resuelve el sistema por sustitución hacia atrás y genera una traza 
    explicativa del despeje paso a paso para la interfaz gráfica.
    Preserva fracciones exactas si la matriz contiene objetos Fraction.
    """
    is_fraction = any(isinstance(val, Fraction) for row in matriz_ref for val in row)
    
    x = [None] * n
    pasos_despeje = []
    
    def format_val(val):
        """Función auxiliar para formatear fracciones o decimales limpiamente."""
        if isinstance(val, Fraction):
            if val.denominator == 1:
                return str(val.numerator)
            return f"{val.numerator}/{val.denominator}"
        else:
            if isinstance(val, float) and abs(val - round(val)) < 1e-9:
                return str(int(round(val)))
            s = f"{val:.2f}"
            if "." in s:
                s = s.rstrip("0").rstrip(".")
            return s

    for i in range(n - 1, -1, -1):
        pivote = matriz_ref[i][i]
        b_val = matriz_ref[i][n]
        
        # Iniciar la suma con el tipo correcto (Fraction o float)
        subst_suma = Fraction(0) if is_fraction else 0.0
        explicacion_subst = []
        
        for j in range(i + 1, n):
            coef = matriz_ref[i][j]
            term = coef * x[j]
            subst_suma += term
            
            is_zero = (coef == 0) if is_fraction else (abs(coef) <= 1e-9)
            if not is_zero:
                explicacion_subst.append(f"({format_val(coef)})*({format_val(x[j])})")
        
        x[i] = (b_val - subst_suma) / pivote
        
        str_despeje = f"Despejando x{i + 1} de la Ec. {i + 1}:\n"
        if explicacion_subst:
            subst_text = " + ".join(explicacion_subst)
            str_despeje += f"  {format_val(pivote)}*x{i + 1} + [{subst_text}] = {format_val(b_val)}\n"
        
        str_despeje += f"  x{i + 1} = ({format_val(b_val)} - ({format_val(subst_suma)})) / {format_val(pivote)} ==> x{i + 1} = {format_val(x[i])}"
        pasos_despeje.append(str_despeje)
        
    return x, pasos_despeje


def extraer_solucion_rref(matriz_rref, n):
    """Para el resultado de Gauss-Jordan: la solucion queda directa en la ultima columna."""
    return [matriz_rref[i][n] for i in range(n)]