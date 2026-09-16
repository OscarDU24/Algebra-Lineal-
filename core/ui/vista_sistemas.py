# ============================================================
# VISTA - SISTEMAS DE ECUACIONES E INDEPENDENCIA LINEAL
# ============================================================

from core.ui.ctk_compat import ctk
# Importamos la lógica pura (ajusta la ruta si es necesario)
from core.sistemas import operaciones_sistemas as op_sis

class VistaSistemas(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.master_dashboard = master
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        
        self.title("Calculadora de Sistemas e Independencia Lineal - FIA UAM")
        self.geometry("1100x800")

        # Variables de control
        self.modo_actual = ctk.StringVar(value="Sistema (Ax = b)")
        self.entries_A = []
        self.entries_b = []

        # Interfaz
        self.crear_frame_superior()
        self.crear_frame_central()
        self.crear_frame_inferior()
        
        # Generar cuadrícula inicial
        self.generar_cuadricula()

    def al_cerrar(self):
        if self.master_dashboard is not None:
            self.master_dashboard.deiconify()
        self.destroy()

    # ========================================================
    # FRAME SUPERIOR (CONFIGURACIÓN)
    # ========================================================
    def crear_frame_superior(self):
        self.frame_superior = ctk.CTkFrame(self)
        self.frame_superior.pack(fill="x", padx=15, pady=15)

        titulo = ctk.CTkLabel(
            self.frame_superior,
            text="Sistemas e Independencia Lineal",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=10)

        # Selector de Modo
        self.selector_modo = ctk.CTkSegmentedButton(
            self.frame_superior,
            values=["Sistema (Ax = b)", "Independencia Lineal"],
            variable=self.modo_actual,
            command=self.cambiar_modo
        )
        self.selector_modo.pack(pady=10)

        # Controles de dimensiones
        frame_datos = ctk.CTkFrame(self.frame_superior, fg_color="transparent")
        frame_datos.pack(pady=5)

        ctk.CTkLabel(frame_datos, text="Ecuaciones / Dimensión (Filas):").grid(row=0, column=0, padx=5)
        self.entry_filas = ctk.CTkEntry(frame_datos, width=80)
        self.entry_filas.insert(0, "3")
        self.entry_filas.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(frame_datos, text="Variables / Vectores (Columnas):").grid(row=0, column=2, padx=5)
        self.entry_columnas = ctk.CTkEntry(frame_datos, width=80)
        self.entry_columnas.insert(0, "3")
        self.entry_columnas.grid(row=0, column=3, padx=5)

        boton_generar = ctk.CTkButton(frame_datos, text="Generar Cuadrícula", command=self.generar_cuadricula)
        boton_generar.grid(row=0, column=4, padx=15)

    # ========================================================
    # FRAME CENTRAL (ENTRADAS DINÁMICAS)
    # ========================================================
    def crear_frame_central(self):
        self.frame_central = ctk.CTkScrollableFrame(self, label_text="Datos de la Matriz")
        self.frame_central.pack(fill="both", expand=True, padx=15, pady=5)

    def cambiar_modo(self, value):
        self.mostrar_resultado(f"Modo cambiado a: {value}\nPor favor, genera la cuadrícula nuevamente.")
        self.generar_cuadricula()

    def generar_cuadricula(self):
        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            self.mostrar_resultado("Error: Las dimensiones deben ser números enteros positivos.")
            return

        # Limpiar frame central
        for widget in self.frame_central.winfo_children():
            widget.destroy()

        self.entries_A = []
        self.entries_b = []
        modo = self.modo_actual.get()

        # Generar etiquetas de columnas
        for j in range(columnas):
            etiqueta_texto = f"x{j+1}" if modo == "Sistema (Ax = b)" else f"v{j+1}"
            ctk.CTkLabel(self.frame_central, text=etiqueta_texto, font=("Arial", 12, "bold")).grid(row=0, column=j, padx=5, pady=5)
        
        if modo == "Sistema (Ax = b)":
            ctk.CTkLabel(self.frame_central, text="|", font=("Arial", 16, "bold")).grid(row=0, column=columnas, padx=5, pady=5)
            ctk.CTkLabel(self.frame_central, text="b", font=("Arial", 12, "bold")).grid(row=0, column=columnas+1, padx=5, pady=5)

        # Generar cajas de texto
        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                entry = ctk.CTkEntry(self.frame_central, width=60, justify="center")
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                fila_entries.append(entry)
            self.entries_A.append(fila_entries)

            if modo == "Sistema (Ax = b)":
                # Divisor visual
                ctk.CTkLabel(self.frame_central, text="|", font=("Arial", 16)).grid(row=i+1, column=columnas, padx=5, pady=5)
                # Término independiente
                entry_b = ctk.CTkEntry(self.frame_central, width=60, justify="center")
                entry_b.grid(row=i+1, column=columnas+1, padx=5, pady=5)
                self.entries_b.append(entry_b)

    # ========================================================
    # FRAME INFERIOR (CONSOLA)
    # ========================================================
    def crear_frame_inferior(self):
        self.frame_inferior = ctk.CTkFrame(self)
        self.frame_inferior.pack(fill="x", padx=15, pady=15)

        botones_frame = ctk.CTkFrame(self.frame_inferior, fg_color="transparent")
        botones_frame.pack(pady=5)

        boton_calcular = ctk.CTkButton(botones_frame, text="Calcular y Analizar", command=self.ejecutar_calculo, fg_color="green", hover_color="darkgreen")
        boton_calcular.grid(row=0, column=0, padx=10)

        boton_limpiar = ctk.CTkButton(botones_frame, text="Limpiar Resultados", command=lambda: self.mostrar_resultado(""))
        boton_limpiar.grid(row=0, column=1, padx=10)

        self.texto_resultado = ctk.CTkTextbox(self.frame_inferior, height=200, font=("Consolas", 14))
        self.texto_resultado.pack(fill="both", padx=10, pady=10)

    # ========================================================
    # EJECUCIÓN LÓGICA
    # ========================================================
    def ejecutar_calculo(self):
        try:
            # Extraer matriz A
            matriz_A = []
            for fila_entries in self.entries_A:
                fila = []
                for entry in fila_entries:
                    val = op_sis.convertir_a_fraccion(entry.get())
                    if val is None:
                        raise ValueError("Se encontraron valores no válidos en la matriz.")
                    fila.append(val)
                matriz_A.append(fila)

            modo = self.modo_actual.get()

            if modo == "Sistema (Ax = b)":
                vector_b = []
                for entry in self.entries_b:
                    val = op_sis.convertir_a_fraccion(entry.get())
                    if val is None:
                        raise ValueError("Se encontraron valores no válidos en el vector b.")
                    vector_b.append(val)
                
                resultado = op_sis.resolver_sistema(matriz_A, vector_b)
                self.mostrar_resultado(resultado)

            else:
                # Modo Independencia Lineal
                resultado = op_sis.evaluar_independencia(matriz_A)
                self.mostrar_resultado(resultado)

        except Exception as e:
            self.mostrar_resultado(f"Error durante el cálculo:\n{str(e)}")

    def mostrar_resultado(self, texto):
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)

# ============================================================
# PRUEBA INDEPENDIENTE
# ============================================================
if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    ventana = VistaSistemas(app)
    app.mainloop()