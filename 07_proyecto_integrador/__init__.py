"""
Paquete: 07_proyecto_integrador
Sistema Integrado de Comercio Electrónico y Procesamiento de Pagos en POO.
"""

import os
import sys

# Asegurar resolución en analizadores estáticos y entornos de ejecución
_DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
if _DIR_ACTUAL not in sys.path:
    sys.path.insert(0, _DIR_ACTUAL)

try:
    from modelos import Cliente, ProductoFisico, ProductoDigital
    from carrito import CarritoCompras
    from pasarelas import PasarelaPago, StripePasarela, PayPalPasarela
    from servicios import ServicioCheckout, DescuentoPorcentaje, PublicadorEventos
    from database import Base, engine, SessionLocal, obtener_sesion, inicializar_base_datos
    from modelos_orm import ClienteORM, ProductoORM, OrdenORM, ItemOrdenORM
    from repositorios import (
        IRepositorioCliente,
        IRepositorioProducto,
        IRepositorioOrden,
        SQLAlchemyClienteRepositorio,
        SQLAlchemyProductoRepositorio,
        SQLAlchemyOrdenRepositorio,
    )
except (ImportError, ValueError):
    from .modelos import Cliente, ProductoFisico, ProductoDigital  # type: ignore
    from .carrito import CarritoCompras  # type: ignore
    from .pasarelas import PasarelaPago, StripePasarela, PayPalPasarela  # type: ignore
    from .servicios import ServicioCheckout, DescuentoPorcentaje, PublicadorEventos  # type: ignore
    from .database import Base, engine, SessionLocal, obtener_sesion, inicializar_base_datos  # type: ignore
    from .modelos_orm import ClienteORM, ProductoORM, OrdenORM, ItemOrdenORM  # type: ignore
    from .repositorios import (  # type: ignore
        IRepositorioCliente,
        IRepositorioProducto,
        IRepositorioOrden,
        SQLAlchemyClienteRepositorio,
        SQLAlchemyProductoRepositorio,
        SQLAlchemyOrdenRepositorio,
    )


__all__ = [
    "Cliente",
    "ProductoFisico",
    "ProductoDigital",
    "CarritoCompras",
    "PasarelaPago",
    "StripePasarela",
    "PayPalPasarela",
    "ServicioCheckout",
    "DescuentoPorcentaje",
    "PublicadorEventos",
    "Base",
    "engine",
    "SessionLocal",
    "obtener_sesion",
    "inicializar_base_datos",
    "ClienteORM",
    "ProductoORM",
    "OrdenORM",
    "ItemOrdenORM",
    "IRepositorioCliente",
    "IRepositorioProducto",
    "IRepositorioOrden",
    "SQLAlchemyClienteRepositorio",
    "SQLAlchemyProductoRepositorio",
    "SQLAlchemyOrdenRepositorio",
]

