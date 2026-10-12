import unittest

from core.ui.vista_matricial import VistaMatricial


class EntradaSimulada:
    def __init__(self, valor):
        self.valor = valor

    def get(self):
        return self.valor


class ValidacionDimensionesMatricialesTests(unittest.TestCase):
    def test_rechaza_campos_vacios_con_mensaje_de_validacion(self):
        for valor in ("", "   "):
            with self.subTest(valor=valor):
                with self.assertRaisesRegex(
                    ValueError, "enteros positivos"
                ):
                    VistaMatricial._leer_entero_positivo(EntradaSimulada(valor))

    def test_rechaza_valores_no_enteros_o_no_positivos(self):
        for valor in ("Bodrio", "1.5", "0", "-2"):
            with self.subTest(valor=valor):
                with self.assertRaisesRegex(
                    ValueError, "enteros positivos"
                ):
                    VistaMatricial._leer_entero_positivo(EntradaSimulada(valor))

    def test_acepta_entero_positivo(self):
        self.assertEqual(
            VistaMatricial._leer_entero_positivo(EntradaSimulada(" 3 ")),
            3,
        )


if __name__ == "__main__":
    unittest.main()
