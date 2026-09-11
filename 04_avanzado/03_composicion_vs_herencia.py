"""
==============================================================================
Módulo: 04_avanzado / 03_composicion_vs_herencia.py
Tema: Principio de Diseño: Composición vs Herencia ("Favor Composition over Inheritance").
==============================================================================

El Dilema: "¿Es-Un" vs "¿Tiene-Un"?
-----------------------------------
- Herencia ("Es-Un" / "Is-A"):
  Representa una relación biológica o taxonómica estricta (ej. `Perro` es un `Mamífero`).
  - Problema: Acoplamiento fuerte. Modificar la clase padre puede romper subclases
    inesperadamente ("Fragile Base Class Problem"). Además, no se puede cambiar el
    comportamiento en tiempo de ejecución.

- Composición ("Tiene-Un" / "Has-A"):
  Construye objetos complejos ensamblando partes más pequeñas e independientes
  (ej. Un `Auto` "tiene un" `Motor` y "tiene un" `SistemaDeFrenos`).
  - Ventaja: Desacoplamiento total, alta reutilización, facilidad para pruebas unitarias
    y posibilidad de intercambiar piezas en tiempo de ejecución (Run-time).

La Explosión Combinatoria de la Herencia:
----------------------------------------
Si usamos herencia para modelar combinaciones:
- `AutoGasolina`
- `AutoElectrico`
- `AutoGasolinaConFrenosABS`
- `AutoElectricoConFrenosABS`
- `AutoHibridoConFrenosCeramicos`
¡El número de clases explota exponencialmente! Con composición, sólo creamos
UNA clase `Automovil` a la cual le inyectamos el `Motor` y los `Frenos` deseados.
"""

import sys
from abc import ABC, abstractmethod


# ==============================================================================
# COMPONENTES COMPONIBLES (CONTRATOS DE ABSTRACCIÓN)
# ==============================================================================
class Motor(ABC):
    """Componente abstracto de propulsión."""

    @abstractmethod
    def encender(self) -> str:
        pass

    @abstractmethod
    def tipo_combustible(self) -> str:
        pass


class MotorGasolina(Motor):
    def encender(self) -> str:
        return "🔥 Rugido de pistones e inyección de gasolina (V6 3.0L)"

    def tipo_combustible(self) -> str:
        return "Gasolina Extra"


class MotorElectrico(Motor):
    def encender(self) -> str:
        return "⚡ Silbido magnético de inducción eléctrica trifásica (300 kW)"

    def tipo_combustible(self) -> str:
        return "Electricidad (Batería Li-Ion)"


class SistemaFrenos(ABC):
    """Componente abstracto de frenado."""

    @abstractmethod
    def frenar(self) -> str:
        pass


class FrenosABS(SistemaFrenos):
    def frenar(self) -> str:
        return "🛑 Antibloqueo modulando presión a 15 pulsos/segundo."


class FrenosCarbonoCeramicos(SistemaFrenos):
    def frenar(self) -> str:
        return "🏎️ Frenado de ultra alto rendimiento cerámico sin desvanecimiento térmico."


# ==============================================================================
# CLASE ENSAMBLADA POR COMPOSICIÓN
# ==============================================================================
class Automovil:
    """Clase cliente que 'Tiene-Un' Motor y 'Tiene-Un' Sistema de Frenos."""

    def __init__(self, modelo: str, motor: Motor, frenos: SistemaFrenos):
        self.modelo = modelo
        # Composición: los componentes se inyectan como atributos
        self.motor = motor
        self.frenos = frenos

    def arrancar(self) -> None:
        print(f"🚗 [{self.modelo}] Arrancando:")
        print(f"   Fuente de energía: {self.motor.tipo_combustible()}")
        print(f"   Motor:             {self.motor.encender()}")

    def detener(self) -> None:
        print(f"🛑 [{self.modelo}] Frenando a fondo: {self.frenos.frenar()}")

    def cambiar_motor(self, nuevo_motor: Motor) -> None:
        """Demuestra la enorme ventaja de la composición: ¡Intercambio en tiempo de ejecución!"""
        print(f"\n🔧 [TALLER] Sustituyendo motor en {self.modelo}...")
        self.motor = nuevo_motor


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 03 - Composición vs Herencia")
    print("=" * 65)

    # 1. Ensamblamos un deportivo de combustión
    print("\n--- 1. Ensamble por Composición: Deportivo Gasolina ---")
    motor_v6 = MotorGasolina()
    frenos_abs = FrenosABS()
    auto_pasion = Automovil("Mustang GT", motor=motor_v6, frenos=frenos_abs)

    auto_pasion.arrancar()
    auto_pasion.detener()

    # 2. Ensamblamos un sedán eléctrico con frenos carbocerámicos
    print("\n--- 2. Ensamble por Composición: Hypercar Eléctrico ---")
    motor_ev = MotorElectrico()
    frenos_pro = FrenosCarbonoCeramicos()
    auto_futuro = Automovil("Taycan Turbo", motor=motor_ev, frenos=frenos_pro)

    auto_futuro.arrancar()
    auto_futuro.detener()

    # 3. Flexibilidad Dinámica: Cambiar el motor de Mustang a Eléctrico (Conversión Retrofit EV)
    print("\n--- 3. Modificación en Tiempo de Ejecución (Imposible con Herencia pura) ---")
    auto_pasion.cambiar_motor(MotorElectrico())
    auto_pasion.arrancar()
