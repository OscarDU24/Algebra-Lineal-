"""Interfaz para aplicar manualmente el método de bisección."""

from tkinter import TclError

from core.metodos_numericos import biseccion
from core.ui.audio_manager import reproducir_sonido_error
from core.ui.ctk_compat import ctk
from core.ui.tema import (
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
        self._ventana_grafica = None
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

        entradas = ctk.CTkFrame(self, **estilo_panel_contenedor())
        entradas.pack(fill="x", padx=15, pady=5)
        entradas.grid_columnconfigure(0, weight=2)
        entradas.grid_columnconfigure(1, weight=1)
        entradas.grid_columnconfigure(2, weight=1)
        entradas.grid_columnconfigure(3, weight=1)

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
                entradas,
                text=etiqueta,
                text_color=TEXTO_CLARO,
            ).grid(row=0, column=columna, padx=8, pady=(8, 3), sticky="w")
            opciones = {"width": ancho, "font": ("Consolas", 12)}
            if clave == "funcion":
                opciones["textvariable"] = self.funcion_var
            campo = ctk.CTkEntry(entradas, **opciones)
            campo.grid(
                row=1, column=columna, padx=8, pady=(0, 9), sticky="ew"
            )
            if clave != "funcion":
                campo.insert(0, valor)
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
            text="Biseccionar",
            command=self.resolver,
            **estilo_boton_principal(),
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            acciones,
            text="Borrar",
            command=self.borrar,
            **estilo_boton_secundario(),
        ).pack(side="left")

        salida = ctk.CTkFrame(self, **estilo_panel_contenedor())
        salida.pack(fill="both", expand=True, padx=15, pady=(4, 12))
        ctk.CTkLabel(
            salida,
            text="Salida · iteraciones y contraste numérico",
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

        salida = [
            f"Intervalo manual: [{extremo_a:.12g}, {extremo_b:.12g}]",
            f"Raíz aproximada: {resultado['raiz']:.12g}",
            f"|f(raíz)| (residuo): {abs(resultado['f_raiz']):.6g}",
            f"Iteraciones realizadas: {resultado['iteraciones']}",
            f"Iteraciones teóricas mínimas: {resultado['iteraciones_teoricas']}",
            f"Criterio de paro: {resultado['criterio_paro']}",
            "",
            biseccion.formatear_tabla(resultado),
        ]
        self._mostrar("\n".join(salida))

    def al_ocultar(self):
        cerrar_teclado_matematico(self)
        if self._ventana_grafica is not None:
            try:
                if self._ventana_grafica.winfo_exists():
                    self._ventana_grafica.al_cerrar()
            except TclError:
                pass
            self._ventana_grafica = None

    def borrar(self):
        self.funcion_var.set("")
        for clave in ("a", "b", "tolerancia"):
            self.entradas[clave].delete(0, "end")
        self._mostrar(
            "Campos borrados. Ingrese la función, los extremos a y b, "
            "y la tolerancia."
        )

    def _mostrar(self, texto):
        if texto.startswith("ERROR:"):
            reproducir_sonido_error(self, texto)
        self.texto_salida.delete("1.0", "end")
        self.texto_salida.insert("1.0", texto)
