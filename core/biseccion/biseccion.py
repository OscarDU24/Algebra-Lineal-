import sympy as sp

def biseccionar(f, a, b, error_max):
    c = 0.0
    f_a = 0.0
    f_b = 0.0
    f_c = 0.0
    error = 0.0
    expr = sp.sympify(f)
    salida = ""
    i = 0

    while True:
        c = (a + b)/2

        # Nota: Reemplazar la funcion fija por una dinamica con ayuda de SymPy
        f_a = expr.subs('x', a)
        f_b = expr.subs('x', b)
        f_c = expr.subs('x', c)
        error = abs(f_c)

        salida += f"----------------------------------------\n"
        salida += f"Iteracion {i+1}\n"
        salida += f"\n"
        salida += f"a = {a:.4f}\n"
        salida += f"b = {b:.4f}\n"
        salida += f"c = {c:.4f}\n"
        salida += f"\n"
        salida += f"f(a) = {f_a:.4f}\n"
        salida += f"f(b) = {f_b:.4f}\n"
        salida += f"f(c) = {f_c:.4f}\n"
        salida += f"\n"
        salida += f"Error = {error}\n"

        if (f_a > 0) == (f_c > 0):
            a = c
        else:
            b = c

        if(error <= error_max):
            break

        i += 1
    
    salida += f"----------------------------------------\n"
    salida += f"Resultado: {c:.4f}\n"
    salida += f"Obtenido en {i+1} interaciones\n"
    salida += f"----------------------------------------\n"
    return c, salida


resultado, salida = biseccionar("(x**4) + (-5 * x**3) + (0.5 * x**2) + (-11 * x) + (10)",5.1, 5.3, 0.0001)

print(salida)