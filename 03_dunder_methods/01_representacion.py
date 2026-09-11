"""
==============================================================================
Módulo: 03_dunder_methods / 01_representacion.py
Tema: Métodos Mágicos de Representación: __str__, __repr__ y __format__.
==============================================================================

¿Qué son los Dunder Methods?
----------------------------
"Dunder" es la abreviatura de *Double Underscore* (__metodo__). Son métodos especiales
del Modelo de Datos de Python (*Python Data Model*) que permiten a nuestras clases
personalizadas integrarse de forma nativa con la sintaxis y operadores del lenguaje.

Diferencia Crucial entre `__str__` y `__repr__`:
------------------------------------------------
1. `__repr__(self) -> str`:
   - Audiencia: El DESARROLLADOR / Ingeniero de Software (para debugging y logs).
   - Meta: Ser inequívoco, explícito y, de ser posible, contener el código Python exacto
     que recrearía el objeto (ej. `Punto2D(x=3, y=5)`).
   - Si una clase no define `__str__`, Python usa `__repr__` como respaldo.

2. `__str__(self) -> str`:
   - Audiencia: El USUARIO FINAL.
   - Meta: Ser legible, amigable e intuitivo (ej. `(3, 5)` o `Punto en coordenadas X=3, Y=5`).
   - Se activa al usar `print(obj)`, `str(obj)` o interpolación de strings `f"{obj}"`.

3. `__format__(self, format_spec) -> str`:
   - Permite definir especificadores de formato personalizados con f-strings.
   - Ej: `f"{cuenta:resumen}"` o `f"{cuenta:dolar}"`.
"""

import sys


class Dinero:
    """Representa un valor monetario con divisa y formato avanzado."""

    def __init__(self, monto: float, divisa: str = "USD"):
        self.monto = float(monto)
        self.divisa = divisa.upper()

    def __repr__(self) -> str:
        """Representación formal técnica para desarrolladores."""
        return f"Dinero(monto={self.monto!r}, divisa={self.divisa!r})"

    def __str__(self) -> str:
        """Representación amigable para interfaces de usuario."""
        simbolos = {"USD": "$", "EUR": "€", "COP": "COL$", "GBP": "£"}
        simbolo = simbolos.get(self.divisa, self.divisa)
        return f"{simbolo}{self.monto:,.2f} {self.divisa}"

    def __format__(self, format_spec: str) -> str:
        """Soporte para especificadores personalizados en f-strings."""
        if format_spec == "corto":
            return f"{self.monto:.0f}{self.divisa}"
        elif format_spec == "entero":
            return f"${int(self.monto)}"
        elif format_spec == "tecnico":
            return f"[{self.divisa}:{self.monto:.4f}]"
        # Si no hay especificador o es estándar, usamos __str__
        return str(self)


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 01 - Métodos de Representación: __str__, __repr__, __format__")
    print("=" * 65)

    precio = Dinero(1250.75, "USD")
    ahorros = Dinero(5000000.00, "COP")

    # 1. Diferencia entre __str__ y __repr__
    print("\n--- 1. Salida de __str__ (Amigable al usuario) ---")
    print(f"str(precio):   {str(precio)}")
    print(f"print(precio): {precio}")

    print("\n--- 2. Salida de __repr__ (Técnica para desarrollador) ---")
    print(f"repr(precio):   {repr(precio)}")
    print(f"En colecciones: {[precio, ahorros]}")  # ¡Las listas usan __repr__ de sus elementos!

    # 3. Especificadores personalizados con __format__
    print("\n--- 3. Especificadores personalizados con f-strings ---")
    print(f"Formato por defecto: {precio}")
    print(f"Formato ':corto':   {precio:corto}")
    print(f"Formato ':entero':  {precio:entero}")
    print(f"Formato ':tecnico': {precio:tecnico}")
