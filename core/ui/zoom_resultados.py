"""Consolas de resultados de solo lectura con zoom local.

El zoom afecta únicamente a la consola donde se aplica: cambia el tamaño de un
``CTkFont`` propio de esa consola (CustomTkinter aplica el escalado DPI) y no
toca el escalado global, las entradas ni otras ventanas. No recalcula nada:
solo cambia cómo se ve el texto ya escrito.

Controles:
    Ctrl + rueda del ratón (con el puntero sobre la consola)
    Ctrl + «+» / Ctrl + «=» / Ctrl + «+» del teclado numérico: aumentar
    Ctrl + «-» / Ctrl + «-» del teclado numérico: disminuir
    Ctrl + 0 / Ctrl + 0 del teclado numérico: restablecer a 100 %
    Botones «−», «100 %» (restablece) y «+» sobre la consola.

El nivel se conserva mientras exista la consola (por ejemplo, al cambiar de
panel en Métodos Numéricos) y vuelve a 100 % al cerrar la ventana. No se
guarda en disco.
"""

from core.ui.ctk_compat import ctk
from core.ui.tema import (
    FUENTE_RESULTADOS,
    TEXTO_CLARO,
    estilo_boton_secundario,
    estilo_consola_resultado,
)

NIVEL_MINIMO = 50
NIVEL_MAXIMO = 200
PASO_NIVEL = 10
NIVEL_BASE = 100

_TECLAS_AUMENTAR = ("<Control-plus>", "<Control-equal>", "<Control-KP_Add>")
_TECLAS_DISMINUIR = ("<Control-minus>", "<Control-KP_Subtract>")
_TECLAS_RESTABLECER = ("<Control-Key-0>", "<Control-KP_0>", "<Control-KP_Insert>")


class ZoomConsola:
    """Aplica zoom a un ``CTkTextbox`` sin modificar su contenido."""

    def __init__(self, textbox, tamano_base, familia=FUENTE_RESULTADOS, peso="normal"):
        if tamano_base <= 0:
            raise ValueError("El tamaño base de la fuente debe ser positivo.")
        self.textbox = textbox
        self.tamano_base = tamano_base
        self.nivel = NIVEL_BASE
        self._observadores = []
        self.fuente = ctk.CTkFont(family=familia, size=tamano_base, weight=peso)
        textbox.configure(font=self.fuente)
        self._instalar_atajos()

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    @property
    def tamano_actual(self):
        return self.tamano_para(self.nivel)

    def tamano_para(self, nivel):
        # Siempre se calcula desde el tamaño base: no se acumulan redondeos.
        return max(1, round(self.tamano_base * nivel / 100))

    def establecer(self, nivel):
        nivel = max(NIVEL_MINIMO, min(NIVEL_MAXIMO, int(nivel)))
        if nivel == self.nivel:
            return self.nivel
        posicion = self._guardar_posicion()
        self.nivel = nivel
        self.fuente.configure(size=self.tamano_actual)
        self._restaurar_posicion(posicion)
        for observador in list(self._observadores):
            observador(self.nivel)
        return self.nivel

    def aumentar(self):
        return self.establecer(self.nivel + PASO_NIVEL)

    def disminuir(self):
        return self.establecer(self.nivel - PASO_NIVEL)

    def restablecer(self):
        return self.establecer(NIVEL_BASE)

    def agregar_observador(self, funcion):
        """Registra una función que recibe el nivel cada vez que cambia."""
        self._observadores.append(funcion)
        funcion(self.nivel)

    # ------------------------------------------------------------------
    # Atajos (solo en esta consola; nunca bind_all)
    # ------------------------------------------------------------------
    def _instalar_atajos(self):
        texto = self.textbox._textbox
        # El texto de solo lectura también debe poder recibir el foco para que
        # funcionen los atajos de teclado y Ctrl+C.
        texto.configure(takefocus=1)
        texto.bind("<Button-1>", lambda _evento: texto.focus_set(), add="+")
        texto.bind("<Control-MouseWheel>", self._al_girar_rueda)
        # X11 entrega la rueda como botones 4 y 5.
        texto.bind("<Control-Button-4>", lambda _e: self._accion(self.aumentar))
        texto.bind("<Control-Button-5>", lambda _e: self._accion(self.disminuir))
        for secuencia in _TECLAS_AUMENTAR:
            texto.bind(secuencia, lambda _e: self._accion(self.aumentar))
        for secuencia in _TECLAS_DISMINUIR:
            texto.bind(secuencia, lambda _e: self._accion(self.disminuir))
        for secuencia in _TECLAS_RESTABLECER:
            texto.bind(secuencia, lambda _e: self._accion(self.restablecer))

    def _al_girar_rueda(self, evento):
        if evento.delta > 0:
            self.aumentar()
        elif evento.delta < 0:
            self.disminuir()
        # "break" impide que la rueda también desplace el texto o un
        # CTkScrollableFrame exterior.
        return "break"

    @staticmethod
    def _accion(funcion):
        funcion()
        return "break"

    # ------------------------------------------------------------------
    # Posición de lectura
    # ------------------------------------------------------------------
    def _guardar_posicion(self):
        texto = self.textbox._textbox
        try:
            return texto.index("@0,0"), texto.xview()[0]
        except Exception:  # El widget puede no estar visible todavía.
            return None

    def _restaurar_posicion(self, posicion):
        if posicion is None:
            return
        indice, fraccion_x = posicion
        texto = self.textbox._textbox
        texto.update_idletasks()
        texto.yview(indice)
        texto.xview_moveto(fraccion_x)


