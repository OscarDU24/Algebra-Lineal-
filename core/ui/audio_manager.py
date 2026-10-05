"""Reproducción opcional de música y efectos breves para la interfaz."""

from pathlib import Path
import time
import tkinter as tk


class AudioManager:
    """Centraliza el audio; si pygame o el dispositivo fallan, la app sigue en silencio."""

    EFECTOS = {
        "cursor": "CursorSelect.mp3",
        "calcular": "CalcularAct.mp3",
        "limpiar": "LimpiarAct.mp3",
        "error": "ErrorDT.mp3",
    }
    CONTROLES_INTERACTIVOS = {
        "CTkButton",
        "CTkCheckBox",
        "CTkComboBox",
        "CTkSegmentedButton",
        "CTkSwitch",
    }

    def __init__(self, carpeta_audio=None):
        self.carpeta_audio = carpeta_audio or (
            Path(__file__).resolve().parents[1] / "assets" / "SoundEffects"
        )
        self.musica_habilitada = True
        self.en_lobby = False
        self.disponible = False
        self._pygame = None
        self._efectos = {}
        self._ultimo_hover = 0.0
        self._ultimo_control_hover = None

        try:
            import pygame

            pygame.mixer.init()
            self._pygame = pygame
            self.disponible = True
            self._cargar_efectos()
        except Exception as error:
            print(f"Audio desactivado: no se pudo iniciar pygame.mixer ({error}).")

    def _cargar_efectos(self):
        for nombre, archivo in self.EFECTOS.items():
            ruta = self.carpeta_audio / archivo
            if not ruta.is_file():
                continue
            try:
                self._efectos[nombre] = self._pygame.mixer.Sound(str(ruta))
            except Exception as error:
                print(f"Audio: no se pudo cargar {archivo} ({error}).")

    def iniciar_musica_lobby(self):
        """Inicia o reinicia la música mientras se muestra portada o selector."""
        self.en_lobby = True
        if not self.disponible or not self.musica_habilitada:
            return

        ruta = self.carpeta_audio / "BackgroundMusic.mp3"
        if not ruta.is_file():
            return
        try:
            self._pygame.mixer.music.stop()
            self._pygame.mixer.music.load(str(ruta))
            self._pygame.mixer.music.play(-1)
        except Exception as error:
            print(f"Audio: no se pudo reproducir BackgroundMusic.mp3 ({error}).")

    def detener_musica_lobby(self):
        self.en_lobby = False
        if self.disponible:
            try:
                self._pygame.mixer.music.stop()
            except Exception:
                pass

    def establecer_musica_habilitada(self, habilitada):
        self.musica_habilitada = bool(habilitada)
        if self.en_lobby:
            if self.musica_habilitada:
                self.iniciar_musica_lobby()
            else:
                self.detener_musica_lobby()
                self.en_lobby = True

    def alternar_musica(self):
        self.establecer_musica_habilitada(not self.musica_habilitada)
        return self.musica_habilitada

    def reproducir_efecto(self, nombre):
        if not self.disponible:
            return
        sonido = self._efectos.get(nombre)
        if sonido is None:
            return
        if nombre == "cursor":
            ahora = time.monotonic()
            if ahora - self._ultimo_hover < 0.14:
                return
            self._ultimo_hover = ahora
        try:
            sonido.play()
        except Exception:
            pass

    def _control_interactivo(self, widget, raiz):
        actual = widget
        boton_encontrado = None
        while actual is not None:
            nombre_clase = actual.__class__.__name__
            if nombre_clase in {"CTkComboBox", "CTkSegmentedButton"}:
                return actual
            if (
                nombre_clase in self.CONTROLES_INTERACTIVOS
                or isinstance(actual, (tk.Button, tk.Checkbutton))
            ):
                if boton_encontrado is None:
                    boton_encontrado = actual
            if actual is raiz:
                break
            actual = getattr(actual, "master", None)
        return boton_encontrado

    def instalar_sonidos_interfaz(self, raiz):
        """Añade sonidos globales a botones y selectores sin sustituir sus comandos."""
        def al_entrar(event):
            control = self._control_interactivo(event.widget, raiz)
            if control is None:
                return
            identidad = id(control)
            if identidad != self._ultimo_control_hover:
                self._ultimo_control_hover = identidad
                self.reproducir_efecto("cursor")

        def al_salir(event):
            control = self._control_interactivo(event.widget, raiz)
            if control is not None and id(control) == self._ultimo_control_hover:
                self._ultimo_control_hover = None

        def al_pulsar(event):
            control = self._control_interactivo(event.widget, raiz)
            if control is None:
                return
            if control.__class__.__name__ in {"CTkComboBox", "CTkSegmentedButton"}:
                self.reproducir_efecto("cursor")
                return
            try:
                texto = str(control.cget("text")).casefold()
            except Exception:
                texto = ""
            if "limpiar" in texto:
                self.reproducir_efecto("limpiar")
            elif any(palabra in texto for palabra in ("calcular", "resolver", "convertir", "iniciar")):
                self.reproducir_efecto("calcular")
            else:
                self.reproducir_efecto("calcular")

        raiz.bind_all("<Enter>", al_entrar, add="+")
        raiz.bind_all("<Leave>", al_salir, add="+")
        raiz.bind_all("<ButtonPress-1>", al_pulsar, add="+")

    def cerrar(self):
        self.detener_musica_lobby()
        if self.disponible:
            try:
                self._pygame.mixer.quit()
            except Exception:
                pass
            self.disponible = False


def reproducir_sonido_error(widget, mensaje):
    """Reproduce el aviso sonoro cuando una vista presenta un error al usuario."""
    primera_linea = str(mensaje).lstrip().splitlines()[0].casefold() if str(mensaje).strip() else ""
    if not primera_linea.startswith(("error", "advertencia")) and " error" not in primera_linea:
        return

    actual = widget
    while actual is not None:
        audio_manager = getattr(actual, "audio_manager", None)
        if audio_manager is not None:
            audio_manager.reproducir_efecto("error")
            return
        actual = getattr(actual, "master", None)
