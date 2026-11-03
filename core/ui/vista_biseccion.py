"""Interfaz para el método de bisección y su contraste con SciPy."""

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


class VistaBiseccion(ctk.CTkFrame):
    """Panel con campos, tabla iterativa y contraste SciPy."""

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self._crear_interfaz()

    def _crear_interfaz(self):
        encabezado = ctk.CTkFrame(self, **estilo_panel_contenedor())
        encabezado.pack(fill="x", padx=15, pady=(15, 8))
        ctk.CTkLabel(
            encabezado,
            text="Método de Bisección",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(
            encabezado,
            text="f(x), intervalo [a, b], tolerancia y comparación con scipy.optimize.bisect",
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=12, pady=(0, 10))

        entradas = ctk.CTkFrame(self, **estilo_panel_contenedor())
        entradas.pack(fill="x", padx=15, pady=6)
        campos = (
            ("Función f(x)", "funcion", "x**3 - x - 2", 300),
            ("Valor de a", "a", "1", 125),
            ("Valor de b", "b", "2", 125),
            ("Tolerancia/Error Max", "tolerancia", "1e-6", 150),
        )
        self.entradas = {}
        for columna, (etiqueta, clave, valor, ancho) in enumerate(campos):
            ctk.CTkLabel(entradas, text=etiqueta, text_color=TEXTO_CLARO).grid(
                row=0, column=columna, padx=8, pady=(10, 3), sticky="w"
            )
            campo = ctk.CTkEntry(entradas, width=ancho, font=("Consolas", 13))
            campo.grid(row=1, column=columna, padx=8, pady=(0, 10), sticky="ew")
            campo.insert(0, valor)
            self.entradas[clave] = campo
            entradas.grid_columnconfigure(columna, weight=1)

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(
            acciones,
            text="Biseccionar",
            command=self.calcular,
            **estilo_boton_principal(),
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            acciones,
            text="Borrar",
            command=self.borrar,
            **estilo_boton_secundario(),
        ).pack(side="left")

        salida = ctk.CTkFrame(self, **estilo_panel_contenedor())
        salida.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        ctk.CTkLabel(
            salida,
            text="Salida · tabla de iteraciones y contraste numérico",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=10, pady=(8, 4))
        self.texto_salida = ctk.CTkTextbox(
            salida,
            font=("Consolas", 12),
            wrap="none",
            **estilo_consola_resultado(),
        )
        self.texto_salida.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._mostrar(
            "Ingrese una función válida usando x, aritmética y funciones permitidas "
            "(sin, cos, tan, sqrt, exp, log, abs)."
        )

    def calcular(self):
        try:
            resultado = biseccion.resolver_biseccion(
                self.entradas["funcion"].get(),
                self.entradas["a"].get(),
                self.entradas["b"].get(),
                self.entradas["tolerancia"].get(),
            )
        except (ValueError, ArithmeticError) as error:
            self._mostrar(f"ERROR: {error}")
            return

        salida = [
            f"Raíz aproximada (bisección): {resultado['raiz']:.12g}",
            f"f(raíz): {resultado['f_raiz']:.6g}",
            f"Iteraciones realizadas: {resultado['iteraciones']}",
            f"Iteraciones teóricas mínimas: {resultado['iteraciones_teoricas']}",
            f"Criterio de paro: {resultado['criterio_paro']}",
            "",
            biseccion.formatear_tabla(resultado),
            "",
            f"Raíz con scipy.optimize.bisect: {resultado['raiz_scipy']:.12g}",
            f"Diferencia absoluta: {resultado['diferencia_absoluta']:.6g}",
        ]
        self._mostrar("\n".join(salida))

    def borrar(self):
        for campo in self.entradas.values():
            campo.delete(0, "end")
        self._mostrar("Campos borrados.")

    def _mostrar(self, texto):
        reproducir_sonido_error(self, texto)
        self.texto_salida.delete("1.0", "end")
        self.texto_salida.insert("1.0", texto)
