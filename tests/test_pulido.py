"""Regresiones de la entrega de pulido (comportamiento y estabilidad)."""

import tkinter as tk
import unittest
from fractions import Fraction as F

from core.lineal.eliminacion import eliminacion_por_filas
from core.lineal.solucion import enrutar_resolucion_matricial
from core.metodos_numericos.biseccion import _crear_funcion
from core.metodos_numericos.metodo_secante import resolver_secante
from core.metodos_numericos.newton_raphson import (
    ESTADO_RESIDUO_SIN_SIGNO,
    resolver_newton_raphson,
    verificar_cambio_de_signo,
)


class ResiduoSinCambioDeSignoTests(unittest.TestCase):
    def test_verificacion_de_cambio_de_signo(self):
        self.assertTrue(verificar_cambio_de_signo(_crear_funcion("x - 2"), 2.0000001, 1e-6))
        self.assertTrue(verificar_cambio_de_signo(_crear_funcion("x - 2"), 2.0, 0))
        self.assertFalse(verificar_cambio_de_signo(_crear_funcion("exp(x)"), -19.0, 1.0))

    def test_newton_no_declara_raiz_donde_la_funcion_solo_se_acerca_a_cero(self):
        resultado = resolver_newton_raphson("exp(x)", 0, 1e-8, 200, forzar=True)
        self.assertFalse(resultado["convergio"])
        self.assertEqual(resultado["estado"], ESTADO_RESIDUO_SIN_SIGNO)

    def test_secante_no_declara_raiz_donde_la_funcion_solo_se_acerca_a_cero(self):
        resultado = resolver_secante("exp(x)", 0, 1, 1e-8, 200)
        self.assertFalse(resultado["convergio"])
        self.assertEqual(resultado["estado"], ESTADO_RESIDUO_SIN_SIGNO)

    def test_raices_simples_siguen_convergiendo(self):
        newton = resolver_newton_raphson("x^3 - x - 2", 1.5, 1e-8, 50)
        secante = resolver_secante("x^3 - x - 2", 1, 2, 1e-8, 50)
        self.assertTrue(newton["convergio"])
        self.assertTrue(secante["convergio"])

    def test_x0_que_cumple_la_tolerancia_no_se_llama_raiz_exacta(self):
        exacta = resolver_newton_raphson("x - 2", 2, 1e-8, 10)
        aproximada = resolver_newton_raphson("x - 2", 2 + 1e-10, 1e-8, 10)
        self.assertEqual(exacta["estado"], "Raíz exacta en x0")
        self.assertEqual(aproximada["estado"], "Tolerancia por residuo alcanzada en x0")


class FormatoDePasosTests(unittest.TestCase):
    def test_eliminacion_usa_el_formato_recibido_en_los_pasos(self):
        _, pasos, _ = eliminacion_por_filas(
            [[F(3), F(1), F(1)], [F(1), F(2), F(0)]],
            modo="gauss",
            formatear=lambda v: f"<{float(v):.3f}>",
        )
        descripciones = " ".join(descripcion for descripcion, _ in pasos)
        # F1 / 3, F2 - 1·F1 y F2 / (5/3): todos con el formato recibido.
        self.assertIn("F1 = F1 / (<3.000>)", descripciones)
        self.assertIn("F2 = F2 / (<1.667>)", descripciones)
        self.assertNotIn("5/3", descripciones)

    def test_sustitucion_hacia_atras_usa_el_formato_recibido(self):
        resultado = enrutar_resolucion_matricial(
            [[F(3), F(1)], [F(1), F(2)]],
            vector_b=[F(1), F(0)],
            metodo="gauss",
            formatear=lambda v: f"<{float(v):.3f}>",
        )
        self.assertIn("<", " ".join(resultado["pasos_despeje"]))
        self.assertEqual(resultado["solucion"], [F(2, 5), F(-1, 5)])


class VentanasSecundariasTests(unittest.TestCase):
    def test_fallo_al_abrir_herramienta_no_deja_la_ventana_oculta(self):
        try:
            root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f"Tk no disponible: {error}")
        root.withdraw()
        try:
            from core.ui.vista_matricial import VistaMatricial

            vista = VistaMatricial(root)

            def constructor_que_falla(_master):
                raise RuntimeError("fallo simulado")

            with self.assertLogs("heyalgb.ui.matricial", level="ERROR"):
                ventana = vista._abrir_secundaria(constructor_que_falla, "Prueba")
            self.assertIsNone(ventana)
            self.assertEqual(vista.state(), "normal")
            texto = vista.texto_resultado.get("1.0", "end")
            self.assertIn("No se pudo abrir «Prueba»", texto)
            self.assertNotIn("fallo simulado", texto)
            vista.destroy()
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
