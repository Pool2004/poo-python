"""
==============================================================================
Módulo: 03_dunder_methods / 03_operadores_aritmeticos.py
Tema: Sobrecarga de Operadores Aritméticos, Reflejados e In-Place.
==============================================================================

La Sobrecarga de Operadores en Python:
-------------------------------------
Permite que objetos de clases personalizadas utilicen operadores nativos
como `+`, `-`, `*`, `/`, `abs()`, etc.

Tres Familias de Métodos Aritméticos:
------------------------------------
1. Operadores Estándar (Izquierda):
   `a + b`  ->  `a.__add__(b)`
   `a - b`  ->  `a.__sub__(b)`
   `a * b`  ->  `a.__mul__(b)`

2. Operadores Reflejados o Reversos (Derecha):
   Si `a` es un entero primitivo (como `3`) y `v` es nuestro Vector:
   `3 * v`  -> Python intenta `(3).__mul__(v)`. Como el entero no conoce
               nuestra clase, retorna `NotImplemented`.
               Inmediatamente Python busca en el lado derecho: `v.__rmul__(3)`.

3. Operadores In-Place (Asignación Aumentada):
   `v += otro`  ->  `v.__iadd__(otro)`

4. Operadores Unarios:
   `-v`    -> `__neg__`
   `abs(v)` -> `__abs__`
"""

import math
import sys


class Vector2D:
    """Modela un vector bidimensional en física o gráficos con álgebra vectorial completa."""

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    # --- 1. OPERADORES UNARIOS ---
    def __neg__(self) -> "Vector2D":
        """Inversión de signo: -v"""
        return Vector2D(-self.x, -self.y)

    def __abs__(self) -> float:
        """Magnitud / Norma Euclidiana del vector: abs(v)"""
        return math.hypot(self.x, self.y)

    # --- 2. SUMA Y RESTA (+, -) ---
    def __add__(self, other: object) -> "Vector2D":
        """Suma vectorial: v1 + v2"""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: object) -> "Vector2D":
        """Resta vectorial: v1 - v2"""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)

    # --- 3. MULTIPLICACIÓN (*) ---
    def __mul__(self, other: object):
        """Multiplicación:
        - Si es un escalar (int/float): Escalamiento v * 2
        - Si es otro Vector2D: Producto Punto (Dot Product)
        """
        if isinstance(other, (int, float)):
            return Vector2D(self.x * other, self.y * other)
        elif isinstance(other, Vector2D):
            # Producto punto (retorna un escalar escalar)
            return (self.x * other.x) + (self.y * other.y)
        return NotImplemented

    # --- 4. OPERADOR REFLEJADO (__rmul__) ---
    def __rmul__(self, other: object):
        """Permite la multiplicación por izquierda: 2 * v"""
        return self.__mul__(other)

    # --- 5. OPERADOR IN-PLACE (__iadd__) ---
    def __iadd__(self, other: object) -> "Vector2D":
        """Asignación aumentada: v += otro (optimización mutable si aplica)"""
        if not isinstance(other, Vector2D):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}i + {self.y}j)"


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 03 - Sobrecarga de Operadores Aritméticos")
    print("=" * 65)

    v1 = Vector2D(3, 4)
    v2 = Vector2D(1, 2)

    print(f"Vector 1 (v1): {v1} | Magnitud: {abs(v1)}")
    print(f"Vector 2 (v2): {v2} | Magnitud: {abs(v2):.2f}")

    # 1. Suma y Resta
    print("\n--- 1. Suma y Resta ---")
    v_suma = v1 + v2
    v_resta = v1 - v2
    print(f"v1 + v2 = {v_suma}")
    print(f"v1 - v2 = {v_resta}")

    # 2. Escalamiento (Operador normal y reflejado)
    print("\n--- 2. Multiplicación por Escalar (Normal y Reflejada) ---")
    v_escalado = v1 * 3
    print(f"v1 * 3 (v.__mul__(3)) = {v_escalado}")

    v_reflejado = 3 * v1  # 3 no sabe qué es Vector2D, entra __rmul__
    print(f"3 * v1 (v.__rmul__(3)) = {v_reflejado}")

    # 3. Producto Punto (Dot Product)
    print("\n--- 3. Producto Punto Vectorial ---")
    producto_punto = v1 * v2  # (3*1) + (4*2) = 11
    print(f"v1 * v2 (Producto Punto) = {producto_punto}")

    # 4. Operador Unario Inverso
    print("\n--- 4. Negación Unaria (-v) ---")
    print(f"-v1 = {-v1}")

    # 5. Operador In-Place (+=)
    print("\n--- 5. Operador In-Place (+=) ---")
    print(f"v1 antes de += : {v1}")
    v1 += Vector2D(10, 10)
    print(f"v1 después de +=: {v1}")
