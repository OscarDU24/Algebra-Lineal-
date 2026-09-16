# ============================================================
# CALCULADORA DE OPERACIONES MATRICIALES
# ============================================================

import customtkinter as ctk

import Matriciales.operacionesMatriciales as op
import Matriciales.conversionesMatriciales as conv
import Matriciales.solucionMatriciales as sol
import Matriciales.visualizacionMatriciales as vis


# ============================================================
# CONFIGURACION DE LA INTERFAZ
# ============================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ============================================================
# CLASE PRINCIPAL
# ============================================================

class AppCalculadoraMatriciales(ctk.CTk):

    # ========================================================
    # INICIALIZAR APLICACION
    # ========================================================

    def __init__(self):

        super().__init__()

        self.title(
            "Calculadora de Operaciones Matriciales - FIA UAM"
        )

        self.geometry(
            "980x780"
        )

        self.minsize(
            900,
            700
        )

        self.matriz_a_entries = []
        self.matriz_b_entries = []
        self.vector_x_entries = []
        self.vector_b_entries = []

        self.controles = {}

        self.crear_interfaz()

        self.cambiar_operacion()


    # ========================================================
    # INTERFAZ PRINCIPAL
    # ========================================================

    def crear_interfaz(self):

        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Calculadora de Operaciones Matriciales",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.lbl_titulo.pack(
            pady=(15, 10)
        )


        # ----------------------------------------------------
        # CONTROLES SUPERIORES
        # ----------------------------------------------------

        self.frame_sup = ctk.CTkFrame(
            self
        )

        self.frame_sup.pack(
            pady=5,
            padx=20,
            fill="x"
        )


        self.frame_controles = ctk.CTkFrame(
            self.frame_sup,
            fg_color="transparent"
        )

        self.frame_controles.pack(
            fill="x",
            padx=10,
            pady=10
        )


        # ----------------------------------------------------
        # AREA CENTRAL
        # ----------------------------------------------------

        self.frame_centro = ctk.CTkScrollableFrame(
            self,
            label_text="Datos de entrada"
        )

        self.frame_centro.pack(
            pady=10,
            padx=20,
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # CONTROLES INFERIORES
        # ----------------------------------------------------

        self.frame_inf = ctk.CTkFrame(
            self
        )

        self.frame_inf.pack(
            pady=(5, 15),
            padx=20,
            fill="x"
        )

        self.crear_controles_inferiores()


    # ========================================================
    # CONTROLES INFERIORES
    # ========================================================

    def crear_controles_inferiores(self):

        # ----------------------------------------------------
        # MENU DE OPERACION
        # ----------------------------------------------------

        self.opcion_operacion = ctk.CTkOptionMenu(
            self.frame_inf,
            values=[
                "A + B",
                "A - B",
                "cA",
                "A × B",
                "Transponer A",
                "A × x → b",
                "Resolver Ax = b"
            ],
            command=self.cambiar_operacion,
            width=180
        )

        self.opcion_operacion.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )


        # ----------------------------------------------------
        # FORMATO
        # ----------------------------------------------------

        self.label_formato = ctk.CTkLabel(
            self.frame_inf,
            text="Formato:"
        )

        self.label_formato.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )


        self.opcion_numform = ctk.CTkOptionMenu(
            self.frame_inf,
            values=[
                "Fracciones",
                "Decimales"
            ],
            width=120
        )

        self.opcion_numform.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )


        # ----------------------------------------------------
        # BOTON CALCULAR
        # ----------------------------------------------------

        self.btn_calcular = ctk.CTkButton(
            self.frame_inf,
            text="Calcular",
            fg_color="green",
            hover_color="darkgreen",
            font=ctk.CTkFont(
                weight="bold"
            ),
            command=self.calcular,
            width=110
        )

        self.btn_calcular.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )


        # ----------------------------------------------------
        # BOTON LIMPIAR
        # ----------------------------------------------------

        self.btn_limpiar = ctk.CTkButton(
            self.frame_inf,
            text="Limpiar",
            command=self.limpiar,
            width=100
        )

        self.btn_limpiar.grid(
            row=0,
            column=4,
            padx=10,
            pady=10
        )


        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        self.txt_resultados = ctk.CTkTextbox(
            self.frame_inf,
            height=150,
            font=("Courier New", 12)
        )

        self.txt_resultados.grid(
            row=1,
            column=0,
            columnspan=5,
            padx=10,
            pady=10,
            sticky="ew"
        )


        self.frame_inf.grid_columnconfigure(
            0,
            weight=1
        )


        self._escribir_en_visor(
            "Seleccione una operación."
        )


    # ========================================================
    # CAMBIAR OPERACION
    # ========================================================

    def cambiar_operacion(
        self,
        valor=None
    ):

        operacion = (
            self.opcion_operacion.get()
        )


        # ----------------------------------------------------
        # ELIMINAR CONTROLES ANTERIORES
        # ----------------------------------------------------

        for widget in (
            self.frame_controles.winfo_children()
        ):

            widget.destroy()

        self.controles.clear()


        # ----------------------------------------------------
        # A + B
        # ----------------------------------------------------

        if operacion in [
            "A + B",
            "A - B"
        ]:

            self.crear_control_dimension(
                "Filas de A:",
                0,
                2
            )

            self.crear_control_dimension(
                "Columnas de A:",
                2,
                2
            )

            self.crear_control_dimension(
                "Filas de B:",
                4,
                2
            )

            self.crear_control_dimension(
                "Columnas de B:",
                6,
                2
            )

            self.crear_boton_generar()


        # ----------------------------------------------------
        # cA
        # ----------------------------------------------------

        elif operacion == "cA":

            self.crear_control_dimension(
                "Filas de A:",
                0,
                2
            )

            self.crear_control_dimension(
                "Columnas de A:",
                2,
                2
            )

            self.crear_control_escalar(
                4
            )

            self.crear_boton_generar()


        # ----------------------------------------------------
        # A × B
        # ----------------------------------------------------

        elif operacion == "A × B":

            self.crear_control_dimension(
                "Filas de A:",
                0,
                2
            )

            self.crear_control_dimension(
                "Columnas de A:",
                2,
                2
            )

            self.crear_control_dimension(
                "Filas de B:",
                4,
                2
            )

            self.crear_control_dimension(
                "Columnas de B:",
                6,
                2
            )

            self.crear_boton_generar()


        # ----------------------------------------------------
        # TRANSPONER A
        # ----------------------------------------------------

        elif operacion == "Transponer A":

            self.crear_control_dimension(
                "Filas de A:",
                0,
                2
            )

            self.crear_control_dimension(
                "Columnas de A:",
                2,
                2
            )

            self.crear_boton_generar()


        # ----------------------------------------------------
        # A × x → b
        # ----------------------------------------------------

        elif operacion == "A × x → b":

            self.crear_control_dimension(
                "Filas de A:",
                0,
                2
            )

            self.crear_control_dimension(
                "Columnas de A:",
                2,
                2
            )

            self.crear_boton_generar()


        # ----------------------------------------------------
        # RESOLVER Ax = b
        # ----------------------------------------------------

        elif operacion == "Resolver Ax = b":

            self.crear_control_dimension(
                "Filas de A:",
                0,
                2
            )

            self.crear_control_dimension(
                "Columnas de A:",
                2,
                2
            )

            self.crear_boton_generar()


        # ----------------------------------------------------
        # LIMPIAR DATOS DE ENTRADA
        # ----------------------------------------------------

        self.matriz_a_entries = []
        self.matriz_b_entries = []
        self.vector_x_entries = []
        self.vector_b_entries = []

        for widget in (
            self.frame_centro.winfo_children()
        ):

            widget.destroy()

        self._escribir_en_visor(
            "Ingrese las dimensiones y presione "
            "'Generar'."
        )


    # ========================================================
    # CREAR CONTROL DE DIMENSION
    # ========================================================

    def crear_control_dimension(
        self,
        nombre,
        columna,
        valor_inicial
    ):

        label = ctk.CTkLabel(
            self.frame_controles,
            text=nombre
        )

        label.grid(
            row=0,
            column=columna,
            padx=(5, 3),
            pady=5
        )


        entry = ctk.CTkEntry(
            self.frame_controles,
            width=70
        )

        entry.insert(
            0,
            str(valor_inicial)
        )

        entry.grid(
            row=0,
            column=columna + 1,
            padx=(3, 10),
            pady=5
        )


        self.controles[
            nombre
        ] = entry


    # ========================================================
    # CREAR CONTROL DE ESCALAR
    # ========================================================

    def crear_control_escalar(
        self,
        columna
    ):

        label = ctk.CTkLabel(
            self.frame_controles,
            text="Escalar:"
        )

        label.grid(
            row=0,
            column=columna,
            padx=(10, 3),
            pady=5
        )


        entry = ctk.CTkEntry(
            self.frame_controles,
            width=70
        )

        entry.grid(
            row=0,
            column=columna + 1,
            padx=(3, 10),
            pady=5
        )


        self.controles[
            "Escalar:"
        ] = entry


    # ========================================================
    # CREAR BOTON GENERAR
    # ========================================================

    def crear_boton_generar(self):

        boton = ctk.CTkButton(
            self.frame_controles,
            text="Generar",
            command=self.generar_datos,
            width=90
        )

        boton.grid(
            row=0,
            column=8,
            padx=10,
            pady=5
        )


    # ========================================================
    # OBTENER ENTERO DE CONTROL
    # ========================================================

    def obtener_entero(
        self,
        nombre
    ):

        entry = self.controles.get(
            nombre
        )

        if entry is None:

            raise ValueError(
                f"No existe el campo {nombre}."
            )


        try:

            valor = int(
                entry.get()
            )

        except ValueError:

            raise ValueError(
                f"{nombre} debe ser un entero."
            )


        if valor <= 0:

            raise ValueError(
                f"{nombre} debe ser mayor que cero."
            )


        return valor


    # ========================================================
    # GENERAR DATOS
    # ========================================================

    def generar_datos(self):

        try:

            operacion = (
                self.opcion_operacion.get()
            )


            # ------------------------------------------------
            # LIMPIAR ENTRADAS ANTERIORES
            # ------------------------------------------------

            for widget in (
                self.frame_centro.winfo_children()
            ):

                widget.destroy()


            self.matriz_a_entries = []
            self.matriz_b_entries = []
            self.vector_x_entries = []
            self.vector_b_entries = []


            # ------------------------------------------------
            # DIMENSIONES DE A
            # ------------------------------------------------

            filas_a = self.obtener_entero(
                "Filas de A:"
            )

            columnas_a = self.obtener_entero(
                "Columnas de A:"
            )


            # ------------------------------------------------
            # MATRIZ A
            # ------------------------------------------------

            self.crear_matriz_a(
                filas_a,
                columnas_a
            )


            # ------------------------------------------------
            # MATRIZ B
            # ------------------------------------------------

            if operacion in [
                "A + B",
                "A - B",
                "A × B"
            ]:

                filas_b = self.obtener_entero(
                    "Filas de B:"
                )

                columnas_b = self.obtener_entero(
                    "Columnas de B:"
                )

                self.crear_matriz_b(
                    filas_b,
                    columnas_b
                )


            # ------------------------------------------------
            # A × x → b
            # ------------------------------------------------

            elif operacion == "A × x → b":

                self.crear_vector_x(
                    columnas_a
                )


            # ------------------------------------------------
            # RESOLVER Ax = b
            # ------------------------------------------------

            elif operacion == "Resolver Ax = b":

                self.crear_vector_b(
                    filas_a
                )


            self._escribir_en_visor(
                "Ingrese los valores y presione "
                "'Calcular'."
            )


        except ValueError as error:

            self.mostrar_error(
                str(error)
            )


    # ========================================================
    # CREAR MATRIZ A
    # ========================================================

    def crear_matriz_a(
        self,
        filas,
        columnas
    ):

        titulo = ctk.CTkLabel(
            self.frame_centro,
            text="Matriz A",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(10, 5)
        )


        contenedor = ctk.CTkFrame(
            self.frame_centro
        )

        contenedor.pack(
            pady=5
        )


        for i in range(filas):

            fila_entries = []

            for j in range(columnas):

                entry = ctk.CTkEntry(
                    contenedor,
                    width=75,
                    justify="center"
                )

                entry.insert(
                    0,
                    "0"
                )

                entry.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                fila_entries.append(
                    entry
                )

            self.matriz_a_entries.append(
                fila_entries
            )


    # ========================================================
    # CREAR MATRIZ B
    # ========================================================

    def crear_matriz_b(
        self,
        filas,
        columnas
    ):

        titulo = ctk.CTkLabel(
            self.frame_centro,
            text="Matriz B",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(20, 5)
        )


        contenedor = ctk.CTkFrame(
            self.frame_centro
        )

        contenedor.pack(
            pady=5
        )


        for i in range(filas):

            fila_entries = []

            for j in range(columnas):

                entry = ctk.CTkEntry(
                    contenedor,
                    width=75,
                    justify="center"
                )

                entry.insert(
                    0,
                    "0"
                )

                entry.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                fila_entries.append(
                    entry
                )

            self.matriz_b_entries.append(
                fila_entries
            )


    # ========================================================
    # CREAR VECTOR x
    # ========================================================

    def crear_vector_x(
        self,
        dimension
    ):

        titulo = ctk.CTkLabel(
            self.frame_centro,
            text="Vector x",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(20, 5)
        )


        contenedor = ctk.CTkFrame(
            self.frame_centro
        )

        contenedor.pack(
            pady=5
        )


        for i in range(dimension):

            ctk.CTkLabel(
                contenedor,
                text=f"x{i + 1}"
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=4
            )


            entry = ctk.CTkEntry(
                contenedor,
                width=100,
                justify="center"
            )

            entry.insert(
                0,
                "0"
            )

            entry.grid(
                row=i,
                column=1,
                padx=10,
                pady=4
            )


            self.vector_x_entries.append(
                entry
            )


    # ========================================================
    # CREAR VECTOR b
    # ========================================================

    def crear_vector_b(
        self,
        dimension
    ):

        titulo = ctk.CTkLabel(
            self.frame_centro,
            text="Vector b",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(20, 5)
        )


        contenedor = ctk.CTkFrame(
            self.frame_centro
        )

        contenedor.pack(
            pady=5
        )


        for i in range(dimension):

            ctk.CTkLabel(
                contenedor,
                text=f"b{i + 1}"
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=4
            )


            entry = ctk.CTkEntry(
                contenedor,
                width=100,
                justify="center"
            )

            entry.insert(
                0,
                "0"
            )

            entry.grid(
                row=i,
                column=1,
                padx=10,
                pady=4
            )


            self.vector_b_entries.append(
                entry
            )


    # ========================================================
    # OBTENER MATRIZ A
    # ========================================================

    def obtener_matriz_a(self):

        matriz = []

        for i, fila_entries in enumerate(
            self.matriz_a_entries
        ):

            fila = []

            for j, entry in enumerate(
                fila_entries
            ):

                valor = entry.get().strip()

                if not valor:

                    raise ValueError(
                        f"A[{i + 1}][{j + 1}] "
                        "está vacío."
                    )


                numero = (
                    conv.convertir_a_decimal(
                        valor
                    )
                )

                if numero is None:

                    raise ValueError(
                        f"A[{i + 1}][{j + 1}] "
                        "no contiene un número válido."
                    )


                fila.append(
                    numero
                )

            matriz.append(
                fila
            )

        return matriz


    # ========================================================
    # OBTENER MATRIZ B
    # ========================================================

    def obtener_matriz_b(self):

        matriz = []

        for i, fila_entries in enumerate(
            self.matriz_b_entries
        ):

            fila = []

            for j, entry in enumerate(
                fila_entries
            ):

                valor = entry.get().strip()

                if not valor:

                    raise ValueError(
                        f"B[{i + 1}][{j + 1}] "
                        "está vacío."
                    )


                numero = (
                    conv.convertir_a_decimal(
                        valor
                    )
                )

                if numero is None:

                    raise ValueError(
                        f"B[{i + 1}][{j + 1}] "
                        "no contiene un número válido."
                    )


                fila.append(
                    numero
                )

            matriz.append(
                fila
            )

        return matriz


    # ========================================================
    # OBTENER VECTOR x
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


            numero = (
                conv.convertir_a_decimal(
                    valor
                )
            )

            if numero is None:

                raise ValueError(
                    f"x{i + 1} no contiene "
                    "un número válido."
                )


            vector.append(
                numero
            )

        return vector


    # ========================================================
    # OBTENER VECTOR b
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


            numero = (
                conv.convertir_a_decimal(
                    valor
                )
            )

            if numero is None:

                raise ValueError(
                    f"b{i + 1} no contiene "
                    "un número válido."
                )


            vector.append(
                numero
            )

        return vector


    # ========================================================
    # OBTENER ESCALAR
    # ========================================================

    def obtener_escalar(self):

        entry = self.controles.get(
            "Escalar:"
        )

        if entry is None:

            raise ValueError(
                "No existe el campo Escalar."
            )


        valor = entry.get().strip()

        if not valor:

            raise ValueError(
                "Debe ingresar un escalar."
            )


        numero = (
            conv.convertir_a_decimal(
                valor
            )
        )

        if numero is None:

            raise ValueError(
                "El escalar no es válido."
            )


        return numero


    # ========================================================
    # CALCULAR
    # ========================================================

    def calcular(self):

        try:

            operacion = (
                self.opcion_operacion.get()
            )

            formato = (
                self.opcion_numform.get()
            )


            # ------------------------------------------------
            # A + B
            # ------------------------------------------------

            if operacion == "A + B":

                matriz_a = (
                    self.obtener_matriz_a()
                )

                matriz_b = (
                    self.obtener_matriz_b()
                )

                resultado = (
                    op.sumar_matrices(
                        matriz_a,
                        matriz_b
                    )
                )

                texto = (
                    vis.operacion_matrices_a_string(
                        matriz_a,
                        matriz_b,
                        resultado,
                        "+",
                        formato
                    )
                )


            # ------------------------------------------------
            # A - B
            # ------------------------------------------------

            elif operacion == "A - B":

                matriz_a = (
                    self.obtener_matriz_a()
                )

                matriz_b = (
                    self.obtener_matriz_b()
                )

                resultado = (
                    op.restar_matrices(
                        matriz_a,
                        matriz_b
                    )
                )

                texto = (
                    vis.operacion_matrices_a_string(
                        matriz_a,
                        matriz_b,
                        resultado,
                        "-",
                        formato
                    )
                )


            # ------------------------------------------------
            # cA
            # ------------------------------------------------

            elif operacion == "cA":

                matriz_a = (
                    self.obtener_matriz_a()
                )

                escalar = (
                    self.obtener_escalar()
                )

                resultado = (
                    op.multiplicar_matriz_escalar(
                        matriz_a,
                        escalar
                    )
                )

                texto = (
                    vis.matriz_escalar_a_string(
                        matriz_a,
                        escalar,
                        resultado,
                        formato
                    )
                )


            # ------------------------------------------------
            # A × B
            # ------------------------------------------------

            elif operacion == "A × B":

                matriz_a = (
                    self.obtener_matriz_a()
                )

                matriz_b = (
                    self.obtener_matriz_b()
                )

                resultado = (
                    op.multiplicar_matrices(
                        matriz_a,
                        matriz_b
                    )
                )

                texto = (
                    vis.producto_matrices_a_string(
                        matriz_a,
                        matriz_b,
                        resultado,
                        formato
                    )
                )


            # ------------------------------------------------
            # TRANSPONER A
            # ------------------------------------------------

            elif operacion == "Transponer A":

                matriz_a = (
                    self.obtener_matriz_a()
                )

                transpuesta = (
                    op.transponer_matriz(
                        matriz_a
                    )
                )

                texto = (
                    vis.matriz_transpuesta_a_string(
                        matriz_a,
                        transpuesta,
                        formato
                    )
                )


            # ------------------------------------------------
            # A × x → b
            #
            # A y x son conocidos.
            # Se calcula b.
            # ------------------------------------------------

            elif operacion == "A × x → b":

                matriz_a = (
                    self.obtener_matriz_a()
                )

                vector_x = (
                    self.obtener_vector_x()
                )

                vector_b, pasos = (
                    op.producto_matriz_vector_detallado(
                        matriz_a,
                        vector_x
                    )
                )

                texto = (
                    vis.producto_matriz_vector_a_string(
                        matriz_a,
                        vector_x,
                        vector_b,
                        formato
                    )
                )

                texto += (
                    "\n\n"
                    + vis.pasos_producto_matriz_vector_a_string(
                        pasos
                    )
                )


            # ------------------------------------------------
            # RESOLVER Ax = b
            #
            # A y b son conocidos.
            # Se calcula x.
            # ------------------------------------------------

            elif operacion == "Resolver Ax = b":

                matriz_a = (
                    self.obtener_matriz_a()
                )

                vector_b = (
                    self.obtener_vector_b()
                )

                informacion = (
                    sol.resolver_ecuacion_matricial(
                        matriz_a,
                        vector_b
                    )
                )

                texto = (
                    vis.ecuacion_matricial_a_string(
                        matriz_a,
                        vector_b,
                        formato
                    )
                )

                texto += (
                    "\n\n"
                    + vis.solucion_ecuacion_matricial_a_string(
                        informacion,
                        formato
                    )
                )


            else:

                raise ValueError(
                    "Operación no reconocida."
                )


            # ------------------------------------------------
            # MOSTRAR RESULTADO
            # ------------------------------------------------

            self._escribir_en_visor(
                texto
            )


        except ValueError as error:

            self.mostrar_error(
                str(error)
            )


        except Exception as error:

            self.mostrar_error(
                "Ocurrió un error inesperado:\n\n"
                + str(error)
            )


    # ========================================================
    # MOSTRAR ERROR
    # ========================================================

    def mostrar_error(
        self,
        mensaje
    ):

        self._escribir_en_visor(
            "ERROR\n\n"
            + mensaje
        )


    # ========================================================
    # ESCRIBIR EN VISOR
    # ========================================================

    def _escribir_en_visor(
        self,
        texto
    ):

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


    # ========================================================
    # LIMPIAR
    # ========================================================

    def limpiar(self):

        self.matriz_a_entries = []
        self.matriz_b_entries = []
        self.vector_x_entries = []
        self.vector_b_entries = []


        for widget in (
            self.frame_centro.winfo_children()
        ):

            widget.destroy()


        self._escribir_en_visor(
            "Seleccione una operación."
        )


# ============================================================
# EJECUTAR PROGRAMA
# ============================================================

if __name__ == "__main__":

    app = AppCalculadoraMatriciales()

    app.mainloop()