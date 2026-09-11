"""
==============================================================================
Módulo: 05_solid / 04_interface_segregation.py
Tema: Principio de Segregación de Interfaces (ISP - Interface Segregation Principle).
==============================================================================

Definición:
-----------
> "Los clientes no deben verse forzados a depender de interfaces o métodos que no utilizan."

En lugar de crear interfaces gigantescas ("Interfaces Gordas" o Fat Interfaces) con
docenas de métodos para cubrir todos los escenarios posibles, es mucho mejor diseñar
múltiples interfaces pequeñas, granulares y altamente cohesivas.

En Python:
----------
Se implementa mediante Clases Abstractas (`abc.ABC`) o Protocolos (`typing.Protocol`).
Una clase concreta puede heredar o implementar múltiples interfaces pequeñas según
sus capacidades reales.
"""

import sys
from abc import ABC, abstractmethod

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. ANTIPATRÓN: INTERFAZ GORDA QUE VIOLA ISP
# ==============================================================================
class DispositivoOficinaMonolitico(ABC):
    """VIOLA ISP: Obliga a cualquier impresora simple a saber de faxes y escaneos."""

    @abstractmethod
    def imprimir(self, documento: str) -> None:
        pass

    @abstractmethod
    def escanear(self) -> str:
        pass

    @abstractmethod
    def enviar_fax(self, numero: str) -> None:
        pass


class ImpresoraTermicaTicketsIncorreta(DispositivoOficinaMonolitico):
    """Sólo imprime tirillas de pago, pero la interfaz le exige implementar fax y escáner."""

    def imprimir(self, documento: str) -> None:
        print(f"Imprimiendo ticket: {documento}")

    def escanear(self) -> str:
        # Método forzado e inútil
        raise NotImplementedError("Este dispositivo no tiene hardware de escáner.")

    def enviar_fax(self, numero: str) -> None:
        # Método forzado e inútil
        raise NotImplementedError("Este dispositivo no tiene módem de fax.")


# ==============================================================================
# 2. DISEÑO REFRACTORIZADO APLICANDO ISP (INTERFACES SEGREGADAS)
# ==============================================================================
class DispositivoImpresion(ABC):
    """Interfaz pequeña: Exclusiva para emitir impresiones."""

    @abstractmethod
    def imprimir(self, contenido: str) -> None:
        pass


class DispositivoEscaneo(ABC):
    """Interfaz pequeña: Exclusiva para digitalizar documentos."""

    @abstractmethod
    def escanear(self) -> str:
        pass


class DispositivoFax(ABC):
    """Interfaz pequeña: Exclusiva para transmisión por fax."""

    @abstractmethod
    def enviar_fax(self, destino: str, contenido: str) -> None:
        pass


# Implementación 1: Impresora básica de punto de venta (Sólo implementa lo que hace)
class ImpresoraTermicaPOS(DispositivoImpresion):
    def imprimir(self, contenido: str) -> None:
        print(f"🧾 [TICKET POS]: Imprimiendo recibo térmico -> '{contenido}'")


# Implementación 2: Máquina multifuncional corporativa (Implementa las interfaces que necesita)
class ImpresoraMultifuncional(DispositivoImpresion, DispositivoEscaneo, DispositivoFax):
    def imprimir(self, contenido: str) -> None:
        print(f"🖨️ [MULTIFUNCIONAL]: Imprimiendo a color en alta calidad -> '{contenido}'")

    def escanear(self) -> str:
        print("🔍 [MULTIFUNCIONAL]: Escaneando superficie plana a 1200 DPI...")
        return "imagen_escaneada.png"

    def enviar_fax(self, destino: str, contenido: str) -> None:
        print(f"📠 [MULTIFUNCIONAL]: Transmitiendo fax a {destino}...")


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 04 - Principio de Segregación de Interfaces (ISP)")
    print("=" * 65)

    pos = ImpresoraTermicaPOS()
    multifuncional = ImpresoraMultifuncional()

    # 1. Función que sólo requiere capacidad de imprimir
    def procesar_recibo(impresora: DispositivoImpresion, texto: str):
        impresora.imprimir(texto)

    print("\n--- 1. Ambos dispositivos cumplen DispositivoImpresion ---")
    procesar_recibo(pos, "Compra $45.00 - Aprobado")
    procesar_recibo(multifuncional, "Reporte Trimestral Financiero")

    # 2. La multifuncional puede realizar tareas adicionales sin contaminar a la POS
    print("\n--- 2. Capacidades segregadas de la multifuncional ---")
    doc_digital = multifuncional.escanear()
    multifuncional.enviar_fax("+1-800-555-0199", doc_digital)
