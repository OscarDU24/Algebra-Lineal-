import unittest

from core.metodos_numericos.biseccion import (
    COLUMNAS_TABLA,
    _crear_funcion,
    analizar_intervalos,
    formatear_tabla,
    muestrear_funcion,
    resolver_biseccion,
)
from core.metodos_numericos import regla_falsa
from core.metodos_numericos.newton_raphson import resolver_newton_raphson
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
    def test_biseccion_admite_potencias_y_multiplicacion_implicita(self):
        resultado = resolver_biseccion("x^2 - 4", 1, 3, 1e-8)

        self.assertAlmostEqual(resultado["raiz"], 2)

    def test_evaluador_admite_productos_entre_parentesis_y_simbolos_visuales(self):
        evaluar = _crear_funcion("(x + 1)(x - 1) + 2×x − π")

        self.assertAlmostEqual(evaluar(2), 7 - 3.141592653589793)

    def test_evaluador_admite_raiz_escrita_con_simbolo(self):
        evaluar = _crear_funcion("√(x^2)")

        self.assertAlmostEqual(evaluar(-3), 3)

    def test_evaluador_admite_exponentes_unicode_visuales(self):
        evaluar = _crear_funcion("x² + x⁽³⁺¹⁾")

        self.assertAlmostEqual(evaluar(2), 20)

    def test_evaluador_admite_exponente_negativo_unicode(self):
        evaluar = _crear_funcion("e⁻ᵡ")

        self.assertAlmostEqual(evaluar(1), 0.36787944117144233, places=6)

    def test_evaluador_admite_cosecante_secante_y_cotangente(self):
        evaluar_csc = _crear_funcion("csc(pi/2)")
        evaluar_sec = _crear_funcion("sec(0)")
        evaluar_cot = _crear_funcion("cot(pi/4)")
        evaluar_alias = _crear_funcion("cosecante(pi/2) + secante(0) + cotangente(pi/4)")

        self.assertAlmostEqual(evaluar_csc(0), 1)
        self.assertAlmostEqual(evaluar_sec(0), 1)
        self.assertAlmostEqual(evaluar_cot(0), 1)
        self.assertAlmostEqual(evaluar_alias(0), 3)

    def test_evaluador_rechaza_reciprocas_trigonometricas_no_definidas(self):
        for funcion in ("csc(0)", "sec(pi/2)", "cot(0)"):
            with self.subTest(funcion=funcion):
                with self.assertRaises(ValueError):
                    _crear_funcion(funcion)(0)

    def test_evaluador_admite_exponencial_e_elevado_a_x(self):
        evaluar = _crear_funcion("1/(e^x) - x")

        self.assertAlmostEqual(evaluar(0), 1)
        self.assertAlmostEqual(evaluar(1), (1 / 2.718281828459045) - 1)

    def test_biseccion_retorna_raiz_y_tabla_con_columnas_requeridas(self):
        resultado = resolver_biseccion("x**3 - x - 2", 1, 2, 1e-8)

        self.assertEqual(resultado["columnas"], COLUMNAS_TABLA)
        self.assertGreater(len(resultado["tabla"]), 0)
        self.assertTrue(all(len(fila) == 8 for fila in resultado["tabla"]))
        self.assertAlmostEqual(resultado["raiz"], 1.5213797, places=6)
        self.assertLess(abs(resultado["f_raiz"]), 1e-7)
        self.assertIn("Iteración", formatear_tabla(resultado))
        self.assertIn("Ea (%)", formatear_tabla(resultado))

    def test_biseccion_calcula_estimacion_teorica_de_iteraciones(self):
        resultado = resolver_biseccion("x", -1, 1, 0.125)

        self.assertEqual(resultado["iteraciones_teoricas"], 4)
        self.assertEqual(resultado["criterio_paro"], "raíz exacta")
        self.assertEqual(resultado["raiz"], 0)

    def test_tolerancia_se_aplica_al_ancho_del_intervalo_no_al_porcentaje(self):
        resultado = resolver_biseccion(
            "x - 1000000.1",
            900000,
            1100000,
            1,
        )

        self.assertEqual(resultado["criterio_paro"], "ancho del intervalo")
        self.assertEqual(resultado["iteraciones"], resultado["iteraciones_teoricas"])
        self.assertLessEqual(abs(resultado["raiz"] - 1000000.1), 1)

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

    def test_detecta_dos_intervalos_para_funcion_con_dos_raices(self):
        resultado = analizar_intervalos("x**2 - 4", -3, 3, 601)

        self.assertEqual(len(resultado["intervalos"]), 2)
        self.assertLess(resultado["intervalos"][0]["a"], -2)
        self.assertGreaterEqual(resultado["intervalos"][0]["b"], -2)
        self.assertLessEqual(resultado["intervalos"][1]["a"], 2)
        self.assertGreaterEqual(resultado["intervalos"][1]["b"], 2)

    def test_detecta_raiz_que_coincide_con_punto_muestreado(self):
        resultado = analizar_intervalos("x", -1, 1, 5)

        self.assertEqual(len(resultado["intervalos"]), 1)
        intervalo = resultado["intervalos"][0]
        self.assertIn(intervalo["raiz_muestreada"], (intervalo["a"], intervalo["b"]))

    def test_no_conecta_cambio_de_signo_a_traves_de_punto_indefinido(self):
        resultado = analizar_intervalos("1/x", -1, 1, 5)

        self.assertEqual(resultado["intervalos"], [])

    def test_muestrea_funcion_para_graficar_sin_seleccionar_intervalos(self):
        resultado = muestrear_funcion("x", -1, 1, 5)

        self.assertEqual(resultado["x"], [-1.0, -0.5, 0.0, 0.5, 1.0])
        self.assertEqual(resultado["y"], [-1.0, -0.5, 0.0, 0.5, 1.0])
        self.assertNotIn("intervalos", resultado)

    def test_muestreo_marca_como_hueco_los_puntos_no_definidos(self):
        resultado = muestrear_funcion("1/x", -1, 1, 5)

        self.assertIsNone(resultado["y"][2])

    def test_analizar_intervalos_valida_rango_muestras_y_funcion(self):
        casos = [
            ("x", 1, 1, 20, "x_min < x_max"),
            ("x", -1e308, 1e308, 20, "ancho del rango"),
            ("x", -1, 1, 2, "entre 3 y 5000"),
            ("__import__('os')", -1, 1, 20, "permitida"),
            ("sin", -1, 1, 20, "no permitidas"),
        ]
        for funcion, minimo, maximo, muestras, mensaje in casos:
            with self.subTest(funcion=funcion, minimo=minimo, maximo=maximo):
                with self.assertRaisesRegex(ValueError, mensaje):
                    analizar_intervalos(funcion, minimo, maximo, muestras)


