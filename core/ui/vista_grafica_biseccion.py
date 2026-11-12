"""Explorador gráfico independiente para la función del método de bisección."""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from core.metodos_numericos.biseccion import (
    analizar_intervalos,
    muestrear_funcion,
    resolver_biseccion,
)
from core.ui.ctk_compat import ctk
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_panel_contenedor,
)
from core.ui.teclado_matematico import (
    abrir_teclado_matematico,
    cerrar_teclado_matematico,
)


class VistaGraficaBiseccion(ctk.CTkToplevel):
    """Grafica una función en un rango ajustable sin elegir a ni b."""

    def __init__(
        self,
        master,
        funcion_var,
        on_x_selected=None,
        on_range_updated=None,
        marcar_raices_reales=False,
        mostrar_marcas_raices=True,
        mostrar_estado_actualizacion=True,
    ):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self.title("Explorador gráfico · Métodos Numéricos")
        self.geometry("900x650")
        self.minsize(700, 500)
        self.funcion_var = funcion_var
        self.on_x_selected = on_x_selected
        self.on_range_updated = on_range_updated
        self.marcar_raices_reales = marcar_raices_reales
        self.mostrar_marcas_raices = mostrar_marcas_raices
        self.mostrar_estado_actualizacion = mostrar_estado_actualizacion
        self._x_seleccionado = None
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self._crear_interfaz()
        self.canvas.mpl_connect("button_press_event", self._seleccionar_x)
        self.graficar()

    def _crear_interfaz(self):
        controles = ctk.CTkFrame(self, **estilo_panel_contenedor())
        controles.pack(fill="x", padx=14, pady=(14, 7))

        ctk.CTkLabel(
            controles,
            text="Función f(x) · acepta 2x y x^2",
            text_color=TEXTO_CLARO,
        ).grid(row=0, column=0, padx=8, pady=(8, 2), sticky="w")
        self.entrada_funcion = ctk.CTkEntry(
            controles,
            textvariable=self.funcion_var,
            font=("Consolas", 12),
        )
        self.entrada_funcion.grid(
            row=1, column=0, padx=8, pady=(0, 8), sticky="ew"
        )
        self.boton_teclado = ctk.CTkButton(
            controles,
            text="Teclado matemático",
            command=lambda: abrir_teclado_matematico(
                self, self.entrada_funcion
            ),
            **estilo_boton_secundario(),
        )
        self.boton_teclado.grid(
            row=2, column=0, padx=8, pady=(0, 8), sticky="w"
        )

        for columna, etiqueta, valor, clave in (
            (1, "Rango mínimo", "-10", "x_min"),
            (2, "Rango máximo", "10", "x_max"),
        ):
            ctk.CTkLabel(
                controles,
                text=etiqueta,
                text_color=TEXTO_CLARO,
            ).grid(row=0, column=columna, padx=8, pady=(8, 2), sticky="w")
            campo = ctk.CTkEntry(
                controles,
                width=120,
                font=("Consolas", 12),
            )
            campo.grid(row=1, column=columna, padx=8, pady=(0, 8), sticky="ew")
            campo.insert(0, valor)
            setattr(self, f"entrada_{clave}", campo)

        controles.grid_columnconfigure(0, weight=1)

        self.boton_graficar = ctk.CTkButton(
            controles,
            text="Actualizar gráfica",
            command=self.graficar,
            **estilo_boton_principal(),
        )
        self.boton_graficar.grid(
            row=2, column=3, padx=8, pady=(0, 8), sticky="ew"
        )

        panel_grafica = ctk.CTkFrame(self, **estilo_panel_contenedor())
        panel_grafica.pack(fill="both", expand=True, padx=14, pady=(0, 7))
        self.figura = Figure(
            figsize=(8, 5),
            dpi=90,
            facecolor=FONDO_CALCULADORA,
        )
        self.ejes = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=panel_grafica)
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=7, pady=7
        )
        self._estilizar_ejes()

        self.estado = ctk.CTkLabel(
            self,
            text=(
                "Use la gráfica para explorar f(x), sus raíces candidatas y "
                "seleccionar valores cuando el método lo permita."
            ),
            text_color=TEXTO_CLARO,
            wraplength=850,
        )
        self.estado.pack(fill="x", padx=18, pady=(0, 12))

    def graficar(self):
        try:
            datos = muestrear_funcion(
                self.funcion_var.get(),
                self.entrada_x_min.get(),
                self.entrada_x_max.get(),
            )
            analisis = analizar_intervalos(
                self.funcion_var.get(),
                self.entrada_x_min.get(),
                self.entrada_x_max.get(),
            )
        except (ValueError, ArithmeticError, OverflowError) as error:
            self.ejes.clear()
            self._estilizar_ejes()
            self.ejes.set_title(
                "No se pudo generar la gráfica",
                color=TEXTO_CLARO,
            )
            self.canvas.draw_idle()
            self.estado.configure(text=f"ERROR: {error}")
            return

        self.ejes.clear()
        self._estilizar_ejes()
        self.ejes.plot(
            datos["x"],
            datos["y"],
            color="#56a8ff",
            linewidth=1.8,
            label="f(x)",
        )
        self.ejes.axhline(0, color="#eeeeee", linewidth=1, linestyle="--")
        raices_candidatas = analisis["intervalos"]
        raices_aproximadas = []
        candidatas_sin_refinar = 0
        if (
            raices_candidatas
            and self.mostrar_marcas_raices
            and self.marcar_raices_reales
        ):
            for intervalo in raices_candidatas:
                try:
                    resultado_raiz = resolver_biseccion(
                        self.funcion_var.get(),
                        intervalo["a"],
                        intervalo["b"],
                        1e-10,
                    )
                except (ValueError, ArithmeticError, OverflowError):
                    candidatas_sin_refinar += 1
                    continue
                raices_aproximadas.append(resultado_raiz["raiz"])

            if raices_aproximadas:
                self.ejes.scatter(
                    raices_aproximadas,
                    [0] * len(raices_aproximadas),
                    color="#67e8a5",
                    edgecolors="#111111",
                    linewidths=0.8,
                    marker="o",
                    s=54,
                    label="Raíz real aproximada",
                    zorder=5,
                )
                for raiz in raices_aproximadas:
                    self.ejes.annotate(
                        f"x ≈ {raiz:.6g}",
                        (raiz, 0),
                        xytext=(0, 8),
                        textcoords="offset points",
                        ha="center",
                        color="#67e8a5",
                        fontsize=8,
                    )
        elif raices_candidatas and self.mostrar_marcas_raices:
            puntos_raiz = [
                (
                    intervalo["raiz_muestreada"]
                    if intervalo["raiz_muestreada"] is not None
                    else (intervalo["a"] + intervalo["b"]) / 2
                )
                for intervalo in raices_candidatas
            ]
            self.ejes.scatter(
                puntos_raiz,
                [0] * len(puntos_raiz),
                color="#ff6b6b",
                marker="x",
                s=60,
                label="Raíz candidata",
                zorder=4,
            )
        if self._x_seleccionado is not None:
            self.ejes.axvline(
                self._x_seleccionado,
                color="#ffd166",
                linewidth=1.2,
                linestyle=":",
                label=f"x0 = {self._x_seleccionado:.6g}",
            )
        self.ejes.set_xlim(*datos["rango"])
        self.ejes.set_xlabel("x", color=TEXTO_CLARO)
        self.ejes.set_ylabel("f(x)", color=TEXTO_CLARO)
        self.ejes.set_title("Exploración visual de f(x)", color=TEXTO_CLARO)
        self.ejes.grid(True, color="#555555", alpha=0.35)
        self.ejes.legend(facecolor="#202020", labelcolor=TEXTO_CLARO)
        self.figura.tight_layout()
        self.canvas.draw_idle()
        if self.on_x_selected is None:
            detalle_seleccion = (
                "Haga clic sobre la gráfica para consultar el valor de x."
            )
        else:
            detalle_seleccion = (
                "Haga clic sobre la gráfica para usar ese x como punto inicial "
                "x0 en Newton-Raphson."
            )
        detalle_raices = ""
        if self.marcar_raices_reales:
            detalle_raices = (
                f" Raíces reales aproximadas marcadas: "
                f"{len(raices_aproximadas)}."
            )
            if candidatas_sin_refinar:
                detalle_raices += (
                    f" Candidatos sin refinar: {candidatas_sin_refinar}."
                )
        self.estado.configure(
            text=(
                f"Gráfica actualizada con {datos['muestras']} muestras en "
                f"[{datos['rango'][0]:g}, {datos['rango'][1]:g}]. "
                f"Raíces candidatas (cambios de signo o ceros muestreados): "
                f"{len(raices_candidatas)}. "
                f"{detalle_raices}"
                f"{detalle_seleccion} La cantidad es una estimación por muestreo; "
                "puede omitir raíces tangenciales o muy cercanas. Los candidatos "
                "refinados requieren que la función sea continua en el intervalo."
                )
            if self.mostrar_estado_actualizacion
            else ""
        )
        self._texto_estado_grafica = self.estado.cget("text")
        if self.on_range_updated is not None:
            self.on_range_updated(datos["rango"])

    def _seleccionar_x(self, evento):
        if evento.inaxes is not self.ejes or evento.xdata is None:
            return
        self._x_seleccionado = float(evento.xdata)
        if self.on_x_selected is not None:
            self.on_x_selected(self._x_seleccionado)
        self.graficar()
        if self.mostrar_estado_actualizacion:
            if self.on_x_selected is None:
                self.estado.configure(
                    text=f"Coordenada seleccionada: x = {self._x_seleccionado:.12g}. "
                    + self._texto_estado_grafica
                )
            else:
                self.estado.configure(
                    text=f"x0 actualizado a {self._x_seleccionado:.12g}. "
                    + self._texto_estado_grafica
                )

    def al_cerrar(self):
        cerrar_teclado_matematico(self)
        self.destroy()

    def _estilizar_ejes(self):
        self.ejes.set_facecolor("#111111")
        self.ejes.tick_params(colors=TEXTO_CLARO)
        for borde in self.ejes.spines.values():
            borde.set_color("#777777")
