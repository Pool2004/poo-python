"""
==============================================================================
Módulo: 07_proyecto_integrador / repositorios.py
Tema: Patrón Repository y Data Mapper (Abstracciones e Implementación SQLAlchemy).
==============================================================================
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session

try:
    from .modelos import Cliente, Producto, ProductoFisico, ProductoDigital
    from .modelos_orm import ClienteORM, ProductoORM, OrdenORM, ItemOrdenORM
    from .carrito import CarritoCompras
    from .servicios import ResumenOrden
except (ImportError, ValueError):
    from modelos import Cliente, Producto, ProductoFisico, ProductoDigital
    from modelos_orm import ClienteORM, ProductoORM, OrdenORM, ItemOrdenORM
    from carrito import CarritoCompras
    from servicios import ResumenOrden


# ==============================================================================
# CONTRATOS ABSTRACTOS (INTERFACES DE REPOSITORIO - DIP / ISP)
# ==============================================================================
class IRepositorioCliente(ABC):
    """Contrato para la persistencia y consulta de Clientes."""

    @abstractmethod
    def guardar(self, cliente: Cliente) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id_usuario: str) -> Optional[Cliente]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Cliente]:
        pass

    @abstractmethod
    def actualizar_saldo(self, id_usuario: str, nuevo_saldo: float) -> None:
        pass


class IRepositorioProducto(ABC):
    """Contrato para la persistencia y consulta de Productos."""

    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        pass

    @abstractmethod
    def buscar_por_sku(self, sku: str) -> Optional[Producto]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Producto]:
        pass


class IRepositorioOrden(ABC):
    """Contrato para la persistencia y consulta de Órdenes de Compra."""

    @abstractmethod
    def guardar_orden(self, resumen: ResumenOrden, carrito: CarritoCompras) -> OrdenORM:
        pass

    @abstractmethod
    def buscar_por_id(self, id_orden: str) -> Optional[OrdenORM]:
        pass

    @abstractmethod
    def listar_por_cliente(self, cliente_id: str) -> List[OrdenORM]:
        pass


# ==============================================================================
# IMPLEMENTACIÓN CONCRETA MEDIANTE SQLALCHEMY Y MYSQL
# ==============================================================================
class SQLAlchemyClienteRepositorio(IRepositorioCliente):
    """Implementación del repositorio de clientes utilizando SQLAlchemy ORM."""

    def __init__(self, sesion: Session):
        self.sesion = sesion

    def guardar(self, cliente: Cliente) -> None:
        existente = self.sesion.get(ClienteORM, cliente.id_usuario)
        if existente:
            existente.nombre = cliente.nombre
            existente.email = cliente.email
            existente.direccion = cliente.direccion
            existente.saldo_billetera = cliente.saldo_billetera
        else:
            orm_cliente = ClienteORM(
                id_usuario=cliente.id_usuario,
                nombre=cliente.nombre,
                email=cliente.email,
                direccion=cliente.direccion,
                saldo_billetera=cliente.saldo_billetera,
            )
            self.sesion.add(orm_cliente)
        self.sesion.flush()

    def buscar_por_id(self, id_usuario: str) -> Optional[Cliente]:
        orm = self.sesion.get(ClienteORM, id_usuario)
        if not orm:
            return None
        return Cliente(
            id_usuario=orm.id_usuario,
            nombre=orm.nombre,
            email=orm.email,
            direccion=orm.direccion,
            saldo_billetera=orm.saldo_billetera
        )

    def listar_todos(self) -> List[Cliente]:
        entidades = self.sesion.query(ClienteORM).all()
        return [
            Cliente(
                id_usuario=e.id_usuario,
                nombre=e.nombre,
                email=e.email,
                direccion=e.direccion,
                saldo_billetera=e.saldo_billetera
            )
            for e in entidades
        ]

    def actualizar_saldo(self, id_usuario: str, nuevo_saldo: float) -> None:
        orm = self.sesion.get(ClienteORM, id_usuario)
        if orm:
            orm.saldo_billetera = float(nuevo_saldo)
            self.sesion.flush()


class SQLAlchemyProductoRepositorio(IRepositorioProducto):
    """
    Implementación del repositorio de productos con soporte de mapeo polimórfico.
    Convierte entidades ProductoORM a instancias de ProductoFisico o ProductoDigital.
    """

    def __init__(self, sesion: Session):
        self.sesion = sesion

    def guardar(self, producto: Producto) -> None:
        existente = self.sesion.get(ProductoORM, producto.sku)
        tipo = "FISICO" if isinstance(producto, ProductoFisico) else "DIGITAL"
        peso = getattr(producto, "peso_kg", None)
        url = getattr(producto, "url_descarga", None)

        if existente:
            existente.nombre = producto.nombre
            existente.precio_base = producto.precio_base
            existente.tipo = tipo
            existente.peso_kg = peso
            existente.url_descarga = url
        else:
            orm_prod = ProductoORM(
                sku=producto.sku,
                nombre=producto.nombre,
                precio_base=producto.precio_base,
                tipo=tipo,
                peso_kg=peso,
                url_descarga=url
            )
            self.sesion.add(orm_prod)
        self.sesion.flush()

    def buscar_por_sku(self, sku: str) -> Optional[Producto]:
        orm = self.sesion.get(ProductoORM, sku.upper())
        if not orm:
            return None
        return self._mapear_a_dominio(orm)

    def listar_todos(self) -> List[Producto]:
        registros = self.sesion.query(ProductoORM).all()
        return [self._mapear_a_dominio(r) for r in registros]

    @staticmethod
    def _mapear_a_dominio(orm: ProductoORM) -> Producto:
        if orm.tipo == "FISICO":
            return ProductoFisico(
                sku=orm.sku,
                nombre=orm.nombre,
                precio_base=orm.precio_base,
                peso_kg=orm.peso_kg or 0.0
            )
        else:
            return ProductoDigital(
                sku=orm.sku,
                nombre=orm.nombre,
                precio_base=orm.precio_base,
                url_descarga=orm.url_descarga or ""
            )


class SQLAlchemyOrdenRepositorio(IRepositorioOrden):
    """Repositorio para transacciones completas de Órdenes y sus Líneas de Detalle."""

    def __init__(self, sesion: Session):
        self.sesion = sesion

    def guardar_orden(self, resumen: ResumenOrden, carrito: CarritoCompras) -> OrdenORM:
        # 1. Asegurar que el cliente existe en BD
        cliente_orm = self.sesion.get(ClienteORM, resumen.cliente.id_usuario)
        if not cliente_orm:
            cliente_orm = ClienteORM(
                id_usuario=resumen.cliente.id_usuario,
                nombre=resumen.cliente.nombre,
                email=resumen.cliente.email,
                direccion=resumen.cliente.direccion,
                saldo_billetera=resumen.cliente.saldo_billetera
            )
            self.sesion.add(cliente_orm)

        # 2. Crear cabecera de orden
        orden_orm = OrdenORM(
            id_orden=resumen.id_orden,
            cliente_id=resumen.cliente.id_usuario,
            subtotal=resumen.subtotal,
            descuento=resumen.descuento,
            envio=resumen.envio,
            total=resumen.total,
            estado="PAGADA" if resumen.transaccion.exitoso else "FALLIDA",
            referencia_pago=getattr(resumen.transaccion, "id_transaccion", str(resumen.transaccion))
        )
        self.sesion.add(orden_orm)

        # 3. Crear items asociados
        for item in carrito:
            # Asegurar que el producto existe en BD
            prod_orm = self.sesion.get(ProductoORM, item.producto.sku)
            if not prod_orm:
                tipo = "FISICO" if isinstance(item.producto, ProductoFisico) else "DIGITAL"
                prod_orm = ProductoORM(
                    sku=item.producto.sku,
                    nombre=item.producto.nombre,
                    precio_base=item.producto.precio_base,
                    tipo=tipo,
                    peso_kg=getattr(item.producto, "peso_kg", None),
                    url_descarga=getattr(item.producto, "url_descarga", None)
                )
                self.sesion.add(prod_orm)

            item_orm = ItemOrdenORM(
                orden_id=resumen.id_orden,
                producto_sku=item.producto.sku,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio_base,
                subtotal=item.subtotal
            )
            self.sesion.add(item_orm)

        self.sesion.flush()
        return orden_orm

    def buscar_por_id(self, id_orden: str) -> Optional[OrdenORM]:
        return self.sesion.get(OrdenORM, id_orden)

    def listar_por_cliente(self, cliente_id: str) -> List[OrdenORM]:
        return (
            self.sesion.query(OrdenORM)
            .filter(OrdenORM.cliente_id == cliente_id)
            .all()
        )
