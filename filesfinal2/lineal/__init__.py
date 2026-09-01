from .entrada import (
    leer_dimensiones,
    construir_matriz_aumentada,
    leer_metodo,
)
from .visualizacion import (
    imprimir_matriz, 
    copiar_matriz, 
    imprimir_sistema_ecuaciones,
)
from .eliminacion import eliminacion_por_filas
from .clasificacion import clasificar_sistema
from .solucion import (
    sustitucion_hacia_atras, 
    extraer_solucion_rref, 
    sustitucion_hacia_atras_detallada,
)
from .verificacion import verificar_solucion

__all__ = [
    "leer_dimensiones",
    "construir_matriz_aumentada",
    "leer_metodo",
    "imprimir_matriz",
    "copiar_matriz",
    "imprimir_sistema_ecuaciones",
    "eliminacion_por_filas",
    "clasificar_sistema",
    "sustitucion_hacia_atras",
    "extraer_solucion_rref",
    "sustitucion_hacia_atras_detallada",
    "verificar_solucion",
]