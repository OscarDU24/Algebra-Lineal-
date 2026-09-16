# ============================================================
# OPERACIONES - CÁLCULO DE LÍMITES CON SYMPY
# ============================================================

import sympy as sp

def calcular_limite(funcion_str, punto_str, direccion="bilateral"):
    """
    Evalúa el límite de una función matemática en un punto dado usando SymPy.
    """
    x = sp.Symbol('x')
    salida = []
    
    try:
        # 1. Transformar el texto a expresiones matemáticas seguras
        f = sp.sympify(funcion_str)
        
        # 2. Manejo de infinitos en el punto de evaluación
        punto_limpio = punto_str.lower().strip()
        if punto_limpio in ['inf', 'infinito', 'oo']:
            c = sp.oo
        elif punto_limpio in ['-inf', '-infinito', '-oo']:
            c = -sp.oo
        else:
            c = sp.sympify(punto_limpio)
            
        # 3. Mapeo de dirección para SymPy
        dir_sympy = "+-"  # Bilateral por defecto
        if direccion == "izquierda":
            dir_sympy = "-"
        elif direccion == "derecha":
            dir_sympy = "+"
            
        # 4. Calcular el límite exacto
        limite = sp.limit(f, x, c, dir=dir_sympy)
        
        # 5. Formatear la salida para la consola
        salida.append("=========================================")
        salida.append("   ANÁLISIS DE LÍMITE (MOTOR SIMBÓLICO)")
        salida.append("=========================================")
        salida.append(f"Función original : f(x) = {f}")
        salida.append(f"Evaluando cuando : x -> {c}")
        salida.append(f"Dirección        : {direccion.capitalize()}")
        salida.append("-----------------------------------------")
        
        # Verificar si es una oscilación infinita (ej: límite de sin(1/x) cuando x->0)
        if limite.has(sp.AccumBounds):
            salida.append("\n[!] RESULTADO: El límite no existe.")
            salida.append("Motivo: La función oscila infinitamente en ese punto sin converger a un valor.")
        else:
            salida.append(f"\n[>] RESULTADO EXACTO: {limite}")
            
            # Si el límite exacto es algo complejo (como una fracción o expresión con pi), 
            # mostramos la aproximación decimal de cortesía
            if limite.is_number and not limite in [sp.oo, -sp.oo, sp.zoo, sp.nan]:
                aproximacion = limite.evalf()
                if str(limite) != str(aproximacion):
                    salida.append(f"    (Aprox. Decimal: {aproximacion:.6f})")

        return "\n".join(salida)

    except sp.SympifyError:
        return "ERROR: Sintaxis matemática inválida.\nRevisa que los paréntesis y operadores (como '*', '**') estén correctos."
    except Exception as e:
        return f"ERROR INTERNO durante el cálculo:\n{str(e)}"