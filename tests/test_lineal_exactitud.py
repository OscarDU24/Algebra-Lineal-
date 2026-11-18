"""Regresiones de exactitud para core/lineal (vista Matrices individuales)."""

import unittest
from fractions import Fraction as F

from core.lineal import conversiones as conv
from core.lineal.clasificacion import clasificar_sistema
from core.lineal.eliminacion import eliminacion_por_filas
from core.lineal.solucion import (
    enrutar_resolucion_matricial,
    invertir_matriz_gauss_jordan,
    multiplicar_matrices,
)
from core.lineal.verificacion import verificar_solucion
from core.lineal.visualizacion import imprimir_sistema_ecuaciones


class ConversionesTests(unittest.TestCase):
    def test_convertir_a_racional_es_exacto(self):
        self.assertEqual(conv.convertir_a_racional("1/3"), F(1, 3))
        self.assertEqual(conv.convertir_a_racional(" 0.1 "), F(1, 10))
        self.assertEqual(conv.convertir_a_racional("-2"), F(-2))
        self.assertEqual(conv.convertir_a_racional("1e-3"), F(1, 1000))

    def test_convertir_a_racional_rechaza_entradas_invalidas(self):
        for texto in ("abc", "1/0", "inf", "nan", ""):
            with self.subTest(texto=texto):
                self.assertIsNone(conv.convertir_a_racional(texto))

    def test_fraccion_no_aproxima_valores(self):
        self.assertEqual(conv.convertir_a_fraccion(F(1, 1001)), "1/1001")
        self.assertEqual(conv.convertir_a_fraccion(0.0004), "1/2500")
        self.assertEqual(conv.convertir_a_fraccion(F(6, 3)), "2")

    def test_decimal_no_oculta_valores_pequenos(self):
        self.assertEqual(conv.formatear_decimal(F(1, 4)), "0.25")
        self.assertEqual(conv.formatear_decimal(F(0)), "0")
        self.assertEqual(conv.formatear_decimal(-0.0), "0")
        self.assertNotEqual(conv.formatear_decimal(F(1, 10**8)), "0")


class EliminacionExactaTests(unittest.TestCase):
    def test_pivote_racional_pequeno_no_se_toma_como_cero(self):
        reducida, _, pivotes = eliminacion_por_filas(
            [[F(1, 10**10), F(1)]], modo="gauss_jordan"
        )
        self.assertEqual(pivotes, [0])
        self.assertEqual(reducida[0], [F(1), F(10**10)])
        self.assertEqual(
            clasificar_sistema(reducida, pivotes), "Sistema Consistente Determinado"
        )

    def test_enteros_y_fracciones_mezclados_permanecen_exactos(self):
        reducida, _, _ = eliminacion_por_filas(
            [[F(1, 2), 2, 1], [3, 4, 2]], modo="gauss_jordan"
        )
        self.assertTrue(all(isinstance(v, F) for fila in reducida for v in fila))
        # x/2 + 2y = 1 y 3x + 4y = 2  ->  x = 0, y = 1/2
        self.assertEqual([fila[-1] for fila in reducida], [F(0), F(1, 2)])

    def test_floats_conservan_la_tolerancia(self):
        reducida, _, pivotes = eliminacion_por_filas(
            [[1e-12, 1.0], [0.0, 0.0]], modo="gauss_jordan"
        )
        self.assertEqual(pivotes, [])
        self.assertEqual(clasificar_sistema(reducida, pivotes), "Sistema Inconsistente")

    def test_sistema_exacto_completo(self):
        resultado = enrutar_resolucion_matricial(
            [[F(1), F(1, 3)], [F(2), F(-1)]],
            vector_b=[F(1), F(1, 7)],
            metodo="gauss",
        )
        self.assertEqual(resultado["clasificacion"], "Sistema Consistente Determinado")
        x = resultado["solucion"]
        self.assertTrue(all(isinstance(v, F) for v in x))
        original = [[F(1), F(1, 3), F(1)], [F(2), F(-1), F(1, 7)]]
        self.assertTrue(verificar_solucion(original, x))
        self.assertFalse(verificar_solucion(original, [x[0] + F(1, 10**12), x[1]]))


class InversaExactaTests(unittest.TestCase):
    def test_inversa_de_fracciones_es_exacta(self):
        inversa = invertir_matriz_gauss_jordan([[F(1), F(2)], [F(3), F(4)]])
        self.assertEqual(inversa, [[F(-2), F(1)], [F(3, 2), F(-1, 2)]])
        self.assertTrue(all(isinstance(v, F) for fila in inversa for v in fila))

    def test_pivote_exacto_pequeno_es_invertible(self):
        inversa = invertir_matriz_gauss_jordan([[F(1, 10**12), F(0)], [F(0), F(1)]])
        self.assertEqual(inversa[0][0], F(10**12))

    def test_singular_exacta_se_detecta(self):
        with self.assertRaisesRegex(ValueError, "no es invertible"):
            invertir_matriz_gauss_jordan([[F(1), F(2)], [F(2), F(4)]])

    def test_producto_por_la_inversa_es_identidad_exacta(self):
        a = [[F(1, 3), F(2)], [F(5), F(-1, 7)]]
        producto = multiplicar_matrices(a, invertir_matriz_gauss_jordan(a))
        self.assertEqual(producto, [[1, 0], [0, 1]])

    def test_enteros_siguen_en_punto_flotante(self):
        inversa = invertir_matriz_gauss_jordan([[2, 0], [0, 4]])
        self.assertEqual(inversa, [[0.5, 0.0], [0.0, 0.25]])
        self.assertIsInstance(inversa[0][0], float)


class VisualizacionTests(unittest.TestCase):
    def test_sistema_de_ecuaciones_usa_el_formato_recibido(self):
        texto = imprimir_sistema_ecuaciones(
            [[F(1, 2500), F(1), F(1, 3)]], conv.convertir_a_fraccion
        )
        self.assertEqual(texto, "1/2500x1 + x2 = 1/3")


if __name__ == "__main__":
    unittest.main()
