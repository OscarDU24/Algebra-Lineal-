"""Interfaz para aplicar manualmente el método de bisección."""

from tkinter import TclError

from core.metodos_numericos import biseccion
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
from core.ui.tema import (
    ACENTO,
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_panel_contenedor,
)
from core.ui.teclado_matematico import abrir_teclado_matematico
from core.ui.teclado_matematico import cerrar_teclado_matematico


class VistaBiseccion(ctk.CTkFrame):
    """Permite explorar la función y resolver con extremos escritos por el usuario."""

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self._reporte_academico = None
        self._ventana_grafica = None
        self._al_resolver_completado = None
        self._al_copiar_completado = None
        self._al_zoom_cambiado = None
        self._resaltados = {}
        self._crear_interfaz()

    def _crear_interfaz(self):
        encabezado = ctk.CTkFrame(self, **estilo_panel_contenedor())
        encabezado.pack(fill="x", padx=15, pady=(12, 6))
        ctk.CTkLabel(
            encabezado,
            text="Método de Bisección",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(
            encabezado,
            text=(
                "Use notación algebraica (por ejemplo, 2x o x^2), explore "
                "f(x) en la gráfica independiente y escriba manualmente "
                "el intervalo [a, b]."
            ),
            text_color=TEXTO_CLARO,
            wraplength=950,
        ).pack(anchor="w", padx=12, pady=(0, 8))

        self.marco_entradas = ctk.CTkFrame(self, **estilo_panel_contenedor())
        self.marco_entradas.pack(fill="x", padx=15, pady=5)
        self.marco_entradas.grid_columnconfigure(0, weight=2)
        self.marco_entradas.grid_columnconfigure(1, weight=1)
        self.marco_entradas.grid_columnconfigure(2, weight=1)
        self.marco_entradas.grid_columnconfigure(3, weight=1)

        campos = (
            ("Función f(x)", "funcion", "x² - x - 1", 300),
            ("Valor de a", "a", "1", 130),
            ("Valor de b", "b", "2", 130),
            ("Tolerancia en x", "tolerancia", "1e-6", 140),
        )
        self.entradas = {}
        self.funcion_var = ctk.StringVar(value=campos[0][2])
        for columna, (etiqueta, clave, valor, ancho) in enumerate(campos):
            ctk.CTkLabel(
                self.marco_entradas,
                text=etiqueta,
                text_color=TEXTO_CLARO,
            ).grid(row=0, column=columna, padx=8, pady=(8, 3), sticky="w")
            opciones = {"width": ancho, "font": ("Consolas", 12)}
            if clave == "funcion":
                opciones["textvariable"] = self.funcion_var
            campo = ctk.CTkEntry(self.marco_entradas, **opciones)
            campo.grid(
                row=1, column=columna, padx=8, pady=(0, 9), sticky="ew"
            )
            if clave != "funcion":
                campo.insert(0, valor)
            self.entradas[clave] = campo

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.pack(fill="x", padx=15, pady=4)
        self.boton_teclado = ctk.CTkButton(
            acciones,
            text="Teclado matemático",
            command=lambda: abrir_teclado_matematico(
                self, self.entradas["funcion"]
            ),
            **estilo_boton_secundario(),
        )
        self.boton_teclado.pack(side="left", padx=(0, 8))
        self.boton_grafica = ctk.CTkButton(
            acciones,
            text="Explorar gráfica",
            command=self.abrir_grafica,
            **estilo_boton_secundario(),
        )
        self.boton_grafica.pack(side="left", padx=(0, 8))
        self.boton_resolver = ctk.CTkButton(
            acciones,
            text="Biseccionar",
            command=self.resolver,
            **estilo_boton_principal(),
        )
        self.boton_resolver.pack(side="left", padx=(0, 8))
        self.boton_limpiar = ctk.CTkButton(
            acciones,
            text="Limpiar entradas",
            command=self.borrar,
            **estilo_boton_secundario(),
        )
        self.boton_limpiar.pack(side="left")

        salida = ctk.CTkFrame(self, **estilo_panel_contenedor())
        salida.pack(fill="both", expand=True, padx=15, pady=(4, 12))
        ctk.CTkLabel(
            salida,
            text="Salida · iteraciones y contraste numérico",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=10, pady=(6, 2))
        self.contenedor_salida, self.texto_salida, self.zoom_salida = (
            crear_consola_resultados(
                salida,
                tamano=11,
                formateador_copia=self._formatear_reporte_copiado,
                al_copiar=self._notificar_copia,
            )
        )
        self.contenedor_salida.pack(fill="both", expand=True, padx=8, pady=(0, 7))
        self.boton_copiar = self.contenedor_salida.barra.boton_copiar
        self.controles_zoom = self.contenedor_salida.controles_zoom
        self.boton_zoom_mas = self.controles_zoom.boton_mas
        self.zoom_salida.agregar_observador(self._notificar_zoom)
        self._mostrar(
            "Ingrese f(x), los extremos manuales a y b, y una tolerancia "
            "positiva. La gráfica solo sirve como apoyo visual."
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
            extremo_a = biseccion._convertir_finito(
                self.entradas["a"].get(), "El extremo a"
            )
            extremo_b = biseccion._convertir_finito(
                self.entradas["b"].get(), "El extremo b"
            )
            resultado = biseccion.resolver_biseccion(
                self.funcion_var.get(),
                extremo_a,
                extremo_b,
                self.entradas["tolerancia"].get(),
            )
        except (ValueError, ArithmeticError, OverflowError) as error:
            self._mostrar(f"ERROR: {error}")
            return

        formula = (
            "x_r = (a + b) / 2; si f(a)·f(x_r) < 0, conservar [a, x_r]; "
            "en otro caso, conservar [x_r, b]."
        )
        criterio = resultado["criterio_paro"]
        if criterio == "ancho del intervalo":
            criterio_visible = (
                "Ancho del intervalo b - a < tolerancia. La parada no exige "
                "|f(x_r)| < tolerancia; el residuo puede ser ligeramente mayor."
            )
        elif criterio in ("raíz exacta", "raíz en un extremo"):
            criterio_visible = "Raíz exacta: f(x_r) = 0."
        else:
            criterio_visible = criterio
        residuo = abs(resultado["f_raiz"])
        tabla = biseccion.formatear_tabla(resultado)
        salida = [
            f"Intervalo manual: [{extremo_a:.12g}, {extremo_b:.12g}]",
            f"Raíz aproximada: {resultado['raiz']:.12g}",
            f"|f(raíz)| (residuo): {residuo:.10e}",
            f"Iteraciones realizadas: {resultado['iteraciones']}",
            f"Iteraciones teóricas mínimas: {resultado['iteraciones_teoricas']}",
            f"Fórmula iterativa: {formula}",
            f"Criterio de parada: {criterio_visible}",
            "",
            tabla,
        ]
        reporte = "\n".join(
            [
                "Método seleccionado: Bisección",
                "Justificación de elección e intervalo/valores iniciales: "
                "[Completar por el estudiante]",
                (
                    "Datos iniciales: "
                    f"f(x) = {self.funcion_var.get()}; a = "
                    f"{self.entradas['a'].get()}; b = "
                    f"{self.entradas['b'].get()}; tolerancia = "
                    f"{self.entradas['tolerancia'].get()}."
                ),
                f"Fórmula iterativa: {formula}",
                f"Criterio de parada: {criterio_visible}",
                f"Tabla de iteraciones:\n{tabla}",
                (
                    f"Aproximación final: x ≈ {resultado['raiz']:.12g} | "
                    f"Residuo |f(x)|: {residuo:.10e}"
                ),
            ]
        )
        self._mostrar("\n".join(salida), reporte)
        if self._al_resolver_completado is not None:
            self._al_resolver_completado(resultado)

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
        """Carga f(x) = x^3 - x - 2 en [1, 2]; no ejecuta el método."""
        ejemplo = {"a": "1", "b": "2", "tolerancia": "1e-6"}
        actuales = [self.funcion_var.get()] + [self.entradas[c].get() for c in ejemplo]
        if not confirmar_reemplazo(self, actuales, ["x^3 - x - 2", *ejemplo.values()]):
            return False
        self.funcion_var.set("x^3 - x - 2")
        for clave, valor in ejemplo.items():
            escribir_campo(self.entradas[clave], valor)
        self._mostrar("Ejemplo cargado: x^3 - x - 2 en [1, 2]. Pulse «Biseccionar».")
        return True

    def borrar(self):
        self.funcion_var.set("")
        for clave in ("a", "b", "tolerancia"):
            self.entradas[clave].delete(0, "end")
        self._mostrar(
            "Campos borrados. Ingrese la función, los extremos a y b, "
            "y la tolerancia."
        )

    def _formatear_reporte_copiado(self, texto):
        return self._reporte_academico if self._reporte_academico is not None else texto

    def _notificar_copia(self):
        if self._al_copiar_completado is not None:
            self._al_copiar_completado()

    def _notificar_zoom(self, nivel):
        if self._al_zoom_cambiado is not None:
            self._al_zoom_cambiado(nivel)

    def resaltar_borde(self, widget, clave, activo):
        if activo:
            if clave not in self._resaltados:
                self._resaltados[clave] = (
                    widget.cget("border_color"),
                    widget.cget("border_width"),
                )
            widget.configure(border_color=ACENTO, border_width=4)
        elif clave in self._resaltados:
            color, ancho = self._resaltados.pop(clave)
            widget.configure(border_color=color, border_width=ancho)

    def _mostrar(self, texto, reporte=None):
        self._reporte_academico = reporte
        if texto.startswith("ERROR:"):
            reproducir_sonido_error(self, texto)
        escribir_consola(self.texto_salida, texto)
