import customtkinter as ctk

import Matriciales.conversionesMatriciales as conv
import Matriciales.operacionesMatriciales as op
import Matriciales.solucionMatriciales as sol
import Matriciales.verificacionMatriciales as ver
import Matriciales.visualizacionMatriciales as vis


# ============================================================
# CONFIGURACION DE LA INTERFAZ
# ============================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ============================================================
# CLASE PRINCIPAL
# ============================================================

class AppCalculadoraMatricial(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(
            "Calculadora de Operaciones Matriciales - FIA UAM"
        )

        self.geometry(
            "1100x850"
        )

        # ----------------------------------------------------
        # Listas donde se almacenan los Entry
        # ----------------------------------------------------

        self.matriz_entries = []

        self.vector_x_entries = []

        self.vector_b_entries = []

        self.vector_y_entries = []

        # ----------------------------------------------------
        # Crear interfaz
        # ----------------------------------------------------

        self.crear_frame_superior()

        self.crear_frame_central()

        self.crear_frame_inferior()

        # ----------------------------------------------------
        # Generar matriz inicial
        # ----------------------------------------------------

        self.generar_estructura()


    # ========================================================
    # FRAME SUPERIOR
    # ========================================================

    def crear_frame_superior(self):

        self.frame_sup = ctk.CTkFrame(
            self
        )

        self.frame_sup.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # ----------------------------------------------------
        # Filas
        # ----------------------------------------------------

        lbl_filas = ctk.CTkLabel(
            self.frame_sup,
            text="Filas de A:",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        lbl_filas.pack(
            side="left",
            padx=(10, 5),
            pady=10
        )

        self.entry_filas = ctk.CTkEntry(
            self.frame_sup,
            width=60
        )

        self.entry_filas.insert(
            0,
            "3"
        )

        self.entry_filas.pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # Columnas
        # ----------------------------------------------------

        lbl_columnas = ctk.CTkLabel(
            self.frame_sup,
            text="Columnas de A:",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        lbl_columnas.pack(
            side="left",
            padx=(20, 5)
        )

        self.entry_columnas = ctk.CTkEntry(
            self.frame_sup,
            width=60
        )

        self.entry_columnas.insert(
            0,
            "3"
        )

        self.entry_columnas.pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # Generar
        # ----------------------------------------------------

        btn_generar = ctk.CTkButton(
            self.frame_sup,
            text="Generar Estructura",
            command=self.generar_estructura
        )

        btn_generar.pack(
            side="left",
            padx=15
        )

        # ----------------------------------------------------
        # Limpiar
        # ----------------------------------------------------

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


    # ========================================================
    # FRAME CENTRAL
    # ========================================================

    def crear_frame_central(self):

        self.frame_centro = ctk.CTkScrollableFrame(
            self,
            label_text="Matriz A y vectores x, b"
        )

        self.frame_centro.pack(
            pady=10,
            padx=20,
            fill="both",
            expand=True
        )


    # ========================================================
    # FRAME INFERIOR
    # ========================================================

    def crear_frame_inferior(self):

        self.frame_inf = ctk.CTkFrame(
            self
        )

        self.frame_inf.pack(
            pady=10,
            padx=20,
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Acciones
        # ----------------------------------------------------

        subframe_acciones = ctk.CTkFrame(
            self.frame_inf,
            fg_color="transparent"
        )

        subframe_acciones.pack(
            fill="x",
            pady=5,
            padx=10
        )

        # ----------------------------------------------------
        # Operacion
        # ----------------------------------------------------

        lbl_operacion = ctk.CTkLabel(
            subframe_acciones,
            text="Operación:"
        )

        lbl_operacion.pack(
            side="left",
            padx=(0, 5)
        )

        self.opcion_operacion = ctk.CTkOptionMenu(
            subframe_acciones,
            values=[
                "Producto A·x",
                "Ecuación matricial A·x = b",
                "Ecuación vectorial",
                "Conjunto solución",
                "Propiedad A(x+y) = Ax+Ay",
                "Propiedad A(cx) = c(Ax)"
            ]
        )

        self.opcion_operacion.pack(
            side="left",
            padx=(0, 15)
        )

        # ----------------------------------------------------
        # Escalar
        # ----------------------------------------------------

        self.entry_escalar = ctk.CTkEntry(
            subframe_acciones,
            width=100,
            placeholder_text="Escalar c"
        )

        self.entry_escalar.pack(
            side="left",
            padx=(0, 10)
        )

        # ----------------------------------------------------
        # Formato
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Calcular
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Visor
        # ----------------------------------------------------

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
            "Ingrese la matriz A y los vectores.\n\n"
            "Seleccione una operación para comenzar."
        )


    # ========================================================
    # GENERAR ESTRUCTURA
    # ========================================================

    def generar_estructura(self):

        # ----------------------------------------------------
        # Eliminar widgets anteriores
        # ----------------------------------------------------

        for widget in self.frame_centro.winfo_children():

            widget.destroy()

        # ----------------------------------------------------
        # Limpiar listas
        # ----------------------------------------------------

        self.matriz_entries.clear()

        self.vector_x_entries.clear()

        self.vector_b_entries.clear()

        self.vector_y_entries.clear()

        # ----------------------------------------------------
        # Obtener dimensiones
        # ----------------------------------------------------

        try:

            filas = int(
                self.entry_filas.get()
            )

            columnas = int(
                self.entry_columnas.get()
            )

            if filas <= 0 or columnas <= 0:

                raise ValueError

        except ValueError:

            self._escribir_en_visor(
                "ERROR: Las filas y columnas "
                "deben ser enteros positivos."
            )

            return

        # ----------------------------------------------------
        # Titulo A
        # ----------------------------------------------------

        lbl_a = ctk.CTkLabel(
            self.frame_centro,
            text="Matriz A",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        lbl_a.grid(
            row=0,
            column=0,
            columnspan=columnas,
            padx=10,
            pady=10
        )

        # ----------------------------------------------------
        # Matriz A
        # ----------------------------------------------------

        for i in range(filas):

            fila_entries = []

            for j in range(columnas):

                entry = ctk.CTkEntry(
                    self.frame_centro,
                    width=75,
                    justify="center"
                )

                entry.grid(
                    row=i + 1,
                    column=j,
                    padx=4,
                    pady=4
                )

                fila_entries.append(
                    entry
                )

            self.matriz_entries.append(
                fila_entries
            )

        # ----------------------------------------------------
        # Separacion visual
        # ----------------------------------------------------

        columna_inicio = columnas + 1

        # ----------------------------------------------------
        # Vector x
        # ----------------------------------------------------

        lbl_x = ctk.CTkLabel(
            self.frame_centro,
            text="Vector x",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        lbl_x.grid(
            row=0,
            column=columna_inicio,
            padx=20,
            pady=10
        )

        for i in range(columnas):

            entry_x = ctk.CTkEntry(
                self.frame_centro,
                width=75,
                justify="center"
            )

            entry_x.grid(
                row=i + 1,
                column=columna_inicio,
                padx=10,
                pady=4
            )

            self.vector_x_entries.append(
                entry_x
            )

        # ----------------------------------------------------
        # Vector b
        # ----------------------------------------------------

        columna_b = columna_inicio + 1

        lbl_b = ctk.CTkLabel(
            self.frame_centro,
            text="Vector b",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        lbl_b.grid(
            row=0,
            column=columna_b,
            padx=20,
            pady=10
        )

        for i in range(filas):

            entry_b = ctk.CTkEntry(
                self.frame_centro,
                width=75,
                justify="center"
            )

            entry_b.grid(
                row=i + 1,
                column=columna_b,
                padx=10,
                pady=4
            )

            self.vector_b_entries.append(
                entry_b
            )

        # ----------------------------------------------------
        # Vector y
        # ----------------------------------------------------

        columna_y = columna_b + 1

        lbl_y = ctk.CTkLabel(
            self.frame_centro,
            text="Vector y",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        lbl_y.grid(
            row=0,
            column=columna_y,
            padx=20,
            pady=10
        )

        for i in range(columnas):

            entry_y = ctk.CTkEntry(
                self.frame_centro,
                width=75,
                justify="center"
            )

            entry_y.grid(
                row=i + 1,
                column=columna_y,
                padx=10,
                pady=4
            )

            self.vector_y_entries.append(
                entry_y
            )


    # ========================================================
    # OBTENER MATRIZ A
    # ========================================================

    def obtener_matriz(self):

        matriz = []

        for i, fila_entries in enumerate(
            self.matriz_entries
        ):

            fila = []

            for j, entry in enumerate(
                fila_entries
            ):

                valor = entry.get().strip()

                if not valor:

                    raise ValueError(
                        f"A[{i + 1}][{j + 1}] está vacía."
                    )

                numero = conv.convertir_a_decimal(
                    valor
                )

                if numero is None:

                    raise ValueError(
                        f"El valor '{valor}' en "
                        f"A[{i + 1}][{j + 1}] no es válido."
                    )

                fila.append(
                    numero
                )

            matriz.append(
                fila
            )

        return matriz


    # ========================================================
    # OBTENER VECTOR X
    # ========================================================

    def obtener_vector_x(self):

        vector = []

        for i, entry in enumerate(
            self.vector_x_entries
        ):

            valor = entry.get().strip()

            if not valor:

                raise ValueError(
                    f"x{i + 1} está vacío."
                )

            numero = conv.convertir_a_decimal(
                valor
            )

            if numero is None:

                raise ValueError(
                    f"El valor '{valor}' en "
                    f"x{i + 1} no es válido."
                )

            vector.append(
                numero
            )

        return vector


    # ========================================================
    # OBTENER VECTOR B
    # ========================================================

    def obtener_vector_b(self):

        vector = []

        for i, entry in enumerate(
            self.vector_b_entries
        ):

            valor = entry.get().strip()

            if not valor:

                raise ValueError(
                    f"b{i + 1} está vacío."
                )

            numero = conv.convertir_a_decimal(
                valor
            )

            if numero is None:

                raise ValueError(
                    f"El valor '{valor}' en "
                    f"b{i + 1} no es válido."
                )

            vector.append(
                numero
            )

        return vector


    # ========================================================
    # OBTENER VECTOR Y
    # ========================================================

    def obtener_vector_y(self):

        vector = []

        for i, entry in enumerate(
            self.vector_y_entries
        ):

            valor = entry.get().strip()

            if not valor:

                raise ValueError(
                    f"y{i + 1} está vacío."
                )

            numero = conv.convertir_a_decimal(
                valor
            )

            if numero is None:

                raise ValueError(
                    f"El valor '{valor}' en "
                    f"y{i + 1} no es válido."
                )

            vector.append(
                numero
            )

        return vector


    # ========================================================
    # OBTENER ESCALAR
    # ========================================================

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


    # ========================================================
    # FORMATEAR MATRIZ
    # ========================================================

    def matriz_a_string(
        self,
        matriz,
        nombre="A"
    ):

        formato = self.opcion_numform.get()

        salida = [
            f"{nombre} ="
        ]

        for fila in matriz:

            valores = []

            for valor in fila:

                if formato == "Fracciones":

                    valores.append(
                        conv.convertir_a_fraccion(
                            valor
                        )
                    )

                else:

                    valores.append(
                        f"{valor:.6f}".rstrip(
                            "0"
                        ).rstrip(
                            "."
                        )
                    )

            salida.append(
                "| "
                + "   ".join(valores)
                + " |"
            )

        return "\n".join(
            salida
        )


    # ========================================================
    # FORMATEAR VECTOR
    # ========================================================

    def vector_a_string(
        self,
        vector,
        nombre="x"
    ):

        formato = self.opcion_numform.get()

        salida = [
            f"{nombre} ="
        ]

        for valor in vector:

            if formato == "Fracciones":

                valor_texto = (
                    conv.convertir_a_fraccion(
                        valor
                    )
                )

            else:

                valor_texto = (
                    f"{valor:.6f}"
                    .rstrip("0")
                    .rstrip(".")
                )

            salida.append(
                f"| {valor_texto:>10} |"
            )

        return "\n".join(
            salida
        )


    # ========================================================
    # CALCULAR
    # ========================================================

    def accion_calcular(self):

        try:

            matriz = self.obtener_matriz()

            vector_x = self.obtener_vector_x()

            vector_b = self.obtener_vector_b()

            operacion = (
                self.opcion_operacion.get()
            )

            salida = []

            # ------------------------------------------------
            # PRODUCTO A·x
            # ------------------------------------------------

            if operacion == "Producto A·x":

                resultado, pasos = (
                    op.producto_matriz_vector_detallado(
                        matriz,
                        vector_x
                    )
                )

                salida.append(
                    "========================================================="
                )

                salida.append(
                    "             PRODUCTO MATRIZ-VECTOR"
                )

                salida.append(
                    "=========================================================\n"
                )

                salida.append(
                    self.matriz_a_string(
                        matriz,
                        "A"
                    )
                )

                salida.append("")

                salida.append(
                    self.vector_a_string(
                        vector_x,
                        "x"
                    )
                )

                salida.append("")

                salida.append(
                    "--- REGLA FILA-VECTOR ---"
                )

                for paso in pasos:

                    salida.append(
                        paso
                    )

                salida.append("")

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Ax"
                    )
                )

            # ------------------------------------------------
            # ECUACION MATRICIAL
            # ------------------------------------------------

            elif (
                operacion
                == "Ecuación matricial A·x = b"
            ):

                resultado, pasos = (
                    op.producto_matriz_vector_detallado(
                        matriz,
                        vector_x
                    )
                )

                cumple = ver.verificar_vector(
                    resultado,
                    vector_b
                )

                salida.append(
                    "========================================================="
                )

                salida.append(
                    "              ECUACIÓN MATRICIAL"
                )

                salida.append(
                    "=========================================================\n"
                )

                salida.append(
                    self.matriz_a_string(
                        matriz,
                        "A"
                    )
                )

                salida.append("")

                salida.append(
                    self.vector_a_string(
                        vector_x,
                        "x"
                    )
                )

                salida.append("")

                salida.append(
                    self.vector_a_string(
                        vector_b,
                        "b"
                    )
                )

                salida.append("")

                salida.append(
                    "Comprobación de A·x = b:"
                )

                for paso in pasos:

                    salida.append(
                        paso
                    )

                salida.append("")

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Ax"
                    )
                )

                salida.append("")

                if cumple:

                    salida.append(
                        "RESULTADO: A·x = b"
                    )

                    salida.append(
                        "El vector x satisface la ecuación."
                    )

                else:

                    salida.append(
                        "RESULTADO: A·x ≠ b"
                    )

                    salida.append(
                        "El vector x no satisface "
                        "la ecuación."
                    )

            # ------------------------------------------------
            # ECUACION VECTORIAL
            # ------------------------------------------------

            elif operacion == "Ecuación vectorial":

                columnas = op.obtener_columnas(
                    matriz
                )

                salida.append(
                    "========================================================="
                )

                salida.append(
                    "                ECUACIÓN VECTORIAL"
                )

                salida.append(
                    "=========================================================\n"
                )

                salida.append(
                    "Las columnas de A representan "
                    "los vectores de la ecuación:"
                )

                salida.append("")

                for i, columna in enumerate(
                    columnas
                ):

                    salida.append(
                        self.vector_a_string(
                            columna,
                            f"a{i + 1}"
                        )
                    )

                    salida.append("")

                salida.append(
                    "Ecuación:"
                )

                terminos = []

                for i in range(
                    len(columnas)
                ):

                    terminos.append(
                        f"x{i + 1}·a{i + 1}"
                    )

                salida.append(
                    " + ".join(
                        terminos
                    )
                    + " = b"
                )

                salida.append("")

                salida.append(
                    "Valores de x:"
                )

                salida.append(
                    self.vector_a_string(
                        vector_x,
                        "x"
                    )
                )

                resultado = (
                    op.combinacion_lineal(
                        columnas,
                        vector_x
                    )
                )

                salida.append("")

                salida.append(
                    "Resultado de la combinación lineal:"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "A·x"
                    )
                )

                salida.append("")

                if ver.verificar_vector(
                    resultado,
                    vector_b
                ):

                    salida.append(
                        "La ecuación vectorial se cumple."
                    )

                else:

                    salida.append(
                        "La ecuación vectorial no se cumple."
                    )

            # ------------------------------------------------
            # CONJUNTO SOLUCION
            # ------------------------------------------------

            elif operacion == "Conjunto solución":

                informacion = (
                    sol.obtener_conjunto_solucion(
                        matriz,
                        vector_b
                    )
                )

                salida.append(
                    "========================================================="
                )

                salida.append(
                    "                CONJUNTO SOLUCIÓN"
                )

                salida.append(
                    "=========================================================\n"
                )

                salida.append(
                    self.matriz_a_string(
                        matriz,
                        "A"
                    )
                )

                salida.append("")

                salida.append(
                    self.vector_a_string(
                        vector_b,
                        "b"
                    )
                )

                salida.append("")

                salida.append(
                    vis.conjunto_solucion_a_string(
                        informacion
                    )
                )

            # ------------------------------------------------
            # PROPIEDAD DISTRIBUTIVA
            # ------------------------------------------------

            elif (
                operacion
                == "Propiedad A(x+y) = Ax+Ay"
            ):

                vector_y = (
                    self.obtener_vector_y()
                )

                izquierda, derecha = (
                    op.verificar_distributividad_suma(
                        matriz,
                        vector_x,
                        vector_y
                    )
                )

                salida.append(
                    "========================================================="
                )

                salida.append(
                    "       PROPIEDAD DISTRIBUTIVA DEL PRODUCTO"
                )

                salida.append(
                    "=========================================================\n"
                )

                salida.append(
                    "A(x + y) = Ax + Ay"
                )

                salida.append("")

                salida.append(
                    self.vector_a_string(
                        vector_x,
                        "x"
                    )
                )

                salida.append("")

                salida.append(
                    self.vector_a_string(
                        vector_y,
                        "y"
                    )
                )

                salida.append("")

                salida.append(
                    "Lado izquierdo:"
                )

                salida.append(
                    "A(x + y)"
                )

                salida.append(
                    self.vector_a_string(
                        izquierda,
                        "Resultado"
                    )
                )

                salida.append("")

                salida.append(
                    "Lado derecho:"
                )

                salida.append(
                    "Ax + Ay"
                )

                salida.append(
                    self.vector_a_string(
                        derecha,
                        "Resultado"
                    )
                )

                salida.append("")

                if ver.verificar_propiedad(
                    izquierda,
                    derecha
                ):

                    salida.append(
                        "La propiedad se cumple."
                    )

                else:

                    salida.append(
                        "La propiedad no se cumple."
                    )

            # ------------------------------------------------
            # PROPIEDAD HOMOGENEIDAD
            # ------------------------------------------------

            elif (
                operacion
                == "Propiedad A(cx) = c(Ax)"
            ):

                escalar = (
                    self.obtener_escalar()
                )

                izquierda, derecha = (
                    op.verificar_homogeneidad(
                        matriz,
                        vector_x,
                        escalar
                    )
                )

                salida.append(
                    "========================================================="
                )

                salida.append(
                    "       PROPIEDAD HOMOGÉNEA DEL PRODUCTO"
                )

                salida.append(
                    "=========================================================\n"
                )

                salida.append(
                    "A(cx) = c(Ax)"
                )

                salida.append("")

                salida.append(
                    f"Escalar c = {escalar}"
                )

                salida.append("")

                salida.append(
                    "Vector x:"
                )

                salida.append(
                    self.vector_a_string(
                        vector_x,
                        "x"
                    )
                )

                salida.append("")

                salida.append(
                    "Lado izquierdo:"
                )

                salida.append(
                    "A(cx)"
                )

                salida.append(
                    self.vector_a_string(
                        izquierda,
                        "Resultado"
                    )
                )

                salida.append("")

                salida.append(
                    "Lado derecho:"
                )

                salida.append(
                    "c(Ax)"
                )

                salida.append(
                    self.vector_a_string(
                        derecha,
                        "Resultado"
                    )
                )

                salida.append("")

                if ver.verificar_propiedad(
                    izquierda,
                    derecha
                ):

                    salida.append(
                        "La propiedad se cumple."
                    )

                else:

                    salida.append(
                        "La propiedad no se cumple."
                    )

            self._escribir_en_visor(
                "\n".join(salida)
            )

        except ValueError as e:

            self._escribir_en_visor(
                f"ERROR DE ENTRADA:\n\n{str(e)}"
            )


    # ========================================================
    # LIMPIAR ENTRADAS
    # ========================================================

    def limpiar_entradas(self):

        for fila in self.matriz_entries:

            for entry in fila:

                entry.delete(
                    0,
                    "end"
                )

        for entry in self.vector_x_entries:

            entry.delete(
                0,
                "end"
            )

        for entry in self.vector_b_entries:

            entry.delete(
                0,
                "end"
            )

        for entry in self.vector_y_entries:

            entry.delete(
                0,
                "end"
            )

        self.entry_escalar.delete(
            0,
            "end"
        )

        self._escribir_en_visor(
            "Campos limpios. "
            "Ingrese nuevos valores."
        )


    # ========================================================
    # ESCRIBIR EN EL VISOR
    # ========================================================

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

    app = AppCalculadoraMatricial()

    app.mainloop()