"""
==============================================================================
Módulo: 07_proyecto_integrador / modelos.py
Tema: Modelos de Dominio con Dataclasses, Herencia, Encapsulamiento y Validaciones.
==============================================================================
"""

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# MODELO DE USUARIOS (HERENCIA Y ENCAPSULAMIENTO)
# ==============================================================================
class Usuario(ABC):
    """Clase base abstracta de usuario del sistema."""

    def __init__(self, id_usuario: str, nombre: str, email: str):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self._email = email

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, nuevo_email: str) -> None:
        if "@" not in nuevo_email or "." not in nuevo_email:
            raise ValueError(f"Email inválido: {nuevo_email}")
        self._email = nuevo_email

    @abstractmethod
    def obtener_rol(self) -> str:
        pass


class Cliente(Usuario):
    """Cliente comprador con billetera virtual y dirección de envío."""

    def __init__(self, id_usuario: str, nombre: str, email: str, direccion: str, saldo_billetera: float = 0.0):
        super().__init__(id_usuario, nombre, email)
        self.direccion = direccion
        self._saldo_billetera = 0.0
        self.saldo_billetera = saldo_billetera

    @property
    def saldo_billetera(self) -> float:
        return self._saldo_billetera

    @saldo_billetera.setter
    def saldo_billetera(self, monto: float) -> None:
        if monto < 0:
            raise ValueError("El saldo de la billetera no puede ser negativo.")
        self._saldo_billetera = float(monto)

    def obtener_rol(self) -> str:
        return "CLIENTE_ESTANDAR"

    def __repr__(self) -> str:
        return f"Cliente(id={self.id_usuario!r}, nombre={self.nombre!r}, saldo=${self._saldo_billetera:,.2f})"


# ==============================================================================
# MODELO DE PRODUCTOS (JERARQUÍA POLIMÓRFICA)
# ==============================================================================
class Producto(ABC):
    """Contrato base para cualquier producto comercializable."""

    def __init__(self, sku: str, nombre: str, precio_base: float):
        if precio_base <= 0:
            raise ValueError("El precio base debe ser mayor a 0.")
        self._sku = sku.upper()
        self.nombre = nombre
        self.precio_base = float(precio_base)

    @property
    def sku(self) -> str:
        return self._sku

    @abstractmethod
    def calcular_costo_envio(self) -> float:
        """Calcula el costo de transporte/entrega según el tipo de producto."""
        pass

    @abstractmethod
    def entregar(self, cliente: Cliente) -> str:
        """Lógica de despacho o entrega al cliente."""
        pass

    def precio_final_con_envio(self) -> float:
        return self.precio_base + self.calcular_costo_envio()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Producto):
            return NotImplemented
        return self._sku == other._sku

    def __hash__(self) -> int:
        return hash(self._sku)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sku={self._sku!r}, nombre={self.nombre!r}, precio=${self.precio_base:.2f})"


class ProductoFisico(Producto):
    """Producto tangible que requiere transporte físico y peso."""

    def __init__(self, sku: str, nombre: str, precio_base: float, peso_kg: float):
        super().__init__(sku, nombre, precio_base)
        self.peso_kg = float(peso_kg)

    def calcular_costo_envio(self) -> float:
        # Tarifa base de $5 + $2 por cada kilo
        return 5.0 + (self.peso_kg * 2.0)

    def entregar(self, cliente: Cliente) -> str:
        return f"📦 Envíando paquete de {self.peso_kg} kg a la dirección: '{cliente.direccion}'"


class ProductoDigital(Producto):
    """Producto descargable (E-Book, Software, Licencia) sin costo de envío."""

    def __init__(self, sku: str, nombre: str, precio_base: float, url_descarga: str):
        super().__init__(sku, nombre, precio_base)
        self.url_descarga = url_descarga

    def calcular_costo_envio(self) -> float:
        return 0.0  # Envío digital instantáneo y gratuito

    def entregar(self, cliente: Cliente) -> str:
        return f"⚡ Enlace de descarga activado y enviado al email {cliente.email}: {self.url_descarga}"
