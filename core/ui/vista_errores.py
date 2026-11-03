"""Interfaz educativa para errores, propagación y punto flotante."""

from core.metodos_numericos import operaciones_errores as op_errores
from core.metodos_numericos import verificacion_matriz
from core.ui.audio_manager import reproducir_sonido_error
from core.ui.ctk_compat import ctk
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_panel_contenedor,
)


class VistaErrores(ctk.CTkFrame):
    """Panel de cálculos de error y demostraciones de representación."""

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self._crear_interfaz()

    def _crear_interfaz(self):
        encabezado = ctk.CTkFrame(self, **estilo_panel_contenedor())
        encabezado.pack(fill="x", padx=15, pady=(15, 8))
        ctk.CTkLabel(
            encabezado,
            text="Análisis de Errores Numéricos",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=12, pady=10)

        self.pestanas = ctk.CTkTabview(self)
        self.pestanas.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.pestana_calculo = self.pestanas.add("Errores y propagación")
        self.pestana_redondeo = self.pestanas.add("Truncamiento y redondeo")
        self.pestana_float = self.pestanas.add("Punto flotante")
        self.pestana_verificacion = self.pestanas.add("Gauss-Jordan")
        self._crear_pestana_calculo()
        self._crear_pestana_redondeo()
        self._crear_pestana_float()
        self._crear_pestana_verificacion()

    def _crear_salida(self, master, alto=160):
        salida = ctk.CTkTextbox(
            master,
            height=alto,
            font=("Consolas", 12),
            **estilo_consola_resultado(),
        )
        salida.pack(fill="both", expand=True, padx=8, pady=8)
        return salida

    def _crear_pestana_calculo(self):
        panel = ctk.CTkFrame(self.pestana_calculo, **estilo_panel_contenedor())
        panel.pack(fill="x", padx=6, pady=6)
        self._crear_campo(panel, "Valor aproximado", "aproximado", "3.14", 0, 0)
        self._crear_campo(panel, "Valor exacto", "exacto", "3.14159265", 0, 2)

        ctk.CTkLabel(
            panel,
            text="Función para propagación f(x)",
            text_color=TEXTO_CLARO,
        ).grid(row=1, column=0, padx=8, pady=(8, 2), sticky="w")
        self.campo_funcion = ctk.CTkEntry(panel, width=300)
        self.campo_funcion.insert(0, "x**2")
        self.campo_funcion.grid(row=2, column=0, columnspan=2, padx=8, pady=(0, 8), sticky="ew")
        self.campo_x = self._crear_campo(panel, "x", "x", "2", 1, 2)
        self.campo_delta_x = self._crear_campo(panel, "Δx", "delta_x", "0.01", 1, 4)

        botones = ctk.CTkFrame(self.pestana_calculo, fg_color="transparent")
        botones.pack(fill="x", padx=6, pady=4)
        ctk.CTkButton(
            botones,
            text="Calcular errores",
            command=self.calcular_errores,
            **estilo_boton_principal(),
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            botones,
            text="Propagar error",
            command=self.calcular_propagacion,
            **estilo_boton_secundario(),
        ).pack(side="left")
        self.salida_calculo = self._crear_salida(self.pestana_calculo)
        self._mostrar(self.salida_calculo, "Compare los valores o estime Δy ≈ f'(x)·Δx.")

    def _crear_pestana_redondeo(self):
        panel = ctk.CTkFrame(self.pestana_redondeo, **estilo_panel_contenedor())
        panel.pack(fill="x", padx=6, pady=6)
        self.campo_valor = self._crear_campo(panel, "Valor", "valor", "3.14159265", 0, 0)
        self.campo_decimales = self._crear_campo(panel, "Decimales k", "k", "3", 0, 2)
        ctk.CTkButton(
            panel,
            text="Comparar",
            command=self.calcular_redondeo,
            **estilo_boton_principal(),
        ).grid(row=0, column=4, rowspan=3, padx=10, pady=12)
        self.salida_redondeo = self._crear_salida(self.pestana_redondeo, 250)
        self._mostrar(self.salida_redondeo, "La truncación corta hacia cero; el redondeo usa mitad hacia arriba.")

    def _crear_pestana_float(self):
        panel = ctk.CTkFrame(self.pestana_float, **estilo_panel_contenedor())
        panel.pack(fill="x", padx=6, pady=6)
        ctk.CTkLabel(
            panel,
            text="Demostraciones reproducibles con Python y NumPy",
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=10, pady=10)
        ctk.CTkButton(
            panel,
            text="Ejecutar demostración",
            command=self.demostrar_float,
            **estilo_boton_principal(),
        ).pack(anchor="w", padx=10, pady=(0, 10))
        self.salida_float = self._crear_salida(self.pestana_float, 260)
        self.demostrar_float()

    def _crear_pestana_verificacion(self):
        panel = ctk.CTkFrame(self.pestana_verificacion, **estilo_panel_contenedor())
        panel.pack(fill="x", padx=6, pady=6)
        ctk.CTkLabel(
            panel,
            text=(
                "Matriz cuadrada, una fila por línea y celdas separadas por espacios. "
                "Admite enteros, decimales y fracciones como 1/2."
            ),
            text_color=TEXTO_CLARO,
            wraplength=850,
        ).pack(anchor="w", padx=10, pady=(8, 4))
        self.entrada_matriz = ctk.CTkTextbox(
            panel,
            height=130,
            font=("Consolas", 12),
            **estilo_consola_resultado(),
        )
        self.entrada_matriz.pack(fill="x", padx=8, pady=4)
        self.entrada_matriz.insert("1.0", "2 1\n1 2")
        acciones = ctk.CTkFrame(self.pestana_verificacion, fg_color="transparent")
        acciones.pack(fill="x", padx=6, pady=4)
        ctk.CTkButton(
            acciones,
            text="Comparar inversas",
            command=self.calcular_verificacion,
            **estilo_boton_principal(),
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            acciones,
            text="Cargar Hilbert 5×5",
            command=self.cargar_hilbert,
            **estilo_boton_secundario(),
        ).pack(side="left")
        self.salida_verificacion = self._crear_salida(
            self.pestana_verificacion, 250
        )
        self._mostrar(
            self.salida_verificacion,
            "Compare la inversa exacta con Gauss-Jordan float y NumPy.",
        )

    def cargar_hilbert(self):
        matriz = verificacion_matriz.matriz_hilbert(5)
        texto = "\n".join(
            " ".join(str(valor) for valor in fila) for fila in matriz
        )
        self.entrada_matriz.delete("1.0", "end")
        self.entrada_matriz.insert("1.0", texto)
        self.calcular_verificacion()

    def calcular_verificacion(self):
        try:
            matriz = verificacion_matriz.parsear_matriz(
                self.entrada_matriz.get("1.0", "end")
            )
            resultado = verificacion_matriz.comparar_inversas(matriz)
            texto = (
                "INVERSA EXACTA (Gauss-Jordan con Fraction)\n"
                f"{verificacion_matriz.matriz_a_texto(resultado['inversa_exacta'])}\n\n"
                "INVERSA EN PUNTO FLOTANTE (Gauss-Jordan)\n"
                f"{verificacion_matriz.matriz_a_texto(resultado['inversa_float'], 'decimales')}\n\n"
                "COMPARACIÓN Y ESTABILIDAD\n"
                f"Error absoluto G-J vs exacta: {resultado['error_gj_absoluto']:.6g}\n"
                f"Error relativo G-J vs exacta: {resultado['error_gj_relativo']:.6g}\n"
                f"Residuo máximo G-J, |A·A⁻¹-I|: {resultado['residuo_gj']:.6g}\n"
                f"Error absoluto NumPy vs exacta: {resultado['error_numpy_absoluto']:.6g}\n"
                f"Error relativo NumPy vs exacta: {resultado['error_numpy_relativo']:.6g}\n"
                f"Residuo máximo NumPy: {resultado['residuo_numpy']:.6g}\n"
                f"Número de condición κ₂(A), NumPy: {resultado['condicion']:.6g}"
            )
        except (ValueError, ArithmeticError, OverflowError) as error:
            texto = f"ERROR: {error}"
        self._mostrar(self.salida_verificacion, texto)

    def _crear_campo(self, master, etiqueta, clave, valor, fila, columna):
        ctk.CTkLabel(master, text=etiqueta, text_color=TEXTO_CLARO).grid(
            row=fila * 3, column=columna, padx=8, pady=(8, 2), sticky="w"
        )
        campo = ctk.CTkEntry(master, width=150, font=("Consolas", 12))
        campo.insert(0, valor)
        campo.grid(row=fila * 3 + 1, column=columna, padx=8, pady=(0, 8), sticky="ew")
        setattr(self, f"campo_{clave}", campo)
        return campo

    def calcular_errores(self):
        try:
            resultado = op_errores.calcular_errores(
                self.campo_aproximado.get(), self.campo_exacto.get()
            )
            relativo = resultado["error_relativo"]
            porcentual = resultado["error_porcentual"]
            texto = f"Error absoluto: {resultado['error_absoluto']:.12g}\n"
            texto += (
                f"Error relativo: {relativo:.12g}\n"
                if relativo is not None
                else "Error relativo: no definido (referencia cero)\n"
            )
            texto += (
                f"Error porcentual: {porcentual:.12g}%"
                if porcentual is not None
                else "Error porcentual: no definido (referencia cero)"
            )
        except (ValueError, ArithmeticError) as error:
            texto = f"ERROR: {error}"
        self._mostrar(self.salida_calculo, texto)

    def calcular_propagacion(self):
        try:
            resultado = op_errores.propagar_error(
                self.campo_funcion.get(),
                self.campo_x.get(),
                self.campo_delta_x.get(),
            )
            texto = (
                "Aproximación diferencial Δy ≈ f'(x)·Δx\n"
                f"f'(x) numérica: {resultado['derivada_aproximada']:.12g}\n"
                f"Δy aproximado: {resultado['delta_y_aproximado']:.12g}\n"
                f"Δy exacto por diferencia finita: {resultado['delta_y_exacto']:.12g}\n"
                f"Diferencia absoluta: {resultado['error_absoluto_aproximacion']:.12g}"
            )
        except (ValueError, ArithmeticError) as error:
            texto = f"ERROR: {error}"
        self._mostrar(self.salida_calculo, texto)

    def calcular_redondeo(self):
        try:
            decimales = int(self.campo_k.get())
            resultado = op_errores.simular_truncamiento_redondeo(
                self.campo_valor.get(), decimales
            )
            texto = (
                f"Valor original: {resultado['original']:.17g}\n"
                f"Decimales solicitados: {resultado['decimales']}\n"
                f"Truncado: {resultado['truncado']:.17g}\n"
                f"Redondeado: {resultado['redondeado']:.17g}\n"
                f"Error de truncamiento: {resultado['error_truncamiento']:.12g}\n"
                f"Error de redondeo: {resultado['error_redondeo']:.12g}"
            )
        except (ValueError, ArithmeticError) as error:
            texto = f"ERROR: {error}"
        self._mostrar(self.salida_redondeo, texto)

    def demostrar_float(self):
        datos = op_errores.demostrar_punto_flotante()
        texto = (
            f"0.1 + 0.2 = {datos['suma_0_1_0_2']:.17g}\n"
            f"(0.1 + 0.2) == 0.3: {datos['suma_0_1_0_2_igual_0_3']}\n"
            f"Épsilon float64: {datos['epsilon_float64']:.17g}\n"
            f"Overflow float32 simulado: {datos['overflow_float32']} "
            f"(infinito: {datos['overflow_es_infinito']})\n"
            f"Underflow float32 simulado: {datos['underflow_float32']} "
            f"(cero: {datos['underflow_es_cero']})\n"
            f"Menor normal float32: {datos['menor_normal_float32']:.8g}"
        )
        self._mostrar(self.salida_float, texto)

    def _mostrar(self, textbox, texto):
        reproducir_sonido_error(self, texto)
        textbox.delete("1.0", "end")
        textbox.insert("1.0", texto)
