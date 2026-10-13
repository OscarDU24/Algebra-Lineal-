from core.ui.ctk_compat import ctk
from core.ui.audio_manager import reproducir_sonido_error
from prettytable import PrettyTable, HRuleStyle, VRuleStyle

from core.lineal import conversiones as conv
from core.lineal.solucion import (
    enrutar_resolucion_matricial,
    multiplicar_matrices,
)
from core.lineal.verificacion import verificar_solucion
from core.lineal.visualizacion import imprimir_sistema_ecuaciones
from core.ui.tema import (
    FONDO_BOTON,
    FONDO_CALCULADORA,
    FONDO_TERMINAL,
    FONDO_TERMINO_INDEPENDIENTE,
    FUENTE_CONTROLES,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_menu_desplegable,
    estilo_panel_contenedor,
)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class VistaMatriz(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)
        
        self.master_dashboard = master

        self.title("Resolver Sistemas de Ecuaciones Lineales")
        self.geometry("980x780")
        
        # Asegurar foco en la ventana secundaria
        self.lift()
        self.focus_force()
        
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        self.matriz_entries = []
        self.modo_matriz_pura = False
        # El checkbox solo afecta al modo inversa: permite usar b para resolver Ax=b.
        self.incluir_b_variable = ctk.BooleanVar(value=False)

        self.crear_frame_superior()
        self.crear_frame_central()
        self.crear_frame_inferior()

        self.generar_cuadricula_matriz()

    def al_cerrar(self):
        """Muestra el Dashboard nuevamente antes de destruir esta ventana."""
        self.master_dashboard.deiconify()
        self.destroy()

    def crear_frame_superior(self):
        """Frame de controles iniciales: dimensiones, generación y reinicio."""
        self.frame_sup = ctk.CTkFrame(self, **estilo_panel_contenedor())
        self.frame_sup.pack(pady=10, padx=20, fill="x")

        lbl_titulo = ctk.CTkLabel(self.frame_sup, text="Dimensiones:", text_color="#ffffff", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_titulo.pack(side="left", padx=10, pady=10)

        lbl_m = ctk.CTkLabel(self.frame_sup, text="Filas (m):", text_color="#ffffff")
        lbl_m.pack(side="left", padx=(10, 2))

        self.entry_m = ctk.CTkEntry(self.frame_sup, width=50)
        self.entry_m.insert(0, "3")
        self.entry_m.pack(side="left", padx=5)

        self.lbl_n = ctk.CTkLabel(self.frame_sup, text="Variables (n):", text_color="#ffffff")
        self.lbl_n.pack(side="left", padx=(10, 2))

        self.entry_n = ctk.CTkEntry(self.frame_sup, width=50)
        self.entry_n.insert(0, "3")
        self.entry_n.pack(side="left", padx=5)

        btn_generar = ctk.CTkButton(self.frame_sup, text="Generar Matriz", **estilo_boton_secundario(), command=self.generar_cuadricula_matriz)
        btn_generar.pack(side="left", padx=15)

        btn_limpiar = ctk.CTkButton(self.frame_sup, text="Limpiar Valores", **estilo_boton_secundario(), command=self.limpiar_entradas)
        btn_limpiar.pack(side="left", padx=5)

    def crear_frame_central(self):
        """Frame dinámico con barra de desplazamiento para la matriz aumentada."""
        self.frame_central = ctk.CTkFrame(self, **estilo_panel_contenedor())
        self.frame_central.pack(pady=10, padx=20, fill="both", expand=True)
        self.frame_centro = ctk.CTkScrollableFrame(
            self.frame_central,
            label_text="Matriz editable [A | b]",
            width=520,
            **estilo_panel_contenedor()
        )
        self.frame_centro.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.frame_previsualizacion = ctk.CTkFrame(
            self.frame_central, width=330, **estilo_panel_contenedor()
        )
        self.frame_previsualizacion.pack(side="right", fill="both", padx=(8, 0))
        self.frame_previsualizacion.pack_propagate(False)
        ctk.CTkLabel(
            self.frame_previsualizacion,
            text="Vista previa de la matriz",
            font=(FUENTE_CONTROLES, 14, "bold"),
            text_color="#ffffff",
        ).pack(pady=(10, 4))
        self.txt_previsualizacion = ctk.CTkTextbox(
            self.frame_previsualizacion,
            font=("Consolas", 12),
            **estilo_consola_resultado(),
        )
        self.txt_previsualizacion.pack(fill="both", expand=True, padx=8, pady=8)
        self._escribir_previsualizacion("Genere la matriz y complete sus valores.")

    def crear_frame_inferior(self):
        """Frame de controles de cálculo y visor de resultados."""
        self.frame_inf = ctk.CTkFrame(self, **estilo_panel_contenedor())
        self.frame_inf.pack(pady=10, padx=20, fill="both", expand=True)

        subframe_acciones = ctk.CTkFrame(self.frame_inf, fg_color="transparent")
        subframe_acciones.pack(fill="x", pady=5, padx=10)

        self.opcion_metodo = ctk.CTkComboBox(
            subframe_acciones,
            values=[
                "Método Escalonado",
                "Gauss",
                "Gauss-Jordan",
                "Matriz pura (A⁻¹)"
            ],
            command=self.al_cambiar_metodo,
            **estilo_menu_desplegable()
        )
        self.opcion_metodo.set("Método Escalonado")
        self.opcion_metodo.pack(side="left", padx=(0, 10))

        self.checkbox_incluir_b = ctk.CTkCheckBox(
            subframe_acciones,
            text="Incluir términos independientes (b)",
            variable=self.incluir_b_variable,
            command=self.al_cambiar_inclusion_b,
            text_color=TEXTO_CLARO,
            fg_color="#fe0000",
            hover_color="#b30000",
        )

        self.opcion_numform = ctk.CTkComboBox(subframe_acciones, values=["Fracciones", "Decimales"], **estilo_menu_desplegable())
        self.opcion_numform.set("Fracciones")
        self.opcion_numform.pack(side="left", padx=(0, 10))

        self.btn_resolver = ctk.CTkButton(
            subframe_acciones,
            text="Resolver Sistema",
            **estilo_boton_principal(),
            command=self.accion_resolver
        )
        self.btn_resolver.pack(side="left")

        self.txt_resultados = ctk.CTkTextbox(self.frame_inf, font=("Courier New", 12), **estilo_consola_resultado())
        self.txt_resultados.pack(pady=10, padx=10, fill="both", expand=True)
        self._escribir_en_visor("Ingrese los coeficientes en la matriz y presione 'Resolver Sistema'...")

    def generar_cuadricula_matriz(self, valores_matriz=None):
        modo_matriz_pura = self.opcion_metodo.get() == "Matriz pura (A⁻¹)"
        # En modo sistema siempre existe TI; en modo inversa depende del checkbox.
        incluir_b = not modo_matriz_pura or self.incluir_b_variable.get()
        self.frame_centro.configure(
            label_text="Matriz editable [A | b]" if incluir_b else "Matriz de coeficientes A"
        )
        for widget in self.frame_centro.winfo_children():
            widget.destroy()

        self.matriz_entries.clear()

        try:
            m = int(self.entry_m.get())
            n = int(self.entry_n.get())
            if m <= 0 or n <= 0:
                raise ValueError
            if modo_matriz_pura and m != n:
                raise ValueError("El modo matriz pura requiere que A sea cuadrada (m = n).")
        except ValueError as error:
            mensaje = str(error)
            if "invalid literal for int()" in mensaje or not mensaje:
                mensaje = "Las dimensiones deben ser enteros positivos."
            print(f"VALIDACIÓN: {mensaje}")
            self._escribir_en_visor(f"ERROR: {mensaje}")
            return

        cantidad_columnas = n + 1 if incluir_b else n
        for i in range(m):
            fila_entries = []
            for j in range(cantidad_columnas):
                entry = ctk.CTkEntry(self.frame_centro, width=65, justify="center")
                entry.grid(row=i, column=j, padx=4, pady=4)
                entry.bind(
                    "<KeyRelease>",
                    lambda event: self.actualizar_previsualizacion()
                )
                if incluir_b and j == n:
                    entry.configure(
                        fg_color=FONDO_TERMINO_INDEPENDIENTE,
                        border_color="#ffffff"
                    )
                if valores_matriz and j < n and i < len(valores_matriz) and j < len(valores_matriz[i]):
                    valor_previo = valores_matriz[i][j]
                    if valor_previo:
                        entry.insert(0, valor_previo)
                fila_entries.append(entry)
            self.matriz_entries.append(fila_entries)
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

    def limpiar_entradas(self):
        for fila in self.matriz_entries:
            for entry in fila:
                entry.delete(0, "end")
        self.actualizar_previsualizacion()
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
                except ValueError:
                    raise ValueError(f"El valor '{val_str}' en la fila {i + 1}, columna {j + 1} no es válido.")
                if val_num is None:
                    raise ValueError(f"El valor '{val_str}' en la fila {i + 1}, columna {j + 1} no es válido.")
                fila_vals.append(val_num)
            matriz.append(fila_vals)
        return matriz

    def actualizar_previsualizacion(self):
        """Muestra A sola o el sistema Ax=b según las entradas visibles."""
        if not self.matriz_entries:
            return

        incluir_b = (
            not self.modo_matriz_pura
            or self.incluir_b_variable.get()
        )
        try:
            cantidad_columnas_a = int(self.entry_n.get())
        except ValueError:
            cantidad_columnas_a = max(
                (len(fila) - 1) if incluir_b else len(fila)
                for fila in self.matriz_entries
            )
        lineas = ["Vista previa de Ax = b:" if incluir_b else "Matriz A:"]
        for fila_entries in self.matriz_entries:
            valores_a = [
                entry.get().strip() or "_"
                for entry in fila_entries[:cantidad_columnas_a]
            ]
            fila = "[ " + "   ".join(valores_a)
            if incluir_b and len(fila_entries) > cantidad_columnas_a:
                valor_b = fila_entries[cantidad_columnas_a].get().strip() or "_"
                fila += "   |   " + valor_b
            lineas.append(fila + " ]")

        self._escribir_previsualizacion("\n".join(lineas))

    def _escribir_previsualizacion(self, texto):
        self.txt_previsualizacion.configure(state="normal")
        self.txt_previsualizacion.delete("1.0", "end")
        self.txt_previsualizacion.insert("1.0", texto)
        self.txt_previsualizacion.configure(state="disabled")

    def _formatear_valor(self, valor, formato):
        """Formatea un número a fracción o decimal sin perder ceros absolutos."""
        if formato == "fr":
            return conv.convertir_a_fraccion(valor)
        
        texto = f"{valor:.2f}".rstrip("0").rstrip(".")
        return texto if texto else "0"

    def _matriz_a_string(self, matriz, formato):
        table = PrettyTable()
        table.hrules = HRuleStyle.HEADER
        table.vrules = VRuleStyle.FRAME
        campos = [f"X{i + 1}" for i in range(len(matriz[0]) - 1)]
        campos.append("TI")
        table.field_names = campos

        for fila in matriz:
            str_fila = [self._formatear_valor(val, formato) for val in fila]
            table.add_row(str_fila)
        return str(table)

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

    def _escribir_en_visor(self, texto):
        reproducir_sonido_error(self, texto)
        self.txt_resultados.configure(state="normal")
        self.txt_resultados.delete("0.0", "end")
        self.txt_resultados.insert("0.0", texto)
        self.txt_resultados.configure(state="disabled")

    def accion_resolver(self):
        metodo_gui = self.opcion_metodo.get()
        formato = "fr" if self.opcion_numform.get() == "Fracciones" else "dc"
        formato_fracciones = formato == "fr"

        if metodo_gui == "Matriz pura (A⁻¹)":
            try:
                filas = int(self.entry_m.get())
                variables = int(self.entry_n.get())
                if filas != variables:
                    raise ValueError(
                        "El modo matriz pura requiere que A sea cuadrada (m = n)."
                    )
            except ValueError as error:
                self._escribir_en_visor(f"ERROR: {error}")
                return

        try:
            matriz_original = self.obtener_matriz_desde_gui()
        except ValueError as e:
            self._escribir_en_visor(f"ERROR DE ENTRADA:\n{str(e)}")
            return

        m = len(matriz_original)
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

        n = len(matriz_original[0]) - 1

        if metodo_gui == "Método Escalonado":
            modo = "escalonado"
        elif metodo_gui == "Gauss":
            modo = "gauss"
        else:
            modo = "gauss_jordan"

        matriz_a = [fila[:-1] for fila in matriz_original]
        vector_b = [fila[-1] for fila in matriz_original]
        resultado = enrutar_resolucion_matricial(
            matriz_a,
            vector_b=vector_b,
            formato_fracciones=formato_fracciones,
            metodo=modo
        )
        matriz_resultado = resultado["matriz_resultado"]
        pasos = resultado["pasos"]
        columnas_pivote = resultado["pivotes"]
        clasificacion = resultado["clasificacion"]

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
                x = resultado["solucion"]
                salida.append("--- Solución leída directamente de la RREF ---")
            else:
                x = resultado["solucion"]
                pasadas_despeje = resultado["pasos_despeje"]
                salida.append("--- Sustitución Hacia Atrás Paso a Paso ---")
                for paso_txt in pasadas_despeje:
                    salida.append(f"{paso_txt}\n")

            salida.append("--- Solución Única Encontrada ---")
            for i in range(n):
                val_formateado = self._formatear_valor(x[i], formato)
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