"""Ventana unificada para las herramientas de métodos numéricos."""

from core.ui.ctk_compat import ctk
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_menu_desplegable,
    estilo_panel_contenedor,
)


class VistaMetodosNumericos(ctk.CTkToplevel):
    """Agrupa los métodos numéricos disponibles bajo un selector."""

    OPERACIONES = (
        "Método de Bisección",
        "Método Regula Falsi",
        "Método de Newton-Raphson",
        "Análisis de Errores",
    )

    def __init__(self, master):
        super().__init__(master)
        self.master_dashboard = master
        self.master_dashboard.withdraw()
        self.audio_manager = getattr(master, "audio_manager", None)
        self.configure(fg_color=FONDO_CALCULADORA)
        self.title("Métodos Numéricos")
        self.geometry("1080x760")
        self.minsize(820, 620)
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self._paneles = {}
        self._operacion_activa = self.OPERACIONES[0]
        self._crear_interfaz()

    def _crear_interfaz(self):
        selector = ctk.CTkFrame(self, **estilo_panel_contenedor())
        selector.pack(fill="x", padx=15, pady=(15, 8))
        ctk.CTkLabel(
            selector,
            text="Métodos Numéricos · Operación",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXTO_CLARO,
        ).pack(side="left", padx=12, pady=10)
        self.menu_operacion = ctk.CTkComboBox(
            selector,
            values=list(self.OPERACIONES),
            command=self.cambiar_operacion,
            **estilo_menu_desplegable(),
        )
        self.menu_operacion.pack(side="left", padx=8, pady=8)
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True)
        self.menu_operacion.set(self.OPERACIONES[0])
        self.cambiar_operacion(self.OPERACIONES[0])

    def cambiar_operacion(self, operacion=None):
        operacion = operacion or self.menu_operacion.get()
        if operacion not in self.OPERACIONES:
            raise ValueError(f"Operación de métodos numéricos no reconocida: {operacion}")

        if operacion != self._operacion_activa:
            panel_activo = self._paneles.get(self._operacion_activa)
            cerrar_auxiliares = getattr(panel_activo, "al_ocultar", None)
            if cerrar_auxiliares is not None:
                cerrar_auxiliares()
        for panel in self._paneles.values():
            panel.pack_forget()
        if operacion not in self._paneles:
            if operacion == self.OPERACIONES[0]:
                from core.ui.vista_biseccion import VistaBiseccion

                panel = VistaBiseccion(self.contenedor)
            elif operacion == self.OPERACIONES[1]:
                from core.ui.vista_regla_falsa import VistaReglaFalsa

                panel = VistaReglaFalsa(self.contenedor)
            elif operacion == self.OPERACIONES[2]:
                from core.ui.vista_newton_raphson import VistaNewtonRaphson

                panel = VistaNewtonRaphson(self.contenedor)
            else:
                from core.ui.vista_errores import VistaErrores

                panel = VistaErrores(self.contenedor)
            self._paneles[operacion] = panel
        self._operacion_activa = operacion
        self._paneles[operacion].pack(fill="both", expand=True)

    def al_cerrar(self):
        for panel in self._paneles.values():
            cerrar_auxiliares = getattr(panel, "al_ocultar", None)
            if cerrar_auxiliares is not None:
                cerrar_auxiliares()
        self.master_dashboard.deiconify()
        self.destroy()
