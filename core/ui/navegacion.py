"""Barra común de navegación de las calculadoras: Volver, Ayuda y Cargar ejemplo.

``instalar_navegacion(ventana, ...)`` se llama al final del constructor de cada
ventana. No es un sistema general de navegación: cada ventana conserva su
propio ``al_cerrar`` (que ya sabe a qué ventana regresar) y aquí solo se
unifica cómo se llega a él:

* El botón «Volver» y la X de la ventana usan el mismo camino.
* Si el usuario escribió datos y alguno sigue presente, se pide confirmación
  antes de descartarlos; si no hay cambios, se sale sin preguntar.
* Los campos muestran un borde visible al recibir el foco.

Todos los bindings se instalan en la ventana (su etiqueta de Toplevel) y no en
``bind_all``: no afectan a otras ventanas.
"""

import tkinter as tk
from tkinter import messagebox

from core.ui.ctk_compat import ctk
from core.ui.tema import (
    COLOR_ADVERTENCIA,
    COLOR_FOCO,
    estilo_boton_secundario,
)

_TECLAS_SIN_CAMBIO = {
    "Tab", "ISO_Left_Tab", "Left", "Right", "Up", "Down", "Home", "End",
    "Prior", "Next", "Shift_L", "Shift_R", "Control_L", "Control_R",
    "Alt_L", "Alt_R", "Escape", "Return", "KP_Enter", "Caps_Lock",
    "Num_Lock", "Insert", "Win_L", "Win_R", "App", "Menu",
} | {f"F{numero}" for numero in range(1, 13)}
_TECLAS_CONTROL_QUE_EDITAN = {"v", "V", "x", "X", "z", "Z", "y", "Y"}
_MASCARA_CONTROL = 0x0004


def _es_editable(widget):
    if not isinstance(widget, (tk.Entry, tk.Text)):
        return False
    try:
        return str(widget.cget("state")) == "normal"
    except tk.TclError:
        return False


def _campos_editables(raiz):
    pendientes = [raiz]
    while pendientes:
        widget = pendientes.pop()
        if _es_editable(widget):
            yield widget
        pendientes.extend(widget.winfo_children())


class GuardiaCambios:
    """Registra si el usuario escribió en algún campo de la ventana."""

    def __init__(self, ventana):
        self.ventana = ventana
        self.modificada = False
        ventana.bind("<KeyPress>", self._al_teclear, add="+")

    def _al_teclear(self, evento):
        if not _es_editable(evento.widget) or evento.keysym in _TECLAS_SIN_CAMBIO:
            return
        if evento.state & _MASCARA_CONTROL and evento.keysym not in _TECLAS_CONTROL_QUE_EDITAN:
            return
        self.modificada = True

    def marcar_modificada(self):
        self.modificada = True

    def hay_datos_para_descartar(self):
        if not self.modificada:
            return False
        for campo in _campos_editables(self.ventana):
            try:
                contenido = (
                    campo.get("1.0", "end-1c") if isinstance(campo, tk.Text) else campo.get()
                )
            except tk.TclError:
                continue
            if contenido.strip():
                return True
        return False

    def confirmar_descartar(self, accion="salir"):
        if not self.hay_datos_para_descartar():
            return True
        return messagebox.askyesno(
            "Datos sin guardar",
            f"Hay datos escritos en esta herramienta. Si decide {accion}, se perderán.\n\n"
            f"¿Desea {accion} de todos modos?",
            icon="warning",
            parent=self.ventana,
        )


def _resaltar_foco(evento, activo):
    widget = evento.widget
    contenedor = getattr(widget, "master", None)
    if not isinstance(widget, tk.Entry) or not isinstance(contenedor, ctk.CTkEntry):
        return
    try:
        if not hasattr(contenedor, "_heyalgb_borde_original"):
            contenedor._heyalgb_borde_original = (
                contenedor.cget("border_color"),
                contenedor.cget("border_width"),
            )
        if getattr(contenedor, "_heyalgb_en_error", False):
            return
        if activo:
            contenedor.configure(border_color=COLOR_FOCO, border_width=2)
        else:
            color, ancho = contenedor._heyalgb_borde_original
            contenedor.configure(border_color=color, border_width=ancho)
    except tk.TclError:
        pass


def marcar_error_campo(entrada):
    """Resalta un CTkEntry con error, le da el foco y lo limpia al editarlo.

    El mensaje explicativo debe mostrarse aparte (con «⚠»): el color solo
    ayuda a localizar el campo.
    """
    if entrada is None:
        return
    try:
        if not hasattr(entrada, "_heyalgb_borde_original"):
            entrada._heyalgb_borde_original = (
                entrada.cget("border_color"),
                entrada.cget("border_width"),
            )
        entrada._heyalgb_en_error = True
        entrada.configure(border_color=COLOR_ADVERTENCIA, border_width=3)
        entrada.focus_set()
        entrada._entry.focus_set()
        entrada._entry.select_range(0, "end")
    except tk.TclError:
        return

    def quitar_marca(_evento=None):
        entrada._heyalgb_en_error = False
        try:
            entrada.configure(border_color=COLOR_FOCO, border_width=2)
        except tk.TclError:
            pass
        entrada._entry.unbind("<KeyPress>", identificador)

    identificador = entrada._entry.bind("<KeyPress>", quitar_marca, add="+")


