# ============================================================
# CALCULADORA DE MATRICES Y VECTORES - FIA UAM
# ============================================================

from core.ui.ctk_compat import ctk

from core.matriciales import conversionesMatriciales as conv
from core.matriciales import operacionesMatriciales as op
from core.matriciales import solucionMatriciales as sol
from core.matriciales import verificacionMatriciales as ver
from core.matriciales import visualizacionMatriciales as vis
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_menu_desplegable,
    estilo_panel_contenedor,
    FUENTE_CONTROLES,
)


# ============================================================
# CONFIGURACION DE LA INTERFAZ
# ============================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ============================================================
# CLASE PRINCIPAL
# ============================================================

class VistaMatricial(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)

        self.master_dashboard = master
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        
        self.title("Operaciones con Matrices y Ecuaciones Matriciales")
        self.geometry("1100x800")

        # Entradas de la matriz
        self.matriz_entries = []

        # Entradas de los vectores
        self.vector_entries = []
        self.vector_b_entries = []

        # Nombres de los vectores
        self.vector_names = []

        # Entradas generales
        self.entry_filas = None
        self.entry_columnas = None
        self.entry_cantidad_vectores = None
        self.entry_escalar = None

        # Crear interfaz
        self.crear_frame_superior()
        self.crear_frame_central()
        self.crear_frame_inferior()

    def al_cerrar(self):
        if self.master_dashboard is not None:
            self.master_dashboard.deiconify()
        self.destroy()

    # ========================================================
    # FRAME SUPERIOR
    # ========================================================

    def crear_frame_superior(self):
        self.frame_superior = ctk.CTkFrame(self, **estilo_panel_contenedor())
        self.frame_superior.pack(fill="x", padx=15, pady=15)

        titulo = ctk.CTkLabel(
            self.frame_superior,
            text="Calculadora de Álgebra Lineal",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=10)

        frame_datos = ctk.CTkFrame(
            self.frame_superior,
            fg_color="transparent"
        )
        frame_datos.pack(pady=5)

        # ----------------------------------------------------
        # FILAS
        # ----------------------------------------------------
        ctk.CTkLabel(frame_datos, text="Filas de A:", text_color=TEXTO_CLARO).grid(row=0, column=0, padx=5)
        self.entry_filas = ctk.CTkEntry(frame_datos, width=80, placeholder_text="2")
        self.entry_filas.grid(row=0, column=1, padx=5)

        # ----------------------------------------------------
        # COLUMNAS
        # ----------------------------------------------------
        ctk.CTkLabel(frame_datos, text="Columnas de A:", text_color=TEXTO_CLARO).grid(row=0, column=2, padx=5)
        self.entry_columnas = ctk.CTkEntry(frame_datos, width=80, placeholder_text="2")
        self.entry_columnas.grid(row=0, column=3, padx=5)

        # ----------------------------------------------------
        # CANTIDAD DE VECTORES
        # ----------------------------------------------------
        ctk.CTkLabel(frame_datos, text="Cantidad de vectores:", text_color=TEXTO_CLARO).grid(row=0, column=4, padx=5)
        self.entry_cantidad_vectores = ctk.CTkEntry(frame_datos, width=80, placeholder_text="2")
        self.entry_cantidad_vectores.grid(row=0, column=5, padx=5)

        # ----------------------------------------------------
        # BOTON GENERAR
        # ----------------------------------------------------
        boton_generar = ctk.CTkButton(
            frame_datos,
            text="Generar",
            **estilo_boton_secundario(),
            command=self.generar_datos
        )
        boton_generar.grid(row=0, column=6, padx=10)

        # ----------------------------------------------------
        # BOTON LIMPIAR
        # ----------------------------------------------------
        boton_limpiar = ctk.CTkButton(
            frame_datos,
            text="Limpiar",
            **estilo_boton_secundario(),
            command=self.limpiar
        )
        boton_limpiar.grid(row=0, column=7, padx=10)

    # ========================================================
    # FRAME CENTRAL
    # ========================================================

    def crear_frame_central(self):
        self.frame_central = ctk.CTkFrame(
            self,
            **estilo_panel_contenedor()
        )
        self.frame_central.pack(fill="both", expand=True, padx=15, pady=5)

        self.frame_centro = ctk.CTkScrollableFrame(
            self.frame_central,
            label_text="Datos de la operación",
            **estilo_panel_contenedor()
        )
        self.frame_centro.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.frame_previsualizacion = ctk.CTkFrame(
            self.frame_central,
            width=330,
            **estilo_panel_contenedor()
        )
        self.frame_previsualizacion.pack(side="right", fill="both", padx=(8, 0))
        self.frame_previsualizacion.pack_propagate(False)

        ctk.CTkLabel(
            self.frame_previsualizacion,
            text="Vista previa de la ecuación matricial",
            font=(FUENTE_CONTROLES, 14, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(pady=(10, 4))

        self.txt_previsualizacion = ctk.CTkTextbox(
            self.frame_previsualizacion,
            font=("Consolas", 12),
            **estilo_consola_resultado(),
        )
        self.txt_previsualizacion.pack(fill="both", expand=True, padx=8, pady=8)
        self._escribir_previsualizacion("Genere la matriz y complete sus valores.")

    # ========================================================
    # FRAME INFERIOR
    # ========================================================

    def crear_frame_inferior(self):
        self.frame_inferior = ctk.CTkFrame(self, **estilo_panel_contenedor())
        self.frame_inferior.pack(fill="x", padx=15, pady=15)

        # ----------------------------------------------------
        # OPERACION
        # ----------------------------------------------------
        ctk.CTkLabel(self.frame_inferior, text="Operación:", text_color=TEXTO_CLARO).grid(row=0, column=0, padx=5, pady=5)
        
        self.menu_operacion = ctk.CTkComboBox(
            self.frame_inferior,
            values=[
                "A × u",
                "A(u + v)",
                "A(u + v + ...)",
                "u + v",
                "c(u)",
                "A(cu)",
                "A(u + v) = Au + Av",
                "A(cu) = c(Au)",
                "Combinación lineal",
                "Mostrar columnas de A",
                "Sistema a ecuación vectorial",
                "Transpuesta de A",
                "Matriz por escalar (cA)",
                "Resolver Ax = b",
                "Tabla de Intercambio",
                "Flujo de Red"
            ],
            **estilo_menu_desplegable()
        )
        self.menu_operacion.set("A × u")
        self.menu_operacion.grid(row=0, column=1, padx=5, pady=5)

        # ----------------------------------------------------
        # FORMATO
        # ----------------------------------------------------
        ctk.CTkLabel(self.frame_inferior, text="Formato:", text_color=TEXTO_CLARO).grid(row=0, column=2, padx=5, pady=5)
        
        self.menu_formato = ctk.CTkComboBox(
            self.frame_inferior,
            values=["Decimales", "Fracciones"],
            **estilo_menu_desplegable()
        )
        self.menu_formato.set("Decimales")
        self.menu_formato.grid(row=0, column=3, padx=5, pady=5)

        # ----------------------------------------------------
        # ESCALAR
        # ----------------------------------------------------
        self.entry_escalar = ctk.CTkEntry(
            self.frame_inferior,
            width=100,
            placeholder_text="Escalar c"
        )
        self.entry_escalar.grid(row=0, column=4, padx=5, pady=5)

        # ----------------------------------------------------
        # CALCULAR
        # ----------------------------------------------------
        boton_calcular = ctk.CTkButton(
            self.frame_inferior,
            text="Calcular",
            **estilo_boton_principal(),
            command=self.accion_calcular
        )
        boton_calcular.grid(row=0, column=5, padx=10, pady=5)

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------
        self.texto_resultado = ctk.CTkTextbox(
            self.frame_inferior, height=180, **estilo_consola_resultado()
        )
        self.texto_resultado.grid(
            row=1, column=0, columnspan=6,
            sticky="nsew", padx=10, pady=10
        )

    # ========================================================
    # GENERAR MATRIZ Y VECTORES
    # ========================================================

    def generar_datos(self):
        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())
            cantidad_vectores = int(self.entry_cantidad_vectores.get())

            if filas <= 0 or columnas <= 0 or cantidad_vectores <= 0:
                raise ValueError
        except ValueError:
            self.mostrar_resultado("Error: las dimensiones deben ser enteros mayores que 0.")
            return

        for widget in self.frame_centro.winfo_children():
            widget.destroy()

        self.matriz_entries = []
        self.vector_entries = []
        self.vector_b_entries = []
        self.vector_names = []

        # MATRIZ A
        etiqueta_a = ctk.CTkLabel(
            self.frame_centro,
            text="MATRIZ A",
            font=("Arial", 18, "bold")
        )
        etiqueta_a.grid(row=0, column=0, columnspan=columnas, pady=10)

        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                entry = ctk.CTkEntry(self.frame_centro, width=80)
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
                entry.bind("<KeyRelease>", lambda event: self.actualizar_previsualizacion())
                fila_entries.append(entry)
            self.matriz_entries.append(fila_entries)

        # VECTORES
        fila_vectores = filas + 3
        etiqueta_vectores = ctk.CTkLabel(
            self.frame_centro,
            text="VECTORES",
            font=("Arial", 18, "bold")
        )
        etiqueta_vectores.grid(row=fila_vectores, column=0, columnspan=cantidad_vectores, pady=10)

        for j in range(cantidad_vectores):
            nombre = self.generar_nombre_vector(j)
            self.vector_names.append(nombre)

            etiqueta = ctk.CTkLabel(
                self.frame_centro,
                text=nombre,
                font=("Arial", 16, "bold")
            )
            etiqueta.grid(row=fila_vectores + 1, column=j, padx=10, pady=5)

        for j in range(cantidad_vectores):
            entradas = []
            for i in range(columnas):
                entry = ctk.CTkEntry(self.frame_centro, width=80)
                entry.grid(row=fila_vectores + 2 + i, column=j, padx=10, pady=5)
                entry.bind("<KeyRelease>", lambda event: self.actualizar_previsualizacion())
                entradas.append(entry)
            self.vector_entries.append(entradas)

        # VECTOR b PARA LA ECUACION MATRICIAL Ax = b
        fila_b = fila_vectores + cantidad_vectores + 3
        etiqueta_b = ctk.CTkLabel(
            self.frame_centro,
            text="VECTOR b (terminos independientes)",
            font=("Arial", 18, "bold")
        )
        etiqueta_b.grid(row=fila_b, column=0, columnspan=filas, pady=10)

        for i in range(filas):
            entry = ctk.CTkEntry(self.frame_centro, width=80)
            entry.grid(row=fila_b + 1 + i, column=0, padx=5, pady=5)
            entry.bind("<KeyRelease>", lambda event: self.actualizar_previsualizacion())
            self.vector_b_entries.append(entry)

        self.actualizar_previsualizacion()
        self.mostrar_resultado("Matriz y vectores generados correctamente.")

    def actualizar_previsualizacion(self):
        """Muestra la estructura de A X = B mientras se capturan los datos."""
        if not hasattr(self, "txt_previsualizacion"):
            return

        if not self.matriz_entries:
            self._escribir_previsualizacion("Genere la matriz y complete sus valores.")
            return

        filas_a = []
        for fila_entries in self.matriz_entries:
            valores = [entry.get().strip() or "_" for entry in fila_entries]
            filas_a.append("[ " + ", ".join(valores) + " ]")

        valores_x = []
        if self.vector_entries:
            valores_x = [entry.get().strip() or "_" for entry in self.vector_entries[0]]
        else:
            valores_x = ["_"] * len(self.matriz_entries[0])

        valores_b = [entry.get().strip() or "_" for entry in self.vector_b_entries]
        if not valores_b:
            valores_b = ["_"] * len(self.matriz_entries)

        lineas = ["A = " + filas_a[0]]
        lineas.extend("    " + fila for fila in filas_a[1:])
        lineas.append("")
        lineas.append("X = [ " + valores_x[0] + " ]")
        lineas.extend("    [ " + valor + " ]" for valor in valores_x[1:])
        lineas.append("")
        lineas.append("B = [ " + valores_b[0] + " ]")
        lineas.extend("    [ " + valor + " ]" for valor in valores_b[1:])
        self._escribir_previsualizacion("\n".join(lineas))

    def _escribir_previsualizacion(self, texto):
        self.txt_previsualizacion.configure(state="normal")
        self.txt_previsualizacion.delete("1.0", "end")
        self.txt_previsualizacion.insert("1.0", texto)
        self.txt_previsualizacion.configure(state="disabled")

    # ========================================================
    # GENERAR NOMBRE DEL VECTOR
    # ========================================================

    def generar_nombre_vector(self, indice):
        nombres = ["u", "v", "w", "z", "p", "q", "r", "s"]
        if indice < len(nombres):
            return nombres[indice]
        return f"v{indice + 1}"

    # ========================================================
    # OBTENER MATRIZ / VECTORES / ESCALAR
    # ========================================================

    def obtener_matriz(self):
        if not self.matriz_entries:
            raise ValueError("Primero debe generar la matriz.")
        matriz = []
        for fila_entries in self.matriz_entries:
            fila = []
            for entry in fila_entries:
                valor = conv.convertir_a_decimal(entry.get())
                if valor is None:
                    raise ValueError("La matriz contiene valores inválidos.")
                fila.append(valor)
            matriz.append(fila)
        return matriz

    def obtener_vectores(self):
        if not self.vector_entries:
            raise ValueError("Primero debe generar los vectores.")
        vectores = []
        for entradas in self.vector_entries:
            vector = []
            for entry in entradas:
                valor = conv.convertir_a_decimal(entry.get())
                if valor is None:
                    raise ValueError("Uno de los vectores contiene valores inválidos.")
                vector.append(valor)
            vectores.append(vector)
        return vectores

    def obtener_vector_b(self):
        """Obtiene el vector b, cuya dimension coincide con las filas de A."""

        if not self.vector_b_entries:
            raise ValueError("Primero debe generar la matriz y el vector b.")

        vector_b = []
        for entry in self.vector_b_entries:
            valor = conv.convertir_a_decimal(entry.get())
            if valor is None:
                raise ValueError("El vector b contiene valores inválidos.")
            vector_b.append(valor)

        return vector_b

    def obtener_escalar(self):
        valor = conv.convertir_a_decimal(self.entry_escalar.get())
        if valor is None:
            raise ValueError("Debe ingresar un escalar válido.")
        return valor

    # ========================================================
    # MÉTODOS DE CÁLCULO
    # ========================================================

    def calcular_au(self):
        matriz = self.obtener_matriz()
        vectores = self.obtener_vectores()
        if len(vectores) < 1:
            raise ValueError("Se necesita el vector u.")
        u = vectores[0]

        resultado, pasos = op.producto_matriz_vector_detallado(matriz, u)
        formato = self.menu_formato.get()
        salida = ["PRODUCTO MATRIZ POR VECTOR", "", "A =", vis.matriz_a_string(matriz, formato), "", vis.vector_a_string(u, "u", formato), "", "Cálculo de Au:"]
        salida.extend(pasos)
        salida.extend(["", "Resultado:", vis.vector_a_string(resultado, "b", formato)])
        self.mostrar_resultado("\n".join(salida))

    def calcular_a_uv(self):
        matriz = self.obtener_matriz()
        vectores = self.obtener_vectores()
        if len(vectores) < 2:
            raise ValueError("Esta operación necesita los vectores u y v.")
        u, v = vectores[0], vectores[1]
        suma = op.sumar_vectores([u, v])
        resultado = op.producto_matriz_vector(matriz, suma)
        formato = self.menu_formato.get()

        salida = [
            "OPERACIÓN A(u + v)", "",
            "u + v = " + vis.vector_horizontal_a_string(suma, formato), "",
            "A(u + v) =", vis.vector_a_string(resultado, "b", formato)
        ]
        self.mostrar_resultado("\n".join(salida))

    def calcular_a_suma_vectores(self):
        matriz = self.obtener_matriz()
        vectores = self.obtener_vectores()
        if len(vectores) < 2:
            raise ValueError("Se necesitan al menos dos vectores.")
        suma = op.sumar_vectores(vectores)
        resultado = op.producto_matriz_vector(matriz, suma)
        formato = self.menu_formato.get()
        nombres = self.vector_names

        salida = [
            "OPERACIÓN A(u + v + ...)", "",
            " + ".join(nombres) + " = " + vis.vector_horizontal_a_string(suma, formato), "",
            "A(" + " + ".join(nombres) + ") =", vis.vector_a_string(resultado, "b", formato)
        ]
        self.mostrar_resultado("\n".join(salida))

    def calcular_uv(self):
        vectores = self.obtener_vectores()
        if len(vectores) < 2:
            raise ValueError("Se necesitan los vectores u y v.")
        resultado = op.sumar_vectores([vectores[0], vectores[1]])
        formato = self.menu_formato.get()
        salida = ["SUMA DE VECTORES", "", "u + v =", vis.vector_a_string(resultado, "b", formato)]
        self.mostrar_resultado("\n".join(salida))

    def calcular_cu(self):
        vectores = self.obtener_vectores()
        if len(vectores) < 1:
            raise ValueError("Se necesita el vector u.")
        escalar = self.obtener_escalar()
        resultado = op.multiplicar_vector_escalar(vectores[0], escalar)
        formato = self.menu_formato.get()
        salida = ["MULTIPLICACIÓN DE VECTOR POR ESCALAR", "", "c(u) =", vis.vector_a_string(resultado, "b", formato)]
        self.mostrar_resultado("\n".join(salida))

    def calcular_a_cu(self):
        matriz = self.obtener_matriz()
        vectores = self.obtener_vectores()
        if len(vectores) < 1:
            raise ValueError("Se necesita el vector u.")
        escalar = self.obtener_escalar()
        cu = op.multiplicar_vector_escalar(vectores[0], escalar)
        resultado = op.producto_matriz_vector(matriz, cu)
        formato = self.menu_formato.get()

        salida = [
            "OPERACIÓN A(cu)", "",
            "cu = " + vis.vector_horizontal_a_string(cu, formato), "",
            "A(cu) =", vis.vector_a_string(resultado, "b", formato)
        ]
        self.mostrar_resultado("\n".join(salida))

    def calcular_distributiva(self):
        matriz = self.obtener_matriz()
        vectores = self.obtener_vectores()
        if len(vectores) < 2:
            raise ValueError("Se necesitan los vectores u y v.")
        izquierda, derecha = op.propiedad_distributiva(matriz, vectores[0], vectores[1])
        coincide = ver.verificar_propiedad(izquierda, derecha)
        formato = self.menu_formato.get()

        salida = [
            "PROPIEDAD DISTRIBUTIVA", "",
            "A(u + v) = " + vis.vector_horizontal_a_string(izquierda, formato), "",
            "Au + Av = " + vis.vector_horizontal_a_string(derecha, formato), ""
        ]
        if coincide:
            salida.extend(["Se cumple:", "A(u + v) = Au + Av"])
        else:
            salida.append("No se cumple la igualdad.")
        self.mostrar_resultado("\n".join(salida))

    def calcular_propiedad_escalar(self):
        matriz = self.obtener_matriz()
        vectores = self.obtener_vectores()
        if len(vectores) < 1:
            raise ValueError("Se necesita el vector u.")
        escalar = self.obtener_escalar()
        izquierda, derecha = op.propiedad_escalar(matriz, vectores[0], escalar)
        coincide = ver.verificar_propiedad(izquierda, derecha)
        formato = self.menu_formato.get()

        salida = [
            "PROPIEDAD DEL ESCALAR", "",
            "A(cu) = " + vis.vector_horizontal_a_string(izquierda, formato), "",
            "c(Au) = " + vis.vector_horizontal_a_string(derecha, formato), ""
        ]
        if coincide:
            salida.extend(["Se cumple:", "A(cu) = c(Au)"])
        else:
            salida.append("No se cumple la igualdad.")
        self.mostrar_resultado("\n".join(salida))

    def calcular_combinacion_lineal(self):
        vectores = self.obtener_vectores()
        if not vectores:
            raise ValueError("Se necesita al menos un vector.")

        ventana = ctk.CTkToplevel(self)
        ventana.title("Escalares")
        ventana.geometry("350x500")

        ctk.CTkLabel(ventana, text="Ingrese los escalares", font=("Arial", 18, "bold")).pack(pady=15)

        entradas = []
        for nombre in self.vector_names:
            entry = ctk.CTkEntry(ventana, width=100, placeholder_text=f"Escalar de {nombre}")
            entry.pack(pady=5)
            entradas.append(entry)

        def calcular():
            try:
                escalares = []
                for entry in entradas:
                    valor = conv.convertir_a_decimal(entry.get())
                    if valor is None:
                        raise ValueError
                    escalares.append(valor)

                resultado = op.combinacion_lineal(vectores, escalares)
                formato = self.menu_formato.get()

                salida = [
                    "COMBINACIÓN LINEAL", "",
                    vis.ecuacion_vectorial_a_string(self.vector_names, escalares, formato), "",
                    "Resultado:",
                    vis.vector_a_string(resultado, "b", formato)
                ]
                self.mostrar_resultado("\n".join(salida))
                ventana.destroy()
            except ValueError:
                self.mostrar_resultado("Error: ingrese escalares válidos.")

        ctk.CTkButton(ventana, text="Calcular", command=calcular).pack(pady=20)

    def mostrar_columnas(self):
        matriz = self.obtener_matriz()
        formato = self.menu_formato.get()
        salida = ["COLUMNAS DE A", "", vis.columnas_a_string(matriz, formato)]
        self.mostrar_resultado("\n".join(salida))

    def calcular_sistema_ecuacion_vectorial(self):
        matriz = self.obtener_matriz()
        vector_b = self.obtener_vector_b()
        formato = self.menu_formato.get()
        vectores = op.obtener_columnas(matriz)
        nombres = [f"a{i + 1}" for i in range(len(vectores))]

        terminos = [
            f"x{i + 1}{nombre}"
            for i, nombre in enumerate(nombres)
        ]
        terminos_desarrollados = [
            f"x{i + 1}{vis.vector_horizontal_a_string(vector, formato)}"
            for i, vector in enumerate(vectores)
        ]

        salida = [
            "SISTEMA A ECUACIÓN VECTORIAL",
            "",
            "Matriz de coeficientes A:",
            vis.matriz_a_string(matriz, formato),
            "",
            "Vector b:",
            vis.vector_a_string(vector_b, "b", formato),
            "",
            "Vectores columna:"
        ]

        salida.extend(
            vis.vector_a_string(vector, nombre, formato)
            for vector, nombre in zip(vectores, nombres)
        )
        salida.extend([
            "",
            "Ecuación vectorial:",
            " + ".join(terminos) + " = b",
            "",
            "Forma desarrollada:",
            " + ".join(terminos_desarrollados)
            + " = "
            + vis.vector_horizontal_a_string(vector_b, formato)
        ])

        self.mostrar_resultado("\n".join(salida))

    def multiplicar_matriz_escalar(self):
        matriz = self.obtener_matriz()
        escalar = self.obtener_escalar()
        formato = self.menu_formato.get()
        resultado = op.multiplicar_matriz_escalar(matriz, escalar)
        salida = [
            "MULTIPLICACIÓN DE MATRIZ POR ESCALAR",
            "",
            f"c = {vis.formatear_numero(escalar, formato)}",
            "cA =",
            vis.matriz_a_string(resultado, formato)
        ]
        self.mostrar_resultado("\n".join(salida))

    def mostrar_transpuesta(self):
        matriz = self.obtener_matriz()
        formato = self.menu_formato.get()
        salida = [
            "TRANSPUESTA DE LA MATRIZ",
            "",
            "(A^T)ij = Aji",
            "A^T =",
            vis.matriz_transpuesta_a_string(matriz, formato)
        ]
        self.mostrar_resultado("\n".join(salida))

    def resolver_ax_b(self):
        matriz = self.obtener_matriz()
        vector_b = self.obtener_vector_b()
        formato = self.menu_formato.get()
        informacion = sol.resolver_ecuacion_matricial(matriz, vector_b)
        matriz_aumentada = sol.crear_matriz_aumentada(matriz, vector_b)

        salida = [
            "RESOLUCIÓN DE LA ECUACIÓN MATRICIAL Ax = b",
            "",
            "Matriz aumentada [A | b]:",
            vis.matriz_a_string(matriz_aumentada, formato),
            ""
        ]

        for descripcion, matriz_paso in informacion["pasos"][1:]:
            salida.extend([
                f">> {descripcion}:",
                vis.matriz_a_string(matriz_paso, formato),
                ""
            ])

        salida.extend([
            "Forma escalonada reducida (RREF):",
            vis.matriz_a_string(informacion["rref"], formato),
            "",
            f"Rango(A) = {informacion['rango_a']}",
            f"Rango([A | b]) = {informacion['rango_aumentada']}",
            f"Clasificación: {informacion['tipo']}"
        ])

        if informacion["tipo"] == "unica":
            solucion = informacion["solucion"]
            salida.extend([
                "",
                "Solución única:",
                vis.vector_a_string(solucion, "x", formato),
                "",
                "Comprobación: A x = b"
            ])
        elif informacion["tipo"] == "infinitas":
            expresiones, parametros = informacion["parametrizacion"]
            salida.extend([
                "",
                "Solución general:",
                "Variables libres: " + ", ".join(parametros.values()),
                "\n".join(
                    f"x{i + 1} = {expresion}"
                    for i, expresion in enumerate(expresiones)
                )
            ])
        else:
            salida.extend([
                "",
                "El sistema es incompatible: no existe solución."
            ])

        self.mostrar_resultado("\n".join(salida))

    def abrir_tabla_intercambio(self):
        """Abre el modelo de Leontief desde el módulo matricial."""

        self.withdraw()
        from core.ui.vista_intercambio import VistaIntercambio

        VistaIntercambio(self)

    def abrir_flujo_red(self):
        """Abre el análisis de flujo de red desde el módulo matricial."""

        self.withdraw()
        from core.ui.vista_flujo_red import VistaFlujoRed

        VistaFlujoRed(self)

    # ========================================================
    # ACCION PRINCIPAL
    # ========================================================

    def accion_calcular(self):
        try:
            operacion = self.menu_operacion.get()

            if operacion == "Tabla de Intercambio":
                self.abrir_tabla_intercambio()
                return
            if operacion == "Flujo de Red":
                self.abrir_flujo_red()
                return

            if operacion == "A × u":
                self.calcular_au()
            elif operacion == "A(u + v)":
                self.calcular_a_uv()
            elif operacion == "A(u + v + ...)":
                self.calcular_a_suma_vectores()
            elif operacion == "u + v":
                self.calcular_uv()
            elif operacion == "c(u)":
                self.calcular_cu()
            elif operacion == "A(cu)":
                self.calcular_a_cu()
            elif operacion == "A(u + v) = Au + Av":
                self.calcular_distributiva()
            elif operacion == "A(cu) = c(Au)":
                self.calcular_propiedad_escalar()
            elif operacion == "Combinación lineal":
                self.calcular_combinacion_lineal()
            elif operacion == "Mostrar columnas de A":
                self.mostrar_columnas()
            elif operacion == "Sistema a ecuación vectorial":
                self.calcular_sistema_ecuacion_vectorial()
            elif operacion == "Transpuesta de A":
                self.mostrar_transpuesta()
            elif operacion == "Matriz por escalar (cA)":
                self.multiplicar_matriz_escalar()
            elif operacion == "Resolver Ax = b":
                self.resolver_ax_b()

        except ValueError as error:
            self.mostrar_resultado("Error: " + str(error))
        except Exception as error:
            self.mostrar_resultado("Ocurrió un error:\n" + str(error))

    # ========================================================
    # MOSTRAR RESULTADO / LIMPIAR
    # ========================================================

    def mostrar_resultado(self, texto):
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)

    def limpiar(self):
        self.entry_filas.delete(0, "end")
        self.entry_columnas.delete(0, "end")
        self.entry_cantidad_vectores.delete(0, "end")
        self.entry_escalar.delete(0, "end")

        for widget in self.frame_centro.winfo_children():
            widget.destroy()

        self.matriz_entries = []
        self.vector_entries = []
        self.vector_b_entries = []
        self.vector_names = []
        self._escribir_previsualizacion("Genere la matriz y complete sus valores.")
        self.mostrar_resultado("")


# ============================================================
# EJECUCION INDEPENDIENTE (PRUEBA)
# ============================================================

if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()  # Oculta la ventana principal temporalmente si se prueba directo
    ventana_matriciales = VistaMatricial(app)
    app.mainloop()