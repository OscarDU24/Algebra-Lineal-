"""Portada de HeyAlgb y ayuda inicial para el usuario."""

import ctypes
import random
import sys
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageTk

from core.ui.ctk_compat import ctk
from core.ui.tema import (
    ACENTO,
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_panel_contenedor,
)
from core.ui import preferencias


class VistaInicio:
    """Portada redimensionable; delega el paso al Dashboard al controlador."""

    FUENTES = (
        ("Anton", "Anton-Regular.ttf"),
        ("Archivo Black", "ArchivoBlack-Regular.ttf"),
        ("Alfa Slab One", "AlfaSlabOne-Regular.ttf"),
        ("Caprasimo", "Caprasimo-Regular.ttf"),
        ("Playfair Display", "PlayfairDisplay-VariableFont_wght.ttf"),
        ("League Spartan", "LeagueSpartan-VariableFont_wght.ttf"),
        ("Helvetica Now Display", "HelveticaNowDisplay-Bold.ttf"),
        ("Oswald", "Oswald-VariableFont_wght.ttf"),
        ("Tinos", "Tinos-Bold.ttf"),
        ("Abril Fatface", "AbrilFatface-Regular.ttf"),
    )

    INTEGRANTES = (
        ("Liang Woo", "Liang_Amamiya.png"),
        ("Óscar Durán", "Oscar_Sakamoto.png"),
        ("Diego Gómez", "Diego_Kitagawa.png"),
        ("Carlos Aguirre", "Charly_Sakura.png"),
    )
    PROFESOR = ("Profesor Iván Argüello Martinez", "Argüello_Sojiro.png")

    MODULOS = [
        (
            "Matrices individuales",
            "Resuelve sistemas lineales por eliminación o mediante matriz inversa.",
            "MatrIndvICON.png",
        ),
        (
            "Operaciones vectoriales",
            "Suma, resta, escala vectores y explora combinaciones lineales.",
            "EcVectorialesCON.png",
        ),
        (
            "Ecuaciones matriciales",
            "Practica productos matriz-vector, propiedades y sistemas Ax=b.",
            "EcMatriciaIesCON.png",
        ),
        (
            "Sistemas e independencia",
            "Analiza sistemas lineales y relaciones entre vectores.",
            "EcLinealICON.png",
        ),
        ("Límites", "Evalúa límites y continuidad con el módulo de cálculo.", "LimitesICON.png"),
        (
            "Sistemas numéricos",
            "Convierte entre bases y entre números arábigos y romanos.",
            "SisNumICON.png",
        ),
        (
            "Determinantes y Factorización LU",
            "Calcula determinantes y resuelve sistemas Ax=b mediante LU.",
            "DeterminantesICON.png",
        ),
        (
            "Métodos Numéricos",
            "Explora métodos iterativos para aproximar raíces y analizar errores.",
            "metNumericosICON.png",
        ),
    ]

    def __init__(self, root, audio_manager, al_iniciar):
        self.root = root
        self.audio = audio_manager
        self.al_iniciar = al_iniciar
        self.var_musica = tk.BooleanVar(value=self.audio.musica_habilitada)
        self.var_efectos = tk.BooleanVar(value=self.audio.efectos_habilitados)
        self.var_volumen_musica = tk.IntVar(
            value=round(self.audio.volumen_musica * 100)
        )
        self.var_volumen_efectos = tk.IntVar(
            value=round(self.audio.volumen_efectos * 100)
        )
        self.controles_audio = {}
        self.controles_volumen = {}
        self._audio_en_foco = None
        self._volumen_arrastrado = None
        self.ventana_ayuda = None
        self._resize_job = None
        self._wipe_job = None
        self._salto_generation = 0
        self._wipe_activo = False
        self._glyph_photos = {}
        self._font_cache = {}
        carpeta_assets = Path(__file__).resolve().parents[1] / "assets"
        self.carpeta_fuentes = carpeta_assets / "fonts"
        self.fuentes_disponibles = [
            (familia, self.carpeta_fuentes / archivo)
            for familia, archivo in self.FUENTES
            if (self.carpeta_fuentes / archivo).is_file()
        ]
        self._registrar_fuentes()
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
        with Image.open(carpeta_assets / self.PROFESOR[1]) as avatar:
            self.profesor_original = avatar.convert("RGBA")

        self.frame = tk.Frame(root, bg="#141414")
        self.frame.pack(fill="both", expand=True)
        self._crear_contenido()
        self.audio.iniciar_musica_lobby()

    def _registrar_fuentes(self):
        self._fuentes_registradas = []
        if sys.platform != "win32" or not hasattr(ctypes, "windll"):
            return

        registrar = ctypes.windll.gdi32.AddFontResourceExW
        registrar.argtypes = [ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
        registrar.restype = ctypes.c_int
        for _, ruta in self.fuentes_disponibles:
            if registrar(str(ruta), 0x10, None):
                self._fuentes_registradas.append(str(ruta))
            else:
                print(f"Advertencia: Windows no pudo registrar la fuente {ruta.name}.")

        faltantes = {
            archivo for _, archivo in self.FUENTES
        } - {ruta.name for _, ruta in self.fuentes_disponibles}
        for archivo in sorted(faltantes):
            print(f"Advertencia: No se encontró la fuente local {archivo}.")

    def _liberar_fuentes(self):
        if not self._fuentes_registradas or not hasattr(ctypes, "windll"):
            return
        quitar = ctypes.windll.gdi32.RemoveFontResourceExW
        quitar.argtypes = [ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
        quitar.restype = ctypes.c_int
        for ruta in self._fuentes_registradas:
            if not quitar(ruta, 0x10, None):
                print(f"Advertencia: Windows no pudo liberar la fuente {Path(ruta).name}.")
        self._fuentes_registradas.clear()

    def _al_destruir_frame(self, event):
        if event.widget is self.frame:
            for atributo in ("_wipe_job", "_resize_job"):
                trabajo = getattr(self, atributo, None)
                if trabajo is not None:
                    try:
                        self.root.after_cancel(trabajo)
                    except tk.TclError:
                        pass
                    setattr(self, atributo, None)
            self._liberar_fuentes()

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
        self.logo_photo = ImageTk.PhotoImage(
            Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        )
        self.logo_item = self.contenido.create_image(
            0, 0, image=self.logo_photo, anchor="center"
        )
        self.subtitulo_texto = "Calculadora educativa de Álgebra Lineal"
        self.subtitulo_tag = "ransom_subtitulo"
        self.facultad_item = self.contenido.create_text(
            0,
            0,
            text="Facultad de Ingeniería y\nArquitectura UAM",
            anchor="w",
            justify="left",
            fill="#f2f2f2",
            font=("Helvetica Now Display", 18, "bold"),
        )

        self.logo_uam_photo = ImageTk.PhotoImage(
            Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        )
        self.logo_uam_item = self.contenido.create_image(
            0, 0, image=self.logo_uam_photo, anchor="center"
        )
        self.profesor_photo = ImageTk.PhotoImage(
            Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        )
        self.profesor_fondo_item = self.contenido.create_rectangle(
            0,
            0,
            1,
            1,
            fill="#c8c8c8",
            outline="#fe0000",
            width=2,
        )
        self.profesor_item = self.contenido.create_image(
            0, 0, image=self.profesor_photo, anchor="center"
        )
        self.profesor_nombre_item = self.contenido.create_text(
            0,
            0,
            text=self.PROFESOR[0].replace(" Argüello ", "\nArgüello "),
            anchor="w",
            justify="left",
            fill=TEXTO_CLARO,
            font=("Helvetica Now Display", 12, "bold"),
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
                tags=("credito",),
            )
            avatar_photo = ImageTk.PhotoImage(
                Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            )
            avatar_item = self.contenido.create_image(
                0, 0, image=avatar_photo, anchor="center", tags=("credito",)
            )
            self.creditos.append(
                {
                    "nombre": nombre,
                    "original": imagen,
                    "background": fondo_avatar,
                    "photo": avatar_photo,
                    "image": avatar_item,
                    "tag": f"credito_nombre_{len(self.creditos)}",
                }
            )

        self._crear_control_audio("musica", "Música de fondo", self.var_musica, 20, 18)
        self._crear_control_audio("efectos", "Efectos de sonido", self.var_efectos, 20, 46)
        self._crear_control_volumen("musica", self.var_volumen_musica)
        self._crear_control_volumen("efectos", self.var_volumen_efectos)
        self.contenido.bind(
            "<B1-Motion>", self._ajustar_volumen_arrastrado, add="+"
        )
        self.contenido.bind(
            "<ButtonRelease-1>", self._terminar_ajuste_volumen, add="+"
        )

        self.opciones = []
        for indice, (texto, color) in enumerate(
            (("INICIAR", "#e3101b"), ("AYUDA", "#bfbfbf"))
        ):
            tag = f"menu_{indice}"
            fondo = self.contenido.create_polygon(
                0,
                0,
                0,
                0,
                0,
                0,
                fill=color,
                outline="",
                tags=(tag,),
            )
            barra_blanca = self.contenido.create_polygon(
                0, 0, 0, 0, 0, 0, 0, 0,
                fill="#ffffff",
                outline="",
                state="hidden",
                tags=(tag,),
            )
            barra_roja = self.contenido.create_polygon(
                0, 0, 0, 0, 0, 0, 0, 0,
                fill="#e3101b",
                outline="",
                state="hidden",
                tags=(tag,),
            )
            insignia = self.contenido.create_polygon(
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                fill="#ffffff",
                outline="",
                tags=(tag,),
            )
            numero = self.contenido.create_text(
                0,
                0,
                text=str(indice + 1),
                fill="#111111",
                font=("Archivo Black", 22),
                tags=(tag,),
            )
            texto_ransom = "".join(
                caracter.upper() if posicion % 2 == 0 else caracter.lower()
                for posicion, caracter in enumerate(texto)
            )
            etiqueta = f"{tag}_texto"
            self.opciones.append(
                {
                    "text": texto,
                    "ransom_text": texto_ransom,
                    "tag": tag,
                    "background": fondo,
                    "white_bar": barra_blanca,
                    "red_bar": barra_roja,
                    "badge": insignia,
                    "number": numero,
                    "label": etiqueta,
                    "base": (0, 0),
                    "size": (0, 0),
                    "color": color,
                    "hover_color": "#ff1724" if indice == 0 else "#858585",
                    "glyph_color": "#ffffff" if indice == 0 else "#111111",
                    "font_size": 22,
                }
            )
            self.contenido.tag_bind(
                tag,
                "<Enter>",
                lambda event, item=indice: self._al_entrar_opcion(event, item),
            )
            self.contenido.tag_bind(
                tag,
                "<Leave>",
                lambda event, item=indice: self._al_salir_opcion(event, item),
            )
            self.contenido.tag_bind(
                tag,
                "<Button-1>",
                lambda event, item=indice: self._al_hacer_clic(event, item),
            )

        self.wipe_items = [
            self.contenido.create_polygon(
                0, 0, 0, 0, 0, 0, 0, 0,
                fill=color,
                outline="",
                state="hidden",
                tags=("wipe",),
            )
            for color in ("#e3101b", "#ffffff")
        ]
        self.opcion_activa = None
        self.root.update_idletasks()
        self.contenido.bind("<Configure>", self._programar_reorganizacion)
        self.contenido.bind("<KeyPress>", self._al_presionar_tecla)
        self.contenido.focus_set()
        self.frame.bind("<Destroy>", self._al_destruir_frame, add="+")
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
        if ancho >= 200 and alto >= 200:
            self._reorganizar_contenido(ancho, alto)

    def _reorganizar_contenido(self, ancho, alto):
        self._resize_job = None
        ancho = self.contenido.winfo_width()
        alto = self.contenido.winfo_height()
        if ancho < 200 or alto < 200:
            return
        self.fondo_photo = ImageTk.PhotoImage(
            self._escalar_fondo_cover(self.fondo_original, ancho, alto)
        )
        self.contenido.itemconfigure(self.fondo_item, image=self.fondo_photo)
        self.contenido.coords(self.fondo_item, 0, 0)

        escala = min(ancho / 1192, alto / 812)
        lado_logo = max(1, int(min(ancho * 0.44, alto * 0.48)))
        self.logo_photo = ImageTk.PhotoImage(
            self.logo_original.resize(
                (lado_logo, lado_logo), Image.Resampling.LANCZOS
            )
        )
        self.contenido.itemconfigure(self.logo_item, image=self.logo_photo)
        self.contenido.coords(self.logo_item, ancho / 2, alto * 0.285)
        self._dibujar_texto_ransom(
            self.subtitulo_texto,
            ancho / 2,
            alto * 0.56,
            max(30, int(46 * escala)),
            self.subtitulo_tag,
            seed=1,
            max_width=ancho * 0.97,
        )

        ancho_boton = max(150, int(ancho * 0.38))
        alto_boton = max(46, int(alto * 0.098))
        separacion = ancho * 0.045
        desplazamiento = ancho_boton / 2 + separacion / 2
        centro_y_botones = alto * 0.695
        centros_botones = (
            ancho / 2 - desplazamiento,
            ancho / 2 + desplazamiento,
        )
        for indice, opcion in enumerate(self.opciones):
            centro_x = centros_botones[indice]
            opcion["base"] = (centro_x, centro_y_botones)
            opcion["size"] = (ancho_boton, alto_boton)
            opcion["font_size"] = max(26, int(42 * escala))
            self._ubicar_opcion(indice, 0)

        tamano_uam = max(80, min(140, int(110 * escala)))
        self.logo_uam_photo = ImageTk.PhotoImage(
            self.logo_uam_original.resize(
                (tamano_uam, tamano_uam), Image.Resampling.LANCZOS
            )
        )
        self.contenido.itemconfigure(self.logo_uam_item, image=self.logo_uam_photo)
        ancho_texto = min(440 * escala, ancho * 0.44)
        espacio_identidad = max(30, 38 * escala)
        ancho_bloque = tamano_uam + espacio_identidad + ancho_texto
        inicio_bloque = ancho * 0.74 - ancho_bloque / 2
        inicio_identidad = inicio_bloque + tamano_uam / 2
        x_texto_identidad = (
            inicio_identidad + tamano_uam / 2 + espacio_identidad
        )
        centro_y_identidad = alto * 0.79
        self.contenido.coords(
            self.logo_uam_item,
            inicio_identidad + max(8, ancho * 0.015),
            alto * 0.84 - max(10, alto * 0.025),
        )
        self.contenido.coords(
            self.facultad_item,
            x_texto_identidad,
            centro_y_identidad,
        )
        self.contenido.itemconfigure(
            self.facultad_item,
            width=ancho_texto,
            font=("Helvetica Now Display", max(15, int(23 * escala)), "bold"),
        )
        tamano_profesor = max(64, min(82, int(100 * escala)))
        self.profesor_photo = ImageTk.PhotoImage(
            self.profesor_original.resize(
                (tamano_profesor, tamano_profesor), Image.Resampling.LANCZOS
            )
        )
        x_logo_uam, y_logo_uam = self.contenido.coords(self.logo_uam_item)
        centro_x_profesor = x_logo_uam
        centro_y_profesor = (
            y_logo_uam
            + tamano_uam / 2
            + tamano_profesor / 2
            + max(8, 10 * escala)
        )
        mitad_profesor = tamano_profesor / 2 + 3
        self.contenido.coords(
            self.profesor_fondo_item,
            centro_x_profesor - mitad_profesor,
            centro_y_profesor - mitad_profesor,
            centro_x_profesor + mitad_profesor,
            centro_y_profesor + mitad_profesor,
        )
        self.contenido.itemconfigure(
            self.profesor_item, image=self.profesor_photo
        )
        self.contenido.coords(
            self.profesor_item, centro_x_profesor, centro_y_profesor
        )
        self.contenido.coords(
            self.profesor_nombre_item,
            x_texto_identidad,
            centro_y_profesor,
        )
        self.contenido.itemconfigure(
            self.profesor_nombre_item,
            width=ancho_texto,
            font=("Helvetica Now Display", max(15, int(21 * escala)), "bold"),
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
        y_avatar = alto * 0.87
        salto_escalonado = max(0, int(9 * escala))
        for indice, credito in enumerate(self.creditos):
            centro_x = (
                base_x_creditos
                + ancho_tarjeta_credito * (indice + 0.5)
            )
            centro_y = y_avatar - (salto_escalonado if indice % 2 else 0)
            mitad = tamano_avatar / 2 + 3
            self.contenido.coords(
                credito["background"],
                centro_x - mitad,
                centro_y - mitad,
                centro_x + mitad,
                centro_y + mitad,
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
            self.contenido.coords(credito["image"], centro_x, centro_y)
            nombre_y = centro_y + tamano_avatar / 2 + max(13, int(17 * escala))
            self._dibujar_texto_ransom(
                credito["nombre"].upper(),
                centro_x,
                nombre_y,
                max(9, int(12 * escala)),
                credito["tag"],
                seed=100 + indice,
                font_family="Anton",
                box_mode="none",
                max_width=ancho_tarjeta_credito - 4,
            )
        self._posicionar_controles_audio(ancho, alto)
    def _fuente_pillow(self, archivo, tamano):
        clave = (str(archivo), tamano)
        if clave not in self._font_cache:
            self._font_cache[clave] = ImageFont.truetype(str(archivo), tamano)
        return self._font_cache[clave]

    def _dibujar_texto_ransom(
        self,
        texto,
        x,
        y,
        tamano,
        tag,
        seed,
        anchor_left=False,
        line_spacing=None,
        max_width=None,
        font_family=None,
        box_mode="menu",
        text_color=None,
    ):
        self.contenido.delete(tag)
        self._glyph_photos[tag] = []
        line_spacing = line_spacing or int(tamano * 1.4)
        lineas = texto.splitlines() or [""]
        alto_total = line_spacing * (len(lineas) - 1)
        rng = random.Random(seed)
        familias = (
            [
                (
                    font_family,
                    next(
                        (
                            ruta for familia, ruta in self.fuentes_disponibles
                            if familia == font_family
                        ),
                        None,
                    ),
                )
            ]
            if font_family is not None
            else self.fuentes_disponibles
        )
        if not familias:
            familias = [("Arial", None)]

        for indice_linea, linea in enumerate(lineas):
            sprites = []
            ancho_linea = 0
            fuente_previa = None
            caja_previa = None
            for caracter in linea:
                if caracter.isspace():
                    ancho_linea += max(4, int(tamano * 0.34))
                    continue
                opciones_fuente = [
                    fuente for fuente in familias
                    if fuente[0] != fuente_previa
                ] or familias
                familia, ruta = rng.choice(opciones_fuente)
                fuente_previa = familia
                escala_letra = rng.uniform(0.88, 1.12)
                tamano_letra = max(7, int(tamano * escala_letra))
                if ruta is not None:
                    fuente = self._fuente_pillow(ruta, tamano_letra)
                else:
                    fuente = ImageFont.load_default(size=tamano_letra)
                caja_texto = rng.choice(("white", "dark", "red"))
                if box_mode == "none":
                    caja_texto = "none"
                elif box_mode == "menu" and caja_texto == caja_previa:
                    caja_texto = "white" if caja_texto != "white" else "red"
                caja_previa = caja_texto

                padding_x = (
                    max(2, int(tamano_letra * 0.12))
                    if caja_texto != "none"
                    else 0
                )
                padding_y = max(1, int(tamano * 0.06)) if caja_texto != "none" else 0
                caja = fuente.getbbox(caracter)
                ancho_glyph = max(1, caja[2] - caja[0])
                alto_glyph = max(1, caja[3] - caja[1])
                tile = Image.new(
                    "RGBA",
                    (
                        ancho_glyph + padding_x * 2,
                        alto_glyph + padding_y * 2,
                    ),
                    (0, 0, 0, 0),
                )
                draw = ImageDraw.Draw(tile)
                if caja_texto == "white":
                    color_fondo, color_texto = "#f2f2f2", "#111111"
                elif caja_texto == "dark":
                    color_fondo, color_texto = "#252525", "#ffffff"
                elif caja_texto == "red":
                    color_fondo, color_texto = "#e3101b", "#ffffff"
                else:
                    color_fondo = None
                    color_texto = text_color or "#eeeeee"
                if text_color is not None:
                    color_texto = text_color
                if color_fondo is not None:
                    draw.rectangle(
                        (0, 0, tile.width - 1, tile.height - 1),
                        fill=color_fondo,
                        outline="#ffffff" if caja_texto == "dark" else None,
                    )
                draw.text(
                    (padding_x - caja[0], padding_y - caja[1]),
                    caracter,
                    font=fuente,
                    fill=color_texto,
                )
                rotacion = rng.uniform(-10, 10)
                sprite = tile.rotate(
                    rotacion,
                    resample=Image.Resampling.BICUBIC,
                    expand=True,
                )
                avance = sprite.width + max(2, int(tamano * 0.12))
                sprites.append((sprite, ancho_linea, avance, rng.uniform(-2, 2)))
                ancho_linea += avance

            if max_width is not None and ancho_linea > max_width and sprites:
                factor = max_width / ancho_linea
                sprites = [
                    (
                        sprite.resize(
                            (
                                max(1, int(sprite.width * factor)),
                                max(1, int(sprite.height * factor)),
                            ),
                            Image.Resampling.LANCZOS,
                        ),
                        int(offset * factor),
                        max(1, int(advance * factor)),
                        y_offset,
                    )
                    for sprite, offset, advance, y_offset in sprites
                ]
                ancho_linea = max_width

            inicio_x = x if anchor_left else x - ancho_linea / 2
            centro_y_linea = y - alto_total / 2 + indice_linea * line_spacing
            for sprite, offset, _, y_offset in sprites:
                photo = ImageTk.PhotoImage(sprite)
                self._glyph_photos[tag].append(photo)
                self.contenido.create_image(
                    inicio_x + offset + sprite.width / 2,
                    centro_y_linea + y_offset,
                    image=photo,
                    anchor="center",
                    tags=(tag,),
                )

    def _ubicar_opcion(self, indice, desplazamiento):
        opcion = self.opciones[indice]
        centro_x, centro_y = opcion["base"]
        ancho, alto = opcion["size"]
        centro_x += desplazamiento
        x1, x2 = centro_x - ancho / 2, centro_x + ancho / 2
        y1, y2 = centro_y - alto / 2, centro_y + alto / 2
        insignia_ancho = min(alto * 1.15, ancho * 0.2)
        inclinacion = min(alto * 0.36, ancho * 0.08)
        trapecio = (
            x1 + insignia_ancho * 0.52, y1 + alto * 0.08,
            x2, y1,
            x2 - inclinacion, y2 - alto * 0.05,
            x1 + insignia_ancho * 0.32, y2,
        )
        respaldo_blanco = (
            x1 + insignia_ancho * 0.28, y1 - alto * 0.14,
            x2 + inclinacion * 0.55, y1 - alto * 0.08,
            x2 + inclinacion * 0.25, y2 + alto * 0.2,
            x1 - insignia_ancho * 0.18, y2 + alto * 0.13,
        )
        detalle_rojo = (
            x1 + insignia_ancho * 0.32, y1 - alto * 0.04,
            x2 + inclinacion * 0.35, y1 + alto * 0.02,
            x2 + inclinacion * 0.1, y1 + alto * 0.12,
            x1 + insignia_ancho * 0.25, y1 + alto * 0.08,
        )
        placa = (
            x1, y1 + alto * 0.12,
            x1 + insignia_ancho * 0.88, y1 + alto * 0.02,
            x1 + insignia_ancho, y2 - alto * 0.15,
            x1 + insignia_ancho * 0.12, y2,
            x1 - alto * 0.04, centro_y,
        )
        self.contenido.coords(opcion["background"], *trapecio)
        self.contenido.coords(opcion["white_bar"], *respaldo_blanco)
        self.contenido.coords(opcion["red_bar"], *detalle_rojo)
        self.contenido.coords(opcion["badge"], *placa)
        self.contenido.coords(
            opcion["number"], x1 + insignia_ancho * 0.48, centro_y
        )
        texto_x = x1 + insignia_ancho + (x2 - x1 - insignia_ancho) / 2
        self._dibujar_texto_ransom(
            opcion["ransom_text"],
            texto_x,
            centro_y,
            opcion["font_size"],
            opcion["label"],
            seed=500 + indice,
            max_width=max(1, x2 - x1 - insignia_ancho - alto * 0.22),
            box_mode="none",
            text_color=opcion["glyph_color"],
        )
        self.contenido.tag_lower(opcion["white_bar"], opcion["background"])
        self.contenido.tag_lower(opcion["red_bar"], opcion["background"])

    def _al_entrar_opcion(self, event, indice):
        if self._wipe_activo or event.widget is not self.contenido:
            return
        if indice != self.opcion_activa:
            self.audio.reproducir_efecto("cursor")
            self._seleccionar_opcion(indice)

    def _al_salir_opcion(self, event, indice):
        if self._wipe_activo:
            return
        self.root.after_idle(
            lambda: self._confirmar_salida_opcion(indice, event.x, event.y)
        )

    def _confirmar_salida_opcion(self, indice, x, y):
        if self._wipe_activo or self.opcion_activa != indice:
            return
        items = self.contenido.find_overlapping(x, y, x, y)
        tags = {
            tag
            for item in items
            for tag in self.contenido.gettags(item)
        }
        if self.opciones[indice]["tag"] not in tags:
            self._seleccionar_opcion(None)

    def _seleccionar_opcion(self, indice):
        if indice == self.opcion_activa:
            return
        self._salto_generation += 1
        generation = self._salto_generation
        anterior = self.opcion_activa
        self.opcion_activa = indice
        if anterior is not None:
            self.contenido.itemconfigure(
                self.opciones[anterior]["white_bar"], state="hidden"
            )
            self.contenido.itemconfigure(
                self.opciones[anterior]["red_bar"], state="hidden"
            )
            self.contenido.itemconfigure(
                self.opciones[anterior]["background"],
                fill=self.opciones[anterior]["color"],
            )
            self.contenido.itemconfigure(
                self.opciones[anterior]["badge"], fill="#ffffff"
            )
            self.contenido.itemconfigure(
                self.opciones[anterior]["number"], fill="#111111"
            )
            self.opciones[anterior]["glyph_color"] = (
                "#ffffff" if anterior == 0 else "#111111"
            )
            self._ubicar_opcion(anterior, 0)
        if indice is not None:
            opcion = self.opciones[indice]
            self.contenido.itemconfigure(opcion["white_bar"], state="normal")
            self.contenido.itemconfigure(opcion["red_bar"], state="normal")
            self.contenido.itemconfigure(
                opcion["background"], fill=opcion["hover_color"]
            )
            self.contenido.itemconfigure(opcion["badge"], fill="#e3101b"            )
            self.contenido.itemconfigure(opcion["number"], fill="#ffffff")
            opcion["glyph_color"] = "#ffffff"
            self._animar_salto(indice, generation)

    def _animar_salto(self, indice, generation):
        if generation != self._salto_generation or indice != self.opcion_activa:
            return
        self._ubicar_opcion(indice, 15)

    def _al_hacer_clic(self, event, indice=None):
        if self._wipe_activo:
            return
        if indice is None:
            items = self.contenido.find_overlapping(
                event.x, event.y, event.x, event.y
            )
            tags = {
                tag
                for item in items
                for tag in self.contenido.gettags(item)
            }
            indice = next(
                (
                    i
                    for i, opcion in enumerate(self.opciones)
                    if opcion["tag"] in tags
                ),
                None,
            )
        if indice is None:
            return
        self._seleccionar_opcion(indice)
        if indice == 0:
            self._iniciar_con_wipe()
        else:
            self.mostrar_ayuda()

    def _al_presionar_tecla(self, event):
        if self._wipe_activo:
            return "break"
        controles_audio = (
            "musica",
            "volumen_musica",
            "efectos",
            "volumen_efectos",
        )
        if event.keysym == "Tab" and controles_audio:
            if self._audio_en_foco is None:
                self._audio_en_foco = controles_audio[0]
            elif self._audio_en_foco == controles_audio[-1]:
                self._audio_en_foco = None
            else:
                indice = controles_audio.index(self._audio_en_foco)
                self._audio_en_foco = controles_audio[indice + 1]
            self._actualizar_indicadores_foco_audio()
            return "break"
        if (
            self._audio_en_foco in ("volumen_musica", "volumen_efectos")
            and event.keysym in ("Left", "Right")
        ):
            clave = self._audio_en_foco.removeprefix("volumen_")
            incremento = 5 if event.keysym == "Right" else -5
            actual = self.controles_volumen[clave]["variable"].get()
            self._establecer_volumen(clave, actual + incremento)
            return "break"
        if (
            self._audio_en_foco is not None
            and event.keysym in ("Return", "KP_Enter", "space")
        ):
            if self._audio_en_foco in self.controles_audio:
                comando = (
                    self._alternar_musica
                    if self._audio_en_foco == "musica"
                    else self._alternar_efectos
                )
                comando()
                return "break"
        if event.keysym in ("Down", "Up"):
            actual = self.opcion_activa if self.opcion_activa is not None else -1
            desplazamiento = 1 if event.keysym == "Down" else -1
            siguiente = (actual + desplazamiento) % len(self.opciones)
            self._seleccionar_opcion(siguiente)
            return "break"
        if event.keysym in ("1", "2"):
            indice = int(event.keysym) - 1
            self._seleccionar_opcion(indice)
            if indice == 0:
                self._iniciar_con_wipe()
            else:
                self.mostrar_ayuda()
            return "break"
        if event.keysym in ("Return", "KP_Enter") and self.opcion_activa is not None:
            if self.opcion_activa == 0:
                self._iniciar_con_wipe()
            else:
                self.mostrar_ayuda()
            return "break"
        if event.keysym == "Escape":
            self._audio_en_foco = None
            self._actualizar_indicadores_foco_audio()
            self._seleccionar_opcion(None)
            return "break"
        return None

    def _actualizar_indicadores_foco_audio(self):
        for clave in self.controles_audio:
            self._actualizar_control_audio(clave)
        for clave in self.controles_volumen:
            self._actualizar_control_volumen(clave)

    def _iniciar_con_wipe(self):
        if self._wipe_activo:
            return
        self._wipe_activo = True
        self.audio.reproducir_efecto("interfaces")
        self._animar_wipe(0)

    def _animar_wipe(self, paso):
        ancho = max(1, self.contenido.winfo_width())
        alto = max(1, self.contenido.winfo_height())
        pasos_totales = 28
        progreso = paso / pasos_totales
        inicio = -1.8 * ancho + 3.6 * ancho * progreso
        ancho_banda = 1.3 * ancho
        inclinacion = 0.12 * ancho
        banda_roja = (
            inicio, -alto * 0.15,
            inicio + ancho_banda, -alto * 0.15,
            inicio + ancho_banda - inclinacion, alto * 1.15,
            inicio - inclinacion, alto * 1.15,
        )
        inicio_blanco = inicio + 0.95 * ancho
        banda_blanca = (
            inicio_blanco, -alto * 0.15,
            inicio_blanco + ancho_banda, -alto * 0.15,
            inicio_blanco + ancho_banda - inclinacion, alto * 1.15,
            inicio_blanco - inclinacion, alto * 1.15,
        )
        for item, puntos in zip(self.wipe_items, (banda_roja, banda_blanca)):
            self.contenido.coords(item, *puntos)
            self.contenido.itemconfigure(item, state="normal")
            self.contenido.tag_raise(item)
        # Se guarda el identificador para cancelarlo si el inicio se destruye
        # (por ejemplo, al cerrar la aplicación a mitad de la transición).
        if paso >= 14:
            self._wipe_job = self.root.after(1, self._iniciar)
        elif paso < pasos_totales:
            self._wipe_job = self.root.after(14, lambda: self._animar_wipe(paso + 1))

    def _alternar_musica(self):
        self.var_musica.set(not self.var_musica.get())
        self.audio.establecer_musica_habilitada(self.var_musica.get())
        preferencias.guardar(musica_habilitada=bool(self.var_musica.get()))
        self._actualizar_control_audio("musica")

    def _alternar_efectos(self):
        self.var_efectos.set(not self.var_efectos.get())
        self.audio.establecer_efectos_habilitados(self.var_efectos.get())
        preferencias.guardar(efectos_habilitados=bool(self.var_efectos.get()))
        self._actualizar_control_audio("efectos")

    def _crear_control_audio(self, clave, texto, variable, x, y):
        etiqueta = f"control_audio_{clave}"
        pista = self.contenido.create_oval(
            x, y, x + 32, y + 18,
            fill="#4a4a4a",
            outline="#ffffff",
            width=1,
            tags=(etiqueta,),
        )
        perilla = self.contenido.create_oval(
            x + 2, y + 2, x + 16, y + 16,
            fill="#ffffff",
            outline="#111111",
            tags=(etiqueta,),
        )
        texto_item = self.contenido.create_text(
            x + 40,
            y + 9,
            text=texto,
            anchor="w",
            fill=TEXTO_CLARO,
            font=("Segoe UI", 11, "bold"),
            tags=(etiqueta,),
        )
        self.controles_audio[clave] = {
            "clave": clave,
            "variable": variable,
            "pista": pista,
            "perilla": perilla,
            "texto": texto_item,
            "x": x,
            "y": y,
        }
        comando = self._alternar_musica if clave == "musica" else self._alternar_efectos
        self.contenido.tag_bind(
            etiqueta,
            "<Button-1>",
            lambda _event: (self.contenido.focus_set(), comando()),
        )
        self.contenido.tag_bind(
            etiqueta, "<Enter>", lambda _event: self.contenido.configure(cursor="hand2")
        )
        self.contenido.tag_bind(
            etiqueta, "<Leave>", lambda _event: self.contenido.configure(cursor="")
        )
        self._actualizar_control_audio(clave)

    def _crear_control_volumen(self, clave, variable):
        etiqueta = f"control_volumen_{clave}"
        pista = self.contenido.create_line(
            0, 0, 180, 0,
            fill="#777777",
            width=5,
            capstyle=tk.ROUND,
            tags=(etiqueta,),
        )
        nivel = self.contenido.create_line(
            0, 0, 0, 0,
            fill=ACENTO,
            width=5,
            capstyle=tk.ROUND,
            tags=(etiqueta,),
        )
        perilla = self.contenido.create_oval(
            0, 0, 12, 12,
            fill="#ffffff",
            outline="#111111",
            width=1,
            tags=(etiqueta,),
        )
        valor = self.contenido.create_text(
            0,
            0,
            anchor="e",
            fill=TEXTO_CLARO,
            font=("Segoe UI", 10, "bold"),
            tags=(etiqueta,),
        )
        self.controles_volumen[clave] = {
            "variable": variable,
            "pista": pista,
            "nivel": nivel,
            "perilla": perilla,
            "valor": valor,
            "x": 0,
            "y": 0,
            "ancho": 180,
        }
        self.contenido.tag_bind(
            etiqueta,
            "<Button-1>",
            lambda evento, nombre=clave: self._iniciar_ajuste_volumen(
                nombre, evento
            ),
        )
        self.contenido.tag_bind(
            etiqueta, "<Enter>", lambda _evento: self.contenido.configure(cursor="hand2")
        )
        self.contenido.tag_bind(
            etiqueta, "<Leave>", lambda _evento: self.contenido.configure(cursor="")
        )
        self._actualizar_control_volumen(clave)

    def _posicionar_controles_audio(self, ancho, alto):
        x = max(20, ancho - 235)
        y_musica = int(alto * 0.10)
        y_efectos = int(alto * 0.174)
        for clave, y in (("musica", y_musica), ("efectos", y_efectos)):
            control = self.controles_audio[clave]
            control["x"], control["y"] = x, y
            self.contenido.coords(control["pista"], x, y, x + 32, y + 18)
            self.contenido.coords(
                control["perilla"],
                x + 2,
                y + 2,
                x + 16,
                y + 16,
            )
            self.contenido.coords(control["texto"], x + 40, y + 9)

        for clave, y in (
            ("musica", y_musica + 27),
            ("efectos", y_efectos + 27),
        ):
            volumen = self.controles_volumen[clave]
            volumen["x"] = x + 2
            volumen["y"] = y
            volumen["ancho"] = 176
            self._actualizar_control_volumen(clave)

    def _iniciar_ajuste_volumen(self, clave, evento):
        self._volumen_arrastrado = clave
        self._audio_en_foco = f"volumen_{clave}"
        self._actualizar_volumen_desde_x(clave, evento.x, persistir=False)
        return "break"

    def _ajustar_volumen_arrastrado(self, evento):
        if self._volumen_arrastrado is None:
            return
        self._actualizar_volumen_desde_x(
            self._volumen_arrastrado, evento.x, persistir=False
        )

    def _terminar_ajuste_volumen(self, _evento):
        if self._volumen_arrastrado is not None:
            clave = self._volumen_arrastrado
            campo = f"volumen_{clave}"
            valor = self.controles_volumen[clave]["variable"].get()
            preferencias.guardar(**{campo: valor})
        self._volumen_arrastrado = None

    def _actualizar_volumen_desde_x(self, clave, x, persistir=True):
        control = self.controles_volumen[clave]
        proporcion = (x - control["x"]) / control["ancho"]
        valor = max(0, min(100, round(proporcion * 100)))
        self._establecer_volumen(clave, valor, persistir)

    def _establecer_volumen(self, clave, valor, persistir=True):
        valor = max(0, min(100, int(valor)))
        control = self.controles_volumen[clave]
        control["variable"].set(valor)
        if clave == "musica":
            self.audio.establecer_volumen_musica(valor / 100)
            if persistir:
                preferencias.guardar(volumen_musica=valor)
        else:
            self.audio.establecer_volumen_efectos(valor / 100)
            if persistir:
                preferencias.guardar(volumen_efectos=valor)
        self._actualizar_control_volumen(clave)

    def _actualizar_control_volumen(self, clave):
        control = self.controles_volumen[clave]
        valor = control["variable"].get()
        inicio = control["x"]
        y = control["y"]
        fin = inicio + control["ancho"] * valor / 100
        self.contenido.coords(
            control["pista"], inicio, y, inicio + control["ancho"], y
        )
        self.contenido.coords(control["nivel"], inicio, y, fin, y)
        self.contenido.coords(
            control["perilla"], fin - 6, y - 6, fin + 6, y + 6
        )
        self.contenido.coords(
            control["valor"], inicio + control["ancho"] + 28, y
        )
        self.contenido.itemconfigure(control["valor"], text=f"{valor}%")
        seleccionado = self._audio_en_foco == f"volumen_{clave}"
        self.contenido.itemconfigure(
            control["perilla"],
            outline=ACENTO if seleccionado else "#111111",
            width=2 if seleccionado else 1,
        )

    def _actualizar_control_audio(self, clave):
        control = self.controles_audio[clave]
        habilitado = control["variable"].get()
        x, y = control["x"], control["y"]
        self.contenido.itemconfigure(
            control["pista"],
            fill=ACENTO if habilitado else "#4a4a4a",
            outline=ACENTO if self._audio_en_foco == clave else "#ffffff",
            width=2 if self._audio_en_foco == clave else 1,
        )
        desplazamiento = 16 if habilitado else 2
        self.contenido.coords(
            control["perilla"],
            x + desplazamiento,
            y + 2,
            x + desplazamiento + 14,
            y + 16,
        )

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

        ventana._iconos_modulos = []
        carpeta_assets = Path(__file__).resolve().parents[1] / "assets"
        for nombre, descripcion, archivo_icono in self.MODULOS:
            modulo = ctk.CTkFrame(contenido, **estilo_panel_contenedor())
            modulo.pack(fill="x", padx=10, pady=6)
            modulo.grid_columnconfigure(1, weight=1)
            marco_icono = ctk.CTkFrame(
                modulo,
                width=110,
                height=76,
                fg_color="#202020",
                corner_radius=0,
                border_width=1,
                border_color=ACENTO,
            )
            marco_icono.grid(row=0, column=0, rowspan=2, padx=12, pady=10)
            marco_icono.grid_propagate(False)
            ruta_icono = carpeta_assets / archivo_icono
            with Image.open(ruta_icono) as imagen:
                imagen_icono = ImageOps.contain(
                    imagen.convert("RGBA"),
                    (94, 68),
                    method=Image.Resampling.LANCZOS,
                )
            foto_icono = ctk.CTkImage(
                light_image=imagen_icono,
                dark_image=imagen_icono,
                size=imagen_icono.size,
            )
            ventana._iconos_modulos.append(foto_icono)
            ctk.CTkLabel(
                marco_icono,
                image=foto_icono,
                text="",
                fg_color="#202020",
            ).pack(expand=True)
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
            text="    ·    ".join(nombre for nombre, _archivo in self.INTEGRANTES),
            text_color=TEXTO_CLARO,
            wraplength=850,
        ).pack(anchor="w", padx=14, pady=(0, 12))

        ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)