def instalar_navegacion(
    ventana,
    clave_ayuda,
    texto_volver="← Volver al menú",
    al_cargar_ejemplo=None,
):
    """Añade la barra «Volver · Ayuda · Cargar ejemplo» arriba de la ventana.

    ``clave_ayuda`` es una clave de ``core.ui.ayuda.CONTENIDO`` o una función
    sin argumentos que la devuelve (para ventanas con varios paneles).
    """
    guardia = GuardiaCambios(ventana)
    ventana._guardia_cambios = guardia
    cerrar_original = ventana.al_cerrar
    estado = {"cerrando": False}

    def volver():
        if estado["cerrando"]:
            return
        if not guardia.confirmar_descartar("volver"):
            return
        estado["cerrando"] = True
        from core.ui.ayuda import cerrar_ayuda

        cerrar_ayuda(ventana)
        cerrar_original()

    ventana.volver = volver
    ventana.protocol("WM_DELETE_WINDOW", volver)
    ventana.bind("<FocusIn>", lambda e: _resaltar_foco(e, True), add="+")
    ventana.bind("<FocusOut>", lambda e: _resaltar_foco(e, False), add="+")

    barra = ctk.CTkFrame(ventana, fg_color="transparent")
    hijos = [hijo for hijo in ventana.pack_slaves() if hijo is not barra]
    opciones_pack = {"fill": "x", "padx": 15, "pady": (10, 0)}
    if hijos:
        barra.pack(before=hijos[0], **opciones_pack)
    else:
        barra.pack(**opciones_pack)

    estilo = dict(estilo_boton_secundario(), height=30)
    boton_volver = ctk.CTkButton(barra, text=texto_volver, command=volver, **estilo)
    boton_volver.pack(side="left")
    # Sonido de cambio de interfaz, igual que las tarjetas del Dashboard.
    boton_volver._heyalg_efecto_clic = "interfaces"

    def abrir_ayuda():
        from core.ui.ayuda import mostrar_ayuda

        clave = clave_ayuda() if callable(clave_ayuda) else clave_ayuda
        mostrar_ayuda(ventana, clave)

    ctk.CTkButton(barra, text="? Ayuda", width=90, command=abrir_ayuda, **estilo).pack(
        side="right"
    )
    if al_cargar_ejemplo is not None:
        def cargar_ejemplo():
            if al_cargar_ejemplo() is not False:
                guardia.marcar_modificada()

        ctk.CTkButton(
            barra, text="Cargar ejemplo", command=cargar_ejemplo, **estilo
        ).pack(side="right", padx=(0, 8))
    ventana._barra_navegacion = barra
    # Se ajusta cuando la ventana ya es visible: antes de mostrarse, Tk informa
    # el tamaño del contenido y no la geometría pedida por la vista.
    trabajo = ventana.after(250, lambda: ajustar_a_contenido(ventana))
    ventana.bind(
        "<Destroy>",
        lambda e: _cancelar(ventana, trabajo) if e.widget is ventana else None,
        add="+",
    )
    return barra


def _cancelar(ventana, trabajo):
    try:
        ventana.after_cancel(trabajo)
    except tk.TclError:
        pass


def ajustar_a_contenido(ventana, margen_vertical=80, margen_horizontal=40):
    """Agranda la ventana si su contenido no cabe, sin exceder la pantalla.

    Algunas vistas piden una geometría menor que su contenido y recortaban los
    controles inferiores. Aquí solo se agranda (nunca se reduce lo que el
    usuario o la vista eligieron) y se limita al área visible de la pantalla.
    """
    try:
        from customtkinter.windows.widgets.scaling import ScalingTracker

        if not ventana.winfo_exists() or not ventana.winfo_ismapped():
            return
        ventana.update_idletasks()
        escala = ScalingTracker.get_window_scaling(ventana) or 1.0
        actual_w = ventana.winfo_width()
        actual_h = ventana.winfo_height()
        disponible_w = ventana.winfo_screenwidth() - margen_horizontal
        disponible_h = ventana.winfo_screenheight() - margen_vertical
        nuevo_w = min(max(actual_w, ventana.winfo_reqwidth()), disponible_w)
        nuevo_h = min(max(actual_h, ventana.winfo_reqheight()), disponible_h)
        if (nuevo_w, nuevo_h) != (actual_w, actual_h):
            ventana.geometry(f"{round(nuevo_w / escala)}x{round(nuevo_h / escala)}")
    except (tk.TclError, KeyError, TypeError, ValueError):
        # El ajuste es una comodidad: si falla, la ventana conserva su tamaño.
        pass


def rellenar(filas_de_entradas, filas_de_valores):
    """Escribe valores en una cuadrícula de CTkEntry (lista de filas)."""
    for entradas, valores in zip(filas_de_entradas, filas_de_valores):
        for entrada, valor in zip(entradas, valores):
            entrada.delete(0, "end")
            entrada.insert(0, valor)


def escribir_campo(entrada, valor):
    entrada.delete(0, "end")
    entrada.insert(0, valor)


def confirmar_reemplazo(ventana, valores_actuales, valores_ejemplo):
    """Pide confirmación si los campos tienen datos distintos del ejemplo."""
    actuales = [str(v).strip() for v in valores_actuales]
    if not any(actuales) or actuales == [str(v) for v in valores_ejemplo]:
        return True
    return messagebox.askyesno(
        "Cargar ejemplo",
        "Los campos ya tienen datos. ¿Desea reemplazarlos por el ejemplo?",
        parent=ventana,
    )
