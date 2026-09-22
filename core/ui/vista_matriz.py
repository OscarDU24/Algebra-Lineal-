from core.ui.ctk_compat import ctk
from prettytable import PrettyTable, HRuleStyle, VRuleStyle

from core.lineal import conversiones as conv
from core.lineal.eliminacion import eliminacion_por_filas
from core.lineal.clasificacion import clasificar_sistema
from core.lineal.solucion import sustitucion_hacia_atras_detallada, extraer_solucion_rref
from core.lineal.verificacion import verificar_solucion
from core.lineal.visualizacion import imprimir_sistema_ecuaciones
from core.ui.tema import (
    FONDO_BOTON,
    FONDO_CALCULADORA,
    FONDO_TERMINAL,
    FONDO_TERMINO_INDEPENDIENTE,
    FUENTE_CONTROLES,
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

        lbl_n = ctk.CTkLabel(self.frame_sup, text="Variables (n):", text_color="#ffffff")
        lbl_n.pack(side="left", padx=(10, 2))

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

        self.opcion_metodo = ctk.CTkComboBox(subframe_acciones, values=["Método Escalonado", "Gauss", "Gauss-Jordan"], **estilo_menu_desplegable())
        self.opcion_metodo.set("Método Escalonado")
        self.opcion_metodo.pack(side="left", padx=(0, 10))

        self.opcion_numform = ctk.CTkComboBox(subframe_acciones, values=["Fracciones", "Decimales"], **estilo_menu_desplegable())
        self.opcion_numform.set("Fracciones")
        self.opcion_numform.pack(side="left", padx=(0, 10))

        btn_resolver = ctk.CTkButton(subframe_acciones, text="Resolver Sistema", **estilo_boton_principal(), command=self.accion_resolver)
        btn_resolver.pack(side="left")

        self.txt_resultados = ctk.CTkTextbox(self.frame_inf, font=("Courier New", 12), **estilo_consola_resultado())
        self.txt_resultados.pack(pady=10, padx=10, fill="both", expand=True)
        self._escribir_en_visor("Ingrese los coeficientes en la matriz y presione 'Resolver Sistema'...")

    def generar_cuadricula_matriz(self):
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
                entry.bind(
                    "<KeyRelease>",
                    lambda event: self.actualizar_previsualizacion()
                )
                if j == n:
                    entry.configure(
                        fg_color=FONDO_TERMINO_INDEPENDIENTE,
                        border_color="#ffffff"
                    )
                fila_entries.append(entry)
            self.matriz_entries.append(fila_entries)

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
                    fila_vals.append(val_num)
                except ValueError:
                    raise ValueError(f"El valor '{val_str}' en la fila {i + 1}, columna {j + 1} no es válido.")
            matriz.append(fila_vals)
        return matriz

    def actualizar_previsualizacion(self):
        """Muestra la matriz escrita antes de seleccionar un método."""
        if not self.matriz_entries:
            return

        filas = []
        for fila_entries in self.matriz_entries:
            valores = []
            for entry in fila_entries:
                texto = entry.get().strip()
                valores.append(texto if texto else "_")
            filas.append("[ " + "   ".join(valores) + " ]")

        self._escribir_previsualizacion("\n".join(filas))

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

    def _escribir_en_visor(self, texto):
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