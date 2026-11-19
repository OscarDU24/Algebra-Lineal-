"""Interfaz para aplicar el método Regula Falsi."""

from tkinter import TclError

from core.metodos_numericos import regla_falsa
from core.ui.audio_manager import reproducir_sonido_error
from core.ui.zoom_resultados import crear_consola_resultados, escribir_consola
from core.ui.navegacion import (
    confirmar_reemplazo,
    escribir_campo,
    instalar_navegacion,
    marcar_error_campo,
    rellenar,
)
from core.ui.ctk_compat import ctk
from core.ui.teclado_matematico import (
    abrir_teclado_matematico,
    cerrar_teclado_matematico,
)
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_panel_contenedor,
)


class VistaReglaFalsa(ctk.CTkFrame):
    """Calcula una raíz con extremos y tolerancia ingresados manualmente."""

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self._reporte_academico = None
        self.funcion_var = ctk.StringVar(value="e⁻ᵡ - x")
        self._ventana_grafica = None
        self._crear_interfaz()

    def _crear_interfaz(self):
        encabezado = ctk.CTkFrame(self, **estilo_panel_contenedor())
        encabezado.pack(fill="x", padx=15, pady=(12, 6))
        ctk.CTkLabel(
            encabezado,
            text="Método Regula Falsi",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(
            encabezado,
            text=(
                "Use un intervalo con cambio de signo. La tolerancia se "
                "compara con el error relativo aproximado Ea, en porcentaje."
            ),
            text_color=TEXTO_CLARO,
            wraplength=950,
        ).pack(anchor="w", padx=12, pady=(0, 8))

        entradas = ctk.CTkFrame(self, **estilo_panel_contenedor())
        entradas.pack(fill="x", padx=15, pady=5)
        for columna, peso in enumerate((3, 1, 1, 2, 1)):
            entradas.grid_columnconfigure(columna, weight=peso)
        campos = (
            ("Función f(x)", "funcion", 300, None),
            ("Valor de a", "a", 115, "0"),
            ("Valor de b", "b", 115, "1"),
            ("Tolerancia Ea (%)", "tolerancia", 150, "0.00001"),
            ("Máx. iteraciones", "max_iteraciones", 125, "100"),
        )
        self.entradas = {}
        for columna, (etiqueta, clave, ancho, valor_inicial) in enumerate(campos):
            ctk.CTkLabel(
                entradas,
                text=etiqueta,
                text_color=TEXTO_CLARO,
            ).grid(row=0, column=columna, padx=7, pady=(8, 3), sticky="w")
            opciones = {"width": ancho, "font": ("Consolas", 12)}
            if clave == "funcion":
                opciones["textvariable"] = self.funcion_var
            campo = ctk.CTkEntry(entradas, **opciones)
            campo.grid(
                row=1, column=columna, padx=7, pady=(0, 9), sticky="ew"
            )
            if valor_inicial is not None:
                campo.insert(0, valor_inicial)
            self.entradas[clave] = campo

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.pack(fill="x", padx=15, pady=4)
        ctk.CTkButton(
            acciones,
            text="Teclado matemático",
            command=lambda: abrir_teclado_matematico(
                self, self.entradas["funcion"]
            ),
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
            text="Limpiar entradas",
            command=self.borrar,
            **estilo_boton_secundario(),
        ).pack(side="left")

        salida = ctk.CTkFrame(self, **estilo_panel_contenedor())
        salida.pack(fill="both", expand=True, padx=15, pady=(4, 12))
        ctk.CTkLabel(
            salida,
            text="Salida · iteraciones y estado de convergencia",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=10, pady=(6, 2))
        contenedor_salida, self.texto_salida, self.zoom_salida = (
            crear_consola_resultados(
                salida,
                tamano=11,
                formateador_copia=self._formatear_reporte_copiado,
            )
        )
        contenedor_salida.pack(fill="both", expand=True, padx=8, pady=(0, 7))
        self._mostrar(
            "Ingrese f(x), los extremos a y b, la tolerancia porcentual de Ea "
            "y el máximo de iteraciones. Use «Explorar gráfica» para orientar "
            "la elección manual del intervalo."
        )

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
        )

    def resolver(self):
        try:
            resultado = regla_falsa.resolver_regla_falsa(
                self.funcion_var.get(),
                self.entradas["a"].get(),
                self.entradas["b"].get(),
                self.entradas["tolerancia"].get(),
                self.entradas["max_iteraciones"].get(),
            )
        except (ValueError, ArithmeticError, OverflowError) as error:
            self._mostrar(f"ERROR: {error}")
            return

        formula = (
            "c = a - f(a)·(b - a) / (f(b) - f(a)); "
            "conservar el subintervalo con cambio de signo."
        )
        if resultado["estado"] == "Raíz exacta encontrada":
            criterio_visible = "Raíz exacta: f(c) = 0."
        elif resultado["convergio"]:
            criterio_visible = (
                "Error relativo aproximado porcentual Ea ≤ tolerancia Ea "
                f"({resultado['tolerancia_porcentual']:.10g} %)."
            )
        else:
            criterio_visible = (
                "No se alcanzó la tolerancia; detenido por: "
                f"{resultado['estado']}."
            )
        aproximacion = (
            resultado["raiz"]
            if resultado["convergio"]
            else resultado["aproximacion"]
        )
        residuo = (
            None
            if resultado["f_aproximacion"] is None
            else abs(resultado["f_aproximacion"])
        )
        tabla = regla_falsa.formatear_tabla(resultado)
        salida = [
            f"Estado: {resultado['estado']}",
            f"Convergió: {'Sí' if resultado['convergio'] else 'No'}",
            f"Iteraciones realizadas: {resultado['iteraciones']}",
        ]
        if resultado["convergio"]:
            salida.append(f"Raíz aproximada: {resultado['raiz']:.12g}")
        elif resultado["aproximacion"] is not None:
            salida.append(
                "Última aproximación (no convergida): "
                f"{resultado['aproximacion']:.12g}"
            )
        if resultado["f_aproximacion"] is not None:
            salida.append(
                f"|f(aproximación)| (residuo): {residuo:.10e}"
            )
        salida.extend(
            [
                f"Fórmula iterativa: {formula}",
                f"Criterio de parada: {criterio_visible}",
                f"Tolerancia Ea: {resultado['tolerancia_porcentual']:.10g}%",
                "",
                tabla,
            ]
        )
        residuo_texto = (
            "No disponible" if residuo is None else f"{residuo:.10e}"
        )
        aproximacion_texto = (
            "No determinada" if aproximacion is None else f"{aproximacion:.12g}"
        )
        reporte = "\n".join(
            [
                "Método seleccionado: Regula Falsi",
                "Justificación de elección e intervalo/valores iniciales: "
                "[Completar por el estudiante]",
                (
                    "Datos iniciales: "
                    f"f(x) = {self.funcion_var.get()}; a = "
                    f"{self.entradas['a'].get()}; b = "
                    f"{self.entradas['b'].get()}; tolerancia Ea = "
                    f"{self.entradas['tolerancia'].get()} %; máximo de "
                    f"iteraciones = {self.entradas['max_iteraciones'].get()}."
                ),
                f"Fórmula iterativa: {formula}",
                f"Criterio de parada: {criterio_visible}",
                f"Tabla de iteraciones:\n{tabla}",
                (
                    f"Aproximación final: {aproximacion_texto} | "
                    f"Residuo |f(x)|: {residuo_texto}"
                ),
            ]
        )
        self._mostrar("\n".join(salida), reporte)

    def al_ocultar(self):
        cerrar_teclado_matematico(self)
        if self._ventana_grafica is not None:
            try:
                if self._ventana_grafica.winfo_exists():
                    self._ventana_grafica.al_cerrar()
            except TclError:
                pass
            self._ventana_grafica = None

    def cargar_ejemplo(self):
        """Carga f(x) = e^(-x) - x en [0, 1]; no ejecuta el método."""
        ejemplo = {"a": "0", "b": "1", "tolerancia": "0.00001", "max_iteraciones": "100"}
        actuales = [self.funcion_var.get()] + [self.entradas[c].get() for c in ejemplo]
        if not confirmar_reemplazo(self, actuales, ["e^(-x) - x", *ejemplo.values()]):
            return False
        self.funcion_var.set("e^(-x) - x")
        for clave, valor in ejemplo.items():
            escribir_campo(self.entradas[clave], valor)
        self._mostrar("Ejemplo cargado: e^(-x) - x en [0, 1]. Pulse «Resolver».")
        return True

    def borrar(self):
        self.funcion_var.set("")
        for clave in ("a", "b", "tolerancia", "max_iteraciones"):
            self.entradas[clave].delete(0, "end")
        self._mostrar("Campos borrados. Ingrese los datos para resolver.")

    def _formatear_reporte_copiado(self, texto):
        return self._reporte_academico if self._reporte_academico is not None else texto

    def _mostrar(self, texto, reporte=None):
        self._reporte_academico = reporte
        if texto.startswith("ERROR:"):
            reproducir_sonido_error(self, texto)
        escribir_consola(self.texto_salida, texto)
