from core.ui.ctk_compat import ctk
from core.ui.audio_manager import reproducir_sonido_error
from prettytable import PrettyTable, HRuleStyle, VRuleStyle

# 1. IMPORTACIONES ADAPTADAS A TU NUEVA ESTRUCTURA (core/lineal/...)
from core.lineal import conversiones as conv
from core.lineal.eliminacion import eliminacion_por_filas
from core.lineal.clasificacion import clasificar_sistema
from core.lineal.solucion import sustitucion_hacia_atras_detallada, extraer_solucion_rref
from core.lineal.verificacion import verificar_solucion
from core.lineal.visualizacion import imprimir_sistema_ecuaciones

# Configuración inicial del tema visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# 2. CAMBIO A CTkToplevel PARA QUE FUNCIONE JUNTO AL DASHBOARD
class VistaMatriz(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)
        
        # Referencia al Dashboard original para poder volver a él
        self.master_dashboard = master

        # Configuración de la ventana (Tu diseño intacto)
        self.title("Calculadora de Sistemas de Ecuaciones Lineales - FIA UAM")
        self.geometry("980x780")
        
        # 3. INTERCEPTAR LA X DE CERRAR LA VENTANA
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        # Almacenamiento bidimensional para los widgets CTkEntry
        self.matriz_entries = []
<<<<<<< Updated upstream
=======
        self.modo_matriz_pura = False
        # El checkbox solo afecta al modo inversa: permite usar b para resolver Ax=b.
        self.incluir_b_variable = ctk.BooleanVar(value=False)
