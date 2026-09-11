"""
==============================================================================
Módulo: 02_pilares / 03_herencia.py
Tema: Tercer Pilar: Herencia Simple, Herencia Múltiple, MRO y Mixins.
==============================================================================

¿Qué es la Herencia?
--------------------
Es el mecanismo mediante el cual una clase (clase hija o subclase) adquiere los
atributos y métodos de otra clase (clase madre, base o superclase). Modela una
relación de tipo "Es-Un" (por ejemplo: un `Perro` "es un" `Animal`).

Conceptos Fundamentales:
------------------------
1. `super()`:
   Permite invocar métodos de la superclase de forma dinámica y cooperativa sin
   tener que codificar rígidamente el nombre de la clase padre.

2. Herencia Múltiple:
   Python permite que una clase herede de dos o más clases al mismo tiempo.

3. El Problema del Diamante y el MRO (Method Resolution Order):
   Cuando una clase D hereda de B y C, y ambas heredan de A: ¿cuál método se ejecuta
   si tanto B como C sobreescriben un método de A?
   Python resuelve esto mediante el algoritmo **C3 Linearization**, garantizando:
   - Los hijos se evalúan antes que los padres.
   - Si hay múltiples padres, se evalúan en el orden exacto especificado en la definición.
   - Sin duplicados ni inconsistencias.
   Se puede consultar el orden exacto con `Clase.mro()` o `Clase.__mro__`.

4. Mixins:
   Son clases pequeñas y especializadas concebidas NO para ser instanciadas por sí solas,
   sino para "mezclar" o inyectar funcionalidades específicas en otras clases sin crear
   árboles de herencia profundos.
"""

import json
import sys


# ==============================================================================
# 1. HERENCIA SIMPLE Y super()
# ==============================================================================
class Vehiculo:
    """Clase base general."""

    def __init__(self, marca: str, modelo: str, anio: int):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    def descripcion(self) -> str:
        return f"{self.marca} {self.modelo} ({self.anio})"

    def mover(self) -> str:
        return "El vehículo se está desplazando por una vía."


class AutoElectrico(Vehiculo):
    """Subclase que extiende Vehiculo agregando capacidad de batería."""

    def __init__(self, marca: str, modelo: str, anio: int, capacidad_bateria_kwh: float):
        # Invocamos el constructor de la superclase
        super().__init__(marca, modelo, anio)
        self.capacidad_bateria_kwh = capacidad_bateria_kwh

    # Sobrescritura de método extendiendo el comportamiento base con super()
    def descripcion(self) -> str:
        base = super().descripcion()
        return f"{base} [Eléctrico: {self.capacidad_bateria_kwh} kWh]"

    def mover(self) -> str:
        return "El auto eléctrico rueda silenciosamente con propulsión eléctrica."


# ==============================================================================
# 2. HERENCIA MÚLTIPLE Y MIXINS
# ==============================================================================
class JSONSerializableMixin:
    """Mixin que otorga a cualquier clase la capacidad de exportarse a JSON."""

    def to_json(self) -> str:
        """Serializa los atributos del objeto a formato JSON."""
        return json.dumps(self.__dict__, indent=2, ensure_ascii=False)


class LoggableMixin:
    """Mixin que provee capacidades de auditoría/logging."""

    def log(self, accion: str) -> None:
        print(f"📋 [AUDITORÍA]: Objeto {self.__class__.__name__} ejecutó acción -> '{accion}'")


# ==============================================================================
# 3. EL PROBLEMA DEL DIAMANTE Y MRO (Method Resolution Order)
# ==============================================================================
class DispositivoA:
    """Nodo raíz del diamante."""

    def encender(self) -> str:
        return "DispositivoA: Energía base activada."


class TelefonoB(DispositivoA):
    def encender(self) -> str:
        return f"TelefonoB: Módem celular activado -> {super().encender()}"


class CamaraC(DispositivoA):
    def encender(self) -> str:
        return f"CamaraC: Sensor de imagen calibrado -> {super().encender()}"


class SmartphoneD(TelefonoB, CamaraC, JSONSerializableMixin, LoggableMixin):
    """Nodo final: Hereda de TelefonoB, CamaraC y dos Mixins."""

    def __init__(self, marca: str, modelo: str, camara_mpx: int):
        self.marca = marca
        self.modelo = modelo
        self.camara_mpx = camara_mpx

    def encender(self) -> str:
        return f"SmartphoneD: Arranque completo -> {super().encender()}"


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 03 - Herencia Simple, Múltiple, MRO y Mixins")
    print("=" * 65)

    # 1. Herencia simple
    print("\n--- 1. Herencia Simple y super() ---")
    tesla = AutoElectrico("Tesla", "Model 3", 2024, 75.0)
    print(f"Descripción: {tesla.descripcion()}")
    print(f"Movimiento:  {tesla.mover()}")
    print(f"¿Es instancia de Vehiculo?     {isinstance(tesla, Vehiculo)}")
    print(f"¿AutoElectrico es subclase?   {issubclass(AutoElectrico, Vehiculo)}")

    # 2. Herencia múltiple con Mixins
    print("\n--- 2. Capacidades de los Mixins en SmartphoneD ---")
    celular = SmartphoneD("Google", "Pixel 9", camara_mpx=50)

    # Capacidad provista por LoggableMixin
    celular.log("Toma de fotografía nocturna")

    # Capacidad provista por JSONSerializableMixin
    print("\nExportación a JSON (vía Mixin):")
    print(celular.to_json())

    # 3. El diamante y el MRO
    print("\n--- 3. Resolución del Diamante y MRO ---")
    print("Secuencia de encendido cooperativo:")
    print(celular.encender())

    print("\nOrden de Resolución de Métodos (MRO) para SmartphoneD:")
    for indice, clase in enumerate(SmartphoneD.mro(), start=1):
        print(f"  {indice}. {clase.__name__}")
