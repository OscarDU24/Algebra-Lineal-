"""Pruebas de la etapa final de UX: preferencias, navegación, ayuda, bienvenida,
ejemplos y copia de resultados. Las que necesitan Tk crean ventanas fuera de la
pantalla y se omiten si no hay escritorio disponible."""

import json
import os
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest import mock

from core.ui import preferencias


class _ConfigTemporal(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self._env = mock.patch.dict(os.environ, {"HEYALGB_CONFIG_DIR": self._dir.name})
        self._env.start()

    def tearDown(self):
        self._env.stop()
        self._dir.cleanup()


class PreferenciasTests(_ConfigTemporal):
    def test_sin_archivo_usa_predeterminadas(self):
        self.assertEqual(preferencias.cargar(), preferencias.PREDETERMINADAS)

    def test_guardar_y_recuperar(self):
        self.assertTrue(preferencias.guardar(mostrar_bienvenida=False, efectos_habilitados=False))
        datos = preferencias.cargar()
        self.assertFalse(datos["mostrar_bienvenida"])
        self.assertFalse(datos["efectos_habilitados"])
        self.assertTrue(datos["musica_habilitada"])

    def test_ultimo_modulo_utilizado_se_guarda_y_recupera(self):
        self.assertTrue(
            preferencias.guardar(ultimo_modulo_utilizado="Métodos Numéricos")
        )
        self.assertEqual(
            preferencias.cargar()["ultimo_modulo_utilizado"], "Métodos Numéricos"
        )

    def test_volumenes_por_defecto_y_validacion_de_rango(self):
        valores = preferencias.cargar()
        self.assertEqual(valores["volumen_musica"], 50)
        self.assertEqual(valores["volumen_efectos"], 45)
        with self.assertLogs("heyalgb.preferencias", level="WARNING"):
            preferencias.guardar(volumen_musica=101, volumen_efectos=-1)
        valores = preferencias.cargar()
        self.assertEqual(valores["volumen_musica"], 50)
        self.assertEqual(valores["volumen_efectos"], 45)

    def test_archivo_danado_o_con_tipos_incorrectos(self):
        ruta = preferencias.ruta_preferencias()
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text("{esto no es json", encoding="utf-8")
        with self.assertLogs("heyalgb.preferencias", level="WARNING"):
            self.assertEqual(preferencias.cargar(), preferencias.PREDETERMINADAS)
        ruta.write_text(json.dumps({"mostrar_bienvenida": "no", "otra": 1}), encoding="utf-8")
        self.assertTrue(preferencias.cargar()["mostrar_bienvenida"])
        ruta.write_text("[1, 2]", encoding="utf-8")
        with self.assertLogs("heyalgb.preferencias", level="WARNING"):
            self.assertEqual(preferencias.cargar(), preferencias.PREDETERMINADAS)
        # Guardar sobre un archivo dañado lo repara.
        self.assertTrue(preferencias.guardar(musica_habilitada=False))
        self.assertFalse(preferencias.cargar()["musica_habilitada"])

    def test_la_carpeta_no_esta_dentro_del_repositorio(self):
        with mock.patch.dict(os.environ, {"HEYALGB_CONFIG_DIR": ""}):
            carpeta = preferencias.carpeta_configuracion().resolve()
        repositorio = Path(__file__).resolve().parents[1]
        self.assertNotIn(repositorio, [carpeta, *carpeta.parents])


class AyudaContenidoTests(unittest.TestCase):
    def test_todas_las_herramientas_tienen_ayuda_completa(self):
        from core.ui.ayuda import CONTENIDO, texto_ayuda

        claves = {
            "general", "matriz", "vector", "matricial", "intercambio", "flujo_red",
            "particiones", "sistemas", "limites", "numerica", "determinantes",
            "biseccion", "regla_falsa", "abiertos", "errores",
        }
        self.assertEqual(set(CONTENIDO), claves)
        for clave in claves:
            texto = texto_ayuda(clave)
            for seccion in ("PARA QUÉ SIRVE", "FORMATOS ADMITIDOS", "EJEMPLO VÁLIDO",
                            "RESTRICCIONES", "CÓMO LEER LA SALIDA", "ATAJOS DE TECLADO"):
                self.assertIn(seccion, texto, (clave, seccion))

    def test_ejemplos_de_la_ayuda_coinciden_con_el_codigo(self):
        from fractions import Fraction as F

        from core.determinantes import operaciones_determinantes as det
        from core.lineal.solucion import enrutar_resolucion_matricial
        from core.sistemas_numericos import operaciones_numericas as num

        resultado = enrutar_resolucion_matricial(
            [[F(2), F(1), F(-1)], [F(-3), F(-1), F(2)], [F(-2), F(1), F(2)]],
            vector_b=[F(8), F(-11), F(-3)],
        )
        self.assertEqual(resultado["solucion"], [2, 3, -1])
        self.assertEqual(
            det.determinante_lu_valor([[F(2), F(-1), F(0)], [F(1), F(3), F(2)], [F(0), F(1), F(4)]]),
            24,
        )
        self.assertEqual(
            num.convertir_decimal_a_base(num.parsear_decimal("45.75"), 2, "Binario")[0],
            "101101.11",
        )


class _ConTk(_ConfigTemporal):
    def setUp(self):
        super().setUp()
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f"Tk no disponible: {error}")
        self.root.geometry("300x200+-4000+-4000")
        self.root.update()

    def tearDown(self):
        try:
            # CustomTkinter programa tareas internas (barra de título, scrollbars)
            # unos cientos de ms después de crear ventanas; se dejan terminar para
            # que no se ejecuten sobre el intérprete de la siguiente prueba.
            self.root.after(400, self.root.quit)
            self.root.mainloop()
            self.root.destroy()
        finally:
            super().tearDown()


