import unittest
from fractions import Fraction

from core.lineal.solucion import invertir_matriz_gauss_jordan
from core.matriciales import particiones_logica as particiones


class OperacionesMatricesParticionadasTests(unittest.TestCase):
    def test_particiona_y_reensambla_matriz_rectangular(self):
        matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        bloques = particiones.particionar_matriz(matriz, 1, 2)

        self.assertEqual(bloques["A11"], [[1, 2]])
        self.assertEqual(bloques["A12"], [[3]])
        self.assertEqual(bloques["A21"], [[4, 5], [7, 8]])
        self.assertEqual(bloques["A22"], [[6], [9]])
        self.assertEqual(particiones.reensamblar_bloques(bloques), matriz)

    def test_rechaza_cortes_en_bordes(self):
        with self.assertRaisesRegex(ValueError, "corte horizontal"):
            particiones.particionar_matriz([[1, 2], [3, 4]], 2, 1)
        with self.assertRaisesRegex(ValueError, "corte vertical"):
            particiones.particionar_matriz([[1, 2], [3, 4]], 1, 0)

    def test_suma_bloques(self):
        a = particiones.particionar_matriz([[1, 2], [3, 4]], 1, 1)
        b = particiones.particionar_matriz([[5, 6], [7, 8]], 1, 1)

        resultado = particiones.suma_bloques(a, b)

        self.assertEqual(particiones.reensamblar_bloques(resultado), [[6, 8], [10, 12]])

    def test_suma_rechaza_bloques_no_conformables(self):
        a = particiones.particionar_matriz([[1, 2], [3, 4]], 1, 1)
        b = particiones.particionar_matriz([[1, 2, 3], [4, 5, 6]], 1, 1)

        with self.assertRaisesRegex(ValueError, "mismas dimensiones"):
            particiones.suma_bloques(a, b)

    def test_multiplicacion_por_bloques(self):
        a = particiones.particionar_matriz([[1, 2, 3], [4, 5, 6]], 1, 1)
        b = particiones.particionar_matriz([[7, 8], [9, 10], [11, 12]], 1, 1)

        resultado = particiones.multiplicacion_bloques(a, b)

        self.assertEqual(
            particiones.reensamblar_bloques(resultado),
            [[58, 64], [139, 154]],
        )

    def test_multiplicacion_omite_producto_de_bloques_nulos(self):
        a = particiones.particionar_matriz([[0, 0], [1, 2]], 1, 1)
        b = particiones.particionar_matriz([[3, 4], [5, 6]], 1, 1)
        producto_original = particiones._producto_matrices
        productos = []

        def registrar_producto(matriz_a, matriz_b):
            productos.append((matriz_a, matriz_b))
            return producto_original(matriz_a, matriz_b)

        particiones._producto_matrices = registrar_producto
        try:
            resultado = particiones.multiplicacion_bloques(a, b)
        finally:
            particiones._producto_matrices = producto_original

        self.assertEqual(particiones.reensamblar_bloques(resultado), [[0, 0], [13, 16]])
        self.assertEqual(len(productos), 4)

    def test_multiplicacion_rechaza_particiones_incompatibles(self):
        a = {
            "A11": [[1]],
            "A12": [[2, 3]],
            "A21": [[4]],
            "A22": [[5, 6]],
        }
        b = {
            "A11": [[1]],
            "A12": [[2]],
            "A21": [[3], [4], [5]],
            "A22": [[6], [7], [8]],
        }
        with self.assertRaisesRegex(ValueError, "partición interna"):
            particiones.multiplicacion_bloques(a, b)

    def test_inversa_triangular_superior_por_bloques(self):
        bloques = particiones.particionar_matriz([[2, 1], [0, 3]], 1, 1)

        inversa = particiones.inversa_triangular_bloques(
            bloques["A11"],
            bloques["A12"],
            bloques["A22"],
            invertir_matriz_gauss_jordan,
        )

        matriz = particiones.reensamblar_bloques(inversa)
        self.assertEqual(matriz, [[0.5, -1 / 6], [0.0, 1 / 3]])

    def test_inversa_detecta_bloque_singular_y_conformabilidad(self):
        with self.assertRaisesRegex(ValueError, "no es invertible"):
            particiones.inversa_triangular_bloques(
                [[0]], [[1]], [[2]], invertir_matriz_gauss_jordan
            )
        with self.assertRaisesRegex(ValueError, "A12"):
            particiones.inversa_triangular_bloques(
                [[1, 0], [0, 1]], [[1]], [[1]], invertir_matriz_gauss_jordan
            )

    def test_admite_datos_racionales_nativos(self):
        a = particiones.particionar_matriz(
            [[Fraction(1, 2), Fraction(1, 3)],
             [Fraction(1, 4), Fraction(1, 5)]],
            1,
            1,
        )
        b = particiones.particionar_matriz(
            [[Fraction(1, 2), Fraction(2, 3)],
             [Fraction(3, 4), Fraction(4, 5)]],
            1,
            1,
        )

        resultado = particiones.suma_bloques(a, b)

        self.assertEqual(particiones.reensamblar_bloques(resultado)[0], [1, 1])


if __name__ == "__main__":
    unittest.main()
