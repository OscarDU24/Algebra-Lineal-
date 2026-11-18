"""Ayuda contextual de cada herramienta (sin conexión).

El contenido está centralizado en ``CONTENIDO``. Los formatos de entrada se
comprobaron contra los conversores del código (2026-11-18):

* ``lineal.conversiones.convertir_a_racional``, ``sistemas.operaciones_sistemas``
  y ``determinantes.operaciones_determinantes``: usan ``Fraction(texto)``.
* ``vectores`` y ``matriciales``: ``float(Fraction(texto))`` (resultado decimal).
* ``metodos_numericos.biseccion._crear_funcion``: evaluador AST de expresiones.

``mostrar_ayuda(ventana, clave)`` abre una sola ventana de ayuda por ventana
padre; si ya existe, la trae al frente y actualiza su contenido.
"""

from core.ui.ctk_compat import ctk
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
)

NUMEROS_EXACTOS = (
    "Enteros (-3), decimales con punto (0.25), fracciones (1/3) y notación "
    "científica (1e-3). La coma decimal (1,5) no se admite. El cálculo es exacto "
    "con fracciones."
)
NUMEROS_DECIMALES = (
    "Enteros (-3), decimales con punto (0.25), fracciones (1/3) y notación "
    "científica (1e-3). La coma decimal (1,5) no se admite. El cálculo se hace "
    "en decimales (aproximado)."
)
EXPRESIONES = (
    "Expresiones en x: + - * / y potencias con ^ o ** (x^2, 2^x). Se admite la "
    "multiplicación implícita (2x, 3(x+1), (x+1)(x-1)). Funciones: sin/sen, cos, "
    "tan/tg, csc, sec, cot, sqrt/raiz, exp, ln/log (log es logaritmo natural) y "
    "abs, siempre con paréntesis: sin(x). Constantes: pi (o π) y e. Máximo 300 "
    "caracteres; los exponentes numéricos deben tener valor absoluto ≤ 1000."
)

ATAJOS = """ATAJOS DE TECLADO
• Tab / Shift+Tab: pasar al campo siguiente o anterior. El campo activo se marca con un borde rojo.
• En una consola de resultados (haga clic en ella primero):
    Ctrl + rueda, Ctrl + «+», Ctrl + «-»: zoom   ·   Ctrl + 0: zoom al 100 %
    Ctrl + C: copiar el texto seleccionado
• Pantalla de inicio: 1 = Iniciar, 2 = Ayuda, ↑/↓ para elegir, Enter para confirmar, Esc para quitar la selección.
• «← Volver» o la X regresan a la pantalla anterior; si escribió datos, se pide confirmación.
• Los botones «Copiar resultados», «Limpiar resultados» y los de zoom están sobre cada consola."""