class ReglaFalsaTests(unittest.TestCase):
    def test_interpolacion_no_desborda_con_valores_de_funcion_grandes(self):
        punto = regla_falsa.calcular_punto_c(-1, 1, 1e308, -1e308)

        self.assertEqual(punto, 0)

    def test_resuelve_ejemplo_de_elevado_a_menos_x(self):
        resultado = regla_falsa.resolver_regla_falsa(
            "1/(e^x) - x",
            0,
            1,
            0.00001,
            100,
        )

        self.assertTrue(resultado["convergio"])
        self.assertAlmostEqual(resultado["raiz"], 0.56714329, places=7)
        self.assertEqual(
            resultado["criterio_paro"],
            "error relativo aproximado porcentual",
        )
        self.assertTrue(
            all(len(fila) == len(regla_falsa.COLUMNAS_TABLA) for fila in resultado["tabla"])
        )
        self.assertIn("Ea (%)", regla_falsa.formatear_tabla(resultado))

    def test_retorna_raiz_exacta_si_esta_en_un_extremo(self):
        resultado = regla_falsa.resolver_regla_falsa("x - 2", 2, 4, 1e-5, 50)

        self.assertTrue(resultado["convergio"])
        self.assertEqual(resultado["raiz"], 2)
        self.assertEqual(resultado["iteraciones"], 0)
        self.assertEqual(resultado["estado"], "Raíz exacta en a")

    def test_rechaza_intervalo_sin_cambio_de_signo(self):
        with self.assertRaisesRegex(ValueError, "cambio de signo"):
            regla_falsa.resolver_regla_falsa("x^2 + 1", -1, 1, 1e-5, 50)

    def test_no_presenta_ultima_aproximacion_como_raiz_si_no_converge(self):
        resultado = regla_falsa.resolver_regla_falsa(
            "x^10 - 1",
            0,
            2,
            0.00001,
            100,
        )

        self.assertFalse(resultado["convergio"])
        self.assertIsNone(resultado["raiz"])
        self.assertIsNotNone(resultado["aproximacion"])
        self.assertEqual(resultado["estado"], "Máximo de iteraciones alcanzado")

    def test_valida_extremos_tolerancia_maximo_y_funcion(self):
        casos = [
            ("x", 2, 1, 1e-5, 10, "a < b"),
            ("x", 1, 2, 0, 10, "mayor que cero"),
            ("x", float("inf"), 2, 1e-5, 10, "finito"),
            ("x", 1, 2, 1e-5, 0, "entre 1 y 100000"),
            ("x", 1, 2, 1e-5, 2.5, "número entero"),
            ("__import__('os')", 1, 2, 1e-5, 10, "permitidas"),
        ]
        for funcion, a, b, tol, max_iteraciones, mensaje in casos:
            with self.subTest(funcion=funcion, max_iteraciones=max_iteraciones):
                with self.assertRaisesRegex(ValueError, mensaje):
                    regla_falsa.resolver_regla_falsa(
                        funcion, a, b, tol, max_iteraciones
                    )

    def test_maximo_de_iteraciones_vacio_tiene_mensaje_claro(self):
        with self.assertRaisesRegex(ValueError, "Ingrese el máximo de iteraciones"):
            regla_falsa.resolver_regla_falsa("x", -1, 1, 1e-5, "")

    def test_maximo_de_iteraciones_no_entero_tiene_mensaje_claro(self):
        with self.assertRaisesRegex(ValueError, "debe ser un número entero"):
            regla_falsa.resolver_regla_falsa("x", -1, 1, 1e-5, "muchas")

    def test_tolerancia_vacia_tiene_mensaje_claro(self):
        with self.assertRaisesRegex(ValueError, "tolerancia porcentual"):
            regla_falsa.resolver_regla_falsa("x", -1, 1, "", 100)

    def test_maximo_de_iteraciones_acepta_cadena_entera(self):
        resultado = regla_falsa.resolver_regla_falsa("x", -1, 1, 1e-5, "20")

        self.assertEqual(resultado["estado"], "Raíz exacta encontrada")


