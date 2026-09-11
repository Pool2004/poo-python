"""
==============================================================================
Módulo: 06_patrones_diseno / 03_comportamiento.py
Tema: Patrones de Comportamiento: Strategy, Observer y Command.
==============================================================================

Los Patrones de Comportamiento:
-------------------------------
Se ocupan de los algoritmos y la asignación de responsabilidades entre objetos.
Describen no sólo los patrones de objetos o clases, sino también los patrones de
comunicación entre ellos.

1. Strategy (Estrategia):
   Define una familia de algoritmos, encapsula cada uno y los hace intercambiables.
   Permite que el algoritmo varíe independientemente de los clientes que lo usan.

2. Observer (Observador / Publicador-Suscriptor):
   Define una dependencia de uno-a-muchos entre objetos, de manera que cuando un
   objeto cambia de estado, todos sus dependientes son notificados y actualizados
   automáticamente.

3. Command (Comando):
   Encapsula una petición o acción como un objeto autónomo. Esto permite parametrizar
   clientes con diferentes peticiones, encolar operaciones y soportar operaciones
   reversibles con "Deshacer" (Undo/Redo).
"""

import sys
from abc import ABC, abstractmethod

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. PATRÓN STRATEGY (Cálculo de Rutas de Navegación)
# ==============================================================================
class EstrategiaRuta(ABC):
    @abstractmethod
    def calcular_tiempo(self, distancia_km: float) -> str:
        pass


class RutaEnAuto(EstrategiaRuta):
    def calcular_tiempo(self, distancia_km: float) -> str:
        horas = distancia_km / 80.0
        return f"🚗 En Auto (80 km/h prom): {horas * 60:.0f} minutos"


class RutaEnBicicleta(EstrategiaRuta):
    def calcular_tiempo(self, distancia_km: float) -> str:
        horas = distancia_km / 15.0
        return f"🚲 En Bicicleta (15 km/h prom): {horas * 60:.0f} minutos"


class NavegadorGPS:
    def __init__(self, estrategia: EstrategiaRuta):
        self.estrategia = estrategia

    def planificar_viaje(self, distancia_km: float) -> None:
        print(f"🗺️ Calculando ruta de {distancia_km} km...")
        print(f"   Resultado: {self.estrategia.calcular_tiempo(distancia_km)}")


# ==============================================================================
# 2. PATRÓN OBSERVER (Notificación de Eventos / Pub-Sub)
# ==============================================================================
class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento: str, datos: dict) -> None:
        pass


class SujetoObservable:
    """Mantiene la lista de observadores y emite notificaciones."""

    def __init__(self):
        self._observadores: list[Observador] = []

    def suscribir(self, observador: Observador) -> None:
        self._observadores.append(observador)

    def desuscribir(self, observador: Observador) -> None:
        self._observadores.remove(observador)

    def notificar(self, evento: str, datos: dict) -> None:
        for obs in self._observadores:
            obs.actualizar(evento, datos)


# Observadores concretos:
class CanalEmailAlerta(Observador):
    def actualizar(self, evento: str, datos: dict) -> None:
        print(f"📧 [EMAIL]: Evento '{evento}' recibido -> Notificando a usuario sobre {datos}")


class CanalAuditoriaSeguridad(Observador):
    def actualizar(self, evento: str, datos: dict) -> None:
        print(f"🛡️ [AUDITORÍA]: Registro de seguridad persistido para '{evento}' -> {datos}")


# ==============================================================================
# 3. PATRÓN COMMAND (Operaciones con Soporte de Deshacer / Undo)
# ==============================================================================
class Comando(ABC):
    @abstractmethod
    def ejecutar(self) -> None:
        pass

    @abstractmethod
    def deshacer(self) -> None:
        pass


class CuentaBancariaSimple:
    """Receptor (Receiver) de las órdenes de comando."""

    def __init__(self, saldo_inicial: float = 0.0):
        self.saldo = saldo_inicial

    def depositar(self, monto: float) -> None:
        self.saldo += monto
        print(f"   [CUENTA]: Depósito de ${monto:.2f}. Saldo: ${self.saldo:.2f}")

    def retirar(self, monto: float) -> None:
        self.saldo -= monto
        print(f"   [CUENTA]: Retiro de ${monto:.2f}. Saldo: ${self.saldo:.2f}")


class ComandoDeposito(Comando):
    def __init__(self, cuenta: CuentaBancariaSimple, monto: float):
        self.cuenta = cuenta
        self.monto = monto

    def ejecutar(self) -> None:
        self.cuenta.depositar(self.monto)

    def deshacer(self) -> None:
        print(f"↩️ Deshaciendo depósito de ${self.monto:.2f}...")
        self.cuenta.retirar(self.monto)


class GestorHistorialComandos:
    """Invocador (Invoker) que administra el historial y el 'Ctrl+Z'."""

    def __init__(self):
        self._historial: list[Comando] = []

    def ejecutar_comando(self, comando: Comando) -> None:
        comando.ejecutar()
        self._historial.append(comando)

    def deshacer_ultimo(self) -> None:
        if not self._historial:
            print("⚠️ No hay comandos para deshacer.")
            return
        ultimo = self._historial.pop()
        ultimo.deshacer()


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 03 - Patrones de Comportamiento (Strategy, Observer, Command)")
    print("=" * 65)

    # 1. Strategy
    print("\n--- 1. Patrón Strategy ---")
    gps = NavegadorGPS(RutaEnAuto())
    gps.planificar_viaje(45.0)

    # Cambiamos la estrategia en caliente
    gps.estrategia = RutaEnBicicleta()
    gps.planificar_viaje(45.0)

    # 2. Observer
    print("\n--- 2. Patrón Observer ---")
    sistema_pagos = SujetoObservable()
    canal_mail = CanalEmailAlerta()
    canal_seg = CanalAuditoriaSeguridad()

    sistema_pagos.suscribir(canal_mail)
    sistema_pagos.suscribir(canal_seg)

    print("Disparando evento de pago:")
    sistema_pagos.notificar("PAGO_REALIZADO", {"orden_id": "ORD-5541", "monto": 99.90})

    # 3. Command
    print("\n--- 3. Patrón Command con Operación Deshacer (Undo) ---")
    cuenta = CuentaBancariaSimple(saldo_inicial=100.0)
    gestor = GestorHistorialComandos()

    print(f"Saldo inicial: ${cuenta.saldo:.2f}")
    gestor.ejecutar_comando(ComandoDeposito(cuenta, 50.0))
    gestor.ejecutar_comando(ComandoDeposito(cuenta, 200.0))

    print(f"Saldo tras depósitos: ${cuenta.saldo:.2f}")

    # Ejecutamos Ctrl+Z (Undo)
    gestor.deshacer_ultimo()
    print(f"Saldo tras primer undo: ${cuenta.saldo:.2f}")
    gestor.deshacer_ultimo()
    print(f"Saldo tras segundo undo: ${cuenta.saldo:.2f}")