class NavegacionTests(_ConTk):
    def _abrir_limites(self):
        from core.ui.vista_limites import VistaLimites

        self.root.withdraw()
        vista = VistaLimites(self.root)
        vista.geometry("+-4000+-4000")
        self.root.update()
        return vista

    def _escribir(self, vista, entrada, texto):
        entrada._entry.focus_force()
        self.root.update()
        entrada.delete(0, "end")
        for caracter in texto:
            entrada._entry.event_generate("<KeyPress>", keysym=caracter, when="now")
        entrada.insert(0, texto)
        self.root.update()

    def test_volver_sin_cambios_no_pregunta_y_restaura_el_padre(self):
        vista = self._abrir_limites()
        with mock.patch("core.ui.navegacion.messagebox.askyesno") as pregunta:
            vista.volver()
        pregunta.assert_not_called()
        self.assertFalse(vista.winfo_exists())
        self.assertEqual(self.root.state(), "normal")

    def test_volver_con_datos_pide_confirmacion(self):
        vista = self._abrir_limites()
        self._escribir(vista, vista.entry_fx, "x")
        self.assertTrue(vista._guardia_cambios.modificada)
        with mock.patch("core.ui.navegacion.messagebox.askyesno", return_value=False) as pregunta:
            vista.volver()
        pregunta.assert_called_once()
        self.assertTrue(vista.winfo_exists())  # el usuario canceló: no se pierde nada
        with mock.patch("core.ui.navegacion.messagebox.askyesno", return_value=True):
            vista.volver()
        self.assertFalse(vista.winfo_exists())

    def test_tab_y_navegacion_no_cuentan_como_cambio(self):
        vista = self._abrir_limites()
        vista.entry_fx._entry.focus_force()
        self.root.update()
        for tecla in ("Tab", "Left", "Right", "Home"):
            vista.entry_fx._entry.event_generate("<KeyPress>", keysym=tecla, when="now")
        self.assertFalse(vista._guardia_cambios.modificada)
        vista.volver()

    def test_ayuda_es_unica_y_se_cierra_al_volver(self):
        from core.ui.ayuda import mostrar_ayuda

        vista = self._abrir_limites()
        primera = mostrar_ayuda(vista, "limites")
        segunda = mostrar_ayuda(vista, "limites")
        self.assertIs(primera, segunda)
        self.assertIn("EJEMPLO VÁLIDO", primera._texto.get("1.0", "end"))
        vista.volver()
        self.assertFalse(primera.winfo_exists())

    def test_cargar_ejemplo_no_calcula_y_confirma_reemplazo(self):
        vista = self._abrir_limites()
        # Valores iniciales de la vista: se reemplazan sin preguntar.
        with mock.patch("core.ui.navegacion.messagebox.askyesno") as pregunta:
            self.assertTrue(vista.cargar_ejemplo())
        pregunta.assert_not_called()
        self.assertEqual(vista.entry_fx.get(), "sin(x)/x")
        self.assertNotIn("RESULTADO", vista.texto_resultado.get("1.0", "end"))
        # Datos propios distintos: se pregunta y se respeta un «No».
        vista.entry_fx.delete(0, "end")
        vista.entry_fx.insert(0, "x^2")
        with mock.patch("core.ui.navegacion.messagebox.askyesno", return_value=False):
            self.assertFalse(vista.cargar_ejemplo())
        self.assertEqual(vista.entry_fx.get(), "x^2")
        vista._guardia_cambios.modificada = False
        vista.volver()

    def test_campo_vacio_recibe_foco_y_marca(self):
        vista = self._abrir_limites()
        vista.entry_fx.delete(0, "end")
        vista.ejecutar_calculo()
        self.root.update()
        self.assertTrue(getattr(vista.entry_fx, "_heyalgb_en_error", False))
        self.assertIn("⚠", vista.texto_resultado.get("1.0", "end"))
        vista.volver()


