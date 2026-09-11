"""
==============================================================================
Módulo: 04_avanzado / 01_dataclasses.py
Tema: Dataclasses Modernas en Python: @dataclass, frozen, field y __post_init__.
==============================================================================

¿Qué son las Dataclasses?
-------------------------
Introducidas en Python 3.7 (módulo estándar `dataclasses`), son clases diseñadas
primordialmente para almacenar datos y estado.
Eliminan cientos de líneas de código repetitivo ("boilerplate"):
- Generan automáticamente `__init__`, `__repr__`, `__eq__`.
- Opcionalmente generan métodos de comparación (`order=True`).
- Soportan inmutabilidad (`frozen=True`).

Características Avanzadas:
--------------------------
1. `field(default_factory=list)`:
   Solución definitiva y limpia para evitar la trampa de colecciones mutables por defecto.
2. `__post_init__(self)`:
   Método especial que se invoca inmediatamente después de `__init__` para
   realizar validaciones o calcular campos derivados.
3. `frozen=True`:
   Convierte la instancia en inmutable (read-only) y le otorga automáticamente
   un método `__hash__`, haciéndola apta para sets y diccionarios.
4. `kw_only=True` (Python 3.10+):
   Obliga a que los parámetros deban pasarse por nombre y no por posición.
"""

import sys
from dataclasses import dataclass, field


# ==============================================================================
# 1. DATACLASS BÁSICA Y VALIDACIÓN CON __post_init__
# ==============================================================================
@dataclass(order=True)
class Tarea:
    """Modela una tarea priorizada con ordenamiento automático."""

    # El campo prioridad se usará para ordenar (order=True usa el orden de definición de campos)
    prioridad: int
    titulo: str = field(compare=False)
    etiquetas: list[str] = field(default_factory=list, compare=False)
    completada: bool = field(default=False, compare=False)

    def __post_init__(self):
        """Se ejecuta tras el __init__ generado automáticamente."""
        if not self.titulo.strip():
            raise ValueError("El título de la tarea no puede estar vacío.")
        if self.prioridad < 1:
            raise ValueError("La prioridad debe ser un entero >= 1.")


# ==============================================================================
# 2. DATACLASS INMUTABLE (FROZEN) CON VALORES CALCULADOS
# ==============================================================================
@dataclass(frozen=True, kw_only=True)
class CoordenadaGPS:
    """Coordenada inmutable. No se puede modificar tras crearse y es hashable."""

    latitud: float
    longitud: float
    descripcion: str = "Punto geográfico"

    def __post_init__(self):
        # En una dataclass frozen, self.attr = x está bloqueado.
        # Para validar o inicializar usamos object.__setattr__ si hiciera falta,
        # o simplemente validamos:
        if not (-90 <= self.latitud <= 90):
            raise ValueError(f"Latitud inválida: {self.latitud}")
        if not (-180 <= self.longitud <= 180):
            raise ValueError(f"Longitud inválida: {self.longitud}")


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 01 - Dataclasses Modernas en Python")
    print("=" * 65)

    # 1. Creación e inspección de __repr__ automático
    print("\n--- 1. Generación automática de __repr__ y __init__ ---")
    t1 = Tarea(prioridad=2, titulo="Escribir documentación", etiquetas=["docs", "poo"])
    t2 = Tarea(prioridad=1, titulo="Corregir bug crítico en servidor", etiquetas=["urgente"])
    t3 = Tarea(prioridad=3, titulo="Revisar pull requests pendientes")

    print(f"Tarea 1 creada: {t1}")
    print(f"Tarea 2 creada: {t2}")

    # 2. Ordenamiento automático por prioridad (order=True)
    print("\n--- 2. Ordenamiento automático con order=True ---")
    lista_tareas = [t1, t2, t3]
    print(f"Lista sin ordenar: {[t.titulo for t in lista_tareas]}")
    lista_tareas.sort()
    print(f"Lista ordenada (prioridad 1 a 3):")
    for t in lista_tareas:
        print(f"  [Prioridad {t.prioridad}] {t.titulo}")

    # 3. Inmutabilidad con frozen=True
    print("\n--- 3. Inmutabilidad y Hashabilidad con frozen=True ---")
    bogota = CoordenadaGPS(latitud=4.7110, longitud=-74.0721, descripcion="Bogotá D.C.")
    print(f"Ubicación: {bogota}")

    try:
        # Intentar modificar un campo de una frozen dataclass
        bogota.latitud = 10.0  # type: ignore
    except Exception as err:
        print(f"🛡️ Bloqueado por frozen=True: {type(err).__name__} -> {err}")

    # Al ser inmutable, tiene __hash__ y puede ser llave de diccionario o miembro de set:
    sitios_interes = {bogota: "Capital de Colombia"}
    print(f"Ubicación en diccionario: {sitios_interes[bogota]}")
