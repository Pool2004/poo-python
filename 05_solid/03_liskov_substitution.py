"""
==============================================================================
Módulo: 05_solid / 03_liskov_substitution.py
Tema: Principio de Sustitución de Liskov (LSP - Liskov Substitution Principle).
==============================================================================

Definición de Barbara Liskov (1987):
-----------------------------------
> "Si por cada objeto o1 de tipo S existe un objeto o2 de tipo T tal que para
>  todos los programas P definidos en términos de T, el comportamiento de P
>  no cambia cuando o1 se sustituye por o2, entonces S es un subtipo de T."

En lenguaje simple:
-------------------
Las clases derivadas (hijas) deben poder ser utilizadas como sustitutos directos
de sus clases base (padres) sin romper la lógica del programa ni arrojar comportamientos
inesperados (como lanzar excepciones sorpresivas o violar invariantes).

Ejemplos Clásicos de Violación:
-------------------------------
1. El Pingüino o Avestruz heredando de `Ave` con método `volar()`.
   Como el pingüino no vuela, el desarrollador suele poner `raise Exception("No puedo volar")`.
   ¡Cualquier función que itere sobre aves y llame a `.volar()` explotará!
2. El Cuadrado heredando del Rectángulo modificando silenciosamente el ancho al cambiar el alto.
"""

import sys
from abc import ABC, abstractmethod

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. ANTIPATRÓN: VIOLACIÓN DEL PRINCIPIO DE LISKOV
# ==============================================================================
class AveIncorrecta(ABC):
    @abstractmethod
    def comer(self) -> str:
        pass

    @abstractmethod
    def volar(self) -> str:
        pass


class Halcon(AveIncorrecta):
    def comer(self) -> str:
        return "El halcón caza y come carne."

    def volar(self) -> str:
        return "El halcón vuela a 300 km/h."


class PinguinoIncorrecto(AveIncorrecta):
    def comer(self) -> str:
        return "El pingüino come peces."

    def volar(self) -> str:
        # ¡VIOLA LSP! La firma promete que vuela, pero rompe en ejecución
        raise NotImplementedError("❌ ¡Los pingüinos no pueden volar!")


# ==============================================================================
# 2. DISEÑO CORRECTO RESPETANDO LISKOV (Jerarquía Fiel al Dominio)
# ==============================================================================
class Ave(ABC):
    """Comportamiento garantizado para TODAS las aves."""

    def __init__(self, especie: str):
        self.especie = especie

    @abstractmethod
    def alimentarse(self) -> str:
        pass


class AveVoladora(Ave):
    """Subtipo especializado: Garantiza contractualmente que puede volar."""

    @abstractmethod
    def volar(self) -> str:
        pass


class Aguila(AveVoladora):
    def alimentarse(self) -> str:
        return f"{self.especie}: Caza presas pequeñas."

    def volar(self) -> str:
        return f"{self.especie}: Vuela planeando a gran altitud."


class Pinguino(Ave):
    """Hereda de Ave, pero NO de AveVoladora. No rompe ningún contrato."""

    def alimentarse(self) -> str:
        return f"{self.especie}: Se alimenta nadando tras cardúmenes de peces."

    def nadar(self) -> str:
        return f"{self.especie}: Nada a gran velocidad bajo el agua polar."


# Funciones consumidoras que confían ciegamente en sus contratos
def liberar_en_el_aire(aves: list[AveVoladora]) -> None:
    """Esta función sólo acepta aves que garantizan que pueden volar."""
    for ave in aves:
        print(f"🛫 {ave.volar()}")


def alimentar_santuario(aves: list[Ave]) -> None:
    """Esta función acepta a CUALQUIER ave."""
    for ave in aves:
        print(f"🌾 {ave.alimentarse()}")


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 03 - Principio de Sustitución de Liskov (LSP)")
    print("=" * 65)

    aguila = Aguila("Águila Real")
    pinguino = Pinguino("Pingüino Emperador")

    # 1. Alimentar a todas las aves (LSP garantizado para la clase base Ave)
    print("\n--- 1. Sustitución Segura en la Clase Base Ave ---")
    alimentar_santuario([aguila, pinguino])

    # 2. Vuelo garantizado sin excepciones
    print("\n--- 2. Vuelo exclusivo de AveVoladora ---")
    flota_aerea: list[AveVoladora] = [aguila]
    liberar_en_el_aire(flota_aerea)

    print("\n✨ Gracias al diseño LSP, el pingüino jamás causará un fallo en tiempo")
    print("   de ejecución porque su tipo refleja sus verdaderas capacidades.")
