"""Interfaz para particionar matrices y realizar operaciones por bloques."""

import csv
from fractions import Fraction
from tkinter import filedialog
from tkinter import TclError

from core.lineal.solucion import invertir_matriz_gauss_jordan
from core.matriciales import particiones_logica as logica
from core.matriciales import visualizacionMatriciales as vis
from core.ui.audio_manager import reproducir_sonido_error
from core.ui.ctk_compat import ctk
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_consola_resultado,
    estilo_menu_desplegable,
    estilo_panel_contenedor,
)


class VistaParticiones(ctk.CTkToplevel):
    """Ventana modal secundaria para matrices particionadas en bloques 2 x 2."""

    OPERACIONES = (
        "Suma por bloques",
        "Multiplicación por bloques",
        "Inversa triangular superior",
    )

    def __init__(self, master):
        super().__init__(master)
        self.master_matricial = master
        self.master_matricial.withdraw()
        self.transient(master)
        self.configure(fg_color=FONDO_CALCULADORA)
        self.title("Matrices Particionadas y Operaciones por Bloques")
        self.geometry("1120x850")
        self.minsize(850, 650)
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        self.entradas = {"A": [], "B": []}
        self.crear_interfaz()
        self.generar_datos()
        self.grab_set()

    def al_cerrar(self):
        try:
            self.grab_release()
        except TclError:
            pass
        self.master_matricial.deiconify()
        self.destroy()

    def crear_interfaz(self):
        encabezado = ctk.CTkFrame(self, **estilo_panel_contenedor())
        encabezado.pack(fill="x", padx=15, pady=(15, 8))
        ctk.CTkLabel(
            encabezado,
            text="Matrices Particionadas",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 22, "bold"),
        ).pack(side="left", padx=12, pady=10)
        ctk.CTkLabel(
            encabezado,
            text="Ingrese una matriz y defina los cortes de sus bloques",
            text_color=TEXTO_CLARO,
            font=("Consolas", 12),
        ).pack(side="right", padx=12)

        opciones = ctk.CTkFrame(self, **estilo_panel_contenedor())
        opciones.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(opciones, text="Operación:", text_color=TEXTO_CLARO).grid(
            row=0, column=0, padx=8, pady=8, sticky="w"
        )
        self.menu_operacion = ctk.CTkComboBox(
            opciones,
            values=list(self.OPERACIONES),
            width=240,
            command=self.cambiar_operacion,
            **estilo_menu_desplegable(),
        )
        self.menu_operacion.set(self.OPERACIONES[0])
        self.menu_operacion.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        ctk.CTkLabel(opciones, text="Formato:", text_color=TEXTO_CLARO).grid(
            row=0, column=2, padx=(18, 4), pady=8
        )
        self.menu_formato = ctk.CTkComboBox(
            opciones,
            values=["Fracciones", "Decimales"],
            width=140,
            **estilo_menu_desplegable(),
        )
        self.menu_formato.set("Fracciones")
        self.menu_formato.grid(row=0, column=3, padx=5, pady=8, sticky="w")
        ctk.CTkButton(
            opciones,
            text="Generar editores",
            **estilo_boton_secundario(),
            command=self.generar_datos,
        ).grid(row=0, column=4, padx=12, pady=8)

        self.configuracion = ctk.CTkFrame(self, fg_color="transparent")
        self.configuracion.pack(fill="x", padx=15, pady=4)
        self.configuracion.grid_columnconfigure(0, weight=1)
        self.configuracion.grid_columnconfigure(1, weight=1)
        self.controles = {}
        self._crear_controles_matriz("A", 0)
        self._crear_controles_matriz("B", 1)

        self.area_matrices = ctk.CTkScrollableFrame(
            self,
            label_text="Matrices de entrada",
            **estilo_panel_contenedor(),
        )
        self.area_matrices.pack(fill="both", expand=True, padx=15, pady=6)
        self.editor_a = ctk.CTkFrame(self.area_matrices, **estilo_panel_contenedor())
        self.editor_b = ctk.CTkFrame(self.area_matrices, **estilo_panel_contenedor())
        self.editor_a.pack(fill="x", padx=8, pady=8)
        self.editor_b.pack(fill="x", padx=8, pady=8)

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.pack(fill="x", padx=15, pady=4)
        ctk.CTkButton(
            acciones,
            text="Calcular",
            **estilo_boton_principal(),
            command=self.calcular,
        ).pack(side="left")

        self.texto_resultado = ctk.CTkTextbox(
            self,
            height=250,
            font=("Consolas", 12),
            **estilo_consola_resultado(),
        )
        self.texto_resultado.pack(fill="both", padx=15, pady=(4, 14))
        self.cambiar_operacion(self.OPERACIONES[0])

    def _crear_controles_matriz(self, nombre, columna):
        panel = ctk.CTkFrame(self.configuracion, **estilo_panel_contenedor())
        panel.grid(row=0, column=columna, sticky="ew", padx=4, pady=4)
        ctk.CTkLabel(
            panel, text=f"Configuración de matriz {nombre}", text_color=TEXTO_CLARO
        ).grid(row=0, column=0, columnspan=4, padx=6, pady=(6, 2), sticky="w")

        campos = (
            ("Filas", "filas", "2"),
            ("Columnas", "columnas", "2"),
            ("Corte horizontal", "corte_fila", "1"),
            ("Corte vertical", "corte_columna", "1"),
        )
        controles = {}
        for indice, (etiqueta, clave, valor_inicial) in enumerate(campos):
            fila = indice // 2 + 1
            col = (indice % 2) * 2
            ctk.CTkLabel(panel, text=etiqueta, text_color=TEXTO_CLARO).grid(
                row=fila, column=col, padx=(6, 3), pady=4, sticky="w"
            )
            entrada = ctk.CTkEntry(panel, width=58, justify="center")
            entrada.insert(0, valor_inicial)
            entrada.grid(row=fila, column=col + 1, padx=(2, 6), pady=4)
            controles[clave] = entrada

        boton_cargar = ctk.CTkButton(
            panel,
            text=f"Cargar CSV en {nombre}",
            **estilo_boton_secundario(),
            command=lambda etiqueta=nombre: self.cargar_csv(etiqueta),
        )
        boton_cargar.grid(row=3, column=0, columnspan=4, padx=6, pady=(4, 8))
        controles["panel"] = panel
        self.controles[nombre] = controles

    def _leer_configuracion(self, nombre):
        controles = self.controles[nombre]
        try:
            filas = int(controles["filas"].get().strip())
            columnas = int(controles["columnas"].get().strip())
            corte_fila = int(controles["corte_fila"].get().strip())
            corte_columna = int(controles["corte_columna"].get().strip())
        except ValueError as error:
            raise ValueError(
                f"Dimensiones y cortes de {nombre} deben ser enteros."
            ) from error
        if filas <= 0 or columnas <= 0:
            raise ValueError(f"Las dimensiones de {nombre} deben ser positivas.")
        return filas, columnas, corte_fila, corte_columna

    def generar_datos(self):
        try:
            filas_a, columnas_a, corte_fila_a, corte_columna_a = (
                self._leer_configuracion("A")
            )
            logica._validar_cortes(
                filas_a, columnas_a, corte_fila_a, corte_columna_a
            )
            if self.menu_operacion.get() != "Inversa triangular superior":
                filas_b, columnas_b, corte_fila_b, corte_columna_b = (
                    self._leer_configuracion("B")
                )
                logica._validar_cortes(
                    filas_b, columnas_b, corte_fila_b, corte_columna_b
                )
        except ValueError as error:
            self.mostrar_resultado(f"ERROR: {error}")
            return

        self._crear_editor("A", filas_a, columnas_a)
        if self.menu_operacion.get() != "Inversa triangular superior":
            self._crear_editor("B", filas_b, columnas_b)
        self.mostrar_resultado(
            "Introduzca las matrices y verifique los cortes de cada partición."
        )

    def _crear_editor(self, nombre, filas, columnas, valores=None):
        panel = self.editor_a if nombre == "A" else self.editor_b
        for widget in panel.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            panel,
            text=f"Matriz {nombre}  [{filas} × {columnas}]",
            text_color=TEXTO_CLARO,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=8, pady=(6, 2))
        cuadrilla = ctk.CTkFrame(panel, fg_color="transparent")
        cuadrilla.pack(anchor="w", padx=6, pady=(0, 8))
        entradas = []
        for fila in range(filas):
            entradas_fila = []
            for columna in range(columnas):
                entrada = ctk.CTkEntry(cuadrilla, width=72, justify="center")
                entrada.grid(row=fila, column=columna, padx=2, pady=2)
                if valores is not None:
                    entrada.insert(0, str(valores[fila][columna]))
                entradas_fila.append(entrada)
            entradas.append(entradas_fila)
        self.entradas[nombre] = entradas

    def _establecer_control(self, nombre, clave, valor):
        entrada = self.controles[nombre][clave]
        entrada.delete(0, "end")
        entrada.insert(0, str(valor))

    def cargar_csv(self, nombre):
        ruta = filedialog.askopenfilename(
            title=f"Cargar matriz {nombre}",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivos de texto", "*.txt")],
        )
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
                muestra = archivo.read(4096)
                archivo.seek(0)
                primera_linea = muestra.splitlines()[0] if muestra.splitlines() else ""
                delimitador = (
                    ";"
                    if ";" in primera_linea and "," not in primera_linea
                    else ","
                )
                filas = list(csv.reader(archivo, delimiter=delimitador))
            matriz = [
                [self._convertir_numero(valor) for valor in fila]
                for fila in filas if fila
            ]
            filas_matriz, columnas_matriz = logica._validar_matriz(
                matriz, f"La matriz {nombre} cargada"
            )
        except (OSError, csv.Error, ValueError) as error:
            self.mostrar_resultado(f"ERROR al cargar matriz {nombre}: {error}")
            return

        self._establecer_control(nombre, "filas", filas_matriz)
        self._establecer_control(nombre, "columnas", columnas_matriz)
        for clave, dimension in (
            ("corte_fila", filas_matriz),
            ("corte_columna", columnas_matriz),
        ):
            try:
                corte = int(self.controles[nombre][clave].get())
            except ValueError:
                corte = 0
            if not 0 < corte < dimension:
                self._establecer_control(nombre, clave, max(1, dimension // 2))
        self._crear_editor(nombre, filas_matriz, columnas_matriz, matriz)
        self.mostrar_resultado(
            f"Matriz {nombre} cargada. Compruebe sus cortes antes de calcular."
        )

    @staticmethod
    def _convertir_numero(texto):
        valor = texto.strip()
        if not valor:
            raise ValueError("El archivo contiene una celda vacía.")
        try:
            return Fraction(valor)
        except (ValueError, ZeroDivisionError) as error:
            raise ValueError(f"El valor '{valor}' no es numérico.") from error

    def _leer_matriz(self, nombre):
        matriz = []
        for indice_fila, entradas_fila in enumerate(self.entradas[nombre]):
            fila = []
            for indice_columna, entrada in enumerate(entradas_fila):
                try:
                    fila.append(self._convertir_numero(entrada.get()))
                except ValueError as error:
                    raise ValueError(
                        f"{nombre}[{indice_fila + 1},{indice_columna + 1}]: {error}"
                    ) from error
            matriz.append(fila)
        filas_esperadas, columnas_esperadas, _, _ = self._leer_configuracion(nombre)
        filas_leidas, columnas_leidas = logica._validar_matriz(
            matriz, f"La matriz {nombre}"
        )
        if (filas_leidas, columnas_leidas) != (
            filas_esperadas,
            columnas_esperadas,
        ):
            raise ValueError(
                f"La matriz {nombre} tiene dimensiones {filas_leidas} × "
                f"{columnas_leidas}; genere de nuevo los editores para "
                f"{filas_esperadas} × {columnas_esperadas}."
            )
        return matriz

    def _particionar(self, nombre, matriz):
        _, _, corte_fila, corte_columna = self._leer_configuracion(nombre)
        return logica.particionar_matriz(matriz, corte_fila, corte_columna)

    def _mostrar_bloques(self, titulo, bloques, formato):
        lineas = [titulo]
        for nombre in ("A11", "A12", "A21", "A22"):
            lineas.extend([
                f"{nombre}:",
                vis.matriz_a_string(bloques[nombre], formato),
            ])
        return "\n".join(lineas)

    def calcular(self):
        try:
            operacion = self.menu_operacion.get()
            formato = self.menu_formato.get()
            matriz_a = self._leer_matriz("A")
            bloques_a = self._particionar("A", matriz_a)
            salida = [self._mostrar_bloques("PARTICIÓN DE A", bloques_a, formato), ""]

            if operacion == "Inversa triangular superior":
                if any(valor != 0 for fila in bloques_a["A21"] for valor in fila):
                    raise ValueError(
                        "La inversa por bloques requiere que A21 sea una matriz de ceros."
                    )
                resultado = logica.inversa_triangular_bloques(
                    bloques_a["A11"],
                    bloques_a["A12"],
                    bloques_a["A22"],
                    invertir_matriz_gauss_jordan,
                )
                salida.extend([
                    self._mostrar_bloques("BLOQUES DE A⁻¹", resultado, formato),
                    "",
                    "MATRIZ INVERSA REENSAMBLADA:",
                    vis.matriz_a_string(
                        logica.reensamblar_bloques(resultado), formato
                    ),
                ])
            else:
                matriz_b = self._leer_matriz("B")
                bloques_b = self._particionar("B", matriz_b)
                salida.extend([
                    self._mostrar_bloques("PARTICIÓN DE B", bloques_b, formato),
                    "",
                ])
                if operacion == "Suma por bloques":
                    resultado = logica.suma_bloques(bloques_a, bloques_b)
                    nombre_resultado = "A + B"
                else:
                    resultado = logica.multiplicacion_bloques(bloques_a, bloques_b)
                    nombre_resultado = "A × B"
                salida.extend([
                    self._mostrar_bloques(f"BLOQUES DE {nombre_resultado}", resultado, formato),
                    "",
                    f"MATRIZ {nombre_resultado} REENSAMBLADA:",
                    vis.matriz_a_string(
                        logica.reensamblar_bloques(resultado), formato
                    ),
                ])
            self.mostrar_resultado("\n".join(salida))
        except ValueError as error:
            self.mostrar_resultado(f"ERROR: {error}")

    def cambiar_operacion(self, operacion=None):
        es_inversa = (operacion or self.menu_operacion.get()) == (
            "Inversa triangular superior"
        )
        panel_b = self.controles["B"]["panel"]
        if es_inversa:
            panel_b.grid_remove()
            self.editor_b.pack_forget()
        else:
            panel_b.grid()
            self.editor_b.pack(fill="x", padx=8, pady=8)

    def mostrar_resultado(self, texto):
        reproducir_sonido_error(self, texto)
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)
