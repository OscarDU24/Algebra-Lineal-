import tkinter as tk
from tkinter import messagebox
import ctypes
from pathlib import Path
from PIL import Image, ImageTk

from core.ui import preferencias

class Dashboard:
    def __init__(self, root, audio_manager=None, al_volver_inicio=None):
        self.root = root
        self.audio_manager = audio_manager or getattr(root, "audio_manager", None)
        self.al_volver_inicio = al_volver_inicio
        self.fuentes_registradas = []
        self.fuente_titulo = "Segoe UI"
        self.fuente_tarjetas = "Segoe UI"
        self.fuente_menu = "Segoe UI"
        self.ventana_activa = None
        self.tarjetas = []
        self._tarjeta_resaltada = None
        self._bienvenida_dashboard = None
        self._recorrido_activo = False
        self._recorrido_estado = None
        self._recorrido_ventana = None
        self._recorrido_panel = None
        self._recorrido_copiado = False
        self._recorrido_calculado = False
        self._recorrido_zoom = False
        self._recorrido_resultado = None
        self._recorrido_volviendo_anterior = False
        self._resize_job = None
        self.ultimo_modulo = preferencias.cargar()["ultimo_modulo_utilizado"]
        self.registrar_fuentes()
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        # El canvas permite conservar las transparencias del borde decorativo.
        # Mismo título que asigna main.py, para que la ventana no cambie de nombre.
        self.root.title("HeyAlgb · Álgebra Lineal")

        # ==========================================
        # INYECCIÓN DEL FONDO DECORATIVO (CAPA 0)
        # ==========================================
        
        try:
            ruta_fondo = Path(__file__).resolve().parents[1] / "assets" / "BordesFinales.png"
            self.fondo = Image.open(ruta_fondo).convert("RGBA")
            self.bg_image = ImageTk.PhotoImage(self.fondo)
            self.fondo_item = None
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el fondo decorativo: {e}")
            self.fondo = None
            self.bg_image = None

        self.contenido = tk.Canvas(
            self.root,
            width=980,
            height=780,
            bg="#ffffff",
            highlightthickness=0,
            borderwidth=0,
        )
        self.contenido.pack(expand=True, fill="both")
        if self.bg_image is not None:
            self.fondo_item = self.contenido.create_image(0, 0, image=self.bg_image, anchor="nw")


        
        # ==========================================
        # BARRA DE MENÚ SUPERIOR
        # ==========================================
        self.menu_bar = tk.Menu(
            self.root,
            font=(self.fuente_menu, 11),
            bg="#ffffff",
            fg="#000000",
            activebackground="#8f0000",
            activeforeground="#ffffff"
        )
        
        self.menu_archivo = tk.Menu(
            self.menu_bar,
            tearoff=0,
            font=(self.fuente_menu, 11),
            bg="#ffffff",
            fg="#000000",
            activebackground="#8f0000",
            activeforeground="#ffffff"
        )
        self.menu_archivo.add_command(label="Salir", command=self.cerrar_aplicacion)
        self.menu_bar.add_cascade(label="Archivo", menu=self.menu_archivo)
        
        self.menu_ayuda = tk.Menu(
            self.menu_bar,
            tearoff=0,
            font=(self.fuente_menu, 11),
            bg="#ffffff",
            fg="#000000",
            activebackground="#8f0000",
            activeforeground="#ffffff"
        )
        self.menu_ayuda.add_command(label="Guía de bienvenida", command=self.abrir_guia)
        self.menu_ayuda.add_command(
            label="Cómo usar HeyAlgb y atajos de teclado", command=self.abrir_ayuda_general
        )
        self.menu_ayuda.add_separator()
        self.menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        self.menu_bar.add_cascade(label="Ayuda", menu=self.menu_ayuda)
        
        self.root.config(menu=self.menu_bar)

        # ==========================================
        # TÍTULO PRINCIPAL
        # ==========================================
        self.titulo_item = self.contenido.create_text(
            0,
            0,
            text="Seleccione su sistema",
            font=(self.fuente_titulo, 75),
            fill="#fe0000",
        )

        # ==========================================
        # CREACIÓN DE TARJETAS
        # ==========================================
        # Fila 0
        self.crear_tarjeta(0, 0, "Operaciones Básicas de Matrices", self.abrir_matrices, "MatrIndvICON.png")
        self.crear_tarjeta(0, 1, "Operaciones Vectoriales", self.abrir_vectores, "EcVectorialesCON.png")
        self.crear_tarjeta(0, 2, "Ecuaciones matriciales", self.abrir_ec_matriciales, "EcMatriciaIesCON.png")

        # Fila 1
        self.crear_tarjeta(1, 0, "Sistemas de Ecuaciones Lineales", self.abrir_sistemas, "EcLinealICON.png")
        self.crear_tarjeta(1, 1, "Evaluación de Límites", self.abrir_limites, "LimitesICON.png")
        self.crear_tarjeta(1, 2, "Sistemas numéricos", self.abrir_sistemas_numericos, "SisNumICON.png")
        self.crear_tarjeta(
            2, 2,
            "Determinantes y Factorización LU",
            self.abrir_determinantes,
            "DeterminantesICON.png",
        )
        self.crear_tarjeta(
            2,
            1,
            "Métodos Numéricos",
            self.abrir_metodos_numericos,
            "metNumericosICON.png",
        )

        # ==========================================
        # BARRA DE ESTADO INFERIOR
        # ==========================================
        self.lbl_estado = tk.Label(
            self.contenido,
            text=f"Último módulo utilizado: {self.ultimo_modulo}",
            font=(self.fuente_menu, 14),
            bg="#dcdcdc",
            fg="#333333",
            anchor="center",
            pady=8,
        )
        self.estado_item = self.contenido.create_window(
            0, 0, window=self.lbl_estado, width=980, height=36
        )
        self.var_musica = tk.BooleanVar(
            master=self.root,
            value=self.audio_manager.musica_habilitada if self.audio_manager else False
        )
        self.var_efectos = tk.BooleanVar(
            master=self.root,
            value=getattr(self.audio_manager, "efectos_habilitados", True)
            if self.audio_manager else False
        )
        # Ambos controles se guardan en las preferencias del usuario y muestran
        # un borde al recibir el foco con Tab.
        self.panel_audio = tk.Frame(self.contenido, bg="#ffffff")
        estilo_casilla = dict(
            bg="#ffffff",
            fg="#111111",
            activebackground="#ffffff",
            selectcolor="#ffffff",
            font=(self.fuente_menu, 12),
            bd=0,
            highlightthickness=1,
            highlightbackground="#ffffff",
            highlightcolor="#fe0000",
        )
        self.control_musica = tk.Checkbutton(
            self.panel_audio,
            text="Música de fondo",
            variable=self.var_musica,
            command=self._alternar_musica,
            **estilo_casilla,
        )
        self.control_musica.pack(side="left", padx=(0, 8))
        self.control_efectos = tk.Checkbutton(
            self.panel_audio,
            text="Efectos de sonido",
            variable=self.var_efectos,
            command=self._alternar_efectos,
            **estilo_casilla,
        )
        self.control_efectos.pack(side="left")
        self.musica_item = self.contenido.create_window(
            0, 0, window=self.panel_audio, anchor="nw"
        )
        self.boton_inicio = tk.Button(
            self.contenido,
            text="← Volver al inicio",
            font=(self.fuente_menu, 12, "bold"),
            bg="#ffffff",
            fg="#000000",
            activebackground="#e2e2e2",
            activeforeground="#000000",
            bd=1,
            highlightthickness=1,
            highlightbackground="#ffffff",
            highlightcolor="#fe0000",
            cursor="hand2",
            command=self.volver_al_inicio,
        )
        self.volver_item = self.contenido.create_window(
            0, 0, window=self.boton_inicio, anchor="ne"
        )
        self.contenido.bind("<Configure>", self._programar_reorganizacion)
        self.contenido.bind(
            "<Destroy>", self._cancelar_reorganizacion, add="+"
        )
        self._reorganizar_elementos(980, 780)

    def crear_tarjeta(self, fila, columna, texto, comando, nombre_icono):
        """
        Crea una tarjeta con el icono de la calculadora y su etiqueta.
        """
        # Contenedor principal de la tarjeta con borde externo
        card_frame = tk.Frame(
            self.contenido,
            bg="#ffffff",
            width=255,
            height=220,
            highlightbackground="#000000",
            highlightthickness=1
        )
        ventana_item = self.contenido.create_window(
            0,
            0,
            window=card_frame,
            width=255,
            height=220,
        )
        card_frame.grid_propagate(False)
        card_frame.configure(cursor="hand2")

        preview_frame = tk.Frame(
            card_frame,
            bg="#ffffff",
            width=210,
            height=145,
        )
        preview_frame.pack(padx=8, pady=(8, 4))
        preview_frame.pack_propagate(False)

        imagen_original = None
        imagen_icono = None
        if nombre_icono is None:
            texto_icono = "det(A)\nLU"
        else:
            ruta_icono = Path(__file__).resolve().parents[1] / "assets" / nombre_icono
            try:
                imagen_original = Image.open(ruta_icono).convert("RGBA")
                imagen_icono = ImageTk.PhotoImage(
                    imagen_original.resize((132, 132), Image.Resampling.LANCZOS)
                )
                self.iconos = getattr(self, "iconos", [])
                self.iconos.append(imagen_icono)
                texto_icono = ""
            except Exception as error:
                print(f"Advertencia: No se pudo cargar el icono {nombre_icono}: {error}")
                texto_icono = "Icono no disponible"

        boton_icono = tk.Button(
            preview_frame,
            image=imagen_icono,
            text=texto_icono,
            fg="#fe0000",
            bg="#ffffff",
            activebackground="#ffffff",
            activeforeground="#fe0000",
            bd=0,
            # Borde rojo visible cuando la tarjeta recibe el foco con Tab.
            highlightthickness=2,
            highlightbackground="#ffffff",
            highlightcolor="#fe0000",
            takefocus=1,
            cursor="hand2",
            command=lambda: self._activar_modulo(comando, texto)
        )
        boton_icono.bind("<Return>", lambda _e: self._activar_modulo(comando, texto))
        boton_icono.bind("<KP_Enter>", lambda _e: self._activar_modulo(comando, texto))
        if self.audio_manager is not None:
            self.audio_manager.registrar_control_sonido(boton_icono, "interfaces")
        boton_icono.pack(expand=True, fill="both")

        # Etiqueta inferior con el nombre del módulo
        lbl_nombre = tk.Label(
            card_frame,
            text=texto,
            font=(self.fuente_tarjetas, 14),
            bg="#ffffff",
            fg="#000000",
            justify="center",
            pady=12
        )
        lbl_nombre.pack(side="bottom", fill="x")
        if self.audio_manager is not None:
            self.audio_manager.registrar_control_sonido(lbl_nombre, "interfaces")

        def seleccionar(event=None):
            es_tutorial = self._tarjeta_resaltada is card_frame
            card_frame.configure(
                highlightbackground="#fe0000",
                highlightthickness=4 if es_tutorial else 2,
            )

        def deseleccionar(event=None):
            es_tutorial = self._tarjeta_resaltada is card_frame
            card_frame.configure(
                highlightbackground="#fe0000" if es_tutorial else "#000000",
                highlightthickness=4 if es_tutorial else 1,
            )

        def activar(event=None):
            self._activar_modulo(comando, texto)

        for widget in (card_frame, preview_frame, lbl_nombre):
            widget.bind("<Enter>", seleccionar, add="+")
            widget.bind("<Leave>", deseleccionar, add="+")
        boton_icono.bind("<FocusIn>", seleccionar, add="+")
        boton_icono.bind("<FocusOut>", deseleccionar, add="+")

        lbl_nombre.bind("<Button-1>", activar)
        self.tarjetas.append({
            "row": fila,
            "column": columna,
            "window": ventana_item,
            "frame": card_frame,
            "preview": preview_frame,
            "button": boton_icono,
            "icon": imagen_original,
            "text": texto,
        })

    def _activar_modulo(self, comando, nombre=None):
        if self._recorrido_activo and nombre != "Métodos Numéricos":
            self.lbl_estado.config(
                text="El recorrido activo usa únicamente Métodos Numéricos."
            )
            return
        comando()

    def _alternar_musica(self):
        if self.audio_manager is not None:
            self.audio_manager.establecer_musica_habilitada(self.var_musica.get())
        preferencias.guardar(musica_habilitada=bool(self.var_musica.get()))

    def _alternar_efectos(self):
        if self.audio_manager is not None:
            self.audio_manager.establecer_efectos_habilitados(self.var_efectos.get())
        preferencias.guardar(efectos_habilitados=bool(self.var_efectos.get()))

    def abrir_guia(self):
        if self._recorrido_activo or self.ventana_activa is not None:
            return
        from core.ui.bienvenida import abrir_bienvenida

        self.contenido.pack_forget()
        self.root.config(menu="")
        self._bienvenida_dashboard = abrir_bienvenida(
            self.root,
            al_comenzar=lambda: self._cerrar_bienvenida_dashboard(True),
            al_omitir=lambda: self._cerrar_bienvenida_dashboard(False),
        )

    def _cerrar_bienvenida_dashboard(self, comenzar_recorrido):
        self._bienvenida_dashboard = None
        self.root.config(menu=self.menu_bar)
        self.contenido.pack(expand=True, fill="both")
        if comenzar_recorrido:
            self.iniciar_recorrido()

    def iniciar_recorrido(self):
        if self._recorrido_activo or self.ventana_activa is not None:
            return False
        from core.ui.bienvenida import PanelRecorrido

        self._recorrido_activo = True
        self._recorrido_copiado = False
        self._recorrido_calculado = False
        self._recorrido_zoom = False
        self._recorrido_resultado = None
        self.root.config(menu="")
        self._recorrido_panel = PanelRecorrido(
            self.root,
            anterior=self.recorrido_anterior,
            salir=self.salir_recorrido,
            siguiente=self.recorrido_siguiente,
        )
        self._mostrar_layout_recorrido()
        self._resaltar_tarjeta("Métodos Numéricos")
        self._mostrar_paso_recorrido("tarjeta")
        return True

    def _mostrar_layout_recorrido(self):
        self.contenido.pack_forget()
        if self._recorrido_panel is not None:
            self._recorrido_panel.pack(
                side="right", fill="y", padx=(0, 12), pady=12
            )
        self.contenido.pack(side="left", expand=True, fill="both")

    def _mostrar_layout_normal(self, mostrar_fin=False):
        self.contenido.pack_forget()
        if self._recorrido_panel is not None:
            if mostrar_fin:
                self._recorrido_panel.pack(
                    side="right", fill="y", padx=(0, 12), pady=12
                )
                self.contenido.pack(side="left", expand=True, fill="both")
                self._recorrido_panel.mostrar_fin()
                return
            self._recorrido_panel.destroy()
            self._recorrido_panel = None
        self.contenido.pack(expand=True, fill="both")

    def _resaltar_tarjeta(self, nombre):
        self._tarjeta_resaltada = None
        for tarjeta in self.tarjetas:
            coincide = tarjeta["text"] == nombre
            if coincide:
                self._tarjeta_resaltada = tarjeta["frame"]
            tarjeta["frame"].configure(
                highlightbackground="#fe0000" if coincide else "#000000",
                highlightthickness=4 if coincide else 1,
            )

    def _contenido_paso_recorrido(self, estado):
        pasos = {
            "tarjeta": (
                1,
                "Métodos Numéricos",
                "La tarjeta resaltada abre la herramienta real que usaremos. "
                "Haz clic en «Métodos Numéricos» para continuar.",
                False,
                False,
            ),
            "ejemplo": (
                2,
                "Cargar Ej. 1",
                "En la barra superior, abre «Cargar ejemplo...» y elige «Ej. 1». "
                "Se llenarán f(x), a, b y la tolerancia; todavía no se calcula.",
                True,
                False,
            ),
            "campos": (
                3,
                "Revisar datos iniciales",
                "Los campos reales muestran f(x) = x**3 - 4*x - 9, a = 2, b = 3 "
                "y tolerancia = 1e-6. f(x) admite la sintaxis de la calculadora; "
                "a y b son los extremos del intervalo.",
                True,
                True,
            ),
            "calcular": (
                4,
                "Ejecutar Biseccionar",
                (
                    "Pulsa el botón real «Biseccionar». Se ejecutará el solver "
                    "existente y se mostrará la tabla. Si los datos son inválidos, "
                    "corrígelos: el recorrido no avanzará."
                    if not self._recorrido_calculado
                    else "El cálculo ya terminó correctamente. Pulsa «Siguiente» "
                    "para revisar el resultado; no necesitas volver a calcular."
                ),
                True,
                self._recorrido_calculado,
            ),
            "resultado": (
                5,
                "Leer el resultado",
                self._resumen_resultado_recorrido(),
                True,
                True,
            ),
            "copiar": (
                6,
                "Copiar el informe",
                "Pulsa «Copiar resultados» sobre la consola. La acción copiará "
                "el procedimiento y la tabla al portapapeles.",
                True,
                self._recorrido_copiado,
            ),
            "zoom": (
                7,
                "Probar el zoom",
                "Pulsa «+» en los controles «Zoom» de la consola para ampliar "
                "el texto. El porcentaje cambia sin recalcular el resultado.",
                True,
                self._recorrido_zoom,
            ),
            "volver": (
                8,
                "Volver al menú",
                "Pulsa el botón real «← Volver al menú» de la barra superior "
                "para regresar al Dashboard y terminar el recorrido.",
                True,
                False,
            ),
        }
        paso, titulo, descripcion, anterior, siguiente = pasos[estado]
        return {
            "paso": paso,
            "total": 8,
            "titulo": titulo,
            "descripcion": descripcion,
            "anterior": anterior,
            "siguiente": siguiente,
        }

    def _resumen_resultado_recorrido(self):
        resultado = self._recorrido_resultado
        if not resultado:
            return (
                "El motor de Bisección mostrará la aproximación, el residuo, "
                "el criterio de parada y la tabla de iteraciones."
            )
        residuo = abs(resultado["f_raiz"])
        return (
            f"El motor obtuvo x ≈ {resultado['raiz']:.12g} después de "
            f"{resultado['iteraciones']} iteraciones, con |f(x)| = "
            f"{residuo:.8e}. El criterio de parada fue "
            f"«{resultado['criterio_paro']}». Revisa la tabla de iteraciones "
            "en la consola real."
        )

    def _mostrar_paso_recorrido(self, estado):
        if not self._recorrido_activo:
            return
        self._recorrido_estado = estado
        contenido = self._contenido_paso_recorrido(estado)
        if self._recorrido_ventana is not None:
            try:
                if self._recorrido_ventana.winfo_exists():
                    self._recorrido_ventana.aplicar_paso_recorrido(
                        estado, contenido
                    )
                    return
            except tk.TclError:
                self._recorrido_ventana = None
        if self._recorrido_panel is not None:
            self._recorrido_panel.mostrar(
                contenido["paso"],
                contenido["total"],
                contenido["titulo"],
                contenido["descripcion"],
                anterior_habilitado=contenido["anterior"],
                siguiente_habilitado=contenido["siguiente"],
                siguiente_texto=contenido.get("siguiente_texto", "Siguiente →"),
            )

    def vista_recorrido_abierta(self, ventana):
        if not self._recorrido_activo:
            return
        self._recorrido_ventana = ventana
        if self._recorrido_panel is not None:
            self._recorrido_panel.pack_forget()
        self._mostrar_paso_recorrido("ejemplo")

    def ejemplo_cargado(self):
        if self._recorrido_activo and self._recorrido_estado == "ejemplo":
            self._mostrar_paso_recorrido("campos")

    def ejemplo_no_esperado(self):
        if self._recorrido_activo:
            self._mostrar_paso_recorrido("ejemplo")
            panel = self._recorrido_ventana.panel_recorrido
            panel.descripcion.configure(
                text="Para este recorrido, elige «Ej. 1» en el selector superior."
            )

    def calculo_no_esperado(self):
        if self._recorrido_activo:
            self._mostrar_paso_recorrido("calcular")
            self._recorrido_ventana.panel_recorrido.descripcion.configure(
                text=(
                    "El cálculo terminó, pero los datos ya no corresponden al "
                    "Ej. 1. Vuelve a cargar ese ejemplo antes de continuar."
                )
            )

    def calculo_completado(self, resultado):
        if not self._recorrido_activo or self._recorrido_estado != "calcular":
            return
        self._recorrido_calculado = True
        self._recorrido_resultado = resultado
        self._mostrar_paso_recorrido("resultado")

    def copia_completada(self):
        if not self._recorrido_activo or self._recorrido_estado != "copiar":
            return
        self._recorrido_copiado = True
        self._mostrar_paso_recorrido("zoom")

    def zoom_cambiado(self, nivel):
        if (
            not self._recorrido_activo
            or self._recorrido_estado != "zoom"
            or nivel == 100
        ):
            return
        self._recorrido_zoom = True
        self._mostrar_paso_recorrido("volver")

    def recorrido_siguiente(self):
        if not self._recorrido_activo:
            return
        siguiente = {
            "campos": "calcular",
            "calcular": "resultado",
            "resultado": "copiar",
            "copiar": "zoom",
            "zoom": "volver",
        }.get(self._recorrido_estado)
        if siguiente is not None:
            if siguiente == "resultado" and not self._recorrido_calculado:
                return
            if siguiente == "copiar" and not self._recorrido_calculado:
                return
            if siguiente == "zoom" and not self._recorrido_copiado:
                return
            if siguiente == "volver" and not self._recorrido_zoom:
                return
            self._mostrar_paso_recorrido(siguiente)

    def recorrido_anterior(self):
        if not self._recorrido_activo:
            return
        anterior = {
            "campos": "ejemplo",
            "calcular": "campos",
            "resultado": "calcular",
            "copiar": "resultado",
            "zoom": "copiar",
            "volver": "zoom",
        }.get(self._recorrido_estado)
        if self._recorrido_estado == "ejemplo":
            ventana = self._recorrido_ventana
            if ventana is None:
                return
            self._recorrido_volviendo_anterior = True
            if not ventana.volver():
                self._recorrido_volviendo_anterior = False
                return
            self._recorrido_volviendo_anterior = False
            self._recorrido_ventana = None
            self._mostrar_layout_recorrido()
            self._mostrar_paso_recorrido("tarjeta")
        elif anterior is not None:
            self._mostrar_paso_recorrido(anterior)

    def _ventana_recorrido_cerrada(self):
        self._recorrido_ventana = None
        if self._recorrido_volviendo_anterior:
            return
        if self._recorrido_estado == "volver":
            self._finalizar_recorrido()
        else:
            self.salir_recorrido()

    def _finalizar_recorrido(self):
        self._recorrido_activo = False
        self._recorrido_estado = None
        self._recorrido_ventana = None
        self.root.config(menu=self.menu_bar)
        self._resaltar_tarjeta(None)
        self._mostrar_layout_normal(mostrar_fin=True)

    def salir_recorrido(self):
        if not self._recorrido_activo:
            if self._recorrido_panel is not None and self._recorrido_estado is None:
                self._mostrar_layout_normal()
            return
        ventana = self._recorrido_ventana
        self._recorrido_activo = False
        self._recorrido_estado = None
        self._recorrido_ventana = None
        self.root.config(menu=self.menu_bar)
        self._resaltar_tarjeta(None)
        if ventana is not None:
            try:
                if ventana.winfo_exists():
                    ventana.desactivar_recorrido()
                    self._mostrar_layout_normal()
                    return
            except tk.TclError:
                pass
        self._mostrar_layout_normal()

    def abrir_ayuda_general(self):
        from core.ui.ayuda import mostrar_ayuda

        mostrar_ayuda(self.root, "general")

    def _programar_reorganizacion(self, event):
        if self._resize_job is not None:
            self.root.after_cancel(self._resize_job)
        self._resize_job = self.root.after(
            80,
            lambda ancho=event.width, alto=event.height: self._reorganizar_elementos(ancho, alto)
        )

    def _cancelar_reorganizacion(self, event):
        if event.widget is not self.contenido or self._resize_job is None:
            return
        try:
            self.root.after_cancel(self._resize_job)
        except tk.TclError:
            pass
        self._resize_job = None

    def _reorganizar_elementos(self, ancho, alto):
        self._resize_job = None
        ancho = max(640, ancho)
        alto = max(520, alto)
        if self.bg_image is not None and self.fondo_item is not None:
            imagen = self.fondo.resize((ancho, alto), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(imagen)
            self.contenido.itemconfigure(self.fondo_item, image=self.bg_image)
            self.contenido.coords(self.fondo_item, 0, 0)

        self.contenido.coords(self.titulo_item, ancho / 2, alto * 0.13)
        self.contenido.itemconfigure(
            self.titulo_item,
            font=(self.fuente_titulo, max(32, min(64, int(alto * 0.075))))
        )

        margen = max(20, ancho * 0.14)
        espacio = max(12, ancho * 0.025)
        ancho_tarjeta = min(310, (ancho - 2 * margen - 2 * espacio) / 3)
        tiene_tres_filas = len(self.tarjetas) > 6
        alto_tarjeta = (
            min(175, max(125, alto * 0.22))
            if tiene_tres_filas
            else min(240, max(155, alto * 0.235))
        )
        centros_x = [
            margen + ancho_tarjeta / 2,
            ancho / 2,
            ancho - margen - ancho_tarjeta / 2,
        ]
        centros_y = (
            [alto * 0.32, alto * 0.56, alto * 0.80]
            if tiene_tres_filas
            else [alto * 0.405, alto * 0.705]
        )

        for tarjeta in self.tarjetas:
            x = centros_x[tarjeta["column"]]
            y = centros_y[tarjeta["row"]]
            self.contenido.coords(tarjeta["window"], x, y)
            self.contenido.itemconfigure(
                tarjeta["window"],
                width=int(ancho_tarjeta),
                height=int(alto_tarjeta)
            )
            tarjeta["frame"].configure(width=int(ancho_tarjeta), height=int(alto_tarjeta))
            alto_vista = max(90, int(alto_tarjeta * 0.67))
            tarjeta["preview"].configure(
                width=max(100, int(ancho_tarjeta - 32)),
                height=alto_vista
            )
            if tarjeta["icon"] is not None:
                lado_icono = max(72, min(132, int(alto_vista * 0.82)))
                imagen = ImageTk.PhotoImage(
                    tarjeta["icon"].resize((lado_icono, lado_icono), Image.Resampling.LANCZOS)
                )
                tarjeta["button"].configure(image=imagen)
                tarjeta["button"].image = imagen

        self.contenido.coords(self.estado_item, ancho / 2, alto - 22)
        self.contenido.itemconfigure(self.estado_item, width=ancho, height=36)
        alto_panel_audio = self.panel_audio.winfo_reqheight()
        alto_boton_inicio = self.boton_inicio.winfo_reqheight()
        x_panel_audio = margen - 45
        y_panel_audio = 18 + (alto_boton_inicio - alto_panel_audio) / 2 + 15
        self.contenido.coords(self.musica_item, x_panel_audio, y_panel_audio)
        self.contenido.coords(self.volver_item, ancho - 20, 18)

    def registrar_fuentes(self):
        """Registra las fuentes solo durante la vida de esta aplicación."""
        if not hasattr(ctypes, "windll"):
            return

        AddFontResourceExW = ctypes.windll.gdi32.AddFontResourceExW
        AddFontResourceExW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
        AddFontResourceExW.restype = ctypes.c_int

        carpeta_fuentes = Path(__file__).resolve().parents[1] / "assets" / "fonts"
        fuentes = {
            "UltraCondensedSansSerif.ttf": ("fuente_titulo", "UltraCondensedSansSerif"),
            "HelveticaNowDisplay-Bold.ttf": ("fuente_tarjetas", "Helvetica Now Display"),
            "Democratica Bold.ttf": ("fuente_menu", "Democratica"),
        }

        for nombre_archivo, (atributo, familia) in fuentes.items():
            ruta = carpeta_fuentes / nombre_archivo
            if ruta.exists() and AddFontResourceExW(str(ruta), 0x10, None):
                self.fuentes_registradas.append(ruta)
                setattr(self, atributo, familia)

    def desregistrar_fuentes(self):
        if not hasattr(ctypes, "windll"):
            return

        RemoveFontResourceExW = ctypes.windll.gdi32.RemoveFontResourceExW
        RemoveFontResourceExW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
        RemoveFontResourceExW.restype = ctypes.c_int

        for ruta in self.fuentes_registradas:
            RemoveFontResourceExW(str(ruta), 0x10, None)
        self.fuentes_registradas.clear()

    def cerrar_aplicacion(self):
        self.desregistrar_fuentes()
        if self.audio_manager is not None:
            self.audio_manager.cerrar()
        self.root.destroy()

    def volver_al_inicio(self):
        if (
            self.al_volver_inicio is None
            or self.ventana_activa is not None
            or self._recorrido_activo
        ):
            return
        if self._resize_job is not None:
            self.root.after_cancel(self._resize_job)
            self._resize_job = None
        self.desregistrar_fuentes()
        self.root.config(menu="")
        self.contenido.destroy()
        self.al_volver_inicio()

    def _abrir_ventana(self, constructor, nombre_modulo):
        """Abre una sola calculadora y evita dobles aperturas por doble clic."""
        if self.ventana_activa is not None:
            if self.ventana_activa is True:
                return
            if self.ventana_activa.winfo_exists():
                self.ventana_activa.lift()
                self.ventana_activa.focus_force()
                return

        if self.audio_manager is not None:
            self.audio_manager.detener_musica_lobby()
        self.root.withdraw()
        self.ventana_activa = True
        try:
            ventana = constructor(self.root)
        except Exception:
            self.ventana_activa = None
            self.root.deiconify()
            if self.audio_manager is not None:
                self.audio_manager.iniciar_musica_lobby()
            if self._recorrido_activo:
                self._recorrido_ventana = None
                self._mostrar_layout_recorrido()
                self._mostrar_paso_recorrido("tarjeta")
            raise

        self.ventana_activa = ventana
        self.ultimo_modulo = nombre_modulo
        self.lbl_estado.config(text=f"Último módulo utilizado: {nombre_modulo}")
        preferencias.guardar(ultimo_modulo_utilizado=nombre_modulo)

        def limpiar_referencia(event):
            if event.widget != ventana:
                return
            self.ventana_activa = None
            try:
                if not self.root.winfo_exists():
                    return
                self.root.deiconify()
            except tk.TclError:
                return
            if self.audio_manager is not None:
                self.audio_manager.iniciar_musica_lobby()
            if self._recorrido_activo and self._recorrido_ventana is ventana:
                self._ventana_recorrido_cerrada()

        ventana.bind("<Destroy>", limpiar_referencia, add="+")

    # ==========================================
    # FUNCIONES DE TRANSICIÓN (CONTROLADORES)
    # ==========================================
    def abrir_matrices(self):
        print("Abriendo módulo de Matrices...")
        from core.ui.vista_matriz import VistaMatriz
        self._abrir_ventana(VistaMatriz, "Matrices individuales")

    def abrir_vectores(self):
        print("Abriendo módulo de Vectores...")
        from core.ui.vista_vector import VistaVector
        self._abrir_ventana(VistaVector, "Operaciones vectoriales")

    def abrir_ec_matriciales(self):
        print("Abriendo módulo de Ecuaciones Matriciales...")
        from core.ui.vista_matricial import VistaMatricial
        self._abrir_ventana(VistaMatricial, "Ecuaciones matriciales")

    def abrir_sistemas(self):
        print("Abriendo módulo de Sistemas...")
        from core.ui.vista_sistemas import VistaSistemas
        self._abrir_ventana(VistaSistemas, "Sistemas e Independencia")
    
    def abrir_limites(self):
        print("Abriendo módulo de Límites...")
        from core.ui.vista_limites import VistaLimites
        self._abrir_ventana(VistaLimites, "Cálculo de Límites")

    def abrir_sistemas_numericos(self):
        print("Abriendo módulo de Sistemas Numéricos...")
        from core.ui.vista_numerica import VistaSistemasNumericos
        self._abrir_ventana(VistaSistemasNumericos, "Sistemas Numéricos")

    def abrir_metodos_numericos(self):
        print("Abriendo módulo de Métodos Numéricos...")
        from core.ui.vista_metodos_numericos import VistaMetodosNumericos
        if self._recorrido_activo:
            self._abrir_ventana(
                lambda parent: VistaMetodosNumericos(parent, recorrido=self),
                "Métodos Numéricos",
            )
        else:
            self._abrir_ventana(VistaMetodosNumericos, "Métodos Numéricos")

    def abrir_determinantes(self):
        print("Abriendo módulo de Determinantes...")
        from core.ui.vista_determinantes import VistaDeterminantes
        self._abrir_ventana(VistaDeterminantes, "Determinantes y Factorización LU")
        
    def proximamente(self):
        messagebox.showinfo("Próximamente", "Este módulo aún está en desarrollo.")

    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "Calculadora de Álgebra Lineal - FIA UAM\nVersión unificada.")