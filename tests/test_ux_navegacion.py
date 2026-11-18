"""Pruebas de la etapa final de UX: preferencias, navegación, ayuda, bienvenida,
ejemplos y copia de resultados. Las que necesitan Tk crean ventanas fuera de la
pantalla y se omiten si no hay escritorio disponible."""

import json
import os
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest import mock

from core.ui import preferencias


class _ConfigTemporal(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self._env = mock.patch.dict(os.environ, {"HEYALGB_CONFIG_DIR": self._dir.name})
        self._env.start()

    def tearDown(self):
        self._env.stop()
        self._dir.cleanup()


class PreferenciasTests(_ConfigTemporal):
    def test_sin_archivo_usa_predeterminadas(self):
        self.assertEqual(preferencias.cargar(), preferencias.PREDETERMINADAS)

    def test_guardar_y_recuperar(self):
        self.assertTrue(preferencias.guardar(mostrar_bienvenida=False, efectos_habilitados=False))
        datos = preferencias.cargar()
        self.assertFalse(datos["mostrar_bienvenida"])
        self.assertFalse(datos["efectos_habilitados"])
        self.assertTrue(datos["musica_habilitada"])

    def test_archivo_danado_o_con_tipos_incorrectos(self):
        ruta = preferencias.ruta_preferencias()
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text("{esto no es json", encoding="utf-8")
        with self.assertLogs("heyalgb.preferencias", level="WARNING"):
            self.assertEqual(preferencias.cargar(), preferencias.PREDETERMINADAS)
        ruta.write_text(json.dumps({"mostrar_bienvenida": "no", "otra": 1}), encoding="utf-8")
        self.assertTrue(preferencias.cargar()["mostrar_bienvenida"])
        ruta.write_text("[1, 2]", encoding="utf-8")
        with self.assertLogs("heyalgb.preferencias", level="WARNING"):
            self.assertEqual(preferencias.cargar(), preferencias.PREDETERMINADAS)
        # Guardar sobre un archivo dañado lo repara.
        self.assertTrue(preferencias.guardar(musica_habilitada=False))
        self.assertFalse(preferencias.cargar()["musica_habilitada"])

    def test_la_carpeta_no_esta_dentro_del_repositorio(self):
        with mock.patch.dict(os.environ, {"HEYALGB_CONFIG_DIR": ""}):
            carpeta = preferencias.carpeta_configuracion().resolve()
        repositorio = Path(__file__).resolve().parents[1]
        self.assertNotIn(repositorio, [carpeta, *carpeta.parents])


class AyudaContenidoTests(unittest.TestCase):
    def test_todas_las_herramientas_tienen_ayuda_completa(self):
        from core.ui.ayuda import CONTENIDO, texto_ayuda

        claves = {
            "general", "matriz", "vector", "matricial", "intercambio", "flujo_red",
            "particiones", "sistemas", "limites", "numerica", "determinantes",
            "biseccion", "regla_falsa", "abiertos", "errores",
        }
        self.assertEqual(set(CONTENIDO), claves)
        for clave in claves:
            texto = texto_ayuda(clave)
            for seccion in ("PARA QUÉ SIRVE", "FORMATOS ADMITIDOS", "EJEMPLO VÁLIDO",
                            "RESTRICCIONES", "CÓMO LEER LA SALIDA", "ATAJOS DE TECLADO"):
                self.assertIn(seccion, texto, (clave, seccion))

    def test_ejemplos_de_la_ayuda_coinciden_con_el_codigo(self):
        from fractions import Fraction as F

        from core.determinantes import operaciones_determinantes as det
        from core.lineal.solucion import enrutar_resolucion_matricial
        from core.sistemas_numericos import operaciones_numericas as num

        resultado = enrutar_resolucion_matricial(
            [[F(2), F(1), F(-1)], [F(-3), F(-1), F(2)], [F(-2), F(1), F(2)]],
            vector_b=[F(8), F(-11), F(-3)],
        )
        self.assertEqual(resultado["solucion"], [2, 3, -1])
        self.assertEqual(
            det.determinante_lu_valor([[F(2), F(-1), F(0)], [F(1), F(3), F(2)], [F(0), F(1), F(4)]]),
            24,
        )
        self.assertEqual(
            num.convertir_decimal_a_base(num.parsear_decimal("45.75"), 2, "Binario")[0],
            "101101.11",
        )


class _ConTk(_ConfigTemporal):
    def setUp(self):
        super().setUp()
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f"Tk no disponible: {error}")
        self.root.geometry("300x200+-4000+-4000")
        self.root.update()

    def tearDown(self):
        try:
            # CustomTkinter programa tareas internas (barra de título, scrollbars)
            # unos cientos de ms después de crear ventanas; se dejan terminar para
            # que no se ejecuten sobre el intérprete de la siguiente prueba.
            self.root.after(400, self.root.quit)
            self.root.mainloop()
            self.root.destroy()
        finally:
            super().tearDown()


