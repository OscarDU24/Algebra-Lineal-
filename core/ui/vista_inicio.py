"""Portada de HeyAlgb y ayuda inicial para el usuario."""

import tkinter as tk
from pathlib import Path
from PIL import Image, ImageOps, ImageTk

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

    INTEGRANTES = (
        ("Liang Woo", "Liang_Amamiya.png"),
        ("Óscar Durán", "Oscar_Sakamoto.png"),
        ("Diego Gómez", "Diego_Kitagawa.png"),
        ("Carlos Aguirre", "Charly_Sakura.png"),
    )

    MODULOS = [
        ("Matrices individuales", "Resuelve sistemas lineales por eliminación o mediante matriz inversa."),
        ("Operaciones vectoriales", "Suma, resta, escala vectores y explora combinaciones lineales."),
        ("Ecuaciones matriciales", "Practica productos matriz-vector, propiedades y sistemas Ax=b."),
        ("Sistemas e independencia", "Analiza sistemas lineales y relaciones entre vectores."),
        ("Límites", "Evalúa límites y continuidad con el módulo de cálculo."),
        ("Sistemas numéricos", "Convierte entre bases y entre números arábigos y romanos."),
        ("Determinantes y Factorización LU", "Calcula determinantes y resuelve sistemas Ax=b mediante LU."),
    ]

    def __init__(self, root, audio_manager, al_iniciar):
        self.root = root
        self.audio = audio_manager
        self.al_iniciar = al_iniciar
        self.var_musica = tk.BooleanVar(value=self.audio.musica_habilitada)
        self.ventana_ayuda = None
        self._resize_job = None
        carpeta_assets = Path(__file__).resolve().parents[1] / "assets"
        with Image.open(carpeta_assets / "FondoMAIN.png") as fondo:
            self.fondo_original = fondo.convert("RGB")
        with Image.open(
            carpeta_assets / "HeyAlgbLogoBlanco.png"
        ) as logo:
            self.logo_original = logo.convert("RGBA")
        with Image.open(carpeta_assets / "UAMICON.png") as logo_uam:
            self.logo_uam_original = logo_uam.convert("RGBA")
        self.integrantes_originales = []
        for nombre, archivo in self.INTEGRANTES:
            with Image.open(carpeta_assets / archivo) as avatar:
                self.integrantes_originales.append((nombre, avatar.convert("RGBA")))

        self.frame = tk.Frame(root, bg="#141414")
        self.frame.pack(fill="both", expand=True)
        self._crear_contenido()
        self.audio.iniciar_musica_lobby()

    def _crear_contenido(self):
        self.contenido = tk.Canvas(
            self.frame,
            bg="#141414",
            highlightthickness=0,
            borderwidth=0,
        )
        self.contenido.pack(fill="both", expand=True)

        self.fondo_photo = ImageTk.PhotoImage(self.fondo_original)
        self.fondo_item = self.contenido.create_image(
            0, 0, image=self.fondo_photo, anchor="nw"
        )
        self.logo_photo = ImageTk.PhotoImage(self.logo_original)
        self.logo_item = self.contenido.create_image(
            0, 0, image=self.logo_photo, anchor="center"
        )
        self.subtitulo_item = self.contenido.create_text(
            0,
            0,
            text="Calculadora educativa de Álgebra Lineal",
            fill="#929292",
            font=("Times New Roman", 20),
            anchor="center",
        )

        estilo_iniciar = estilo_boton_principal()
        estilo_iniciar["font"] = ("Times New Roman", 22)
        estilo_ayuda = estilo_boton_secundario()
        estilo_ayuda["fg_color"] = "#bfbfbf"
        estilo_ayuda["font"] = ("Times New Roman", 22)
        self.boton_iniciar = ctk.CTkButton(
            self.contenido,
            text="Iniciar",
            **estilo_iniciar,
            command=self._iniciar,
            height=78,
        )
        self.boton_ayuda = ctk.CTkButton(
            self.contenido,
            text="Ayuda",
            **estilo_ayuda,
            command=self.mostrar_ayuda,
            height=78,
        )
        self.boton_iniciar_item = self.contenido.create_window(
            0, 0, window=self.boton_iniciar, anchor="center"
        )
        self.boton_ayuda_item = self.contenido.create_window(
            0, 0, window=self.boton_ayuda, anchor="center"
        )

        self.logo_uam_photo = ImageTk.PhotoImage(self.logo_uam_original)
        self.logo_uam_item = self.contenido.create_image(
            0, 0, image=self.logo_uam_photo, anchor="center"
        )
        self.facultad_item = self.contenido.create_text(
            0,
            0,
            text="Facultad de Ingeniería y\nArquitectura UAM",
            fill="#929292",
            font=("Times New Roman", 17),
            anchor="w",
            justify="left",
        )

        self.creditos_titulo_item = self.contenido.create_text(
            0,
            0,
            text="EQUIPO",
            fill="#ffffff",
            font=("Arial", 13, "bold"),
            anchor="w",
        )
        self.creditos = []
        for nombre, imagen in self.integrantes_originales:
            fondo_avatar = self.contenido.create_rectangle(
                0,
                0,
                1,
                1,
                fill="#c8c8c8",
                outline="#fe0000",
                width=2,
            )
            avatar_photo = ImageTk.PhotoImage(imagen)
            avatar_item = self.contenido.create_image(
                0, 0, image=avatar_photo, anchor="center"
            )
            nombre_item = self.contenido.create_text(
                0,
                0,
                text=nombre.upper(),
                fill="#e5e5e5",
                font=("Arial", 11, "bold"),
                anchor="center",
            )
            self.creditos.append(
                {
                    "nombre": nombre,
                    "original": imagen,
                    "background": fondo_avatar,
                    "photo": avatar_photo,
                    "image": avatar_item,
                    "label": nombre_item,
                }
            )

        self.switch_musica = ctk.CTkSwitch(
            self.contenido,
            text="Música de fondo",
            variable=self.var_musica,
            command=self._alternar_musica,
            text_color=TEXTO_CLARO,
            progress_color=ACENTO,
        )
        self.musica_item = self.contenido.create_window(
            0, 0, window=self.switch_musica, anchor="ne"
        )
        self.contenido.bind("<Configure>", self._programar_reorganizacion)
        self.root.after_idle(self._reorganizar_desde_canvas)

    @staticmethod
    def _escalar_fondo_cover(imagen, ancho, alto):
        return ImageOps.fit(
            imagen,
            (ancho, alto),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )

    def _programar_reorganizacion(self, event):
        if self._resize_job is not None:
            self.root.after_cancel(self._resize_job)
        self._resize_job = self.root.after(
            80,
            lambda ancho=event.width, alto=event.height: self._reorganizar_contenido(
                ancho, alto
            ),
        )

    def _reorganizar_desde_canvas(self):
        ancho = self.contenido.winfo_width()
        alto = self.contenido.winfo_height()
        if ancho > 1 and alto > 1:
            self._reorganizar_contenido(ancho, alto)

    def _reorganizar_contenido(self, ancho, alto):
        self._resize_job = None
        ancho = max(1, ancho)
        alto = max(1, alto)
        self.fondo_photo = ImageTk.PhotoImage(
            self._escalar_fondo_cover(self.fondo_original, ancho, alto)
        )
        self.contenido.itemconfigure(self.fondo_item, image=self.fondo_photo)
        self.contenido.coords(self.fondo_item, 0, 0)

        escala = min(ancho / 1192, alto / 812)
        lado_logo = max(1, int(min(ancho * 0.44, alto * 0.57)))
        self.logo_photo = ImageTk.PhotoImage(
            self.logo_original.resize(
                (lado_logo, lado_logo), Image.Resampling.LANCZOS
            )
        )
        self.contenido.itemconfigure(self.logo_item, image=self.logo_photo)
        self.contenido.coords(self.logo_item, ancho / 2, alto * 0.28)
        self.contenido.coords(
            self.subtitulo_item, ancho / 2, alto * 0.55
        )
        self.contenido.itemconfigure(
            self.subtitulo_item,
            font=("Times New Roman", max(13, int(20 * escala))),
        )

        ancho_boton = max(150, int(ancho * 0.38))
        alto_boton = max(46, int(alto * 0.098))
        separacion = ancho * 0.045
        desplazamiento = ancho_boton / 2 + separacion / 2
        centro_y_botones = alto * 0.695
        for boton in (self.boton_iniciar, self.boton_ayuda):
            boton.configure(
                width=ancho_boton,
                height=alto_boton,
                font=("Times New Roman", max(15, int(22 * escala))),
            )
        self.contenido.coords(
            self.boton_iniciar_item,
            ancho / 2 - desplazamiento,
            centro_y_botones,
        )
        self.contenido.coords(
            self.boton_ayuda_item,
            ancho / 2 + desplazamiento,
            centro_y_botones,
        )

        tamano_uam = max(38, min(68, int(68 * escala)))
        self.logo_uam_photo = ImageTk.PhotoImage(
            self.logo_uam_original.resize(
                (tamano_uam, tamano_uam), Image.Resampling.LANCZOS
            )
        )
        self.contenido.itemconfigure(self.logo_uam_item, image=self.logo_uam_photo)
        ancho_texto = min(270 * escala, ancho * 0.3)
        espacio_identidad = 14 * escala
        ancho_identidad = tamano_uam + espacio_identidad + ancho_texto
        inicio_identidad = ancho * 0.60 - ancho_identidad / 2
        centro_y_identidad = alto * 0.85
        self.contenido.coords(
            self.logo_uam_item,
            inicio_identidad + tamano_uam / 2,
            centro_y_identidad,
        )
        self.contenido.coords(
            self.facultad_item,
            inicio_identidad + tamano_uam + espacio_identidad,
            centro_y_identidad,
        )
        self.contenido.itemconfigure(
            self.facultad_item,
            font=("Times New Roman", max(12, int(17 * escala))),
            width=ancho_texto,
        )

        escala_ancho = ancho / 1192
        ancho_creditos = min(ancho * 0.47, 520 * escala_ancho)
        margen_creditos = max(12, 18 * escala)
        ancho_tarjeta_credito = (ancho_creditos - margen_creditos * 2) / len(
            self.creditos
        )
        tamano_avatar = max(
            34,
            min(70, int(min(68 * escala, ancho_tarjeta_credito * 0.68))),
        )
        base_x_creditos = margen_creditos
        y_titulo_creditos = alto * 0.79
        y_avatar = alto * 0.87
        y_nombre = alto * 0.95
        self.contenido.coords(
            self.creditos_titulo_item,
            base_x_creditos,
            y_titulo_creditos,
        )
        self.contenido.itemconfigure(
            self.creditos_titulo_item,
            font=("Arial", max(9, int(13 * escala)), "bold"),
        )
        for indice, credito in enumerate(self.creditos):
            centro_x = (
                base_x_creditos
                + ancho_tarjeta_credito * (indice + 0.5)
            )
            mitad = tamano_avatar / 2 + 3
            self.contenido.coords(
                credito["background"],
                centro_x - mitad,
                y_avatar - mitad,
                centro_x + mitad,
                y_avatar + mitad,
            )
            avatar = credito["original"].copy()
            avatar.thumbnail(
                (tamano_avatar, tamano_avatar),
                Image.Resampling.LANCZOS,
            )
            credito["photo"] = ImageTk.PhotoImage(avatar)
            self.contenido.itemconfigure(
                credito["image"], image=credito["photo"]
            )
            self.contenido.coords(credito["image"], centro_x, y_avatar)
            self.contenido.coords(credito["label"], centro_x, y_nombre)
            self.contenido.itemconfigure(
                credito["label"],
                font=("Arial", max(7, int(10 * escala)), "bold"),
                width=max(60, ancho_tarjeta_credito - 3),
            )
        self.contenido.coords(self.musica_item, ancho - 18, 16)

    def _alternar_musica(self):
        self.audio.establecer_musica_habilitada(self.var_musica.get())

    def _iniciar(self):
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
