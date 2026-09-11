"""
==============================================================================
Módulo: 05_solid / 02_open_closed.py
Tema: Principio de Abierto / Cerrado (OCP - Open/Closed Principle).
==============================================================================

Definición de Bertrand Meyer:
-----------------------------
> "Las entidades de software (clases, módulos, funciones) deben estar abiertas
>  para su extensión, pero cerradas para su modificación."

¿Qué significa en la práctica?
------------------------------
- **Abierto para extensión**: Debemos poder agregar nuevos comportamientos o funcionalidades
  al sistema con facilidad.
- **Cerrado para modificación**: Al agregar esa nueva funcionalidad, NO deberíamos tener
  que alterar el código fuente ya existente y probado en producción (reduciendo el riesgo de regresiones).

Antipatrón común:
-----------------
El uso de cadenas interminables de `if / elif / else` basadas en tipos o strings.
Cada vez que el negocio inventa una nueva regla, tienes que editar la función original.
"""

import sys
from abc import ABC, abstractmethod

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. ANTIPATRÓN: VIOLA OCP CON IF/ELIF FRÁGILES
# ==============================================================================
class CalculadoraDescuentoIncorreta:
    """VIOLA OCP: Si agregamos un descuento de 'CIBERLUNES', hay que MODIFICAR este código."""

    def calcular(self, tipo_cliente: str, monto: float) -> float:
        if tipo_cliente == "REGULAR":
            return monto * 0.05
        elif tipo_cliente == "VIP":
            return monto * 0.20
        elif tipo_cliente == "EMPLEADO":
            return monto * 0.30
        # Cada nuevo caso requiere tocar esta función...
        return 0.0


# ==============================================================================
# 2. DISEÑO REFRACTORIZADO APLICANDO OCP (POLIMORFISMO Y ABSTRACCIÓN)
# ==============================================================================
class EstrategiaDescuento(ABC):
    """Contrato base abierto a extensiones."""

    @abstractmethod
    def calcular_descuento(self, monto: float) -> float:
        pass

    @property
    @abstractmethod
    def nombre(self) -> str:
        pass


# Extensiones independientes (Nuevas clases sin tocar las existentes)
class DescuentoRegular(EstrategiaDescuento):
    @property
    def nombre(self) -> str:
        return "Cliente Regular (5%)"

    def calcular_descuento(self, monto: float) -> float:
        return monto * 0.05


class DescuentoVIP(EstrategiaDescuento):
    @property
    def nombre(self) -> str:
        return "Cliente VIP Oro (20%)"

    def calcular_descuento(self, monto: float) -> float:
        return monto * 0.20


class DescuentoBlackFriday(EstrategiaDescuento):
    """¡Nueva promoción agregada sin tocar ninguna clase anterior!"""

    @property
    def nombre(self) -> str:
        return "Promo Black Friday (40%)"

    def calcular_descuento(self, monto: float) -> float:
        return monto * 0.40


# Clase consumidora: Cerrada a modificaciones
class ProcesadorVentas:
    """Calcula precios finales recibiendo cualquier estrategia que cumpla el contrato."""

    def calcular_total_con_descuento(self, monto: float, estrategia: EstrategiaDescuento) -> float:
        descuento = estrategia.calcular_descuento(monto)
        total_final = monto - descuento
        print(f"💰 Monto Base: ${monto:,.2f} | {estrategia.nombre} -> Descuento: -${descuento:,.2f} | Total: ${total_final:,.2f}")
        return total_final


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 02 - Principio de Abierto/Cerrado (OCP)")
    print("=" * 65)

    procesador = ProcesadorVentas()
    monto_compra = 1000.0

    print("\n--- Procesando ventas con diferentes estrategias ---")
    procesador.calcular_total_con_descuento(monto_compra, DescuentoRegular())
    procesador.calcular_total_con_descuento(monto_compra, DescuentoVIP())
    procesador.calcular_total_con_descuento(monto_compra, DescuentoBlackFriday())
