"""
==============================================================================
Módulo: 01_fundamentos / 01_clases_y_objetos.py
Tema: Clases, Instancias, la convención `self` y Atributos de Instancia.
==============================================================================

¿Qué es la Programación Orientada a Objetos (POO)?
-------------------------------------------------
Es un paradigma de programación que organiza el diseño del software alrededor
de "objetos", en lugar de funciones o lógica secuencial. Un objeto representa
una entidad del mundo real o conceptual que agrupa:
1. Estado (datos / atributos).
2. Comportamiento (acciones / métodos).

Conceptos Clave de este Módulo:
-------------------------------
1. Clase:
   Es el "molde", plantilla o plano arquitectónico a partir del cual se crean
   los objetos. Define qué propiedades y métodos tendrán los objetos creados con ella.

2. Objeto (o Instancia):
   Es la materialización concreta de una clase en memoria. Si la clase es `Auto`,
   tu Toyota Corolla rojo estacionado afuera es un objeto/instancia.

3. La palabra clave `self`:
   En Python, `self` no es una palabra reservada del lenguaje, sino una fuerte
   convención de diseño. Hace referencia explícita a la instancia actual del objeto
   sobre la cual se está ejecutando el método. Permite acceder a los atributos y
   métodos de ese objeto específico.

4. El método `__init__`:
   Es el constructor o método de inicialización. Se ejecuta automáticamente cada
   vez que creamos una nueva instancia de la clase.
"""


class Celular:
    """Representa un dispositivo móvil inteligente."""

    def __init__(self, marca: str, modelo: str, bateria: int = 100):
        """Constructor de la clase. Inicializa los atributos de la instancia.

        Args:
            marca (str): Marca del fabricante (ej. Apple, Samsung).
            modelo (str): Modelo específico (ej. iPhone 15, Galaxy S24).
            bateria (int): Nivel inicial de batería en porcentaje (0-100).
        """
        # Atributos de instancia: pertenecen a CADA objeto individual
        self.marca = marca
        self.modelo = modelo
        self.bateria = max(0, min(100, bateria))  # Asegura rango 0-100
        self.encendido = False

    def encender(self) -> str:
        """Enciende el teléfono si tiene batería suficiente."""
        if self.bateria <= 0:
            return f"❌ [{self.marca} {self.modelo}] No tiene batería suficiente para encender."

        if self.encendido:
            return f"ℹ️ [{self.marca} {self.modelo}] Ya se encuentra encendido."

        self.encendido = True
        return f"✅ [{self.marca} {self.modelo}] Se ha encendido correctamente."

    def apagar(self) -> str:
        """Apaga el teléfono."""
        if not self.encendido:
            return f"ℹ️ [{self.marca} {self.modelo}] Ya está apagado."

        self.encendido = False
        return f"🔌 [{self.marca} {self.modelo}] Se ha apagado."

    def usar_app(self, nombre_app: str, consumo_bateria: int) -> str:
        """Simula el uso de una aplicación consumiendo batería."""
        if not self.encendido:
            return f"⚠️ No puedes usar '{nombre_app}'. El dispositivo está apagado."

        if self.bateria < consumo_bateria:
            self.bateria = 0
            self.encendido = False
            return f"🪫 [{self.marca} {self.modelo}] Se agotó la batería usando '{nombre_app}'. Teléfono apagado."

        self.bateria -= consumo_bateria
        return (
            f"📱 Usando '{nombre_app}'. Consumo: {consumo_bateria}%. "
            f"Batería restante: {self.bateria}%"
        )

    def cargar(self, cantidad: int) -> str:
        """Recarga la batería del dispositivo."""
        if cantidad <= 0:
            return "⚠️ La cantidad a cargar debe ser un número positivo."

        self.bateria = min(100, self.bateria + cantidad)
        return f"⚡ Batería cargada al {self.bateria}% en [{self.marca} {self.modelo}]."

    def obtener_info(self) -> str:
        """Retorna el estado general del celular."""
        estado = "Encendido" if self.encendido else "Apagado"
        return (
            f"┌{'─' * 38}┐\n"
            f"│ Dispositivo: {self.marca} {self.modelo:<21} │\n"
            f"│ Batería:     {self.bateria:>3}% {'🔋' if self.bateria > 20 else '🪫'}                  │\n"
            f"│ Estado:      {estado:<26} │\n"
            f"└{'─' * 38}┘"
        )


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 60)
    print("DEMOSTRACIÓN: 01 - Clases, Objetos y 'self'")
    print("=" * 60)

    # 1. Creación de Instancias (Instanciación)
    print("\n--- 1. Instanciando objetos ---")
    telefono_juan = Celular("Samsung", "Galaxy S24", bateria=80)
    telefono_maria = Celular("Apple", "iPhone 15 Pro", bateria=50)

    # Cada objeto es independiente y ocupa su propio espacio en memoria
    print(f"Objeto Juan:  {telefono_juan} (ID en memoria: {hex(id(telefono_juan))})")
    print(f"Objeto María: {telefono_maria} (ID en memoria: {hex(id(telefono_maria))})")

    # 2. Acceso a atributos y llamadas a métodos
    print("\n--- 2. Estado inicial e Interacción ---")
    print(telefono_juan.obtener_info())

    print("\nAcciones con el teléfono de Juan:")
    print(telefono_juan.encender())
    print(telefono_juan.usar_app("YouTube", 25))
    print(telefono_juan.usar_app("Juego 3D", 40))
    print(telefono_juan.obtener_info())

    print("\nAcciones con el teléfono de María:")
    print(telefono_maria.usar_app("WhatsApp", 10))  # Aún está apagado
    print(telefono_maria.encender())
    print(telefono_maria.usar_app("Instagram", 30))
    print(telefono_maria.cargar(40))
    print(telefono_maria.obtener_info())

    # 3. Demostración de cómo Python traduce self tras bambalinas:
    print("\n--- 3. ¿Cómo funciona 'self' internamente? ---")
    # Estas dos llamadas son EXACTAMENTE equivalentes en Python:
    resultado_metodo = telefono_juan.encender()
    resultado_clase = Celular.encender(telefono_juan)
    print(f"Llamada normal:  telefono_juan.encender() -> {resultado_metodo}")
    print(f"Llamada directa: Celular.encender(telefono_juan) -> {resultado_clase}")
