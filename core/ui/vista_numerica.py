# ============================================================
# VISTA - SISTEMAS NUMÉRICOS
# ============================================================

from core.ui.ctk_compat import ctk
from core.sistemas_numericos import operaciones_numericas as op_num
from core.ui.tema import (
    ACENTO,
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_panel_contenedor,
)


class VistaSistemasNumericos(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)

        self.master_dashboard = master
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        self.title("Conversor de Sistemas Numéricos")
        self.geometry("880x720")
        self.minsize(760, 620)

        self.nombres_sistemas = list(op_num.SISTEMAS.keys())  # Binario, Octal, Decimal, Hexadecimal

        self.crear_encabezado()
        self.crear_tabs()
        self.crear_consola()

    def al_cerrar(self):
        if self.master_dashboard is not None:
            self.master_dashboard.deiconify()
        self.destroy()

    # ========================================================
    # ENCABEZADO
    # ========================================================
    def crear_encabezado(self):
        frame = ctk.CTkFrame(self, **estilo_panel_contenedor())
        frame.pack(fill="x", padx=15, pady=(15, 8))

        ctk.CTkLabel(
            frame,
            text="Conversor de Sistemas Numéricos",
            font=("Segoe UI", 24, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(pady=(12, 2))

        ctk.CTkLabel(
            frame,
            text="Elige abajo qué quieres convertir: Decimal → otra base, u otra base → Decimal.",
            text_color=TEXTO_CLARO,
        ).pack(pady=(0, 12))

    # ========================================================
    # PESTAÑAS: los dos módulos que pide la guía
    # ========================================================
    def crear_tabs(self):
        self.tabs = ctk.CTkTabview(
            self,
            height=360,
            fg_color="#111111",
            segmented_button_fg_color="#111111",
            segmented_button_selected_color=ACENTO,
            segmented_button_selected_hover_color="#b30000",
            segmented_button_unselected_color="#333333",
            segmented_button_unselected_hover_color="#555555",
            text_color=TEXTO_CLARO,
        )
        self.tabs.pack(fill="x", padx=15, pady=8)

        tab_dec = self.tabs.add("Decimal → Otra base")
        tab_a_dec = self.tabs.add("Otra base → Decimal")

        # Pasar los módulos dentro de las pestañas
        self.crear_modulo_decimal_a_base(tab_dec)
        self.crear_modulo_base_a_decimal(tab_a_dec)

    # --------------------------------------------------------
    # MÓDULO 1: Decimal -> Binario / Octal / Hexadecimal
    # El usuario ESCRIBE el número decimal y ELIGE la base destino.
    # --------------------------------------------------------
    def crear_modulo_decimal_a_base(self, contenedor):
        ctk.CTkLabel(
            contenedor,
            text="Número decimal a convertir:",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=20, pady=(18, 4))

        self.entry_decimal = ctk.CTkEntry(
            contenedor, width=300, font=("Consolas", 16), placeholder_text="Ej: 156 o 45.75"
        )
        self.entry_decimal.pack(anchor="w", padx=20, pady=(0, 10))

        ctk.CTkLabel(
            contenedor,
            text="¿A qué sistema quieres convertirlo?",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=20, pady=(0, 6))

        # Solo se ofrecen los destinos que pide la guía (no incluye "Decimal").
        destinos = [n for n in self.nombres_sistemas if n != "Decimal"]
        self.selector_destino = ctk.CTkSegmentedButton(
            contenedor,
            values=destinos,
            selected_color=ACENTO,
            selected_hover_color="#b30000",
            text_color=TEXTO_CLARO,
        )
        self.selector_destino.set(destinos[0])
        self.selector_destino.pack(anchor="w", padx=20, pady=(0, 15))

        ctk.CTkButton(
            contenedor,
            text="Convertir y mostrar procedimiento",
            **estilo_boton_principal(),
            command=self.ejecutar_decimal_a_base,
            height=38,
        ).pack(anchor="w", padx=20, pady=(0, 10))

    # --------------------------------------------------------
    # MÓDULO 2: Binario / Octal / Decimal / Hexadecimal -> Decimal
    # El usuario ELIGE la base de origen y ESCRIBE el número en esa base.
    # Se muestra la combinación lineal que genera el número.
    # --------------------------------------------------------
    def crear_modulo_base_a_decimal(self, contenedor):
        ctk.CTkLabel(
            contenedor,
            text="¿En qué sistema está el número que vas a convertir?",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=20, pady=(18, 6))

        # Se ofrecen todas las bases definidas por el conversor.
        origenes = self.nombres_sistemas
        self.selector_origen = ctk.CTkSegmentedButton(
            contenedor,
            values=origenes,
            command=self.al_cambiar_origen,
            selected_color=ACENTO,
            selected_hover_color="#b30000",
            text_color=TEXTO_CLARO,
        )
        self.selector_origen.set(origenes[0])
        self.selector_origen.pack(anchor="w", padx=20, pady=(0, 16))

        self.label_numero_origen = ctk.CTkLabel(
            contenedor,
            text=f"Número en {origenes[0]}:",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXTO_CLARO,
        )
        self.label_numero_origen.pack(anchor="w", padx=20, pady=(0, 4))

        self.entry_origen = ctk.CTkEntry(
            contenedor, width=300, font=("Consolas", 16), placeholder_text="Ej: 1011.01"
        )
        self.entry_origen.pack(anchor="w", padx=20, pady=(0, 20))

        ctk.CTkButton(
            contenedor,
            text="Convertir y mostrar combinación lineal",
            **estilo_boton_principal(),
            command=self.ejecutar_base_a_decimal,
            height=38,
        ).pack(anchor="w", padx=20, pady=(0, 10))

    def al_cambiar_origen(self, valor_seleccionado):
        self.label_numero_origen.configure(text=f"Número en {valor_seleccionado}:")

    # ========================================================
    # CONSOLA DE PROCEDIMIENTO (SOLO LECTURA)
    # ========================================================
    def crear_consola(self):
        frame = ctk.CTkFrame(self, **estilo_panel_contenedor())
        frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        ctk.CTkLabel(
            frame, text="Procedimiento y resultado:", font=("Segoe UI", 13, "bold"), text_color=TEXTO_CLARO
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.texto_resultado = ctk.CTkTextbox(frame, height=180, font=("Consolas", 14), **estilo_consola_resultado())
        self.texto_resultado.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_resultado(self, texto):
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)

    # ========================================================
    # EJECUCIÓN DE CADA MÓDULO
    # ========================================================
    def ejecutar_decimal_a_base(self):
        try:
            numero = op_num.parsear_decimal(self.entry_decimal.get())
        except ValueError as e:
            self.mostrar_resultado(f"Error: {e}")
            return

        nombre_destino = self.selector_destino.get()
        base_destino = op_num.SISTEMAS[nombre_destino]

        resultado, procedimiento = op_num.convertir_decimal_a_base(
            numero, base_destino, nombre_destino
        )
        self.mostrar_resultado(
            f"=== RESULTADO ===\n{resultado}\n\n"
            f"=== PROCEDIMIENTO (divisiones/multiplicaciones sucesivas) ===\n{procedimiento}"
        )

    def ejecutar_base_a_decimal(self):
        nombre_origen = self.selector_origen.get()
        base_origen = op_num.SISTEMAS[nombre_origen]
        numero_str = self.entry_origen.get().strip()

        try:
            resultado, procedimiento = op_num.convertir_a_decimal(
                numero_str, base_origen, nombre_origen
            )
        except ValueError as e:
            self.mostrar_resultado(f"Error: {e}")
            return

        self.mostrar_resultado(
            f"=== RESULTADO ===\n{resultado}\n\n"
            f"=== PROCEDIMIENTO (combinación lineal) ===\n{procedimiento}"
        )


# ============================================================
# PRUEBA INDEPENDIENTE
# ============================================================
if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    ventana = VistaSistemasNumericos(app)
    app.mainloop()