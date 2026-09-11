"""
==============================================================================
Módulo: 06_patrones_diseno / 01_creacionales.py
Tema: Patrones de Diseño Creacionales: Singleton, Factory Method y Builder.
==============================================================================

Los Patrones Creacionales:
--------------------------
Abstraen el proceso de instanciación y creación de objetos. Hacen que un sistema
sea independiente de cómo se crean, componen y representan sus objetos.

1. Singleton:
   Garantiza que una clase tenga una ÚNICA instancia global y proporciona un
   punto de acceso central a ella (ej. Configuración global, Pool de conexiones).
   En Python, implementarlo mediante una Metaclase es la forma más elegante y reutilizable.

2. Factory Method (Método de Fábrica):
   Define una interfaz para crear un objeto, pero delega en una fábrica o subclase
   la decisión de qué clase concreta instanciar. Evita acoplar el código cliente
   a clases concretas.

3. Builder (Constructor):
   Separa la construcción de un objeto complejo de su representación final,
   permitiendo que el mismo proceso de construcción pueda crear diferentes representaciones
   paso a paso de forma legible y fluida (Fluent Interface).
"""

import sys
from abc import ABC, abstractmethod

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. PATRÓN SINGLETON (Vía Metaclase Reutilizable)
# ==============================================================================
class SingletonMeta(type):
    """Metaclase que asegura una única instancia por clase en memoria."""
    _instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            # Si no existe, crea la instancia y la guarda en la caché
            instancia = super().__call__(*args, **kwargs)
            cls._instancias[cls] = instancia
        return cls._instancias[cls]


class ConfiguracionSistema(metaclass=SingletonMeta):
    """Gestor de configuración global único en toda la aplicación."""

    def __init__(self):
        self.ambiente = "PRODUCCION"
        self.version = "1.0.0"
        self.parametros = {"max_conexiones": 50, "timeout": 30}


# ==============================================================================
# 2. PATRÓN FACTORY METHOD
# ==============================================================================
class Notificacion(ABC):
    @abstractmethod
    def enviar(self, mensaje: str) -> str:
        pass


class NotificacionEmail(Notificacion):
    def enviar(self, mensaje: str) -> str:
        return f"📧 [EMAIL]: {mensaje}"


class NotificacionSMS(Notificacion):
    def enviar(self, mensaje: str) -> str:
        return f"📱 [SMS]: {mensaje}"


class NotificacionPush(Notificacion):
    def enviar(self, mensaje: str) -> str:
        return f"🔔 [PUSH NOTIF]: {mensaje}"


class FabricaNotificaciones:
    """Fábrica que centraliza la creación de notificaciones según el canal."""

    @staticmethod
    def crear_notificador(canal: str) -> Notificacion:
        canales = {
            "email": NotificacionEmail,
            "sms": NotificacionSMS,
            "push": NotificacionPush
        }
        clase = canales.get(canal.lower())
        if not clase:
            raise ValueError(f"Canal no soportado: '{canal}'. Válidos: {list(canales.keys())}")
        return clase()


# ==============================================================================
# 3. PATRÓN BUILDER (CONSTRUCTOR FLUÍDO)
# ==============================================================================
class Computadora:
    """Producto complejo ensamblado por el Builder."""

    def __init__(self):
        self.procesador: str = ""
        self.ram_gb: int = 0
        self.disco_gb: int = 0
        self.tarjeta_grafica: str | None = None
        self.refrigeracion_liquida: bool = False

    def __str__(self) -> str:
        detalles = [
            f"CPU: {self.procesador}",
            f"RAM: {self.ram_gb} GB",
            f"Almacenamiento: {self.disco_gb} GB SSD",
            f"GPU: {self.tarjeta_grafica or 'Integrada'}",
            f"Refrig. Líquida: {'Sí' if self.refrigeracion_liquida else 'No'}"
        ]
        return " | ".join(detalles)


class ComputadoraBuilder:
    """Constructor paso a paso con Fluent Interface (retorna self)."""

    def __init__(self):
        self._pc = Computadora()

    def con_procesador(self, cpu: str) -> "ComputadoraBuilder":
        self._pc.procesador = cpu
        return self

    def con_ram(self, ram_gb: int) -> "ComputadoraBuilder":
        self._pc.ram_gb = ram_gb
        return self

    def con_almacenamiento(self, disco_gb: int) -> "ComputadoraBuilder":
        self._pc.disco_gb = disco_gb
        return self

    def con_tarjeta_grafica(self, gpu: str) -> "ComputadoraBuilder":
        self._pc.tarjeta_grafica = gpu
        return self

    def con_refrigeracion_liquida(self, activar: bool = True) -> "ComputadoraBuilder":
        self._pc.refrigeracion_liquida = activar
        return self

    def build(self) -> Computadora:
        """Valida y retorna el producto terminado."""
        if not self._pc.procesador or self._pc.ram_gb <= 0:
            raise ValueError("La computadora debe tener al menos CPU y RAM definidos.")
        return self._pc


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 01 - Patrones Creacionales (Singleton, Factory, Builder)")
    print("=" * 65)

    # 1. Prueba de Singleton
    print("\n--- 1. Patrón Singleton ---")
    c1 = ConfiguracionSistema()
    c2 = ConfiguracionSistema()
    print(f"¿c1 y c2 son el MISMO objeto en memoria? {c1 is c2}")
    c1.ambiente = "TESTING"
    print(f"Ambiente en c2 tras cambiar c1: {c2.ambiente} (¡Sincronizado!)")

    # 2. Prueba de Factory Method
    print("\n--- 2. Patrón Factory Method ---")
    for tipo in ["email", "sms", "push"]:
        notificador = FabricaNotificaciones.crear_notificador(tipo)
        print(notificador.enviar("Tu código de verificación es 4982"))

    # 3. Prueba de Builder
    print("\n--- 3. Patrón Builder (Construcción Fluida Paso a Paso) ---")
    pc_gamer = (
        ComputadoraBuilder()
        .con_procesador("AMD Ryzen 9 7950X")
        .con_ram(64)
        .con_almacenamiento(2000)
        .con_tarjeta_grafica("NVIDIA RTX 4090 24GB")
        .con_refrigeracion_liquida(True)
        .build()
    )

    pc_oficina = (
        ComputadoraBuilder()
        .con_procesador("Intel Core i3 12100")
        .con_ram(16)
        .con_almacenamiento(512)
        .build()
    )

    print(f"PC Gamer:   {pc_gamer}")
    print(f"PC Oficina: {pc_oficina}")