CONTENIDO = {
    "general": {
        "titulo": "HeyAlgb",
        "para_que": "Calculadora educativa de álgebra lineal y métodos numéricos que muestra el procedimiento paso a paso.",
        "datos": "Elija una tarjeta del menú para abrir una herramienta. Cada herramienta tiene su propia ayuda («? Ayuda»).",
        "formatos": NUMEROS_EXACTOS,
        "ejemplo": "Abra «Operaciones Básicas de Matrices», pulse «Cargar ejemplo» y después «Resolver Sistema».",
        "restricciones": "Los resultados aproximados se indican como tales; los límites son estimaciones numéricas.",
        "salida": "La consola de cada herramienta muestra primero el procedimiento y, al final, el resultado.",
    },
    "matriz": {
        "titulo": "Operaciones Básicas de Matrices",
        "para_que": "Resolver sistemas Ax = b por eliminación (Escalonado, Gauss o Gauss-Jordan) o calcular la inversa A⁻¹.",
        "datos": "Indique filas (m) y variables (n), pulse «Generar Matriz» y escriba los coeficientes. La última columna (TI) es el término independiente b.",
        "formatos": NUMEROS_EXACTOS,
        "ejemplo": "2x + y − z = 8, −3x − y + 2z = −11, −2x + y + 2z = −3  →  x = 2, y = 3, z = −1.",
        "restricciones": "«Matriz pura (A⁻¹)» exige m = n. Todas las casillas deben tener un número.",
        "salida": "Se muestra cada operación de fila, la matriz final, las columnas pivote, la clasificación (determinado, indeterminado o incompatible) y, si existe, la solución verificada. «Fracciones» o «Decimales» solo cambian la presentación.",
    },
    "vector": {
        "titulo": "Operaciones Vectoriales",
        "para_que": "Suma, resta, escalar, producto punto y cruz, magnitud, normalización, ángulo, proyección, distancia, combinación lineal y vectores a matriz.",
        "datos": "Elija la operación, indique la dimensión, pulse «Generar» y escriba las componentes de u, v (y los demás vectores si la operación los pide).",
        "formatos": NUMEROS_DECIMALES,
        "ejemplo": "u = (1, 2, 3), v = (4, 5, 6): producto punto = 32; producto cruz = (−3, 6, −3).",
        "restricciones": "El producto cruz requiere dimensión 3. Normalizar, ángulo y proyección no admiten el vector cero.",
        "salida": "La consola muestra la fórmula aplicada y el resultado en el formato elegido (fracción aproximada o decimal).",
    },
    "matricial": {
        "titulo": "Ecuaciones Matriciales",
        "para_que": "Productos A·u, propiedades (A(u+v) = Au + Av, A(cu) = c(Au)), combinación lineal, transpuesta, cA, inversa y Ax = b. También abre Tabla de Intercambio, Flujo de Red y Matrices Particionadas.",
        "datos": "Elija la operación, indique las dimensiones, pulse «Generar datos» y complete las casillas.",
        "formatos": NUMEROS_DECIMALES,
        "ejemplo": "A = [[1, 2], [3, 4]], u = (1, 1)  →  A·u = (3, 7).",
        "restricciones": "El vector debe tener tantas componentes como columnas tiene A. Las tres herramientas especiales se abren en su propia ventana; al volver, sus datos de aquí se conservan.",
        "salida": "Procedimiento y resultado en la consola inferior.",
    },
    "intercambio": {
        "titulo": "Tabla de Intercambio (Leontief)",
        "para_que": "Calcular la producción X del modelo abierto (I − A)X = D, o del modelo cerrado con el sector hogares.",
        "datos": "Indique el número de sectores, pulse «Generar tabla» y complete A (coeficientes técnicos) y D (demanda final). Para el modelo cerrado active «Sector hogares endógeno» y complete consumo e ingreso.",
        "formatos": NUMEROS_DECIMALES,
        "ejemplo": "A = [[0.2, 0.3], [0.4, 0.1]], D = (50, 30).",
        "restricciones": "Si I − A es singular, no hay producción única.",
        "salida": "Se muestran I − A, la matriz aumentada, los pasos de Gauss-Jordan y el vector X.",
    },
    "flujo_red": {
        "titulo": "Flujo de Red",
        "para_que": "Encontrar flujos que cumplan la conservación en cada nodo: salidas − entradas = balance externo.",
        "datos": "Indique nodos y ramas, pulse «Generar red», escriba para cada rama su nodo origen y destino, y el balance externo de cada nodo.",
        "formatos": "Nodos: enteros de 1 al número de nodos. Balances: " + NUMEROS_DECIMALES,
        "ejemplo": "3 nodos, 3 ramas: 1→2, 2→3, 1→3; balances (10, 0, −10).",
        "restricciones": "La suma de balances debe ser 0 para que exista solución. El flujo es positivo en el sentido origen → destino.",
        "salida": "Matriz de incidencia, sistema [C | b], pivotes, ramas libres y flujos (con restricciones fi ≥ 0 cuando hay infinitas soluciones).",
    },
    "particiones": {
        "titulo": "Matrices Particionadas",
        "para_que": "Suma y multiplicación por bloques, e inversa de una matriz triangular superior por bloques.",
        "datos": "Elija la operación, las dimensiones y los cortes de bloques; pulse «Generar editores», complete las matrices y pulse «Calcular».",
        "formatos": NUMEROS_EXACTOS,
        "ejemplo": "A = [[2, 1], [0, 3]] con corte 1|1, inversa triangular  →  [[1/2, −1/6], [0, 1/3]].",
        "restricciones": "Los cortes deben ser compatibles entre A y B; para la inversa, los bloques diagonales deben ser invertibles.",
        "salida": "Bloques de entrada, operaciones por bloque y la matriz reensamblada.",
    },
    "sistemas": {
        "titulo": "Sistemas de Ecuaciones Lineales",
        "para_que": "Resolver Ax = b por Gauss-Jordan, Factorización LU o Regla de Cramer, o analizar la independencia lineal de vectores (columnas de A).",
        "datos": "Elija el modo, indique filas y columnas, pulse «Generar Cuadrícula» y complete A (y b en modo sistema).",
        "formatos": NUMEROS_EXACTOS,
        "ejemplo": "x + 2y = 5, 3x + 4y = 6  →  x = −4, y = 9/2.",
        "restricciones": "Cramer y LU requieren A cuadrada; Cramer, además, det(A) ≠ 0.",
        "salida": "Procedimiento del método elegido y la solución, o la clasificación del sistema; en independencia, el número de pivotes y la conclusión.",
    },
    "limites": {
        "titulo": "Evaluación de Límites",
        "para_que": "Estimar numéricamente un límite evaluando f(x) cada vez más cerca del punto.",
        "datos": "Escriba f(x), el punto c y la dirección (bilateral, izquierda o derecha).",
        "formatos": EXPRESIONES + " El punto admite números, expresiones como pi/2 e infinito: inf, -inf, oo, ∞.",
        "ejemplo": "f(x) = sin(x)/x, c = 0, bilateral  →  lím ≈ 1.",
        "restricciones": "Es una estimación numérica, no una demostración: puede informar «no se estabiliza» en funciones que oscilan o crecen muy lento.",
        "salida": "f(c), una tabla de aproximaciones por cada lado, la tendencia (valor, +∞, −∞, no definida) y el resultado; si los laterales difieren, se indica que el límite no existe.",
    },
    "numerica": {
        "titulo": "Sistemas Numéricos",
        "para_que": "Convertir entre decimal, binario, octal y hexadecimal, y entre números arábigos y romanos.",
        "datos": "Elija la pestaña, escriba el número y elija la base de destino u origen.",
        "formatos": "Decimal: entero o con punto (45.75), con signo; hasta 300 dígitos enteros. Otra base: solo dígitos válidos de esa base (binario 0-1, octal 0-7, hexadecimal 0-9 y A-F) y opcionalmente un punto. Romanos: de 1 a 3999.",
        "ejemplo": "45.75 a binario  →  101101.11.",
        "restricciones": "La parte fraccionaria se calcula con 8 dígitos en la base destino.",
        "salida": "Resultado arriba y, debajo, divisiones o multiplicaciones sucesivas (o la descomposición polinómica).",
    },
    "determinantes": {
        "titulo": "Determinantes y Factorización LU",
        "para_que": "Calcular det(A) con Sarrus, cofactores o LU, mostrando cada paso.",
        "datos": "Indique el orden n, pulse «Generar matriz», complete A, elija el método y pulse «Calcular».",
        "formatos": NUMEROS_EXACTOS,
        "ejemplo": "A = [[2, −1, 0], [1, 3, 2], [0, 1, 4]]  →  det(A) = 24.",
        "restricciones": "Sarrus solo para 3×3 y 4×4. «Automático» usa el cálculo directo hasta orden 3 y LU desde orden 4.",
        "salida": "La evaluación de eficiencia aparece arriba; el procedimiento y el determinante, en la consola inferior.",
    },
    "biseccion": {
        "titulo": "Método de Bisección",
        "para_que": "Aproximar una raíz de f(x) = 0 en un intervalo [a, b] con cambio de signo.",
        "datos": "f(x), los extremos a y b, y la tolerancia (ancho del intervalo). «Explorar gráfica» ayuda a elegir a y b.",
        "formatos": EXPRESIONES,
        "ejemplo": "f(x) = x^3 − x − 2, a = 1, b = 2, tolerancia 1e-6  →  x ≈ 1.52138.",
        "restricciones": "Se requiere a < b, tolerancia > 0 y f(a)·f(b) < 0. La gráfica orienta, pero no garantiza continuidad.",
        "salida": "Raíz aproximada, f(raíz), criterio de paro y la tabla de iteraciones (xl, xu, xr, f, Ea %).",
    },
    "regla_falsa": {
        "titulo": "Método Regula Falsi",
        "para_que": "Aproximar una raíz con la recta secante entre los extremos de un intervalo con cambio de signo.",
        "datos": "f(x), a, b, tolerancia de Ea (%) y máximo de iteraciones.",
        "formatos": EXPRESIONES + " Máximo de iteraciones: entero de 1 a 100000.",
        "ejemplo": "f(x) = e^(−x) − x, a = 0, b = 1, tolerancia 0.00001 %  →  x ≈ 0.567143.",
        "restricciones": "Requiere cambio de signo. Si se agotan las iteraciones, se informa la última aproximación como no convergida.",
        "salida": "Estado (convergió o no), aproximación y tabla con a, b, c, f(c), extremo reemplazado y Ea %.",
    },
    "abiertos": {
        "titulo": "Métodos Abiertos (Newton-Raphson y Secante)",
        "para_que": "Aproximar raíces a partir de uno (Newton) o dos (Secante) valores iniciales, sin intervalo.",
        "datos": "Elija el método, escriba f(x), x0 (y x1 en Secante), la tolerancia y el máximo de iteraciones. Puede elegir el punto haciendo clic en la gráfica.",
        "formatos": EXPRESIONES + " Máximo de iteraciones: entero de 1 a 100000.",
        "ejemplo": "Newton: f(x) = x^3 − x − 2, x0 = 1.5, tolerancia 1e-8  →  x ≈ 1.5213797.",
        "restricciones": "Newton se detiene si no detecta cambios de signo en el rango de la gráfica (pulse «Forzar cálculo» para intentarlo). Un residuo pequeño sin cambio de signo cercano se informa como no convergido.",
        "salida": "Estado, raíz o última aproximación, el cálculo de la derivada numérica (Newton) o de la secante, y la tabla de iteraciones.",
    },
    "errores": {
        "titulo": "Análisis de Errores",
        "para_que": "Errores absoluto, relativo y porcentual; propagación de errores; truncamiento y redondeo; ejemplos de punto flotante; inversa exacta frente a la de punto flotante.",
        "datos": "Cada pestaña pide sus propios datos. En «Gauss-Jordan», escriba la matriz con una fila por línea y los elementos separados por espacios.",
        "formatos": "Números con punto decimal. Funciones de propagación: " + EXPRESIONES,
        "ejemplo": "Aproximado 9.8 y exacto 10  →  error absoluto 0.2, relativo 0.02 y porcentual 2 %. «Cargar Hilbert 5×5» carga un ejemplo de matriz.",
        "restricciones": "Si el valor exacto es 0, los errores relativo y porcentual no están definidos.",
        "salida": "Cada pestaña muestra su resultado en su propia consola.",
    },
}

