import unittest

from core.metodos_numericos.biseccion import (
    COLUMNAS_TABLA,
    formatear_tabla,
    resolver_biseccion,
)
from core.metodos_numericos.operaciones_errores import (
    calcular_errores,
    demostrar_punto_flotante,
    propagar_error,
    simular_truncamiento_redondeo,
)
from core.metodos_numericos.verificacion_matriz import (
    comparar_inversas,
    matriz_hilbert,
    parsear_matriz,
)


class BiseccionTests(unittest.TestCase):
    def test_biseccion_retorna_tabla_con_columnas_requeridas_y_contraste_scipy(self):
        resultado = resolver_biseccion("x**3 - x - 2", 1, 2, 1e-8)

        self.assertEqual(resultado["columnas"], COLUMNAS_TABLA)
        self.assertGreater(len(resultado["tabla"]), 0)
        self.assertTrue(all(len(fila) == 8 for fila in resultado["tabla"]))
        self.assertAlmostEqual(resultado["raiz"], 1.5213797, places=6)
        self.assertLess(resultado["diferencia_absoluta"], 1e-7)
        self.assertIn("Iteración", formatear_tabla(resultado))
        self.assertIn("Ea (%)", formatear_tabla(resultado))

    def test_biseccion_calcula_estimacion_teorica_de_iteraciones(self):
        resultado = resolver_biseccion("x", -1, 1, 0.125)

        self.assertEqual(resultado["iteraciones_teoricas"], 4)
        self.assertEqual(resultado["criterio_paro"], "raíz exacta")
        self.assertEqual(resultado["raiz"], 0)

    def test_biseccion_rechaza_intervalo_sin_cambio_de_signo(self):
        with self.assertRaisesRegex(ValueError, "cambio de signo"):
            resolver_biseccion("x**2 + 1", -1, 1, 1e-6)

    def test_biseccion_valida_intervalo_tolerancia_y_funcion(self):
        casos = [
            ("x", 2, 1, 1e-6, "a < b"),
            ("x", 1, 2, 0, "mayor que cero"),
            ("x", float("inf"), 2, 1e-6, "finito"),
            ("x", 1, 2, float("nan"), "finito"),
            ("__import__('os')", 1, 2, 1e-6, "permitida"),
        ]
        for funcion, a, b, tol, mensaje in casos:
            with self.subTest(funcion=funcion, a=a, b=b, tol=tol):
                with self.assertRaisesRegex(ValueError, mensaje):
                    resolver_biseccion(funcion, a, b, tol)

    def test_formatea_tabla_vacia_cuando_la_raiz_esta_en_un_extremo(self):
        resultado = resolver_biseccion("x - 1", 1, 2, 1e-6)

        self.assertEqual(resultado["tabla"], [])
        self.assertIn("Iteración", formatear_tabla(resultado))


class OperacionesErroresTests(unittest.TestCase):
    def test_calcula_errores_absoluto_relativo_y_porcentual(self):
        resultado = calcular_errores(9.8, 10)

        self.assertAlmostEqual(resultado["error_absoluto"], 0.2)
        self.assertAlmostEqual(resultado["error_relativo"], 0.02)
        self.assertAlmostEqual(resultado["error_porcentual"], 2)

    def test_error_relativo_indefinido_si_referencia_cero(self):
        resultado = calcular_errores(1, 0)
        self.assertIsNone(resultado["error_relativo"])
        self.assertIsNone(resultado["error_porcentual"])

    def test_propaga_error_y_compara_con_cambio_finito(self):
        resultado = propagar_error("x**2", 2, 0.01)

        self.assertAlmostEqual(resultado["derivada_aproximada"], 4, places=5)
        self.assertAlmostEqual(resultado["delta_y_aproximado"], 0.04, places=5)
        self.assertAlmostEqual(resultado["delta_y_exacto"], 0.0401, places=8)
        self.assertAlmostEqual(
            resultado["error_absoluto_aproximacion"], 0.0001, places=6
        )

    def test_compara_truncamiento_y_redondeo(self):
        resultado = simular_truncamiento_redondeo(3.146, 2)

        self.assertEqual(resultado["truncado"], 3.14)
        self.assertEqual(resultado["redondeado"], 3.15)
        self.assertGreater(resultado["error_truncamiento"], 0)
        self.assertGreater(resultado["error_redondeo"], 0)

    def test_demostracion_float32_muestra_overflow_y_underflow(self):
        resultado = demostrar_punto_flotante()

        self.assertNotEqual(resultado["suma_0_1_0_2"], 0.3)
        self.assertGreater(resultado["epsilon_float64"], 0)
        self.assertTrue(resultado["overflow_es_infinito"])
        self.assertTrue(resultado["underflow_es_cero"])


class VerificacionMatrizTests(unittest.TestCase):
    def test_compara_inversa_exacta_flotante_y_numpy(self):
        matriz = parsear_matriz("2 1\n1 2")
        resultado = comparar_inversas(matriz)

        self.assertAlmostEqual(float(resultado["inversa_exacta"][0][0]), 2 / 3)
        self.assertAlmostEqual(resultado["inversa_float"][0][0], 2 / 3)
        self.assertLess(resultado["residuo_gj"], 1e-12)
        self.assertLess(resultado["residuo_numpy"], 1e-12)
        self.assertGreaterEqual(resultado["condicion"], 1)

    def test_hilbert_muestra_condicionamiento_mayor(self):
        resultado = comparar_inversas(matriz_hilbert(5))

        self.assertGreater(resultado["condicion"], 1e5)
        self.assertTrue(
            all(
                valor.denominator == 1
                for fila in resultado["inversa_exacta"]
                for valor in fila
            )
        )

    def test_rechaza_matriz_no_cuadrada_y_singular(self):
        with self.assertRaisesRegex(ValueError, "cuadrada"):
            parsear_matriz("1 2\n3")
        with self.assertRaisesRegex(ValueError, "singular"):
            comparar_inversas([[1, 2], [2, 4]])


if __name__ == "__main__":
    unittest.main()
