"""Motor de flujo de redes mediante matrices de incidencia y Gauss-Jordan."""

from core.lineal.eliminacion import eliminacion_por_filas

TOLERANCIA = 1e-9


def construir_matriz_incidencia(cantidad_nodos, ramas):
    """Construye la matriz nodo-rama con signo salida (+1) y entrada (-1)."""
    if cantidad_nodos <= 0:
        raise ValueError("La red debe tener al menos un nodo.")
    if not ramas:
        raise ValueError("La red debe tener al menos una rama.")

    matriz = [[0.0 for _ in ramas] for _ in range(cantidad_nodos)]
    for indice, rama in enumerate(ramas):
        origen, destino = rama
        if not 1 <= origen <= cantidad_nodos or not 1 <= destino <= cantidad_nodos:
            raise ValueError("Cada rama debe apuntar a nodos existentes.")
        if origen == destino:
            raise ValueError("Una rama no puede conectar un nodo consigo mismo.")
        matriz[origen - 1][indice] = 1.0
        matriz[destino - 1][indice] = -1.0
    return matriz


def construir_matriz_aumentada(cantidad_nodos, ramas, balances):
    """Construye [C | b] para el sistema de conservación C f = b."""
    if len(balances) != cantidad_nodos:
        raise ValueError("Debe existir un balance por cada nodo.")
    incidencia = construir_matriz_incidencia(cantidad_nodos, ramas)
    return [fila + [balances[indice]] for indice, fila in enumerate(incidencia)]


def resolver_flujo(cantidad_nodos, ramas, balances):
    """Resuelve los flujos y clasifica el sistema de conservación de nodos."""
    aumentada = construir_matriz_aumentada(cantidad_nodos, ramas, balances)
    incidencia = [fila[:-1] for fila in aumentada]
    reducida, pasos, pivotes = eliminacion_por_filas(
        aumentada,
        modo="gauss_jordan"
    )
    cantidad_ramas = len(ramas)

    for fila in reducida:
        coeficientes_nulos = all(
            abs(fila[columna]) < TOLERANCIA
            for columna in range(cantidad_ramas)
        )
        if coeficientes_nulos and abs(fila[-1]) >= TOLERANCIA:
            return {
                "tipo": "incompatible",
                "incidencia": incidencia,
                "aumentada": aumentada,
                "reducida": reducida,
                "pasos": pasos,
                "pivotes": pivotes,
                "flujos": None,
                "variables_libres": [],
            }

    variables_libres = [
        indice for indice in range(cantidad_ramas)
        if indice not in pivotes
    ]
    flujos = [0.0] * cantidad_ramas

    for fila in reducida:
        for columna in range(cantidad_ramas):
            if abs(fila[columna] - 1) < TOLERANCIA:
                flujos[columna] = fila[-1]
                break

    tipo = "determinado" if not variables_libres else "indeterminado"
    return {
        "tipo": tipo,
        "incidencia": incidencia,
        "aumentada": aumentada,
        "reducida": reducida,
        "pasos": pasos,
        "pivotes": pivotes,
        "flujos": flujos,
        "variables_libres": variables_libres,
    }
