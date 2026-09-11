"""
==============================================================================
Módulo de Pruebas: test_dunder.py
Verifica las funcionalidades del bloque 03_dunder_methods.
==============================================================================
"""

import os
import sys
import unittest
import importlib.util

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def cargar_modulo(nombre: str, ruta_relativa: str):
    ruta_completa = os.path.join(ROOT_DIR, ruta_relativa)
    spec = importlib.util.spec_from_file_location(nombre, ruta_completa)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


mod_repr = cargar_modulo("mod_repr", "03_dunder_methods/01_representacion.py")
mod_comp = cargar_modulo("mod_comp", "03_dunder_methods/02_comparacion.py")
mod_arit = cargar_modulo("mod_arit", "03_dunder_methods/03_operadores_aritmeticos.py")
mod_cont = cargar_modulo("mod_cont", "03_dunder_methods/04_contenedores_e_iteracion.py")
mod_call = cargar_modulo("mod_call", "03_dunder_methods/05_context_managers_y_call.py")


class TestDunderMethods(unittest.TestCase):

    def test_01_representacion_str_repr_format(self):
        d = mod_repr.Dinero(100.50, "USD")
        self.assertEqual(repr(d), "Dinero(monto=100.5, divisa='USD')")
        self.assertEqual(str(d), "$100.50 USD")
        # Redondeo bancario de Python para 100.5 -> '100USD'
        self.assertEqual(f"{d:corto}", "100USD")

    def test_02_comparaciones_y_hashabilidad(self):
        p1 = mod_comp.Producto("SKU-1", "Laptop", 1000)
        p2 = mod_comp.Producto("SKU-1", "Laptop Copia", 1000)
        p3 = mod_comp.Producto("SKU-2", "Mouse", 50)

        # Igualdad y hash
        self.assertEqual(p1, p2)
        self.assertEqual(hash(p1), hash(p2))

        # total_ordering
        self.assertTrue(p3 < p1)
        self.assertTrue(p1 > p3)
        self.assertTrue(p3 <= p1)
        self.assertTrue(p1 >= p3)

    def test_03_operadores_vectoriales(self):
        v1 = mod_arit.Vector2D(3, 4)
        v2 = mod_arit.Vector2D(1, 2)

        # Magnitud
        self.assertEqual(abs(v1), 5.0)

        # Suma
        v_sum = v1 + v2
        self.assertEqual(v_sum.x, 4.0)
        self.assertEqual(v_sum.y, 6.0)

        # Escalamiento y reflejado
        v_mul = v1 * 2
        v_rmul = 2 * v1
        self.assertEqual(v_mul.x, 6.0)
        self.assertEqual(v_rmul.x, 6.0)

        # Producto punto
        self.assertEqual(v1 * v2, 11.0)

    def test_04_contenedores_y_slicing(self):
        playlist = mod_cont.Playlist("Rock Classics")
        c1 = mod_cont.Cancion("Canción A", "Banda 1", 200)
        c2 = mod_cont.Cancion("Canción B", "Banda 2", 300)

        playlist.agregar(c1)
        playlist.agregar(c2)

        # __len__
        self.assertEqual(len(playlist), 2)

        # __getitem__
        self.assertEqual(playlist[0], c1)
        self.assertEqual(playlist[1], c2)

        # __contains__
        self.assertTrue("Canción A" in playlist)
        self.assertTrue(c2 in playlist)
        self.assertFalse("Inexistente" in playlist)

        # __iter__
        titulos = [c.titulo for c in playlist]
        self.assertEqual(titulos, ["Canción A", "Canción B"])

    def test_05_call_y_context_manager(self):
        filtro = mod_call.FiltroMultiplicador(factor=4.0)
        self.assertEqual(filtro(10), 40.0)
        self.assertEqual(filtro.total_invocaciones, 1)

        # Supresión de excepciones con __exit__
        with mod_call.Temporizador("Test", suprimir_errores=True):
            _ = 1 / 0  # No debe explotar el test gracias al gestor


if __name__ == "__main__":
    unittest.main()
