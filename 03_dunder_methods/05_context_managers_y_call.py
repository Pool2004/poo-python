"""
==============================================================================
Módulo: 03_dunder_methods / 05_context_managers_y_call.py
Tema: Objetos Invocables (__call__) y Gestores de Contexto (__enter__, __exit__).
==============================================================================

1. Objetos Invocables (`__call__`):
----------------------------------
En Python, "todo es un objeto", ¡incluso las funciones!
Si implementas el método `__call__` en una clase, sus instancias pueden ser
invocadas directamente usando paréntesis `objeto(arg1, arg2)` exactamente igual
que una función ordinaria.
- Caso de uso: Funciones con estado interno persistente, memorización (cache),
  o pipelines configurables.

2. Gestores de Contexto (`__enter__` y `__exit__`):
--------------------------------------------------
El protocolo de gestión de contexto permite utilizar la sentencia `with objeto as x:`.
Garantiza que los recursos se limpien y cierren adecuadamente (archivos, sockets,
bloqueos de concurrencia, transacciones de BD), ocurran o no excepciones dentro del bloque.

Firma de `__exit__(self, exc_type, exc_val, exc_tb)`:
- Si no ocurre ningún error: los 3 argumentos son `None`.
- Si ocurre una excepción: recibe el tipo, el valor y el traceback.
- Si retorna `True`: La excepción es SUPRIMIDA (silenciada).
- Si retorna `False` (o `None`): La excepción es PROPAGADA normalmente.
"""

import sys
import time


# ==============================================================================
# 1. EJEMPLO DE __call__: Función con Estado / Pipeline
# ==============================================================================
class FiltroMultiplicador:
    """Instancia que actúa como función invocable manteniendo contador de ejecuciones."""

    def __init__(self, factor: float):
        self.factor = factor
        self.total_invocaciones = 0

    def __call__(self, valor: float) -> float:
        """Permite invocar la instancia como: filtro(10)"""
        self.total_invocaciones += 1
        return valor * self.factor

    def __repr__(self) -> str:
        return f"FiltroMultiplicador(factor={self.factor}, invocaciones={self.total_invocaciones})"


# ==============================================================================
# 2. EJEMPLO DE GESTOR DE CONTEXTO: Cronómetro y Manejo Seguro de Excepciones
# ==============================================================================
class Temporizador:
    """Mide el tiempo de ejecución de un bloque de código y audita errores."""

    def __init__(self, nombre_bloque: str, suprimir_errores: bool = False):
        self.nombre_bloque = nombre_bloque
        self.suprimir_errores = suprimir_errores
        self.inicio = 0.0
        self.duracion = 0.0

    def __enter__(self) -> "Temporizador":
        """Se ejecuta al entrar al bloque 'with'."""
        print(f"⏱️ Iniciando bloque [{self.nombre_bloque}]...")
        self.inicio = time.perf_counter()
        return self  # Lo que se asigna a la variable 'as x'

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Se ejecuta SIEMPRE al salir del bloque 'with'."""
        self.duracion = time.perf_counter() - self.inicio

        if exc_type is not None:
            print(f"⚠️ [ERROR en {self.nombre_bloque}] Tipo: {exc_type.__name__} | Mensaje: {exc_val}")
            print(f"⏱️ Bloque abortado tras {self.duracion * 1000:.3f} ms")
            # Si suprimir_errores es True, devolvemos True para silenciar la excepción
            return self.suprimir_errores

        print(f"✅ [{self.nombre_bloque}] Completado con éxito en {self.duracion * 1000:.3f} ms")
        return False  # No hubo errores


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 05 - __call__ y Gestores de Contexto (with)")
    print("=" * 65)

    # 1. Uso de __call__
    print("\n--- 1. Instancias Invocables con __call__ ---")
    duplicador = FiltroMultiplicador(factor=2.0)
    triplicador = FiltroMultiplicador(factor=3.0)

    print(f"¿Es invocable (callable)? {callable(duplicador)}")

    # Invocamos el objeto directamente como función:
    print(f"duplicador(5)   -> {duplicador(5)}")
    print(f"duplicador(12)  -> {duplicador(12)}")
    print(f"triplicador(10) -> {triplicador(10)}")
    print(f"Estado de duplicador: {duplicador}")

    # 2. Gestor de contexto exitoso
    print("\n--- 2. Gestor de Contexto: Ejecución Exitosa ---")
    with Temporizador("Cálculo de Suma de Cuadrados") as crono:
        total = sum(x**2 for x in range(100_000))
        print(f"Resultado computado: {total}")
    print(f"Duración registrada en crono.duracion: {crono.duracion * 1000:.3f} ms")

    # 3. Gestor de contexto con manejo y supresión de excepciones
    print("\n--- 3. Gestor de Contexto: Manejo de Excepción Controlada ---")
    with Temporizador("Operación con Falla Controlada", suprimir_errores=True):
        print("Realizando cálculo riesgoso...")
        division = 10 / 0  # Provoca ZeroDivisionError
        print("Esta línea nunca se ejecutará.")

    print("🚀 El programa continúa con normalidad porque __exit__ suprimió la excepción.")
