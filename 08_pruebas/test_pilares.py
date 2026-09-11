"""
==============================================================================
Módulo de Pruebas: test_pilares.py
Verifica las funcionalidades del bloque 02_pilares.
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


mod_encapsulamiento = cargar_modulo("mod_encap", "02_pilares/01_encapsulamiento.py")
mod_abstraccion = cargar_modulo("mod_abs", "02_pilares/02_abstraccion.py")
mod_herencia = cargar_modulo("mod_her", "02_pilares/03_herencia.py")
mod_polimorfismo = cargar_modulo("mod_poli", "02_pilares/04_polimorfismo.py")


class TestPilares(unittest.TestCase):

    def test_01_encapsulamiento_property_y_validaciones(self):
        cuenta = mod_encapsulamiento.CuentaBancaria("Juan Perez", 500.0, pin="1234")
        self.assertEqual(cuenta.saldo, 500.0)

        # Probar asignación válida
        cuenta.saldo = 800.0
        self.assertEqual(cuenta.saldo, 800.0)

        # Probar validación de valor negativo
        with self.assertRaises(ValueError):
            cuenta.saldo = -100.0

        # Probar propiedad de sólo lectura
        with self.assertRaises(AttributeError):
            cuenta.numero_cuenta = "NUEVA-CTA"

        # Probar Name Mangling
        self.assertTrue(hasattr(cuenta, "_CuentaBancaria__pin"))
        self.assertFalse(hasattr(cuenta, "__pin"))

    def test_02_abstraccion_abc_y_contratos(self):
        # La clase abstracta pura no puede instanciarse
        with self.assertRaises(TypeError):
            mod_abstraccion.PasarelaPago("clave")

        # La clase incompleta tampoco
        with self.assertRaises(TypeError):
            mod_abstraccion.PasarelaIncompleta("clave")

        # Las clases concretas sí
        stripe = mod_abstraccion.PasarelaStripe("clave_stripe")
        self.assertEqual(stripe.nombre_proveedor, "Stripe Payments")
        res = stripe.procesar_cobro(100.0, "ref_1")
        self.assertTrue(res["exito"])

    def test_03_herencia_mro_y_mixins(self):
        tesla = mod_herencia.AutoElectrico("Tesla", "Model Y", 2024, 82.0)
        self.assertIn("Eléctrico: 82.0 kWh", tesla.descripcion())

        # Smartphone con MRO y Mixin
        telefono = mod_herencia.SmartphoneD("Apple", "iPhone 16", camara_mpx=48)
        self.assertTrue(hasattr(telefono, "to_json"))
        self.assertIn('"marca": "Apple"', telefono.to_json())

        # Verificar orden MRO
        mro_names = [c.__name__ for c in mod_herencia.SmartphoneD.mro()]
        self.assertLess(mro_names.index("TelefonoB"), mro_names.index("CamaraC"))
        self.assertLess(mro_names.index("CamaraC"), mro_names.index("DispositivoA"))

    def test_04_polimorfismo_y_duck_typing(self):
        discord = mod_polimorfismo.NotificadorDiscordWebhook()
        # No hereda de la clase base
        self.assertFalse(isinstance(discord, mod_polimorfismo.Notificador))
        # Pero tiene el método 'enviar' (Duck typing)
        self.assertTrue(callable(getattr(discord, "enviar", None)))


if __name__ == "__main__":
    unittest.main()
