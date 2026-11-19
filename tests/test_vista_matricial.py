from fractions import Fraction
import unittest

from core.determinantes.operaciones_determinantes import determinante_lu_valor
from core.lineal.solucion import invertir_matriz_gauss_jordan, multiplicar_matrices
from core.ui.vista_matriz import VistaMatriz, _formatear_resultado_matriz_singular
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


class DeterminanteEInversaMatrizPuraTests(unittest.TestCase):
    BANCO = (
        ([[-4, 5, -4, 5], [-3, 3, -1, 3], [-3, 5, 1, -1], [1, -4, -1, -3]], -146),
        ([[3, -3, -1, 4], [0, -3, 0, 6], [0, 0, -2, 2], [-3, -3, 3, 3]], -54),
        ([[-3, -4, 2, 0], [1, 6, -3, 3], [1, 2, 0, 5], [3, 4, 3, -2]], 348),
        ([[-2, 0, -4, -1], [-3, -3, -3, 0], [6, -3, 4, 2], [-2, -3, -1, 2]], -99),
        ([[1, -3, 4, 5], [2, 4, 4, 2], [0, -3, -4, -1], [0, -3, 3, -3]], 342),
        ([[3, -3, 2, -3], [3, 3, 1, 5], [1, 6, 6, -1], [3, -2, 5, 1]], 844),
        ([[5, 6, -2, 4], [-1, 4, 1, 3], [1, 6, 3, 0], [6, 0, -1, 6]], 728),
        ([[5, 6, 1, 2], [6, 6, 2, -1], [-3, -3, 4, -2], [-3, 1, 3, 6]], 75),
        ([[2, -1, -3, 5], [-3, -4, 0, 1], [0, -3, -1, 6], [5, 4, 1, 2]], 55),
        ([[-4, -2, -4, 5], [-2, 2, 1, 4], [2, 0, 2, 4], [5, 3, -2, -4]], -654),
    )

    def test_banco_de_diez_matrices_tiene_inversa_exacta_y_producto_identidad(self):
        identidad = [
            [Fraction(int(fila == columna)) for columna in range(4)]
            for fila in range(4)
        ]
        for numero, (matriz, determinante_esperado) in enumerate(self.BANCO, start=1):
            with self.subTest(ejercicio=numero):
                matriz_exacta = [
                    [Fraction(valor) for valor in fila]
                    for fila in matriz
                ]
                self.assertEqual(
                    determinante_lu_valor(matriz_exacta),
                    Fraction(determinante_esperado),
                )
                inversa = invertir_matriz_gauss_jordan(matriz_exacta)
                self.assertEqual(
                    multiplicar_matrices(matriz_exacta, inversa),
                    identidad,
                )

    def test_salida_de_inversa_incluye_determinante_y_justificacion(self):
        vista = type("VistaSimulada", (), {})()
        vista._formatear_valor = lambda valor, _formato: str(valor)
        vista._matriz_cuadrada_a_string = lambda _matriz, _formato: "MATRIZ"
        vista._matriz_aumentada_inversa_a_string = (
            lambda _matriz, _dimension, _formato: "AUMENTADA"
        )
        vista._descripcion_paso_inversa = lambda _operacion, _formato: "PASO"
        vista._escribir_en_visor = lambda texto: setattr(vista, "salida", texto)

        VistaMatriz.mostrar_matriz_inversa(
            vista,
            [[Fraction(1)]],
            [[Fraction(1)]],
            [],
            [[Fraction(1)]],
            "fr",
            Fraction(1),
            "det(A) = 1",
        )

        self.assertIn("DETERMINANTE Y EXISTENCIA DE LA INVERSA", vista.salida)
        self.assertIn("det(A) = 1", vista.salida)
        self.assertIn("A es invertible y existe A⁻¹.", vista.salida)
        self.assertIn("Comprobación: A · A⁻¹ = Matriz Identidad (I)", vista.salida)

    def test_matriz_singular_explica_por_que_no_existe_inversa(self):
        salida = _formatear_resultado_matriz_singular("det(A) = 0")

        self.assertIn("det(A) = 0", salida)
        self.assertIn("A es singular y no existe A⁻¹.", salida)


if __name__ == "__main__":
    unittest.main()
