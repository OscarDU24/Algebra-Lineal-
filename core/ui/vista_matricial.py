# ============================================================
# CALCULADORA DE MATRICES Y VECTORES - FIA UAM
# ============================================================

from core.ui.ctk_compat import ctk

from core.matriciales import conversionesMatriciales as conv
from core.matriciales import operacionesMatriciales as op
from core.matriciales import verificacionMatriciales as ver
from core.matriciales import visualizacionMatriciales as vis


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

        self.master_dashboard = master
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        
        self.title("Calculadora de Matrices y Vectores - FIA UAM")
        self.geometry("1100x800")

        # Entradas de la matriz
        self.matriz_entries = []

        # Entradas de los vectores
        self.vector_entries = []

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
        self.frame_superior = ctk.CTkFrame(self)
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
        ctk.CTkLabel(frame_datos, text="Filas de A:").grid(row=0, column=0, padx=5)
        self.entry_filas = ctk.CTkEntry(frame_datos, width=80, placeholder_text="2")
        self.entry_filas.grid(row=0, column=1, padx=5)

        # ----------------------------------------------------
        # COLUMNAS
        # ----------------------------------------------------
        ctk.CTkLabel(frame_datos, text="Columnas de A:").grid(row=0, column=2, padx=5)
        self.entry_columnas = ctk.CTkEntry(frame_datos, width=80, placeholder_text="2")
        self.entry_columnas.grid(row=0, column=3, padx=5)

        # ----------------------------------------------------
        # CANTIDAD DE VECTORES
        # ----------------------------------------------------
        ctk.CTkLabel(frame_datos, text="Cantidad de vectores:").grid(row=0, column=4, padx=5)
        self.entry_cantidad_vectores = ctk.CTkEntry(frame_datos, width=80, placeholder_text="2")
        self.entry_cantidad_vectores.grid(row=0, column=5, padx=5)

        # ----------------------------------------------------
        # BOTON GENERAR
        # ----------------------------------------------------
        boton_generar = ctk.CTkButton(
            frame_datos,
            text="Generar",
            command=self.generar_datos
        )
        boton_generar.grid(row=0, column=6, padx=10)

        # ----------------------------------------------------
        # BOTON LIMPIAR
        # ----------------------------------------------------
        boton_limpiar = ctk.CTkButton(
            frame_datos,
            text="Limpiar",
            command=self.limpiar
        )
        boton_limpiar.grid(row=0, column=7, padx=10)

    # ========================================================
    # FRAME CENTRAL
    # ========================================================

    def crear_frame_central(self):
        self.frame_central = ctk.CTkScrollableFrame(
            self,
            label_text="Datos de la operación"
        )
        self.frame_central.pack(fill="both", expand=True, padx=15, pady=5)

    # ========================================================
    # FRAME INFERIOR
    # ========================================================

    def crear_frame_inferior(self):
        self.frame_inferior = ctk.CTkFrame(self)
        self.frame_inferior.pack(fill="x", padx=15, pady=15)

        # ----------------------------------------------------
        # OPERACION
        # ----------------------------------------------------
        ctk.CTkLabel(self.frame_inferior, text="Operación:").grid(row=0, column=0, padx=5, pady=5)
        
        self.menu_operacion = ctk.CTkOptionMenu(
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
                "Mostrar columnas de A"
            ]
        )
        self.menu_operacion.grid(row=0, column=1, padx=5, pady=5)

        # ----------------------------------------------------
        # FORMATO
        # ----------------------------------------------------
        ctk.CTkLabel(self.frame_inferior, text="Formato:").grid(row=0, column=2, padx=5, pady=5)
        
        self.menu_formato = ctk.CTkOptionMenu(
            self.frame_inferior,
            values=["Decimales", "Fracciones"]
        )
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
            command=self.accion_calcular
        )
        boton_calcular.grid(row=0, column=5, padx=10, pady=5)

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------
        self.texto_resultado = ctk.CTkTextbox(
            self.frame_inferior,
            height=180
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

        for widget in self.frame_central.winfo_children():
            widget.destroy()

        self.matriz_entries = []
        self.vector_entries = []
        self.vector_names = []

        # MATRIZ A
        etiqueta_a = ctk.CTkLabel(
            self.frame_central,
            text="MATRIZ A",
            font=("Arial", 18, "bold")
        )
        etiqueta_a.grid(row=0, column=0, columnspan=columnas, pady=10)

        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                entry = ctk.CTkEntry(self.frame_central, width=80)
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
                fila_entries.append(entry)
            self.matriz_entries.append(fila_entries)

        # VECTORES
        fila_vectores = filas + 3
        etiqueta_vectores = ctk.CTkLabel(
            self.frame_central,
            text="VECTORES",
            font=("Arial", 18, "bold")
        )
        etiqueta_vectores.grid(row=fila_vectores, column=0, columnspan=cantidad_vectores, pady=10)

        for j in range(cantidad_vectores):
            nombre = self.generar_nombre_vector(j)
            self.vector_names.append(nombre)

            etiqueta = ctk.CTkLabel(
                self.frame_central,
                text=nombre,
                font=("Arial", 16, "bold")
            )
            etiqueta.grid(row=fila_vectores + 1, column=j, padx=10, pady=5)

        for j in range(cantidad_vectores):
            entradas = []
            for i in range(columnas):
                entry = ctk.CTkEntry(self.frame_central, width=80)
                entry.grid(row=fila_vectores + 2 + i, column=j, padx=10, pady=5)
                entradas.append(entry)
            self.vector_entries.append(entradas)

        self.mostrar_resultado("Matriz y vectores generados correctamente.")

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

    # ========================================================
    # ACCION PRINCIPAL
    # ========================================================

    def accion_calcular(self):
        try:
            operacion = self.menu_operacion.get()

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

        for widget in self.frame_central.winfo_children():
            widget.destroy()

        self.matriz_entries = []
        self.vector_entries = []
        self.vector_names = []
        self.mostrar_resultado("")


# ============================================================
# EJECUCION INDEPENDIENTE (PRUEBA)
# ============================================================

if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()  # Oculta la ventana principal temporalmente si se prueba directo
    ventana_matriciales = VistaMatricial(app)
    app.mainloop()