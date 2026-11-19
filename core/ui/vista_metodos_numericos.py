"""Ventana unificada para las herramientas de métodos numéricos."""

from tkinter import messagebox

from core.ui.ctk_compat import ctk
from core.ui.navegacion import (
    confirmar_reemplazo,
    escribir_campo,
    instalar_navegacion,
)
from core.ui.tema import (
    ACENTO,
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_menu_desplegable,
    estilo_panel_contenedor,
)


class VistaMetodosNumericos(ctk.CTkToplevel):
    """Agrupa los métodos numéricos disponibles bajo un selector."""

    EJEMPLOS = {
        "Ej. 1": {
            "operacion": "Método de Bisección",
            "funcion": "x**3 - 4*x - 9",
            "datos": {"a": "2", "b": "3"},
        },
        "Ej. 2a (raíz menor)": {
            "operacion": "Método de Bisección",
            "funcion": "exp(x) - 3*x**2",
            "datos": {"a": "0", "b": "1"},
        },
        "Ej. 2b (raíz mayor)": {
            "operacion": "Método de Bisección",
            "funcion": "exp(x) - 3*x**2",
            "datos": {"a": "3", "b": "4"},
        },
        "Ej. 3": {
            "operacion": "Métodos Abiertos",
            "funcion": "cos(x) - x*exp(x)",
            "datos": {"x0": "0.5"},
        },
        "Ej. 4": {
            "operacion": "Métodos Abiertos",
            "funcion": "x*log(x) - 1",
            "datos": {"x0": "2"},
        },
        "Ej. 5": {
            "operacion": "Método de Bisección",
            "funcion": "x**4 - 3*x**2 - 3",
            "datos": {"a": "1", "b": "2"},
        },
        "Ej. 6": {
            "operacion": "Método de Bisección",
            "funcion": "log(x + 2) + x**2 - 2",
            "datos": {"a": "0", "b": "1"},
        },
        "Ej. 7": {
            "operacion": "Métodos Abiertos",
            "funcion": "exp(-x) - x**2 + 0.5",
            "datos": {"x0": "1"},
        },
        "Ej. 8": {
            "operacion": "Métodos Abiertos",
            "funcion": "x**3 + x - 1",
            "datos": {"x0": "0.5"},
        },
        "Ej. 9a (raíz menor)": {
            "operacion": "Método de Bisección",
            "funcion": "x*exp(-x) - 0.2",
            "datos": {"a": "0", "b": "1"},
        },
        "Ej. 9b (raíz mayor)": {
            "operacion": "Método de Bisección",
            "funcion": "x*exp(-x) - 0.2",
            "datos": {"a": "2", "b": "3"},
        },
        "Ej. 10 (raíz no trivial)": {
            "operacion": "Método de Bisección",
            "funcion": "x**2 - 5*sin(x)",
            "datos": {"a": "2", "b": "3"},
        },
    }

    OPERACIONES = (
        "Método de Bisección",
        "Método Regula Falsi",
        "Métodos Abiertos",
        "Análisis de Errores",
    )

    def __init__(self, master, recorrido=None):
        super().__init__(master)
        self.master_dashboard = master
        self._recorrido = recorrido
        self._ejemplo_guiado_cargado = False
        self._resaltados = {}
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
        self._barra_navegacion = instalar_navegacion(
            self,
            lambda: self.CLAVES_AYUDA[self._operacion_activa],
            opciones_ejemplo=self.EJEMPLOS,
            al_seleccionar_ejemplo=self.seleccionar_ejemplo,
        )
        if self._recorrido is not None:
            self._activar_recorrido()

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

    def seleccionar_ejemplo(self, nombre):
        """Carga un ejercicio del banco sin iniciar el cálculo."""
        ejemplo = self.EJEMPLOS.get(nombre)
        if ejemplo is None:
            raise ValueError(f"Ejemplo de métodos numéricos no reconocido: {nombre}")
        if self._recorrido is not None and nombre != "Ej. 1":
            self._recorrido.ejemplo_no_esperado()
            return False

        operacion = ejemplo["operacion"]
        panel = self._paneles.get(operacion)
        tolerancia = "1e-6"
        reemplazo_tutorial_nuevo = (
            self._recorrido is not None and not self._ejemplo_guiado_cargado
        )
        if panel is not None and not reemplazo_tutorial_nuevo:
            if operacion == "Método de Bisección":
                claves = ("a", "b", "tolerancia")
                valores_actuales = [
                    panel.funcion_var.get(),
                    *[panel.entradas[clave].get() for clave in claves],
                ]
                valores_ejemplo = [
                    ejemplo["funcion"],
                    ejemplo["datos"]["a"],
                    ejemplo["datos"]["b"],
                    tolerancia,
                ]
            else:
                valores_actuales = [
                    panel.funcion_var.get(),
                    panel.metodo_var.get(),
                    panel.entradas["x0"].get(),
                    panel.entradas["tolerancia"].get(),
                ]
                valores_ejemplo = [
                    ejemplo["funcion"],
                    "newton",
                    ejemplo["datos"]["x0"],
                    tolerancia,
                ]
            if not confirmar_reemplazo(self, valores_actuales, valores_ejemplo):
                return False

        self.cambiar_operacion(operacion)
        panel = self._paneles[operacion]
        panel.funcion_var.set(ejemplo["funcion"])
        if operacion == "Método de Bisección":
            for clave, valor in ejemplo["datos"].items():
                escribir_campo(panel.entradas[clave], valor)
            escribir_campo(panel.entradas["tolerancia"], tolerancia)
        else:
            panel.metodo_var.set("newton")
            panel._cambiar_metodo()
            escribir_campo(panel.entradas["x0"], ejemplo["datos"]["x0"])
            escribir_campo(panel.entradas["tolerancia"], tolerancia)
        panel._mostrar(
            f"{nombre} cargado. Revise los datos y pulse «Resolver» para "
            "iniciar el método."
        )
        if self._recorrido is not None:
            self._ejemplo_guiado_cargado = True
            self._no_marcar_ejemplo_como_cambio = True
            self._recorrido.ejemplo_cargado()
        return True

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
        self.area_contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.area_contenido.pack(fill="both", expand=True)
        self.panel_recorrido = None
        if self._recorrido is not None:
            from core.ui.bienvenida import PanelRecorrido

            self.panel_recorrido = PanelRecorrido(
                self.area_contenido,
                anterior=self._recorrido.recorrido_anterior,
                salir=self._recorrido.salir_recorrido,
                siguiente=self._recorrido.recorrido_siguiente,
            )
            self.panel_recorrido.pack(
                side="right", fill="y", padx=(0, 12), pady=(8, 12)
            )
        self.contenedor = ctk.CTkFrame(self.area_contenido, fg_color="transparent")
        self.contenedor.pack(side="left", fill="both", expand=True)
        self.menu_operacion.set(self.OPERACIONES[0])
        self.cambiar_operacion(self.OPERACIONES[0])

    def _activar_recorrido(self):
        self.menu_operacion.configure(state="disabled")
        self._barra_navegacion.boton_ayuda.configure(state="disabled")
        panel = self._paneles["Método de Bisección"]
        panel._al_resolver_completado = self._validar_resultado_recorrido
        panel._al_copiar_completado = self._recorrido.copia_completada
        panel._al_zoom_cambiado = self._recorrido.zoom_cambiado
        self._recorrido.vista_recorrido_abierta(self)

    def desactivar_recorrido(self):
        """Retira las restricciones y resaltados si el usuario sale del tutorial."""
        if self._recorrido is None:
            return
        self._recorrido = None
        self._limpiar_resaltados()
        self.menu_operacion.configure(state="normal")
        self._barra_navegacion.boton_ayuda.configure(state="normal")
        self._barra_navegacion.boton_volver.configure(state="normal")
        self._barra_navegacion.selector_ejemplo.configure(state="normal")
        panel = self._paneles["Método de Bisección"]
        panel._al_resolver_completado = None
        panel._al_copiar_completado = None
        panel._al_zoom_cambiado = None
        for boton in (
            panel.boton_teclado,
            panel.boton_grafica,
            panel.boton_resolver,
            panel.boton_limpiar,
            panel.boton_copiar,
        ):
            boton.configure(state="normal")
        nivel = panel.zoom_salida.nivel
        panel.boton_zoom_mas.configure(
            state="disabled" if nivel >= 200 else "normal"
        )
        panel.controles_zoom.boton_menos.configure(
            state="disabled" if nivel <= 50 else "normal"
        )
        panel.controles_zoom.boton_nivel.configure(state="normal")
        if self.panel_recorrido is not None:
            self.panel_recorrido.destroy()
            self.panel_recorrido = None

    def aplicar_paso_recorrido(self, estado, contenido):
        if self.panel_recorrido is None:
            return
        self.panel_recorrido.mostrar(
            contenido["paso"],
            contenido["total"],
            contenido["titulo"],
            contenido["descripcion"],
            anterior_habilitado=contenido["anterior"],
            siguiente_habilitado=contenido["siguiente"],
            siguiente_texto=contenido.get("siguiente_texto", "Siguiente →"),
        )
        panel = self._paneles["Método de Bisección"]
        self._limpiar_resaltados()
        widgets = {
            "campos": panel.marco_entradas,
            "calcular": panel.boton_resolver,
            "resultado": panel.contenedor_salida,
            "copiar": panel.boton_copiar,
            "zoom": panel.boton_zoom_mas,
            "volver": self._barra_navegacion.boton_volver,
        }
        if estado == "ejemplo":
            self._resaltar_selector(True)
        elif estado in widgets:
            panel.resaltar_borde(widgets[estado], estado, True)

        self._barra_navegacion.selector_ejemplo.configure(
            state="normal" if estado == "ejemplo" else "disabled"
        )
        self._barra_navegacion.boton_volver.configure(
            state="normal" if estado == "volver" else "disabled"
        )
        panel.boton_teclado.configure(state="disabled")
        panel.boton_grafica.configure(state="disabled")
        panel.boton_limpiar.configure(state="disabled")
        panel.boton_resolver.configure(
            state="normal" if estado == "calcular" else "disabled"
        )
        panel.boton_copiar.configure(
            state="normal" if estado == "copiar" else "disabled"
        )
        zoom_habilitado = estado == "zoom"
        panel.controles_zoom.boton_mas.configure(
            state=(
                "disabled"
                if not zoom_habilitado or panel.zoom_salida.nivel >= 200
                else "normal"
            )
        )
        panel.controles_zoom.boton_menos.configure(
            state=(
                "disabled"
                if not zoom_habilitado or panel.zoom_salida.nivel <= 50
                else "normal"
            )
        )
        panel.controles_zoom.boton_nivel.configure(
            state="normal" if zoom_habilitado else "disabled"
        )

    def mostrar_fin_recorrido(self):
        if self.panel_recorrido is not None:
            self.panel_recorrido.mostrar_fin()

    def _validar_resultado_recorrido(self, resultado):
        panel = self._paneles["Método de Bisección"]
        try:
            datos_coinciden = (
                panel.funcion_var.get().strip() == self.EJEMPLOS["Ej. 1"]["funcion"]
                and float(panel.entradas["a"].get()) == 2.0
                and float(panel.entradas["b"].get()) == 3.0
                and float(panel.entradas["tolerancia"].get()) == 1e-6
            )
        except ValueError:
            datos_coinciden = False
        if not datos_coinciden:
            self._recorrido.calculo_no_esperado()
            self._barra_navegacion.selector_ejemplo.configure(state="normal")
            return
        self._recorrido.calculo_completado(resultado)

    def _resaltar_selector(self, activo):
        selector = self._barra_navegacion.selector_ejemplo
        if activo:
            if "selector" not in self._resaltados:
                self._resaltados["selector"] = {
                    clave: selector.cget(clave)
                    for clave in (
                        "fg_color",
                        "text_color",
                        "button_color",
                        "button_hover_color",
                    )
                }
            selector.configure(
                fg_color=ACENTO,
                text_color=TEXTO_CLARO,
                button_color=ACENTO,
                button_hover_color="#b30000",
            )
        elif "selector" in self._resaltados:
            selector.configure(**self._resaltados.pop("selector"))

    def _limpiar_resaltados(self):
        self._resaltar_selector(False)
        panel = self._paneles.get("Método de Bisección")
        if panel is not None:
            for clave in tuple(panel._resaltados):
                widget = {
                    "campos": panel.marco_entradas,
                    "calcular": panel.boton_resolver,
                    "resultado": panel.contenedor_salida,
                    "copiar": panel.boton_copiar,
                    "zoom": panel.boton_zoom_mas,
                    "volver": self._barra_navegacion.boton_volver,
                }.get(clave)
                if widget is not None:
                    panel.resaltar_borde(widget, clave, False)

    def cambiar_operacion(self, operacion=None):
        operacion = operacion or self.menu_operacion.get()
        if operacion not in self.OPERACIONES:
            raise ValueError(f"Operación de métodos numéricos no reconocida: {operacion}")
        self.menu_operacion.set(operacion)

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
