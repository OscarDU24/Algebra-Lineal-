import unittest
from fractions import Fraction

from core.determinantes import operaciones_determinantes as op


class OperacionesDeterminantesTests(unittest.TestCase):
    def test_determinante_lu_aplica_signo_por_intercambio(self):
        matriz = [[0, 2], [1, 3]]

        resultado = op.determinante_lu_a_string(matriz, "Fracciones")

        self.assertIn("Intercambios de filas: 1", resultado)
        self.assertIn("Factor de signo: (-1)^1 = -1", resultado)
        self.assertIn("RESULTADO: det(A) = -2", resultado)

    def test_lu_y_cofactores_coinciden_en_matrices_de_varios_ordenes(self):
        matrices = [
            [[7]],
            [[2, 3], [4, 5]],
            [[0, 2, 1], [1, 1, 0], [2, 0, 1]],
            [[1, 2, 3, 4], [2, 0, 1, 3], [4, 1, 0, 2], [3, 2, 1, 0]],
        ]
        for matriz in matrices:
            with self.subTest(orden=len(matriz)):
                lu = op.determinante_lu_a_string(matriz, "Fracciones")
                cofactores = op.determinante_cofactores_a_string(matriz, "Fracciones")
                resultado_lu = lu.split("RESULTADO: det(A) = ")[-1].splitlines()[0]
                resultado_cofactores = cofactores.split("det(A) = ")[-1].splitlines()[0]
                self.assertEqual(resultado_lu, resultado_cofactores)

    def test_determinante_lu_singular_es_cero(self):
        matriz = [[1, 2], [2, 4]]

        resultado = op.determinante_lu_a_string(matriz, "Fracciones")

        self.assertIn("RESULTADO: det(A) = 0", resultado)

    def test_recomendacion_por_orden(self):
        recomendaciones = {
            1: "Cofactores",
            3: "Cofactores",
            4: "LU / Triangulación",
            5: "LU / Triangulación",
        }
        for orden, esperado in recomendaciones.items():
            matriz = [
                [int(fila == columna) for columna in range(orden)]
                for fila in range(orden)
            ]
            with self.subTest(orden=orden):
                informe, recomendado = op.analizar_eficiencia_determinante(matriz)
                self.assertEqual(recomendado, esperado)
                self.assertIn(f"{orden} × {orden}", informe)

    def test_entradas_racionales_y_validacion(self):
        self.assertEqual(op.convertir_entrada("1/3"), Fraction(1, 3))
        with self.assertRaises(ValueError):
            op.convertir_entrada("Bodrio")
        with self.assertRaises(ValueError):
            op.convertir_entrada("1/0")
        with self.assertRaisesRegex(ValueError, "cuadrada"):
            op.analizar_eficiencia_determinante([[1, 2, 3], [4, 5, 6]])

    def test_sarrus_3x3_detalla_operaciones_sustituciones_y_parciales(self):
        resultado = op.determinante_sarrus_a_string(
            [[3, 5, 7], [1, 4, 9], [2, 6, 8]],
            "Fracciones",
        )

        self.assertIn(
            "Operación: (a11*a22*a33 + a21*a32*a13 + a31*a12*a23) - "
            "(a31*a22*a13 + a11*a32*a23 + a21*a12*a33)",
            resultado,
        )
        self.assertIn(
            "Sustitución: (3x4x8 + 1x6x7 + 2x5x9) - "
            "(2x4x7 + 3x6x9 + 1x5x8)",
            resultado,
        )
        self.assertIn("Sumas parciales: (96 + 42 + 90) - (56 + 162 + 40)", resultado)
        self.assertIn("Resultado: 228 - 258 = -30", resultado)
        self.assertIn("RESULTADO: det(A) = -30", resultado)

    def test_sarrus_4x4_coincide_con_lu_en_matrices_con_signos_y_singularidad(self):
        matrices = [
            [[1, 2, 3, 4], [2, 0, 1, 3], [4, 1, 0, 2], [3, 2, 1, 0]],
            [[0, 2, 1, 3], [1, 1, 0, 2], [2, 0, 1, 1], [1, 3, 2, 0]],
            [[1, 2, 3, 4], [2, 4, 6, 8], [3, 1, 0, 2], [4, 0, 1, 3]],
        ]
        for matriz in matrices:
            with self.subTest(matriz=matriz):
                sarrus = op.determinante_sarrus_a_string(matriz, "Fracciones")
                lu = op.determinante_lu_a_string(matriz, "Fracciones")
                resultado_sarrus = sarrus.split("RESULTADO: det(A) = ")[-1].splitlines()[0]
                resultado_lu = lu.split("RESULTADO: det(A) = ")[-1].splitlines()[0]
                self.assertEqual(resultado_sarrus, resultado_lu)
                self.assertEqual(sarrus.count("ETAPA "), 3)
                self.assertIn("Matriz extendida:", sarrus)

    def test_sarrus_rechaza_ordenes_no_admitidos(self):
        with self.assertRaisesRegex(ValueError, "3 × 3 y 4 × 4"):
            op.determinante_sarrus_a_string([[1, 2], [3, 4]])
        with self.assertRaisesRegex(ValueError, "3 × 3 y 4 × 4"):
            op.determinante_sarrus_a_string(
                [[int(fila == columna) for columna in range(5)] for fila in range(5)]
            )

    def test_cofactores_muestra_menores_2x2_signos_aportes_y_suma(self):
        resultado = op.determinante_cofactores_a_string(
            [[1, 2, 3], [0, 4, 5], [1, 0, 6]],
            "Fracciones",
        )

        self.assertIn("Elemento a1,1 = 1 (Signo: +1)", resultado)
        self.assertIn("Submatriz M1,1:\n[ 4   5 ]\n[ 0   6 ]", resultado)
        self.assertIn("Operación: det(M1,1) = (4 * 6) - (5 * 0) = 24 - 0 = 24", resultado)
        self.assertIn("Aporte: 1 * +1 * 24 = 24", resultado)
        self.assertIn("Elemento a1,2 = 2 (Signo: -1)", resultado)
        self.assertIn("Aporte: 2 * -1 * -5 = 10", resultado)
        self.assertIn("Suma final de aportes: 24 + 10 - 12 = 22", resultado)
        self.assertIn("det(A) = 22", resultado)


if __name__ == "__main__":
    unittest.main()
