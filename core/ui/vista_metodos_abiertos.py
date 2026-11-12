"""Interfaz unificada para los métodos abiertos de Newton y Secante."""

from tkinter import TclError

from core.metodos_numericos import metodo_secante
from core.metodos_numericos import newton_raphson
from core.ui.audio_manager import reproducir_sonido_error
from core.ui.ctk_compat import ctk
from core.ui.teclado_matematico import abrir_teclado_matematico, cerrar_teclado_matematico
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_panel_contenedor,
)


class VistaMetodosAbiertos(ctk.CTkFrame):
    """Agrupa Newton-Raphson y Secante en un único panel."""

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self._rango_grafica = (-10.0, 10.0)
        self.funcion_var = ctk.StringVar(value="x³ - x - 2")
        self.metodo_var = ctk.StringVar(value="newton")
        self._ventana_grafica = None
        self._crear_interfaz()

    def _crear_interfaz(self):
        encabezado = ctk.CTkFrame(self, **estilo_panel_contenedor())
        encabezado.pack(fill="x", padx=15, pady=(12, 6))
        ctk.CTkLabel(
            encabezado,
            text="Métodos Abiertos",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(
            encabezado,
            text=(
                "Seleccione Newton-Raphson o Secante. Ambos métodos aproximan "
                "raíces usando valores iniciales y no requieren un intervalo cerrado."
            ),
            text_color=TEXTO_CLARO,
            wraplength=950,
        ).pack(anchor="w", padx=12, pady=(0, 8))

        selector_metodo = ctk.CTkFrame(self, **estilo_panel_contenedor())
        selector_metodo.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(
            selector_metodo,
            text="Método:",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left", padx=(12, 8), pady=8)
        ctk.CTkRadioButton(
            selector_metodo,
            text="Newton-Raphson",
            variable=self.metodo_var,
            value="newton",
            command=self._cambiar_metodo,
        ).pack(side="left", padx=8, pady=8)
        ctk.CTkRadioButton(
            selector_metodo,
            text="Secante",
            variable=self.metodo_var,
            value="secante",
            command=self._cambiar_metodo,
        ).pack(side="left", padx=8, pady=8)

        entradas = ctk.CTkFrame(self, **estilo_panel_contenedor())
        entradas.pack(fill="x", padx=15, pady=5)
        for columna, peso in enumerate((3, 1, 1, 1, 1)):
            entradas.grid_columnconfigure(columna, weight=peso)

        campos = (
            ("Función f(x)", "funcion", 260, None),
            ("x0", "x0", 110, "1.5"),
            ("x1", "x1", 110, "2"),
            ("Tolerancia", "tolerancia", 130, "1e-8"),
            ("Máx. iteraciones", "max_iteraciones", 120, "50"),
        )
        self.entradas = {}
        self.etiquetas_entrada = {}
        for columna, (etiqueta, clave, ancho, valor_inicial) in enumerate(campos):
            etiqueta_widget = ctk.CTkLabel(
                entradas,
                text=etiqueta,
                text_color=TEXTO_CLARO,
            )
            etiqueta_widget.grid(row=0, column=columna, padx=7, pady=(8, 3), sticky="w")
            opciones = {"width": ancho, "font": ("Consolas", 12)}
            if clave == "funcion":
                opciones["textvariable"] = self.funcion_var
            campo = ctk.CTkEntry(entradas, **opciones)
            campo.grid(row=1, column=columna, padx=7, pady=(0, 9), sticky="ew")
            if clave != "funcion":
                campo.insert(0, valor_inicial)
            self.entradas[clave] = campo
            self.etiquetas_entrada[clave] = etiqueta_widget

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        self.acciones = acciones
        acciones.pack(fill="x", padx=15, pady=4)
        ctk.CTkButton(
            acciones,
            text="Teclado f(x)",
            command=lambda: abrir_teclado_matematico(self, self.entradas["funcion"]),
            **estilo_boton_secundario(),
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            acciones,
            text="Explorar gráfica",
            command=self.abrir_grafica,
            **estilo_boton_secundario(),
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            acciones,
            text="Resolver",
            command=self.resolver,
            **estilo_boton_principal(),
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            acciones,
            text="Borrar",
            command=self.borrar,
            **estilo_boton_secundario(),
        ).pack(side="left")
        self.boton_forzar = ctk.CTkButton(
            acciones,
            text="Forzar cálculo",
            command=lambda: self.resolver(forzar=True),
            **estilo_boton_secundario(),
        )
        salida = ctk.CTkFrame(self, **estilo_panel_contenedor())
        salida.pack(fill="both", expand=True, padx=15, pady=(4, 12))
        ctk.CTkLabel(
            salida,
            text="Salida · iteraciones y criterio de paro",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=10, pady=(6, 2))
        self.texto_salida = ctk.CTkTextbox(
            salida,
            font=("Consolas", 11),
            wrap="none",
            **estilo_consola_resultado(),
        )
        self.texto_salida.pack(fill="both", expand=True, padx=8, pady=(0, 7))
        self._mostrar(
            "Newton-Raphson utiliza x0 y calcula la derivada numéricamente "
            "mediante diferencia finita central."
        )
        self._cambiar_metodo()

    def abrir_grafica(self):
        if self._ventana_grafica is not None:
            try:
                if self._ventana_grafica.winfo_exists():
                    self._ventana_grafica.lift()
                    self._ventana_grafica.focus_force()
                    return
            except TclError:
                self._ventana_grafica = None

        from core.ui.vista_grafica_biseccion import VistaGraficaBiseccion

        self._ventana_grafica = VistaGraficaBiseccion(
            self.winfo_toplevel(),
            self.funcion_var,
            on_x_selected=self._actualizar_x0_desde_grafica,
            on_range_updated=self._actualizar_rango_grafica,
            mostrar_marcas_raices=False,
            mostrar_estado_actualizacion=False,
        )

    def _actualizar_x0_desde_grafica(self, valor):
        entrada_x0 = self.entradas["x0"]
        entrada_x0.delete(0, "end")
        entrada_x0.insert(0, f"{valor:.12g}")

    def _actualizar_rango_grafica(self, rango):
        self._rango_grafica = rango

    def _cambiar_metodo(self):
        es_secante = self.metodo_var.get() == "secante"
        if es_secante:
            self.etiquetas_entrada["x1"].grid()
            self.entradas["x1"].grid()
        else:
            self.etiquetas_entrada["x1"].grid_remove()
            self.entradas["x1"].grid_remove()
            self.boton_forzar.pack_forget()
        self._mostrar(
            "Secante utiliza dos aproximaciones iniciales x0 y x1."
            if es_secante
            else (
                "Newton-Raphson utiliza x0 y calcula la derivada "
                "numéricamente mediante diferencia finita central."
            )
        )

    def resolver(self, forzar=False):
        self.boton_forzar.pack_forget()
        try:
            if self.metodo_var.get() == "secante":
                resultado = metodo_secante.resolver_secante(
                    self.funcion_var.get(),
                    self.entradas["x0"].get(),
                    self.entradas["x1"].get(),
                    self.entradas["tolerancia"].get(),
                    self.entradas["max_iteraciones"].get(),
                )
            else:
                resultado = newton_raphson.resolver_newton_raphson(
                    self.funcion_var.get(),
                    self.entradas["x0"].get(),
                    self.entradas["tolerancia"].get(),
                    self.entradas["max_iteraciones"].get(),
                    rango_analizado=self._rango_grafica,
                    forzar=forzar,
                )
        except (ValueError, ArithmeticError, OverflowError) as error:
            self._mostrar(f"ERROR: {error}")
            return

        if (
            self.metodo_var.get() == "newton"
            and resultado["detencion_preventiva"]
        ):
            x_minimo, x_maximo = resultado["rango_analizado"]
            self.boton_forzar.pack(side="left", padx=(8, 0))
            self._mostrar(
                f"{resultado['estado']} "
                f"[{x_minimo:g}, {x_maximo:g}]. "
                "El muestreo no demuestra que no existan raíces reales fuera "
                "de este rango y puede omitir raíces tangenciales o muy cercanas. "
                "Amplíe el rango en la gráfica o pulse «Forzar cálculo» para "
                "intentar Newton-Raphson con el x0 actual. Iteraciones: 0."
            )
            return

        if self.metodo_var.get() == "secante":
            self._mostrar_resultado_secante(resultado)
            return

        if resultado["procedimiento_derivada"]:
            derivada_info = [
                f"Derivada calculada: {resultado['metodo_derivada']}",
                resultado["formula_derivada"],
                (
                    "h = "
                    f"{resultado['paso_relativo_derivada']:.0e} · "
                    "max(1, |x_n|)"
                ),
                "",
                "Procedimiento de derivación en cada iteración:",
                self._formatear_procedimiento_derivada(
                    resultado["procedimiento_derivada"]
                ),
            ]
        else:
            derivada_info = [
                "Derivada calculada: no requerida; x0 ya satisface la tolerancia."
            ]
        salida = [
            *(
                [
                    "Aviso: cálculo forzado; el preanálisis no detectó raíces "
                    "candidatas en el rango visualizado."
                ]
                if resultado["forzado"]
                else []
            ),
            *derivada_info,
            "",
            f"Estado: {resultado['estado']}",
            f"Convergió: {'Sí' if resultado['convergio'] else 'No'}",
            f"Iteraciones realizadas: {resultado['iteraciones']}",
        ]
        if resultado["convergio"] and resultado["raiz"] is not None:
            salida.append(f"Raíz aproximada: {resultado['raiz']:.12g}")
        elif resultado["raiz"] is not None:
            salida.append(
                "Última aproximación (no convergida): "
                f"{resultado['raiz']:.12g}"
            )
        salida.extend(
            [
                f"Tolerancia: {resultado['tolerancia']:.6g}",
                "",
                newton_raphson.formatear_tabla(resultado),
            ]
        )
        self._mostrar("\n".join(salida))

    def _mostrar_resultado_secante(self, resultado):
        procedimiento = []
        for indice, paso in enumerate(
            resultado["procedimiento_secante"],
            start=1,
        ):
            procedimiento.extend(
                [
                    (
                        f"Iteración {indice}: x_(n-1) = "
                        f"{paso['x_anterior']:.12g}, "
                        f"x_n = {paso['x_actual']:.12g}"
                    ),
                    (
                        f"  f(x_(n-1)) = {paso['f_anterior']:.12g}, "
                        f"f(x_n) = {paso['f_actual']:.12g}"
                    ),
                    (
                        "  x_(n+1) = x_n - f(x_n)(x_n - x_(n-1)) / "
                        "(f(x_n) - f(x_(n-1)))"
                    ),
                    (
                        f"  x_(n+1) = {paso['x_actual']:.12g} - "
                        f"({paso['numerador']:.12g} / "
                        f"{paso['denominador']:.12g}) = "
                        f"{paso['x_siguiente']:.12g}"
                    ),
                    (
                        f"  |Δx| = {paso['delta_x']:.12g}; "
                        f"|f(x_(n+1))| = {paso['residuo']:.12g}"
                    ),
                ]
            )
        salida = [
            f"Estado: {resultado['estado']}",
            f"Convergió: {'Sí' if resultado['convergio'] else 'No'}",
            f"Iteraciones realizadas: {resultado['iteraciones']}",
        ]
        if resultado["convergio"] and resultado["raiz"] is not None:
            salida.append(f"Raíz aproximada: {resultado['raiz']:.12g}")
        elif resultado["raiz"] is not None:
            salida.append(
                "Última aproximación (no convergida): "
                f"{resultado['raiz']:.12g}"
            )
        salida.extend(
            [
                f"Tolerancia: {resultado['tolerancia']:.6g}",
                "",
                "Procedimiento de la secante:",
                "\n".join(procedimiento) if procedimiento else "No se requirieron iteraciones.",
                "",
                metodo_secante.formatear_tabla(resultado),
            ]
        )
        self._mostrar("\n".join(salida))

    @staticmethod
    def _formatear_procedimiento_derivada(procedimientos):
        lineas = []
        for indice, detalle in enumerate(procedimientos, start=1):
            lineas.extend(
                [
                    (
                        f"Iteración {indice}: x_n = "
                        f"{detalle['x']:.12g}"
                    ),
                    (
                        f"  h = {newton_raphson.PASO_RELATIVO_DERIVADA:.0e} "
                        f"· max(1, |{detalle['x']:.12g}|) = "
                        f"{detalle['h']:.12g}"
                    ),
                    (
                        f"  x_n + h = {detalle['x_mas_h']:.12g}; "
                        f"f(x_n + h) = {detalle['f_mas_h']:.12g}"
                    ),
                    (
                        f"  x_n - h = {detalle['x_menos_h']:.12g}; "
                        f"f(x_n - h) = {detalle['f_menos_h']:.12g}"
                    ),
                    (
                        "  f'(x_n) ≈ "
                        f"({detalle['f_mas_h']:.12g} - "
                        f"({detalle['f_menos_h']:.12g})) / "
                        f"(2 · {detalle['h']:.12g})"
                    ),
                    (
                        f"  f'(x_n) ≈ {detalle['diferencia_funcion']:.12g} / "
                        f"{detalle['divisor']:.12g} = "
                        f"{detalle['derivada']:.12g}"
                    ),
                ]
            )
        return "\n".join(lineas)

    def borrar(self):
        for clave in ("x0", "x1", "tolerancia", "max_iteraciones"):
            self.entradas[clave].delete(0, "end")
        self.funcion_var.set("x³ - x - 2")
        self.entradas["x0"].insert(0, "1.5")
        self.entradas["x1"].insert(0, "2")
        self.entradas["tolerancia"].insert(0, "1e-8")
        self.entradas["max_iteraciones"].insert(0, "50")
        self._mostrar("Campos reiniciados con el caso guía de Newton-Raphson.")

    def al_ocultar(self):
        cerrar_teclado_matematico(self)
        if self._ventana_grafica is not None:
            try:
                if self._ventana_grafica.winfo_exists():
                    self._ventana_grafica.al_cerrar()
            except TclError:
                pass
            self._ventana_grafica = None

    def _mostrar(self, texto):
        if texto.startswith("ERROR:"):
            reproducir_sonido_error(self, texto)
        self.texto_salida.delete("1.0", "end")
        self.texto_salida.insert("1.0", texto)
