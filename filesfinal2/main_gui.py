import customtkinter as ctk
from lineal import conversiones as conv
from prettytable import PrettyTable, HRuleStyle, VRuleStyle

# Importación de la lógica matemática del paquete lineal
from lineal import (
    eliminacion_por_filas,
    clasificar_sistema,
    sustitucion_hacia_atras_detallada,
    extraer_solucion_rref,
    verificar_solucion,
    imprimir_sistema_ecuaciones,
)


# Configuración inicial del tema visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AppCalculadora(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Calculadora de Sistemas de Ecuaciones Lineales - FIA UAM")
        self.geometry("980x780")

        # Almacenamiento bidimensional para los widgets CTkEntry
        self.matriz_entries = []

        # Estructura de la interfaz
        self.crear_frame_superior()
        self.crear_frame_central()
        self.crear_frame_inferior()

        # Generar cuadrícula inicial 3x3
        self.generar_cuadricula_matriz()


    def crear_frame_superior(self):
        """
        Frame de controles iniciales:
        dimensiones, generación y reinicio.
        """

        self.frame_sup = ctk.CTkFrame(self)
        self.frame_sup.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # Título
        lbl_titulo = ctk.CTkLabel(
            self.frame_sup,
            text="Dimensiones:",
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

        # Filas
        lbl_m = ctk.CTkLabel(
            self.frame_sup,
            text="Filas (m):"
        )

        lbl_m.pack(
            side="left",
            padx=(10, 2)
        )

        self.entry_m = ctk.CTkEntry(
            self.frame_sup,
            width=50
        )

        self.entry_m.insert(0, "3")

        self.entry_m.pack(
            side="left",
            padx=5
        )

        # Variables
        lbl_n = ctk.CTkLabel(
            self.frame_sup,
            text="Variables (n):"
        )

        lbl_n.pack(
            side="left",
            padx=(10, 2)
        )

        self.entry_n = ctk.CTkEntry(
            self.frame_sup,
            width=50
        )

        self.entry_n.insert(0, "3")

        self.entry_n.pack(
            side="left",
            padx=5
        )

        # Botón generar
        btn_generar = ctk.CTkButton(
            self.frame_sup,
            text="Generar Matriz",
            command=self.generar_cuadricula_matriz
        )

        btn_generar.pack(
            side="left",
            padx=15
        )

        # Botón limpiar
        btn_limpiar = ctk.CTkButton(
            self.frame_sup,
            text="Limpiar Valores",
            fg_color="#555555",
            hover_color="#333333",
            command=self.limpiar_entradas
        )

        btn_limpiar.pack(
            side="left",
            padx=5
        )


    def crear_frame_central(self):
        """
        Frame dinámico con barra de desplazamiento
        para la matriz aumentada.
        """

        self.frame_centro = ctk.CTkScrollableFrame(
            self,
            label_text="Matriz Aumentada [A | b]"
        )

        self.frame_centro.pack(
            pady=10,
            padx=20,
            fill="both",
            expand=True
        )


    def crear_frame_inferior(self):
        """
        Frame de controles de cálculo y visor de resultados.
        """

        self.frame_inf = ctk.CTkFrame(self)

        self.frame_inf.pack(
            pady=10,
            padx=20,
            fill="both",
            expand=True
        )

        # Contenedor horizontal para menú y botón resolver
        subframe_acciones = ctk.CTkFrame(
            self.frame_inf,
            fg_color="transparent"
        )

        subframe_acciones.pack(
            fill="x",
            pady=5,
            padx=10
        )

        # ---------------------------------------------------------
        # SELECCIÓN DEL MÉTODO
        # ---------------------------------------------------------

        self.opcion_metodo = ctk.CTkOptionMenu(
            subframe_acciones,
            values=[
                "Método Escalonado",
                "Gauss",
                "Gauss-Jordan"
            ]
        )

        self.opcion_metodo.pack(
            side="left",
            padx=(0, 10)
        )

        # ---------------------------------------------------------
        # FORMATO DE NÚMEROS
        # ---------------------------------------------------------

        self.opcion_numform = ctk.CTkOptionMenu(
            subframe_acciones,
            values=[
                "Fracciones",
                "Decimales"
            ]
        )

        self.opcion_numform.pack(
            side="left",
            padx=(0, 10)
        )

        # ---------------------------------------------------------
        # BOTÓN RESOLVER
        # ---------------------------------------------------------

        btn_resolver = ctk.CTkButton(
            subframe_acciones,
            text="Resolver Sistema",
            fg_color="green",
            hover_color="darkgreen",
            font=ctk.CTkFont(
                weight="bold"
            ),
            command=self.accion_resolver
        )

        btn_resolver.pack(
            side="left"
        )

        # ---------------------------------------------------------
        # VISOR DE RESULTADOS
        # ---------------------------------------------------------

        self.txt_resultados = ctk.CTkTextbox(
            self.frame_inf,
            font=("Courier New", 12)
        )

        self.txt_resultados.pack(
            pady=10,
            padx=10,
            fill="both",
            expand=True
        )

        self._escribir_en_visor(
            "Ingrese los coeficientes en la matriz "
            "y presione 'Resolver Sistema'..."
        )


    def generar_cuadricula_matriz(self):
        """
        Dibuja dinámicamente las casillas para la matriz.
        """

        for widget in self.frame_centro.winfo_children():
            widget.destroy()

        self.matriz_entries.clear()

        try:

            m = int(self.entry_m.get())
            n = int(self.entry_n.get())

            if m <= 0 or n <= 0:
                raise ValueError

        except ValueError:

            self._escribir_en_visor(
                "ERROR: Ingrese números enteros positivos válidos "
                "para m y n."
            )

            return

        # Crear matriz aumentada
        for i in range(m):

            fila_entries = []

            for j in range(n + 1):

                entry = ctk.CTkEntry(
                    self.frame_centro,
                    width=65,
                    justify="center"
                )

                entry.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                # Última columna = términos independientes
                if j == n:

                    entry.configure(
                        fg_color="#2b2b2b",
                        border_color="#1f538d"
                    )

                fila_entries.append(entry)

            self.matriz_entries.append(
                fila_entries
            )


    def limpiar_entradas(self):
        """
        Limpia las casillas de la matriz
        y el visor de resultados.
        """

        for fila in self.matriz_entries:

            for entry in fila:

                entry.delete(
                    0,
                    "end"
                )

        self._escribir_en_visor(
            "Campos limpios. Ingrese un nuevo sistema."
        )


    def obtener_matriz_desde_gui(self):
        """
        Extrae los datos numéricos desde los widgets CTkEntry.
        """

        matriz = []

        for i, fila_entries in enumerate(
            self.matriz_entries
        ):

            fila_vals = []

            for j, entry in enumerate(
                fila_entries
            ):

                val_str = entry.get().strip()

                if not val_str:

                    raise ValueError(
                        f"La casilla en la fila {i + 1}, "
                        f"columna {j + 1} está vacía."
                    )

                try:

                    val_num = conv.convertir_a_decimal(
                        val_str
                    )

                    fila_vals.append(
                        val_num
                    )

                except ValueError:

                    raise ValueError(
                        f"El valor '{val_str}' en la fila "
                        f"{i + 1}, columna {j + 1} "
                        f"no es válido."
                    )

            matriz.append(
                fila_vals
            )

        return matriz


    def _matriz_a_string(self, matriz, formato):
        """
        Convierte una matriz en un bloque de texto
        alineado con PrettyTable.
        """

        table = PrettyTable()

        table.hrules = HRuleStyle.HEADER
        table.vrules = VRuleStyle.FRAME

        campos = []

        for i in range(
            len(matriz[0]) - 1
        ):

            campos.append(
                f"X{i + 1}"
            )

        campos.append("TI")

        table.field_names = campos

        for fila in matriz:

            str_fila = []

            for j in range(
                len(matriz[0]) - 1
            ):

                if formato == "fr":

                    str_fila.append(
                        conv.convertir_a_fraccion(
                            fila[j]
                        )
                    )

                else:

                    str_fila.append(
                        f"{fila[j]:0.4f}"
                        .rstrip("0")
                        .rstrip(".")
                    )

            if formato == "fr":

                str_fila.append(
                    conv.convertir_a_fraccion(
                        fila[-1]
                    )
                )

            else:

                str_fila.append(
                    f"{fila[-1]:0.4f}"
                    .rstrip("0")
                    .rstrip(".")
                )

            table.add_row(
                str_fila
            )

        return str(table)


    def _escribir_en_visor(self, texto):
        """
        Escribe en el CTkTextbox de forma segura
        manteniendo el estado bloqueado.
        """

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


    def accion_resolver(self):
        """
        Orquesta el cálculo completo e inyecta
        la salida detallada.
        """

        # ---------------------------------------------------------
        # OBTENER MATRIZ
        # ---------------------------------------------------------

        try:

            matriz_original = (
                self.obtener_matriz_desde_gui()
            )

        except ValueError as e:

            self._escribir_en_visor(
                f"ERROR DE ENTRADA:\n{str(e)}"
            )

            return

        m = len(
            matriz_original
        )

        n = len(
            matriz_original[0]
        ) - 1

        # ---------------------------------------------------------
        # OBTENER MÉTODO SELECCIONADO
        # ---------------------------------------------------------

        metodo_gui = self.opcion_metodo.get()

        if metodo_gui == "Método Escalonado":

            modo = "escalonado"

        elif metodo_gui == "Gauss":

            modo = "gauss"

        else:

            modo = "gauss_jordan"

        # ---------------------------------------------------------
        # OBTENER FORMATO
        # ---------------------------------------------------------

        formato_gui = self.opcion_numform.get()

        if formato_gui == "Fracciones":

            formato = "fr"

        else:

            formato = "dc"

        # ---------------------------------------------------------
        # EJECUTAR MÉTODO DE ELIMINACIÓN
        # ---------------------------------------------------------

        (
            matriz_resultado,
            pasos,
            columnas_pivote
        ) = eliminacion_por_filas(
            matriz_original,
            modo
        )

        # ---------------------------------------------------------
        # CONSTRUIR SALIDA
        # ---------------------------------------------------------

        salida = []

        salida.append(
            "========================================================="
        )

        salida.append(
            f"   PROCESO DE ELIMINACIÓN POR FILAS "
            f"({metodo_gui.upper()})"
        )

        salida.append(
            "=========================================================\n"
        )

        # Mostrar pasos
        for descripcion, matriz_paso in pasos[1:]:

            salida.append(
                f">> {descripcion}:"
            )

            salida.append(
                self._matriz_a_string(
                    matriz_paso,
                    formato
                )
            )

            salida.append("")

        # ---------------------------------------------------------
        # MOSTRAR RESULTADO SEGÚN EL MÉTODO
        # ---------------------------------------------------------

        if modo == "escalonado":

            salida.append(
                "========================================================="
            )

            salida.append(
                "   MATRIZ EN FORMA ESCALONADA"
            )

            salida.append(
                "========================================================="
            )

            salida.append(
                self._matriz_a_string(
                    matriz_resultado,
                    formato
                )
            )

            salida.append("")


        elif modo == "gauss":

            salida.append(
                "========================================================="
            )

            salida.append(
                "   SISTEMA DE ECUACIONES EQUIVALENTE (GAUSS)"
            )

            salida.append(
                "========================================================="
            )

            salida.append(
                imprimir_sistema_ecuaciones(
                    matriz_resultado
                )
            )

            salida.append("")


        elif modo == "gauss_jordan":

            salida.append(
                "========================================================="
            )

            salida.append(
                "   MATRIZ EN FORMA ESCALONADA REDUCIDA"
            )

            salida.append(
                "========================================================="
            )

            salida.append(
                self._matriz_a_string(
                    matriz_resultado,
                    formato
                )
            )

            salida.append("")


        # ---------------------------------------------------------
        # CLASIFICACIÓN DEL SISTEMA
        # ---------------------------------------------------------

        clasificacion = clasificar_sistema(
            matriz_resultado,
            columnas_pivote
        )

        salida.append(
            "========================================================="
        )

        salida.append(
            "   ANÁLISIS DE PIVOTES Y CLASIFICACIÓN DEL SISTEMA"
        )

        salida.append(
            "========================================================="
        )

        # Identificación de columnas pivote
        cols_pivote_str = ", ".join(
            [
                f"x{c + 1} (Columna {c + 1})"
                for c in columnas_pivote
            ]
        )

        salida.append(
            f"• Columnas Pivote: "
            f"{cols_pivote_str if cols_pivote_str else 'Ninguna'}"
        )

        # Identificación de variables libres
        todas_las_vars = set(
            range(n)
        )

        vars_libres = (
            todas_las_vars
            - set(columnas_pivote)
        )

        if vars_libres:

            libres_str = ", ".join(
                [
                    f"x{c + 1}"
                    for c in sorted(vars_libres)
                ]
            )

            salida.append(
                f"• Variables Libres: Sí ({libres_str})"
            )

        else:

            salida.append(
                "• Variables Libres: No"
            )

        salida.append(
            f"• Clasificación: "
            f"{clasificacion.upper()}\n"
        )

        # ---------------------------------------------------------
        # SISTEMA CONSISTENTE DETERMINADO
        # ---------------------------------------------------------

        if (
            clasificacion
            == "Sistema Consistente Determinado"
        ):

            if modo == "gauss_jordan":

                x = extraer_solucion_rref(
                    matriz_resultado,
                    n
                )

                salida.append(
                    "--- Solución leída directamente "
                    "de la RREF ---"
                )

            else:

                x, pasadas_despeje = (
                    sustitucion_hacia_atras_detallada(
                        matriz_resultado,
                        n
                    )
                )

                salida.append(
                    "--- Sustitución Hacia Atrás "
                    "Paso a Paso ---"
                )

                for paso_txt in pasadas_despeje:

                    salida.append(
                        f"{paso_txt}\n"
                    )

            salida.append(
                "--- Solución Única Encontrada ---"
            )

            for i in range(n):

                if formato == "fr":

                    val_formateado = (
                        conv.convertir_a_fraccion(
                            x[i]
                        )
                    )

                else:

                    val_formateado = (
                        f"{x[i]:.6f}"
                    )

                salida.append(
                    f"  x{i + 1} = {val_formateado}"
                )

            # Verificación
            es_correcta = verificar_solucion(
                matriz_original,
                x
            )

            salida.append(
                "\n--- Verificación en el sistema original ---"
            )

            if es_correcta:

                salida.append(
                    "Comprobación exitosa: "
                    "La solución satisface todas las ecuaciones."
                )

            else:

                salida.append(
                    "Advertencia: La solución "
                    "no pudo ser verificada correctamente."
                )

        # ---------------------------------------------------------
        # SISTEMA CONSISTENTE INDETERMINADO
        # ---------------------------------------------------------

        elif (
            clasificacion
            == "Sistema Consistente Indeterminado"
        ):

            salida.append(
                "--- Solución General "
                "(Infinitas Soluciones) ---"
            )

            salida.append(
                "El sistema posee infinitas soluciones "
                "en función de las variables libres."
            )

            salida.append(
                "Variables dependientes "
                f"(con pivote): "
                f"{[f'x{c + 1}' for c in columnas_pivote]}"
            )

            salida.append(
                "Variables libres: "
                f"{[f'x{c + 1}' for c in sorted(vars_libres)]}"
            )

        # ---------------------------------------------------------
        # SISTEMA INCONSISTENTE
        # ---------------------------------------------------------

        else:

            salida.append(
                "--- Sistema Inconsistente ---"
            )

            salida.append(
                "El sistema no tiene solución."
            )

            salida.append(
                "Se detectó una contradicción "
                "del tipo 0 = k "
                "(con k distinto de 0)."
            )

        # Mostrar resultado final
        self._escribir_en_visor(
            "\n".join(salida)
        )


if __name__ == "__main__":

    app = AppCalculadora()

    app.mainloop()
