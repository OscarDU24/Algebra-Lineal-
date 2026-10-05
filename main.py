import tkinter as tk
from core.ui.audio_manager import AudioManager
from core.ui.dashboard import Dashboard
from core.ui.vista_inicio import VistaInicio

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