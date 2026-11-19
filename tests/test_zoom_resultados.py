"""Pruebas del zoom local de las consolas de resultados (requiere Tk)."""

import tkinter as tk
import unittest

from core.ui import zoom_resultados as zr
from core.ui.ctk_compat import ctk


class ZoomResultadosTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.root = ctk.CTk()
        except tk.TclError as error:  # Sin pantalla disponible.
            raise unittest.SkipTest(f"Tk no disponible: {error}")
        # Visible pero fuera de la pantalla: Tk solo entrega teclado y rueda a
        # ventanas mapeadas que pueden tener el foco.
        cls.root.geometry("500x300+-4000+-4000")
        cls.root.update()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def setUp(self):
        self.contenedor, self.textbox, self.zoom = zr.crear_consola_resultados(
            self.root, tamano=11
        )
        self.contenedor.pack(fill="both", expand=True)
        self.texto = self.textbox._textbox
        self.controles = self.contenedor.winfo_children()[0].winfo_children()[-1]

    def tearDown(self):
        self.contenedor.destroy()

    def _evento(self, secuencia, **kwargs):
        self.root.update()
        self.texto.focus_force()
        self.root.update()
        self.texto.event_generate(secuencia, when="now", **kwargs)
        self.root.update()

    def test_consola_es_de_solo_lectura_y_monoespaciada(self):
        zr.escribir_consola(self.textbox, "[ 1  2 ]\n[ 3  4 ]")
        self.assertEqual(self.texto.cget("state"), "disabled")
        self.textbox.insert("end", "x")  # Ignorado en estado disabled.
        self.assertEqual(self.textbox.get("1.0", "end-1c"), "[ 1  2 ]\n[ 3  4 ]")
        self.assertEqual(self.zoom.fuente.cget("family"), "Consolas")
        self.assertEqual(self.texto.cget("wrap"), "none")

    def test_boton_copiar_aplica_formato_opcional_sin_activar_otras_consolas(self):
        contenedor, texto, _zoom = zr.crear_consola_resultados(
            self.root,
            formateador_copia=lambda contenido: f"Reporte académico\n{contenido}",
        )
        contenedor.pack(fill="both", expand=True)
        zr.escribir_consola(texto, "Resultado y tabla")

        contenedor.barra.copiar()

        self.assertEqual(
            self.root.clipboard_get(),
            "Reporte académico\nResultado y tabla",
        )
        contenedor.destroy()

    def test_limites_y_pasos(self):
        for _ in range(20):
            self.zoom.aumentar()
        self.assertEqual(self.zoom.nivel, 200)
        for _ in range(30):
            self.zoom.disminuir()
        self.assertEqual(self.zoom.nivel, 50)
        self.assertEqual(self.zoom.establecer(73), 73)
        self.assertEqual(self.zoom.establecer(999), 200)

    def test_tamano_se_calcula_desde_la_base_sin_deriva(self):
        for _ in range(15):
            self.zoom.aumentar()
        for _ in range(15):
            self.zoom.disminuir()
        self.assertEqual(self.zoom.nivel, 50)
        self.zoom.restablecer()
        self.assertEqual(self.zoom.tamano_actual, 11)
        self.zoom.establecer(200)
        self.assertEqual(self.zoom.fuente.cget("size"), 22)
        self.zoom.establecer(50)
        self.assertEqual(self.zoom.fuente.cget("size"), 6)

    def test_controles_muestran_el_nivel_y_se_deshabilitan_en_limites(self):
        self.zoom.establecer(200)
        self.assertEqual(self.controles.boton_nivel.cget("text"), "200 %")
        self.assertEqual(self.controles.boton_mas.cget("state"), "disabled")
        self.controles.boton_nivel.invoke()
        self.assertEqual(self.zoom.nivel, 100)
        self.assertEqual(self.controles.boton_mas.cget("state"), "normal")
        self.zoom.establecer(50)
        self.assertEqual(self.controles.boton_menos.cget("state"), "disabled")

    def test_atajos_de_teclado(self):
        # En Windows, Tk no puede sintetizar teclas del teclado numérico
        # (keycode 0); KP_Add/KP_Subtract/KP_0 se verifican manualmente.
        self._evento("<Control-plus>")
        self.assertEqual(self.zoom.nivel, 110)
        self._evento("<Control-equal>")
        self.assertEqual(self.zoom.nivel, 120)
        self._evento("<Control-minus>")
        self.assertEqual(self.zoom.nivel, 110)
        self._evento("<Control-Key-0>")
        self.assertEqual(self.zoom.nivel, 100)

    def test_atajos_del_teclado_numerico_estan_registrados(self):
        for secuencia in ("<Control-KP_Add>", "<Control-KP_Subtract>", "<Control-KP_0>"):
            with self.subTest(secuencia=secuencia):
                self.assertTrue(self.texto.bind(secuencia))

    def test_rueda_con_control_y_sin_control(self):
        self._evento("<Control-MouseWheel>", delta=120)
        self.assertEqual(self.zoom.nivel, 110)
        self._evento("<Control-MouseWheel>", delta=-120)
        self._evento("<Control-MouseWheel>", delta=-120)
        self.assertEqual(self.zoom.nivel, 90)
        self._evento("<MouseWheel>", delta=-120)  # Sin Ctrl: solo desplaza.
        self.assertEqual(self.zoom.nivel, 90)

    def test_zoom_conserva_texto_y_posicion_de_lectura(self):
        contenido = "\n".join(f"fila {i:03d}  [ {i}  {i * 2} ]" for i in range(300))
        zr.escribir_consola(self.textbox, contenido)
        self.root.update()
        self.texto.yview("120.0")
        self.root.update()
        antes = self.texto.index("@0,0")
        self.zoom.establecer(150)
        self.root.update()
        self.assertEqual(self.texto.index("@0,0"), antes)
        self.assertEqual(self.textbox.get("1.0", "end-1c"), contenido)

    def test_no_instala_bindings_globales(self):
        for secuencia in ("<Control-MouseWheel>", "<Control-plus>", "<Control-Key-0>"):
            with self.subTest(secuencia=secuencia):
                self.assertEqual(self.root.bind_all(secuencia), "")
        otra = ctk.CTkEntry(self.root)
        self.assertNotIn("<Control-MouseWheel>", otra._entry.bind())


if __name__ == "__main__":
    unittest.main()
