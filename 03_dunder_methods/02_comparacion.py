"""
==============================================================================
Módulo: 03_dunder_methods / 02_comparacion.py
Tema: Comparaciones Ricas, functools.total_ordering y el Contrato __hash__.
==============================================================================

Métodos de Comparación (Rich Comparison Methods):
-------------------------------------------------
Operador   Método Dunder
---------  --------------------
==         __eq__(self, other)
!=         __ne__(self, other)
<          __lt__(self, other)
<=         __le__(self, other)
>          __gt__(self, other)
>=         __ge__(self, other)

El Decorador `@functools.total_ordering`:
-----------------------------------------
Escribir manualmente los 6 métodos de comparación es repetitivo y propenso a errores.
Python ofrece `@total_ordering`: sólo necesitas implementar:
1. `__eq__`
2. Y uno de los de orden (por ejemplo `__lt__`).
¡El decorador deduce e implementa automáticamente los 4 restantes (`__gt__`, `__le__`, `__ge__`, `__ne__`)!

El Contrato de Hashabilidad (`__hash__`):
-----------------------------------------
- Por defecto, los objetos comparan identidad de memoria (`id`) y son hashables.
- Si defines `__eq__`, Python asume que el objeto es mutable y desactiva `__hash__ = None`.
- Para poder usar tus objetos dentro de un `set` o como llaves de un `dict`, debes
  garantizar que los atributos comparados sean INMUTABLES e implementar `__hash__`.
"""

import sys
from functools import total_ordering


@total_ordering
class Producto:
    """Modela un producto con ordenamiento automático por precio y hashabilidad."""

    def __init__(self, sku: str, nombre: str, precio: float):
        self._sku = sku.upper()
        self.nombre = nombre
        self.precio = float(precio)

    @property
    def sku(self) -> str:
        """SKU inmutable para identificación única."""
        return self._sku

    # 1. Igualdad basada en identidad de negocio (SKU)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Producto):
            return NotImplemented
        return self._sku == other._sku

    # 2. Ordenamiento menor qué (<) basado en el precio
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Producto):
            return NotImplemented
        return self.precio < other.precio

    # 3. Contrato Hash: Permite que el Producto viva en sets y dicts
    def __hash__(self) -> int:
        # El hash debe basarse en el mismo atributo inmutable que determina la igualdad
        return hash(self._sku)

    def __repr__(self) -> str:
        return f"Producto({self._sku!r}, {self.nombre!r}, ${self.precio:.2f})"


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 02 - Comparaciones, total_ordering y __hash__")
    print("=" * 65)

    p1 = Producto("LAP-001", "Laptop Gamer", 1500.0)
    p2 = Producto("MOU-002", "Mouse Óptico", 35.0)
    p3 = Producto("KEY-003", "Teclado Mecánico", 120.0)
    p4 = Producto("LAP-001", "Laptop Gamer Clon", 1500.0)  # Mismo SKU que p1

    # 1. Comparación de Igualdad
    print("\n--- 1. Igualdad (__eq__) ---")
    print(f"¿p1 == p4? (Mismo SKU 'LAP-001'): {p1 == p4}")
    print(f"¿p1 == p2? (Distinto SKU):        {p1 == p2}")

    # 2. Comparaciones de orden generadas por @total_ordering
    print("\n--- 2. Operadores de Ordenamiento (@total_ordering) ---")
    print(f"¿Mouse < Laptop? ({p2.precio} < {p1.precio}):  {p2 < p1}")
    print(f"¿Laptop > Teclado? ({p1.precio} > {p3.precio}): {p1 > p3}  (generado automáticamente)")
    print(f"¿Mouse <= Teclado?: {p2 <= p3} (generado automáticamente)")

    # 3. Ordenamiento nativo de listas con .sort() y sorted()
    print("\n--- 3. Ordenando colecciones con sorted() nativo ---")
    catalogo = [p1, p2, p3]
    catalogo_ordenado = sorted(catalogo)
    print("Catálogo ordenado por precio ascendente:")
    for prod in catalogo_ordenado:
        print(f"  - {prod}")

    # 4. Hashabilidad en Sets (eliminación de duplicados por SKU)
    print("\n--- 4. Hashabilidad en Sets y Diccionarios ---")
    inventario_sin_duplicados = {p1, p2, p3, p4}
    print(f"Total elementos en set (p1 y p4 son idénticos por SKU): {len(inventario_sin_duplicados)}")
    for prod in inventario_sin_duplicados:
        print(f"  * {prod}")