class MetodosNumericosPresentationTests(_ConTk):
    def test_selector_carga_ejemplos_del_banco_y_metodo_sugerido(self):
        from core.ui.vista_metodos_numericos import VistaMetodosNumericos

        self.root.withdraw()
        vista = VistaMetodosNumericos(self.root)
        vista.geometry("+-4000+-4000")
        self.root.update()

        selector = vista._selector_ejemplo
        self.assertEqual(selector.get(), "Cargar ejemplo...")
        self.assertEqual(tuple(selector.cget("values")), tuple(vista.EJEMPLOS))
        self.assertEqual(len(vista.EJEMPLOS), 12)

        selector.set("Ej. 2b (raíz mayor)")
        with mock.patch(
            "core.ui.vista_metodos_numericos.confirmar_reemplazo",
            return_value=True,
        ):
            selector._command("Ej. 2b (raíz mayor)")
        panel_biseccion = vista._paneles["Método de Bisección"]
        self.assertEqual(vista._operacion_activa, "Método de Bisección")
        self.assertEqual(panel_biseccion.funcion_var.get(), "exp(x) - 3*x**2")
        self.assertEqual(panel_biseccion.entradas["a"].get(), "3")
        self.assertEqual(panel_biseccion.entradas["b"].get(), "4")
        self.assertEqual(panel_biseccion.entradas["tolerancia"].get(), "1e-6")

        selector.set("Ej. 3")
        selector._command("Ej. 3")
        panel_abiertos = vista._paneles["Métodos Abiertos"]
        self.assertEqual(vista._operacion_activa, "Métodos Abiertos")
        self.assertEqual(panel_abiertos.metodo_var.get(), "newton")
        self.assertEqual(panel_abiertos.funcion_var.get(), "cos(x) - x*exp(x)")
        self.assertEqual(panel_abiertos.entradas["x0"].get(), "0.5")
        self.assertEqual(panel_abiertos.entradas["tolerancia"].get(), "1e-6")

        vista._guardia_cambios.modificada = False
        selector.set("Ej. 1")
        with mock.patch(
            "core.ui.vista_metodos_numericos.confirmar_reemplazo",
            return_value=False,
        ):
            selector._command("Ej. 1")
        self.assertEqual(selector.get(), "Cargar ejemplo...")
        self.assertFalse(vista._guardia_cambios.modificada)

    def test_salida_biseccion_y_copia_academica(self):
        from core.ui.vista_biseccion import VistaBiseccion

        vista = VistaBiseccion(self.root)
        vista.pack(fill="both", expand=True)
        vista.funcion_var.set("x**2 - 2")
        for clave, valor in (("a", "1"), ("b", "2"), ("tolerancia", "1e-6")):
            vista.entradas[clave].delete(0, "end")
            vista.entradas[clave].insert(0, valor)

        vista.resolver()
        salida = vista.texto_salida.get("1.0", "end-1c")
        self.assertIn("Fórmula iterativa: x_r = (a + b) / 2", salida)
        self.assertIn("Ancho del intervalo b - a < tolerancia", salida)
        self.assertRegex(
            salida,
            r"\|f\(raíz\)\| \(residuo\): \d\.\d{10}e[-+]\d+",
        )

        vista.texto_salida.master.barra.copiar()
        reporte = self.root.clipboard_get()
        self.assertIn("Método seleccionado: Bisección", reporte)
        self.assertIn(
            "Justificación de elección e intervalo/valores iniciales: "
            "[Completar por el estudiante]",
            reporte,
        )
        self.assertIn("Tabla de iteraciones:", reporte)
        self.assertIn("Residuo |f(x)|:", reporte)

    def test_salida_regula_falsi_incluye_formula_criterio_y_residuo_preciso(self):
        from core.ui.vista_regla_falsa import VistaReglaFalsa

        vista = VistaReglaFalsa(self.root)
        vista.pack(fill="both", expand=True)
        vista.funcion_var.set("x - 1")
        for clave, valor in (
            ("a", "0"),
            ("b", "2"),
            ("tolerancia", "1e-6"),
            ("max_iteraciones", "100"),
        ):
            vista.entradas[clave].delete(0, "end")
            vista.entradas[clave].insert(0, valor)

        vista.resolver()
        salida = vista.texto_salida.get("1.0", "end-1c")
        self.assertIn("Fórmula iterativa: c = a - f(a)", salida)
        self.assertIn("Criterio de parada: Raíz exacta", salida)
        self.assertIn("|f(aproximación)| (residuo): 0.0000000000e+00", salida)
        self.assertIn("Método seleccionado: Regula Falsi", vista._reporte_academico)

    def test_salida_newton_y_secante_incluye_formula_criterio_y_residuo(self):
        from core.ui.vista_metodos_abiertos import VistaMetodosAbiertos

        vista = VistaMetodosAbiertos(self.root)
        vista.pack(fill="both", expand=True)
        vista.funcion_var.set("x**2 - 2")
        for clave, valor in (
            ("x0", "1.5"),
            ("tolerancia", "1e-6"),
            ("max_iteraciones", "50"),
        ):
            vista.entradas[clave].delete(0, "end")
            vista.entradas[clave].insert(0, valor)
        vista.resolver()
        salida_newton = vista.texto_salida.get("1.0", "end-1c")
        self.assertIn("Fórmula iterativa: x_(n+1) = x_n - f(x_n) / f'(x_n)", salida_newton)
        self.assertIn("Criterio de parada: Residuo", salida_newton)
        self.assertRegex(
            salida_newton,
            r"\|f\(x\)\| \(residuo final\): \d\.\d{10}e[-+]\d+",
        )

        vista.metodo_var.set("secante")
        vista._cambiar_metodo()
        for clave, valor in (
            ("x0", "1"),
            ("x1", "2"),
            ("tolerancia", "1e-6"),
            ("max_iteraciones", "50"),
        ):
            vista.entradas[clave].delete(0, "end")
            vista.entradas[clave].insert(0, valor)
        vista.resolver()
        salida_secante = vista.texto_salida.get("1.0", "end-1c")
        self.assertIn("Fórmula iterativa: x_(n+1) = x_n - f(x_n)", salida_secante)
        self.assertIn("Criterio de parada:", salida_secante)
        self.assertRegex(
            salida_secante,
            r"\|f\(x\)\| \(residuo final\): \d\.\d{10}e[-+]\d+",
        )

    def test_advertencia_de_muestreo_sigue_visible_sin_estado_dinamico(self):
        from core.ui.vista_grafica_biseccion import VistaGraficaBiseccion

        funcion = tk.StringVar(master=self.root, value="x")
        vista = VistaGraficaBiseccion(
            self.root,
            funcion,
            mostrar_estado_actualizacion=False,
        )
        self.root.update()

        self.assertIn("muestreo son aproximados", vista.nota_muestreo.cget("text"))
        self.assertIn("no garantiza detectar todas las raíces", vista.nota_muestreo.cget("text"))
        self.assertEqual(vista.estado.cget("text"), "")
        vista.al_cerrar()


