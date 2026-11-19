"""Preferencias del usuario guardadas fuera del repositorio.

Se guardan en el directorio de configuración del usuario:

* Windows: ``%APPDATA%\\HeyAlgb\\preferencias.json``
* Otros sistemas: ``~/.config/HeyAlgb/preferencias.json``

La variable de entorno ``HEYALGB_CONFIG_DIR`` permite usar otra carpeta
(pruebas o instalaciones portátiles). Si el archivo falta o está dañado se
usan los valores predeterminados: la aplicación nunca deja de iniciar por
culpa de este archivo.
"""

import json
import logging
import os
from pathlib import Path

PREDETERMINADAS = {
    "mostrar_bienvenida": True,
    "musica_habilitada": True,
    "efectos_habilitados": True,
    "ultimo_modulo_utilizado": "Ninguno",
    "volumen_musica": 50,
    "volumen_efectos": 45,
}
CLAVES_VOLUMEN = {"volumen_musica", "volumen_efectos"}

_registro = logging.getLogger("heyalgb.preferencias")


def carpeta_configuracion():
    personalizada = os.environ.get("HEYALGB_CONFIG_DIR")
    if personalizada:
        return Path(personalizada)
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "HeyAlgb"
    return Path.home() / ".config" / "HeyAlgb"


def ruta_preferencias():
    return carpeta_configuracion() / "preferencias.json"


def cargar():
    """Devuelve las preferencias; ante cualquier problema, las predeterminadas."""
    preferencias = dict(PREDETERMINADAS)
    ruta = ruta_preferencias()
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return preferencias
    except (OSError, ValueError) as error:
        _registro.warning("Preferencias ilegibles en %s; se usan las predeterminadas (%s).", ruta, error)
        return preferencias
    if not isinstance(datos, dict):
        _registro.warning("Preferencias con formato inesperado en %s; se ignoran.", ruta)
        return preferencias
    for clave, valor_predeterminado in PREDETERMINADAS.items():
        valor = datos.get(clave, valor_predeterminado)
        if type(valor) is not type(valor_predeterminado):
            continue
        if clave in CLAVES_VOLUMEN and not 0 <= valor <= 100:
            _registro.warning(
                "Volumen fuera de rango para %s en %s; se usa el valor predeterminado.",
                clave,
                ruta,
            )
            continue
        preferencias[clave] = valor
    return preferencias


def guardar(**cambios):
    """Combina y guarda los cambios. Devuelve True si se escribieron."""
    preferencias = cargar()
    for clave, valor in cambios.items():
        if clave not in PREDETERMINADAS:
            continue
        if type(valor) is not type(PREDETERMINADAS[clave]):
            _registro.warning("Se ignoró un valor con tipo inválido para %s.", clave)
            continue
        if clave in CLAVES_VOLUMEN and not 0 <= valor <= 100:
            _registro.warning("Se ignoró un volumen fuera de rango para %s.", clave)
            continue
        preferencias[clave] = valor
    ruta = ruta_preferencias()
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        temporal = ruta.with_suffix(".tmp")
        temporal.write_text(
            json.dumps(preferencias, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        # replace() es atómico: un cierre a mitad de escritura no daña el archivo.
        temporal.replace(ruta)
        return True
    except OSError as error:
        _registro.warning("No se pudieron guardar las preferencias en %s (%s).", ruta, error)
        return False
