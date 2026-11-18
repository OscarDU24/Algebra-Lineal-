"""Ventana unificada para las herramientas de métodos numéricos."""

from tkinter import messagebox

from core.ui.ctk_compat import ctk
from core.ui.navegacion import confirmar_reemplazo, instalar_navegacion
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
        "Métodos Abiertos",
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
        # La ayuda corresponde al panel visible en cada momento.
        instalar_navegacion(
            self,
            lambda: self.CLAVES_AYUDA[self._operacion_activa],
            al_cargar_ejemplo=self.cargar_ejemplo,
        )

    CLAVES_AYUDA = {
        "Método de Bisección": "biseccion",
        "Método Regula Falsi": "regla_falsa",
        "Métodos Abiertos": "abiertos",
        "Análisis de Errores": "errores",
    }

    def cargar_ejemplo(self):
        """Carga el ejemplo del panel visible sin ejecutar el método."""
        panel = self._paneles.get(self._operacion_activa)
        cargar = getattr(panel, "cargar_ejemplo", None)
        if cargar is not None:
            return cargar()
        if self._operacion_activa == "Métodos Abiertos":
            # El panel ya restablece su caso guía con «Borrar»; se reutiliza
            # sin modificar ese módulo, pidiendo confirmación si hay otros datos.
            claves = ("x0", "x1", "tolerancia", "max_iteraciones")
            actuales = [panel.funcion_var.get()] + [panel.entradas[c].get() for c in claves]
            ejemplo = ["x³ - x - 2", "1.5", "2", "1e-8", "50"]
            if not confirmar_reemplazo(self, actuales, ejemplo):
                return False
            panel.borrar()
            return True
        messagebox.showinfo(
            "Cargar ejemplo",
            "Análisis de Errores tiene ejemplos en cada pestaña; en «Gauss-Jordan» "
            "use «Cargar Hilbert 5×5».",
            parent=self,
        )
        return False

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
                from core.ui.vista_metodos_abiertos import VistaMetodosAbiertos

                panel = VistaMetodosAbiertos(self.contenedor)
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
