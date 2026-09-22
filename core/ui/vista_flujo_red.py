from core.ui.ctk_compat import ctk
from core.matriciales import visualizacionMatriciales as vis
from core.vectores import conversionesVectores as conv
from core.vectores import flujo_red
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_menu_desplegable,
    estilo_panel_contenedor,
)


class VistaFlujoRed(ctk.CTkToplevel):
    """Interfaz para resolver balances de flujo en redes dirigidas."""

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self.title("Análisis de Flujo en Redes")
        self.geometry("980x780")
        self.master_matricial = master
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self.ramas_entries = []
        self.balance_entries = []
        self.crear_controles()
        self.crear_area_datos()
        self.generar_datos()

    def al_cerrar(self):
        self.master_matricial.deiconify()
        self.destroy()

    def crear_controles(self):
        frame = ctk.CTkFrame(self, **estilo_panel_contenedor())
        frame.pack(fill="x", padx=15, pady=12)
        ctk.CTkLabel(frame, text="Nodos:", text_color=TEXTO_CLARO).pack(side="left", padx=5)
        self.entry_nodos = ctk.CTkEntry(frame, width=55)
        self.entry_nodos.insert(0, "3")
        self.entry_nodos.pack(side="left", padx=5)
        ctk.CTkLabel(frame, text="Ramas:", text_color=TEXTO_CLARO).pack(side="left", padx=5)
        self.entry_ramas = ctk.CTkEntry(frame, width=55)
        self.entry_ramas.insert(0, "3")
        self.entry_ramas.pack(side="left", padx=5)
        ctk.CTkButton(
            frame, text="Generar red", **estilo_boton_secundario(), command=self.generar_datos
        ).pack(side="left", padx=8)
        ctk.CTkButton(
            frame, text="Calcular", **estilo_boton_principal(),
            command=self.calcular
        ).pack(side="left", padx=8)
        self.menu_formato = ctk.CTkComboBox(
            frame, values=["Decimales", "Fracciones"],
            **estilo_menu_desplegable()
        )
        self.menu_formato.set("Decimales")
        self.menu_formato.pack(side="right", padx=8)

    def crear_area_datos(self):
        self.area_datos = ctk.CTkScrollableFrame(
            self, label_text="Ramas y balances de conservación", **estilo_panel_contenedor()
        )
        self.area_datos.pack(fill="both", expand=True, padx=15, pady=5)
        self.texto_resultado = ctk.CTkTextbox(self, height=220, **estilo_consola_resultado())
        self.texto_resultado.pack(fill="both", padx=15, pady=12)

    def _limpiar_area(self):
        for widget in self.area_datos.winfo_children():
            widget.destroy()
        self.ramas_entries = []
        self.balance_entries = []

    def _entrada(self, fila, columna, valor=""):
        entry = ctk.CTkEntry(self.area_datos, width=90, justify="center")
        entry.grid(row=fila, column=columna, padx=5, pady=4)
        if valor:
            entry.insert(0, valor)
        return entry

    def generar_datos(self):
        try:
            nodos = int(self.entry_nodos.get())
            ramas = int(self.entry_ramas.get())
            if nodos <= 0 or ramas <= 0:
                raise ValueError
        except ValueError:
            self.mostrar_resultado("ERROR: nodos y ramas deben ser enteros positivos.")
            return

        self._limpiar_area()
        encabezados = ["Rama", "Origen", "Destino"]
        for columna, texto in enumerate(encabezados):
            ctk.CTkLabel(self.area_datos, text=texto, text_color=TEXTO_CLARO).grid(
                row=0, column=columna, padx=5, pady=5
            )
        ctk.CTkLabel(
            self.area_datos,
            text="El flujo se toma positivo en el sentido origen -> destino.",
            text_color=TEXTO_CLARO
        ).grid(row=0, column=3, columnspan=2, padx=8)

        for indice in range(ramas):
            ctk.CTkLabel(self.area_datos, text=f"f{indice + 1}", text_color=TEXTO_CLARO).grid(
                row=indice + 1, column=0, padx=5, pady=4
            )
            origen = self._entrada(indice + 1, 1, str((indice % nodos) + 1))
            destino = self._entrada(indice + 1, 2, str(((indice + 1) % nodos) + 1))
            self.ramas_entries.append((origen, destino))

        fila_balance = ramas + 3
        ctk.CTkLabel(
            self.area_datos,
            text="Balance externo por nodo: salidas - entradas = balance",
            text_color=TEXTO_CLARO
        ).grid(row=fila_balance, column=0, columnspan=3, pady=8)
        for indice in range(nodos):
            ctk.CTkLabel(self.area_datos, text=f"Nodo {indice + 1}", text_color=TEXTO_CLARO).grid(
                row=fila_balance + indice + 1, column=0, padx=5, pady=4
            )
            self.balance_entries.append(
                self._entrada(fila_balance + indice + 1, 1, "0")
            )

    def _leer(self, entry, nombre):
        valor = conv.convertir_a_decimal(entry.get().strip())
        if valor is None:
            raise ValueError(f"Valor inválido en {nombre}.")
        return valor

    def _leer_red(self):
        nodos = int(self.entry_nodos.get())
        ramas = []
        for indice, (origen_entry, destino_entry) in enumerate(self.ramas_entries):
            origen = int(self._leer(origen_entry, f"origen de f{indice + 1}"))
            destino = int(self._leer(destino_entry, f"destino de f{indice + 1}"))
            ramas.append((origen, destino))
        balances = [
            self._leer(entry, f"balance del nodo {indice + 1}")
            for indice, entry in enumerate(self.balance_entries)
        ]
        return nodos, ramas, balances

    def _matriz(self, matriz):
        return vis.matriz_a_string(matriz, self.menu_formato.get())

    def calcular(self):
        try:
            nodos, ramas, balances = self._leer_red()
            resultado = flujo_red.resolver_flujo(nodos, ramas, balances)
            nombres = [f"f{indice + 1}" for indice in range(len(ramas))]
            salida = [
                "ANÁLISIS DE FLUJO DE RED",
                "",
                "Convención: salidas - entradas = balance",
                "",
                "Matriz de incidencia C:",
                self._matriz(resultado["incidencia"]),
                "",
                "Sistema aumentado [C | b]:",
                self._matriz(resultado["aumentada"]),
                "",
            ]
            for descripcion, matriz_paso in resultado["pasos"][1:]:
                salida.extend([f">> {descripcion}", self._matriz(matriz_paso), ""])
            salida.extend([
                f"Clasificación: {resultado['tipo']}",
                "Pivotes: " + ", ".join(
                    nombres[indice] for indice in resultado["pivotes"]
                ) if resultado["pivotes"] else "Pivotes: ninguno",
            ])
            if resultado["tipo"] == "incompatible":
                salida.append("No existe un flujo que cumpla todos los balances.")
            else:
                if resultado["variables_libres"]:
                    salida.append(
                        "Variables libres: " + ", ".join(
                            nombres[indice] for indice in resultado["variables_libres"]
                        )
                    )
                salida.append("Flujos:")
                salida.extend(
                    f"  {nombre} ({origen} -> {destino}) = "
                    f"{self._formatear(resultado['flujos'][indice])}"
                    for indice, (nombre, (origen, destino)) in enumerate(zip(nombres, ramas))
                )
            self.mostrar_resultado("\n".join(salida))
        except (ValueError, TypeError) as error:
            self.mostrar_resultado(f"ERROR: {error}")

    def _formatear(self, valor):
        if self.menu_formato.get() == "Fracciones":
            return conv.convertir_a_fraccion(valor)
        return f"{valor:.2f}"

    def mostrar_resultado(self, texto):
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)
