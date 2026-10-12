import unittest

from core.determinantes import operaciones_determinantes as op_det
from core.sistemas import operaciones_sistemas as op_sis


class ResolucionSistemasPorMetodosTests(unittest.TestCase):
    def test_lu_resuelve_con_pivoteo_y_muestra_sustituciones(self):
        matriz = [[0, 2, 1], [1, 1, 0], [2, 0, 1]]
        vector = [7, 3, 5]

        resultado = op_sis.resolver_sistema_lu_a_string(
            matriz, vector, "Fracciones"
        )

        self.assertIn("Vector permutado P·b:", resultado)
        self.assertIn("SUSTITUCIÓN HACIA ADELANTE", resultado)
        self.assertIn("SUSTITUCIÓN HACIA ATRÁS", resultado)
        self.assertIn("SOLUCIÓN:\n[ 1   2   3 ]", resultado)

    def test_pivoteo_posterior_conserva_multiplicadores_previos_de_l(self):
        matriz = [[2, 1, 1], [4, 4, 2], [8, 7, 7]]
        vector = [7, 18, 43]

        determinante_lu = op_det.determinante_lu_a_string(matriz, "Fracciones")
        determinante_cofactores = op_det.determinante_cofactores_a_string(
            matriz, "Fracciones"
        )
        solucion = op_sis.resolver_sistema_lu_a_string(
            matriz, vector, "Fracciones"
        )

        resultado_lu = determinante_lu.split("RESULTADO: det(A) = ")[-1].splitlines()[0]
        resultado_cofactores = determinante_cofactores.split("det(A) = ")[-1].splitlines()[0]
        self.assertEqual(resultado_lu, resultado_cofactores)
        self.assertIn("Intercambios de filas: 2", determinante_lu)
        self.assertIn("SOLUCIÓN:\n[ 1   2   3 ]", solucion)

    def test_cramer_resuelve_y_detecta_determinante_principal_cero(self):
        resultado = op_sis.resolver_sistema_cramer_a_string(
            [[2, 1], [1, 1]], [5, 3], "Fracciones"
        )
        self.assertIn("SOLUCIÓN:\n[ 2   1 ]", resultado)

        singular = op_sis.resolver_sistema_cramer_a_string(
            [[1, 2], [2, 4]], [3, 6], "Fracciones"
        )
        self.assertIn("D = 0", singular)
        self.assertIn("no permite obtener una solución única", singular)

    def test_lu_rechaza_sistema_singular(self):
        with self.assertRaisesRegex(ValueError, "singular"):
            op_sis.resolver_sistema_lu_a_string([[1, 2], [2, 4]], [3, 6])

    def test_inversa_gauss_jordan_es_exacta_y_muestra_escalonamiento(self):
        resultado = op_sis.invertir_matriz_a_string(
            [[2, 1], [1, 1]],
            "Fracciones",
        )

        self.assertIn("Matriz aumentada inicial [A | I]", resultado)
        self.assertIn("Normalizar F1", resultado)
        self.assertIn("Eliminar la entrada", resultado)
        self.assertIn("MATRIZ INVERSA A⁻¹:", resultado)
        self.assertIn("[ 1   -1 ]\n[ -1   2 ]", resultado)

    def test_inversa_rechaza_matriz_rectangular_y_singular(self):
        with self.assertRaisesRegex(ValueError, "cuadradas"):
            op_sis.invertir_matriz_a_string([[1, 2, 3], [4, 5, 6]])
        with self.assertRaisesRegex(ValueError, "singular"):
            op_sis.invertir_matriz_a_string([[1, 2], [2, 4]])

    def test_gauss_jordan_mantiene_resultado_compatible_y_opcionalmente_traza(self):
        matriz = [[1, 2], [3, 4]]
        reducida, pivotes = op_sis.gauss_jordan(matriz)
        reducida_con_traza, pivotes_con_traza, pasos = op_sis.gauss_jordan(
            matriz, devolver_pasos=True
        )

        self.assertEqual((reducida, pivotes), (reducida_con_traza, pivotes_con_traza))
        self.assertGreater(len(pasos), 1)

    def test_resolutores_quedaron_en_el_modulo_de_sistemas(self):
        self.assertTrue(callable(op_sis.resolver_sistema_lu_a_string))
        self.assertTrue(callable(op_sis.resolver_sistema_cramer_a_string))
        self.assertFalse(hasattr(op_det, "resolver_sistema_lu_a_string"))
        self.assertFalse(hasattr(op_det, "resolver_sistema_cramer_a_string"))


if __name__ == "__main__":
    unittest.main()