class DashboardRegresoTests(_ConTk):
    def test_dashboard_alinea_controles_y_equilibra_margenes_de_tarjetas(self):
        from core.ui.dashboard import Dashboard

        self.root.geometry("980x780+-4000+-4000")
        self.root.update()
        dashboard = Dashboard(self.root)
        self.root.update()
        ancho = dashboard.contenido.winfo_width()
        alto = dashboard.contenido.winfo_height()
        dashboard._reorganizar_elementos(ancho, alto)

        tarjeta_izquierda = next(
            item for item in dashboard.tarjetas
            if item["row"] == 0 and item["column"] == 0
        )
        ecuaciones = next(
            item for item in dashboard.tarjetas
            if item["row"] == 0 and item["column"] == 2
        )
        determinantes = next(
            item for item in dashboard.tarjetas
            if item["row"] == 2 and item["column"] == 2
        )
        ancho_tarjeta = dashboard.contenido.itemcget(
            tarjeta_izquierda["window"], "width"
        )
        ancho_tarjeta = float(ancho_tarjeta)
        centro_izquierdo = dashboard.contenido.coords(
            tarjeta_izquierda["window"]
        )[0]
        centro_derecho = dashboard.contenido.coords(ecuaciones["window"])[0]
        margen_izquierdo = centro_izquierdo - ancho_tarjeta / 2
        margen_derecho = ancho - centro_derecho - ancho_tarjeta / 2

        self.assertAlmostEqual(margen_izquierdo, margen_derecho, delta=1)
        self.assertAlmostEqual(margen_izquierdo, max(20, ancho * 0.14), delta=1)
        self.assertAlmostEqual(
            centro_derecho,
            dashboard.contenido.coords(determinantes["window"])[0],
            delta=1,
        )
        centro_panel = (
            dashboard.contenido.coords(dashboard.musica_item)[1]
            + dashboard.panel_audio.winfo_reqheight() / 2
        )
        centro_boton = (
            dashboard.contenido.coords(dashboard.volver_item)[1]
            + dashboard.boton_inicio.winfo_reqheight() / 2
        )
        self.assertAlmostEqual(
            dashboard.contenido.coords(dashboard.musica_item)[0],
            max(20, ancho * 0.14) - 45,
            delta=1,
        )
        self.assertAlmostEqual(centro_panel, centro_boton + 15, delta=1)
        dashboard.desregistrar_fuentes()

    def test_dashboard_regresa_a_portada_sin_destruir_la_aplicacion(self):
        from core.ui.dashboard import Dashboard

        volver = mock.Mock()
        dashboard = Dashboard(self.root, al_volver_inicio=volver)
        self.root.update()

        dashboard.volver_al_inicio()

        volver.assert_called_once_with()
        self.assertTrue(self.root.winfo_exists())
        self.assertFalse(dashboard.contenido.winfo_exists())


