"""Teclado visual para insertar notación algebraica en un campo de función."""

from tkinter import TclError

from core.ui.ctk_compat import ctk
from core.ui.tema import (
    FONDO_CALCULADORA,
    TEXTO_CLARO,
    estilo_boton_principal,
    estilo_boton_secundario,
    estilo_panel_contenedor,
)


class TecladoMatematico(ctk.CTkToplevel):
    """Inserta símbolos y funciones sin ejecutar expresiones externas."""

    _CARACTERES_SUPERINDICE = {
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
        "+": "⁺",
        "-": "⁻",
        "(": "⁽",
        ")": "⁾",
        ".": "˙",
        "-": "⁻",
        "−": "⁻",
        "x": "ᵡ",
        "e": "ᵉ",
    }

    TECLAS = (
        (("7", "7"), ("8", "8"), ("9", "9"), ("×", "×"), ("÷", "÷"), ("(", "(")),
        (("4", "4"), ("5", "5"), ("6", "6"), ("−", "−"), ("+", "+"), (")", ")")),
        (("1", "1"), ("2", "2"), ("3", "3"), ("x", "x"), ("xʸ", "POWER"), ("⌫", "⌫")),
        (("0", "0"), (".", "."), ("π", "π"), ("e", "e"), ("√", "sqrt("), ("C", "C")),
        (
            ("sin", "sin("),
            ("cos", "cos("),
            ("tan", "tan("),
            ("log", "log("),
            ("ln", "ln("),
            ("exp", "exp("),
        ),
        (
            ("abs", "abs("),
            ("x²", "²"),
            ("x³", "³"),
            ("·", "·"),
            ("Finalizar exp.", "FINISH_POWER"),
            ("Cerrar", "Cerrar"),
        ),
    )

    def __init__(self, master, entrada):
        super().__init__(master.winfo_toplevel())
        self.configure(fg_color=FONDO_CALCULADORA)
        self.title("Teclado matemático")
        self.geometry("560x420")
        self.resizable(False, False)
        self.transient(master.winfo_toplevel())
        self._master_widget = master
        self.entrada = entrada
        self.modo_exponente = False
        self._entrada_bind_id = None
        self._vincular_entrada(entrada)
        self.protocol("WM_DELETE_WINDOW", self._cerrar)
        self._crear_interfaz()

    def _crear_interfaz(self):
        panel = ctk.CTkFrame(self, **estilo_panel_contenedor())
        panel.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(
            panel,
            text="Teclado de función · admite 2x, 3(x+1) y x^2",
            text_color=TEXTO_CLARO,
            wraplength=480,
        ).pack(anchor="w", padx=10, pady=(8, 4))
        self.estado = ctk.CTkLabel(
            panel,
            text="Pulse xʸ y escriba el exponente; puede finalizarlo manualmente.",
            text_color=TEXTO_CLARO,
            wraplength=480,
        )
        self.estado.pack(anchor="w", padx=10, pady=(0, 4))

        teclado = ctk.CTkFrame(panel, fg_color="transparent")
        teclado.pack(fill="both", expand=True, padx=5, pady=5)
        for fila, teclas in enumerate(self.TECLAS):
            for columna, (etiqueta, texto) in enumerate(teclas):
                estilo = (
                    estilo_boton_secundario()
                    if etiqueta in {"⌫", "C", "Cerrar", "Finalizar exp."}
                    else estilo_boton_principal()
                )
                boton = ctk.CTkButton(
                    teclado,
                    text=etiqueta,
                    width=92 if etiqueta == "Finalizar exp." else 72,
                    height=42,
                    command=lambda valor=texto: self._accion(valor),
                    **estilo,
                )
                boton.grid(
                    row=fila,
                    column=columna,
                    padx=3,
                    pady=3,
                    sticky="nsew",
                )
        for columna in range(6):
            teclado.grid_columnconfigure(columna, weight=1)
        for fila in range(len(self.TECLAS)):
            teclado.grid_rowconfigure(fila, weight=1)

    def _accion(self, valor):
        if valor == "Cerrar":
            self._cerrar()
        elif valor == "POWER":
            self._activar_exponente()
        elif valor == "FINISH_POWER":
            self._finalizar_exponente()
        elif valor == "C":
            self.modo_exponente = False
            self._actualizar_estado()
            self.entrada.delete(0, "end")
            self.entrada.focus_set()
        elif valor == "⌫":
            self._borrar_caracter()
        elif valor in {"×", "·", "÷", "*", "/"}:
            self._finalizar_exponente()
            self._insertar(valor)
        elif (
            valor in {"+", "-", "−"}
            and self.modo_exponente
            and not self._signo_dentro_del_exponente()
        ):
            self._finalizar_exponente()
            self._insertar(valor)
        elif valor in {"sin(", "cos(", "tan(", "log(", "ln(", "exp(", "sqrt(", "abs("}:
            self._finalizar_exponente()
            self._insertar(valor)
        else:
            cerrar_exponente = self.modo_exponente and valor == ")"
            self._insertar(valor)
            if cerrar_exponente:
                self._finalizar_exponente()

    def _vincular_entrada(self, entrada):
        if self._entrada_bind_id is not None:
            try:
                self.entrada.unbind("<KeyPress>", self._entrada_bind_id)
            except TclError:
                pass
        self.entrada = entrada
        self._entrada_bind_id = self.entrada.bind(
            "<KeyPress>",
            self._procesar_tecla,
            add="+",
        )

    def _procesar_tecla(self, evento):
        if not self.modo_exponente:
            if evento.char == "^":
                self._activar_exponente()
                return "break"
            return None

        if (
            evento.char in {"+", "-", "−"}
            and not self._signo_dentro_del_exponente()
        ):
            self._finalizar_exponente()
            return None
        if evento.char in self._CARACTERES_SUPERINDICE:
            self._insertar(evento.char)
            if evento.char == ")":
                self._finalizar_exponente()
            return "break"
        if evento.char and evento.char.isprintable():
            self._finalizar_exponente()
        return None

    def _signo_dentro_del_exponente(self):
        posicion = self.entrada.index("insert")
        prefijo = self.entrada.get()[:posicion]
        caracteres = set(self._CARACTERES_SUPERINDICE.values())
        exponente = []
        for caracter in reversed(prefijo):
            if caracter not in caracteres:
                break
            exponente.append(caracter)
        exponente.reverse()
        if not exponente:
            return True
        apertura = exponente.count("⁽")
        cierre = exponente.count("⁾")
        return apertura > cierre or exponente[-1] in {"⁽", "⁺", "⁻"}

    def _activar_exponente(self):
        if self.modo_exponente:
            self._finalizar_exponente()
            return
        posicion = self.entrada.index("insert")
        anterior = self.entrada.get()[:posicion].rstrip()
        if not anterior or anterior[-1] not in (
            "0123456789.)xyeπ"
            "⁰¹²³⁴⁵⁶⁷⁸⁹⁾ᵡᵉ"
        ):
            self.estado.configure(
                text="Coloque el cursor después de la base antes de pulsar xʸ."
            )
            return
        self.modo_exponente = True
        self._actualizar_estado()
        self.entrada.focus_set()

    def _finalizar_exponente(self):
        self.modo_exponente = False
        self._actualizar_estado()
        self.entrada.focus_set()

    def _actualizar_estado(self):
        if self.modo_exponente:
            texto = "Modo exponente activo · pulse «Finalizar exp.» al terminar."
        else:
            texto = "Modo normal · pulse xʸ para escribir un exponente."
        self.estado.configure(text=texto)

    def _insertar(self, texto):
        try:
            inicio = self.entrada.index("sel.first")
            fin = self.entrada.index("sel.last")
            self.entrada.delete(inicio, fin)
        except TclError:
            inicio = self.entrada.index("insert")
        if self.modo_exponente:
            texto_visible = "".join(
                self._CARACTERES_SUPERINDICE.get(caracter, caracter)
                for caracter in texto
            )
        else:
            texto_visible = texto
        self.entrada.insert(inicio, texto_visible)
        self.entrada.icursor(inicio + len(texto_visible))
        self.entrada.focus_set()

    def _borrar_caracter(self):
        try:
            inicio = self.entrada.index("sel.first")
            fin = self.entrada.index("sel.last")
            self.entrada.delete(inicio, fin)
        except TclError:
            posicion = self.entrada.index("insert")
            if posicion > 0:
                self.entrada.delete(posicion - 1, posicion)
        self.entrada.focus_set()

    def _cerrar(self):
        if getattr(self._master_widget, "_ventana_teclado", None) is self:
            self._master_widget._ventana_teclado = None
        if self._entrada_bind_id is not None:
            try:
                self.entrada.unbind("<KeyPress>", self._entrada_bind_id)
            except TclError:
                pass
        self.destroy()


def abrir_teclado_matematico(master, entrada):
    """Abre o reutiliza el teclado asociado a una vista."""
    ventana = getattr(master, "_ventana_teclado", None)
    if ventana is not None:
        try:
            if ventana.winfo_exists():
                ventana._vincular_entrada(entrada)
                ventana.modo_exponente = False
                ventana._actualizar_estado()
                ventana.lift()
                ventana.focus_force()
                return ventana
        except TclError:
            pass

    ventana = TecladoMatematico(master, entrada)
    master._ventana_teclado = ventana
    return ventana


def cerrar_teclado_matematico(master):
    """Cierra el teclado auxiliar asociado a una vista, si está abierto."""
    ventana = getattr(master, "_ventana_teclado", None)
    if ventana is not None:
        try:
            ventana._cerrar()
        except TclError:
            master._ventana_teclado = None
