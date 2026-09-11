"""
==============================================================================
Módulo: 06_patrones_diseno / 02_estructurales.py
Tema: Patrones Estructurales: Adapter, Decorator (POO GoF) y Facade.
==============================================================================

Los Patrones Estructurales:
---------------------------
Se enfocan en cómo se componen y organizan las clases y objetos para formar
estructuras más grandes, manteniendo la flexibilidad y la eficiencia.

1. Adapter (Adaptador):
   Permite que dos clases con interfaces incompatibles puedan trabajar juntas.
   Actúa como un "conversor de enchufe eléctrico", traduciendo llamadas de la
   interfaz cliente a la interfaz del objeto adaptado.

2. Decorator (Decorador de Objetos - GoF):
   Permite añadir responsabilidades o comportamientos adicionales a un objeto
   individual de manera dinámica y acumulativa, envolviéndolo en sucesivas capas
   sin necesidad de crear infinitas subclases.

3. Facade (Fachada):
   Proporciona una interfaz simplificada de alto nivel para interactuar con un
   subsistema complejo compuesto por múltiples clases y pasos intrincados.
"""

import sys
from abc import ABC, abstractmethod

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. PATRÓN ADAPTER (Adaptador)
# ==============================================================================
# Interfaz esperada por nuestra aplicación moderna:
class MotorAnaliticaModerna(ABC):
    @abstractmethod
    def rastrear_evento(self, evento: str, metadata: dict) -> None:
        pass


# Librería externa o código heredado (Legacy) incompatible:
class ServicioAnaliticaXMLTerceros:
    """Librería antigua que sólo acepta cadenas de texto formateadas en XML."""

    def enviar_payload_xml(self, xml_data: str) -> None:
        print(f"📡 [API XML LEGACY]: Transmitiendo -> {xml_data}")


# Adaptador que une ambos mundos:
class AdaptadorAnaliticaXML(MotorAnaliticaModerna):
    def __init__(self, servicio_legado: ServicioAnaliticaXMLTerceros):
        self.servicio_legado = servicio_legado

    def rastrear_evento(self, evento: str, metadata: dict) -> None:
        # Convertimos la llamada moderna de Python (dict) al formato antiguo XML
        xml_tags = "".join(f"<{k}>{v}</{k}>" for k, v in metadata.items())
        xml_string = f"<evento nombre='{evento}'>{xml_tags}</evento>"
        self.servicio_legado.enviar_payload_xml(xml_string)


# ==============================================================================
# 2. PATRÓN DECORATOR (GoF - Envoltura Dinámica)
# ==============================================================================
class Bebida(ABC):
    """Componente base abstracto."""

    @abstractmethod
    def costo(self) -> float:
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass


class CafeEspresso(Bebida):
    """Componente concreto."""

    def costo(self) -> float:
        return 2.50

    def descripcion(self) -> str:
        return "Café Espresso"


class AgregadoDecorator(Bebida):
    """Decorador base abstracto: Envuelve otra Bebida."""

    def __init__(self, bebida: Bebida):
        self._bebida = bebida

    def costo(self) -> float:
        return self._bebida.costo()

    def descripcion(self) -> str:
        return self._bebida.descripcion()


class ConLeche(AgregadoDecorator):
    def costo(self) -> float:
        return self._bebida.costo() + 0.75

    def descripcion(self) -> str:
        return f"{self._bebida.descripcion()} + Leche Vaporizada"


class ConCaramelo(AgregadoDecorator):
    def costo(self) -> float:
        return self._bebida.costo() + 0.50

    def descripcion(self) -> str:
        return f"{self._bebida.descripcion()} + Jarabe de Caramelo"


# ==============================================================================
# 3. PATRÓN FACADE (Fachada)
# ==============================================================================
# Subsistemas complejos:
class LucesAmbiente:
    def atenuar(self, nivel: int) -> None:
        print(f"💡 Luces atenuadas al {nivel}%.")


class Proyector4K:
    def encender(self) -> None:
        print("📽️ Proyector 4K láser encendido.")

    def modo_cine(self) -> None:
        print("📽️ Proyector configurado en formato 21:9 HDR.")


class SistemaSonidoSurround:
    def encender(self) -> None:
        print("🔊 Sistema Dolby Atmos 7.1 activado.")

    def volumen(self, nivel: int) -> None:
        print(f"🔊 Volumen establecido en nivel {nivel}.")


class ReproductorPeliculas:
    def reproducir(self, pelicula: str) -> None:
        print(f"🍿 Reproduciendo '{pelicula}' en resolución original.")


# Fachada de Alto Nivel:
class CineEnCasaFacade:
    """Oculta la complejidad de encender y calibrar 4 subsistemas distintos."""

    def __init__(self):
        self.luces = LucesAmbiente()
        self.proyector = Proyector4K()
        self.sonido = SistemaSonidoSurround()
        self.reproductor = ReproductorPeliculas()

    def iniciar_pelicula(self, titulo: str) -> None:
        print(f"\n🎬 [FACHADA CINE]: Preparando experiencia cinematográfica para '{titulo}'...")
        self.luces.atenuar(10)
        self.proyector.encender()
        self.proyector.modo_cine()
        self.sonido.encender()
        self.sonido.volumen(40)
        self.reproductor.reproducir(titulo)


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 02 - Patrones Estructurales (Adapter, Decorator, Facade)")
    print("=" * 65)

    # 1. Adapter
    print("\n--- 1. Patrón Adapter ---")
    servicio_legacy = ServicioAnaliticaXMLTerceros()
    adaptador: MotorAnaliticaModerna = AdaptadorAnaliticaXML(servicio_legacy)
    adaptador.rastrear_evento("CLICK_BOTON_COMPRA", {"usuario_id": "99", "item": "Auriculares"})

    # 2. Decorator
    print("\n--- 2. Patrón Decorator (Envoltorios dinámicos en capas) ---")
    mi_cafe = CafeEspresso()
    print(f"Base:      {mi_cafe.descripcion()} -> ${mi_cafe.costo():.2f}")

    # Decoramos agregando Leche
    mi_cafe = ConLeche(mi_cafe)
    print(f"Capa 1:    {mi_cafe.descripcion()} -> ${mi_cafe.costo():.2f}")

    # Decoramos agregando Caramelo
    mi_cafe = ConCaramelo(mi_cafe)
    print(f"Capa 2:    {mi_cafe.descripcion()} -> ${mi_cafe.costo():.2f}")

    # 3. Facade
    print("\n--- 3. Patrón Facade ---")
    cine_casa = CineEnCasaFacade()
    cine_casa.iniciar_pelicula("Interstellar (2014)")