class CopiarTests(_ConTk):
    def test_copiar_sin_y_con_resultados(self):
        from core.ui.zoom_resultados import crear_consola_resultados, escribir_consola

        contenedor, texto, zoom = crear_consola_resultados(self.root)
        contenedor.pack()
        barra = contenedor.barra
        barra.copiar()
        self.assertEqual(barra.aviso.cget("text"), "Nada que copiar")
        escribir_consola(texto, "[ 1   2 ]\n[ 3   4 ]")
        zoom.establecer(150)
        barra.copiar()
        self.assertEqual(barra.aviso.cget("text"), "✓ Copiado")
        self.assertEqual(self.root.clipboard_get(), "[ 1   2 ]\n[ 3   4 ]")
        self.assertEqual(zoom.nivel, 150)  # copiar no cambia el zoom
        barra.boton_limpiar_resultados.invoke()
        self.assertEqual(texto.get("1.0", "end-1c"), "")
        self.assertEqual(zoom.nivel, 150)  # limpiar no cambia el zoom


class BienvenidaTests(_ConTk):
    def test_bienvenida_integrada_preferencia_y_reapertura(self):
        from core.ui.bienvenida import (
            GuiaBienvenida,
            abrir_bienvenida,
            mostrar_bienvenida_si_corresponde,
        )

        acciones = []
        guia = mostrar_bienvenida_si_corresponde(
            self.root,
            al_comenzar=lambda: acciones.append("comenzar"),
            al_omitir=lambda: acciones.append("omitir"),
        )
        self.assertIsInstance(guia, GuiaBienvenida)
        self.assertIs(guia.master, self.root)
        self.assertIs(abrir_bienvenida(self.root), guia)
        guia.var_no_mostrar.set(True)
        guia.comenzar()
        self.assertFalse(preferencias.cargar()["mostrar_bienvenida"])
        self.assertEqual(acciones, ["comenzar"])
        self.assertIsNone(mostrar_bienvenida_si_corresponde(self.root))

        # La guía puede reabrirse manualmente aunque se haya desactivado al inicio.
        guia = abrir_bienvenida(
            self.root, al_omitir=lambda: acciones.append("reabierta")
        )
        guia.var_no_mostrar.set(False)
        guia.omitir()
        self.assertTrue(preferencias.cargar()["mostrar_bienvenida"])
        self.assertEqual(acciones, ["comenzar", "reabierta"])

    def test_recorrido_completo_usa_calculo_copia_zoom_y_volver_reales(self):
        from core.ui.dashboard import Dashboard

        dashboard = Dashboard(self.root)
        dashboard.iniciar_recorrido()
        self.assertEqual(dashboard._recorrido_estado, "tarjeta")
        tarjeta = next(
            item for item in dashboard.tarjetas
            if item["text"] == "Métodos Numéricos"
        )
        tarjeta["button"].invoke()
        vista = dashboard.ventana_activa
        tarjeta["button"].invoke()
        self.assertIs(dashboard.ventana_activa, vista)
        self.assertEqual(dashboard._recorrido_estado, "ejemplo")
        self.assertIs(vista.master_dashboard, self.root)
        self.assertIsNotNone(vista.panel_recorrido)
        self.root.geometry("1100x700+-4000+-4000")
        self.root.update()
        self.assertGreater(vista.panel_recorrido.descripcion.cget("wraplength"), 0)

        vista._selector_ejemplo.set("Ej. 1")
        vista._selector_ejemplo._command("Ej. 1")
        self.assertEqual(dashboard._recorrido_estado, "campos")
        dashboard.recorrido_siguiente()
        self.assertEqual(dashboard._recorrido_estado, "calcular")

        panel = vista._paneles["Método de Bisección"]
        panel.entradas["b"].delete(0, "end")
        panel.entradas["b"].insert(0, "2")
        panel.resolver()
        self.assertEqual(dashboard._recorrido_estado, "calcular")
        self.assertIn("ERROR:", panel.texto_salida.get("1.0", "end"))

        panel.entradas["b"].delete(0, "end")
        panel.entradas["b"].insert(0, "3")
        panel.resolver()
        self.assertEqual(dashboard._recorrido_estado, "resultado")
        dashboard.recorrido_siguiente()
        self.assertEqual(dashboard._recorrido_estado, "copiar")
        panel.boton_copiar.invoke()
        self.assertEqual(dashboard._recorrido_estado, "zoom")
        panel.controles_zoom.boton_mas.invoke()
        self.assertEqual(dashboard._recorrido_estado, "volver")

        vista._barra_navegacion.boton_volver.invoke()
        self.assertFalse(dashboard._recorrido_activo)
        self.assertIsNone(dashboard.ventana_activa)
        self.assertEqual(self.root.state(), "normal")
        self.assertEqual(
            dashboard._recorrido_panel.titulo.cget("text"),
            "Ya conoces el flujo",
        )
        dashboard.salir_recorrido()
        self.assertIsNone(dashboard._recorrido_panel)
        dashboard.desregistrar_fuentes()

    def test_ayuda_reabre_la_bienvenida_integrada_y_permite_omitir(self):
        from core.ui.bienvenida import GuiaBienvenida
        from core.ui.dashboard import Dashboard

        volver = mock.Mock()
        dashboard = Dashboard(self.root, al_volver_inicio=volver)
        dashboard.abrir_guia()
        guia = dashboard._bienvenida_dashboard
        self.assertIsInstance(guia, GuiaBienvenida)
        self.assertIs(guia.master, self.root)
        self.assertEqual(dashboard.contenido.winfo_manager(), "")
        guia.omitir()
        self.assertIsNone(dashboard._bienvenida_dashboard)
        self.assertEqual(dashboard.contenido.winfo_manager(), "pack")
        self.assertFalse(dashboard._recorrido_activo)

        dashboard.abrir_guia()
        dashboard._bienvenida_dashboard.comenzar()
        self.assertTrue(dashboard._recorrido_activo)
        dashboard.volver_al_inicio()
        volver.assert_not_called()
        dashboard.salir_recorrido()
        self.assertFalse(dashboard._recorrido_activo)
        dashboard.desregistrar_fuentes()

    def test_anterior_y_cierre_x_restauran_el_dashboard(self):
        from core.ui.dashboard import Dashboard

        class Audio:
            musica_habilitada = True
            efectos_habilitados = True

            def __init__(self):
                self.detenciones = 0
                self.inicios = 0

            def registrar_control_sonido(self, *_argumentos):
                pass

            def detener_musica_lobby(self):
                self.detenciones += 1

            def iniciar_musica_lobby(self):
                self.inicios += 1

        audio = Audio()
        dashboard = Dashboard(self.root, audio)
        dashboard.iniciar_recorrido()
        dashboard.abrir_metodos_numericos()
        self.assertEqual(audio.detenciones, 1)
        dashboard.recorrido_anterior()
        self.assertTrue(self.root.winfo_exists())
        self.assertEqual(self.root.state(), "normal")
        self.assertEqual(dashboard._recorrido_estado, "tarjeta")
        self.assertIsNone(dashboard.ventana_activa)
        self.assertEqual(audio.inicios, 1)

        dashboard.abrir_metodos_numericos()
        vista = dashboard.ventana_activa
        self.assertEqual(audio.detenciones, 2)
        vista.volver()
        self.assertFalse(dashboard._recorrido_activo)
        self.assertEqual(self.root.state(), "normal")
        self.assertIsNone(dashboard._recorrido_panel)
        self.assertEqual(audio.inicios, 2)
        dashboard.desregistrar_fuentes()


