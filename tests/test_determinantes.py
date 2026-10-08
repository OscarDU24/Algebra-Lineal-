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

    def test_resuelve_sistema_con_pivoteo_y_muestra_sustituciones(self):
        matriz = [[0, 2, 1], [1, 1, 0], [2, 0, 1]]
        vector = [7, 3, 5]

        resultado = op.resolver_sistema_lu_a_string(matriz, vector, "Fracciones")

        self.assertIn("Vector permutado P·b:", resultado)
        self.assertIn("SUSTITUCIÓN HACIA ADELANTE", resultado)
        self.assertIn("SUSTITUCIÓN HACIA ATRÁS", resultado)
        self.assertIn("SOLUCIÓN:\n[ 1   2   3 ]", resultado)

    def test_pivoteo_posterior_conserva_multiplicadores_previos_de_l(self):
        matriz = [[2, 1, 1], [4, 4, 2], [8, 7, 7]]
        vector = [7, 18, 43]

        determinante_lu = op.determinante_lu_a_string(matriz, "Fracciones")
        determinante_cofactores = op.determinante_cofactores_a_string(
            matriz, "Fracciones"
        )
        solucion = op.resolver_sistema_lu_a_string(matriz, vector, "Fracciones")

        resultado_lu = determinante_lu.split("RESULTADO: det(A) = ")[-1].splitlines()[0]
        resultado_cofactores = determinante_cofactores.split("det(A) = ")[-1].splitlines()[0]
        self.assertEqual(resultado_lu, resultado_cofactores)
        self.assertIn("Intercambios de filas: 2", determinante_lu)
        self.assertIn("SOLUCIÓN:\n[ 1   2   3 ]", solucion)

    def test_cramer_resuelve_y_detecta_determinante_principal_cero(self):
        resultado = op.resolver_sistema_cramer_a_string(
            [[2, 1], [1, 1]], [5, 3], "Fracciones"
        )
        self.assertIn("SOLUCIÓN:\n[ 2   1 ]", resultado)

        singular = op.resolver_sistema_cramer_a_string(
            [[1, 2], [2, 4]], [3, 6], "Fracciones"
        )
        self.assertIn("D = 0", singular)
        self.assertIn("no permite obtener una solución única", singular)

    def test_determinante_singular_es_cero_y_sistema_singular_error(self):
        matriz = [[1, 2], [2, 4]]

        resultado = op.determinante_lu_a_string(matriz, "Fracciones")

        self.assertIn("RESULTADO: det(A) = 0", resultado)
        with self.assertRaisesRegex(ValueError, "singular"):
            op.resolver_sistema_lu_a_string(matriz, [3, 6])

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


if __name__ == "__main__":
    unittest.main()
