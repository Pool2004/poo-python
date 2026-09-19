"""
==============================================================================
Módulo de Pruebas: test_orm.py
Verifica la funcionalidad completa de la integración ORM con SQLAlchemy 2.0.
Cubre repositorios, mapeo relacional, polimorfismo y transaccionalidad.
==============================================================================
"""

import os
import sys
import unittest
from datetime import datetime

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROY_DIR = os.path.join(ROOT_DIR, "07_proyecto_integrador")
sys.path.insert(0, PROY_DIR)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, engine as default_mysql_engine
from modelos import Cliente, ProductoFisico, ProductoDigital
from modelos_orm import ClienteORM, ProductoORM, OrdenORM, ItemOrdenORM
from carrito import CarritoCompras
from pasarelas import ResultadoTransaccion
from servicios import ResumenOrden
from repositorios import (
    SQLAlchemyClienteRepositorio,
    SQLAlchemyProductoRepositorio,
    SQLAlchemyOrdenRepositorio
)


class TestORMIntegration(unittest.TestCase):
    """Pruebas unitarias y de integración para la capa ORM y Repositorios."""

    @classmethod
    def setUpClass(cls):
        # Utilizamos una base de datos SQLite en memoria para tests aislados, rápidos y reproducibles
        cls.test_engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(bind=cls.test_engine)
        cls.TestSession = sessionmaker(bind=cls.test_engine, autoflush=False, autocommit=False)

    def setUp(self):
        self.sesion = self.TestSession()

    def tearDown(self):
        self.sesion.rollback()
        self.sesion.close()

    def test_01_cliente_repositorio_crud(self):
        """Verifica las operaciones CRUD del repositorio de clientes."""
        repo = SQLAlchemyClienteRepositorio(self.sesion)
        cliente = Cliente(
            id_usuario="CLI-TEST-1",
            nombre="Carlos Mendoza",
            email="carlos.mendoza@test.com",
            direccion="Carrera 15 # 85-30",
            saldo_billetera=350.0
        )

        # 1. Guardar
        repo.guardar(cliente)
        self.sesion.commit()

        # 2. Buscar por ID
        encontrado = repo.buscar_por_id("CLI-TEST-1")
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, "Carlos Mendoza")
        self.assertEqual(encontrado.email, "carlos.mendoza@test.com")
        self.assertEqual(encontrado.saldo_billetera, 350.0)

        # 3. Actualizar saldo
        repo.actualizar_saldo("CLI-TEST-1", 500.0)
        self.sesion.commit()
        actualizado = repo.buscar_por_id("CLI-TEST-1")
        self.assertEqual(actualizado.saldo_billetera, 500.0)

        # 4. Listar todos
        todos = repo.listar_todos()
        self.assertGreaterEqual(len(todos), 1)
        self.assertTrue(any(c.id_usuario == "CLI-TEST-1" for c in todos))

    def test_02_producto_repositorio_polimorfico(self):
        """Verifica que el repositorio maneje correctamente productos físicos y digitales."""
        repo = SQLAlchemyProductoRepositorio(self.sesion)

        teclado = ProductoFisico("SKU-KEYB", "Teclado Gamer", 80.0, peso_kg=1.5)
        ebook = ProductoDigital("SKU-BOOK", "Clean Code Python", 25.0, "https://dl.io/ebook.pdf")

        repo.guardar(teclado)
        repo.guardar(ebook)
        self.sesion.commit()

        # Recuperar producto físico
        p1 = repo.buscar_por_sku("SKU-KEYB")
        self.assertIsInstance(p1, ProductoFisico)
        self.assertEqual(p1.peso_kg, 1.5)
        self.assertEqual(p1.calcular_costo_envio(), 5.0 + (1.5 * 2.0))

        # Recuperar producto digital
        p2 = repo.buscar_por_sku("SKU-BOOK")
        self.assertIsInstance(p2, ProductoDigital)
        self.assertEqual(p2.url_descarga, "https://dl.io/ebook.pdf")
        self.assertEqual(p2.calcular_costo_envio(), 0.0)

    def test_03_orden_repositorio_relaciones_y_cascada(self):
        """Verifica la persistencia de la orden con sus relaciones a cliente y detalle de items."""
        cliente = Cliente(
            id_usuario="CLI-TEST-2",
            nombre="Laura Torres",
            email="laura@test.com",
            direccion="Calle 100 # 20-10",
            saldo_billetera=1000.0
        )
        prod1 = ProductoFisico("SKU-MOUSE", "Mouse Óptico", 40.0, peso_kg=0.3)
        prod2 = ProductoDigital("SKU-SOFT", "Licencia IDE", 60.0, "https://dl.io/license")

        carrito = CarritoCompras()
        carrito.agregar(prod1, cantidad=2)
        carrito.agregar(prod2, cantidad=1)

        transaccion = ResultadoTransaccion(
            exitoso=True,
            id_transaccion="tx_test_9988",
            mensaje="Aprobado",
            monto=145.6
        )

        resumen = ResumenOrden(
            id_orden="ORD-TEST-888",
            cliente=cliente,
            subtotal=140.0,
            descuento=0.0,
            envio=5.6,
            total=145.6,
            transaccion=transaccion
        )

        repo_orden = SQLAlchemyOrdenRepositorio(self.sesion)
        repo_orden.guardar_orden(resumen, carrito)
        self.sesion.commit()

        # Consultar la orden persistida y verificar relaciones
        orden_db = repo_orden.buscar_por_id("ORD-TEST-888")
        self.assertIsNotNone(orden_db)
        self.assertEqual(orden_db.cliente_id, "CLI-TEST-2")
        self.assertEqual(orden_db.cliente.nombre, "Laura Torres")
        self.assertEqual(orden_db.estado, "PAGADA")
        self.assertEqual(len(orden_db.items), 2)

        # Verificar items asociados
        skus = [itm.producto_sku for itm in orden_db.items]
        self.assertIn("SKU-MOUSE", skus)
        self.assertIn("SKU-SOFT", skus)

    def test_04_transaccion_rollback_en_error(self):
        """Verifica que si ocurre un error, los cambios no se aplican en la base de datos."""
        repo = SQLAlchemyClienteRepositorio(self.sesion)
        cli_rollback = Cliente(
            id_usuario="CLI-FAIL",
            nombre="Usuario Temporal",
            email="temp@test.com",
            direccion="Calle Falsa 123",
            saldo_billetera=100.0
        )

        try:
            repo.guardar(cli_rollback)
            # Provocamos un fallo intencional antes del commit
            raise RuntimeError("Fallo forzado para probar rollback")
        except RuntimeError:
            self.sesion.rollback()

        # Verificar que el usuario no quedó persistido
        consultado = repo.buscar_por_id("CLI-FAIL")
        self.assertIsNone(consultado)


if __name__ == "__main__":
    unittest.main()
