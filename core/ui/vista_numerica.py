# ============================================================
# VISTA - SISTEMAS NUMÉRICOS
# ============================================================

import customtkinter as ctk
# Importamos la lógica adaptada
from core.sistemas_numericos import operaciones_numericas as op_num

class VistaSistemasNumericos(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.master_dashboard = master
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        
        self.title("Conversor de Sistemas Numéricos - FIA UAM")
        self.geometry("900x700")

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
            text="Conversor Universal de Sistemas Numéricos", 
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=10)

        instrucciones = (
            "• Ingresa bases del 2 al 36 (o hasta 60 para sistema Sexagesimal).\n"
            "• Para bases > 36, separa los bloques con dos puntos (:). Ej: 12:45:10"
        )
        ctk.CTkLabel(self.frame_sup, text=instrucciones, text_color="gray", justify="left").pack(pady=(0, 15))

        # Cuadro de Entradas
        frame_inputs = ctk.CTkFrame(self.frame_sup, fg_color="transparent")
        frame_inputs.pack(pady=10)

        # Entrada del Número
        ctk.CTkLabel(frame_inputs, text="Número a convertir:", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_numero = ctk.CTkEntry(frame_inputs, width=300, font=("Consolas", 16), placeholder_text="Ej: 1A.8 o 101.11")
        self.entry_numero.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="w")

        # Base Origen
        ctk.CTkLabel(frame_inputs, text="Base Origen:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_base_origen = ctk.CTkEntry(frame_inputs, width=80)
        self.entry_base_origen.insert(0, "2")
        self.entry_base_origen.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Base Destino
        ctk.CTkLabel(frame_inputs, text="Base Destino:").grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.entry_base_destino = ctk.CTkEntry(frame_inputs, width=80)
        self.entry_base_destino.insert(0, "10")
        self.entry_base_destino.grid(row=1, column=3, padx=10, pady=10, sticky="w")

    # ========================================================
    # FRAME INFERIOR (CONSOLA INTEGRADA)
    # ========================================================
    def crear_frame_inferior(self):
        self.frame_inf = ctk.CTkFrame(self)
        self.frame_inf.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        boton_calcular = ctk.CTkButton(
            self.frame_inf, 
            text="Convertir y Mostrar Procedimiento", 
            command=self.ejecutar_calculo, 
            fg_color="green", hover_color="darkgreen",
            height=40, font=("Arial", 14, "bold")
        )
        boton_calcular.pack(pady=15)

        # Consola de solo lectura
        self.texto_resultado = ctk.CTkTextbox(self.frame_inf, font=("Consolas", 14))
        self.texto_resultado.pack(fill="both", expand=True, padx=10, pady=10)

    # ========================================================
    # EJECUCIÓN LÓGICA
    # ========================================================
    def ejecutar_calculo(self):
        numero_str = self.entry_numero.get().strip()
        
        try:
            base_origen = int(self.entry_base_origen.get().strip())
            base_destino = int(self.entry_base_destino.get().strip())
        except ValueError:
            self.mostrar_resultado("Error: Las bases deben ser números enteros (ej. 2, 8, 10, 16, 60).")
            return

        if not numero_str:
            self.mostrar_resultado("Error: Debes ingresar un número para convertir.")
            return

        # Llamar al motor unificado
        resultado, log_procedimiento = op_num.ejecutar_conversion_completa(numero_str, base_origen, base_destino)
        
        # Formatear la salida para la consola
        salida_final = (
            f"=== RESULTADO ===\n"
            f"{resultado}\n\n"
            f"=== PROCEDIMIENTO MATEMÁTICO ===\n"
            f"{log_procedimiento}"
        )
        self.mostrar_resultado(salida_final)

    def mostrar_resultado(self, texto):
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)

# ============================================================
# PRUEBA INDEPENDIENTE
# ============================================================
if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    ventana = VistaSistemasNumericos(app)
    app.mainloop()