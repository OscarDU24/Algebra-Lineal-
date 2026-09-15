import tkinter as tk
from tkinter import messagebox

class Dashboard:
    def __init__(self, root):
        self.root = root
        
        # Fondo claro para aproximar la estética del diseño
        self.root.configure(bg="#ececec")
        self.root.title("Calculadora de Álgebra Lineal - FIA UAM")
        
        # ==========================================
        # BARRA DE MENÚ SUPERIOR
        # ==========================================
        self.menu_bar = tk.Menu(self.root)
        
        self.menu_archivo = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_archivo.add_command(label="Salir", command=self.root.quit)
        self.menu_bar.add_cascade(label="Archivo", menu=self.menu_archivo)
        
        self.menu_ayuda = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        self.menu_bar.add_cascade(label="Ayuda", menu=self.menu_ayuda)
        
        self.root.config(menu=self.menu_bar)

        # ==========================================
        # TÍTULO PRINCIPAL
        # ==========================================
        self.lbl_titulo = tk.Label(
            self.root, 
            text="Seleccione su sistema", 
            font=("Segoe UI", 24, "bold"),
            bg="#ececec",
            fg="#000000"
        )
        self.lbl_titulo.pack(pady=(20, 10))

        # ==========================================
        # CONTENEDOR DE LA CUADRÍCULA (GRID)
        # ==========================================
        self.frame_grid = tk.Frame(self.root, bg="#ececec")
        self.frame_grid.pack(expand=True, fill="both", padx=35, pady=10)

        # uniform="card" garantiza proporciones idénticas en todas las celdas
        for i in range(3):
            self.frame_grid.columnconfigure(i, weight=1, uniform="card_col")
        for j in range(2):
            self.frame_grid.rowconfigure(j, weight=1, uniform="card_row")

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
            self.root, 
            text="Módulo activo: Ninguno", 
            font=("Segoe UI", 11),
            bg="#dcdcdc",
            fg="#333333",
            anchor="center",
            pady=6
        )
        self.lbl_estado.pack(side="bottom", fill="x")

    def crear_tarjeta(self, fila, columna, texto, comando):
        """
        Crea un marco que contiene el área interactiva de [ Vista Previa ] 
        y la etiqueta de texto en la zona inferior.
        """
        # Contenedor principal de la tarjeta con borde externo
        card_frame = tk.Frame(
            self.frame_grid, 
            bg="white", 
            highlightbackground="#1a1a1a", 
            highlightthickness=1
        )
        card_frame.grid(row=fila, column=columna, padx=12, pady=12, sticky="nsew")

        # Botón superior (Área de vista previa clickeable)
        btn_vista_previa = tk.Button(
            card_frame,
            text="[ Vista Previa ]",
            font=("Segoe UI", 11, "italic"),
            fg="#888888",
            bg="#f7f7f7",
            activebackground="#ebebeb",
            activeforeground="#444444",
            relief="flat",
            cursor="hand2",
            command=comando
        )
        btn_vista_previa.pack(expand=True, fill="both", padx=8, pady=(8, 4))

        # Etiqueta inferior con el nombre del módulo
        lbl_nombre = tk.Label(
            card_frame,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#000000",
            justify="center",
            pady=12
        )
        lbl_nombre.pack(side="bottom", fill="x")

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