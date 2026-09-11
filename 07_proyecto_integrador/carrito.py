"""
==============================================================================
Módulo: 07_proyecto_integrador / carrito.py
Tema: Contenedor Carrito de Compras con Dunder Methods (__add__, __len__, __iter__, __getitem__).
==============================================================================
"""

import sys
from dataclasses import dataclass
try:
    from .modelos import Producto
except (ImportError, ValueError):
    from modelos import Producto

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclass
class ItemCarrito:
    producto: Producto
    cantidad: int = 1

    @property
    def subtotal(self) -> float:
        return self.producto.precio_base * self.cantidad

    @property
    def costo_envio(self) -> float:
        return self.producto.calcular_costo_envio() * self.cantidad


class CarritoCompras:
    """Contenedor avanzado que emula el modelo de datos de Python."""

    def __init__(self):
        self._items: dict[str, ItemCarrito] = {}

    def agregar(self, producto: Producto, cantidad: int = 1) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        if producto.sku in self._items:
            self._items[producto.sku].cantidad += cantidad
        else:
            self._items[producto.sku] = ItemCarrito(producto, cantidad)

    def eliminar(self, sku: str) -> None:
        sku = sku.upper()
        if sku in self._items:
            del self._items[sku]

    # --- DUNDER METHODS (PYTHON DATA MODEL) ---
    def __len__(self) -> int:
        """len(carrito) -> Total de unidades de productos."""
        return sum(item.cantidad for item in self._items.values())

    def __iter__(self):
        """Permite: for item in carrito:"""
        return iter(self._items.values())

    def __getitem__(self, index_or_sku):
        """carrito['SKU-1'] o carrito[0]"""
        if isinstance(index_or_sku, str):
            return self._items[index_or_sku.upper()]
        elif isinstance(index_or_sku, int):
            return list(self._items.values())[index_or_sku]
        raise TypeError("El índice debe ser str (SKU) o int (posición).")

    def __contains__(self, item) -> bool:
        """'SKU' in carrito o producto in carrito"""
        if isinstance(item, str):
            return item.upper() in self._items
        elif isinstance(item, Producto):
            return item.sku in self._items
        return False

    def __add__(self, other: object) -> "CarritoCompras":
        """Sobrecarga de operador +:
        - carrito + producto: agrega el producto.
        - carrito1 + carrito2: fusiona ambos carritos.
        """
        nuevo_carrito = CarritoCompras()
        for item in self._items.values():
            nuevo_carrito.agregar(item.producto, item.cantidad)

        if isinstance(other, Producto):
            nuevo_carrito.agregar(other, 1)
            return nuevo_carrito
        elif isinstance(other, CarritoCompras):
            for item in other:
                nuevo_carrito.agregar(item.producto, item.cantidad)
            return nuevo_carrito
        return NotImplemented

    def calcular_subtotal(self) -> float:
        return sum(item.subtotal for item in self._items.values())

    def calcular_envio(self) -> float:
        return sum(item.costo_envio for item in self._items.values())

    def calcular_total_bruto(self) -> float:
        return self.calcular_subtotal() + self.calcular_envio()

    def __repr__(self) -> str:
        return f"CarritoCompras(items={len(self._items)}, unidades={len(self)}, total=${self.calcular_total_bruto():,.2f})"
