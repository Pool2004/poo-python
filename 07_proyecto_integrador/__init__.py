"""
Paquete: 07_proyecto_integrador
Sistema Integrado de Comercio Electrónico y Procesamiento de Pagos en POO.
"""

from .modelos import Cliente, ProductoFisico, ProductoDigital
from .carrito import CarritoCompras
from .pasarelas import PasarelaPago, StripePasarela, PayPalPasarela
from .servicios import ServicioCheckout, DescuentoPorcentaje, PublicadorEventos
from .database import Base, engine, SessionLocal, obtener_sesion, inicializar_base_datos
from .modelos_orm import ClienteORM, ProductoORM, OrdenORM, ItemOrdenORM
from .repositorios import (
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

