from core.ui.ctk_compat import ctk
from core.matriciales import visualizacionMatriciales as vis
from core.vectores import conversionesVectores as conv
from core.vectores import intercambio


class VistaIntercambio(ctk.CTkToplevel):
    """Interfaz para resolver tablas de intercambio de Leontief."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Tabla de Intercambio - Modelos de Leontief")
        self.geometry("980x780")
        self.master_matricial = master
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self.matriz_entries = []
        self.demanda_entries = []
        self.consumo_entries = []
        self.ingreso_entries = []
        self.crear_controles()
        self.crear_area_datos()
        self.generar_datos()

    def al_cerrar(self):
        self.master_matricial.deiconify()
        self.destroy()

    def crear_controles(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=15, pady=12)
        ctk.CTkLabel(frame, text="Sectores:").pack(side="left", padx=8)
        self.entry_dimension = ctk.CTkEntry(frame, width=60)
        self.entry_dimension.insert(0, "2")
        self.entry_dimension.pack(side="left", padx=5)
        self.menu_modelo = ctk.CTkOptionMenu(
            frame,
            values=["Modelo abierto", "Modelo cerrado"]
        )
        self.menu_modelo.pack(side="left", padx=10)
        ctk.CTkButton(
            frame,
            text="Generar tabla",
            command=self.generar_datos
        ).pack(side="left", padx=8)
        ctk.CTkButton(
            frame,
            text="Calcular",
            fg_color="green",
            hover_color="darkgreen",
            command=self.calcular
        ).pack(side="left", padx=8)
        self.menu_formato = ctk.CTkOptionMenu(
            frame,
            values=["Decimales", "Fracciones"]
        )
        self.menu_formato.pack(side="right", padx=8)

    def crear_area_datos(self):
        self.area_datos = ctk.CTkScrollableFrame(
            self,
            label_text="Coeficientes y demanda final"
        )
        self.area_datos.pack(fill="both", expand=True, padx=15, pady=5)
        self.texto_resultado = ctk.CTkTextbox(self, height=210)
        self.texto_resultado.pack(fill="both", padx=15, pady=12)

    def _limpiar_area(self):
        for widget in self.area_datos.winfo_children():
            widget.destroy()
        self.matriz_entries = []
        self.demanda_entries = []
        self.consumo_entries = []
        self.ingreso_entries = []

    def _crear_entrada(self, fila, columna, valor=""):
        entry = ctk.CTkEntry(self.area_datos, width=78, justify="center")
        entry.grid(row=fila, column=columna, padx=3, pady=3)
        if valor:
            entry.insert(0, valor)
        return entry

    def generar_datos(self):
        try:
            dimension = int(self.entry_dimension.get())
            if dimension <= 0:
                raise ValueError
        except ValueError:
            self.mostrar_resultado("ERROR: indique una cantidad positiva de sectores.")
            return

        self._limpiar_area()
        ctk.CTkLabel(
            self.area_datos,
            text="A: coeficientes de consumo entre sectores"
        ).grid(row=0, column=0, columnspan=dimension + 1, pady=8)
        ctk.CTkLabel(self.area_datos, text="Sector").grid(row=1, column=0)
        for columna in range(dimension):
            ctk.CTkLabel(self.area_datos, text=f"S{columna + 1}").grid(row=1, column=columna + 1)
        for fila in range(dimension):
            ctk.CTkLabel(self.area_datos, text=f"S{fila + 1}").grid(row=fila + 2, column=0)
            entradas_fila = []
            for columna in range(dimension):
                entradas_fila.append(self._crear_entrada(fila + 2, columna + 1, "0"))
            self.matriz_entries.append(entradas_fila)

        fila_demanda = dimension + 3
        ctk.CTkLabel(
            self.area_datos,
            text="D: demanda final externa"
        ).grid(row=fila_demanda, column=0, columnspan=dimension + 1, pady=8)
        for fila in range(dimension):
            ctk.CTkLabel(self.area_datos, text=f"D{fila + 1}").grid(row=fila_demanda + 1 + fila, column=0)
            self.demanda_entries.append(self._crear_entrada(fila_demanda + 1 + fila, 1, "0"))

        if self.menu_modelo.get() == "Modelo cerrado":
            fila_cerrado = fila_demanda + dimension + 2
            ctk.CTkLabel(
                self.area_datos,
                text="Sector hogares endógeno"
            ).grid(row=fila_cerrado, column=0, columnspan=dimension + 1, pady=8)
            for fila in range(dimension):
                ctk.CTkLabel(self.area_datos, text=f"Consumo S{fila + 1}").grid(row=fila_cerrado + 1 + fila, column=0)
                self.consumo_entries.append(self._crear_entrada(fila_cerrado + 1 + fila, 1, "0"))
            for columna in range(dimension):
                ctk.CTkLabel(self.area_datos, text=f"Ingreso S{columna + 1}").grid(row=fila_cerrado + 1 + dimension + columna, column=0)
                self.ingreso_entries.append(self._crear_entrada(fila_cerrado + 1 + dimension + columna, 1, "0"))

    def _leer_entrada(self, entry, nombre):
        valor = conv.convertir_a_decimal(entry.get().strip())
        if valor is None:
            raise ValueError(f"Valor inválido en {nombre}.")
        return valor

    def _leer_datos(self):
        dimension = len(self.matriz_entries)
        entradas = [
            [self._leer_entrada(entry, f"A{i + 1},{j + 1}") for j, entry in enumerate(fila)]
            for i, fila in enumerate(self.matriz_entries)
        ]
        demanda = [self._leer_entrada(entry, f"D{i + 1}") for i, entry in enumerate(self.demanda_entries)]
        return dimension, entradas, demanda

    def _formatear_matriz(self, matriz):
        formato = self.menu_formato.get()
        return vis.matriz_a_string(matriz, formato)

    def calcular(self):
        try:
            _, entradas, demanda = self._leer_datos()
            if self.menu_modelo.get() == "Modelo abierto":
                resultado = intercambio.resolver_modelo_abierto(entradas, demanda)
                descripcion = "X = (I - A)^-1 D, resuelto como (I - A)X = D"
            else:
                consumo = [self._leer_entrada(entry, f"consumo S{i + 1}") for i, entry in enumerate(self.consumo_entries)]
                ingreso = [self._leer_entrada(entry, f"ingreso S{i + 1}") for i, entry in enumerate(self.ingreso_entries)]
                resultado = intercambio.resolver_modelo_cerrado(entradas, demanda, consumo, ingreso)
                descripcion = "Sector hogares agregado como sector endógeno"

            salida = [
                "TABLA DE INTERCAMBIO - MODELO DE LEONTIEF",
                f"Modelo: {resultado['modelo'].capitalize()}",
                descripcion,
                "",
                "B = I - A",
                self._formatear_matriz(resultado["base"]),
                "",
                "Matriz aumentada [B | D]",
                self._formatear_matriz(resultado["aumentada"]),
                "",
            ]
            for descripcion_paso, matriz_paso in resultado["pasos"][1:]:
                salida.extend([f">> {descripcion_paso}", self._formatear_matriz(matriz_paso), ""])
            salida.extend([
                "Resultado de producción X:",
                self._formatear_matriz([[valor] for valor in resultado["produccion"]]),
            ])
            self.mostrar_resultado("\n".join(salida))
        except ValueError as error:
            self.mostrar_resultado(f"ERROR: {error}")

    def mostrar_resultado(self, texto):
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)
