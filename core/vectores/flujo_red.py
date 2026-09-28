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
    """Construye [C | b] usando la convención de balance externo entrada - salida.

    ``balances`` se recibe como salidas externas - entradas externas. La
    incidencia interna usa salidas - entradas, por lo que el lado derecho se
    invierte para respetar conservación de flujo.
    """
    if len(balances) != cantidad_nodos:
        raise ValueError("Debe existir un balance por cada nodo.")
    incidencia = construir_matriz_incidencia(cantidad_nodos, ramas)
    return [fila + [-balances[indice]] for indice, fila in enumerate(incidencia)]


def _parametrizar_flujos(reducida, pivotes, cantidad_ramas):
    """Representa cada flujo como una función afín de las ramas libres."""
    libres = [indice for indice in range(cantidad_ramas) if indice not in pivotes]
    filas_pivote = {}
    for fila in reducida:
        for columna in pivotes:
            if abs(fila[columna] - 1) < TOLERANCIA:
                filas_pivote[columna] = fila
                break

    expresiones = []
    for columna in range(cantidad_ramas):
        if columna in libres:
            coeficientes = [0.0] * len(libres)
            coeficientes[libres.index(columna)] = 1.0
            expresiones.append((0.0, coeficientes))
            continue

        fila = filas_pivote.get(columna)
        if fila is None:
            raise ValueError("No se pudo parametrizar una variable pivote.")
        coeficientes = [-fila[indice] for indice in libres]
        expresiones.append((fila[-1], coeficientes))

    return libres, expresiones


def _flujo_minimo_con_un_parametro(expresiones, indice_libre):
    """Busca el menor parámetro que mantiene todos los flujos no negativos."""
    limite_inferior = float("-inf")
    limite_superior = float("inf")

    for constante, coeficientes in expresiones:
        coeficiente = coeficientes[0]
        if abs(coeficiente) < TOLERANCIA:
            if constante < -TOLERANCIA:
                return None, None
            continue

        limite = -constante / coeficiente
        if coeficiente > 0:
            limite_inferior = max(limite_inferior, limite)
        else:
            limite_superior = min(limite_superior, limite)

    limite_inferior = max(limite_inferior, 0.0)
    if limite_inferior > limite_superior + TOLERANCIA:
        return None, (limite_inferior, limite_superior)

    parametro = limite_inferior
    flujos = [
        max(0.0, constante + coeficientes[0] * parametro)
        for constante, coeficientes in expresiones
    ]
    return flujos, (limite_inferior, limite_superior)


def resolver_flujo(cantidad_nodos, ramas, balances):
    """Resuelve el sistema y analiza flujos no negativos en redes dirigidas.

    ``balances`` sigue la convención externa salidas - entradas. Las ramas
    internas están orientadas origen -> destino y se restringen a flujo >= 0.
    """
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
                "expresiones": None,
                "intervalo_parametro": None,
                "factible_no_negativo": False,
            }

    variables_libres = [
        indice for indice in range(cantidad_ramas)
        if indice not in pivotes
    ]
    libres, expresiones = _parametrizar_flujos(
        reducida,
        pivotes,
        cantidad_ramas
    )

    flujos = None
    intervalo_parametro = None
    factible_no_negativo = None
    if not libres:
        flujos_candidato = [constante for constante, _ in expresiones]
        factible_no_negativo = all(
            flujo >= -TOLERANCIA for flujo in flujos_candidato
        )
        if factible_no_negativo:
            flujos = [max(0.0, flujo) for flujo in flujos_candidato]
    elif len(libres) == 1:
        flujos, intervalo_parametro = _flujo_minimo_con_un_parametro(
            expresiones,
            libres[0]
        )
        factible_no_negativo = flujos is not None

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
        "expresiones": expresiones,
        "intervalo_parametro": intervalo_parametro,
        "factible_no_negativo": factible_no_negativo,
    }
