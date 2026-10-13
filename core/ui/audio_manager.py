"""Reproducción opcional de música y efectos breves para la interfaz."""

from pathlib import Path
import time
import tkinter as tk


class AudioManager:
    """Centraliza el audio; si pygame o el dispositivo fallan, la app sigue en silencio."""

    EFECTOS = {
        "cursor": "CursorSelect.mp3",
        "seleccionar": "ChoiceSelect.mp3",
        "calcular": "CalcularAct.mp3",
        "limpiar": "LimpiarAct.mp3",
        "interfaces": "InterfacesSwitch.mp3",
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
        # Localiza la carpeta assets/SoundEffects un nivel arriba del archivo actual
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
        self._hover_pendiente = None

        try:
            import pygame

            # Se inicializa con buffer bajo (512) para que los clics suenen de inmediato
            pygame.mixer.init(buffer=512)
            self._pygame = pygame
            self.disponible = True
            self._cargar_efectos()
        except Exception as error:
            print(f"Audio desactivado: no se pudo iniciar pygame.mixer ({error}).")

    def _cargar_efectos(self):
        """Carga y descomprime los efectos de sonido directamente en la memoria RAM."""
        for nombre, archivo in self.EFECTOS.items():
            ruta = self.carpeta_audio / archivo
            if not ruta.is_file():
                continue
            try:
                self._efectos[nombre] = self._pygame.mixer.Sound(str(ruta))
            except Exception as error:
                print(f"Audio: no se pudo cargar {archivo} ({error}).")

    def iniciar_musica_lobby(self):
        """Inicia la música de fondo transmitiéndola desde el disco para ahorrar RAM."""
        self.en_lobby = True
        if not self.disponible or not self.musica_habilitada:
            return

        ruta = self.carpeta_audio / "BackgroundMusic.mp3"
        if not ruta.is_file():
            return
        try:
            self._pygame.mixer.music.stop()
            self._pygame.mixer.music.load(str(ruta))
            self._pygame.mixer.music.play(-1)  # -1 reproduce en bucle infinito
        except Exception as error:
            print(f"Audio: no se pudo reproducir BackgroundMusic.mp3 ({error}).")

    def detener_musica_lobby(self):
        """Detiene la música de fondo."""
        self.en_lobby = False
        if self.disponible:
            try:
                self._pygame.mixer.music.stop()
            except Exception:
                pass

    def establecer_musica_habilitada(self, habilitada):
        """Activa o desactiva la música según las preferencias del usuario."""
        self.musica_habilitada = bool(habilitada)
        if self.en_lobby:
            if self.musica_habilitada:
                self.iniciar_musica_lobby()
            else:
                self.detener_musica_lobby()
                self.en_lobby = True

    def alternar_musica(self):
        """Método rápido para encender/apagar la música."""
        self.establecer_musica_habilitada(not self.musica_habilitada)
        return self.musica_habilitada

    def reproducir_efecto(self, nombre):
        """Reproduce un efecto con un filtro anti-spam para el sonido del cursor."""
        if not self.disponible:
            return
        sonido = self._efectos.get(nombre)
        if sonido is None:
            return
        if nombre == "cursor":
            ahora = time.monotonic()
            if ahora - self._ultimo_hover < 0.14:  # Cooldown de 140ms
                return
            self._ultimo_hover = ahora
        try:
            sonido.play()
        except Exception:
            pass

    def _control_interactivo(self, widget, raiz):
        """Rastrea el árbol de componentes (widgets) hacia arriba para identificar el control real."""
        actual = widget
        boton_encontrado = None
        while actual is not None:
            nombre_clase = actual.__class__.__name__
            if hasattr(actual, "_heyalg_efecto_clic"):
                return actual
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

    def registrar_control_sonido(self, widget, efecto_clic):
        """Registra controles personalizados que no son botones Tk/CustomTkinter."""
        widget._heyalg_efecto_clic = efecto_clic

    def _actualizar_control_bajo_cursor(self, raiz):
        self._hover_pendiente = None
        if not raiz.winfo_exists():
            return

        x, y = raiz.winfo_pointerxy()
        widget = raiz.winfo_containing(x, y)
        control = self._control_interactivo(widget, raiz) if widget is not None else None
        identidad = id(control) if control is not None else None
        if identidad == self._ultimo_control_hover:
            return

        self._ultimo_control_hover = identidad
        if control is not None:
            self.reproducir_efecto("cursor")

    def instalar_sonidos_interfaz(self, raiz):
        """Inyecta los sonidos globalmente en la ventana sin romper los comandos existentes."""
        def programar_actualizacion_hover(_event):
            if self._hover_pendiente is not None:
                raiz.after_cancel(self._hover_pendiente)
            self._hover_pendiente = raiz.after_idle(
                lambda: self._actualizar_control_bajo_cursor(raiz)
            )

        def al_pulsar(event):
            control = self._control_interactivo(event.widget, raiz)
            if control is None:
                return
            efecto_registrado = getattr(control, "_heyalg_efecto_clic", None)
            if efecto_registrado is not None:
                self.reproducir_efecto(efecto_registrado)
                return
            if control.__class__.__name__ in {"CTkComboBox", "CTkSegmentedButton"}:
                self.reproducir_efecto("seleccionar")
                return
            texto = str(control.cget("text")).casefold()
            if "limpiar" in texto:
                self.reproducir_efecto("limpiar")
            elif "iniciar" in texto:
                self.reproducir_efecto("interfaces")
            elif any(palabra in texto for palabra in ("calcular", "resolver", "convertir")):
                self.reproducir_efecto("calcular")
            else:
                self.reproducir_efecto("seleccionar")

        # add="+" asegura que el sonido conviva con las funciones nativas del botón
        raiz.bind_all("<Enter>", programar_actualizacion_hover, add="+")
        raiz.bind_all("<Leave>", programar_actualizacion_hover, add="+")
        raiz.bind_all("<ButtonPress-1>", al_pulsar, add="+")

    def cerrar(self):
        """Apaga el mezclador de sonido de manera limpia al salir del programa."""
        self.detener_musica_lobby()
        if self.disponible:
            try:
                self._pygame.mixer.quit()
            except Exception:
                pass
            self.disponible = False


def reproducir_sonido_error(widget, mensaje):
    """Busca el AudioManager subiendo por la jerarquía de ventanas y activa el sonido de error."""
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
