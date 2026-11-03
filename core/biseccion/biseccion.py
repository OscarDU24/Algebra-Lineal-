import sympy as sp
from math import isfinite

def biseccionar(f, a, b, error_max):
    c = 0.0
    f_a = 0.0
    f_b = 0.0
    f_c = 0.0
    error = 0.0
    salida = ""
    i = 0

    x = sp.Symbol('x', real=True)

    # Comprobaciones iniciales
    if not isinstance(f, str) or not f.strip():
        salida += "Error: Debe introducir una funcion."
        return c, salida

    try:
        expr = sp.sympify(f, locals={'x': x})
    except sp.SympifyError:
        return -1, "Error: La funcion introducida no es valida o contiene errores."

    # Comprobar que la funcion dependa solamente de x
    if expr.free_symbols - {x}:
        return -1, "Error: La funcion contiene variables no permitidas."

    if x not in expr.free_symbols:
        return -1, "Error: La funcion debe depender de la variable x."

    # Funcion auxiliar de evaluacion

    def evaluar(punto):
        resultado = sp.N(expr.subs(x, punto))

        # Comprobar que el resultado sea real
        if resultado.is_real is not True:
            raise ValueError("La funcion no produce un resultado real.")

        resultado = float(resultado)

        # Comprobar que el resultado sea finito
        if not isfinite(resultado):
            raise ValueError("La funcion produce un resultado no finito.")
        
        return resultado

    # --------------------------------------------------
    # 4. Evaluacion inicial de los extremos
    # --------------------------------------------------

    try:
        f_a = evaluar(a)
        f_b = evaluar(b)
    except Exception as e:
        return c, f"Error: La funcion no esta definida en los extremos del intervalo. {e}"

    # Comprobar si alguno de los extremos es una raiz
    if f_a == 0:
        return a, "Resultado: La raiz se encuentra en el extremo izquierdo."
    if f_b == 0:
        return b, "Resultado: La raiz se encuentra en el extremo derecho."
    
    # Comprobar que exista un cambio de signo
    if (f_a > 0) == (f_b > 0):
        return -1, "Error: El intervalo no presenta un cambio de signo."

    while True:
        c = (a + b)/2

        # Evitar que el intervalo deje de reducirse
        if c == a or c == b:
            salida += "Error: Se alcanzo el limite de precision numerica.\n"
            break

        # Evaluar la funcion en el punto medio
        try:
            f_c = evaluar(c)

        except Exception:
            salida += "Error: No fue posible evaluar la funcion en el punto medio.\n"
            break

        # Nota: Reemplazar la funcion fija por una dinamica con ayuda de SymPy
        f_a = evaluar(a)
        f_b = evaluar(b)
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
        elif (f_b > 0) == (f_c > 0):
            b = c
        else:
            salida += f"Error: No hay cambio de signo en la iteracion {i}\n"
            salida += "El intervalo introducido no es valido para el metodo de biseccion\n"
            return -1, salida

        if(error <= error_max):
            break
        # Comprobar si se encontro la raiz exacta
        if f_c == 0:
            salida += "Se encontro una raiz exacta.\n"
            break

        i += 1
    
    salida += f"----------------------------------------\n"
    salida += f"Resultado: {c:.4f}\n"
    salida += f"Obtenido en {i+1} interaciones\n"
    salida += f"----------------------------------------\n"
    return c, salida


if __name__ == "__main__":
    resultado, salida = biseccionar("(x^4) + (-5 * x^3) + (0.5 * x^2) + (-11 * x) + (10)",5.1, 5.3, 0.0001)
    print(salida)