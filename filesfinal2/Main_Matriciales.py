# ============================================================
# CALCULADORA DE MATRICES Y VECTORES
# ============================================================

import customtkinter as ctk
import Matriciales.operacionesMatriciales as op
import Matriciales.visualizacionMatriciales as vis


# ============================================================
# CONFIGURACION GENERAL
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# APLICACION PRINCIPAL
# ============================================================

class AppCalculadoraMatriciales(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Calculadora de Operaciones Matriciales")
        self.geometry("1100x800")
        self.minsize(950, 700)

        self.matriz_a_entries = []
        self.matriz_b_entries = []
        self.vector_entries = []

        self.controles_superiores = {}

        self.crear_interfaz()
        self.cambiar_operacion()

    # ========================================================
    # INTERFAZ PRINCIPAL
    # ========================================================

    def crear_interfaz(self):

        # ----------------------------------------------------
        # TITULO
        # ----------------------------------------------------

        self.titulo = ctk.CTkLabel(
            self,
            text="Calculadora de Operaciones Matriciales",
            font=ctk.CTkFont(size=24, weight="bold")
        )

        self.titulo.pack(pady=(15, 10))

        # ----------------------------------------------------
        # FRAME SUPERIOR
        # ----------------------------------------------------

        self.frame_configuracion = ctk.CTkFrame(self)
        self.frame_configuracion.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # ----------------------------------------------------
        # FRAME DINAMICO DE CONFIGURACION
        # ----------------------------------------------------

        self.frame_controles = ctk.CTkFrame(
            self.frame_configuracion,
            fg_color="transparent"
        )

        self.frame_controles.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # ----------------------------------------------------
        # FRAME CENTRAL
        # ----------------------------------------------------

        self.frame_entrada = ctk.CTkScrollableFrame(
            self,
            label_text="Datos de entrada"
        )

        self.frame_entrada.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # ----------------------------------------------------
        # FRAME INFERIOR
        # ----------------------------------------------------

        self.frame_operaciones = ctk.CTkFrame(self)
        self.frame_operaciones.pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        # ----------------------------------------------------
        # TIPO DE OPERACION
        # ----------------------------------------------------

        self.label_operacion = ctk.CTkLabel(
            self.frame_operaciones,
            text="Tipo de operación:"
        )

        self.label_operacion.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        operaciones = [
            "A + B",
            "A - B",
            "cA",
            "A × B",
            "A × u",
            "A(u + v)",
            "A(u + v + ...)",
            "u + v",
            "c(u)",
            "A(cu)",
            "A(u + v) = Au + Av",
            "A(cu) = c(Au)",
            "Combinación lineal",
            "Mostrar columnas de A"
        ]

        self.menu_operacion = ctk.CTkOptionMenu(
            self.frame_operaciones,
            values=operaciones,
            command=self.cambiar_operacion
        )

        self.menu_operacion.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # ----------------------------------------------------
        # ESCALAR
        # ----------------------------------------------------

        self.label_escalar = ctk.CTkLabel(
            self.frame_operaciones,
            text="Escalar:"
        )

        self.entry_escalar = ctk.CTkEntry(
            self.frame_operaciones,
            width=100
        )

        # ----------------------------------------------------
        # FORMATO
        # ----------------------------------------------------

        self.label_formato = ctk.CTkLabel(
            self.frame_operaciones,
            text="Formato:"
        )

        self.menu_formato = ctk.CTkOptionMenu(
            self.frame_operaciones,
            values=["Decimales", "Fracciones"]
        )

        # ----------------------------------------------------
        # BOTON CALCULAR
        # ----------------------------------------------------

        self.boton_calcular = ctk.CTkButton(
            self.frame_operaciones,
            text="Calcular",
            command=self.calcular
        )

        self.boton_calcular.grid(
            row=0,
            column=5,
            padx=10,
            pady=10
        )

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        self.label_resultado = ctk.CTkLabel(
            self.frame_operaciones,
            text="Resultado:"
        )

        self.label_resultado.grid(
            row=1,
            column=0,
            padx=10,
            pady=(5, 10),
            sticky="nw"
        )

        self.texto_resultado = ctk.CTkTextbox(
            self.frame_operaciones,
            height=130
        )

        self.texto_resultado.grid(
            row=1,
            column=1,
            columnspan=5,
            padx=10,
            pady=(5, 10),
            sticky="ew"
        )

        self.frame_operaciones.grid_columnconfigure(
            1,
            weight=1
        )

    # ========================================================
    # LIMPIAR CONTROLES SUPERIORES
    # ========================================================

    def limpiar_controles_superiores(self):

        for widget in self.frame_controles.winfo_children():
            widget.destroy()

        self.controles_superiores = {}

    # ========================================================
    # CREAR CONTROL DE DIMENSION
    # ========================================================

    def crear_control_dimension(
        self,
        nombre,
        fila,
        columna,
        valor_inicial
    ):

        label = ctk.CTkLabel(
            self.frame_controles,
            text=nombre
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
            str(valor_inicial)
        )

        entry.grid(
            row=fila,
            column=columna + 1,
            padx=(3, 10),
            pady=5
        )

        self.controles_superiores[nombre] = entry

        return entry

    # ========================================================
    # CREAR CONTROL DE CANTIDAD DE VECTORES
    # ========================================================

    def crear_control_vectores(
        self,
        fila=0,
        valor_inicial=2
    ):

        label = ctk.CTkLabel(
            self.frame_controles,
            text="Cantidad de vectores:"
        )

        label.grid(
            row=fila,
            column=0,
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
            row=fila,
            column=1,
            padx=(3, 10),
            pady=5
        )

        self.controles_superiores["cantidad_vectores"] = entry

        return entry

    # ========================================================
    # CREAR CONTROL DE DIMENSION DE VECTOR
    # ========================================================

    def crear_control_dimension_vector(
        self,
        fila=0,
        valor_inicial=2
    ):

        label = ctk.CTkLabel(
            self.frame_controles,
            text="Dimensión del vector:"
        )

        label.grid(
            row=fila,
            column=2,
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
            row=fila,
            column=3,
            padx=(3, 10),
            pady=5
        )

        self.controles_superiores["dimension_vector"] = entry

        return entry

    # ========================================================
    # BOTON GENERAR
    # ========================================================

    def crear_boton_generar(self):

        boton = ctk.CTkButton(
            self.frame_controles,
            text="Generar",
            command=lambda: self.generar_datos(True)
        )

        boton.grid(
            row=0,
            column=10,
            padx=10,
            pady=5
        )

        self.controles_superiores["boton_generar"] = boton

    # ========================================================
    # CAMBIAR OPERACION
    # ========================================================

    def cambiar_operacion(self, valor=None):

        operacion = self.menu_operacion.get()

        self.limpiar_controles_superiores()

        # Ocultar escalar
        self.label_escalar.grid_forget()
        self.entry_escalar.grid_forget()

        # ----------------------------------------------------
        # A + B
        # ----------------------------------------------------

        if operacion in ["A + B", "A - B", "A × B"]:

            self.crear_control_dimension(
                "Filas de A:",
                0,
                0,
                3
            )

            self.crear_control_dimension(
                "Columnas de A:",
                0,
                2,
                3
            )

            self.crear_control_dimension(
                "Filas de B:",
                0,
                4,
                3
            )

            self.crear_control_dimension(
                "Columnas de B:",
                0,
                6,
                3
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # cA
        # ----------------------------------------------------

        elif operacion == "cA":

            self.crear_control_dimension(
                "Filas de A:",
                0,
                0,
                3
            )

            self.crear_control_dimension(
                "Columnas de A:",
                0,
                2,
                3
            )

            self.crear_boton_generar()

            self.mostrar_escalar()

        # ----------------------------------------------------
        # OPERACIONES CON A Y VECTORES
        # ----------------------------------------------------

        elif operacion in [
            "A × u",
            "A(u + v)",
            "A(u + v + ...)",
            "A(cu)",
            "A(u + v) = Au + Av",
            "A(cu) = c(Au)",
            "Mostrar columnas de A"
        ]:

            self.crear_control_dimension(
                "Filas de A:",
                0,
                0,
                3
            )

            self.crear_control_dimension(
                "Columnas de A:",
                0,
                2,
                3
            )

            # Cantidad de vectores solamente cuando aplica
            if operacion == "A × u":

                self.crear_control_vectores(
                    fila=0,
                    valor_inicial=1
                )

            elif operacion == "A(u + v)":

                self.crear_control_vectores(
                    fila=0,
                    valor_inicial=2
                )

            elif operacion == "A(u + v + ...)":

                self.crear_control_vectores(
                    fila=0,
                    valor_inicial=3
                )

            elif operacion == "A(cu)":

                self.crear_control_vectores(
                    fila=0,
                    valor_inicial=1
                )

            elif operacion == "A(u + v) = Au + Av":

                self.crear_control_vectores(
                    fila=0,
                    valor_inicial=2
                )

            elif operacion == "A(cu) = c(Au)":

                self.crear_control_vectores(
                    fila=0,
                    valor_inicial=1
                )

            self.crear_boton_generar()

            if operacion in [
                "A(cu)",
                "A(cu) = c(Au)"
            ]:
                self.mostrar_escalar()

        # ----------------------------------------------------
        # u + v
        # ----------------------------------------------------

        elif operacion == "u + v":

            self.crear_control_vectores(
                fila=0,
                valor_inicial=2
            )

            self.crear_control_dimension_vector(
                fila=0,
                valor_inicial=3
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # c(u)
        # ----------------------------------------------------

        elif operacion == "c(u)":

            self.crear_control_dimension_vector(
                fila=0,
                valor_inicial=3
            )

            self.crear_boton_generar()

            self.mostrar_escalar()

        # ----------------------------------------------------
        # COMBINACION LINEAL
        # ----------------------------------------------------

        elif operacion == "Combinación lineal":

            self.crear_control_vectores(
                fila=0,
                valor_inicial=2
            )

            self.crear_control_dimension_vector(
                fila=0,
                valor_inicial=3
            )

            self.crear_boton_generar()

        # ----------------------------------------------------
        # ACTUALIZAR AREA CENTRAL
        # ----------------------------------------------------

        self.generar_datos(
            limpiar_resultado=False
        )

    # ========================================================
    # MOSTRAR ESCALAR
    # ========================================================

    def mostrar_escalar(self):

        self.label_escalar.grid(
            row=0,
            column=3,
            padx=(20, 3),
            pady=10
        )

        self.entry_escalar.grid(
            row=0,
            column=4,
            padx=(3, 10),
            pady=10
        )

    # ========================================================
    # OBTENER ENTERO DE CONTROL
    # ========================================================

    def obtener_entero_control(
        self,
        nombre,
        minimo=1
    ):

        entry = self.controles_superiores.get(nombre)

        if entry is None:
            return None

        try:
            valor = int(entry.get())

            if valor < minimo:
                raise ValueError

            return valor

        except ValueError:

            raise ValueError(
                f"El campo '{nombre}' debe contener "
                f"un entero mayor o igual que {minimo}."
            )

    # ========================================================
    # GENERAR DATOS
    # ========================================================

    def generar_datos(
        self,
        limpiar_resultado=True
    ):

        operacion = self.menu_operacion.get()

        try:

            self.matriz_a_entries = []
            self.matriz_b_entries = []
            self.vector_entries = []

            for widget in self.frame_entrada.winfo_children():
                widget.destroy()

            # ------------------------------------------------
            # DATOS DE A
            # ------------------------------------------------

            necesita_a = operacion in [
                "A + B",
                "A - B",
                "cA",
                "A × B",
                "A × u",
                "A(u + v)",
                "A(u + v + ...)",
                "A(cu)",
                "A(u + v) = Au + Av",
                "A(cu) = c(Au)",
                "Mostrar columnas de A"
            ]

            if necesita_a:

                filas_a = self.obtener_entero_control(
                    "Filas de A:"
                )

                columnas_a = self.obtener_entero_control(
                    "Columnas de A:"
                )

                self.crear_matriz_a(
                    filas_a,
                    columnas_a
                )

            # ------------------------------------------------
            # DATOS DE B
            # ------------------------------------------------

            if operacion in [
                "A + B",
                "A - B",
                "A × B"
            ]:

                filas_b = self.obtener_entero_control(
                    "Filas de B:"
                )

                columnas_b = self.obtener_entero_control(
                    "Columnas de B:"
                )

                self.crear_matriz_b(
                    filas_b,
                    columnas_b
                )

            # ------------------------------------------------
            # VECTORES
            # ------------------------------------------------

            if operacion in [
                "A × u",
                "A(u + v)",
                "A(u + v + ...)",
                "A(cu)",
                "A(u + v) = Au + Av",
                "A(cu) = c(Au)"
            ]:

                columnas_a = self.obtener_entero_control(
                    "Columnas de A:"
                )

                cantidad = self.obtener_entero_control(
                    "cantidad_vectores"
                )

                self.crear_vectores(
                    cantidad,
                    columnas_a
                )

            elif operacion in [
                "u + v",
                "c(u)",
                "Combinación lineal"
            ]:

                cantidad = self.obtener_entero_control(
                    "cantidad_vectores"
                )

                dimension = self.obtener_entero_control(
                    "dimension_vector"
                )

                self.crear_vectores(
                    cantidad,
                    dimension
                )

            if limpiar_resultado:

                self.texto_resultado.delete(
                    "1.0",
                    "end"
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
            self.frame_entrada,
            text="Matriz A",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(10, 5)
        )

        frame = ctk.CTkFrame(
            self.frame_entrada
        )

        frame.pack(
            pady=5
        )

        for i in range(filas):

            fila_entries = []

            for j in range(columnas):

                entry = ctk.CTkEntry(
                    frame,
                    width=70
                )

                entry.grid(
                    row=i,
                    column=j,
                    padx=3,
                    pady=3
                )

                entry.insert(
                    0,
                    "0"
                )

                fila_entries.append(entry)

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
            self.frame_entrada,
            text="Matriz B",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        titulo.pack(
            pady=(15, 5)
        )

        frame = ctk.CTkFrame(
            self.frame_entrada
        )

        frame.pack(
            pady=5
        )

        for i in range(filas):

            fila_entries = []

            for j in range(columnas):

                entry = ctk.CTkEntry(
                    frame,
                    width=70
                )

                entry.grid(
                    row=i,
                    column=j,
                    padx=3,
                    pady=3
                )

                entry.insert(
                    0,
                    "0"
                )

                fila_entries.append(entry)

            self.matriz_b_entries.append(
                fila_entries
            )

    # ========================================================
    # CREAR VECTORES
    # ========================================================

    def crear_vectores(
        self,
        cantidad,
        dimension
    ):

        nombres_base = [
            "u",
            "v",
            "w",
            "z",
            "p",
            "q",
            "r",
            "s"
        ]

        for numero in range(cantidad):

            if numero < len(nombres_base):

                nombre = nombres_base[numero]

            else:

                nombre = f"v{numero + 1}"

            titulo = ctk.CTkLabel(
                self.frame_entrada,
                text=f"Vector {nombre}",
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                )
            )

            titulo.pack(
                pady=(15, 5)
            )

            frame = ctk.CTkFrame(
                self.frame_entrada
            )

            frame.pack(
                pady=5
            )

            entradas_vector = []

            for i in range(dimension):

                entry = ctk.CTkEntry(
                    frame,
                    width=70
                )

                entry.grid(
                    row=i,
                    column=0,
                    padx=3,
                    pady=3
                )

                entry.insert(
                    0,
                    "0"
                )

                entradas_vector.append(
                    entry
                )

            self.vector_entries.append(
                entradas_vector
            )

    # ========================================================
    # OBTENER MATRIZ A
    # ========================================================

    def obtener_matriz_a(self):

        matriz = []

        for fila_entries in self.matriz_a_entries:

            fila = []

            for entry in fila_entries:

                valor = op.convertir_a_decimal(
                    entry.get()
                )

                if valor is None:

                    raise ValueError(
                        "Todos los valores de A deben ser numéricos."
                    )

                fila.append(valor)

            matriz.append(fila)

        return matriz

    # ========================================================
    # OBTENER MATRIZ B
    # ========================================================

    def obtener_matriz_b(self):

        matriz = []

        for fila_entries in self.matriz_b_entries:

            fila = []

            for entry in fila_entries:

                valor = op.convertir_a_decimal(
                    entry.get()
                )

                if valor is None:

                    raise ValueError(
                        "Todos los valores de B deben ser numéricos."
                    )

                fila.append(valor)

            matriz.append(fila)

        return matriz

    # ========================================================
    # OBTENER VECTORES
    # ========================================================

    def obtener_vectores(self):

        vectores = []

        for entradas in self.vector_entries:

            vector = []

            for entry in entradas:

                valor = op.convertir_a_decimal(
                    entry.get()
                )

                if valor is None:

                    raise ValueError(
                        "Todos los valores de los vectores "
                        "deben ser numéricos."
                    )

                vector.append(valor)

            vectores.append(vector)

        return vectores

    # ========================================================
    # OBTENER ESCALAR
    # ========================================================

    def obtener_escalar(self):

        valor = op.convertir_a_decimal(
            self.entry_escalar.get()
        )

        if valor is None:

            raise ValueError(
                "El escalar debe ser un número válido."
            )

        return valor

    # ========================================================
    # CALCULAR
    # ========================================================

    def calcular(self):

        try:

            operacion = self.menu_operacion.get()
            formato = self.menu_formato.get()

            matriz_a = None
            matriz_b = None
            vectores = []

            if self.matriz_a_entries:

                matriz_a = self.obtener_matriz_a()

            if self.matriz_b_entries:

                matriz_b = self.obtener_matriz_b()

            if self.vector_entries:

                vectores = self.obtener_vectores()

            resultado = ""

            # ------------------------------------------------
            # A + B
            # ------------------------------------------------

            if operacion == "A + B":

                resultado_matriz = op.sumar_matrices(
                    matriz_a,
                    matriz_b
                )

                resultado = (
                    "A + B =\n\n"
                    + vis.matriz_a_string(
                        resultado_matriz,
                        formato
                    )
                )

            # ------------------------------------------------
            # A - B
            # ------------------------------------------------

            elif operacion == "A - B":

                resultado_matriz = op.restar_matrices(
                    matriz_a,
                    matriz_b
                )

                resultado = (
                    "A - B =\n\n"
                    + vis.matriz_a_string(
                        resultado_matriz,
                        formato
                    )
                )

            # ------------------------------------------------
            # cA
            # ------------------------------------------------

            elif operacion == "cA":

                escalar = self.obtener_escalar()

                resultado_matriz = (
                    op.multiplicar_matriz_escalar(
                        matriz_a,
                        escalar
                    )
                )

                resultado = (
                    f"cA, con c = {escalar}\n\n"
                    + vis.matriz_a_string(
                        resultado_matriz,
                        formato
                    )
                )

            # ------------------------------------------------
            # A × B
            # ------------------------------------------------

            elif operacion == "A × B":

                resultado_matriz = (
                    op.multiplicar_matrices(
                        matriz_a,
                        matriz_b
                    )
                )

                resultado = (
                    "A × B =\n\n"
                    + vis.matriz_a_string(
                        resultado_matriz,
                        formato
                    )
                )

            # ------------------------------------------------
            # A × u
            # ------------------------------------------------

            elif operacion == "A × u":

                resultado_vector = (
                    op.producto_matriz_vector(
                        matriz_a,
                        vectores[0]
                    )
                )

                resultado = (
                    "A × u = b\n\n"
                    + vis.vector_a_string(
                        vectores[0],
                        "u",
                        formato
                    )
                    + "\n\n"
                    + vis.resultado_a_string(
                        resultado_vector,
                        "b",
                        formato
                    )
                )

            # ------------------------------------------------
            # A(u + v)
            # ------------------------------------------------

            elif operacion == "A(u + v)":

                vector_suma, resultado_vector = (
                    op.matriz_sobre_suma_vectores(
                        matriz_a,
                        vectores
                    )
                )

                resultado = (
                    "u + v =\n"
                    + vis.vector_horizontal_a_string(
                        vector_suma,
                        formato
                    )
                    + "\n\nA(u + v) = b\n"
                    + vis.vector_horizontal_a_string(
                        resultado_vector,
                        formato
                    )
                )

            # ------------------------------------------------
            # A(u + v + ...)
            # ------------------------------------------------

            elif operacion == "A(u + v + ...)":

                vector_suma, resultado_vector = (
                    op.matriz_sobre_suma_vectores(
                        matriz_a,
                        vectores
                    )
                )

                nombres = []

                for i in range(len(vectores)):

                    if i == 0:
                        nombres.append("u")
                    elif i == 1:
                        nombres.append("v")
                    else:
                        nombres.append(f"v{i + 1}")

                resultado = (
                    f"{vis.nombres_suma_vectores(nombres)} =\n"
                    + vis.vector_horizontal_a_string(
                        vector_suma,
                        formato
                    )
                    + "\n\n"
                    + f"A({vis.nombres_suma_vectores(nombres)}) = b\n"
                    + vis.vector_horizontal_a_string(
                        resultado_vector,
                        formato
                    )
                )

            # ------------------------------------------------
            # u + v
            # ------------------------------------------------

            elif operacion == "u + v":

                resultado_vector = op.sumar_vectores(
                    vectores
                )

                resultado = (
                    "u + v =\n\n"
                    + vis.vector_horizontal_a_string(
                        resultado_vector,
                        formato
                    )
                )

            # ------------------------------------------------
            # c(u)
            # ------------------------------------------------

            elif operacion == "c(u)":

                escalar = self.obtener_escalar()

                resultado_vector = (
                    op.multiplicar_vector_escalar(
                        vectores[0],
                        escalar
                    )
                )

                resultado = (
                    f"c(u), con c = {escalar}\n\n"
                    + vis.vector_horizontal_a_string(
                        resultado_vector,
                        formato
                    )
                )

            # ------------------------------------------------
            # A(cu)
            # ------------------------------------------------

            elif operacion == "A(cu)":

                escalar = self.obtener_escalar()

                vector_escalado = (
                    op.multiplicar_vector_escalar(
                        vectores[0],
                        escalar
                    )
                )

                resultado_vector = (
                    op.producto_matriz_vector(
                        matriz_a,
                        vector_escalado
                    )
                )

                resultado = (
                    "A(cu) = b\n\n"
                    + vis.vector_horizontal_a_string(
                        resultado_vector,
                        formato
                    )
                )

            # ------------------------------------------------
            # PROPIEDAD DISTRIBUTIVA
            # ------------------------------------------------

            elif operacion == "A(u + v) = Au + Av":

                izquierda, derecha = (
                    op.propiedad_distributiva(
                        matriz_a,
                        vectores[0],
                        vectores[1]
                    )
                )

                resultado = (
                    "A(u + v):\n"
                    + vis.vector_horizontal_a_string(
                        izquierda,
                        formato
                    )
                    + "\n\nAu + Av:\n"
                    + vis.vector_horizontal_a_string(
                        derecha,
                        formato
                    )
                )

            # ------------------------------------------------
            # PROPIEDAD ESCALAR
            # ------------------------------------------------

            elif operacion == "A(cu) = c(Au)":

                escalar = self.obtener_escalar()

                izquierda, derecha = (
                    op.propiedad_escalar(
                        matriz_a,
                        vectores[0],
                        escalar
                    )
                )

                resultado = (
                    "A(cu):\n"
                    + vis.vector_horizontal_a_string(
                        izquierda,
                        formato
                    )
                    + "\n\nc(Au):\n"
                    + vis.vector_horizontal_a_string(
                        derecha,
                        formato
                    )
                )

            # ------------------------------------------------
            # COMBINACION LINEAL
            # ------------------------------------------------

            elif operacion == "Combinación lineal":

                self.abrir_combinacion_lineal(
                    vectores,
                    formato
                )

                return

            # ------------------------------------------------
            # COLUMNAS DE A
            # ------------------------------------------------

            elif operacion == "Mostrar columnas de A":

                resultado = vis.columnas_a_string(
                    matriz_a,
                    formato
                )

            self.texto_resultado.delete(
                "1.0",
                "end"
            )

            self.texto_resultado.insert(
                "1.0",
                resultado
            )

        except ValueError as error:

            self.mostrar_error(
                str(error)
            )

    # ========================================================
    # COMBINACION LINEAL
    # ========================================================

    def abrir_combinacion_lineal(
        self,
        vectores,
        formato
    ):

        ventana = ctk.CTkToplevel(self)

        ventana.title(
            "Combinación lineal"
        )

        ventana.geometry(
            "450x500"
        )

        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Ingrese un escalar para cada vector",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            pady=15
        )

        entradas = []

        nombres = [
            "u",
            "v",
            "w",
            "z",
            "p",
            "q",
            "r",
            "s"
        ]

        for i in range(len(vectores)):

            if i < len(nombres):

                nombre = nombres[i]

            else:

                nombre = f"v{i + 1}"

            frame = ctk.CTkFrame(
                ventana
            )

            frame.pack(
                fill="x",
                padx=30,
                pady=5
            )

            ctk.CTkLabel(
                frame,
                text=f"Escalar de {nombre}:"
            ).pack(
                side="left",
                padx=10
            )

            entry = ctk.CTkEntry(
                frame,
                width=100
            )

            entry.pack(
                side="right",
                padx=10
            )

            entry.insert(
                0,
                "1"
            )

            entradas.append(entry)

        def calcular_combinacion():

            try:

                escalares = []

                for entry in entradas:

                    valor = op.convertir_a_decimal(
                        entry.get()
                    )

                    if valor is None:

                        raise ValueError(
                            "Todos los escalares deben "
                            "ser números válidos."
                        )

                    escalares.append(valor)

                resultado_vector = (
                    op.combinacion_lineal(
                        vectores,
                        escalares
                    )
                )

                resultado = (
                    "Combinación lineal:\n\n"
                    + vis.vector_horizontal_a_string(
                        resultado_vector,
                        formato
                    )
                )

                self.texto_resultado.delete(
                    "1.0",
                    "end"
                )

                self.texto_resultado.insert(
                    "1.0",
                    resultado
                )

                ventana.destroy()

            except ValueError as error:

                self.mostrar_error(
                    str(error)
                )

        ctk.CTkButton(
            ventana,
            text="Calcular",
            command=calcular_combinacion
        ).pack(
            pady=20
        )

    # ========================================================
    # MOSTRAR ERROR
    # ========================================================

    def mostrar_error(
        self,
        mensaje
    ):

        self.texto_resultado.delete(
            "1.0",
            "end"
        )

        self.texto_resultado.insert(
            "1.0",
            "ERROR:\n\n" + mensaje
        )

    # ========================================================
    # LIMPIAR
    # ========================================================

    def limpiar(self):

        for widget in self.frame_entrada.winfo_children():
            widget.destroy()

        self.matriz_a_entries = []
        self.matriz_b_entries = []
        self.vector_entries = []

        self.texto_resultado.delete(
            "1.0",
            "end"
        )

        self.cambiar_operacion()


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    app = AppCalculadoraMatriciales()
    app.mainloop()