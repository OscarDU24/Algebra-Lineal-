from fractions import Fraction
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


class FormatoSistemasProfesorTests(unittest.TestCase):
    BANCO = (
        ([[-3, -1, 4, 5], [3, 4, -2, 3], [-4, 3, -1, 2], [-2, -4, 2, 5]],
         [-6, 16, -12, -12], [4, 2, 2, 0]),
        ([[-1, -1, 3, -2], [6, 4, 5, -1], [1, -1, 2, 3], [0, -3, 6, -2]],
         [-18, 21, 9, -21], [5, 1, -2, 3]),
        ([[6, 2, 6, 6], [-2, 5, -3, -1], [-2, -3, 1, 4], [-2, 6, 1, 6]],
         [-18, 21, -13, 10], [-2, 3, 0, -2]),
        ([[-2, 2, 0, -2], [-1, -2, -4, -2], [2, 3, 4, 2], [1, 2, 5, -2]],
         [-2, -25, 31, 6], [1, 5, 1, 5]),
        ([[1, 4, -1, 3], [3, -2, 1, 3], [-3, 4, 6, 3], [-1, 3, 4, 1]],
         [6, 22, 41, 22], [0, -1, 5, 5]),
        ([[3, 3, 5, 6], [-1, 6, -4, 2], [1, -1, 2, 6], [2, -2, 4, 0]],
         [8, -6, -7, 10], [4, 1, 1, -2]),
        ([[-4, -3, 2, -2], [6, 3, 2, -3], [-3, -1, 3, -2], [4, -1, -2, 4]],
         [-26, 21, -21, 32], [5, 0, 0, 3]),
        ([[0, 0, -2, -2], [-2, 2, -2, 5], [0, -1, -3, 2], [-4, 6, -4, 5]],
         [8, -22, -7, -26], [0, -1, 0, -4]),
        ([[0, 0, 2, 4], [6, -4, -2, 5], [-4, 1, 1, 2], [0, 0, 0, 2]],
         [8, 11, -11, 2], [5, 5, 2, 1]),
        ([[-2, 0, 3, 4], [4, 6, 3, 2], [5, -2, 3, 2], [2, -3, -2, -1]],
         [7, 21, 42, 8], [5, -2, 3, 2]),
    )

    def test_banco_de_diez_sistemas_incluye_procedimiento_y_verificacion(self):
        for numero, (matriz, vector, solucion) in enumerate(self.BANCO, start=1):
            with self.subTest(ejercicio=numero):
                matriz_exacta = [
                    [Fraction(valor) for valor in fila]
                    for fila in matriz
                ]
                vector_exacto = [Fraction(valor) for valor in vector]
                texto = op_sis.resolver_sistema_detallado_a_string(
                    matriz_exacta,
                    vector_exacto,
                )

                self.assertIn("Incógnitas: x, y, z, w", texto)
                self.assertIn("Forma matricial: A·X = B", texto)
                self.assertIn("Matriz aumentada inicial [A | B]", texto)
                self.assertIn("PROCEDIMIENTO POR ELIMINACIÓN DE GAUSS-JORDAN", texto)
                self.assertIn("det(A) =", texto)
                self.assertIn("A es invertible y el sistema tiene solución única.", texto)
                self.assertIn("rango(A) = 4", texto)
                self.assertIn("rango([A | B]) = 4", texto)
                self.assertIn("Clasificación: Sistema Consistente Determinado.", texto)
                self.assertIn("Comprobación exitosa: A·X = B.", texto)
                for nombre, valor in zip(("x", "y", "z", "w"), solucion):
                    self.assertIn(f"{nombre} = {valor}", texto)
                for ecuacion in range(1, 5):
                    self.assertIn(f"Ecuación {ecuacion}:", texto)

    def test_metodos_alternativos_conservan_procedimiento_y_verificacion(self):
        matriz, vector, _ = self.BANCO[0]
        matriz_exacta = [[Fraction(valor) for valor in fila] for fila in matriz]
        vector_exacto = [Fraction(valor) for valor in vector]

        for metodo, encabezado in (
            ("lu", "PROCEDIMIENTO POR FACTORIZACIÓN LU"),
            ("cramer", "PROCEDIMIENTO POR REGLA DE CRAMER"),
        ):
            with self.subTest(metodo=metodo):
                texto = op_sis.resolver_sistema_detallado_a_string(
                    matriz_exacta,
                    vector_exacto,
                    metodo=metodo,
                )
                self.assertIn(encabezado, texto)
                self.assertIn("Forma matricial: A·X = B", texto)
                self.assertIn("Comprobación exitosa: A·X = B.", texto)

    def test_clasifica_sistemas_infinitos_e_incompatibles_por_rangos(self):
        infinitas = op_sis.resolver_sistema_detallado_a_string(
            [[Fraction(1), Fraction(1)], [Fraction(2), Fraction(2)]],
            [Fraction(3), Fraction(6)],
        )
        self.assertIn("rango(A) = 1", infinitas)
        self.assertIn("rango([A | B]) = 1", infinitas)
        self.assertIn("Sistema Consistente Indeterminado", infinitas)
        self.assertIn("Variables libres: y", infinitas)
        self.assertNotIn("Comprobación exitosa", infinitas)

        incompatible = op_sis.resolver_sistema_detallado_a_string(
            [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]],
            [Fraction(1), Fraction(2)],
        )
        self.assertIn("rango(A) = 1", incompatible)
        self.assertIn("rango([A | B]) = 2", incompatible)
        self.assertIn("Sistema Inconsistente", incompatible)
        self.assertNotIn("Comprobación exitosa", incompatible)


if __name__ == "__main__":
    unittest.main()