_SECCIONES = (
    ("para_que", "PARA QUÉ SIRVE"),
    ("datos", "QUÉ DATOS INTRODUCIR"),
    ("formatos", "FORMATOS ADMITIDOS"),
    ("ejemplo", "EJEMPLO VÁLIDO"),
    ("restricciones", "RESTRICCIONES"),
    ("salida", "CÓMO LEER LA SALIDA"),
)


def texto_ayuda(clave):
    """Arma el texto de ayuda de una herramienta, con los atajos al final."""
    contenido = CONTENIDO.get(clave, CONTENIDO["general"])
    partes = [contenido["titulo"].upper(), ""]
    for campo, encabezado in _SECCIONES:
        partes.extend([encabezado, contenido[campo], ""])
    partes.append(ATAJOS)
    return "\n".join(partes)


def mostrar_ayuda(padre, clave):
    """Abre (o trae al frente) la ventana de ayuda de ``padre``."""
    from core.ui.zoom_resultados import crear_consola_resultados, escribir_consola

    ventana = getattr(padre, "_ventana_ayuda", None)
    try:
        existe = ventana is not None and ventana.winfo_exists()
    except Exception:
        existe = False
    if existe:
        escribir_consola(ventana._texto, texto_ayuda(clave))
        ventana.title(f"Ayuda · {CONTENIDO.get(clave, CONTENIDO['general'])['titulo']}")
        ventana.deiconify()
        ventana.lift()
        ventana.focus_force()
        return ventana

    ventana = ctk.CTkToplevel(padre)
    ventana.configure(fg_color=FONDO_CALCULADORA)
    ventana.title(f"Ayuda · {CONTENIDO.get(clave, CONTENIDO['general'])['titulo']}")
    ventana.geometry("640x560")
    ventana.minsize(420, 320)
    ventana.transient(padre)
    padre._ventana_ayuda = ventana

    contenedor, texto, _zoom = crear_consola_resultados(
        ventana, tamano=12, wrap="word", limpiable=False
    )
    contenedor.pack(fill="both", expand=True, padx=12, pady=(12, 6))
    ventana._texto = texto
    escribir_consola(texto, texto_ayuda(clave))

    # Si la ventana padre es modal (grab), la ayuda toma el grab mientras está
    # abierta y lo devuelve al cerrarse; de lo contrario no recibiría clics.
    padre_modal = False
    try:
        padre_modal = padre.grab_current() is padre
    except Exception:
        pass

    def cerrar(_evento=None):
        try:
            if padre_modal:
                ventana.grab_release()
            ventana.destroy()
        finally:
            padre._ventana_ayuda = None
            if padre_modal:
                try:
                    padre.grab_set()
                except Exception:
                    pass

    ctk.CTkLabel(
        ventana,
        text="Esc o «Cerrar» cierran esta ayuda.",
        text_color=TEXTO_CLARO,
    ).pack(side="left", padx=14, pady=(0, 12))
    ctk.CTkButton(
        ventana, text="Cerrar", command=cerrar, **estilo_boton_principal()
    ).pack(side="right", padx=14, pady=(0, 12))
    ventana.protocol("WM_DELETE_WINDOW", cerrar)
    ventana.bind("<Escape>", cerrar)
    ventana._cerrar = cerrar
    ventana.after(50, ventana.focus_force)
    if padre_modal:
        ventana.after(60, ventana.grab_set)
    return ventana


def cerrar_ayuda(padre):
    """Cierra la ayuda abierta desde ``padre``, si existe."""
    ventana = getattr(padre, "_ventana_ayuda", None)
    if ventana is None:
        return
    try:
        if ventana.winfo_exists():
            ventana._cerrar()
    except Exception:
        padre._ventana_ayuda = None
