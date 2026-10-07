# ============================================================
# CALCULADORA DE DETERMINANTES
# FIA UAM
# ============================================================

import customtkinter as ctk

import Matriciales.conversionesMatriciales as conv

import Determinantes.operacionesDeterminantes as op
import Determinantes.cramerDeterminantes as cr
import Determinantes.visualizacionDeterminantes as vis


# ============================================================
# CONFIGURACION DE APARIENCIA
# ============================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ============================================================
# APLICACION PRINCIPAL
# ============================================================

class AppCalculadoraDeterminantes(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "Calculadora de Determinantes - FIA UAM"
        )

        self.geometry(
            "980x780"
        )

        self.minsize(
            900,
            700
        )

        self.matriz_a_entries = []

        self.vector_b_entries = []

        self.controles = {}

        self.crear_interfaz()

        self.cambiar_operacion()


    # ========================================================
    # CREAR INTERFAZ
    # ========================================================

    def crear_interfaz(self):

        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Calculadora de Determinantes",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.lbl_titulo.pack(
            pady=(20, 10)
        )

        self.frame_sup = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.frame_sup.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.frame_controles = ctk.CTkFrame(
            self.frame_sup,
            fg_color="transparent"
        )

        self.frame_controles.pack(
            fill="x"
        )

        self.frame_centro = ctk.CTkScrollableFrame(
            self,
            label_text="Datos de entrada"
        )

        self.frame_centro.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.frame_inf = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.frame_inf.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

        self.crear_controles_inferiores()


    # ========================================================
    # CONTROLES INFERIORES
    # ========================================================

    def crear_controles_inferiores(self):

        self.opcion_operacion = ctk.CTkOptionMenu(
            self.frame_inf,
            values=[
                "Determinante",
                "Regla de Cramer"
            ],
            command=self.cambiar_operacion,
            width=170
        )

        self.opcion_operacion.grid(
            row=0,
            column=0,
            padx=5
        )

        self.opcion_numform = ctk.CTkOptionMenu(
            self.frame_inf,
            values=[
                "Fracciones",
                "Decimales"
            ],
            width=130
        )

        self.opcion_numform.grid(
            row=0,
            column=1,
            padx=5
        )

        self.btn_calcular = ctk.CTkButton(
            self.frame_inf,
            text="Calcular",
            command=self.calcular,
            fg_color="green",
            hover_color="darkgreen",
            width=120
        )

        self.btn_calcular.grid(
            row=0,
            column=2,
            padx=5
        )

        self.btn_limpiar = ctk.CTkButton(
            self.frame_inf,
            text="Limpiar",
            command=self.limpiar,
            width=120
        )

        self.btn_limpiar.grid(
            row=0,
            column=3,
            padx=5
        )

        self.resultado = ctk.CTkTextbox(
            self.frame_inf,
            height=150,
            font=(
                "Courier New",
                12
            )
        )

        self.resultado.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=5,
            pady=(10, 0)
        )

        self.frame_inf.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame_inf.grid_columnconfigure(
            1,
            weight=1
        )

        self.frame_inf.grid_columnconfigure(
            2,
            weight=1
        )

        self.frame_inf.grid_columnconfigure(
            3,
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
        operacion=None
    ):

        if operacion is None:

            operacion = (
                self.opcion_operacion.get()
            )

        for widget in self.frame_controles.winfo_children():

            widget.destroy()

        self.controles.clear()

        if operacion == "Determinante":

            self.crear_control_dimension(
                "Filas A:",
                0,
                "3"
            )

            self.crear_control_dimension(
                "Columnas A:",
                2,
                "3"
            )

            self.crear_control_metodo(
                4
            )

            self.crear_boton_generar()

        elif operacion == "Regla de Cramer":

            self.crear_control_dimension(
                "Filas A:",
                0,
                "3"
            )

            self.crear_control_dimension(
                "Columnas A:",
                2,
                "3"
            )

            self.crear_boton_generar()

        self.matriz_a_entries.clear()

        self.vector_b_entries.clear()

        for widget in self.frame_centro.winfo_children():

            widget.destroy()

        self._escribir_en_visor(
            "Ingrese las dimensiones y presione 'Generar'."
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

        etiqueta = ctk.CTkLabel(
            self.frame_controles,
            text=nombre
        )

        etiqueta.grid(
            row=0,
            column=columna,
            padx=(5, 2),
            pady=5
        )

        entrada = ctk.CTkEntry(
            self.frame_controles,
            width=70
        )

        entrada.insert(
            0,
            valor_inicial
        )

        entrada.grid(
            row=0,
            column=columna + 1,
            padx=(2, 10),
            pady=5
        )

        self.controles[nombre] = entrada


    # ========================================================
    # CREAR CONTROL DE METODO
    # ========================================================

    def crear_control_metodo(
        self,
        columna
    ):

        etiqueta = ctk.CTkLabel(
            self.frame_controles,
            text="Método:"
        )

        etiqueta.grid(
            row=0,
            column=columna,
            padx=(5, 2),
            pady=5
        )

        self.opcion_metodo = ctk.CTkOptionMenu(
            self.frame_controles,
            values=[
                "Automático",
                "ad - bc",
                "Sarrus",
                "Cofactores"
            ],
            width=150
        )

        self.opcion_metodo.grid(
            row=0,
            column=columna + 1,
            padx=(2, 10),
            pady=5
        )

        self.opcion_metodo.set(
            "Automático"
        )


    # ========================================================
    # CREAR BOTON GENERAR
    # ========================================================

    def crear_boton_generar(self):

        boton = ctk.CTkButton(
            self.frame_controles,
            text="Generar",
            command=self.generar_datos,
            width=100
        )

        boton.grid(
            row=0,
            column=8,
            padx=5,
            pady=5
        )


    # ========================================================
    # OBTENER ENTERO
    # ========================================================

    def obtener_entero(
        self,
        nombre
    ):

        entrada = self.controles.get(
            nombre
        )

        if entrada is None:

            raise ValueError(
                "No se encontro el control "
                + nombre
            )

        try:

            valor = int(
                entrada.get().strip()
            )

        except ValueError:

            raise ValueError(
                nombre
                + " debe ser un numero entero."
            )

        if valor <= 0:

            raise ValueError(
                nombre
                + " debe ser mayor que cero."
            )

        return valor


    # ========================================================
    # GENERAR DATOS
    # ========================================================

    def generar_datos(self):

        try:

            for widget in self.frame_centro.winfo_children():

                widget.destroy()

            self.matriz_a_entries.clear()

            self.vector_b_entries.clear()

            filas_a = self.obtener_entero(
                "Filas A:"
            )

            columnas_a = self.obtener_entero(
                "Columnas A:"
            )

            operacion = (
                self.opcion_operacion.get()
            )

            if filas_a != columnas_a:

                raise ValueError(
                    "La matriz debe ser cuadrada "
                    "para trabajar con determinantes."
                )

            if operacion == "Determinante":

                self.crear_matriz_a(
                    filas_a,
                    columnas_a
                )

            elif operacion == "Regla de Cramer":

                self.crear_matriz_a(
                    filas_a,
                    columnas_a
                )

                self.crear_vector_b(
                    filas_a
                )

            self._escribir_en_visor(
                "Ingrese los valores y presione 'Calcular'."
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

        frame = ctk.CTkFrame(
            self.frame_centro
        )

        frame.pack(
            pady=10
        )

        self.matriz_a_entries = []

        for i in range(filas):

            fila_entries = []

            for j in range(columnas):

                entrada = ctk.CTkEntry(
                    frame,
                    width=70
                )

                entrada.insert(
                    0,
                    "0"
                )

                entrada.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                fila_entries.append(
                    entrada
                )

            self.matriz_a_entries.append(
                fila_entries
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
            pady=10
        )

        self.vector_b_entries = []

        for i in range(dimension):

            etiqueta = ctk.CTkLabel(
                frame,
                text="b" + str(i + 1)
            )

            etiqueta.grid(
                row=0,
                column=i,
                padx=4,
                pady=(4, 2)
            )

            entrada = ctk.CTkEntry(
                frame,
                width=70
            )

            entrada.insert(
                0,
                "0"
            )

            entrada.grid(
                row=1,
                column=i,
                padx=4,
                pady=4
            )

            self.vector_b_entries.append(
                entrada
            )


    # ========================================================
    # OBTENER MATRIZ A
    # ========================================================

    def obtener_matriz_a(self):

        matriz = []

        for fila_entries in self.matriz_a_entries:

            fila = []

            for entrada in fila_entries:

                valor = conv.convertir_a_decimal(
                    entrada.get()
                )

                if valor is None:

                    raise ValueError(
                        "Todos los valores de la matriz "
                        "deben ser numeros."
                    )

                fila.append(
                    valor
                )

            matriz.append(
                fila
            )

        return matriz


    # ========================================================
    # OBTENER VECTOR B
    # ========================================================

    def obtener_vector_b(self):

        vector = []

        for entrada in self.vector_b_entries:

            valor = conv.convertir_a_decimal(
                entrada.get()
            )

            if valor is None:

                raise ValueError(
                    "Todos los valores del vector "
                    "deben ser numeros."
                )

            vector.append(
                valor
            )

        return vector


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

            matriz = self.obtener_matriz_a()

            if operacion == "Determinante":

                self.calcular_determinante(
                    matriz,
                    formato
                )

            elif operacion == "Regla de Cramer":

                self.calcular_cramer(
                    matriz,
                    formato
                )

            else:

                self.mostrar_error(
                    "Seleccione una operación."
                )

        except ValueError as error:

            self.mostrar_error(
                str(error)
            )

        except Exception as error:

            self.mostrar_error(
                "Ocurrio un error inesperado:\n"
                + str(error)
            )


    # ========================================================
    # CALCULAR DETERMINANTE
    # ========================================================

    def calcular_determinante(
        self,
        matriz,
        formato
    ):

        orden = len(matriz)

        metodo = (
            self.opcion_metodo.get()
        )

        print("\n")
        print("=" * 60)
        print("CALCULADORA DE DETERMINANTES")
        print("=" * 60)

        print("\nMatriz ingresada:")

        for fila in matriz:

            print(fila)

        print("\nOrden:", orden)
        print("Método seleccionado:", metodo)

        # ----------------------------------------------------
        # AUTOMATICO
        # ----------------------------------------------------

        if metodo == "Automático":

            if orden == 1:

                metodo_real = "1x1"

            elif orden == 2:

                metodo_real = "ad - bc"

            elif orden == 3:

                metodo_real = "Sarrus"

            else:

                metodo_real = "Cofactores"

        else:

            metodo_real = metodo

        print(
            "Método utilizado:",
            metodo_real
        )

        # ----------------------------------------------------
        # VALIDACION DE METODO
        # ----------------------------------------------------

        if metodo_real == "ad - bc" and orden != 2:

            raise ValueError(
                "El método ad - bc solamente "
                "se puede utilizar con matrices 2x2."
            )

        if metodo_real == "Sarrus" and orden != 3:

            raise ValueError(
                "La Regla de Sarrus solamente "
                "se puede utilizar con matrices 3x3."
            )

        if metodo_real == "Cofactores" and orden < 3:

            raise ValueError(
                "El método de Cofactores se utilizará "
                "para matrices de 3x3 o mayores."
            )

        # ----------------------------------------------------
        # 1x1
        # ----------------------------------------------------

        if metodo_real == "1x1":

            resultado = (
                op.determinante_1x1(
                    matriz
                )
            )

            texto = (
                vis.determinante_1x1_a_string(
                    matriz,
                    resultado,
                    formato
                )
            )

            print("\nResultado:")
            print(resultado)

        # ----------------------------------------------------
        # 2x2
        # ----------------------------------------------------

        elif metodo_real == "ad - bc":

            datos = (
                op.determinante_2x2_detallado(
                    matriz
                )
            )

            texto = (
                vis.determinante_2x2_a_string(
                    matriz,
                    datos,
                    formato
                )
            )

            print("\nProcedimiento ad - bc:")

            print(
                "det(A) = ad - bc"
            )

            print(
                "det(A) =",
                datos[4],
                "-",
                datos[5]
            )

            print(
                "det(A) =",
                datos[6]
            )

        # ----------------------------------------------------
        # SARRUS
        # ----------------------------------------------------

        elif metodo_real == "Sarrus":

            datos = (
                op.determinante_sarrus(
                    matriz
                )
            )

            texto = (
                vis.determinante_sarrus_a_string(
                    matriz,
                    datos,
                    formato
                )
            )

            print("\nProcedimiento de Sarrus:")

            print(
                "Diagonales positivas:",
                datos[0],
                "+",
                datos[1],
                "+",
                datos[2]
            )

            print(
                "Diagonales negativas:",
                datos[3],
                "+",
                datos[4],
                "+",
                datos[5]
            )

            print(
                "Suma positiva:",
                datos[6]
            )

            print(
                "Suma negativa:",
                datos[7]
            )

            print(
                "Determinante:",
                datos[8]
            )

        # ----------------------------------------------------
        # COFACTORES
        # ----------------------------------------------------

        elif metodo_real == "Cofactores":

            resultado = (
                op.determinante_cofactores(
                    matriz
                )
            )

            texto = (
                vis.cofactores_a_string(
                    matriz,
                    formato
                )
            )

            print("\nProcedimiento por cofactores:")

            self.mostrar_cofactores_terminal(
                matriz
            )

            print(
                "\nDeterminante:",
                resultado
            )

        else:

            raise ValueError(
                "No se pudo determinar el método."
            )

        print("=" * 60)
        print("FIN DEL PROCEDIMIENTO")
        print("=" * 60)

        self._escribir_en_visor(
            texto
        )


    # ========================================================
    # MOSTRAR COFACTORES EN TERMINAL
    # ========================================================

    def mostrar_cofactores_terminal(
        self,
        matriz
    ):

        orden = len(matriz)

        print(
            "Expansión por la primera fila:"
        )

        for columna in range(orden):

            elemento = matriz[0][columna]

            signo = (
                (-1) ** columna
            )

            menor = (
                op.obtener_menor(
                    matriz,
                    0,
                    columna
                )
            )

            cofactor = (
                op.calcular_cofactor(
                    matriz,
                    0,
                    columna
                )
            )

            print(
                "\nElemento:",
                elemento
            )

            print(
                "Signo:",
                signo
            )

            print(
                "Menor:"
            )

            for fila in menor:

                print(
                    fila
                )

            print(
                "Cofactor:",
                cofactor
            )

            print(
                "Aporte:",
                elemento * cofactor
            )


    # ========================================================
    # CALCULAR CRAMER
    # ========================================================

    def calcular_cramer(
        self,
        matriz,
        formato
    ):

        vector_b = (
            self.obtener_vector_b()
        )

        print("\n")
        print("=" * 60)
        print("REGLA DE CRAMER")
        print("=" * 60)

        print("\nMatriz A:")

        for fila in matriz:

            print(fila)

        print("\nVector b:")

        print(vector_b)

        (
            determinante_principal,
            determinantes,
            solucion
        ) = cr.resolver_cramer(
            matriz,
            vector_b
        )

        print(
            "\nDeterminante principal:",
            determinante_principal
        )

        for i in range(
            len(determinantes)
        ):

            letra = chr(
                ord("x") + i
            )

            print(
                "D" + letra + ":",
                determinantes[i]
            )

            print(
                letra
                + " = "
                + "D"
                + letra
                + " / D =",
                solucion[i]
            )

        print("=" * 60)
        print("FIN DEL PROCEDIMIENTO")
        print("=" * 60)

        texto = (
            vis.procedimiento_cramer_a_string(
                matriz,
                vector_b,
                formato
            )
        )

        self._escribir_en_visor(
            texto
        )


    # ========================================================
    # MOSTRAR ERROR
    # ========================================================

    def mostrar_error(
        self,
        mensaje
    ):

        print("\n")
        print("=" * 60)
        print("ERROR")
        print("=" * 60)
        print(mensaje)
        print("=" * 60)

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

        self.resultado.configure(
            state="normal"
        )

        self.resultado.delete(
            "1.0",
            "end"
        )

        self.resultado.insert(
            "1.0",
            texto
        )

        self.resultado.configure(
            state="disabled"
        )


    # ========================================================
    # LIMPIAR
    # ========================================================

    def limpiar(self):

        self.matriz_a_entries.clear()

        self.vector_b_entries.clear()

        for widget in self.frame_centro.winfo_children():

            widget.destroy()

        self._escribir_en_visor(
            "Seleccione una operación."
        )


# ============================================================
# EJECUTAR APLICACION
# ============================================================

if __name__ == "__main__":

    app = AppCalculadoraDeterminantes()

    app.mainloop()