class InicioAjustesTests(_ConTk):
    def test_controles_bajados_logo_y_credito_del_profesor_reposicionados(self):
        from core.ui.vista_inicio import VistaInicio

        class Audio:
            musica_habilitada = True
            efectos_habilitados = True
            volumen_musica = 0.5
            volumen_efectos = 0.45

            def iniciar_musica_lobby(self):
                pass

            def establecer_musica_habilitada(self, _habilitada):
                pass

            def establecer_efectos_habilitados(self, _habilitados):
                pass

            def establecer_volumen_musica(self, _volumen):
                pass

            def establecer_volumen_efectos(self, _volumen):
                pass

            def reproducir_efecto(self, _nombre):
                pass

        self.root.geometry("980x780+-4000+-4000")
        self.root.update()
        vista = VistaInicio(self.root, Audio(), lambda: None)
        self.root.update()
        ancho = vista.contenido.winfo_width()
        alto = vista.contenido.winfo_height()
        vista._reorganizar_contenido(ancho, alto)

        musica = vista.controles_audio["musica"]
        barra_musica = vista.controles_volumen["musica"]
        self.assertGreater(musica["x"], ancho / 2)
        self.assertAlmostEqual(musica["y"], int(alto * 0.10))
        self.assertEqual(barra_musica["y"], musica["y"] + 27)
        self.assertAlmostEqual(
            vista.contenido.coords(vista.logo_uam_item)[1], alto * 0.815, delta=1
        )
        self.assertAlmostEqual(
            vista.contenido.coords(vista.profesor_item)[0],
            vista.contenido.coords(vista.logo_uam_item)[0],
            delta=1,
        )
        self.assertGreater(
            vista.contenido.coords(vista.profesor_item)[1],
            vista.contenido.coords(vista.logo_uam_item)[1],
        )
        self.assertIn(
            "Argüello Martinez",
            vista.contenido.itemcget(vista.profesor_nombre_item, "text"),
        )
        self.assertAlmostEqual(
            vista.contenido.coords(vista.profesor_nombre_item)[0],
            vista.contenido.coords(vista.facultad_item)[0],
            delta=1,
        )
        self.assertEqual(
            vista.contenido.itemcget(vista.profesor_fondo_item, "fill"),
            "#c8c8c8",
        )
        self.assertEqual(
            vista.contenido.itemcget(vista.profesor_fondo_item, "outline"),
            "#fe0000",
        )
        self.assertGreater(
            vista.contenido.coords(vista.profesor_nombre_item)[0],
            vista.contenido.coords(vista.profesor_item)[0],
        )
        self.assertGreater(
            vista.contenido.coords(vista.profesor_item)[1],
            vista.contenido.coords(vista.facultad_item)[1],
        )
        self.assertGreaterEqual(vista.profesor_photo.width(), 64)
        vista.frame.destroy()


