import customtkinter as ctk

import vectores.conversionesVectores as conv
import vectores.eliminacionVectores as ev


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AppCalculadoraVectores(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Calculadora de Vectores - FIA UAM")
        self.geometry("980x780")

        self.vector_u_entries = []
        self.vector_v_entries = []

        self.crear_frame_superior()
        self.crear_frame_central()
        self.crear_frame_inferior()

        self.generar_vectores()

    # ============================================================
    # FRAME SUPERIOR
    # ============================================================

    def crear_frame_superior(self):

        self.frame_sup = ctk.CTkFrame(self)
        self.frame_sup.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        lbl_titulo = ctk.CTkLabel(
            self.frame_sup,
            text="Dimensión:",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        lbl_titulo.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.entry_dimension = ctk.CTkEntry(
            self.frame_sup,
            width=60
        )

        self.entry_dimension.insert(
            0,
            "3"
        )

        self.entry_dimension.pack(
            side="left",
            padx=5
        )

        btn_generar = ctk.CTkButton(
            self.frame_sup,
            text="Generar Vectores",
            command=self.generar_vectores
        )

        btn_generar.pack(
            side="left",
            padx=15
        )

        btn_limpiar = ctk.CTkButton(
            self.frame_sup,
            text="Limpiar Valores",
            fg_color="#555555",
            hover_color="#333333",
            command=self.limpiar_entradas
        )

        btn_limpiar.pack(
            side="left",
            padx=5
        )

    # ============================================================
    # FRAME CENTRAL
    # ============================================================

    def crear_frame_central(self):

        self.frame_centro = ctk.CTkScrollableFrame(
            self,
            label_text="Vectores"
        )

        self.frame_centro.pack(
            pady=10,
            padx=20,
            fill="both",
            expand=True
        )

    # ============================================================
    # FRAME INFERIOR
    # ============================================================

    def crear_frame_inferior(self):

        self.frame_inf = ctk.CTkFrame(self)

        self.frame_inf.pack(
            pady=10,
            padx=20,
            fill="both",
            expand=True
        )

        subframe_acciones = ctk.CTkFrame(
            self.frame_inf,
            fg_color="transparent"
        )

        subframe_acciones.pack(
            fill="x",
            pady=5,
            padx=10
        )

        self.opcion_operacion = ctk.CTkOptionMenu(
            subframe_acciones,
            values=[
                "Suma",
                "Resta",
                "Multiplicación por escalar",
                "Producto punto",
                "Magnitud de u",
                "Magnitud de v",
                "Normalizar u",
                "Normalizar v"
            ]
        )

        self.opcion_operacion.pack(
            side="left",
            padx=(0, 10)
        )

        self.entry_escalar = ctk.CTkEntry(
            subframe_acciones,
            width=100,
            placeholder_text="Escalar"
        )

        self.entry_escalar.pack(
            side="left",
            padx=(0, 10)
        )

        self.opcion_numform = ctk.CTkOptionMenu(
            subframe_acciones,
            values=[
                "Fracciones",
                "Decimales"
            ]
        )

        self.opcion_numform.pack(
            side="left",
            padx=(0, 10)
        )

        btn_calcular = ctk.CTkButton(
            subframe_acciones,
            text="Calcular",
            fg_color="green",
            hover_color="darkgreen",
            font=ctk.CTkFont(
                weight="bold"
            ),
            command=self.accion_calcular
        )

        btn_calcular.pack(
            side="left"
        )

        self.txt_resultados = ctk.CTkTextbox(
            self.frame_inf,
            font=("Courier New", 12)
        )

        self.txt_resultados.pack(
            pady=10,
            padx=10,
            fill="both",
            expand=True
        )

        self._escribir_en_visor(
            "Ingrese los componentes de los vectores "
            "y seleccione una operación."
        )

    # ============================================================
    # GENERAR VECTORES
    # ============================================================

    def generar_vectores(self):

        for widget in self.frame_centro.winfo_children():
            widget.destroy()

        self.vector_u_entries.clear()
        self.vector_v_entries.clear()

        try:
            dimension = int(
                self.entry_dimension.get()
            )

            if dimension <= 0:
                raise ValueError

        except ValueError:

            self._escribir_en_visor(
                "ERROR: Ingrese una dimensión "
                "entera positiva válida."
            )

            return

        # Encabezado del vector u

        lbl_u = ctk.CTkLabel(
            self.frame_centro,
            text="Vector u",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        lbl_u.grid(
            row=0,
            column=0,
            padx=20,
            pady=10
        )

        # Encabezado del vector v

        lbl_v = ctk.CTkLabel(
            self.frame_centro,
            text="Vector v",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        lbl_v.grid(
            row=0,
            column=1,
            padx=20,
            pady=10
        )

        for i in range(dimension):

            lbl_componente = ctk.CTkLabel(
                self.frame_centro,
                text=f"Componente {i + 1}"
            )

            lbl_componente.grid(
                row=i + 1,
                column=2,
                padx=10,
                pady=4
            )

            entry_u = ctk.CTkEntry(
                self.frame_centro,
                width=100,
                justify="center"
            )

            entry_u.grid(
                row=i + 1,
                column=0,
                padx=10,
                pady=4
            )

            entry_v = ctk.CTkEntry(
                self.frame_centro,
                width=100,
                justify="center"
            )

            entry_v.grid(
                row=i + 1,
                column=1,
                padx=10,
                pady=4
            )

            self.vector_u_entries.append(
                entry_u
            )

            self.vector_v_entries.append(
                entry_v
            )

    # ============================================================
    # LIMPIAR ENTRADAS
    # ============================================================

    def limpiar_entradas(self):

        for entry in self.vector_u_entries:
            entry.delete(
                0,
                "end"
            )

        for entry in self.vector_v_entries:
            entry.delete(
                0,
                "end"
            )

        self.entry_escalar.delete(
            0,
            "end"
        )

        self._escribir_en_visor(
            "Campos limpios. Ingrese nuevos valores."
        )

    # ============================================================
    # OBTENER VECTOR U
    # ============================================================

    def obtener_vector_u(self):

        vector = []

        for i, entry in enumerate(
            self.vector_u_entries
        ):

            valor = entry.get().strip()

            if not valor:

                raise ValueError(
                    f"La componente u{i + 1} está vacía."
                )

            numero = conv.convertir_a_decimal(
                valor
            )

            if numero is None:

                raise ValueError(
                    f"El valor '{valor}' en u{i + 1} "
                    "no es válido."
                )

            vector.append(
                numero
            )

        return vector

    # ============================================================
    # OBTENER VECTOR V
    # ============================================================

    def obtener_vector_v(self):

        vector = []

        for i, entry in enumerate(
            self.vector_v_entries
        ):

            valor = entry.get().strip()

            if not valor:

                raise ValueError(
                    f"La componente v{i + 1} está vacía."
                )

            numero = conv.convertir_a_decimal(
                valor
            )

            if numero is None:

                raise ValueError(
                    f"El valor '{valor}' en v{i + 1} "
                    "no es válido."
                )

            vector.append(
                numero
            )

        return vector

    # ============================================================
    # OBTENER ESCALAR
    # ============================================================

    def obtener_escalar(self):

        valor = self.entry_escalar.get().strip()

        if not valor:

            raise ValueError(
                "Debe ingresar un escalar."
            )

        numero = conv.convertir_a_decimal(
            valor
        )

        if numero is None:

            raise ValueError(
                f"El valor '{valor}' no es un escalar válido."
            )

        return numero

    # ============================================================
    # FORMATEAR VECTOR
    # ============================================================

    def vector_a_string(
        self,
        vector,
        nombre="Vector"
    ):

        formato = self.opcion_numform.get()

        valores = []

        for componente in vector:

            if formato == "Fracciones":

                valores.append(
                    conv.convertir_a_fraccion(
                        componente
                    )
                )

            else:

                valores.append(
                    f"{componente:.6f}".rstrip("0").rstrip(".")
                )

        resultado = [
            f"{nombre} = ["
            + ", ".join(valores)
            + "]"
        ]

        return "\n".join(resultado)

    # ============================================================
    # CALCULAR OPERACION
    # ============================================================

    def accion_calcular(self):

        try:

            vector_u = self.obtener_vector_u()
            vector_v = self.obtener_vector_v()

            operacion = self.opcion_operacion.get()

            salida = []

            salida.append(
                "========================================================="
            )

            salida.append(
                "           CALCULADORA DE VECTORES"
            )

            salida.append(
                "=========================================================\n"
            )

            salida.append(
                self.vector_a_string(
                    vector_u,
                    "u"
                )
            )

            salida.append(
                self.vector_a_string(
                    vector_v,
                    "v"
                )
            )

            salida.append("")

            # ----------------------------------------------------
            # SUMA
            # ----------------------------------------------------

            if operacion == "Suma":

                resultado = ev.sumar_vectores(
                    vector_u,
                    vector_v
                )

                salida.append(
                    "--- SUMA DE VECTORES ---"
                )

                salida.append(
                    "u + v"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Resultado"
                    )
                )

            # ----------------------------------------------------
            # RESTA
            # ----------------------------------------------------

            elif operacion == "Resta":

                resultado = ev.restar_vectores(
                    vector_u,
                    vector_v
                )

                salida.append(
                    "--- RESTA DE VECTORES ---"
                )

                salida.append(
                    "u - v"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Resultado"
                    )
                )

            # ----------------------------------------------------
            # MULTIPLICACION POR ESCALAR
            # ----------------------------------------------------

            elif operacion == "Multiplicación por escalar":

                escalar = self.obtener_escalar()

                resultado = ev.multiplicar_vector_escalar(
                    vector_u,
                    escalar
                )

                salida.append(
                    "--- MULTIPLICACIÓN POR ESCALAR ---"
                )

                salida.append(
                    f"Escalar = {escalar}"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Resultado"
                    )
                )

            # ----------------------------------------------------
            # PRODUCTO PUNTO
            # ----------------------------------------------------

            elif operacion == "Producto punto":

                resultado = ev.producto_punto(
                    vector_u,
                    vector_v
                )

                salida.append(
                    "--- PRODUCTO PUNTO ---"
                )

                salida.append(
                    f"u · v = {resultado:.6f}"
                )

            # ----------------------------------------------------
            # MAGNITUD DE U
            # ----------------------------------------------------

            elif operacion == "Magnitud de u":

                resultado = ev.magnitud_vector(
                    vector_u
                )

                salida.append(
                    "--- MAGNITUD DE U ---"
                )

                salida.append(
                    f"||u|| = {resultado:.6f}"
                )

            # ----------------------------------------------------
            # MAGNITUD DE V
            # ----------------------------------------------------

            elif operacion == "Magnitud de v":

                resultado = ev.magnitud_vector(
                    vector_v
                )

                salida.append(
                    "--- MAGNITUD DE V ---"
                )

                salida.append(
                    f"||v|| = {resultado:.6f}"
                )

            # ----------------------------------------------------
            # NORMALIZAR U
            # ----------------------------------------------------

            elif operacion == "Normalizar u":

                resultado = ev.normalizar_vector(
                    vector_u
                )

                salida.append(
                    "--- NORMALIZACIÓN DE U ---"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Vector unitario"
                    )
                )

            # ----------------------------------------------------
            # NORMALIZAR V
            # ----------------------------------------------------

            elif operacion == "Normalizar v":

                resultado = ev.normalizar_vector(
                    vector_v
                )

                salida.append(
                    "--- NORMALIZACIÓN DE V ---"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Vector unitario"
                    )
                )

            self._escribir_en_visor(
                "\n".join(salida)
            )

        except ValueError as e:

            self._escribir_en_visor(
                f"ERROR DE ENTRADA:\n{str(e)}"
            )

    # ============================================================
    # ESCRIBIR EN EL VISOR
    # ============================================================

    def _escribir_en_visor(self, texto):

        self.txt_resultados.configure(
            state="normal"
        )

        self.txt_resultados.delete(
            "0.0",
            "end"
        )

        self.txt_resultados.insert(
            "0.0",
            texto
        )

        self.txt_resultados.configure(
            state="disabled"
        )


# ============================================================
# EJECUCION DE LA APLICACION
# ============================================================

if __name__ == "__main__":

    app = AppCalculadoraVectores()

    app.mainloop()