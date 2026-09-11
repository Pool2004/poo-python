"""
==============================================================================
Módulo: 05_solid / 05_dependency_inversion.py
Tema: Principio de Inversión de Dependencias (DIP - Dependency Inversion Principle).
==============================================================================

Definición:
-----------
1. Los módulos de alto nivel (la lógica central del negocio) no deben depender
   de módulos de bajo nivel (detalles como bases de datos, APIs de terceros, discos).
   Ambos deben depender de **Abstracciones**.
2. Las abstracciones no deben depender de los detalles. Los detalles deben depender
   de las abstracciones.

¿Qué problema resuelve?
-----------------------
El acoplamiento rígido ("Hardcoding"). Si tu clase de negocio `GestorPedidos`
instancia directamente `MySQLDatabase()` y `TwilioSMS()`:
- No puedes probar `GestorPedidos` con tests unitarios sin levantar una BD real.
- Si la empresa cambia de MySQL a MongoDB, tienes que reescribir la lógica de negocio.
- Si Twilio sube de precio y migras a AWS SNS, rompes la lógica de negocio.

La Solución: Inyección de Dependencias (Dependency Injection)
-------------------------------------------------------------
En lugar de que la clase construya sus dependencias por dentro, se le inyectan
desde afuera (usualmente por el constructor `__init__`) apuntando siempre a interfaces abstractas.
"""

import sys
from abc import ABC, abstractmethod

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. ABSTRACCIONES (CONTRATOS INDEPENDIENTES)
# ==============================================================================
class RepositorioPedidos(ABC):
    """Abstracción para cualquier mecanismo de persistencia de pedidos."""

    @abstractmethod
    def guardar(self, id_pedido: str, datos: dict) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id_pedido: str) -> dict | None:
        pass


class ServicioMensajeria(ABC):
    """Abstracción para cualquier canal de envío de notificaciones."""

    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str) -> None:
        pass


# ==============================================================================
# 2. MÓDULO DE ALTO NIVEL (LÓGICA PURA DE NEGOCIO)
# ==============================================================================
class GestorPedidos:
    """Módulo de Alto Nivel: Depende ÚNICAMENTE de abstracciones inyectadas."""

    def __init__(self, repositorio: RepositorioPedidos, mensajeria: ServicioMensajeria):
        # Inyección de dependencias
        self.repositorio = repositorio
        self.mensajeria = mensajeria

    def crear_pedido(self, id_pedido: str, cliente: str, total: float, contacto: str) -> None:
        datos_pedido = {"cliente": cliente, "total": total, "estado": "CONFIRMADO"}

        # 1. Guardar usando la abstracción
        self.repositorio.guardar(id_pedido, datos_pedido)

        # 2. Notificar usando la abstracción
        mensaje = f"Hola {cliente}, tu pedido #{id_pedido} por ${total:,.2f} ha sido confirmado."
        self.mensajeria.enviar(contacto, mensaje)


# ==============================================================================
# 3. DETALLES DE BAJO NIVEL (IMPLEMENTACIONES CONCRETAS)
# ==============================================================================
# Detalle 1: Persistencia en PostgreSQL
class RepositorioPostgreSQL(RepositorioPedidos):
    def guardar(self, id_pedido: str, datos: dict) -> None:
        print(f"🐘 [PostgreSQL]: INSERT INTO pedidos (id, datos) VALUES ('{id_pedido}', '{datos}')")

    def buscar_por_id(self, id_pedido: str) -> dict | None:
        return {"id": id_pedido}


# Detalle 2: Persistencia en Memoria (¡Ideal para Tests Unitarios ultrarrápidos!)
class RepositorioEnMemoria(RepositorioPedidos):
    def __init__(self):
        self._almacen = {}

    def guardar(self, id_pedido: str, datos: dict) -> None:
        self._almacen[id_pedido] = datos
        print(f"🧠 [RAM MOCK]: Pedido #{id_pedido} guardado en diccionario de memoria.")

    def buscar_por_id(self, id_pedido: str) -> dict | None:
        return self._almacen.get(id_pedido)


# Detalle 3: Mensajería vía SMS
class ServicioTwilioSMS(ServicioMensajeria):
    def enviar(self, destinatario: str, mensaje: str) -> None:
        print(f"📱 [Twilio SMS -> {destinatario}]: '{mensaje}'")


# Detalle 4: Mensajería silenciosa o de consola
class ServicioMensajeriaConsola(ServicioMensajeria):
    def enviar(self, destinatario: str, mensaje: str) -> None:
        print(f"🖥️ [LOG LOCAL]: Mensaje simulado para {destinatario}: {mensaje}")


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 05 - Principio de Inversión de Dependencias (DIP)")
    print("=" * 65)

    # Escenario A: Entorno de Producción (Base de datos real y SMS de pago)
    print("\n--- 1. Configuración de Producción ---")
    gestor_prod = GestorPedidos(
        repositorio=RepositorioPostgreSQL(),
        mensajeria=ServicioTwilioSMS()
    )
    gestor_prod.crear_pedido("PED-001", "Ana Gómez", 280.50, "+573001234567")

    # Escenario B: Entorno de Pruebas Automatizadas (Zero dependencias externas)
    print("\n--- 2. Configuración de Pruebas Unitarias (Tests Rápidos y Aislados) ---")
    repo_test = RepositorioEnMemoria()
    gestor_test = GestorPedidos(
        repositorio=repo_test,
        mensajeria=ServicioMensajeriaConsola()
    )
    gestor_test.crear_pedido("PED-TEST-99", "Tester Automatizado", 10.0, "test@qa.local")
    print(f"Verificación de estado en mock: {repo_test.buscar_por_id('PED-TEST-99')}")
