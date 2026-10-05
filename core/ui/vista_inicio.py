"""Portada de HeyAlgb y ayuda inicial para el usuario."""

import tkinter as tk

from core.ui.ctk_compat import ctk
from core.ui.tema import (
    ACENTO,
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_panel_contenedor,
)


class VistaInicio:
    """Portada redimensionable; delega el paso al Dashboard al controlador."""

    MODULOS = [
        ("Matrices individuales", "Resuelve sistemas lineales por eliminación o mediante matriz inversa."),
        ("Operaciones vectoriales", "Suma, resta, escala vectores y explora combinaciones lineales."),
        ("Ecuaciones matriciales", "Practica productos matriz-vector, propiedades y sistemas Ax=b."),
        ("Sistemas e independencia", "Analiza sistemas lineales y relaciones entre vectores."),
        ("Límites", "Evalúa límites y continuidad con el módulo de cálculo."),
        ("Sistemas numéricos", "Convierte entre bases y entre números arábigos y romanos."),
    ]

    def __init__(self, root, audio_manager, al_iniciar):
        self.root = root
        self.audio = audio_manager
        self.al_iniciar = al_iniciar
        self.var_musica = tk.BooleanVar(value=self.audio.musica_habilitada)
        self.ventana_ayuda = None
        self.frame = ctk.CTkFrame(root, fg_color=FONDO_CALCULADORA, corner_radius=0)
        self.frame.pack(fill="both", expand=True)
        self._crear_contenido()
        self.audio.iniciar_musica_lobby()

    def _crear_contenido(self):
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        panel = ctk.CTkFrame(
            self.frame,
            fg_color="#111111",
            corner_radius=0,
            border_width=2,
            border_color="#4d0000",
        )
        panel.grid(row=1, column=0, sticky="nsew", padx=36, pady=24)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_columnconfigure(1, weight=2)
        panel.grid_rowconfigure(0, weight=1)

        marca = ctk.CTkFrame(panel, fg_color="transparent")
        marca.grid(row=0, column=0, sticky="nsew", padx=(28, 16), pady=28)
        ctk.CTkFrame(
            marca,
            width=150,
            height=150,
            fg_color="#ffffff",
            corner_radius=0,
            border_width=3,
            border_color=ACENTO,
        ).pack(pady=(0, 14))
        logo_placeholder = marca.winfo_children()[0]
        logo_placeholder.pack_propagate(False)
        ctk.CTkLabel(
            logo_placeholder,
            text="LOGO\nUNIVERSIDAD",
            text_color="#111111",
            font=("Segoe UI", 16, "bold"),
            justify="center",
        ).pack(expand=True, fill="both", padx=8, pady=8)
        ctk.CTkLabel(
            marca,
            text="Facultad de Ingeniería y Arquitectura\nUAM",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14, "bold"),
            justify="center",
            wraplength=240,
        ).pack(fill="x")

        contenido = ctk.CTkFrame(panel, fg_color="transparent")
        contenido.grid(row=0, column=1, sticky="nsew", padx=(12, 32), pady=24)
        contenido.grid_columnconfigure(0, weight=1)
        contenido.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            contenido,
            text="HeyAlgb",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 46, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", pady=(8, 2))
        ctk.CTkLabel(
            contenido,
            text="Calculadora educativa de Álgebra Lineal",
            text_color="#d5d5d5",
            font=("Segoe UI", 17),
            anchor="w",
        ).grid(row=1, column=0, sticky="new", pady=(0, 18))

        acciones = ctk.CTkFrame(contenido, fg_color="transparent")
        acciones.grid(row=2, column=0, sticky="ew", pady=(12, 4))
        acciones.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(
            acciones,
            text="Iniciar",
            **estilo_boton_principal(),
            command=self._iniciar,
            height=44,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkButton(
            acciones,
            text="Ayuda",
            **estilo_boton_secundario(),
            command=self.mostrar_ayuda,
            height=44,
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        self.switch_musica = ctk.CTkSwitch(
            contenido,
            text="Música de fondo",
            variable=self.var_musica,
            command=self._alternar_musica,
            text_color=TEXTO_CLARO,
            progress_color=ACENTO,
        )
        self.switch_musica.grid(row=3, column=0, sticky="w", pady=(12, 8))

    def _alternar_musica(self):
        self.audio.establecer_musica_habilitada(self.var_musica.get())

    def _iniciar(self):
        self.audio.reproducir_efecto("calcular")
        if self.ventana_ayuda is not None and self.ventana_ayuda.winfo_exists():
            self.ventana_ayuda.destroy()
        self.frame.destroy()
        self.al_iniciar()

    def mostrar_ayuda(self):
        if self.ventana_ayuda is not None and self.ventana_ayuda.winfo_exists():
            self.ventana_ayuda.lift()
            self.ventana_ayuda.focus_force()
            return

        ventana = ctk.CTkToplevel(self.root)
        self.ventana_ayuda = ventana
        ventana.title("Ayuda · HeyAlgb")
        ancho = max(560, min(1040, self.root.winfo_width() - 48))
        alto = max(500, min(820, self.root.winfo_height() - 48))
        ventana.geometry(f"{ancho}x{alto}")
        ventana.minsize(min(620, ancho), min(520, alto))
        ventana.configure(fg_color=FONDO_CALCULADORA)

        encabezado = ctk.CTkFrame(ventana, **estilo_panel_contenedor())
        encabezado.pack(fill="x", padx=18, pady=(18, 8))
        ctk.CTkLabel(
            encabezado,
            text="Ayuda de HeyAlgb",
            font=("Segoe UI", 25, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=18, pady=(14, 2))
        ctk.CTkLabel(
            encabezado,
            text="Una guía breve para elegir el módulo y entender sus entradas.",
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=18, pady=(0, 14))

        contenido = ctk.CTkScrollableFrame(
            ventana,
            label_text="Módulos",
            **estilo_panel_contenedor(),
        )
        contenido.pack(fill="both", expand=True, padx=18, pady=8)
        ctk.CTkLabel(
            contenido,
            text=(
                "HeyAlgb es una herramienta de apoyo para practicar conceptos de "
                "álgebra lineal. Cada calculadora separa la captura de datos del "
                "cálculo y presenta resultados o procedimientos para facilitar su revisión."
            ),
            text_color=TEXTO_CLARO,
            justify="left",
            wraplength=850,
        ).pack(anchor="w", padx=14, pady=(14, 18))

        for nombre, descripcion in self.MODULOS:
            modulo = ctk.CTkFrame(contenido, **estilo_panel_contenedor())
            modulo.pack(fill="x", padx=10, pady=6)
            modulo.grid_columnconfigure(1, weight=1)
            ctk.CTkFrame(
                modulo,
                width=110,
                height=76,
                fg_color="#202020",
                corner_radius=0,
                border_width=1,
                border_color=ACENTO,
            ).grid(row=0, column=0, rowspan=2, padx=12, pady=10)
            ctk.CTkLabel(
                modulo,
                text="Captura pendiente",
                text_color="#bdbdbd",
                font=("Segoe UI", 10),
            ).grid(row=0, column=0, rowspan=2)
            ctk.CTkLabel(
                modulo,
                text=nombre,
                text_color=TEXTO_CLARO,
                font=("Segoe UI", 15, "bold"),
                anchor="w",
            ).grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=(12, 2))
            ctk.CTkLabel(
                modulo,
                text=descripcion,
                text_color="#d0d0d0",
                justify="left",
                wraplength=760,
                anchor="w",
            ).grid(row=1, column=1, sticky="ew", padx=(0, 12), pady=(0, 12))

        equipo = ctk.CTkFrame(ventana, **estilo_panel_contenedor())
        equipo.pack(fill="x", padx=18, pady=(8, 18))
        ctk.CTkLabel(
            equipo,
            text="Integrantes del equipo",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=14, pady=(10, 4))
        ctk.CTkLabel(
            equipo,
            text="Integrante 1    ·    Integrante 2    ·    Integrante 3    ·    Integrante 4",
            text_color=TEXTO_CLARO,
            wraplength=850,
        ).pack(anchor="w", padx=14, pady=(0, 12))

        ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)
