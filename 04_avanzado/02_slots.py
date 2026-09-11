"""
==============================================================================
Módulo: 04_avanzado / 02_slots.py
Tema: Optimización Extrema de Memoria y Velocidad con __slots__.
==============================================================================

¿Cómo gestiona Python los atributos por defecto?
------------------------------------------------
Por diseño dinámico, cada instancia normal en Python posee un diccionario interno
llamado `__dict__`. Esto permite agregar atributos nuevos en cualquier momento:
`obj.nuevo_campo = 123`.

El Costo Oculto:
----------------
Un diccionario `dict` de Python requiere una cantidad no despreciable de memoria RAM
(overhead de hash table). Si tu sistema crea millones de objetos (ej. registros
financieros, nodos de un grafo, partículas en un juego o filas de una BD), el consumo
de memoria se dispara innecesariamente.

La Solución: `__slots__`
------------------------
Al definir `__slots__ = ('attr1', 'attr2')`:
1. Python NO crea el diccionario `__dict__` para cada instancia.
2. Reserva un arreglo estático de tamaño fijo en C para los atributos indicados.
3. Reduce el consumo de RAM hasta en un 60% - 70%.
4. Acelera ligeramente la lectura y escritura de atributos.
5. Impide la creación accidental de atributos no declarados (evita errores tipográficos).
"""

import sys
import tracemalloc


class PuntoNormal:
    """Clase convencional: posee __dict__ dinámico."""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class PuntoConSlots:
    """Clase optimizada: NO posee __dict__, sólo la tupla estricta __slots__."""

    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA Y BENCHMARK DE MEMORIA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 02 - Optimización de Memoria con __slots__")
    print("=" * 65)

    p_normal = PuntoNormal(1.0, 2.0, 3.0)
    p_slots = PuntoConSlots(1.0, 2.0, 3.0)

    # 1. Comparación estructural: presencia de __dict__
    print("\n--- 1. Inspección Estructural ---")
    print(f"PuntoNormal tiene __dict__:    {hasattr(p_normal, '__dict__')}")
    print(f"PuntoConSlots tiene __dict__:  {hasattr(p_slots, '__dict__')}")

    # En PuntoNormal podemos agregar atributos arbitrarios:
    p_normal.color = "Azul"
    print(f"Atributo dinámico en p_normal: color = {p_normal.color}")

    # En PuntoConSlots está prohibido por diseño (protege contra errores tipográficos):
    try:
        p_slots.color = "Rojo"  # Error tipográfico o intento de añadir atributo no declarado
    except AttributeError as err:
        print(f"🛡️ Bloqueado por __slots__: {err}")

    # 2. Benchmark de memoria instanciando 200,000 objetos
    CANTIDAD = 200_000
    print(f"\n--- 2. Benchmark de Memoria instanciando {CANTIDAD:,} objetos ---")

    # Medición para PuntoNormal
    tracemalloc.start()
    puntos_normales = [PuntoNormal(float(i), float(i), float(i)) for i in range(CANTIDAD)]
    mem_normal_actual, mem_normal_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    del puntos_normales  # Liberar memoria para la siguiente prueba

    # Medición para PuntoConSlots
    tracemalloc.start()
    puntos_slots = [PuntoConSlots(float(i), float(i), float(i)) for i in range(CANTIDAD)]
    mem_slots_actual, mem_slots_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    del puntos_slots

    mb_normal = mem_normal_pico / (1024 * 1024)
    mb_slots = mem_slots_pico / (1024 * 1024)
    ahorro_porcentaje = ((mb_normal - mb_slots) / mb_normal) * 100

    print(f"Memoria consumida (PuntoNormal SIN slots):   {mb_normal:.2f} MB")
    print(f"Memoria consumida (PuntoConSlots CON slots): {mb_slots:.2f} MB")
    print(f"🚀 ¡Ahorro neto de RAM conseguido!:        {ahorro_porcentaje:.1f}%")
