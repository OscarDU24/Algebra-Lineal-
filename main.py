from pathlib import Path
import ctypes
import sys
import tkinter as tk
from PIL import Image, ImageTk

from core.ui import preferencias
from core.ui.audio_manager import AudioManager
from core.ui.bienvenida import mostrar_bienvenida_si_corresponde
from core.ui.dashboard import Dashboard
from core.ui.vista_inicio import VistaInicio


if sys.platform == "win32":
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "com.heyalgb.algebralineal.v1"
        )
    except OSError as error:
        print(f"No se pudo establecer la identidad de HeyAlgb en Windows: {error}")


def main():
    root = tk.Tk()

    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    ancho = min(1440, max(640, int(ancho_pantalla * 0.86)))
    alto = min(960, max(520, int(alto_pantalla * 0.86)))
    root.geometry(
        f"{ancho}x{alto}+{(ancho_pantalla - ancho) // 2}+{(alto_pantalla - alto) // 2}"
    )
    root.minsize(min(760, ancho), min(600, alto))
    root.resizable(True, True)
    root.title("HeyAlgb · Álgebra Lineal")

    carpeta_iconos = Path(__file__).resolve().parent / "core" / "assets"
    ruta_icono = carpeta_iconos / "HeyAlgbLogoBlanco.png"
    with Image.open(ruta_icono) as imagen:
        icono_ventana = ImageTk.PhotoImage(
            imagen.convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS)
        )
    root.iconphoto(True, icono_ventana)
    root.icono_ventana = icono_ventana

    if sys.platform == "win32":
        ruta_icono_windows = carpeta_iconos / "HeyAlgbICON.ico"
        try:
            root.iconbitmap(str(ruta_icono_windows))
        except (OSError, tk.TclError) as error:
            print(f"No se pudo cargar el icono de Windows: {error}")

    # Las preferencias viven en la carpeta de configuración del usuario; si el
    # archivo falta o está dañado se usan los valores predeterminados.9
    preferencias_usuario = preferencias.cargar()
    audio = AudioManager()
    audio.establecer_volumen_musica(preferencias_usuario["volumen_musica"] / 100)
    audio.establecer_volumen_efectos(preferencias_usuario["volumen_efectos"] / 100)
    audio.musica_habilitada = preferencias_usuario["musica_habilitada"]
    audio.establecer_efectos_habilitados(preferencias_usuario["efectos_habilitados"])
    root.audio_manager = audio
    audio.instalar_sonidos_interfaz(root)
    dashboard = {"vista": None}
    bienvenida_mostrada = {"valor": False}

    def mostrar_dashboard(iniciar_recorrido=False):
        dashboard["vista"] = Dashboard(root, audio, al_volver_inicio=mostrar_portada)
        if iniciar_recorrido:
            dashboard["vista"].iniciar_recorrido()

    def iniciar_dashboard():
        if not bienvenida_mostrada["valor"]:
            bienvenida_mostrada["valor"] = True
            guia = mostrar_bienvenida_si_corresponde(
                root,
                al_comenzar=lambda: mostrar_dashboard(iniciar_recorrido=True),
                al_omitir=mostrar_dashboard,
            )
            if guia is not None:
                return
        mostrar_dashboard()

    def mostrar_portada():
        VistaInicio(root, audio, iniciar_dashboard)

    def cerrar_aplicacion():
        audio.cerrar()
        root.destroy()

    mostrar_portada()
    root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
    root.mainloop()
    audio.cerrar()

if __name__ == "__main__":
    main()