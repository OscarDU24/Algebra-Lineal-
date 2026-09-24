import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.ui.ctk_compat import ctk
from core.vectores import conversionesVectores as conv
from core.vectores import eliminacionVectores as ev
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_menu_desplegable,
    estilo_panel_contenedor,
    TEXTO_CLARO,
)



class VistaVector(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.master_dashboard = master
        self.title("Operaciones con Vectores")
        self.geometry("980x780")
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        self.vector_u_entries = []
        self.vector_v_entries = []
        self.vector_entries = []
        self.vector_b_entries = []
        self.matriz_entries = []

        self.crear_frame_superior()
        self.crear_frame_central()
        self.crear_frame_inferior()

        self.generar_vectores()

    def al_cerrar(self):
        self.master_dashboard.deiconify()
        self.destroy()

    # ============================================================
    # FRAME SUPERIOR
    # ============================================================

    def crear_frame_superior(self):

        self.frame_sup = ctk.CTkFrame(self, **estilo_panel_contenedor())
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

        self.lbl_dimension_secundaria = ctk.CTkLabel(
            self.frame_sup,
            text="Cantidad/columnas:"
        )
        self.lbl_dimension_secundaria.pack(side="left", padx=(15, 5))

        self.entry_dimension_secundaria = ctk.CTkEntry(
            self.frame_sup,
            width=60
        )
        self.entry_dimension_secundaria.insert(0, "2")
        self.entry_dimension_secundaria.pack(side="left", padx=5)

        btn_generar = ctk.CTkButton(
            self.frame_sup,
            text="Generar Vectores",
            **estilo_boton_secundario(),
            command=self.generar_vectores
        )

        btn_generar.pack(
            side="left",
            padx=15
        )

        btn_limpiar = ctk.CTkButton(
            self.frame_sup,
            text="Limpiar Valores",
            **estilo_boton_secundario(),
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
        self.frame_central = ctk.CTkFrame(self, **estilo_panel_contenedor())
        self.frame_central.pack(pady=10, padx=20, fill="both", expand=True)

        self.frame_centro = ctk.CTkScrollableFrame(
            self.frame_central,
            label_text="Vectores",
            **estilo_panel_contenedor()
        )
        self.frame_centro.pack(side="left", pady=8, padx=(8, 4), fill="both", expand=True)

        self.frame_previsualizacion = ctk.CTkFrame(
            self.frame_central,
            width=260,
            **estilo_panel_contenedor()
        )
        self.frame_previsualizacion.pack(side="right", pady=8, padx=(4, 8), fill="both")
        self.frame_previsualizacion.pack_propagate(False)
        ctk.CTkLabel(
            self.frame_previsualizacion,
            text="Vista previa de vectores",
            text_color=TEXTO_CLARO,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 4))
        self.txt_previsualizacion = ctk.CTkTextbox(
            self.frame_previsualizacion,
            font=("Consolas", 12),
            **estilo_consola_resultado()
        )
        self.txt_previsualizacion.pack(fill="both", expand=True, padx=8, pady=8)
        self._escribir_previsualizacion("Genere los vectores y complete sus componentes.")

    # ============================================================
    # FRAME INFERIOR
    # ============================================================

    def crear_frame_inferior(self):

        self.frame_inf = ctk.CTkFrame(self, **estilo_panel_contenedor())

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

        self.opcion_operacion = ctk.CTkComboBox(
            subframe_acciones,
            values=[
                "Suma",
                "Resta",
                "Multiplicación por escalar",
                "Producto punto",
                "Magnitud de u",
                "Magnitud de v",
                "Normalizar u",
                "Normalizar v",
                "Producto cruz",
                "Ángulo entre u y v",
                "Proyección de u sobre v",
                "Distancia entre u y v",
                "Combinación lineal",
                "Vectores a matriz",
                "Descomponer matriz en vectores",
                "Matriz a ecuación vectorial",
                "Sistema a ecuación vectorial"
            ],
            command=self.cambiar_operacion,
            **estilo_menu_desplegable()
        )
        self.opcion_operacion.set("Suma")

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

        self.opcion_numform = ctk.CTkComboBox(
            subframe_acciones,
            values=[
                "Fracciones",
                "Decimales"
            ],
            **estilo_menu_desplegable()
        )
        self.opcion_numform.set("Decimales")

        self.opcion_numform.pack(
            side="left",
            padx=(0, 10)
        )

        btn_calcular = ctk.CTkButton(
            subframe_acciones,
            text="Calcular",
            **estilo_boton_principal(),
            command=self.accion_calcular

        )

        btn_calcular.pack(
            side="left"
        )

        self.txt_resultados = ctk.CTkTextbox(
            self.frame_inf, font=("Courier New", 12), **estilo_consola_resultado()
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
        self.vector_entries = []
        self.vector_b_entries = []
        self.matriz_entries = []

        operacion = self.opcion_operacion.get()

        if operacion in {
            "Combinación lineal",
            "Vectores a matriz",
            "Descomponer matriz en vectores",
            "Matriz a ecuación vectorial",
            "Sistema a ecuación vectorial"
        }:
            try:
                primera_dimension = int(self.entry_dimension.get())
                segunda_dimension = int(self.entry_dimension_secundaria.get())
                if primera_dimension <= 0 or segunda_dimension <= 0:
                    raise ValueError

                if operacion in {"Combinación lineal", "Vectores a matriz"}:
                    self.crear_vectores_combinacion(
                        segunda_dimension,
                        primera_dimension
                    )
                    self.crear_vector_b(primera_dimension)
                elif operacion in {
                    "Descomponer matriz en vectores",
                    "Matriz a ecuación vectorial"
                }:
                    self.crear_matriz(primera_dimension, segunda_dimension)
                else:
                    self.crear_sistema(primera_dimension, segunda_dimension)
                return
            except ValueError:
                self._escribir_en_visor(
                    "ERROR: Ingrese dimensiones enteras positivas válidas."
                )
                return

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

            entry_u.bind("<KeyRelease>", lambda event: self.actualizar_previsualizacion())
            entry_v.bind("<KeyRelease>", lambda event: self.actualizar_previsualizacion())

            self.vector_u_entries.append(
                entry_u
            )

            self.vector_v_entries.append(
                entry_v
            )

        self.actualizar_previsualizacion()

    def cambiar_operacion(self, operacion=None):
        operacion = operacion or self.opcion_operacion.get()
        etiquetas = {
            "Combinación lineal": "Cantidad de vectores:",
            "Vectores a matriz": "Cantidad de vectores:",
            "Descomponer matriz en vectores": "Columnas:",
            "Matriz a ecuación vectorial": "Columnas:",
            "Sistema a ecuación vectorial": "Variables:"
        }
        self.lbl_dimension_secundaria.configure(
            text=etiquetas.get(operacion, "Cantidad/columnas:")
        )

    def crear_vectores_combinacion(self, cantidad, dimension):
        titulo = ctk.CTkLabel(
            self.frame_centro,
            text="Vectores generadores",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo.grid(row=0, column=0, columnspan=cantidad, pady=10)

        for columna in range(cantidad):
            ctk.CTkLabel(
                self.frame_centro,
                text=f"v{columna + 1}",
                font=ctk.CTkFont(weight="bold")
            ).grid(row=1, column=columna, padx=8, pady=5)
            entradas = []
            for fila in range(dimension):
                entry = ctk.CTkEntry(self.frame_centro, width=85, justify="center")
                entry.grid(row=fila + 2, column=columna, padx=5, pady=4)
                entradas.append(entry)
            self.vector_entries.append(entradas)

    def crear_vector_b(self, dimension):
        fila_inicial = dimension + 3
        ctk.CTkLabel(
            self.frame_centro,
            text="Vector objetivo b",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=fila_inicial, column=0, columnspan=2, pady=10)

        for indice in range(dimension):
            ctk.CTkLabel(
                self.frame_centro,
                text=f"b{indice + 1}"
            ).grid(row=fila_inicial + indice + 1, column=0, padx=8, pady=4)
            entry = ctk.CTkEntry(self.frame_centro, width=85, justify="center")
            entry.grid(row=fila_inicial + indice + 1, column=1, padx=8, pady=4)
            self.vector_b_entries.append(entry)

    def crear_matriz(self, filas, columnas):
        ctk.CTkLabel(
            self.frame_centro,
            text="Matriz A",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=columnas, pady=10)

        for fila in range(filas):
            entradas = []
            for columna in range(columnas):
                entry = ctk.CTkEntry(self.frame_centro, width=85, justify="center")
                entry.grid(row=fila + 1, column=columna, padx=5, pady=4)
                entradas.append(entry)
            self.matriz_entries.append(entradas)

    def crear_sistema(self, ecuaciones, variables):
        self.crear_matriz(ecuaciones, variables)
        fila_inicial = ecuaciones + 3
        ctk.CTkLabel(
            self.frame_centro,
            text="Vector b",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=fila_inicial, column=0, columnspan=2, pady=10)

        for indice in range(ecuaciones):
            ctk.CTkLabel(
                self.frame_centro,
                text=f"b{indice + 1}"
            ).grid(row=fila_inicial + indice + 1, column=0, padx=8, pady=4)
            entry = ctk.CTkEntry(self.frame_centro, width=85, justify="center")
            entry.grid(row=fila_inicial + indice + 1, column=1, padx=8, pady=4)
            self.vector_b_entries.append(entry)

    def obtener_vector_entradas(self, entradas, nombre):
        vector = []
        for indice, entry in enumerate(entradas):
            valor = entry.get().strip()
            if not valor:
                raise ValueError(f"La componente {nombre}{indice + 1} está vacía.")
            numero = conv.convertir_a_decimal(valor)
            if numero is None:
                raise ValueError(f"El valor '{valor}' en {nombre}{indice + 1} no es válido.")
            vector.append(numero)
        return vector

    def obtener_matriz_especial(self):
        matriz = []
        for fila_indice, entradas in enumerate(self.matriz_entries):
            fila = []
            for columna_indice, entry in enumerate(entradas):
                valor = entry.get().strip()
                if not valor:
                    raise ValueError(
                        f"A[{fila_indice + 1}][{columna_indice + 1}] está vacía."
                    )
                numero = conv.convertir_a_decimal(valor)
                if numero is None:
                    raise ValueError(
                        f"El valor '{valor}' en A[{fila_indice + 1}][{columna_indice + 1}] no es válido."
                    )
                fila.append(numero)
            matriz.append(fila)
        return matriz

    def matriz_a_string(self, matriz):
        return "\n".join(
            "[ " + ", ".join(self.formatear_numero(valor) for valor in fila) + " ]"
            for fila in matriz
        )

    def actualizar_previsualizacion(self):
        """Muestra los componentes actuales de u y v antes de calcular."""
        if not hasattr(self, "txt_previsualizacion"):
            return

        valores_u = [entry.get().strip() or "_" for entry in self.vector_u_entries]
        valores_v = [entry.get().strip() or "_" for entry in self.vector_v_entries]
        texto = "u = [" + ", ".join(valores_u) + "]\n"
        texto += "v = [" + ", ".join(valores_v) + "]"
        self._escribir_previsualizacion(texto)

    def _escribir_previsualizacion(self, texto):
        self.txt_previsualizacion.configure(state="normal")
        self.txt_previsualizacion.delete("1.0", "end")
        self.txt_previsualizacion.insert("1.0", texto)
        self.txt_previsualizacion.configure(state="disabled")

    # ============================================================
    # LIMPIAR ENTRADAS
    # ============================================================

    def limpiar_entradas(self):

        for entradas in self.vector_entries:
            for entry in entradas:
                entry.delete(0, "end")

        for entry in self.vector_b_entries:
            entry.delete(0, "end")

        for fila in self.matriz_entries:
            for entry in fila:
                entry.delete(0, "end")

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

        self.actualizar_previsualizacion()

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

        numero

        return numero

    # ============================================================
    # FORMATEAR VECTOR
    # ============================================================

    def formatear_numero(self, numero):
        """Formatea resultados sin mostrar fracciones desproporcionadas."""

        if abs(numero) < 1e-9:
            numero = 0.0

        if self.opcion_numform.get() == "Fracciones":
            fraccion = conv.convertir_a_fraccion(numero)
            denominador = fraccion.split("/", 1)[1] if "/" in fraccion else "1"

            if abs(int(denominador)) <= 100:
                return fraccion

        return f"{numero:.2f}"

    def vector_a_string(
        self,
        vector,
        nombre="Vector"
    ):

        valores = []

        for componente in vector:
            valores.append(self.formatear_numero(componente))

        resultado = [
            f"{nombre} = ["
            + ", ".join(valores)
            + "]"
        ]

        return "\n".join(resultado)

    def calcular_combinacion_lineal(self):
        vectores = [
            self.obtener_vector_entradas(entradas, f"v{indice + 1}")
            for indice, entradas in enumerate(self.vector_entries)
        ]
        vector_b = self.obtener_vector_entradas(self.vector_b_entries, "b")
        tipo, solucion, _ = ev.determinar_combinacion_lineal(vectores, vector_b)

        salida = [
            "--- COMBINACIÓN LINEAL ---",
            "",
            "Vectores generadores:"
        ]
        for indice, vector in enumerate(vectores):
            salida.append(self.vector_a_string(vector, f"v{indice + 1}"))
        salida.extend([
            "",
            self.vector_a_string(vector_b, "b"),
            "",
            f"Clasificación: {tipo}"
        ])
        if tipo == "unica":
            terminos = [
                f"({self.formatear_numero(valor)})v{indice + 1}"
                for indice, valor in enumerate(solucion)
            ]
            salida.extend([
                "Coeficientes:",
                self.vector_a_string(solucion, "c"),
                "",
                " + ".join(terminos) + " = b"
            ])
        elif tipo == "incompatible":
            salida.append("b no pertenece al espacio generado por los vectores.")
        else:
            salida.append("Existen infinitas combinaciones que producen b.")
        self._escribir_en_visor("\n".join(salida))

    def calcular_matriz_a_vectores(self):
        matriz = self.obtener_matriz_especial()
        vectores = ev.matriz_a_vectores(matriz)
        salida = ["--- MATRIZ DESCOMPUESTA EN VECTORES ---", "", "A =", self.matriz_a_string(matriz), ""]
        salida.extend(
            self.vector_a_string(vector, f"v{indice + 1}")
            for indice, vector in enumerate(vectores)
        )
        self._escribir_en_visor("\n".join(salida))

    def calcular_vectores_a_matriz(self):
        vectores = [
            self.obtener_vector_entradas(entradas, f"v{indice + 1}")
            for indice, entradas in enumerate(self.vector_entries)
        ]
        matriz = ev.vectores_a_matriz(vectores)
        salida = [
            "--- VECTORES A MATRIZ ---",
            "",
            "Vectores de entrada:"
        ]
        salida.extend(
            self.vector_a_string(vector, f"v{indice + 1}")
            for indice, vector in enumerate(vectores)
        )
        salida.extend([
            "",
            "Matriz formada con las columnas:",
            self.matriz_a_string(matriz)
        ])
        self._escribir_en_visor("\n".join(salida))

    def calcular_matriz_a_ecuacion(self):
        matriz = self.obtener_matriz_especial()
        vectores, nombres, ecuacion = ev.matriz_a_ecuacion_vectorial(matriz)
        salida = ["--- MATRIZ A ECUACIÓN VECTORIAL ---", "", "A =", self.matriz_a_string(matriz), ""]
        salida.extend(
            self.vector_a_string(vector, nombre)
            for vector, nombre in zip(vectores, nombres)
        )
        salida.extend(["", "Ecuación vectorial:", ecuacion])
        self._escribir_en_visor("\n".join(salida))

    def calcular_sistema_a_ecuacion(self):
        matriz = self.obtener_matriz_especial()
        vector_b = self.obtener_vector_entradas(self.vector_b_entries, "b")
        matriz_aumentada = [
            fila + [vector_b[indice]]
            for indice, fila in enumerate(matriz)
        ]
        _, vectores, vector_b, nombres, ecuacion = ev.sistema_a_ecuacion_vectorial(
            matriz_aumentada
        )
        salida = [
            "--- SISTEMA A ECUACIÓN VECTORIAL ---",
            "",
            "A =",
            self.matriz_a_string(matriz),
            "",
            self.vector_a_string(vector_b, "b"),
            ""
        ]
        salida.extend(
            self.vector_a_string(vector, nombre)
            for vector, nombre in zip(vectores, nombres)
        )
        salida.extend(["", "Ecuación vectorial:", ecuacion])
        self._escribir_en_visor("\n".join(salida))

    # ============================================================
    # CALCULAR OPERACION
    # ============================================================

    def accion_calcular(self):

        try:

            operacion = self.opcion_operacion.get()

            operaciones_especiales = {
                "Combinación lineal": self.calcular_combinacion_lineal,
                "Vectores a matriz": self.calcular_vectores_a_matriz,
                "Descomponer matriz en vectores": self.calcular_matriz_a_vectores,
                "Matriz a ecuación vectorial": self.calcular_matriz_a_ecuacion,
                "Sistema a ecuación vectorial": self.calcular_sistema_a_ecuacion
            }
            if operacion in operaciones_especiales:
                operaciones_especiales[operacion]()
                return

            vector_u = self.obtener_vector_u()
            vector_v = self.obtener_vector_v()

            salida = []

            salida.append(
                "========================================================="
            )

            salida.append(
                "                     CALCULADORA DE VECTORES"
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
                    "Cada componente: ui + vi"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Resultado"
                    )
                )

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
                    "Cada componente: ui - vi"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Resultado"
                    )
                )

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
                    f"Escalar = {self.formatear_numero(escalar)}"
                )

                salida.append(
                    "Cada componente: escalar * ui"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Resultado"
                    )
                )

            elif operacion == "Producto punto":

                resultado = ev.producto_punto(
                    vector_u,
                    vector_v
                )

                salida.append(
                    "--- PRODUCTO PUNTO ---"
                )

                salida.append(
                    "u · v = "
                    + " + ".join(
                        f"({self.formatear_numero(componente_u)} * "
                        f"{self.formatear_numero(componente_v)})"
                        for componente_u, componente_v in zip(vector_u, vector_v)
                    )
                    + f" = {self.formatear_numero(resultado)}"
                )

            elif operacion == "Magnitud de u":

                resultado = ev.magnitud_vector(
                    vector_u
                )

                salida.append(
                    "--- MAGNITUD DE U ---"
                )

                salida.append(
                    "||u|| = sqrt(u1^2 + u2^2 + ... + un^2) "
                    f"= {self.formatear_numero(resultado)}"
                )

            elif operacion == "Magnitud de v":

                resultado = ev.magnitud_vector(
                    vector_v
                )

                salida.append(
                    "--- MAGNITUD DE V ---"
                )

                salida.append(
                    "||v|| = sqrt(v1^2 + v2^2 + ... + vn^2) "
                    f"= {self.formatear_numero(resultado)}"
                )

            elif operacion == "Normalizar u":

                resultado = ev.normalizar_vector(
                    vector_u
                )

                salida.append(
                    "--- NORMALIZACIÓN DE U ---"
                )

                salida.append(
                    "u_unitario = u / ||u||"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Vector unitario"
                    )
                )

            elif operacion == "Normalizar v":

                resultado = ev.normalizar_vector(
                    vector_v
                )

                salida.append(
                    "--- NORMALIZACIÓN DE V ---"
                )

                salida.append(
                    "v_unitario = v / ||v||"
                )

                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Vector unitario"
                    )
                )

            elif operacion == "Producto cruz":
                resultado = ev.producto_cruz(vector_u, vector_v)
                salida.append("--- PRODUCTO CRUZ ---")
                salida.append("u × v")
                salida.append(
                    "[u2v3 - u3v2, u3v1 - u1v3, u1v2 - u2v1]"
                )
                salida.append(
                    self.vector_a_string(
                        resultado,
                        "Resultado"
                    )
                )

            elif operacion == "Ángulo entre u y v":
                resultado = ev.angulo_entre_vectores(vector_u, vector_v)
                salida.append("--- ÁNGULO ENTRE VECTORES ---")
                salida.append("cos(θ) = (u · v) / (||u|| · ||v||)")
                salida.append(f"θ = {self.formatear_numero(resultado)}°")

            elif operacion == "Proyección de u sobre v":
                resultado = ev.proyeccion_vector(vector_u, vector_v)
                salida.append("--- PROYECCIÓN DE U SOBRE V ---")
                salida.append("proj_v(u) = ((u · v) / ||v||^2) · v")
                salida.append(
                    self.vector_a_string(
                        resultado,
                        "proj_v(u)"
                    )
                )

            elif operacion == "Distancia entre u y v":
                resultado = ev.distancia_vectores(vector_u, vector_v)
                salida.append("--- DISTANCIA ENTRE U Y V ---")
                salida.append("d(u, v) = ||u - v||")
                salida.append(f"d(u, v) = {self.formatear_numero(resultado)}")

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
            "1.0",  
            "end"
        )

        self.txt_resultados.insert(
            "1.0",  
            texto
        )

        self.txt_resultados.configure(
            state="disabled"
        )