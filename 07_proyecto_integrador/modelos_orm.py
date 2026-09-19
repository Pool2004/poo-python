"""
==============================================================================
Módulo: 07_proyecto_integrador / modelos_orm.py
Tema: Modelos Relacionales Mapeados (ORM) con SQLAlchemy 2.0 Declarative.
==============================================================================
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from .database import Base
except (ImportError, ValueError):
    from database import Base


class ClienteORM(Base):
    """Mapeo relacional de la tabla 'clientes'."""
    __tablename__ = "clientes"

    id_usuario: Mapped[str] = mapped_column(String(50), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    direccion: Mapped[str] = mapped_column(String(255), nullable=False)
    saldo_billetera: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación 1-a-Muchos: Un cliente tiene múltiples órdenes
    ordenes: Mapped[List["OrdenORM"]] = relationship(
        "OrdenORM",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<ClienteORM(id='{self.id_usuario}', nombre='{self.nombre}', "
            f"email='{self.email}', saldo={self.saldo_billetera})>"
        )


class ProductoORM(Base):
    """Mapeo relacional de la tabla 'productos' (soporta físicos y digitales)."""
    __tablename__ = "productos"

    sku: Mapped[str] = mapped_column(String(50), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    precio_base: Mapped[float] = mapped_column(Float, nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)  # 'FISICO' | 'DIGITAL'
    peso_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    url_descarga: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<ProductoORM(sku='{self.sku}', nombre='{self.nombre}', "
            f"tipo='{self.tipo}', precio={self.precio_base})>"
        )


class OrdenORM(Base):
    """Mapeo relacional de la cabecera de la orden de compra."""
    __tablename__ = "ordenes"

    id_orden: Mapped[str] = mapped_column(String(50), primary_key=True)
    cliente_id: Mapped[str] = mapped_column(ForeignKey("clientes.id_usuario"), nullable=False, index=True)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)
    descuento: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    envio: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    estado: Mapped[str] = mapped_column(String(30), default="PAGADA", nullable=False)
    referencia_pago: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones ORM
    cliente: Mapped["ClienteORM"] = relationship("ClienteORM", back_populates="ordenes")
    items: Mapped[List["ItemOrdenORM"]] = relationship(
        "ItemOrdenORM",
        back_populates="orden",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<OrdenORM(id='{self.id_orden}', cliente_id='{self.cliente_id}', "
            f"total={self.total}, estado='{self.estado}')>"
        )


class ItemOrdenORM(Base):
    """Mapeo relacional de las líneas de detalle de una orden."""
    __tablename__ = "items_orden"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[str] = mapped_column(ForeignKey("ordenes.id_orden"), nullable=False, index=True)
    producto_sku: Mapped[str] = mapped_column(ForeignKey("productos.sku"), nullable=False, index=True)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)

    # Relaciones
    orden: Mapped["OrdenORM"] = relationship("OrdenORM", back_populates="items")
    producto: Mapped["ProductoORM"] = relationship("ProductoORM")

    def __repr__(self) -> str:
        return (
            f"<ItemOrdenORM(id={self.id}, orden_id='{self.orden_id}', "
            f"sku='{self.producto_sku}', cant={self.cantidad}, subtotal={self.subtotal})>"
        )
