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
        self.ventana_activa = None
        self.registrar_fuentes()
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        # El canvas permite conservar las transparencias del borde decorativo.
        self.root.configure(bg="#ffffff")
        self.root.geometry("980x780")
        self.root.title("Calculadora de Álgebra Lineal - FIA UAM")

        # ==========================================
        # INYECCIÓN DEL FONDO DECORATIVO (CAPA 0)
        # ==========================================
        
        try:
            ruta_fondo = Path(__file__).resolve().parents[1] / "assets" / "BordesFinales.png"
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
        self.menu_bar = tk.Menu(
            self.root,
            font=(self.fuente_menu, 11),
            bg="#ffffff",
            fg="#000000",
            activebackground="#8f0000",
            activeforeground="#ffffff"
        )
        
        self.menu_archivo = tk.Menu(
            self.menu_bar,
            tearoff=0,
            font=(self.fuente_menu, 11),
            bg="#ffffff",
            fg="#000000",
            activebackground="#8f0000",
            activeforeground="#ffffff"
        )
        self.menu_archivo.add_command(label="Salir", command=self.cerrar_aplicacion)
        self.menu_bar.add_cascade(label="Archivo", menu=self.menu_archivo)
        
        self.menu_ayuda = tk.Menu(
            self.menu_bar,
            tearoff=0,
            font=(self.fuente_menu, 11),
            bg="#ffffff",
            fg="#000000",
            activebackground="#8f0000",
            activeforeground="#ffffff"
        )
        self.menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        self.menu_bar.add_cascade(label="Ayuda", menu=self.menu_ayuda)
        
        self.root.config(menu=self.menu_bar)

        # ==========================================
        # TÍTULO PRINCIPAL
        # ==========================================
        self.contenido.create_text(
            465,
            92,
            text="Seleccione su sistema",
            font=(self.fuente_titulo, 75),
            fill="#fe0000",
        )

        # ==========================================
        # CREACIÓN DE TARJETAS
        # ==========================================
        # Fila 0
        self.crear_tarjeta(0, 0, "Operaciones Básicas de Matrices", self.abrir_matrices, "MatrIndvICON.png")
        self.crear_tarjeta(0, 1, "Productos entre Matrices\n(Vectores)", self.abrir_vectores, "EcVectorialesCON.png")
        self.crear_tarjeta(0, 2, "Ecuaciones matriciales", self.abrir_ec_matriciales, "EcMatriciaIesCON.png")

        # Fila 1
        self.crear_tarjeta(1, 0, "Sistemas de Ecuaciones Lineales", self.abrir_sistemas, "EcLinealICON.png")
        self.crear_tarjeta(1, 1, "Evaluación de Límites", self.abrir_limites, "LimitesICON.png")
        self.crear_tarjeta(1, 2, "Sistemas numéricos", self.abrir_sistemas_numericos, "SisNumICON.png")

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

    def crear_tarjeta(self, fila, columna, texto, comando, nombre_icono):
        """
        Crea una tarjeta con el icono de la calculadora y su etiqueta.
        """
        # Contenedor principal de la tarjeta con borde externo
        card_frame = tk.Frame(
            self.contenido,
            bg="#ffffff",
            width=255,
            height=220,
            highlightbackground="#000000",
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
        card_frame.configure(cursor="hand2")

        preview_frame = tk.Frame(
            card_frame,
            bg="#ffffff",
            width=210,
            height=145,
        )
        preview_frame.pack(padx=8, pady=(8, 4))
        preview_frame.pack_propagate(False)

        ruta_icono = Path(__file__).resolve().parents[1] / "assets" / nombre_icono
        try:
            icono = Image.open(ruta_icono).convert("RGBA")
            icono.thumbnail((132, 132), Image.Resampling.LANCZOS)
            imagen_icono = ImageTk.PhotoImage(icono)
            self.iconos = getattr(self, "iconos", [])
            self.iconos.append(imagen_icono)
        except Exception as error:
            print(f"Advertencia: No se pudo cargar el icono {nombre_icono}: {error}")
            imagen_icono = None

        boton_icono = tk.Button(
            preview_frame,
            image=imagen_icono,
            text="Icono no disponible" if imagen_icono is None else "",
            fg="#fe0000",
            bg="#ffffff",
            activebackground="#ffffff",
            activeforeground="#fe0000",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            command=comando
        )
        boton_icono.pack(expand=True, fill="both")

        # Etiqueta inferior con el nombre del módulo
        lbl_nombre = tk.Label(
            card_frame,
            text=texto,
            font=(self.fuente_tarjetas, 11),
            bg="#ffffff",
            fg="#000000",
            justify="center",
            pady=12
        )
        lbl_nombre.pack(side="bottom", fill="x")

        def seleccionar(event=None):
            card_frame.configure(highlightbackground="#fe0000", highlightthickness=2)

        def deseleccionar(event=None):
            card_frame.configure(highlightbackground="#000000", highlightthickness=1)

        def activar(event=None):
            comando()

        for widget in (card_frame, preview_frame, lbl_nombre):
            widget.bind("<Enter>", seleccionar)
            widget.bind("<Leave>", deseleccionar)

        lbl_nombre.bind("<Button-1>", activar)

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

    def _abrir_ventana(self, constructor):
        """Abre una sola calculadora y evita dobles aperturas por doble clic."""
        if self.ventana_activa is not None:
            if self.ventana_activa is True:
                return
            if self.ventana_activa.winfo_exists():
                self.ventana_activa.lift()
                self.ventana_activa.focus_force()
                return

        self.root.withdraw()
        self.ventana_activa = True
        try:
            ventana = constructor(self.root)
        except Exception:
            self.ventana_activa = None
            self.root.deiconify()
            raise

        self.ventana_activa = ventana

        def limpiar_referencia(event):
            if event.widget != ventana:
                return
            self.ventana_activa = None
            self.root.deiconify()

        ventana.bind("<Destroy>", limpiar_referencia)

    # ==========================================
    # FUNCIONES DE TRANSICIÓN (CONTROLADORES)
    # ==========================================
    def abrir_matrices(self):
        self.lbl_estado.config(text="Módulo activo: Matrices individuales")
        print("Abriendo módulo de Matrices...")
        from core.ui.vista_matriz import VistaMatriz
        self._abrir_ventana(VistaMatriz)

    def abrir_vectores(self):
        self.lbl_estado.config(text="Módulo activo: Operaciones vectoriales")
        print("Abriendo módulo de Vectores...")
        from core.ui.vista_vector import VistaVector
        self._abrir_ventana(VistaVector)

    def abrir_ec_matriciales(self):
        self.lbl_estado.config(text="Módulo activo: Ecuaciones matriciales")
        print("Abriendo módulo de Ecuaciones Matriciales...")
        from core.ui.vista_matricial import VistaMatricial
        self._abrir_ventana(VistaMatricial)

    def abrir_sistemas(self):
        self.lbl_estado.config(text="Módulo activo: Sistemas e Independencia")
        print("Abriendo módulo de Sistemas...")
        from core.ui.vista_sistemas import VistaSistemas
        self._abrir_ventana(VistaSistemas)
    
    def abrir_limites(self):
        self.lbl_estado.config(text="Módulo activo: Cálculo de Límites")
        print("Abriendo módulo de Límites...")
        from core.ui.vista_limites import VistaLimites
        self._abrir_ventana(VistaLimites)

    def abrir_sistemas_numericos(self):
        self.lbl_estado.config(text="Módulo activo: Sistemas Numéricos")
        print("Abriendo módulo de Sistemas Numéricos...")
        from core.ui.vista_numerica import VistaSistemasNumericos
        self._abrir_ventana(VistaSistemasNumericos)
        
    def proximamente(self):
        messagebox.showinfo("Próximamente", "Este módulo aún está en desarrollo.")

    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "Calculadora de Álgebra Lineal - FIA UAM\nVersión unificada.")