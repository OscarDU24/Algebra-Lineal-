"""Entrada integrada y panel reutilizable del recorrido de HeyAlgb."""

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


class GuiaBienvenida(ctk.CTkFrame):
    """Presenta la bienvenida dentro de la raíz existente, sin ventanas nuevas."""

    def __init__(self, master, al_comenzar=None, al_omitir=None):
        super().__init__(master, fg_color=FONDO_CALCULADORA)
        self._al_comenzar = al_comenzar
        self._al_omitir = al_omitir
        self.var_no_mostrar = tk.BooleanVar(
            master=self,
            value=not preferencias.cargar()["mostrar_bienvenida"],
        )
        self._crear_interfaz()

    def _crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        panel = ctk.CTkFrame(self, **estilo_panel_contenedor())
        panel.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            panel,
            text="Bienvenido a HeyAlgb",
            text_color=TEXTO_CLARO,
            font=("Impact", 34),
        ).grid(row=0, column=0, padx=28, pady=(28, 8), sticky="w")
        ctk.CTkLabel(
            panel,
            text=(
                "Conoce una herramienta real con un ejercicio guiado. "
                "El recorrido es opcional y puedes salir en cualquier momento."
            ),
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 16),
            justify="left",
            anchor="nw",
            wraplength=680,
        ).grid(row=1, column=0, padx=28, pady=(0, 20), sticky="new")

        acciones = ctk.CTkFrame(panel, fg_color="transparent")
        acciones.grid(row=3, column=0, padx=28, pady=(0, 28), sticky="ew")
        acciones.grid_columnconfigure(0, weight=1)
        ctk.CTkCheckBox(
            acciones,
            text="No mostrar al iniciar",
            variable=self.var_no_mostrar,
            text_color=TEXTO_CLARO,
            fg_color=ACENTO,
            hover_color="#b30000",
        ).grid(row=0, column=0, sticky="w", pady=(0, 16))
        ctk.CTkButton(
            acciones,
            text="Comenzar recorrido",
            command=self.comenzar,
            **estilo_boton_principal(),
        ).grid(row=1, column=0, sticky="w", padx=(0, 10))
        ctk.CTkButton(
            acciones,
            text="Omitir e ir al menú",
            command=self.omitir,
            **estilo_boton_secundario(),
        ).grid(row=1, column=1, sticky="e")
        panel.bind(
            "<Configure>",
            lambda evento: self._ajustar_texto(panel, evento.width),
            add="+",
        )

    def _ajustar_texto(self, panel, ancho):
        for hijo in panel.grid_slaves(row=1, column=0):
            hijo.configure(wraplength=max(220, ancho - 56))

    def comenzar(self):
        self._cerrar_y_continuar(self._al_comenzar)

    def omitir(self):
        self._cerrar_y_continuar(self._al_omitir)

    def _cerrar_y_continuar(self, continuar):
        preferencias.guardar(
            mostrar_bienvenida=not bool(self.var_no_mostrar.get())
        )
        raiz = self.master
        if getattr(raiz, "_guia_bienvenida", None) is self:
            raiz._guia_bienvenida = None
        self.destroy()
        if continuar is not None:
            continuar()


class PanelRecorrido(ctk.CTkFrame):
    """Panel lateral breve reutilizable en el Dashboard y la herramienta."""

    def __init__(self, master, anterior, salir, siguiente):
        super().__init__(master, width=300, **estilo_panel_contenedor())
        self._anterior = anterior
        self._salir = salir
        self._siguiente = siguiente
        self.pack_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.progreso = ctk.CTkLabel(
            self,
            text="",
            text_color=ACENTO,
            font=("Segoe UI", 13, "bold"),
        )
        self.progreso.grid(row=0, column=0, padx=18, pady=(20, 6), sticky="w")
        self.titulo = ctk.CTkLabel(
            self,
            text="",
            text_color=TEXTO_CLARO,
            font=("Impact", 24),
            justify="left",
            anchor="w",
            wraplength=250,
        )
        self.titulo.grid(row=1, column=0, padx=18, pady=(0, 12), sticky="new")
        self.descripcion = ctk.CTkLabel(
            self,
            text="",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14),
            justify="left",
            anchor="nw",
            wraplength=250,
        )
        self.descripcion.grid(
            row=2, column=0, padx=18, pady=(0, 18), sticky="nsew"
        )

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.grid(row=3, column=0, padx=12, pady=(0, 14), sticky="ew")
        acciones.grid_columnconfigure(0, weight=1)
        acciones.grid_columnconfigure(1, weight=1)
        self.boton_anterior = ctk.CTkButton(
            acciones,
            text="← Anterior",
            command=self._anterior,
            width=88,
            **estilo_boton_secundario(),
        )
        self.boton_anterior.grid(row=0, column=0, padx=3, sticky="ew")
        ctk.CTkButton(
            acciones,
            text="Salir del recorrido",
            command=self._salir,
            width=120,
            **estilo_boton_secundario(),
        ).grid(row=1, column=0, columnspan=2, padx=3, pady=(8, 0), sticky="ew")
        self.boton_siguiente = ctk.CTkButton(
            acciones,
            text="Siguiente →",
            command=self._siguiente,
            width=94,
            **estilo_boton_principal(),
        )
        self.boton_siguiente.grid(row=0, column=1, padx=3, sticky="ew")
        self.bind("<Configure>", self._ajustar_texto, add="+")

    def mostrar(
        self,
        paso,
        total,
        titulo,
        descripcion,
        *,
        anterior_habilitado,
        siguiente_habilitado,
        siguiente_texto="Siguiente →",
    ):
        self.progreso.configure(text=f"Paso {paso} de {total}")
        self.titulo.configure(text=titulo)
        self.descripcion.configure(text=descripcion)
        self.boton_anterior.configure(
            state="normal" if anterior_habilitado else "disabled"
        )
        self.boton_siguiente.configure(
            text=siguiente_texto,
            state="normal" if siguiente_habilitado else "disabled",
        )

    def mostrar_fin(self):
        self.progreso.configure(text="Recorrido completado")
        self.titulo.configure(text="Ya conoces el flujo")
        self.descripcion.configure(
            text=(
                "Puedes volver al menú y explorar las demás herramientas. "
                "Cada una conserva su propia ayuda específica."
            )
        )
        self.boton_anterior.configure(state="disabled")
        self.boton_siguiente.configure(state="disabled")

    def _ajustar_texto(self, evento):
        ancho_texto = max(180, evento.width - 44)
        self.titulo.configure(wraplength=ancho_texto)
        self.descripcion.configure(wraplength=ancho_texto)


def abrir_bienvenida(raiz, al_comenzar=None, al_omitir=None):
    """Muestra la bienvenida dentro de ``raiz`` o reutiliza la ya abierta."""
    guia = getattr(raiz, "_guia_bienvenida", None)
    if guia is not None and guia.winfo_exists():
        return guia
    guia = GuiaBienvenida(raiz, al_comenzar, al_omitir)
    guia.pack(fill="both", expand=True)
    raiz._guia_bienvenida = guia
    return guia


def mostrar_bienvenida_si_corresponde(
    raiz,
    al_comenzar=None,
    al_omitir=None,
):
    """Muestra la bienvenida integrada si la preferencia del usuario lo indica."""
    if not preferencias.cargar()["mostrar_bienvenida"]:
        return None
    return abrir_bienvenida(raiz, al_comenzar, al_omitir)
