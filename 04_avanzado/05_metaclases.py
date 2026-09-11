"""
==============================================================================
Módulo: 04_avanzado / 05_metaclases.py
Tema: Metaclases en Python: La Fábrica de Clases (type y __new__).
==============================================================================

¿Qué es una Metaclase?
----------------------
En Python: "Las clases también son objetos".
- Un objeto ordinario es una instancia de una **Clase**.
- Una clase es una instancia de una **Metaclase**.

Por defecto, la metaclase de todas las clases en Python es `type`:
- `type(10)` -> `int`
- `type(int)` -> `type`
- `type(type)` -> `type` (raíz del sistema de tipos)

¿Para qué sirve crear una Metaclase personalizada?
--------------------------------------------------
Permite interceptar la creación y configuración de una clase en el momento exacto
en que el archivo es parseado o importado por Python (tiempo de definición de clase),
mucho antes de que se cree cualquier instancia.

Casos de Uso Reales:
-------------------
1. Registro automático de plugins o controladores (como en frameworks web o CLI tools).
2. Forzar estándares de nomenclatura corporativos (ej. validar que todos los métodos
   de una API comiencen con `api_`).
3. Validación de esquemas y ORM (como hace Django en `models.Model` o Pydantic).
"""

import sys

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. CREACIÓN DINÁMICA DE CLASES CON 'type'
# ==============================================================================
# Normalmente escribes:
# class Gato:
#     def maullar(self): return "Miau!"
#
# Pero con 'type' puedes crear la misma clase en tiempo de ejecución:
def _maullar(self):
    return "¡Miau dinámico!"


ClaseGatoDinamica = type(
    "GatoDinamico",           # Nombre de la clase
    (object,),                # Tupla de clases base
    {"maullar": _maullar}     # Diccionario de atributos y métodos
)


# ==============================================================================
# 2. METACLASE PERSONALIZADA: REGISTRO AUTOMÁTICO DE PLUGINS
# ==============================================================================
REGISTRO_GLOBAL_PLUGINS: dict[str, type] = {}


class RegistroPluginMeta(type):
    """Metaclase que registra automáticamente cualquier subclase creada en un catálogo global."""

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        # 1. Creamos la clase llamando al constructor base de type
        cls = super().__new__(mcs, name, bases, namespace)

        # 2. Evitamos registrar la clase base abstracta "PluginBase"
        if name != "PluginBase":
            nombre_comando = namespace.get("comando", name.lower())
            print(f"⚙️ [METACLASE]: Detectada nueva clase '{name}'. Registrando comando -> '{nombre_comando}'")
            REGISTRO_GLOBAL_PLUGINS[nombre_comando] = cls

        return cls


class PluginBase(metaclass=RegistroPluginMeta):
    """Clase base para todos los plugins del sistema."""

    comando: str = ""

    def ejecutar(self) -> str:
        raise NotImplementedError


# ==============================================================================
# PLUGINS DECLARADOS (¡Se registran solos en tiempo de importación!)
# ==============================================================================
class PluginCompresor(PluginBase):
    comando = "comprimir"

    def ejecutar(self) -> str:
        return "📦 Comprimiendo archivos en formato ZIP..."


class PluginEncriptador(PluginBase):
    comando = "encriptar"

    def ejecutar(self) -> str:
        return "🔐 Encriptando datos con algoritmo AES-256..."


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 05 - Metaclases y Creación Dinámica")
    print("=" * 65)

    # 1. Demostración de clase creada dinámicamente con type()
    print("\n--- 1. Creación dinámica de clases con type() ---")
    gato = ClaseGatoDinamica()
    print(f"Tipo de la instancia:  {type(gato)}")
    print(f"Tipo de la clase Gato: {type(ClaseGatoDinamica)}")
    print(f"Acción del gato:       {gato.maullar()}")

    # 2. Demostración del registro automático por metaclase
    print("\n--- 2. Registro Automático de Plugins Vía Metaclase ---")
    print(f"Total de plugins registrados automáticamente: {len(REGISTRO_GLOBAL_PLUGINS)}")
    for comando, clase_plugin in REGISTRO_GLOBAL_PLUGINS.items():
        print(f"  Comando registrado: '{comando}' -> Clase: {clase_plugin.__name__}")

    # 3. Ejecución dinámica de un comando solicitado por un usuario
    print("\n--- 3. Despacho dinámico de comandos ---")
    solicitud = "encriptar"
    if solicitud in REGISTRO_GLOBAL_PLUGINS:
        instancia_plugin = REGISTRO_GLOBAL_PLUGINS[solicitud]()
        print(f"Ejecutando [{solicitud}]: {instancia_plugin.ejecutar()}")
