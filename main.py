from pathlib import Path
import ctypes
import sys
import tkinter as tk
from PIL import Image, ImageTk

from core.ui.audio_manager import AudioManager
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

    audio = AudioManager()
    root.audio_manager = audio
    audio.instalar_sonidos_interfaz(root)
    dashboard = {"vista": None}

    def iniciar_dashboard():
        dashboard["vista"] = Dashboard(root, audio)

    def cerrar_aplicacion():
        audio.cerrar()
        root.destroy()

    VistaInicio(root, audio, iniciar_dashboard)
    root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
    root.mainloop()
    audio.cerrar()

if __name__ == "__main__":
    main()