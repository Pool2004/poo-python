"""
==============================================================================
Módulo: 02_pilares / 02_abstraccion.py
Tema: Segundo Pilar: Abstracción, Clases Base Abstractas (ABC) e Interfaces.
==============================================================================

¿Qué es la Abstracción?
-----------------------
Es el proceso de simplificar sistemas complejos modelando clases apropiadas para
el problema, ocultando los detalles irrelevantes de implementación y enfatizando
lo esencial (el "qué hace" por sobre el "cómo lo hace").

En Python: Clases Base Abstractas (ABCs)
---------------------------------------
Python provee el módulo `abc` (Abstract Base Classes) para definir abstracciones formales:
1. Heredar de `abc.ABC`.
2. Usar el decorador `@abstractmethod` sobre los métodos que CADA subclase está
   OBLIGADA a implementar.

Reglas Clave:
-------------
- No se puede instanciar directamente una clase que contenga métodos abstractos sin implementar.
  Si lo intentas, Python arroja un `TypeError`.
- Permite definir "Contratos" o "Interfaces" que garantizan que cualquier clase derivada
  tendrá la misma estructura y métodos esperados.
- Se pueden combinar `@property` y `@abstractmethod` para exigir que las subclases tengan
  ciertas propiedades obligatorias.
"""

import sys
from abc import ABC, abstractmethod


class PasarelaPago(ABC):
    """Clase Base Abstracta (Contrato de Pago).

    Define los métodos obligatorios que cualquier procesador de pagos
    (Stripe, PayPal, Cripto, etc.) debe cumplir.
    """

    def __init__(self, clave_api: str):
        self.clave_api = clave_api

    # --- PROPIEDAD ABSTRACTA ---
    @property
    @abstractmethod
    def nombre_proveedor(self) -> str:
        """Nombre del proveedor. Cada subclase DEBE proveer su propio nombre."""
        pass

    # --- MÉTODO ABSTRACTO ---
    @abstractmethod
    def procesar_cobro(self, monto: float, referencia: str) -> dict:
        """Procesa un cobro. Debe ser implementado por la pasarela concreta.

        Retorna un dict con el resultado de la transacción.
        """
        pass

    @abstractmethod
    def emitir_reembolso(self, id_transaccion: str, monto: float) -> bool:
        """Emite un reembolso hacia el cliente original."""
        pass

    # --- MÉTODO CONCRETO (Lógica común compartida) ---
    def registrar_log(self, mensaje: str) -> None:
        """Método no-abstracto que todas las pasarelas pueden reutilizar directamente."""
        print(f"📝 [LOG {self.nombre_proveedor}]: {mensaje}")


# ==============================================================================
# SUBCLASES CONCRETAS
# ==============================================================================
class PasarelaStripe(PasarelaPago):
    """Implementación concreta de la pasarela Stripe."""

    @property
    def nombre_proveedor(self) -> str:
        return "Stripe Payments"

    def procesar_cobro(self, monto: float, referencia: str) -> dict:
        self.registrar_log(f"Iniciando cargo con token API '{self.clave_api[:6]}***'")
        # Simulación de llamada HTTP a la API de Stripe
        return {
            "exito": True,
            "id_transaccion": f"ch_stripe_{hash(referencia) % 1000000}",
            "monto": monto,
            "moneda": "USD",
            "pasarela": self.nombre_proveedor
        }

    def emitir_reembolso(self, id_transaccion: str, monto: float) -> bool:
        self.registrar_log(f"Reembolso de ${monto} procesado para {id_transaccion}")
        return True


class PasarelaPayPal(PasarelaPago):
    """Implementación concreta de la pasarela PayPal."""

    @property
    def nombre_proveedor(self) -> str:
        return "PayPal Express"

    def procesar_cobro(self, monto: float, referencia: str) -> dict:
        self.registrar_log(f"Redirigiendo a sandbox de PayPal con client_id '{self.clave_api[:6]}...'")
        return {
            "exito": True,
            "id_transaccion": f"PAYPAL-TX-{hash(referencia) % 888888}",
            "monto": monto,
            "moneda": "EUR",
            "pasarela": self.nombre_proveedor
        }

    def emitir_reembolso(self, id_transaccion: str, monto: float) -> bool:
        self.registrar_log(f"Reembolso PayPal emitido por ${monto} en cuenta.")
        return True


class PasarelaIncompleta(PasarelaPago):
    """Clase defectuosa que OLVIDA implementar los métodos abstractos obligatorios."""
    pass


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 02 - Abstracción y Clases Base Abstractas (ABC)")
    print("=" * 65)

    # 1. Intentar instanciar la clase abstracta directamente (Falla por diseño)
    print("\n--- 1. Protección contra instanciación de clases abstractas ---")
    try:
        pasarela = PasarelaPago("clave_secreta")
    except TypeError as err:
        print(f"🛡️ Bloqueado intento de instanciar PasarelaPago abstracta:")
        print(f"   {err}")

    # 2. Intentar instanciar una subclase que olvidó implementar los métodos abstractos
    print("\n--- 2. Protección si una subclase olvida implementar el contrato ---")
    try:
        pasarela_incompleta = PasarelaIncompleta("clave_123")
    except TypeError as err:
        print(f"🛡️ Bloqueado: PasarelaIncompleta no implementó los métodos abstractos:")
        print(f"   {err}")

    # 3. Uso de implementaciones concretas que sí cumplen el contrato
    print("\n--- 3. Ejecución con Implementaciones Válidas ---")
    pasarelas: list[PasarelaPago] = [
        PasarelaStripe("sk_live_98374928374"),
        PasarelaPayPal("client_id_paypal_88231")
    ]

    for pasarela in pasarelas:
        print(f"\nProcesando con: {pasarela.nombre_proveedor}")
        resultado = pasarela.procesar_cobro(149.99, referencia="orden_usuario_42")
        print(f"Resultado recibido: {resultado}")
        pasarela.emitir_reembolso(resultado["id_transaccion"], 149.99)
