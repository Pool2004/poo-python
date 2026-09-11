"""
==============================================================================
Módulo de Pruebas: test_fundamentos.py
Verifica las funcionalidades del bloque 01_fundamentos.
==============================================================================
"""

import os
import sys
import unittest
import importlib.util

# Configurar UTF-8
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


mod_01 = cargar_modulo("mod_01", "01_fundamentos/01_clases_y_objetos.py")
mod_02 = cargar_modulo("mod_02", "01_fundamentos/02_atributos_clase_instancia.py")
mod_03 = cargar_modulo("mod_03", "01_fundamentos/03_metodos_instancia_clase_estaticos.py")
mod_04 = cargar_modulo("mod_04", "01_fundamentos/04_ciclo_de_vida.py")


class TestFundamentos(unittest.TestCase):

    def test_01_celular_instanciacion_y_bateria(self):
        celular = mod_01.Celular("Xiaomi", "Redmi 12", bateria=50)
        self.assertEqual(celular.marca, "Xiaomi")
        self.assertEqual(celular.bateria, 50)
        self.assertFalse(celular.encendido)

        # Probar encendido
        res_encendido = celular.encender()
        self.assertTrue(celular.encendido)
        self.assertIn("Se ha encendido", res_encendido)

        # Probar uso de app
        celular.usar_app("App", 20)
        self.assertEqual(celular.bateria, 30)

        # Cargar
        celular.cargar(50)
        self.assertEqual(celular.bateria, 80)

    def test_02_atributos_clase_vs_instancia(self):
        # Resetear contador para la prueba
        mod_02.Empleado.total_empleados = 0
        emp1 = mod_02.Empleado("Lucía", 1000)
        emp2 = mod_02.Empleado("Mario", 2000)

        self.assertEqual(mod_02.Empleado.total_empleados, 2)
        self.assertEqual(emp1.id_empleado, 1)
        self.assertEqual(emp2.id_empleado, 2)

        # Aislamiento de mutabilidad en UsuarioCorrecto
        u1 = mod_02.UsuarioCorrecto("Ana")
        u2 = mod_02.UsuarioCorrecto("Beto")
        u1.amigos.append("Carlos")
        self.assertIn("Carlos", u1.amigos)
        self.assertNotIn("Carlos", u2.amigos)

    def test_03_metodos_instancia_clase_estaticos(self):
        # Constructor tradicional
        fecha = mod_03.Fecha(10, 5, 2024)
        self.assertEqual(fecha.dia, 10)
        self.assertEqual(fecha.mes, 5)

        # Constructor alternativo @classmethod
        fecha_cls = mod_03.Fecha.desde_cadena("01-01-2025")
        self.assertEqual(fecha_cls.dia, 1)
        self.assertEqual(fecha_cls.mes, 1)
        self.assertEqual(fecha_cls.anio, 2025)

        # Método estático @staticmethod
        self.assertTrue(mod_03.Fecha.es_bisiesto(2024))
        self.assertFalse(mod_03.Fecha.es_bisiesto(2023))

    def test_04_gestor_contexto_conexion(self):
        conexion = mod_04.ConexionSegura("PruebaDB")
        self.assertFalse(conexion.conectado)

        with conexion:
            self.assertTrue(conexion.conectado)

        self.assertFalse(conexion.conectado)


if __name__ == "__main__":
    unittest.main()
