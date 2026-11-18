"""Regresiones del evaluador algebraico compartido (límites y métodos numéricos)."""

import math
import subprocess
import sys
import unittest
from pathlib import Path

from core.limites import operaciones_limites as op_lim
from core.metodos_numericos.biseccion import _crear_funcion

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]


class FuncionesElementalesTests(unittest.TestCase):
    def test_raiz_cuadrada_es_exacta_en_magnitudes_grandes(self):
        for valor in (1e20, 1e100, 1e300, 2.0, 1e-300):
            with self.subTest(valor=valor):
                self.assertEqual(op_lim._raiz_cuadrada(valor), math.sqrt(valor))

    def test_raiz_cuadrada_rechaza_negativos(self):
        with self.assertRaises(ValueError):
            op_lim._raiz_cuadrada(-1.0)

    def test_exponencial_es_precisa_para_argumentos_grandes(self):
        for valor in (-30.0, 20.0, 50.0, 700.0):
            with self.subTest(valor=valor):
                self.assertAlmostEqual(
                    op_lim._exponencial(valor) / math.exp(valor), 1.0, places=14
                )

    def test_exponencial_desbordada_se_reporta_como_infinito(self):
        self.assertEqual(op_lim._exponencial(1000.0), math.inf)

    def test_trigonometricas_con_argumentos_grandes(self):
        for valor in (100.0, 1e8, 1e300):
            with self.subTest(valor=valor):
                self.assertEqual(op_lim._seno(valor), math.sin(valor))
                self.assertEqual(op_lim._coseno(valor), math.cos(valor))

    def test_reducir_angulo_queda_en_menos_pi_pi(self):
        for valor in (1e8, -1e300, 7.0):
            with self.subTest(valor=valor):
                self.assertLessEqual(abs(op_lim._reducir_angulo(valor)), math.pi)

    def test_trigonometrica_de_argumento_no_finito_informa_error(self):
        with self.assertRaises(ValueError):
            op_lim._seno(math.inf)

    def test_tangente_conserva_indefinicion_en_pi_medios(self):
        with self.assertRaises(ValueError):
            op_lim._tangente(math.pi / 2)


class EvaluadorCompartidoTests(unittest.TestCase):
    def test_metodos_numericos_evaluan_sqrt_y_exp_correctamente(self):
        self.assertEqual(_crear_funcion("sqrt(x)")(1e20), 1e10)
        self.assertAlmostEqual(
            _crear_funcion("exp(x)")(50) / math.exp(50), 1.0, places=14
        )

    def test_exponencial_desbordada_es_error_en_metodos_numericos(self):
        with self.assertRaises(ValueError):
            _crear_funcion("exp(x)")(1000)

    def test_seno_de_argumento_enorme_no_congela_la_evaluacion(self):
        # Se ejecuta en un proceso aparte: antes de la corrección este caso
        # entraba en un bucle infinito y congelaba la interfaz.
        codigo = (
            "from core.metodos_numericos.biseccion import _crear_funcion\n"
            "from core.limites.operaciones_limites import calcular_limite\n"
            "_crear_funcion('sin(1e300) + x')(1)\n"
            "_crear_funcion('cos(1e9x)')(10)\n"
            "calcular_limite('sin(1e300*x)', '1')\n"
        )
        resultado = subprocess.run(
            [sys.executable, "-B", "-c", codigo],
            cwd=RAIZ_PROYECTO,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(resultado.returncode, 0, resultado.stderr)

    def test_limite_notable_sigue_funcionando(self):
        salida = op_lim.calcular_limite("sin(x)/x", "0")
        self.assertIn("RESULTADO (estimación numérica): lím f(x) ≈ 1\n", salida)


if __name__ == "__main__":
    unittest.main()
