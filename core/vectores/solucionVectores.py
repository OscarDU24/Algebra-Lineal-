TOLERANCIA = 1e-9


# ============================================================
# OBTENER RESULTADO DE UNA OPERACION VECTORIAL
# ============================================================

def obtener_resultado_vector(resultado):
    """
    Devuelve una copia del vector resultado.

    Se utiliza para evitar modificar directamente
    el vector original.
    """

    return resultado[:]


# ============================================================
# VERIFICAR VECTOR CERO
# ============================================================

def es_vector_cero(vector):
    """
    Verifica si todos los componentes de un vector
    son iguales a cero dentro de la tolerancia establecida.

    Retorna:
        True si el vector es cero.
        False en caso contrario.
    """

    for componente in vector:

        if abs(componente) >= TOLERANCIA:
            return False

    return True