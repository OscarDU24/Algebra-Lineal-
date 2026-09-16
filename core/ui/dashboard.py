import tkinter as tk
from tkinter import messagebox
import ctypes
from pathlib import Path
from PIL import Image, ImageTk

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.fuentes_registradas = []
        self.fuente_titulo = "Segoe UI"
        self.fuente_tarjetas = "Segoe UI"
        self.fuente_menu = "Segoe UI"
        self.registrar_fuentes()
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        # El canvas permite conservar las transparencias de Bordes.png.
        self.root.configure(bg="#ffffff")
        self.root.geometry("980x780")
        self.root.title("Calculadora de Álgebra Lineal - FIA UAM")

        # ==========================================
        # INYECCIÓN DEL FONDO DECORATIVO (CAPA 0)
        # ==========================================
        
        try:
            ruta_fondo = Path(__file__).resolve().parents[1] / "assets" / "Bordes.png"
            self.fondo = Image.open(ruta_fondo)
            self.bg_image = ImageTk.PhotoImage(self.fondo)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el fondo decorativo: {e}")
            self.fondo = None
            self.bg_image = None

        self.contenido = tk.Canvas(
            self.root,
            width=980,
            height=780,
            bg="#ffffff",
            highlightthickness=0,
            borderwidth=0,
        )
        self.contenido.pack(expand=True, fill="both")
        if self.bg_image is not None:
            self.contenido.create_image(0, 0, image=self.bg_image, anchor="nw")


        
        # ==========================================
        # BARRA DE MENÚ SUPERIOR
        # ==========================================
        self.menu_bar = tk.Menu(self.root, font=(self.fuente_menu, 11))
        
        self.menu_archivo = tk.Menu(
            self.menu_bar, tearoff=0, font=(self.fuente_menu, 11)
        )
        self.menu_archivo.add_command(label="Salir", command=self.cerrar_aplicacion)
        self.menu_bar.add_cascade(label="Archivo", menu=self.menu_archivo)
        
        self.menu_ayuda = tk.Menu(
            self.menu_bar, tearoff=0, font=(self.fuente_menu, 11)
        )
        self.menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        self.menu_bar.add_cascade(label="Ayuda", menu=self.menu_ayuda)
        
        self.root.config(menu=self.menu_bar)

        # ==========================================
        # TÍTULO PRINCIPAL
        # ==========================================
        self.contenido.create_text(
            490,
            92,
            text="Seleccione su sistema",
            font=(self.fuente_titulo, 75),
            fill="#FFFFFF",
        )

        # ==========================================
        # CREACIÓN DE TARJETAS
        # ==========================================
        # Fila 0
        self.crear_tarjeta(0, 0, "Matrices individuales", self.abrir_matrices)
        self.crear_tarjeta(0, 1, "Operaciones vectoriales\n(individual)", self.abrir_vectores)
        self.crear_tarjeta(0, 2, "Ecuaciones matriciales", self.abrir_ec_matriciales)

        # Fila 1
        self.crear_tarjeta(1, 0, "Ecuaciones Lineales /\nIndependencia lineal", self.abrir_sistemas)
        self.crear_tarjeta(1, 1, "Cálculo de Límites", self.abrir_limites)
        self.crear_tarjeta(1, 2, "Sistemas numéricos", self.abrir_sistemas_numericos)

        # ==========================================
        # BARRA DE ESTADO INFERIOR
        # ==========================================
        self.lbl_estado = tk.Label(
            self.contenido,
            text="Módulo activo: Ninguno", 
            font=(self.fuente_menu, 11),
            bg="#dcdcdc",
            fg="#333333",
            anchor="center",
            pady=6
        )
        self.contenido.create_window(490, 766, window=self.lbl_estado, width=980, height=28)

    def crear_tarjeta(self, fila, columna, texto, comando):
        """
        Crea un marco que contiene el área interactiva de [ Vista Previa ] 
        y la etiqueta de texto en la zona inferior.
        """
        # Contenedor principal de la tarjeta con borde externo
        card_frame = tk.Frame(
            self.contenido,
            bg="white", 
            width=255,
            height=220,
            highlightbackground="#1a1a1a", 
            highlightthickness=1
        )
        posiciones_x = (180, 490, 800)
        posiciones_y = (330, 570)
        self.contenido.create_window(
            posiciones_x[columna],
            posiciones_y[fila],
            window=card_frame,
            width=255,
            height=220,
        )
        card_frame.grid_propagate(False)

        preview_frame = tk.Frame(
            card_frame,
            bg="#f7f7f7",
            width=210,
            height=145,
        )
        preview_frame.pack(padx=8, pady=(8, 4))
        preview_frame.pack_propagate(False)

        # Botón superior (Área de vista previa clickeable)
        btn_vista_previa = tk.Button(
            preview_frame,
            text="[ Vista Previa ]",
            font=(self.fuente_menu, 10, "italic"),
            fg="#888888",
            bg="#f7f7f7",
            activebackground="#ebebeb",
            activeforeground="#444444",
            relief="flat",
            cursor="hand2",
            command=comando
        )
        btn_vista_previa.pack(expand=True, fill="both")

        # Etiqueta inferior con el nombre del módulo
        lbl_nombre = tk.Label(
            card_frame,
            text=texto,
            font=(self.fuente_tarjetas, 11),
            bg="white",
            fg="#000000",
            justify="center",
            pady=12
        )
        lbl_nombre.pack(side="bottom", fill="x")

    def registrar_fuentes(self):
        """Registra las fuentes solo durante la vida de esta aplicación."""
        if not hasattr(ctypes, "windll"):
            return

        AddFontResourceExW = ctypes.windll.gdi32.AddFontResourceExW
        AddFontResourceExW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
        AddFontResourceExW.restype = ctypes.c_int

        carpeta_fuentes = Path(__file__).resolve().parents[1] / "assets" / "fonts"
        fuentes = {
            "UltraCondensedSansSerif.ttf": ("fuente_titulo", "UltraCondensedSansSerif"),
            "HelveticaNowDisplay-Bold.ttf": ("fuente_tarjetas", "Helvetica Now Display"),
            "Democratica Bold.ttf": ("fuente_menu", "Democratica"),
        }

        for nombre_archivo, (atributo, familia) in fuentes.items():
            ruta = carpeta_fuentes / nombre_archivo
            if ruta.exists() and AddFontResourceExW(str(ruta), 0x10, None):
                self.fuentes_registradas.append(ruta)
                setattr(self, atributo, familia)

    def desregistrar_fuentes(self):
        if not hasattr(ctypes, "windll"):
            return

        RemoveFontResourceExW = ctypes.windll.gdi32.RemoveFontResourceExW
        RemoveFontResourceExW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
        RemoveFontResourceExW.restype = ctypes.c_int

        for ruta in self.fuentes_registradas:
            RemoveFontResourceExW(str(ruta), 0x10, None)
        self.fuentes_registradas.clear()

    def cerrar_aplicacion(self):
        self.desregistrar_fuentes()
        self.root.destroy()

    # ==========================================
    # FUNCIONES DE TRANSICIÓN (CONTROLADORES)
    # ==========================================
    def abrir_matrices(self):
        self.lbl_estado.config(text="Módulo activo: Matrices individuales")
        print("Abriendo módulo de Matrices...")
        self.root.withdraw()
        from core.ui.vista_matriz import VistaMatriz
        ventana = VistaMatriz(self.root)

    def abrir_vectores(self):
        self.lbl_estado.config(text="Módulo activo: Operaciones vectoriales")
        print("Abriendo módulo de Vectores...")
        self.root.withdraw()
        from core.ui.vista_vector import VistaVector
        ventana = VistaVector(self.root)

    def abrir_ec_matriciales(self):
        self.lbl_estado.config(text="Módulo activo: Ecuaciones matriciales")
        print("Abriendo módulo de Ecuaciones Matriciales...")
        self.root.withdraw()
        from core.ui.vista_matricial import VistaMatricial
        ventana = VistaMatricial(self.root)

    def abrir_sistemas(self):
        self.lbl_estado.config(text="Módulo activo: Sistemas e Independencia")
        print("Abriendo módulo de Sistemas...")
        self.root.withdraw()
        from core.ui.vista_sistemas import VistaSistemas
        ventana = VistaSistemas(self.root)
    
    def abrir_limites(self):
        self.lbl_estado.config(text="Módulo activo: Cálculo de Límites")
        print("Abriendo módulo de Límites...")
        self.root.withdraw()
        from core.ui.vista_limites import VistaLimites
        ventana = VistaLimites(self.root)

    def abrir_sistemas_numericos(self):
        self.lbl_estado.config(text="Módulo activo: Sistemas Numéricos")
        print("Abriendo módulo de Sistemas Numéricos...")
        self.root.withdraw()
        from core.ui.vista_numerica import VistaSistemasNumericos
        ventana = VistaSistemasNumericos(self.root)   
        
    def proximamente(self):
        messagebox.showinfo("Próximamente", "Este módulo aún está en desarrollo.")

    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "Calculadora de Álgebra Lineal - FIA UAM\nVersión unificada.")