"""Regresiones de Límites, Sistemas numéricos y mensajes de validación."""

import unittest
from decimal import Decimal

from core.limites.operaciones_limites import calcular_limite
from core.metodos_numericos.biseccion import _crear_funcion
from core.sistemas_numericos import operaciones_numericas as num


def _resultado(funcion, punto, direccion="bilateral"):
    salida = calcular_limite(funcion, punto, direccion)
    if salida.startswith("ERROR"):
        return salida
    return next(l for l in salida.splitlines() if l.startswith("[>]"))


class LimitesTests(unittest.TestCase):
    def test_limites_finitos(self):
        casos = [
            ("sin(x)/x", "0", "≈ 1"),
            ("(x^2-1)/(x-1)", "1", "≈ 2"),
            ("(1-cos(x))/x^2", "0", "≈ 0.5"),
            ("(1+1/x)^x", "inf", "≈ 2.71828"),
            ("2x+1", "3", "≈ 7"),
            ("x^2", "pi/2", "≈ 2.4674"),
            ("x^2", "1e10", "≈ 1e+20"),
        ]
        for funcion, punto, esperado in casos:
            with self.subTest(funcion=funcion, punto=punto):
                self.assertIn(f"lím f(x) {esperado}", _resultado(funcion, punto))

    def test_convergencia_lenta_hacia_cero(self):
        self.assertIn("lím f(x) ≈ 0", _resultado("sqrt(x)", "0", "derecha"))
        self.assertIn("lím f(x) ≈ 0", _resultado("exp(-x)", "inf"))

    def test_divergencias_no_se_presentan_como_numeros(self):
        self.assertIn("= +∞", _resultado("1/x^2", "0"))
        self.assertIn("= +∞", _resultado("x", "inf"))
        self.assertIn("= +∞", _resultado("exp(x)", "inf"))
        self.assertIn("= +∞", _resultado("1/x", "0", "derecha"))
        self.assertIn("= -∞", _resultado("1/x", "0", "izquierda"))

    def test_laterales_distintos(self):
        resultado = _resultado("abs(x)/x", "0")
        self.assertIn("NO existe", resultado)
        self.assertIn("izquierda ≈ -1", resultado)
        self.assertIn("derecha ≈ 1", resultado)
        self.assertIn("NO existe", _resultado("1/x", "0"))
        self.assertIn("NO existe", _resultado("tan(x)", "pi/2"))

    def test_casos_sin_estimacion_lo_dicen(self):
        self.assertIn("no se estabiliza", _resultado("sin(1/x)", "0", "derecha"))
        self.assertIn("no está definida", _resultado("sqrt(x)", "0", "izquierda"))

    def test_precision_no_se_pierde_por_redondeo(self):
        self.assertIn("1e-10", _resultado("x^2", "1e-5"))

    def test_errores_son_especificos(self):
        self.assertIn("exponentes", _resultado("10**10**10", "0"))
        self.assertIn("no es válido", _resultado("x", "hola"))
        self.assertIn("con paréntesis", _resultado("sin", "0"))
        self.assertTrue(_resultado("x", "").startswith("ERROR"))
        self.assertTrue(_resultado("x.real", "0").startswith("ERROR"))


class MensajesEvaluadorTests(unittest.TestCase):
    def test_mensajes_de_validacion_llegan_al_estudiante(self):
        casos = [
            ("x^2000", "exponentes"),
            ("y + 1", "«y» no está permitido"),
            ("cos", "con paréntesis"),
            ("(x + 1", "estructura incompleta"),
            ("x + * 2", "error de sintaxis"),
        ]
        for funcion, mensaje in casos:
            with self.subTest(funcion=funcion):
                with self.assertRaisesRegex(ValueError, mensaje):
                    _crear_funcion(funcion)

    def test_mensajes_de_dominio_explican_el_motivo(self):
        casos = [
            ("sqrt(x)", -1, "raíz cuadrada"),
            ("ln(x)", 0, "logaritmo"),
            ("1/x", 0, "división entre cero"),
            ("x^0.5", -8, "complejo"),
        ]
        for funcion, x, mensaje in casos:
            with self.subTest(funcion=funcion):
                with self.assertRaisesRegex(ValueError, mensaje):
                    _crear_funcion(funcion)(x)


class SistemasNumericosTests(unittest.TestCase):
    def test_enteros_grandes_se_convierten_exactamente(self):
        texto = "9" * 30
        binario, _ = num.convertir_decimal_a_base(num.parsear_decimal(texto), 2, "Binario")
        self.assertEqual(int(binario, 2), int(texto))

    def test_parte_entera_grande_con_fraccion(self):
        numero = num.parsear_decimal("123456789012345678901234567890.5")
        hexadecimal, _ = num.convertir_decimal_a_base(numero, 16, "Hexadecimal")
        entero, fraccion = hexadecimal.split(".")
        self.assertEqual(int(entero, 16), 123456789012345678901234567890)
        self.assertEqual(fraccion, "8")

    def test_parseo_exacto(self):
        self.assertEqual(num.parsear_decimal("156"), 156)
        self.assertEqual(num.parsear_decimal("1e3"), 1000)
        self.assertEqual(num.parsear_decimal("45.750"), Decimal("45.75"))
        self.assertEqual(num.convertir_decimal_a_base(Decimal("45.75"), 2, "B")[0], "101101.11")
        self.assertEqual(num.convertir_decimal_a_base(Decimal("45.75"), 10, "D")[0], "45.75")

    def test_parseo_rechaza_entradas_invalidas(self):
        casos = [
            ("", "Debes ingresar"),
            ("abc", "no es un número"),
            ("inf", "finito"),
            ("1e400", "demasiado grande"),
            ("1e-400", "demasiados ceros"),
        ]
        for texto, mensaje in casos:
            with self.subTest(texto=texto):
                with self.assertRaisesRegex(ValueError, mensaje):
                    num.parsear_decimal(texto)


if __name__ == "__main__":
    unittest.main()