def escribir_consola(textbox, texto):
    """Reemplaza el contenido de una consola de solo lectura."""
    textbox.configure(state="normal")
    textbox.delete("1.0", "end")
    textbox.insert("1.0", texto)
    textbox.configure(state="disabled")


def copiar_consola(textbox, formateador=None):
    """Copia todo el contenido de la consola al portapapeles.

    Devuelve True si había texto. No modifica la consola ni recalcula nada.
    No se separa «resultado» de «procedimiento»: el texto de cada herramienta
    no tiene una marca fiable para hacerlo sin cortes frágiles. Un formateador
    opcional permite que una vista prepare una copia distinta de su salida.
    """
    texto = textbox.get("1.0", "end-1c")
    if not texto.strip():
        return False
    texto_copiado = formateador(texto) if formateador is not None else texto
    if not isinstance(texto_copiado, str):
        raise TypeError("El formateador de copia debe devolver texto.")
    if not texto_copiado.strip():
        return False
    textbox.clipboard_clear()
    textbox.clipboard_append(texto_copiado)
    return True


def _crear_acciones(
    barra, textbox, limpiable, formateador_copia=None, al_copiar=None
):
    """Botones «Copiar resultados» y «Limpiar resultados» con aviso breve."""
    estilo = dict(estilo_boton_secundario(), height=24, font=("Arial", 12, "bold"))
    aviso = ctk.CTkLabel(barra, text="", text_color=TEXTO_CLARO, font=("Segoe UI", 12))
    estado = {"trabajo": None}

    def avisar(mensaje):
        aviso.configure(text=mensaje)
        if estado["trabajo"] is not None:
            aviso.after_cancel(estado["trabajo"])
        estado["trabajo"] = aviso.after(1800, limpiar_aviso)

    def limpiar_aviso():
        estado["trabajo"] = None
        aviso.configure(text="")

    def cancelar_aviso(_evento=None):
        if estado["trabajo"] is not None:
            try:
                aviso.after_cancel(estado["trabajo"])
            except Exception:
                pass
            estado["trabajo"] = None

    aviso.bind("<Destroy>", cancelar_aviso, add="+")

    def copiar():
        copiado = copiar_consola(textbox, formateador_copia)
        avisar("✓ Copiado" if copiado else "Nada que copiar")
        if copiado and al_copiar is not None:
            al_copiar()

    boton_copiar = ctk.CTkButton(
        barra, text="Copiar resultados", width=130, command=copiar, **estilo
    )
    boton_copiar.pack(side="left", padx=(0, 4))
    boton_limpiar = None
    if limpiable:
        def limpiar():
            escribir_consola(textbox, "")
            avisar("Resultados limpiados")

        boton_limpiar = ctk.CTkButton(
            barra, text="Limpiar resultados", width=130, command=limpiar, **estilo
        )
        boton_limpiar.pack(side="left", padx=(0, 4))
    aviso.pack(side="left", padx=6)
    barra.boton_copiar = boton_copiar
    barra.boton_limpiar_resultados = boton_limpiar
    barra.aviso = aviso
    barra.copiar = copiar
    return barra