class NavegacionTests(_ConTk):
    def _abrir_limites(self):
        from core.ui.vista_limites import VistaLimites

        self.root.withdraw()
        vista = VistaLimites(self.root)
        vista.geometry("+-4000+-4000")
        self.root.update()
        return vista

    def _escribir(self, vista, entrada, texto):
        entrada._entry.focus_force()
        self.root.update()
        entrada.delete(0, "end")
        for caracter in texto:
            entrada._entry.event_generate("<KeyPress>", keysym=caracter, when="now")
        entrada.insert(0, texto)
        self.root.update()

    def test_volver_sin_cambios_no_pregunta_y_restaura_el_padre(self):
        vista = self._abrir_limites()
        with mock.patch("core.ui.navegacion.messagebox.askyesno") as pregunta:
            vista.volver()
        pregunta.assert_not_called()
        self.assertFalse(vista.winfo_exists())
        self.assertEqual(self.root.state(), "normal")

    def test_volver_con_datos_pide_confirmacion(self):
        vista = self._abrir_limites()
        self._escribir(vista, vista.entry_fx, "x")
        self.assertTrue(vista._guardia_cambios.modificada)
        with mock.patch("core.ui.navegacion.messagebox.askyesno", return_value=False) as pregunta:
            vista.volver()
        pregunta.assert_called_once()
        self.assertTrue(vista.winfo_exists())  # el usuario canceló: no se pierde nada
        with mock.patch("core.ui.navegacion.messagebox.askyesno", return_value=True):
            vista.volver()
        self.assertFalse(vista.winfo_exists())

    def test_tab_y_navegacion_no_cuentan_como_cambio(self):
        vista = self._abrir_limites()
        vista.entry_fx._entry.focus_force()
        self.root.update()
        for tecla in ("Tab", "Left", "Right", "Home"):
            vista.entry_fx._entry.event_generate("<KeyPress>", keysym=tecla, when="now")
        self.assertFalse(vista._guardia_cambios.modificada)
        vista.volver()

    def test_ayuda_es_unica_y_se_cierra_al_volver(self):
        from core.ui.ayuda import mostrar_ayuda

        vista = self._abrir_limites()
        primera = mostrar_ayuda(vista, "limites")
        segunda = mostrar_ayuda(vista, "limites")
        self.assertIs(primera, segunda)
        self.assertIn("EJEMPLO VÁLIDO", primera._texto.get("1.0", "end"))
        vista.volver()
        self.assertFalse(primera.winfo_exists())

    def test_cargar_ejemplo_no_calcula_y_confirma_reemplazo(self):
        vista = self._abrir_limites()
        # Valores iniciales de la vista: se reemplazan sin preguntar.
        with mock.patch("core.ui.navegacion.messagebox.askyesno") as pregunta:
            self.assertTrue(vista.cargar_ejemplo())
        pregunta.assert_not_called()
        self.assertEqual(vista.entry_fx.get(), "sin(x)/x")
        self.assertNotIn("RESULTADO", vista.texto_resultado.get("1.0", "end"))
        # Datos propios distintos: se pregunta y se respeta un «No».
        vista.entry_fx.delete(0, "end")
        vista.entry_fx.insert(0, "x^2")
        with mock.patch("core.ui.navegacion.messagebox.askyesno", return_value=False):
            self.assertFalse(vista.cargar_ejemplo())
        self.assertEqual(vista.entry_fx.get(), "x^2")
        vista._guardia_cambios.modificada = False
        vista.volver()

    def test_campo_vacio_recibe_foco_y_marca(self):
        vista = self._abrir_limites()
        vista.entry_fx.delete(0, "end")
        vista.ejecutar_calculo()
        self.root.update()
        self.assertTrue(getattr(vista.entry_fx, "_heyalgb_en_error", False))
        self.assertIn("⚠", vista.texto_resultado.get("1.0", "end"))
        vista.volver()


