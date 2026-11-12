"""Interfaz para aplicar el método de Newton-Raphson."""

from tkinter import TclError

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


class VistaNewtonRaphson(ctk.CTkFrame):
    """Calcula una raíz con la aproximación inicial y la derivada."""

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self._crear_interfaz()

    def _crear_interfaz(self):
        encabezado = ctk.CTkFrame(self, **estilo_panel_contenedor())
        encabezado.pack(fill="x", padx=15, pady=(12, 6))
        ctk.CTkLabel(
            encabezado,
            text="Método de Newton-Raphson",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(anchor="w", padx=12, pady=(8, 2))
        ctk.CTkLabel(
            encabezado,
            text=(
                "Escriba la función f(x), opcionalmente su derivada f'(x), "
                "el valor inicial x0 y la tolerancia. Si no escribe la derivada, "
                "se apoya en una diferencia finita central segura."
            ),
            text_color=TEXTO_CLARO,
            wraplength=950,
        ).pack(anchor="w", padx=12, pady=(0, 8))

        entradas = ctk.CTkFrame(self, **estilo_panel_contenedor())
        entradas.pack(fill="x", padx=15, pady=5)
        for columna, peso in enumerate((3, 3, 1, 1, 1)):
            entradas.grid_columnconfigure(columna, weight=peso)

        campos = (
            ("Función f(x)", "funcion", 300, "x^3 - x - 2"),
            ("Derivada f'(x)", "derivada", 300, "3*x^2 - 1"),
            ("x0", "x0", 120, "1.5"),
            ("Tolerancia", "tolerancia", 140, "1e-8"),
            ("Máx. iteraciones", "max_iteraciones", 130, "50"),
        )
        self.entradas = {}
        for columna, (etiqueta, clave, ancho, valor_inicial) in enumerate(campos):
            ctk.CTkLabel(
                entradas,
                text=etiqueta,
                text_color=TEXTO_CLARO,
            ).grid(row=0, column=columna, padx=7, pady=(8, 3), sticky="w")
            campo = ctk.CTkEntry(entradas, width=ancho, font=("Consolas", 12))
            campo.grid(row=1, column=columna, padx=7, pady=(0, 9), sticky="ew")
            campo.insert(0, valor_inicial)
            self.entradas[clave] = campo

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.pack(fill="x", padx=15, pady=4)
        ctk.CTkButton(
            acciones,
            text="Teclado f(x)",
            command=lambda: abrir_teclado_matematico(self, self.entradas["funcion"]),
            **estilo_boton_secundario(),
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            acciones,
            text="Teclado f'(x)",
            command=lambda: abrir_teclado_matematico(self, self.entradas["derivada"]),
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
            "Ingrese la función, el valor inicial x0 y la tolerancia. "
            "La derivada puede quedar vacía para calcularla numéricamente."
        )

    def resolver(self):
        try:
            resultado = newton_raphson.resolver_newton_raphson(
                self.entradas["funcion"].get(),
                self.entradas["x0"].get(),
                self.entradas["tolerancia"].get(),
                self.entradas["max_iteraciones"].get(),
                self.entradas["derivada"].get(),
            )
        except (ValueError, ArithmeticError, OverflowError) as error:
            self._mostrar(f"ERROR: {error}")
            return

        salida = [
            f"Estado: {resultado['estado']}",
            f"Convergió: {'Sí' if resultado['convergio'] else 'No'}",
            f"Iteraciones realizadas: {resultado['iteraciones']}",
        ]
        if resultado["raiz"] is not None:
            salida.append(f"Raíz aproximada: {resultado['raiz']:.12g}")
        salida.extend(
            [
                f"Tolerancia: {resultado['tolerancia']:.6g}",
                "",
                newton_raphson.formatear_tabla(resultado),
            ]
        )
        self._mostrar("\n".join(salida))

    def borrar(self):
        for clave in ("funcion", "derivada", "x0", "tolerancia", "max_iteraciones"):
            self.entradas[clave].delete(0, "end")
        self.entradas["funcion"].insert(0, "x^3 - x - 2")
        self.entradas["derivada"].insert(0, "3*x^2 - 1")
        self.entradas["x0"].insert(0, "1.5")
        self.entradas["tolerancia"].insert(0, "1e-8")
        self.entradas["max_iteraciones"].insert(0, "50")
        self._mostrar("Campos reiniciados con el caso guía de Newton-Raphson.")

    def al_ocultar(self):
        cerrar_teclado_matematico(self)

    def _mostrar(self, texto):
        if texto.startswith("ERROR:"):
            reproducir_sonido_error(self, texto)
        self.texto_salida.delete("1.0", "end")
        self.texto_salida.insert("1.0", texto)