def crear_consola_resultados(
    master,
    tamano=12,
    wrap="none",
    height=None,
    titulo=None,
    limpiable=True,
    formateador_copia=None,
    al_copiar=None,
):
    """Crea una consola monoespaciada de solo lectura con controles de zoom.

    Sobre la consola se muestran «Copiar resultados», «Limpiar resultados»
    (si ``limpiable``) y el zoom. Devuelve ``(contenedor, textbox, zoom)``.
    El contenedor es el widget que la vista debe ubicar con ``pack`` o ``grid``.
    """
    contenedor = ctk.CTkFrame(master, fg_color="transparent")
    barra = ctk.CTkFrame(contenedor, fg_color="transparent")
    barra.pack(fill="x", pady=(0, 2))
    if titulo:
        ctk.CTkLabel(
            barra,
            text=titulo,
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left", padx=(2, 0))

    opciones = dict(estilo_consola_resultado(), wrap=wrap)
    if height is not None:
        opciones["height"] = height
    textbox = ctk.CTkTextbox(contenedor, **opciones)
    textbox.pack(fill="both", expand=True)
    textbox.configure(state="disabled")
    zoom = ZoomConsola(textbox, tamano)

    _crear_acciones(barra, textbox, limpiable, formateador_copia, al_copiar)
    contenedor.barra = barra
    controles = crear_controles_zoom(barra, zoom)
    controles.pack(side="right")
    contenedor.controles_zoom = controles
    return contenedor, textbox, zoom


def crear_controles_zoom(master, zoom):
    """Botones discretos «−», porcentaje (restablece) y «+»."""
    marco = ctk.CTkFrame(master, fg_color="transparent")
    estilo = dict(estilo_boton_secundario(), height=24, font=("Arial", 12, "bold"))
    # La etiqueta deja claro que el porcentaje es el zoom y que al pulsarlo
    # se restablece (distinto de «Limpiar resultados»).
    ctk.CTkLabel(
        marco, text="Zoom (clic en % = 100 %):", text_color=TEXTO_CLARO, font=("Segoe UI", 12)
    ).pack(side="left", padx=(0, 4))
    boton_menos = ctk.CTkButton(marco, text="−", width=28, command=zoom.disminuir, **estilo)
    boton_nivel = ctk.CTkButton(marco, text="100 %", width=62, command=zoom.restablecer, **estilo)
    boton_mas = ctk.CTkButton(marco, text="+", width=28, command=zoom.aumentar, **estilo)
    boton_menos.pack(side="left")
    boton_nivel.pack(side="left", padx=2)
    boton_mas.pack(side="left")

    def actualizar(nivel):
        boton_nivel.configure(text=f"{nivel} %")
        boton_menos.configure(state="normal" if nivel > NIVEL_MINIMO else "disabled")
        boton_mas.configure(state="normal" if nivel < NIVEL_MAXIMO else "disabled")

    zoom.agregar_observador(actualizar)
    marco.boton_menos = boton_menos
    marco.boton_nivel = boton_nivel
    marco.boton_mas = boton_mas
    return marco