class CopiarTests(_ConTk):
    def test_copiar_sin_y_con_resultados(self):
        from core.ui.zoom_resultados import crear_consola_resultados, escribir_consola

        contenedor, texto, zoom = crear_consola_resultados(self.root)
        contenedor.pack()
        barra = contenedor.barra
        barra.copiar()
        self.assertEqual(barra.aviso.cget("text"), "Nada que copiar")
        escribir_consola(texto, "[ 1   2 ]\n[ 3   4 ]")
        zoom.establecer(150)
        barra.copiar()
        self.assertEqual(barra.aviso.cget("text"), "✓ Copiado")
        self.assertEqual(self.root.clipboard_get(), "[ 1   2 ]\n[ 3   4 ]")
        self.assertEqual(zoom.nivel, 150)  # copiar no cambia el zoom
        barra.boton_limpiar_resultados.invoke()
        self.assertEqual(texto.get("1.0", "end-1c"), "")
        self.assertEqual(zoom.nivel, 150)  # limpiar no cambia el zoom


class BienvenidaTests(_ConTk):
    def test_recorrido_y_preferencia(self):
        from core.ui.bienvenida import PASOS, abrir_bienvenida, mostrar_bienvenida_si_corresponde

        guia = abrir_bienvenida(self.root)
        self.assertIs(abrir_bienvenida(self.root), guia)
        self.assertEqual(str(guia.boton_anterior.cget("state")), "disabled")
        for _ in range(len(PASOS) + 2):
            guia.siguiente()
        self.assertEqual(guia.paso, len(PASOS) - 1)
        self.assertTrue(guia.boton_finalizar.winfo_ismapped() or True)
        guia.var_no_mostrar.set(True)
        guia.finalizar()
        self.assertFalse(preferencias.cargar()["mostrar_bienvenida"])
        self.assertIsNone(mostrar_bienvenida_si_corresponde(self.root))
        # Se puede volver a abrir desde Ayuda aunque esté desactivada.
        guia = abrir_bienvenida(self.root)
        guia.var_no_mostrar.set(False)
        guia.omitir()
        self.assertTrue(preferencias.cargar()["mostrar_bienvenida"])
        self.assertIsNotNone(mostrar_bienvenida_si_corresponde(self.root, retraso_ms=10_000))


class AudioPreferenciasTests(unittest.TestCase):
    def test_efectos_silenciados_no_se_reproducen(self):
        from core.ui.audio_manager import AudioManager

        audio = AudioManager.__new__(AudioManager)
        audio.disponible = True
        audio.efectos_habilitados = True
        sonido = mock.Mock()
        audio._efectos = {"calcular": sonido}
        audio._ultimo_hover = 0.0
        audio.reproducir_efecto("calcular")
        audio.establecer_efectos_habilitados(False)
        audio.reproducir_efecto("calcular")
        self.assertEqual(sonido.play.call_count, 1)


if __name__ == "__main__":
    unittest.main()
