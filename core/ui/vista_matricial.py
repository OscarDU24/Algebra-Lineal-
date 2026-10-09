# ============================================================
# CALCULADORA DE MATRICES Y VECTORES - FIA UAM
# ============================================================

from core.ui.ctk_compat import ctk
from core.ui.audio_manager import reproducir_sonido_error

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

        self.frame_datos = ctk.CTkFrame(
            self.frame_superior,
            fg_color="transparent"
        )
        self.frame_datos.pack(pady=5, fill="x")

        self.frame_dimensiones = ctk.CTkFrame(
            self.frame_datos,
            fg_color="transparent"
        )
        self.frame_dimensiones.pack(side="left", expand=True)

        self.frame_dimensiones_matriz = ctk.CTkFrame(
            self.frame_dimensiones,
            fg_color="transparent"
        )
        self.frame_dimensiones_vector = ctk.CTkFrame(
            self.frame_dimensiones,
            fg_color="transparent"
        )
        self.frame_dimensiones_cantidad = ctk.CTkFrame(
            self.frame_dimensiones,
            fg_color="transparent"
        )

        self.lbl_filas = ctk.CTkLabel(self.frame_dimensiones_matriz, text="Filas de A:", text_color=TEXTO_CLARO)
        self.lbl_filas.pack(side="left", padx=(5, 2))
        self.entry_filas = ctk.CTkEntry(self.frame_dimensiones_matriz, width=60, placeholder_text="2")
        self.entry_filas.pack(side="left", padx=(2, 10))

        self.lbl_columnas = ctk.CTkLabel(self.frame_dimensiones_matriz, text="Columnas de A:", text_color=TEXTO_CLARO)
        self.lbl_columnas.pack(side="left", padx=(5, 2))
        self.entry_columnas = ctk.CTkEntry(self.frame_dimensiones_matriz, width=60, placeholder_text="2")
        self.entry_columnas.pack(side="left", padx=(2, 10))

        self.lbl_dimension_vector = ctk.CTkLabel(self.frame_dimensiones_vector, text="Dimensión:", text_color=TEXTO_CLARO)
        self.lbl_dimension_vector.pack(side="left", padx=(5, 2))
        self.entry_dimension_vector = ctk.CTkEntry(self.frame_dimensiones_vector, width=60, placeholder_text="2")
        self.entry_dimension_vector.pack(side="left", padx=(2, 10))

        self.lbl_cantidad_vectores = ctk.CTkLabel(self.frame_dimensiones_cantidad, text="Cantidad de vectores:", text_color=TEXTO_CLARO)
        self.lbl_cantidad_vectores.pack(side="left", padx=(5, 2))
        self.entry_cantidad_vectores = ctk.CTkEntry(self.frame_dimensiones_cantidad, width=60, placeholder_text="2")
        self.entry_cantidad_vectores.insert(0, "2")
        self.entry_cantidad_vectores.pack(side="left", padx=(2, 10))

        self.frame_botones_generacion = ctk.CTkFrame(
            self.frame_datos,
            fg_color="transparent"
        )
        self.frame_botones_generacion.pack(side="right")
        self.boton_generar = ctk.CTkButton(
            self.frame_botones_generacion,
            text="Generar",
            **estilo_boton_secundario(),
            command=self.generar_datos
        )
        self.boton_generar.pack(side="left", padx=5)

        self.boton_limpiar = ctk.CTkButton(
            self.frame_botones_generacion,
            text="Limpiar",
            **estilo_boton_secundario(),
            command=self.limpiar
        )
        self.boton_limpiar.pack(side="left", padx=5)

        self.frame_especial = ctk.CTkFrame(self.frame_datos, fg_color="transparent")
        self.frame_especial.grid_columnconfigure(0, weight=1)
        self.frame_especial.grid_columnconfigure(3, weight=1)
        self.lbl_operacion_especial = ctk.CTkLabel(
            self.frame_especial,
            text="Operación especial: requiere una interfaz dedicada",
            text_color=TEXTO_CLARO,
            font=estilo_boton_principal()["font"]
        )
        self.lbl_operacion_especial.grid(row=0, column=1, padx=10, pady=5)
        self.boton_abrir_especial = ctk.CTkButton(
            self.frame_especial,
            text="Abrir ventana especial",
            **estilo_boton_principal(),
            command=self.accion_calcular
        )
        self.boton_abrir_especial.grid(row=0, column=2, padx=10, pady=5)

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
            text="Vista previa de datos",
            font=(FUENTE_CONTROLES, 14, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(pady=(10, 4))

        self.txt_previsualizacion = ctk.CTkTextbox(
            self.frame_previsualizacion,
            font=("Consolas", 12),
            **estilo_consola_resultado(),
        )
        self.txt_previsualizacion.pack(fill="both", expand=True, padx=8, pady=8)
        self._escribir_previsualizacion("Seleccione una operación y configure sus dimensiones.")

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
                "Flujo de Red",
                "Matrices Particionadas"
            ],
            command=self.cambiar_operacion,
            **estilo_menu_desplegable()
        )
        self.menu_operacion.set("A × u")
        self.menu_operacion.grid(row=0, column=1, padx=5, pady=5)

        # ----------------------------------------------------
        # FORMATO
        # ----------------------------------------------------
        self.lbl_formato = ctk.CTkLabel(self.frame_inferior, text="Formato:", text_color=TEXTO_CLARO)
        self.lbl_formato.grid(row=0, column=2, padx=5, pady=5)
        
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
        self.boton_calcular = ctk.CTkButton(
            self.frame_inferior,
            text="Calcular",
            **estilo_boton_principal(),
            command=self.accion_calcular
        )
        self.boton_calcular.grid(row=0, column=5, padx=10, pady=5)

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

        self.cambiar_operacion()

    def cambiar_operacion(self, operacion=None):
        operacion = operacion or self.menu_operacion.get()

        for frame in (
            self.frame_dimensiones_matriz,
            self.frame_dimensiones_vector,
            self.frame_dimensiones_cantidad
        ):
            frame.pack_forget()
        self.frame_dimensiones.pack_forget()
        self.frame_especial.pack_forget()
        self.frame_botones_generacion.pack_forget()

        self.lbl_formato.grid()
        self.menu_formato.grid()
        self.boton_calcular.grid()
        self.entry_escalar.grid_remove()

        especiales = {
            "Tabla de Intercambio": "Tabla de Intercambio (Modelo Leontief)",
            "Flujo de Red": "Flujo de Red",
            "Matrices Particionadas": "Matrices Particionadas"
        }
        if operacion in especiales:
            self.lbl_operacion_especial.configure(
                text=f"{especiales[operacion]}: requiere interfaz dedicada"
            )
            self.boton_abrir_especial.configure(
                text=f"Abrir {especiales[operacion]}"
            )
            self.frame_especial.pack(fill="x", expand=True)
            self.lbl_formato.grid_remove()
            self.menu_formato.grid_remove()
            self.boton_calcular.grid_remove()
            self._limpiar_datos_generados()
            self._escribir_previsualizacion(
                "Esta operación se abrirá en una ventana especializada."
            )
            return

        self.boton_generar.configure(text="Generar datos")
        self.frame_dimensiones.pack(side="left", expand=True)
        self.frame_botones_generacion.pack(side="right")

        solo_vectores = {"u + v", "c(u)", "Combinación lineal"}
        operaciones_con_matriz = {
            "A × u", "A(u + v)", "A(u + v + ...)", "A(cu)",
            "A(u + v) = Au + Av", "A(cu) = c(Au)",
            "Mostrar columnas de A", "Sistema a ecuación vectorial",
            "Transpuesta de A", "Matriz por escalar (cA)", "Resolver Ax = b"
        }
        if operacion in solo_vectores:
            self.lbl_dimension_vector.configure(text="Dimensión del vector:")
            self.frame_dimensiones_vector.pack(side="left")
        elif operacion in operaciones_con_matriz:
            self.frame_dimensiones_matriz.pack(side="left")

        if operacion in {"A(u + v + ...)", "Combinación lineal"}:
            self.frame_dimensiones_cantidad.pack(side="left")

        if operacion in {
            "Multiplicación de vector por escalar",
            "c(u)", "A(cu)", "A(cu) = c(Au)", "Matriz por escalar (cA)"
        }:
            self.entry_escalar.grid()

        self._limpiar_datos_generados()
        self._escribir_previsualizacion(
            "Configure las dimensiones y pulse 'Generar datos'."
        )

    def _limpiar_datos_generados(self):
        for widget in self.frame_centro.winfo_children():
            widget.destroy()
        self.matriz_entries = []
        self.vector_entries = []
        self.vector_b_entries = []
        self.vector_names = []

    # ========================================================
    # GENERAR MATRIZ Y VECTORES
    # ========================================================

    def generar_datos(self):
        operacion = self.menu_operacion.get()
        operaciones_especiales = {
            "Tabla de Intercambio", "Flujo de Red", "Matrices Particionadas"
        }
        if operacion in operaciones_especiales:
            self.accion_calcular()
            return

        requiere_matriz = operacion not in {"u + v", "c(u)", "Combinación lineal"}
        requiere_dimension_vector = operacion in {"u + v", "c(u)", "Combinación lineal"}
        requiere_b = operacion in {"Resolver Ax = b", "Sistema a ecuación vectorial"}
        operaciones_con_vector = {
            "A × u", "A(u + v)", "A(u + v + ...)", "A(cu)",
            "A(u + v) = Au + Av", "A(cu) = c(Au)", "u + v",
            "c(u)", "Combinación lineal"
        }
        requiere_vectores = operacion in operaciones_con_vector

        try:
            if requiere_dimension_vector:
                dimension = int(self.entry_dimension_vector.get())
                if dimension <= 0:
                    raise ValueError("La dimensión debe ser mayor que cero.")
                filas = dimension
                columnas = dimension
            elif requiere_matriz:
                filas = int(self.entry_filas.get())
                columnas = int(self.entry_columnas.get())
                if filas <= 0 or columnas <= 0:
                    raise ValueError("Las dimensiones de A deben ser mayores que cero.")
            else:
                filas = columnas = 0

            if operacion in {"A(u + v + ...)", "Combinación lineal"}:
                cantidad_vectores = int(self.entry_cantidad_vectores.get())
                minimo = 2 if operacion == "A(u + v + ...)" else 1
                if cantidad_vectores < minimo:
                    raise ValueError(f"Se requieren al menos {minimo} vectores.")
            elif operacion == "A(u + v)" or operacion == "A(u + v) = Au + Av" or operacion == "u + v":
                cantidad_vectores = 2
            elif requiere_vectores:
                cantidad_vectores = 1
            else:
                cantidad_vectores = 0
        except ValueError as error:
            mensaje = str(error)
            if "invalid literal for int()" in mensaje:
                mensaje = "Las dimensiones y cantidades deben ser enteros positivos."
            print(f"VALIDACIÓN: {mensaje}")
            self.mostrar_resultado(f"Error: {error}")
            return

        self._limpiar_datos_generados()
        fila_siguiente = 0

        if requiere_matriz:
            ctk.CTkLabel(
                self.frame_centro,
                text="MATRIZ A",
                font=("Arial", 18, "bold")
            ).grid(row=0, column=0, columnspan=columnas, pady=10)
            for i in range(filas):
                fila_entries = []
                for j in range(columnas):
                    entry = ctk.CTkEntry(self.frame_centro, width=80)
                    entry.grid(row=i + 1, column=j, padx=5, pady=5)
                    entry.bind("<KeyRelease>", lambda event: self.actualizar_previsualizacion())
                    fila_entries.append(entry)
                self.matriz_entries.append(fila_entries)
            fila_siguiente = filas + 3

        if requiere_vectores:
            ctk.CTkLabel(
                self.frame_centro,
                text="VECTORES",
                font=("Arial", 18, "bold")
            ).grid(row=fila_siguiente, column=0, columnspan=max(cantidad_vectores, 1), pady=10)
            vector_dimension = columnas if requiere_matriz else filas
            for j in range(cantidad_vectores):
                nombre = self.generar_nombre_vector(j)
                self.vector_names.append(nombre)
                ctk.CTkLabel(
                    self.frame_centro,
                    text=nombre,
                    font=("Arial", 16, "bold")
                ).grid(row=fila_siguiente + 1, column=j, padx=10, pady=5)
                entradas = []
                for i in range(vector_dimension):
                    entry = ctk.CTkEntry(self.frame_centro, width=80)
                    entry.grid(row=fila_siguiente + 2 + i, column=j, padx=10, pady=5)
                    entry.bind("<KeyRelease>", lambda event: self.actualizar_previsualizacion())
                    entradas.append(entry)
                self.vector_entries.append(entradas)
            fila_siguiente += vector_dimension + 3

        if requiere_b:
            ctk.CTkLabel(
                self.frame_centro,
                text="VECTOR b (términos independientes)",
                font=("Arial", 18, "bold")
            ).grid(row=fila_siguiente, column=0, columnspan=max(filas, 1), pady=10)
            for i in range(filas):
                entry = ctk.CTkEntry(self.frame_centro, width=80)
                entry.grid(row=fila_siguiente + 1 + i, column=0, padx=5, pady=5)
                entry.bind("<KeyRelease>", lambda event: self.actualizar_previsualizacion())
                self.vector_b_entries.append(entry)

        self.actualizar_previsualizacion()
        self.mostrar_resultado(f"Entradas generadas para: {operacion}.")

    def actualizar_previsualizacion(self):
        """Muestra únicamente los datos generados para la operación activa."""
        if not hasattr(self, "txt_previsualizacion"):
            return

        if not (self.matriz_entries or self.vector_entries or self.vector_b_entries):
            self._escribir_previsualizacion("Configure la operación y genere sus datos.")
            return

        lineas = []
        if self.matriz_entries:
            lineas.append("A =")
            lineas.extend(
                "[ " + ", ".join(entry.get().strip() or "_" for entry in fila) + " ]"
                for fila in self.matriz_entries
            )

        for indice, entradas in enumerate(self.vector_entries):
            if lineas:
                lineas.append("")
            nombre = self.vector_names[indice] if indice < len(self.vector_names) else f"u{indice + 1}"
            valores = [entry.get().strip() or "_" for entry in entradas]
            lineas.append(f"{nombre} = [ " + ", ".join(valores) + " ]")

        if self.vector_b_entries:
            valores_b = [entry.get().strip() or "_" for entry in self.vector_b_entries]
            if lineas:
                lineas.append("")
            lineas.append("b = [ " + ", ".join(valores_b) + " ]")

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

    def abrir_particiones(self):
        """Abre las operaciones por bloques desde el módulo matricial."""
        self.withdraw()
        from core.ui.particiones_gui import VistaParticiones

        VistaParticiones(self)

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
            if operacion == "Matrices Particionadas":
                self.abrir_particiones()
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
        reproducir_sonido_error(self, texto)
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)

    def limpiar(self):
        self.entry_filas.delete(0, "end")
        self.entry_columnas.delete(0, "end")
        self.entry_dimension_vector.delete(0, "end")
        self.entry_cantidad_vectores.delete(0, "end")
        self.entry_escalar.delete(0, "end")

        self._limpiar_datos_generados()
        self._escribir_previsualizacion("Configure la operación y genere sus datos.")
        self.mostrar_resultado("")


# ============================================================
# EJECUCION INDEPENDIENTE (PRUEBA)
# ============================================================

if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()  # Oculta la ventana principal temporalmente si se prueba directo
    ventana_matriciales = VistaMatricial(app)
    app.mainloop()