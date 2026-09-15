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
        self.minsize(900, 700)

        self.vector_entries = []
        self.vector_b_entries = []
        self.matriz_entries = []
        self.controles = {}

        self.crear_interfaz()
        self.cambiar_operacion()

    # ========================================================
    # INTERFAZ PRINCIPAL
    # ========================================================

    def crear_interfaz(self):

        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Calculadora de Vectores",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.lbl_titulo.pack(
            pady=(15, 10)
        )

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

        self.opcion_operacion = ctk.CTkOptionMenu(
            self.frame_inf,
            values=[
                "Suma",
                "Resta",
                "Multiplicación por escalar",
                "Producto punto",
                "Magnitud de u",
                "Magnitud de v",
                "Normalizar u",
                "Normalizar v",
                "Combinación lineal",
                "Descomponer matriz en vectores",
                "Matriz a ecuación vectorial",
                "Sistema a ecuación vectorial"
            ],
            command=self.cambiar_operacion
        )

        self.opcion_operacion.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.label_formato = ctk.CTkLabel(
            self.frame_inf,
            text="Formato:"
        )

        self.opcion_numform = ctk.CTkOptionMenu(
            self.frame_inf,
            values=[
                "Fracciones",
                "Decimales"
            ]
        )

        self.label_formato.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.opcion_numform.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        self.btn_calcular = ctk.CTkButton(
            self.frame_inf,
            text="Calcular",
            fg_color="green",
            hover_color="darkgreen",
            font=ctk.CTkFont(
                weight="bold"
            ),
            command=self.accion_calcular
        )

        self.btn_calcular.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )

        self.txt_resultados = ctk.CTkTextbox(
            self.frame_inf,
            height=150,
            font=("Courier New", 12)
        )

        self.txt_resultados.grid(
            row=1,
            column=0,
            columnspan=4,
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

    def cambiar_operacion(self, valor=None):

        operacion = self.opcion_operacion.get()

        # ----------------------------------------------------
        # ELIMINAR LOS CONTROLES ANTERIORES
        # ----------------------------------------------------

        for widget in self.frame_controles.winfo_children():
            widget.destroy()

        self.controles.clear()

        # ----------------------------------------------------
        # SUMA
        # ----------------------------------------------------

        if operacion == "Suma":

            self.crear_dimension(
                "Dimensión:",
                0,
                0,
                3
            )

            self.crear_cantidad_vectores(
                0,
                2
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # RESTA
        # ----------------------------------------------------

        elif operacion == "Resta":

            self.crear_dimension(
                "Dimensión:",
                0,
                0,
                3
            )

            self.crear_cantidad_vectores(
                0,
                2
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # MULTIPLICACION POR ESCALAR
        # ----------------------------------------------------

        elif operacion == "Multiplicación por escalar":

            self.crear_dimension(
                "Dimensión:",
                0,
                0,
                3
            )

            self.crear_escalar()

            self.crear_boton_generar()

        # ----------------------------------------------------
        # PRODUCTO PUNTO
        # ----------------------------------------------------

        elif operacion == "Producto punto":

            self.crear_dimension(
                "Dimensión:",
                0,
                0,
                3
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # MAGNITUD
        # ----------------------------------------------------

        elif operacion in [
            "Magnitud de u",
            "Magnitud de v"
        ]:

            self.crear_dimension(
                "Dimensión:",
                0,
                0,
                3
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # NORMALIZACION
        # ----------------------------------------------------

        elif operacion in [
            "Normalizar u",
            "Normalizar v"
        ]:

            self.crear_dimension(
                "Dimensión:",
                0,
                0,
                3
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # COMBINACION LINEAL
        # ----------------------------------------------------

        elif operacion == "Combinación lineal":

            self.crear_dimension(
                "Dimensión:",
                0,
                0,
                3
            )

            self.crear_cantidad_vectores(
                0,
                2
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # DESCOMPONER MATRIZ
        # ----------------------------------------------------

        elif operacion == "Descomponer matriz en vectores":

            self.crear_dimension(
                "Filas:",
                0,
                0,
                3
            )

            self.crear_dimension(
                "Columnas:",
                0,
                2,
                3
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # MATRIZ A ECUACION VECTORIAL
        # ----------------------------------------------------

        elif operacion == "Matriz a ecuación vectorial":

            self.crear_dimension(
                "Filas:",
                0,
                0,
                3
            )

            self.crear_dimension(
                "Columnas:",
                0,
                2,
                3
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # SISTEMA A ECUACION VECTORIAL
        # ----------------------------------------------------

        elif operacion == "Sistema a ecuación vectorial":

            self.crear_dimension(
                "Ecuaciones:",
                0,
                0,
                3
            )

            self.crear_dimension(
                "Variables:",
                0,
                2,
                3
            )

            self.crear_boton_generar()

        self.generar_datos()

    # ========================================================
    # CREAR DIMENSION
    # ========================================================

    def crear_dimension(
        self,
        texto,
        fila,
        columna,
        valor
    ):

        label = ctk.CTkLabel(
            self.frame_controles,
            text=texto
        )

        label.grid(
            row=fila,
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
            str(valor)
        )

        entry.grid(
            row=fila,
            column=columna + 1,
            padx=(3, 10),
            pady=5
        )

        self.controles[texto] = entry

    # ========================================================
    # CREAR CANTIDAD DE VECTORES
    # ========================================================

    def crear_cantidad_vectores(
        self,
        fila,
        valor
    ):

        label = ctk.CTkLabel(
            self.frame_controles,
            text="Cantidad de vectores:"
        )

        label.grid(
            row=fila,
            column=4,
            padx=(5, 3),
            pady=5
        )

        entry = ctk.CTkEntry(
            self.frame_controles,
            width=70
        )

        entry.insert(
            0,
            str(valor)
        )

        entry.grid(
            row=fila,
            column=5,
            padx=(3, 10),
            pady=5
        )

        self.controles[
            "Cantidad de vectores"
        ] = entry

    # ========================================================
    # CREAR ESCALAR
    # ========================================================

    def crear_escalar(self):

        label = ctk.CTkLabel(
            self.frame_controles,
            text="Escalar:"
        )

        label.grid(
            row=0,
            column=4,
            padx=(15, 3),
            pady=5
        )

        entry = ctk.CTkEntry(
            self.frame_controles,
            width=70
        )

        entry.grid(
            row=0,
            column=5,
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
            command=self.generar_datos
        )

        boton.grid(
            row=0,
            column=8,
            padx=10,
            pady=5
        )

    # ========================================================
    # OBTENER ENTERO
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
                f"No existe el campo {nombre}"
            )

        try:

            valor = int(
                entry.get()
            )

            if valor <= 0:

                raise ValueError

            return valor

        except ValueError:

            raise ValueError(
                f"{nombre} debe ser un entero "
                "mayor que cero."
            )

    # ========================================================
    # GENERAR DATOS
    # ========================================================

    def generar_datos(self):

        try:

            operacion = self.opcion_operacion.get()

            for widget in self.frame_centro.winfo_children():
                widget.destroy()

            self.vector_entries = []
            self.vector_b_entries = []
            self.matriz_entries = []

            # ------------------------------------------------
            # SUMA
            # ------------------------------------------------

            if operacion == "Suma":

                dimension = self.obtener_entero(
                    "Dimensión:"
                )

                cantidad = self.obtener_entero(
                    "Cantidad de vectores"
                )

                if cantidad < 2:

                    raise ValueError(
                        "La cantidad de vectores debe "
                        "ser al menos 2."
                    )

                self.crear_vectores_operacion(
                    cantidad,
                    dimension
                )

            # ------------------------------------------------
            # RESTA
            # ------------------------------------------------

            elif operacion == "Resta":

                dimension = self.obtener_entero(
                    "Dimensión:"
                )

                cantidad = self.obtener_entero(
                    "Cantidad de vectores"
                )

                if cantidad < 2:

                    raise ValueError(
                        "La cantidad de vectores debe "
                        "ser al menos 2."
                    )

                self.crear_vectores_operacion(
                    cantidad,
                    dimension
                )

            # ------------------------------------------------
            # MULTIPLICACION POR ESCALAR
            # ------------------------------------------------

            elif operacion == "Multiplicación por escalar":

                dimension = self.obtener_entero(
                    "Dimensión:"
                )

                self.crear_un_vector(
                    dimension,
                    "u"
                )

            # ------------------------------------------------
            # PRODUCTO PUNTO
            # ------------------------------------------------

            elif operacion == "Producto punto":

                dimension = self.obtener_entero(
                    "Dimensión:"
                )

                self.crear_dos_vectores(
                    dimension
                )

            # ------------------------------------------------
            # MAGNITUD
            # ------------------------------------------------

            elif operacion in [
                "Magnitud de u",
                "Magnitud de v"
            ]:

                dimension = self.obtener_entero(
                    "Dimensión:"
                )

                nombre = "u"

                if operacion == "Magnitud de v":
                    nombre = "v"

                self.crear_un_vector(
                    dimension,
                    nombre
                )

            # ------------------------------------------------
            # NORMALIZACION
            # ------------------------------------------------

            elif operacion in [
                "Normalizar u",
                "Normalizar v"
            ]:

                dimension = self.obtener_entero(
                    "Dimensión:"
                )

                nombre = "u"

                if operacion == "Normalizar v":
                    nombre = "v"

                self.crear_un_vector(
                    dimension,
                    nombre
                )

            # ------------------------------------------------
            # COMBINACION LINEAL
            # ------------------------------------------------

            elif operacion == "Combinación lineal":

                dimension = self.obtener_entero(
                    "Dimensión:"
                )

                cantidad = self.obtener_entero(
                    "Cantidad de vectores"
                )

                if cantidad < 1:

                    raise ValueError(
                        "Debe existir al menos un vector."
                    )

                self.crear_vectores_combinacion(
                    cantidad,
                    dimension
                )

                self.crear_vector_b(
                    dimension
                )

            # ------------------------------------------------
            # DESCOMPONER MATRIZ
            # ------------------------------------------------

            elif operacion == "Descomponer matriz en vectores":

                filas = self.obtener_entero(
                    "Filas:"
                )

                columnas = self.obtener_entero(
                    "Columnas:"
                )

                self.crear_matriz(
                    filas,
                    columnas
                )

            # ------------------------------------------------
            # MATRIZ A ECUACION VECTORIAL
            # ------------------------------------------------

            elif operacion == "Matriz a ecuación vectorial":

                filas = self.obtener_entero(
                    "Filas:"
                )

                columnas = self.obtener_entero(
                    "Columnas:"
                )

                self.crear_matriz(
                    filas,
                    columnas
                )

            # ------------------------------------------------
            # SISTEMA A ECUACION VECTORIAL
            # ------------------------------------------------

            elif operacion == "Sistema a ecuación vectorial":

                ecuaciones = self.obtener_entero(
                    "Ecuaciones:"
                )

                variables = self.obtener_entero(
                    "Variables:"
                )

                self.crear_sistema(
                    ecuaciones,
                    variables
                )

            self._escribir_en_visor(
                "Ingrese los valores y presione "
                "'Calcular'."
            )

        except ValueError as error:

            self._escribir_en_visor(
                f"ERROR:\n\n{error}"
            )

    # ========================================================
    # CREAR VECTORES PARA SUMA Y RESTA
    # ========================================================

    def crear_vectores_operacion(
        self,
        cantidad,
        dimension
    ):

        titulo = ctk.CTkLabel(
            self.frame_centro,
            text="Vectores",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(10, 5)
        )

        frame = ctk.CTkFrame(
            self.frame_centro
        )

        frame.pack(
            pady=10
        )

        self.vector_entries = []

        for j in range(cantidad):

            nombre = f"v{j + 1}"

            ctk.CTkLabel(
                frame,
                text=nombre,
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=0,
                column=j,
                padx=8,
                pady=8
            )

            self.vector_entries.append(
                []
            )

        for i in range(dimension):

            for j in range(cantidad):

                entry = ctk.CTkEntry(
                    frame,
                    width=75,
                    justify="center"
                )

                entry.grid(
                    row=i + 1,
                    column=j,
                    padx=5,
                    pady=4
                )

                self.vector_entries[j].append(
                    entry
                )

    # ========================================================
    # CREAR UN VECTOR
    # ========================================================

    def crear_un_vector(
        self,
        dimension,
        nombre
    ):

        titulo = ctk.CTkLabel(
            self.frame_centro,
            text=f"Vector {nombre}",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(10, 5)
        )

        frame = ctk.CTkFrame(
            self.frame_centro
        )

        frame.pack(
            pady=5
        )

        entradas = []

        for i in range(dimension):

            ctk.CTkLabel(
                frame,
                text=f"{nombre}{i + 1}"
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=4
            )

            entry = ctk.CTkEntry(
                frame,
                width=100,
                justify="center"
            )

            entry.grid(
                row=i,
                column=1,
                padx=10,
                pady=4
            )

            entradas.append(
                entry
            )

        self.vector_entries.append(
            entradas
        )

    # ========================================================
    # CREAR DOS VECTORES
    # ========================================================

    def crear_dos_vectores(
        self,
        dimension
    ):

        self.vector_entries = [
            [],
            []
        ]

        frame = ctk.CTkFrame(
            self.frame_centro
        )

        frame.pack(
            pady=10
        )

        ctk.CTkLabel(
            frame,
            text="Vector u",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=30,
            pady=10
        )

        ctk.CTkLabel(
            frame,
            text="Vector v",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).grid(
            row=0,
            column=2,
            columnspan=2,
            padx=30,
            pady=10
        )

        for i in range(dimension):

            ctk.CTkLabel(
                frame,
                text=f"u{i + 1}"
            ).grid(
                row=i + 1,
                column=0,
                padx=5,
                pady=4
            )

            entry_u = ctk.CTkEntry(
                frame,
                width=100,
                justify="center"
            )

            entry_u.grid(
                row=i + 1,
                column=1,
                padx=10,
                pady=4
            )

            ctk.CTkLabel(
                frame,
                text=f"v{i + 1}"
            ).grid(
                row=i + 1,
                column=2,
                padx=5,
                pady=4
            )

            entry_v = ctk.CTkEntry(
                frame,
                width=100,
                justify="center"
            )

            entry_v.grid(
                row=i + 1,
                column=3,
                padx=10,
                pady=4
            )

            self.vector_entries[0].append(
                entry_u
            )

            self.vector_entries[1].append(
                entry_v
            )

    # ========================================================
    # CREAR VECTORES PARA COMBINACION LINEAL
    # ========================================================

    def crear_vectores_combinacion(
        self,
        cantidad,
        dimension
    ):

        frame = ctk.CTkFrame(
            self.frame_centro
        )

        frame.pack(
            pady=10
        )

        self.vector_entries = []

        for j in range(cantidad):

            nombre = f"v{j + 1}"

            ctk.CTkLabel(
                frame,
                text=nombre,
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=0,
                column=j,
                padx=8,
                pady=8
            )

            self.vector_entries.append(
                []
            )

        for i in range(dimension):

            for j in range(cantidad):

                entry = ctk.CTkEntry(
                    frame,
                    width=75,
                    justify="center"
                )

                entry.grid(
                    row=i + 1,
                    column=j,
                    padx=5,
                    pady=4
                )

                self.vector_entries[j].append(
                    entry
                )

    # ========================================================
    # CREAR VECTOR B
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

        frame = ctk.CTkFrame(
            self.frame_centro
        )

        frame.pack(
            pady=5
        )

        self.vector_b_entries = []

        for i in range(dimension):

            ctk.CTkLabel(
                frame,
                text=f"b{i + 1}"
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=4
            )

            entry = ctk.CTkEntry(
                frame,
                width=100,
                justify="center"
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
    # CREAR MATRIZ
    # ========================================================

    def crear_matriz(
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

        frame = ctk.CTkFrame(
            self.frame_centro
        )

        frame.pack(
            pady=5
        )

        self.matriz_entries = []

        for i in range(filas):

            fila = []

            for j in range(columnas):

                entry = ctk.CTkEntry(
                    frame,
                    width=75,
                    justify="center"
                )

                entry.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                fila.append(
                    entry
                )

            self.matriz_entries.append(
                fila
            )

    # ========================================================
    # CREAR SISTEMA
    # ========================================================

    def crear_sistema(
        self,
        ecuaciones,
        variables
    ):

        titulo = ctk.CTkLabel(
            self.frame_centro,
            text="Matriz de coeficientes A",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(10, 5)
        )

        frame_a = ctk.CTkFrame(
            self.frame_centro
        )

        frame_a.pack(
            pady=5
        )

        self.matriz_entries = []

        for j in range(variables):

            ctk.CTkLabel(
                frame_a,
                text=f"x{j + 1}",
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=0,
                column=j,
                padx=8,
                pady=5
            )

        for i in range(ecuaciones):

            fila = []

            for j in range(variables):

                entry = ctk.CTkEntry(
                    frame_a,
                    width=75,
                    justify="center"
                )

                entry.grid(
                    row=i + 1,
                    column=j,
                    padx=4,
                    pady=4
                )

                fila.append(
                    entry
                )

            self.matriz_entries.append(
                fila
            )

        titulo_b = ctk.CTkLabel(
            self.frame_centro,
            text="Vector b",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        titulo_b.pack(
            pady=(20, 5)
        )

        frame_b = ctk.CTkFrame(
            self.frame_centro
        )

        frame_b.pack(
            pady=5
        )

        self.vector_b_entries = []

        for i in range(ecuaciones):

            ctk.CTkLabel(
                frame_b,
                text=f"b{i + 1}"
            ).grid(
                row=i,
                column=0,
                padx=10,
                pady=4
            )

            entry = ctk.CTkEntry(
                frame_b,
                width=100,
                justify="center"
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
    # OBTENER VECTOR
    # ========================================================

    def obtener_vector(
        self,
        entradas,
        nombre
    ):

        vector = []

        for i, entry in enumerate(
            entradas
        ):

            valor = entry.get().strip()

            if not valor:

                raise ValueError(
                    f"La componente {nombre}{i + 1} "
                    "está vacía."
                )

            numero = conv.convertir_a_decimal(
                valor
            )

            if numero is None:

                raise ValueError(
                    f"El valor '{valor}' en "
                    f"{nombre}{i + 1} no es válido."
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
                "No existe el campo Escalar:"
            )

        valor = entry.get().strip()

        if not valor:

            raise ValueError(
                "Debe ingresar un escalar."
            )

        numero = conv.convertir_a_decimal(
            valor
        )

        if numero is None:

            raise ValueError(
                f"El valor '{valor}' no es un "
                "escalar válido."
            )

        return numero

    # ========================================================
    # OBTENER MATRIZ
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
                        f"A[{i + 1}][{j + 1}] "
                        "está vacío."
                    )

                numero = conv.convertir_a_decimal(
                    valor
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
    # FORMATEAR NUMERO
    # ========================================================

    def formatear_numero(
        self,
        valor
    ):

        if self.opcion_numform.get() == "Fracciones":

            return conv.convertir_a_fraccion(
                valor
            )

        return (
            f"{valor:.6f}"
            .rstrip("0")
            .rstrip(".")
        )

    # ========================================================
    # VECTOR A STRING
    # ========================================================

    def vector_a_string(
        self,
        vector,
        nombre="Vector"
    ):

        valores = []

        for componente in vector:

            valores.append(
                self.formatear_numero(
                    componente
                )
            )

        return (
            f"{nombre} = ["
            + ", ".join(valores)
            + "]"
        )

    # ========================================================
    # VECTOR SIN NOMBRE
    # ========================================================

    def vector_simple_a_string(
        self,
        vector
    ):

        valores = []

        for componente in vector:

            valores.append(
                self.formatear_numero(
                    componente
                )
            )

        return (
            "["
            + ", ".join(valores)
            + "]"
        )

    # ========================================================
    # MATRIZ A STRING
    # ========================================================

    def matriz_a_string(
        self,
        matriz
    ):

        lineas = []

        for fila in matriz:

            valores = []

            for elemento in fila:

                valores.append(
                    self.formatear_numero(
                        elemento
                    )
                )

            lineas.append(
                "[ "
                + "  ".join(valores)
                + " ]"
            )

        return "\n".join(
            lineas
        )

    # ========================================================
    # CALCULAR
    # ========================================================

    def accion_calcular(self):

        try:

            operacion = self.opcion_operacion.get()

            salida = []

            salida.append(
                "========================================================="
            )

            salida.append(
                "             CALCULADORA DE VECTORES"
            )

            salida.append(
                "=========================================================\n"
            )

            # ------------------------------------------------
            # SUMA
            # ------------------------------------------------

            if operacion == "Suma":

                vectores = []

                for i, entradas in enumerate(
                    self.vector_entries
                ):

                    vector = self.obtener_vector(
                        entradas,
                        f"v{i + 1}"
                    )

                    vectores.append(
                        vector
                    )

                resultado = ev.sumar_vectores(
                    vectores
                )

                for i, vector in enumerate(
                    vectores
                ):

                    salida.append(
                        self.vector_a_string(
                            vector,
                            f"v{i + 1}"
                        )
                    )

                salida.append(
                    "\n--- SUMA ---"
                )

                terminos = []

                for i in range(
                    len(vectores)
                ):

                    terminos.append(
                        f"v{i + 1}"
                    )

                salida.append(
                    " + ".join(terminos)
                    + " = "
                    + self.vector_simple_a_string(
                        resultado
                    )
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Resultado"
                    )
                )

            # ------------------------------------------------
            # RESTA
            # ------------------------------------------------

            elif operacion == "Resta":

                vectores = []

                for i, entradas in enumerate(
                    self.vector_entries
                ):

                    vector = self.obtener_vector(
                        entradas,
                        f"v{i + 1}"
                    )

                    vectores.append(
                        vector
                    )

                resultado = ev.restar_vectores(
                    vectores
                )

                for i, vector in enumerate(
                    vectores
                ):

                    salida.append(
                        self.vector_a_string(
                            vector,
                            f"v{i + 1}"
                        )
                    )

                salida.append(
                    "\n--- RESTA ---"
                )

                terminos = []

                for i in range(
                    len(vectores)
                ):

                    if i == 0:

                        terminos.append(
                            f"v{i + 1}"
                        )

                    else:

                        terminos.append(
                            f"- v{i + 1}"
                        )

                salida.append(
                    " ".join(terminos)
                    + " = "
                    + self.vector_simple_a_string(
                        resultado
                    )
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Resultado"
                    )
                )

            # ------------------------------------------------
            # MULTIPLICACION POR ESCALAR
            # ------------------------------------------------

            elif operacion == "Multiplicación por escalar":

                u = self.obtener_vector(
                    self.vector_entries[0],
                    "u"
                )

                escalar = self.obtener_escalar()

                resultado = (
                    ev.multiplicar_vector_escalar(
                        u,
                        escalar
                    )
                )

                salida.append(
                    self.vector_a_string(
                        u,
                        "u"
                    )
                )

                salida.append(
                    "Escalar = "
                    + self.formatear_numero(
                        escalar
                    )
                )

                salida.append(
                    "\n--- RESULTADO ---"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "cu"
                    )
                )

            # ------------------------------------------------
            # PRODUCTO PUNTO
            # ------------------------------------------------

            elif operacion == "Producto punto":

                u = self.obtener_vector(
                    self.vector_entries[0],
                    "u"
                )

                v = self.obtener_vector(
                    self.vector_entries[1],
                    "v"
                )

                resultado = ev.producto_punto(
                    u,
                    v
                )

                salida.append(
                    self.vector_a_string(
                        u,
                        "u"
                    )
                )

                salida.append(
                    self.vector_a_string(
                        v,
                        "v"
                    )
                )

                salida.append(
                    "\n--- PRODUCTO PUNTO ---"
                )

                salida.append(
                    "u · v = "
                    + self.formatear_numero(
                        resultado
                    )
                )

            # ------------------------------------------------
            # MAGNITUD DE U
            # ------------------------------------------------

            elif operacion == "Magnitud de u":

                u = self.obtener_vector(
                    self.vector_entries[0],
                    "u"
                )

                resultado = ev.magnitud_vector(
                    u
                )

                salida.append(
                    self.vector_a_string(
                        u,
                        "u"
                    )
                )

                salida.append(
                    "\n--- MAGNITUD ---"
                )

                salida.append(
                    "||u|| = "
                    + self.formatear_numero(
                        resultado
                    )
                )

            # ------------------------------------------------
            # MAGNITUD DE V
            # ------------------------------------------------

            elif operacion == "Magnitud de v":

                v = self.obtener_vector(
                    self.vector_entries[0],
                    "v"
                )

                resultado = ev.magnitud_vector(
                    v
                )

                salida.append(
                    self.vector_a_string(
                        v,
                        "v"
                    )
                )

                salida.append(
                    "\n--- MAGNITUD ---"
                )

                salida.append(
                    "||v|| = "
                    + self.formatear_numero(
                        resultado
                    )
                )

            # ------------------------------------------------
            # NORMALIZAR U
            # ------------------------------------------------

            elif operacion == "Normalizar u":

                u = self.obtener_vector(
                    self.vector_entries[0],
                    "u"
                )

                resultado = ev.normalizar_vector(
                    u
                )

                salida.append(
                    self.vector_a_string(
                        u,
                        "u"
                    )
                )

                salida.append(
                    "\n--- VECTOR UNITARIO ---"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "u/||u||"
                    )
                )

            # ------------------------------------------------
            # NORMALIZAR V
            # ------------------------------------------------

            elif operacion == "Normalizar v":

                v = self.obtener_vector(
                    self.vector_entries[0],
                    "v"
                )

                resultado = ev.normalizar_vector(
                    v
                )

                salida.append(
                    self.vector_a_string(
                        v,
                        "v"
                    )
                )

                salida.append(
                    "\n--- VECTOR UNITARIO ---"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "v/||v||"
                    )
                )

            # ------------------------------------------------
            # COMBINACION LINEAL
            # ------------------------------------------------

            elif operacion == "Combinación lineal":

                vectores = []
                nombres = []

                for i, entradas in enumerate(
                    self.vector_entries
                ):

                    nombre = f"v{i + 1}"

                    vector = self.obtener_vector(
                        entradas,
                        nombre
                    )

                    vectores.append(
                        vector
                    )

                    nombres.append(
                        nombre
                    )

                b = self.obtener_vector(
                    self.vector_b_entries,
                    "b"
                )

                tipo, solucion, matriz = (
                    ev.determinar_combinacion_lineal(
                        vectores,
                        b
                    )
                )

                salida.append(
                    "--- COMBINACIÓN LINEAL ---"
                )

                salida.append("")

                for i, vector in enumerate(
                    vectores
                ):

                    salida.append(
                        self.vector_a_string(
                            vector,
                            nombres[i]
                        )
                    )

                salida.append("")

                salida.append(
                    self.vector_a_string(
                        b,
                        "b"
                    )
                )

                salida.append("")

                if tipo == "incompatible":

                    salida.append(
                        "RESULTADO:"
                    )

                    salida.append(
                        "b NO es combinación lineal "
                        "de los vectores proporcionados."
                    )

                elif tipo == "unica":

                    salida.append(
                        "RESULTADO:"
                    )

                    salida.append(
                        "b SI es combinación lineal "
                        "de los vectores."
                    )

                    salida.append(
                        "\nEscalares encontrados:"
                    )

                    for i, valor in enumerate(
                        solucion
                    ):

                        salida.append(
                            f"c{i + 1} = "
                            + self.formatear_numero(
                                valor
                            )
                        )

                    salida.append(
                        "\nPor lo tanto:"
                    )

                    terminos = []

                    for i, valor in enumerate(
                        solucion
                    ):

                        terminos.append(
                            "("
                            + self.formatear_numero(
                                valor
                            )
                            + ")"
                            + nombres[i]
                        )

                    salida.append(
                        " + ".join(
                            terminos
                        )
                        + " = b"
                    )

                else:

                    salida.append(
                        "RESULTADO:"
                    )

                    salida.append(
                        "b SI es combinación lineal "
                        "de los vectores."
                    )

                    salida.append(
                        "Existen infinitas combinaciones "
                        "de escalares que producen b."
                    )

            # ------------------------------------------------
            # DESCOMPONER MATRIZ EN VECTORES
            # ------------------------------------------------

            elif operacion == (
                "Descomponer matriz en vectores"
            ):

                matriz = self.obtener_matriz()

                vectores = ev.matriz_a_vectores(
                    matriz
                )

                salida.append(
                    "--- DESCOMPOSICIÓN DE MATRIZ ---"
                )

                salida.append("")

                salida.append(
                    "Matriz A:"
                )

                salida.append(
                    self.matriz_a_string(
                        matriz
                    )
                )

                salida.append(
                    "\nVectores columna:"
                )

                for i, vector in enumerate(
                    vectores
                ):

                    salida.append(
                        self.vector_a_string(
                            vector,
                            f"v{i + 1}"
                        )
                    )

                matriz_reconstruida = (
                    ev.vectores_a_matriz(
                        vectores
                    )
                )

                salida.append(
                    "\nMatriz reconstruida:"
                )

                salida.append(
                    self.matriz_a_string(
                        matriz_reconstruida
                    )
                )

            # ------------------------------------------------
            # MATRIZ A ECUACION VECTORIAL
            # ------------------------------------------------

            elif operacion == (
                "Matriz a ecuación vectorial"
            ):

                matriz = self.obtener_matriz()

                vectores = ev.matriz_a_vectores(
                    matriz
                )

                salida.append(
                    "--- MATRIZ A ECUACIÓN VECTORIAL ---"
                )

                salida.append("")

                salida.append(
                    "Matriz A:"
                )

                salida.append(
                    self.matriz_a_string(
                        matriz
                    )
                )

                salida.append(
                    "\nVectores columna:"
                )

                for i, vector in enumerate(
                    vectores
                ):

                    salida.append(
                        self.vector_a_string(
                            vector,
                            f"v{i + 1}"
                        )
                    )

                salida.append(
                    "\nEcuación vectorial:"
                )

                terminos = []

                for i in range(
                    len(vectores)
                ):

                    terminos.append(
                        f"x{i + 1}v{i + 1}"
                    )

                salida.append(
                    " + ".join(
                        terminos
                    )
                    + " = b"
                )

            # ------------------------------------------------
            # SISTEMA A ECUACION VECTORIAL
            # ------------------------------------------------

            elif operacion == (
                "Sistema a ecuación vectorial"
            ):

                matriz = self.obtener_matriz()

                b = self.obtener_vector(
                    self.vector_b_entries,
                    "b"
                )

                vectores = ev.matriz_a_vectores(
                    matriz
                )

                salida.append(
                    "--- SISTEMA A ECUACIÓN VECTORIAL ---"
                )

                salida.append("")

                salida.append(
                    "Matriz de coeficientes A:"
                )

                salida.append(
                    self.matriz_a_string(
                        matriz
                    )
                )

                salida.append(
                    "\nVector b:"
                )

                salida.append(
                    self.vector_a_string(
                        b,
                        "b"
                    )
                )

                salida.append(
                    "\nVectores columna:"
                )

                for i, vector in enumerate(
                    vectores
                ):

                    salida.append(
                        self.vector_a_string(
                            vector,
                            f"v{i + 1}"
                        )
                    )

                salida.append(
                    "\nEcuación vectorial:"
                )

                terminos = []

                for i in range(
                    len(vectores)
                ):

                    terminos.append(
                        f"x{i + 1}v{i + 1}"
                    )

                salida.append(
                    " + ".join(terminos)
                    + " = b"
                )

                salida.append(
                    "\nForma desarrollada:"
                )

                terminos = []

                for i, vector in enumerate(
                    vectores
                ):

                    terminos.append(
                        f"x{i + 1}"
                        + self.vector_simple_a_string(
                            vector
                        )
                    )

                salida.append(
                    " + ".join(terminos)
                    + " = "
                    + self.vector_simple_a_string(
                        b
                    )
                )

            self._escribir_en_visor(
                "\n".join(
                    salida
                )
            )

        except ValueError as error:

            self._escribir_en_visor(
                f"ERROR DE ENTRADA:\n\n{error}"
            )

    # ========================================================
    # ESCRIBIR RESULTADO
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


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":

    app = AppCalculadoraVectores()

    app.mainloop()