class AudioPreferenciasTests(unittest.TestCase):
    def test_volumen_configurable_se_aplica_a_musica_y_efectos(self):
        from core.ui.audio_manager import AudioManager

        audio = AudioManager.__new__(AudioManager)
        audio.disponible = True
        audio._pygame = mock.Mock()
        sonido = mock.Mock()
        audio._efectos = {"calcular": sonido}

        audio.establecer_volumen_musica(0.3)
        audio.establecer_volumen_efectos(0.4)

        audio._pygame.mixer.music.set_volume.assert_called_once_with(0.3)
        sonido.set_volume.assert_called_once_with(0.4)
        self.assertEqual(audio.volumen_musica, 0.3)
        self.assertEqual(audio.volumen_efectos, 0.4)

    def test_efectos_se_cargan_al_45_por_ciento_de_volumen(self):
        from core.ui.audio_manager import AudioManager

        with tempfile.TemporaryDirectory() as directorio:
            ruta = Path(directorio) / "CalcularAct.mp3"
            ruta.touch()
            sonido = mock.Mock()
            audio = AudioManager.__new__(AudioManager)
            audio.carpeta_audio = Path(directorio)
            audio._pygame = mock.Mock()
            audio._pygame.mixer.Sound.return_value = sonido
            audio._efectos = {}
            audio.volumen_efectos = 0.45

            audio._cargar_efectos()

        sonido.set_volume.assert_called_once_with(0.45)
        self.assertIs(audio._efectos["calcular"], sonido)

    def test_efectos_silenciados_no_se_reproducen(self):
        from core.ui.audio_manager import AudioManager

        audio = AudioManager.__new__(AudioManager)
        audio.disponible = True
        audio.efectos_habilitados = True
        sonido = mock.Mock()
        audio._efectos = {"calcular": sonido}
        audio._ultimo_hover = 0.0
        audio.reproducir_efecto("calcular")
        audio.establecer_efectos_habilitados(False)
        audio.reproducir_efecto("calcular")
        self.assertEqual(sonido.play.call_count, 1)


if __name__ == "__main__":
    unittest.main()
