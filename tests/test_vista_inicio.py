import unittest
from pathlib import Path

from PIL import Image

from core.ui.vista_inicio import VistaInicio


class VistaInicioTests(unittest.TestCase):
    def test_creditos_respetan_el_orden_y_los_nombres_del_equipo(self):
        self.assertEqual(
            VistaInicio.INTEGRANTES,
            (
                ("Liang Woo", "Liang_Amamiya.png"),
                ("Óscar Durán", "Oscar_Sakamoto.png"),
                ("Diego Gómez", "Diego_Kitagawa.png"),
                ("Carlos Aguirre", "Charly_Sakura.png"),
            ),
        )
        self.assertEqual(
            VistaInicio.PROFESOR,
            ("Profesor Iván Argüello Martinez", "Argüello_Sojiro.png"),
        )

    def test_ayuda_reutiliza_iconos_existentes_para_todos_los_modulos(self):
        carpeta_assets = Path(__file__).resolve().parents[1] / "core" / "assets"

        self.assertEqual(len(VistaInicio.MODULOS), 8)
        for _nombre, _descripcion, archivo_icono in VistaInicio.MODULOS:
            with self.subTest(icono=archivo_icono):
                self.assertTrue((carpeta_assets / archivo_icono).is_file())

    def test_fondo_cover_llena_el_tamano_solicitado_y_recorta_al_centro(self):
        imagen = Image.new("RGB", (8, 4))
        for x in range(imagen.width):
            for y in range(imagen.height):
                imagen.putpixel((x, y), (x * 20, y * 20, 0))

        resultado = VistaInicio._escalar_fondo_cover(imagen, 4, 4)

        self.assertEqual(resultado.size, (4, 4))
        self.assertEqual(resultado.getpixel((0, 0)), (40, 0, 0))
        self.assertEqual(resultado.getpixel((3, 3)), (100, 60, 0))


if __name__ == "__main__":
    unittest.main()