>>>>>>> Stashed changes

        # Estructura de la interfaz
        self.crear_frame_superior()
        self.crear_frame_central()
        self.crear_frame_inferior()

        # Generar cuadrícula inicial 3x3
        self.generar_cuadricula_matriz()

    def al_cerrar(self):
        """Muestra el Dashboard nuevamente antes de destruir esta ventana."""
        self.master_dashboard.deiconify()
        self.destroy()

    def crear_frame_superior(self):
        """Frame de controles iniciales: dimensiones, generación y reinicio."""
        self.frame_sup = ctk.CTkFrame(self)
        self.frame_sup.pack(pady=10, padx=20, fill="x")

        # Título
        lbl_titulo = ctk.CTkLabel(self.frame_sup, text="Dimensiones:", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_titulo.pack(side="left", padx=10, pady=10)

        # Filas
        lbl_m = ctk.CTkLabel(self.frame_sup, text="Filas (m):")
        lbl_m.pack(side="left", padx=(10, 2))

        self.entry_m = ctk.CTkEntry(self.frame_sup, width=50)
        self.entry_m.insert(0, "3")
        self.entry_m.pack(side="left", padx=5)

        # Variables
        lbl_n = ctk.CTkLabel(self.frame_sup, text="Variables (n):")
        lbl_n.pack(side="left", padx=(10, 2))

        self.entry_n = ctk.CTkEntry(self.frame_sup, width=50)
        self.entry_n.insert(0, "3")
        self.entry_n.pack(side="left", padx=5)

        # Botón generar
        btn_generar = ctk.CTkButton(self.frame_sup, text="Generar Matriz", command=self.generar_cuadricula_matriz)
        btn_generar.pack(side="left", padx=15)

        # Botón limpiar
        btn_limpiar = ctk.CTkButton(self.frame_sup, text="Limpiar Valores", fg_color="#555555", hover_color="#333333", command=self.limpiar_entradas)
        btn_limpiar.pack(side="left", padx=5)

    def crear_frame_central(self):
        """Frame dinámico con barra de desplazamiento para la matriz aumentada."""
        self.frame_centro = ctk.CTkScrollableFrame(self, label_text="Matriz Aumentada [A | b]")
        self.frame_centro.pack(pady=10, padx=20, fill="both", expand=True)

    def crear_frame_inferior(self):
        """Frame de controles de cálculo y visor de resultados."""
        self.frame_inf = ctk.CTkFrame(self)
        self.frame_inf.pack(pady=10, padx=20, fill="both", expand=True)

        subframe_acciones = ctk.CTkFrame(self.frame_inf, fg_color="transparent")
        subframe_acciones.pack(fill="x", pady=5, padx=10)

        # Selección del método
        self.opcion_metodo = ctk.CTkOptionMenu(subframe_acciones, values=["Método Escalonado", "Gauss", "Gauss-Jordan"])
        self.opcion_metodo.pack(side="left", padx=(0, 10))

        # Formato de números
        self.opcion_numform = ctk.CTkOptionMenu(subframe_acciones, values=["Fracciones", "Decimales"])
        self.opcion_numform.pack(side="left", padx=(0, 10))

        # Botón resolver
        btn_resolver = ctk.CTkButton(subframe_acciones, text="Resolver Sistema", fg_color="green", hover_color="darkgreen", font=ctk.CTkFont(weight="bold"), command=self.accion_resolver)
        btn_resolver.pack(side="left")

        # Visor de resultados
        self.txt_resultados = ctk.CTkTextbox(self.frame_inf, font=("Courier New", 12))
        self.txt_resultados.pack(pady=10, padx=10, fill="both", expand=True)
        self._escribir_en_visor("Ingrese los coeficientes en la matriz y presione 'Resolver Sistema'...")

<<<<<<< Updated upstream
    def generar_cuadricula_matriz(self):
=======
    def generar_cuadricula_matriz(self, valores_matriz=None):
        modo_matriz_pura = self.opcion_metodo.get() == "Matriz pura (A⁻¹)"
        # En modo sistema siempre existe TI; en modo inversa depende del checkbox.
        incluir_b = not modo_matriz_pura or self.incluir_b_variable.get()
        self.frame_centro.configure(
            label_text="Matriz editable [A | b]" if incluir_b else "Matriz de coeficientes A"
        )
>>>>>>> Stashed changes
        for widget in self.frame_centro.winfo_children():
            widget.destroy()

        self.matriz_entries.clear()

        try:
            m = int(self.entry_m.get())
            n = int(self.entry_n.get())
            if m <= 0 or n <= 0:
                raise ValueError
        except ValueError:
            self._escribir_en_visor("ERROR: Ingrese números enteros positivos válidos para m y n.")
            return

        for i in range(m):
            fila_entries = []
            for j in range(n + 1):
                entry = ctk.CTkEntry(self.frame_centro, width=65, justify="center")
                entry.grid(row=i, column=j, padx=4, pady=4)
                if j == n:
                    entry.configure(fg_color="#2b2b2b", border_color="#1f538d")
                fila_entries.append(entry)
            self.matriz_entries.append(fila_entries)
<<<<<<< Updated upstream
=======
        self.actualizar_previsualizacion()

    def al_cambiar_metodo(self, metodo):
        modo_matriz_pura = metodo == "Matriz pura (A⁻¹)"
        if modo_matriz_pura == self.modo_matriz_pura:
            return

        self.modo_matriz_pura = modo_matriz_pura
        self.lbl_n.configure(
            text="Columnas (n):" if modo_matriz_pura else "Variables (n):"
        )
        if modo_matriz_pura:
            self.checkbox_incluir_b.pack(side="left", padx=(0, 10))
        else:
            self.checkbox_incluir_b.pack_forget()
            self.incluir_b_variable.set(False)
        self.btn_resolver.configure(
            text=(
                "Resolver Ax = b con A⁻¹"
                if modo_matriz_pura and self.incluir_b_variable.get()
                else "Calcular inversa"
                if modo_matriz_pura
                else "Resolver Sistema"
            )
        )
        self.generar_cuadricula_matriz()

    def al_cambiar_inclusion_b(self):
        try:
            cantidad_columnas_a = int(self.entry_n.get())
        except ValueError:
            incluia_b_antes = not self.incluir_b_variable.get()
            cantidad_columnas_a = max(
                (len(fila) - 1) if incluia_b_antes else len(fila)
                for fila in self.matriz_entries
            ) if self.matriz_entries else 0
        valores_matriz = [
            [entry.get() for entry in fila[:cantidad_columnas_a]]
            for fila in self.matriz_entries
        ]
        # Regenerar añade o quita la columna b sin perder los coeficientes ya ingresados.
        self.btn_resolver.configure(
            text=(
                "Resolver Ax = b con A⁻¹"
                if self.incluir_b_variable.get()
                else "Calcular inversa"
            )
        )
        self.generar_cuadricula_matriz(valores_matriz)
>>>>>>> Stashed changes

    def limpiar_entradas(self):
        for fila in self.matriz_entries:
            for entry in fila:
                entry.delete(0, "end")
        self._escribir_en_visor("Campos limpios. Ingrese un nuevo sistema.")

    def obtener_matriz_desde_gui(self):
        matriz = []
        for i, fila_entries in enumerate(self.matriz_entries):
            fila_vals = []
            for j, entry in enumerate(fila_entries):
                val_str = entry.get().strip()
                if not val_str:
                    raise ValueError(f"La casilla en la fila {i + 1}, columna {j + 1} está vacía.")
                try:
                    val_num = conv.convertir_a_decimal(val_str)
                    fila_vals.append(val_num)
                except ValueError:
                    raise ValueError(f"El valor '{val_str}' en la fila {i + 1}, columna {j + 1} no es válido.")
            matriz.append(fila_vals)
        return matriz

    def _matriz_a_string(self, matriz, formato):
        table = PrettyTable()
        table.hrules = HRuleStyle.HEADER
        table.vrules = VRuleStyle.FRAME
        campos = [f"X{i + 1}" for i in range(len(matriz[0]) - 1)]
        campos.append("TI")
        table.field_names = campos

        for fila in matriz:
            str_fila = []
            for j in range(len(matriz[0]) - 1):
                if formato == "fr":
                    str_fila.append(conv.convertir_a_fraccion(fila[j]))
                else:
                    str_fila.append(f"{fila[j]:0.2}".rstrip("0").rstrip("."))
            if formato == "fr":
                str_fila.append(conv.convertir_a_fraccion(fila[-1]))
            else:
                str_fila.append(f"{fila[-1]:0.2f}".rstrip("0").rstrip("."))
            table.add_row(str_fila)
        return str(table)

<<<<<<< Updated upstream
=======
    def _matriz_cuadrada_a_string(self, matriz, formato):
        table = PrettyTable()
        table.hrules = HRuleStyle.HEADER
        table.vrules = VRuleStyle.FRAME
        table.field_names = [f"C{i + 1}" for i in range(len(matriz))]
        for fila in matriz:
            table.add_row([self._formatear_valor(valor, formato) for valor in fila])
        return str(table)

    def _matriz_aumentada_inversa_a_string(self, matriz, dimension, formato):
        table = PrettyTable()
        table.hrules = HRuleStyle.HEADER
        table.vrules = VRuleStyle.FRAME
        table.field_names = (
            [f"A{i + 1}" for i in range(dimension)]
            + ["|"]
            + [f"I{i + 1}" for i in range(dimension)]
        )
        for fila in matriz:
            table.add_row(
                [self._formatear_valor(valor, formato) for valor in fila[:dimension]]
                + ["|"]
                + [self._formatear_valor(valor, formato) for valor in fila[dimension:]]
            )
        return str(table)

    def _descripcion_paso_inversa(self, operacion, formato):
        tipo = operacion["tipo"]
        if tipo == "inicial":
            return "Matriz aumentada inicial [A | I]:"
        if tipo == "intercambio":
            return (
                f"F{operacion['fila'] + 1} ↔ "
                f"F{operacion['otra_fila'] + 1}"
            )
        if tipo == "normalizar":
            return (
                f"F{operacion['fila'] + 1} = F{operacion['fila'] + 1} / "
                f"{self._formatear_valor(operacion['pivote'], formato)}"
            )
        if tipo == "eliminar":
            return (
                f"F{operacion['fila'] + 1} = F{operacion['fila'] + 1} - "
                f"({self._formatear_valor(operacion['factor'], formato)}) * "
                f"F{operacion['fila_pivote'] + 1}"
            )
        return "Operación elemental de fila:"

    def mostrar_matriz_inversa(
        self,
        matriz_a,
        matriz_inversa,
        pasos,
        producto_verificacion,
        formato,
        vector_b=None,
        vector_solucion=None,
        producto_solucion=None
    ):
        dimension = len(matriz_a)
        salida = [
            "=========================================================",
            "          CÁLCULO DE LA MATRIZ INVERSA (A⁻¹)",
            "=========================================================",
            "",
            "Matriz original A de coeficientes recibida con éxito.",
            "Procesando reducción por Gauss-Jordan en [A | I]...",
            "",
            "Matriz original A:",
            self._matriz_cuadrada_a_string(matriz_a, formato),
            "",
            "Pasos de reducción por Gauss-Jordan en [A | I]:",
        ]
        # La traza guarda la descripción estructurada y una copia de [A | I] tras cada operación.
        for operacion, matriz_paso in pasos:
            salida.append(self._descripcion_paso_inversa(operacion, formato))
            salida.append(
                self._matriz_aumentada_inversa_a_string(
                    matriz_paso,
                    dimension,
                    formato
                )
            )
            salida.append("")

        salida.extend([
            "Matriz Inversa Resultante:",
            self._matriz_cuadrada_a_string(matriz_inversa, formato),
        ])
        if vector_b is not None:
            # En el modo combinado, b se conserva aparte de A y se aplica x = A^-1 b.
            salida.extend([
                "",
                "Resolución del sistema Ax = b usando la inversa:",
                "b = [ " + ", ".join(
                    self._formatear_valor(valor, formato)
                    for valor in vector_b
                ) + " ]ᵀ",
                "x = A⁻¹ · b:"
            ])
            for indice, fila in enumerate(matriz_inversa):
                terminos = [
                    f"({self._formatear_valor(coeficiente, formato)})"
                    f"({self._formatear_valor(vector_b[columna], formato)})"
                    for columna, coeficiente in enumerate(fila)
                ]
                salida.append(
                    f"x{indice + 1} = " + " + ".join(terminos)
                    + f" = {self._formatear_valor(vector_solucion[indice], formato)}"
                )
            salida.extend([
                "",
                "Vector solución x = [x1, x2, ..., xn]ᵀ:",
                "[ " + ", ".join(
                    self._formatear_valor(valor, formato)
                    for valor in vector_solucion
                ) + " ]ᵀ",
                "Producto matricial A⁻¹ · b:",
                "\n".join(
                    f"| {self._formatear_valor(fila[0], formato)} |"
                    for fila in producto_solucion
                ),
            ])
        salida.extend([
            "",
            "Comprobación: A · A⁻¹ = Matriz Identidad (I)",
            self._matriz_cuadrada_a_string(producto_verificacion, formato),
        ])
        self._escribir_en_visor("\n".join(salida))

>>>>>>> Stashed changes
    def _escribir_en_visor(self, texto):
        reproducir_sonido_error(self, texto)
        self.txt_resultados.configure(state="normal")
        self.txt_resultados.delete("0.0", "end")
        self.txt_resultados.insert("0.0", texto)
        self.txt_resultados.configure(state="disabled")

    def accion_resolver(self):
        try:
            matriz_original = self.obtener_matriz_desde_gui()
        except ValueError as e:
            self._escribir_en_visor(f"ERROR DE ENTRADA:\n{str(e)}")
            return

        m = len(matriz_original)
<<<<<<< Updated upstream
=======
        if metodo_gui == "Matriz pura (A⁻¹)":
            try:
                incluir_b = self.incluir_b_variable.get()
                n = int(self.entry_n.get())
                # La cuadrícula puede ser [A] o [A | b]; separar ambos datos antes de invertir.
                matriz_a = [fila[:n] for fila in matriz_original]
                vector_b = [fila[n] for fila in matriz_original] if incluir_b else None
                # La inversión siempre recibe solo A; b se usa después en el producto A^-1 b.
                resultado = enrutar_resolucion_matricial(
                    matriz_a,
                    vector_b=None,
                    formato_fracciones=formato_fracciones
                )
                producto_solucion = None
                vector_solucion = None
                if vector_b is not None:
                    # Convertir b a matriz columna permite reutilizar el producto matricial general.
                    vector_b_columna = [[valor] for valor in vector_b]
                    producto_solucion = multiplicar_matrices(
                        resultado["matriz_inversa"],
                        vector_b_columna
                    )
                    vector_solucion = [fila[0] for fila in producto_solucion]
                # Comprobar numéricamente que A por su inversa aproxima la identidad.
                producto_verificacion = multiplicar_matrices(
                    matriz_a,
                    resultado["matriz_inversa"]
                )
                self.mostrar_matriz_inversa(
                    matriz_a,
                    resultado["matriz_inversa"],
                    resultado["pasos"],
                    producto_verificacion,
                    formato,
                    vector_b=vector_b,
                    vector_solucion=vector_solucion,
                    producto_solucion=producto_solucion
                )
            except ValueError as error:
                if "no se puede calcular su inversa" in str(error):
                    self._escribir_en_visor(
                        "Error: El sistema es singular (Determinante = 0), "
                        "por lo tanto la matriz A no tiene inversa"
                    )
                else:
                    self._escribir_en_visor(f"ERROR: {error}")
            return

>>>>>>> Stashed changes
        n = len(matriz_original[0]) - 1
        metodo_gui = self.opcion_metodo.get()

        if metodo_gui == "Método Escalonado":
            modo = "escalonado"
        elif metodo_gui == "Gauss":
            modo = "gauss"
        else:
            modo = "gauss_jordan"

        formato = "fr" if self.opcion_numform.get() == "Fracciones" else "dc"

        matriz_resultado, pasos, columnas_pivote = eliminacion_por_filas(matriz_original, modo)

        salida = []
        salida.append("=========================================================")
        salida.append(f"   PROCESO DE ELIMINACIÓN POR FILAS ({metodo_gui.upper()})")
        salida.append("=========================================================\n")

        for descripcion, matriz_paso in pasos[1:]:
            salida.append(f">> {descripcion}:")
            salida.append(self._matriz_a_string(matriz_paso, formato))
            salida.append("")

        if modo == "escalonado":
            salida.append("=========================================================")
            salida.append("   MATRIZ EN FORMA ESCALONADA")
            salida.append("=========================================================")
            salida.append(self._matriz_a_string(matriz_resultado, formato))
            salida.append("")
        elif modo == "gauss":
            salida.append("=========================================================")
            salida.append("   SISTEMA DE ECUACIONES EQUIVALENTE (GAUSS)")
            salida.append("=========================================================")
            salida.append(imprimir_sistema_ecuaciones(matriz_resultado))
            salida.append("")
        elif modo == "gauss_jordan":
            salida.append("=========================================================")
            salida.append("   MATRIZ EN FORMA ESCALONADA REDUCIDA")
            salida.append("=========================================================")
            salida.append(self._matriz_a_string(matriz_resultado, formato))
            salida.append("")

        clasificacion = clasificar_sistema(matriz_resultado, columnas_pivote)

        salida.append("=========================================================")
        salida.append("   ANÁLISIS DE PIVOTES Y CLASIFICACIÓN DEL SISTEMA")
        salida.append("=========================================================")

        cols_pivote_str = ", ".join([f"x{c + 1} (Columna {c + 1})" for c in columnas_pivote])
        salida.append(f"• Columnas Pivote: {cols_pivote_str if cols_pivote_str else 'Ninguna'}")

        todas_las_vars = set(range(n))
        vars_libres = todas_las_vars - set(columnas_pivote)

        if vars_libres:
            libres_str = ", ".join([f"x{c + 1}" for c in sorted(vars_libres)])
            salida.append(f"• Variables Libres: Sí ({libres_str})")
        else:
            salida.append("• Variables Libres: No")

        salida.append(f"• Clasificación: {clasificacion.upper()}\n")

        if clasificacion == "Sistema Consistente Determinado":
            if modo == "gauss_jordan":
                x = extraer_solucion_rref(matriz_resultado, n)
                salida.append("--- Solución leída directamente de la RREF ---")
            else:
                x, pasadas_despeje = sustitucion_hacia_atras_detallada(matriz_resultado, n)
                salida.append("--- Sustitución Hacia Atrás Paso a Paso ---")
                for paso_txt in pasadas_despeje:
                    salida.append(f"{paso_txt}\n")

            salida.append("--- Solución Única Encontrada ---")
            for i in range(n):
                val_formateado = conv.convertir_a_fraccion(x[i]) if formato == "fr" else f"{x[i]:.6f}"
                salida.append(f"  x{i + 1} = {val_formateado}")

            es_correcta = verificar_solucion(matriz_original, x)
            salida.append("\n--- Verificación en el sistema original ---")
            if es_correcta:
                salida.append("Comprobación exitosa: La solución satisface todas las ecuaciones.")
            else:
                salida.append("Advertencia: La solución no pudo ser verificada correctamente.")

        elif clasificacion == "Sistema Consistente Indeterminado":
            salida.append("--- Solución General (Infinitas Soluciones) ---")
            salida.append("El sistema posee infinitas soluciones en función de las variables libres.")
            salida.append(f"Variables dependientes (con pivote): {[f'x{c + 1}' for c in columnas_pivote]}")
            salida.append(f"Variables libres: {[f'x{c + 1}' for c in sorted(vars_libres)]}")

        else:
            salida.append("--- Sistema Inconsistente ---")
            salida.append("El sistema no tiene solución.")
            salida.append("Se detectó una contradicción del tipo 0 = k (con k distinto de 0).")

        self._escribir_en_visor("\n".join(salida))