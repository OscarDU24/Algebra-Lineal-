"""Guía de bienvenida breve y omisible (4 pasos).

Aparece la primera vez que se muestra el Dashboard en cada sesión, salvo que
el usuario haya marcado «No mostrar al iniciar» (se guarda con
``core.ui.preferencias``). Se puede abrir de nuevo desde Ayuda › Guía de
bienvenida. No usa música, animaciones ni imágenes.
"""

import tkinter as tk

from core.ui import preferencias
from core.ui.ctk_compat import ctk
from core.ui.tema import (
    ACENTO,
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_panel_contenedor,
)

PASOS = (
    (
        "1 · Elija una herramienta",
        "Cada tarjeta del menú abre una calculadora: matrices, vectores, sistemas, "
        "límites, determinantes, sistemas numéricos o métodos numéricos. "
        "Haga clic en la tarjeta que necesite.",
    ),
    (
        "2 · Introduzca datos o cargue un ejemplo",
        "Escriba números como 3, 0.25 o 1/3. Si no sabe por dónde empezar, pulse "
        "«Cargar ejemplo»: llena los campos, pero no calcula nada. «? Ayuda» explica "
        "los formatos admitidos de cada herramienta.",
    ),
    (
        "3 · Calcule y lea el procedimiento",
        "Pulse el botón rojo de la herramienta. La consola muestra el procedimiento "
        "paso a paso y, al final, el resultado. Si algo falta o está mal escrito, el "
        "mensaje lo indica y el campo queda resaltado.",
    ),
    (
        "4 · Copie, amplíe y vuelva",
        "«Copiar resultados» copia la consola. Para ampliar el texto use Ctrl + rueda "
        "o los botones de zoom. «← Volver» regresa al menú; si escribió datos, se le "
        "pedirá confirmación antes de descartarlos.",
    ),
)


class GuiaBienvenida(ctk.CTkToplevel):
    """Ventana de 4 pasos con Anterior, Siguiente, Omitir y Finalizar."""

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self.title("Bienvenida · HeyAlgb")
        self.geometry("560x340")
        self.minsize(440, 300)
        self.transient(master)
        self.resizable(True, True)
        self.paso = 0
        self.var_no_mostrar = tk.BooleanVar(
            master=self, value=not preferencias.cargar()["mostrar_bienvenida"]
        )
        self._crear_interfaz()
        self._mostrar_paso()
        self.protocol("WM_DELETE_WINDOW", self.omitir)
        self.bind("<Escape>", lambda _e: self.omitir())
        self.bind("<Right>", lambda _e: self.siguiente())
        self.bind("<Left>", lambda _e: self.anterior())
        self.after(80, self._enfocar)

    def _crear_interfaz(self):
        panel = ctk.CTkFrame(self, **estilo_panel_contenedor())
        panel.pack(fill="both", expand=True, padx=14, pady=(14, 8))
        self.indicador = ctk.CTkLabel(panel, text="", text_color=ACENTO, font=("Segoe UI", 12, "bold"))
        self.indicador.pack(anchor="w", padx=14, pady=(12, 0))
        self.titulo = ctk.CTkLabel(panel, text="", text_color=TEXTO_CLARO, font=("Impact", 24))
        self.titulo.pack(anchor="w", padx=14, pady=(2, 6))
        self.cuerpo = ctk.CTkLabel(
            panel,
            text="",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14),
            justify="left",
            anchor="nw",
            wraplength=490,
        )
        self.cuerpo.pack(fill="x", anchor="n", padx=14, pady=(0, 12))
        panel.bind("<Configure>", lambda e: self.cuerpo.configure(wraplength=max(260, e.width - 40)))

        inferior = ctk.CTkFrame(self, fg_color="transparent")
        inferior.pack(fill="x", padx=14, pady=(0, 14))
        self.casilla = ctk.CTkCheckBox(
            inferior,
            text="No mostrar al iniciar",
            variable=self.var_no_mostrar,
            text_color=TEXTO_CLARO,
            fg_color=ACENTO,
            hover_color="#b30000",
        )
        self.casilla.pack(side="left")

        estilo = dict(estilo_boton_secundario(), width=96)
        self.boton_finalizar = ctk.CTkButton(
            inferior, text="Finalizar", width=96, command=self.finalizar, **estilo_boton_principal()
        )
        self.boton_siguiente = ctk.CTkButton(
            inferior, text="Siguiente →", width=110, command=self.siguiente, **estilo_boton_principal()
        )
        self.boton_anterior = ctk.CTkButton(inferior, text="← Anterior", command=self.anterior, **estilo)
        self.boton_omitir = ctk.CTkButton(inferior, text="Omitir", command=self.omitir, **estilo)
        self.boton_siguiente.pack(side="right")
        self.boton_anterior.pack(side="right", padx=6)
        self.boton_omitir.pack(side="right")

    def _mostrar_paso(self):
        titulo, texto = PASOS[self.paso]
        self.indicador.configure(text=f"Paso {self.paso + 1} de {len(PASOS)}")
        self.titulo.configure(text=titulo)
        self.cuerpo.configure(text=texto)
        self.boton_anterior.configure(state="normal" if self.paso > 0 else "disabled")
        ultimo = self.paso == len(PASOS) - 1
        if ultimo:
            self.boton_siguiente.pack_forget()
            self.boton_finalizar.pack(side="right", before=self.boton_anterior)
        else:
            self.boton_finalizar.pack_forget()
            self.boton_siguiente.pack(side="right", before=self.boton_anterior)

    def _enfocar(self):
        try:
            self.lift()
            self.focus_force()
        except tk.TclError:
            pass

    def siguiente(self):
        if self.paso < len(PASOS) - 1:
            self.paso += 1
            self._mostrar_paso()

    def anterior(self):
        if self.paso > 0:
            self.paso -= 1
            self._mostrar_paso()

    def _cerrar(self):
        preferencias.guardar(mostrar_bienvenida=not bool(self.var_no_mostrar.get()))
        master = self.master
        self.destroy()
        try:
            master._guia_bienvenida = None
            master.focus_force()
        except (tk.TclError, AttributeError):
            pass

    def omitir(self):
        self._cerrar()

    def finalizar(self):
        self._cerrar()


def abrir_bienvenida(raiz):
    """Abre la guía (o la trae al frente si ya está abierta)."""
    guia = getattr(raiz, "_guia_bienvenida", None)
    try:
        if guia is not None and guia.winfo_exists():
            guia.lift()
            guia.focus_force()
            return guia
    except tk.TclError:
        pass
    guia = GuiaBienvenida(raiz)
    raiz._guia_bienvenida = guia
    return guia


def mostrar_bienvenida_si_corresponde(raiz, retraso_ms=300):
    """Programa la guía tras mostrarse el Dashboard, si la preferencia lo indica.

    Devuelve el identificador de ``after`` (o None) para poder cancelarlo.
    """
    if not preferencias.cargar()["mostrar_bienvenida"]:
        return None

    def abrir():
        try:
            if raiz.winfo_exists() and raiz.state() != "withdrawn":
                abrir_bienvenida(raiz)
        except tk.TclError:
            pass

    return raiz.after(retraso_ms, abrir)
