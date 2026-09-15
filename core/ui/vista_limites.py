# ============================================================
# VISTA - CÁLCULO DE LÍMITES
# ============================================================

import customtkinter as ctk
# Importamos la lógica pura (ajusta la ruta si es necesario)
from core.limites import operaciones_limites as op_lim

class VistaLimites(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.master_dashboard = master
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        
        self.title("Calculadora de Límites - FIA UAM")
        self.geometry("900x700")

        # Variable de control
        self.direccion_var = ctk.StringVar(value="bilateral")

        # Generar Interfaz
        self.crear_frame_superior()
        self.crear_frame_inferior()

    def al_cerrar(self):
        if self.master_dashboard is not None:
            self.master_dashboard.deiconify()
        self.destroy()

    # ========================================================
    # FRAME SUPERIOR (ENTRADA DE DATOS)
    # ========================================================
    def crear_frame_superior(self):
        self.frame_sup = ctk.CTkFrame(self)
        self.frame_sup.pack(fill="x", padx=15, pady=15)

        titulo = ctk.CTkLabel(
            self.frame_sup, 
            text="Evaluación de Límites y Continuidad", 
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=10)

        # Instrucciones de uso para SymPy
        ayuda_texto = (
            "Guía de sintaxis matemática:\n"
            "• Potencias: Usa doble asterisco (x**2)\n"
            "• Funciones: sin(x), cos(x), tan(x), log(x), exp(x)\n"
            "• Infinito: Escribe 'oo' (doble letra o) o 'inf'"
        )
        ctk.CTkLabel(self.frame_sup, text=ayuda_texto, text_color="gray", justify="left").pack(pady=(0, 15))

        # Cuadro de Entradas
        frame_inputs = ctk.CTkFrame(self.frame_sup, fg_color="transparent")
        frame_inputs.pack(pady=10)

        # Entrada para la función
        ctk.CTkLabel(frame_inputs, text="Función f(x) =", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_fx = ctk.CTkEntry(frame_inputs, width=350, font=("Consolas", 14), placeholder_text="Ej: (x**2 - 1)/(x - 1)")
        self.entry_fx.grid(row=0, column=1, padx=10, pady=10)
        self.entry_fx.insert(0, "(x**2 - 1)/(x - 1)")

        # Entrada para la tendencia de 'x'
        ctk.CTkLabel(frame_inputs, text="x tiende a ->", font=("Arial", 14, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_c = ctk.CTkEntry(frame_inputs, width=120, font=("Consolas", 14), placeholder_text="Ej: 1 o oo")
        self.entry_c.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.entry_c.insert(0, "1")

        # Selectores Laterales
        frame_radios = ctk.CTkFrame(self.frame_sup, fg_color="transparent")
        frame_radios.pack(pady=15)
        
        ctk.CTkLabel(frame_radios, text="Dirección de evaluación:").pack(side="left", padx=10)
        ctk.CTkRadioButton(frame_radios, text="Bilateral", variable=self.direccion_var, value="bilateral").pack(side="left", padx=10)
        ctk.CTkRadioButton(frame_radios, text="Izquierda (x -> c⁻)", variable=self.direccion_var, value="izquierda").pack(side="left", padx=10)
        ctk.CTkRadioButton(frame_radios, text="Derecha (x -> c⁺)", variable=self.direccion_var, value="derecha").pack(side="left", padx=10)

    # ========================================================
    # FRAME INFERIOR (CONSOLA INTEGADA)
    # ========================================================
    def crear_frame_inferior(self):
        self.frame_inf = ctk.CTkFrame(self)
        self.frame_inf.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        botones_frame = ctk.CTkFrame(self.frame_inf, fg_color="transparent")
        botones_frame.pack(pady=10)

        boton_calcular = ctk.CTkButton(botones_frame, text="Evaluar Límite", command=self.ejecutar_calculo, fg_color="green", hover_color="darkgreen")
        boton_calcular.grid(row=0, column=0, padx=10)

        boton_limpiar = ctk.CTkButton(botones_frame, text="Limpiar Consola", command=lambda: self.mostrar_resultado(""))
        boton_limpiar.grid(row=0, column=1, padx=10)

        self.texto_resultado = ctk.CTkTextbox(self.frame_inf, font=("Consolas", 14))
        self.texto_resultado.pack(fill="both", expand=True, padx=10, pady=10)

    # ========================================================
    # EJECUCIÓN LÓGICA
    # ========================================================
    def ejecutar_calculo(self):
        funcion = self.entry_fx.get().strip()
        punto = self.entry_c.get().strip()
        direccion = self.direccion_var.get()

        if not funcion or not punto:
            self.mostrar_resultado("Error: Debes ingresar tanto la función como el punto de evaluación.")
            return

        # Llamar al motor de SymPy
        resultado = op_lim.calcular_limite(funcion, punto, direccion)
        self.mostrar_resultado(resultado)

    def mostrar_resultado(self, texto):
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)

# ============================================================
# PRUEBA INDEPENDIENTE
# ============================================================
if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    ventana = VistaLimites(app)
    app.mainloop()