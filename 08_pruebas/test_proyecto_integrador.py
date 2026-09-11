"""
==============================================================================
Módulo de Pruebas: test_proyecto_integrador.py
Verifica la funcionalidad completa del proyecto integrador (07_proyecto_integrador).
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
PROY_DIR = os.path.join(ROOT_DIR, "07_proyecto_integrador")
sys.path.insert(0, PROY_DIR)

from modelos import Cliente, ProductoFisico, ProductoDigital
from carrito import CarritoCompras
from pasarelas import StripePasarela, PayPalPasarela
from servicios import ServicioCheckout, PublicadorEventos, DescuentoPorcentaje, SinDescuento


class TestProyectoIntegrador(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente(
            id_usuario="USR-TEST",
            nombre="Tester Profesional",
            email="test@dominio.com",
            direccion="Av Siempre Viva 742",
            saldo_billetera=500.0
        )
        self.fisico = ProductoFisico("SKU-F", "Teclado", 100.0, peso_kg=2.0)
        self.digital = ProductoDigital("SKU-D", "E-Book", 30.0, "https://dl.link/ebook")

    def test_01_validacion_cliente_y_productos(self):
        self.assertEqual(self.cliente.nombre, "Tester Profesional")
        with self.assertRaises(ValueError):
            self.cliente.email = "email_invalido_sin_arroba"

        # Envío físico: 5 + (2 * 2) = 9
        self.assertEqual(self.fisico.calcular_costo_envio(), 9.0)
        # Envío digital es 0
        self.assertEqual(self.digital.calcular_costo_envio(), 0.0)

    def test_02_carrito_operaciones_y_dunder(self):
        carrito = CarritoCompras()
        carrito.agregar(self.fisico, cantidad=2)
        self.assertEqual(len(carrito), 2)
        self.assertEqual(carrito.calcular_subtotal(), 200.0)
        self.assertEqual(carrito.calcular_envio(), 18.0)

        # Operador +
        nuevo_carrito = carrito + self.digital
        self.assertEqual(len(nuevo_carrito), 3)
        self.assertTrue("SKU-D" in nuevo_carrito)
        self.assertTrue(self.digital in nuevo_carrito)

    def test_03_checkout_exitoso_con_descuento(self):
        carrito = CarritoCompras()
        carrito.agregar(self.fisico, 1)  # Subtotal 100, Envio 9 = 109

        bus_eventos = PublicadorEventos()
        notificaciones = []

        class MockListener:
            def on_orden_completada(self, orden_id, cliente, monto):
                notificaciones.append((orden_id, monto))

        bus_eventos.suscribir(MockListener())

        pasarela = StripePasarela("sk_test_123")
        checkout = ServicioCheckout(pasarela, bus_eventos)

        # 10% de descuento sobre 100 = 10
        # Total: (100 - 10) + 9 = 99
        descuento = DescuentoPorcentaje(10.0)
        resumen = checkout.procesar_compra(self.cliente, carrito, descuento)

        self.assertEqual(resumen.subtotal, 100.0)
        self.assertEqual(resumen.descuento, 10.0)
        self.assertEqual(resumen.envio, 9.0)
        self.assertEqual(resumen.total, 99.0)
        self.assertTrue(resumen.transaccion.exitoso)
        self.assertEqual(len(notificaciones), 1)

    def test_04_checkout_carrito_vacio_falla(self):
        carrito_vacio = CarritoCompras()
        checkout = ServicioCheckout(PayPalPasarela("client_id"), PublicadorEventos())

        with self.assertRaises(ValueError):
            checkout.procesar_compra(self.cliente, carrito_vacio)


if __name__ == "__main__":
    unittest.main()