class NewtonRaphsonTests(unittest.TestCase):
    def test_resuelve_caso_guia_con_derivada_numerica(self):
        resultado = resolver_newton_raphson(
            "x^3 - x - 2",
            1.5,
            1e-8,
            50,
        )

        self.assertTrue(resultado["convergio"])
        self.assertAlmostEqual(resultado["raiz"], 1.521379707, places=7)
        self.assertEqual(resultado["estado"], "Tolerancia por residuo alcanzada")
        self.assertGreater(len(resultado["tabla"]), 0)
        self.assertTrue(all(len(fila) == len(resultado["columnas"]) for fila in resultado["tabla"]))
        self.assertAlmostEqual(resultado["tabla"][0][3], 5.75, places=6)
        self.assertEqual(resultado["metodo_derivada"], "Diferencia finita central")
        detalle = resultado["procedimiento_derivada"][0]
        self.assertAlmostEqual(detalle["h"], 1.5e-5)
        self.assertAlmostEqual(detalle["x_mas_h"], 1.5 + detalle["h"])
        self.assertAlmostEqual(detalle["x_menos_h"], 1.5 - detalle["h"])
        self.assertAlmostEqual(
            detalle["derivada"],
            detalle["diferencia_funcion"] / detalle["divisor"],
        )
        self.assertEqual(len(resultado["procedimiento_derivada"]), resultado["iteraciones"])

    def test_rechaza_derivada_cero(self):
        with self.assertRaisesRegex(ValueError, "derivada es cero"):
            resolver_newton_raphson("x^2 + 1", 0, 1e-8, 20)

    def test_deriva_funcion_con_secante_numerica(self):
        resultado = resolver_newton_raphson("sec(x) - 2", 1, 1e-8, 50)

        self.assertTrue(resultado["convergio"])
        self.assertAlmostEqual(resultado["raiz"], 1.04719755, places=6)


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
