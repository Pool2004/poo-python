"""
==============================================================================
Módulo: 07_proyecto_integrador / pasarelas.py
Tema: Abstracción y Polimorfismo en Procesamiento de Pagos.
==============================================================================
"""

import sys
from abc import ABC, abstractmethod

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ResultadoTransaccion:
    """Contenedor de respuesta de cobro."""

    def __init__(self, exitoso: bool, id_transaccion: str, mensaje: str, monto: float):
        self.exitoso = exitoso
        self.id_transaccion = id_transaccion
        self.mensaje = mensaje
        self.monto = monto

    def __repr__(self) -> str:
        estado = "APROBADO ✅" if self.exitoso else "RECHAZADO ❌"
        return f"[{estado}] Ref: {self.id_transaccion} | Monto: ${self.monto:,.2f} | {self.mensaje}"


class PasarelaPago(ABC):
    """Interfaz abstracta que desacopla la aplicación de los proveedores de pago."""

    @property
    @abstractmethod
    def nombre(self) -> str:
        pass

    @abstractmethod
    def procesar_pago(self, monto: float, referencia: str) -> ResultadoTransaccion:
        pass


class StripePasarela(PasarelaPago):
    """Implementación de cobro con tarjeta de crédito vía Stripe."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def nombre(self) -> str:
        return "Stripe Credit Cards"

    def procesar_pago(self, monto: float, referencia: str) -> ResultadoTransaccion:
        # Simulación de transacción de red
        if monto > 10_000:
            return ResultadoTransaccion(False, "N/A", "Límite de tarjeta excedido", monto)

        tx_id = f"str_ch_{abs(hash(referencia)) % 1000000}"
        return ResultadoTransaccion(True, tx_id, "Cargo a tarjeta aprobado exitosamente", monto)


class PayPalPasarela(PasarelaPago):
    """Implementación de cobro mediante cuenta PayPal."""

    def __init__(self, client_id: str):
        self.client_id = client_id

    @property
    def nombre(self) -> str:
        return "PayPal Sandbox"

    def procesar_pago(self, monto: float, referencia: str) -> ResultadoTransaccion:
        tx_id = f"PAYPAL-TX-{abs(hash(referencia)) % 999999}"
        return ResultadoTransaccion(True, tx_id, "Pago procesado con cuenta PayPal", monto)
