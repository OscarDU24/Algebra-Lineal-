"""Interfaz de HeyAlgb para determinantes y sistemas resueltos mediante LU."""

from core.ui.ctk_compat import ctk
from core.ui.audio_manager import reproducir_sonido_error
from core.determinantes import operaciones_determinantes as op_det
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_menu_desplegable,
    estilo_panel_contenedor,
)


class VistaDeterminantes(ctk.CTkToplevel):
    """Ventana secundaria para determinantes y resolución de Ax=b mediante LU."""

    def __init__(self, master):
        super().__init__(master)
        self.master_dashboard = master
        self.master_dashboard.withdraw()
        self.configure(fg_color=FONDO_CALCULADORA)
        self.title("Determinantes y Factorización LU")
        self.geometry("1080x800")
        self.minsize(820, 650)
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self.entradas_matriz = []
        self.entradas_b = []
        self.crear_interfaz()
        self.generar_matriz()

    def al_cerrar(self):
        if self.master_dashboard is not None:
            self.master_dashboard.deiconify()
        self.destroy()

    def crear_interfaz(self):
        encabezado = ctk.CTkFrame(self, **estilo_panel_contenedor())
        encabezado.pack(fill="x", padx=15, pady=(15, 8))
        ctk.CTkLabel(
            encabezado,
            text="Calculadora de Determinantes",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 22, "bold"),
        ).pack(side="left", padx=12, pady=10)
        ctk.CTkLabel(
            encabezado,
            text="Aritmética racional · Cofactores · LU",
            text_color=TEXTO_CLARO,
            font=("Consolas", 12),
        ).pack(side="right", padx=12)

        controles = ctk.CTkFrame(self, **estilo_panel_contenedor())
        controles.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(controles, text="Orden n:", text_color=TEXTO_CLARO).pack(
            side="left", padx=(10, 4)
        )
        self.entrada_orden = ctk.CTkEntry(controles, width=65, justify="center")
        self.entrada_orden.insert(0, "3")
        self.entrada_orden.pack(side="left", padx=4, pady=8)
        ctk.CTkButton(
            controles,
            text="Generar matriz",
            **estilo_boton_secundario(),
            command=self.generar_matriz,
        ).pack(side="left", padx=7)
        ctk.CTkButton(
            controles,
            text="Limpiar valores",
            **estilo_boton_secundario(),
            command=self.limpiar,
        ).pack(side="left", padx=4)
        self.menu_formato = ctk.CTkComboBox(
            controles,
            values=["Fracciones", "Decimales"],
            width=140,
            **estilo_menu_desplegable(),
        )
        self.menu_formato.set("Fracciones")
        self.menu_formato.pack(side="right", padx=10)

        self.area_datos = ctk.CTkScrollableFrame(
            self,
            label_text="Matriz de coeficientes A y vector b",
            **estilo_panel_contenedor(),
        )
        self.area_datos.pack(fill="both", expand=True, padx=15, pady=6)

        self.panel_eficiencia = ctk.CTkFrame(self, **estilo_panel_contenedor())
        self.panel_eficiencia.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(
            self.panel_eficiencia,
            text="Evaluación previa de eficiencia",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=10, pady=(6, 0))
        self.texto_eficiencia = ctk.CTkTextbox(
            self.panel_eficiencia,
            height=82,
            font=("Consolas", 12),
            **estilo_consola_resultado(),
        )
        self.texto_eficiencia.pack(fill="x", padx=8, pady=6)

        self.panel_resultado = ctk.CTkFrame(self, **estilo_panel_contenedor())
        self.panel_resultado.pack(fill="both", padx=15, pady=(6, 14))
        ctk.CTkLabel(
            self.panel_resultado,
            text="Operación y procedimiento",
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=10, pady=(7, 0))
        acciones = ctk.CTkFrame(self.panel_resultado, fg_color="transparent")
        acciones.pack(fill="x", padx=8, pady=6)
        self.menu_operacion = ctk.CTkComboBox(
            acciones,
            values=[
                "Determinante",
                "Resolver sistema (LU)",
                "Resolver sistema (Cramer)",
            ],
            width=190,
            command=self.cambiar_operacion,
            **estilo_menu_desplegable(),
        )
        self.menu_operacion.set("Determinante")
        self.menu_operacion.pack(side="left", padx=(0, 8))
        self.menu_metodo = ctk.CTkComboBox(
            acciones,
            values=["Automático", "Cofactores", "LU / Triangulación"],
            width=190,
            **estilo_menu_desplegable(),
        )
        self.menu_metodo.set("Automático")
        self.menu_metodo.pack(side="left", padx=(0, 8))
        self.btn_calcular = ctk.CTkButton(
            acciones,
            text="Calcular",
            **estilo_boton_principal(),
            command=self.calcular,
        )
        self.btn_calcular.pack(side="left")
        self.texto_resultado = ctk.CTkTextbox(
            self.panel_resultado,
            height=210,
            font=("Consolas", 12),
            **estilo_consola_resultado(),
        )
        self.texto_resultado.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.mostrar_resultado("Genere la matriz, ingrese sus valores y presione «Calcular».")

    def generar_matriz(self):
        try:
            orden = int(self.entrada_orden.get().strip())
            if orden <= 0:
                raise ValueError
        except ValueError:
            self.mostrar_resultado("ERROR: el orden debe ser un entero positivo.")
            return

        for widget in self.area_datos.winfo_children():
            widget.destroy()
        self.entradas_matriz = []
        self.entradas_b = []

        self.frame_matriz = ctk.CTkFrame(self.area_datos, fg_color="transparent")
        self.frame_matriz.pack(anchor="n", pady=(8, 12))
        ctk.CTkLabel(
            self.frame_matriz, text="Matriz A", text_color=TEXTO_CLARO
        ).grid(row=0, column=0, columnspan=orden, pady=(0, 5))
        for fila in range(orden):
            entradas_fila = []
            for columna in range(orden):
                entrada = ctk.CTkEntry(
                    self.frame_matriz, width=72, justify="center"
                )
                entrada.grid(row=fila + 1, column=columna, padx=3, pady=3)
                entrada.bind("<KeyRelease>", self.actualizar_eficiencia)
                entradas_fila.append(entrada)
            self.entradas_matriz.append(entradas_fila)

        self.frame_vector = ctk.CTkFrame(self.area_datos, fg_color="transparent")
        self.frame_vector.pack(anchor="n", pady=(0, 8))
        ctk.CTkLabel(
            self.frame_vector,
            text="Vector b (para resolver Ax = b)",
            text_color=TEXTO_CLARO,
        ).grid(row=0, column=0, columnspan=orden, pady=(0, 5))
        for columna in range(orden):
            entrada = ctk.CTkEntry(self.frame_vector, width=72, justify="center")
            entrada.grid(row=1, column=columna, padx=3, pady=3)
            self.entradas_b.append(entrada)

        self.actualizar_vector_visible()
        self.actualizar_eficiencia()
        self.mostrar_resultado("Ingrese los valores de A y elija la operación.")

    def actualizar_vector_visible(self):
        if self.menu_operacion.get() != "Determinante":
            self.frame_vector.pack(anchor="n", pady=(0, 8))
        else:
            self.frame_vector.pack_forget()

    def cambiar_operacion(self, valor=None):
        operacion = valor or self.menu_operacion.get()
        if operacion == "Determinante":
            self.menu_metodo.pack(
                side="left", padx=(0, 8), before=self.btn_calcular
            )
        else:
            self.menu_metodo.pack_forget()
        self.actualizar_vector_visible()

    def _leer_matriz(self):
        if not self.entradas_matriz:
            raise ValueError("Primero genere la matriz.")
        matriz = []
        for indice_fila, entradas in enumerate(self.entradas_matriz):
            fila = []
            for indice_columna, entrada in enumerate(entradas):
                texto = entrada.get().strip()
                if not texto:
                    raise ValueError(
                        f"La celda A[{indice_fila + 1},{indice_columna + 1}] está vacía."
                    )
                try:
                    fila.append(op_det.convertir_entrada(texto))
                except ValueError as error:
                    raise ValueError(
                        f"A[{indice_fila + 1},{indice_columna + 1}]: {error}"
                    ) from error
            matriz.append(fila)
        return matriz

    def _leer_vector_b(self):
        vector = []
        for indice, entrada in enumerate(self.entradas_b):
            texto = entrada.get().strip()
            if not texto:
                raise ValueError(f"La componente b{indice + 1} está vacía.")
            try:
                vector.append(op_det.convertir_entrada(texto))
            except ValueError as error:
                raise ValueError(f"b{indice + 1}: {error}") from error
        return vector

    def actualizar_eficiencia(self, _evento=None):
        try:
            matriz = self._leer_matriz()
        except ValueError:
            self._escribir_eficiencia(
                "Complete la matriz cuadrada con valores numéricos para ver la "
                "recomendación antes de calcular."
            )
            return
        analisis, metodo = op_det.analizar_eficiencia_determinante(matriz)
        self._escribir_eficiencia(f"{analisis}\nMétodo sugerido: {metodo}")

    def calcular(self):
        try:
            matriz = self._leer_matriz()
            formato = self.menu_formato.get()
            operacion = self.menu_operacion.get()
            if operacion == "Resolver sistema (LU)":
                texto = op_det.resolver_sistema_lu_a_string(
                    matriz, self._leer_vector_b(), formato
                )
            elif operacion == "Resolver sistema (Cramer)":
                texto = op_det.resolver_sistema_cramer_a_string(
                    matriz, self._leer_vector_b(), formato
                )
            else:
                metodo = self.menu_metodo.get()
                if metodo == "Automático":
                    metodo = (
                        "Automático directo"
                        if len(matriz) <= 3
                        else "LU / Triangulación"
                    )
                if metodo == "Cofactores":
                    texto = op_det.determinante_cofactores_a_string(matriz, formato)
                elif metodo == "LU / Triangulación":
                    texto = op_det.determinante_lu_a_string(matriz, formato)
                else:
                    texto = op_det.determinante_directo_a_string(matriz, formato)
            self.mostrar_resultado(texto)
        except ValueError as error:
            self.mostrar_resultado(f"ERROR: {error}")

    def limpiar(self):
        for entradas in self.entradas_matriz:
            for entrada in entradas:
                entrada.delete(0, "end")
        for entrada in self.entradas_b:
            entrada.delete(0, "end")
        self.actualizar_eficiencia()
        self.mostrar_resultado("Campos limpios.")

    def _escribir_eficiencia(self, texto):
        self.texto_eficiencia.configure(state="normal")
        self.texto_eficiencia.delete("1.0", "end")
        self.texto_eficiencia.insert("1.0", texto)
        self.texto_eficiencia.configure(state="disabled")

    def mostrar_resultado(self, texto):
        reproducir_sonido_error(self, texto)
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)
