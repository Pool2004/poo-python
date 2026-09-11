"""
==============================================================================
Módulo: 01_fundamentos / 04_ciclo_de_vida.py
Tema: Ciclo de Vida del Objeto: __new__, __init__ y __del__.
==============================================================================

El Ciclo de Vida en Python:
---------------------------
Cuando escribes `obj = MiClase("argumento")`, internamente ocurren varias fases:

1. FASE DE ASIGNACIÓN / CREACIÓN: `__new__(cls, *args, **kwargs)`
   - Es el VERDADERO constructor de bajo nivel.
   - Es un método estático implícito que toma la clase `cls` y devuelve una
     NUEVA instancia en memoria (usualmente llamando a `super().__new__(cls)`).
   - Raramente se sobreescribe, excepto al crear tipos inmutables (subclases de int/str/tuple)
     o en patrones como el Singleton.

2. FASE DE INICIALIZACIÓN: `__init__(self, *args, **kwargs)`
   - Es el inicializador. Recibe la instancia ya creada en `__new__` como `self`.
   - Establece los atributos iniciales del objeto.
   - NO devuelve ningún valor (debe retornar `None`).

3. FASE DE USO:
   - El objeto vive en memoria mientras tenga al menos una referencia activa
     (Conteo de Referencias de CPython).

4. FASE DE DESTRUCCIÓN / RECOLECCIÓN: `__del__(self)`
   - Es el destructor (finalizador).
   - Se ejecuta cuando el contador de referencias llega a 0 y el Garbage Collector
     reclama la memoria.
   - ⚠️ ADVERTENCIA: No se debe usar `__del__` para liberar recursos críticos (como
     cerrar archivos o conexiones a BD), porque el momento de ejecución no está
     garantizado. Para eso se utilizan Gestores de Contexto (`with`).
"""

import sys


class DemostracionCicloVida:
    """Clase para inspeccionar cada paso del ciclo de vida de un objeto."""

    def __new__(cls, *args, **kwargs):
        print(f"1. [__new__] Reservando memoria para una nueva instancia de {cls.__name__}...")
        instancia = super().__new__(cls)
        return instancia

    def __init__(self, nombre: str):
        print(f"2. [__init__] Inicializando el estado de la instancia con nombre='{nombre}'...")
        self.nombre = nombre

    def __del__(self):
        # NOTA: En la salida estándar durante la terminación del programa esto puede
        # ejecutarse en cualquier momento.
        print(f"3. [__del__] Objeto '{self.nombre}' destruido de la memoria (Garbage Collection).")


class ConexionSegura:
    """Demostración de por qué los Gestores de Contexto son superiores a __del__."""

    def __init__(self, servicio: str):
        self.servicio = servicio
        self.conectado = False

    def conectar(self):
        self.conectado = True
        print(f"🔌 Conectado a {self.servicio}")

    def desconectar(self):
        self.conectado = False
        print(f"🛑 Desconectado de {self.servicio}")

    # Soporte para la sentencia 'with' (Gestor de contexto)
    def __enter__(self):
        self.conectar()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.desconectar()


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 04 - Ciclo de Vida: __new__, __init__ y __del__")
    print("=" * 65)

    print("\n--- 1. Creación e Inicialización ---")
    obj = DemostracionCicloVida("Instancia Alfa")
    print(f"Objeto creado exitosamente: {obj.nombre}")

    print("\n--- 2. Conteo de Referencias y Destrucción explícita ---")
    # sys.getrefcount retorna el número de referencias + 1 (la llamada de getrefcount cuenta como 1)
    print(f"Referencias iniciales hacia obj: {sys.getrefcount(obj) - 1}")

    copia_referencia = obj
    print(f"Tras asignar copia_referencia: {sys.getrefcount(obj) - 1} referencias")

    del copia_referencia
    print(f"Tras 'del copia_referencia': {sys.getrefcount(obj) - 1} referencias")

    print("\nEliminando la última referencia hacia obj...")
    del obj  # Aquí el contador llega a 0 y se dispara __del__ de inmediato

    print("\n--- 3. La forma profesional de gestionar recursos: 'with' ---")
    with ConexionSegura("BaseDeDatos_Produccion") as db:
        print(f"Trabajando de forma segura con {db.servicio}...")
    # Al salir del bloque 'with', la desconexión es INMEDIATA y 100% garantizada
