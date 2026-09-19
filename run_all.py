"""
==============================================================================
Script Principal: run_all.py
Lanzador Interactivo y Ejecutor de la Suite de POO en Python.
==============================================================================
"""

import os
import subprocess
import sys

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

MODULOS = [
    ("01_fundamentos/01_clases_y_objetos.py", "Fundamentos: Clases, Objetos y 'self'"),
    ("01_fundamentos/02_atributos_clase_instancia.py", "Fundamentos: Atributos de Clase vs Instancia"),
    ("01_fundamentos/03_metodos_instancia_clase_estaticos.py", "Fundamentos: Métodos (@classmethod, @staticmethod)"),
    ("01_fundamentos/04_ciclo_de_vida.py", "Fundamentos: Ciclo de Vida (__new__, __init__, __del__)"),
    ("02_pilares/01_encapsulamiento.py", "Pilares: 1. Encapsulamiento y @property"),
    ("02_pilares/02_abstraccion.py", "Pilares: 2. Abstracción y Clases Abstractas (ABC)"),
    ("02_pilares/03_herencia.py", "Pilares: 3. Herencia, MRO y Mixins"),
    ("02_pilares/04_polimorfismo.py", "Pilares: 4. Polimorfismo y Duck Typing"),
    ("03_dunder_methods/01_representacion.py", "Dunder: __str__, __repr__ y __format__"),
    ("03_dunder_methods/02_comparacion.py", "Dunder: Comparaciones y @total_ordering"),
    ("03_dunder_methods/03_operadores_aritmeticos.py", "Dunder: Sobrecarga de Operadores (+, -, *, etc.)"),
    ("03_dunder_methods/04_contenedores_e_iteracion.py", "Dunder: Secuencias, Slices e Iteradores"),
    ("03_dunder_methods/05_context_managers_y_call.py", "Dunder: __call__ y Gestores de Contexto (with)"),
    ("04_avanzado/01_dataclasses.py", "Avanzado: @dataclass, frozen y __post_init__"),
    ("04_avanzado/02_slots.py", "Avanzado: Optimización de RAM con __slots__"),
    ("04_avanzado/03_composicion_vs_herencia.py", "Avanzado: Composición vs Herencia"),
    ("04_avanzado/04_typing_y_protocols.py", "Avanzado: Structural Typing con typing.Protocol"),
    ("04_avanzado/05_metaclases.py", "Avanzado: Metaclases y Fabricación de Clases"),
    ("05_solid/01_single_responsibility.py", "SOLID: S - Single Responsibility (SRP)"),
    ("05_solid/02_open_closed.py", "SOLID: O - Open / Closed (OCP)"),
    ("05_solid/03_liskov_substitution.py", "SOLID: L - Liskov Substitution (LSP)"),
    ("05_solid/04_interface_segregation.py", "SOLID: I - Interface Segregation (ISP)"),
    ("05_solid/05_dependency_inversion.py", "SOLID: D - Dependency Inversion (DIP)"),
    ("06_patrones_diseno/01_creacionales.py", "Patrones: Creacionales (Singleton, Factory, Builder)"),
    ("06_patrones_diseno/02_estructurales.py", "Patrones: Estructurales (Adapter, Decorator, Facade)"),
    ("06_patrones_diseno/03_comportamiento.py", "Patrones: Comportamiento (Strategy, Observer, Command)"),
    ("07_proyecto_integrador/main.py", "Proyecto Integrador: E-Commerce con ORM MySQL (SQLAlchemy)"),
]


def ejecutar_script(ruta: str) -> None:
    print("\n" + "=" * 75)
    print(f"🚀 EJECUTANDO: {ruta}")
    print("=" * 75)
    resultado = subprocess.run([sys.executable, ruta])
    print("=" * 75)
    if resultado.returncode == 0:
        print(f"✅ Finalizado con éxito (Código: 0)")
    else:
        print(f"❌ Error en la ejecución (Código: {resultado.returncode})")
    print("=" * 75)


def ejecutar_pruebas() -> None:
    print("\n" + "=" * 75)
    print("🧪 EJECUTANDO SUITE COMPLETA DE PRUEBAS UNITARIAS")
    print("=" * 75)
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "08_pruebas", "-p", "test_*.py", "-v"])


def ejecutar_todo() -> None:
    for ruta, desc in MODULOS:
        ejecutar_script(ruta)
    ejecutar_pruebas()


def mostrar_menu():
    while True:
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║      MASTER DE PROGRAMACIÓN ORIENTADA A OBJETOS (POO) EN PYTHON     ║")
        print("╠" + "═" * 68 + "╣")
        print("║ Selecciona una opción para ejecutar:                               ║")

        for idx, (_, desc) in enumerate(MODULOS, start=1):
            print(f"║  {idx:>2}. {desc:<63} ║")

        print("╠" + "═" * 68 + "╣")
        print("║   T. Ejecutar TODAS las lecciones en secuencia                     ║")
        print("║   P. Ejecutar la suite de PRUEBAS unitarias automatizadas          ║")
        print("║   0. Salir                                                         ║")
        print("╚" + "═" * 68 + "╝")

        opcion = input("👉 Ingresa tu elección: ").strip().upper()

        if opcion == "0":
            print("\n👋 ¡Hasta pronto! Sigue dominando Python y la POO.\n")
            break
        elif opcion == "T":
            ejecutar_todo()
        elif opcion == "P":
            ejecutar_pruebas()
        elif opcion.isdigit():
            num = int(opcion)
            if 1 <= num <= len(MODULOS):
                ruta, _ = MODULOS[num - 1]
                ejecutar_script(ruta)
            else:
                print("⚠️ Número fuera de rango. Intenta de nuevo.")
        else:
            print("⚠️ Opción no válida.")


if __name__ == "__main__":
    # Si se pasa un argumento por línea de comandos (ej. python run_all.py all)
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("all", "--all", "-a"):
            ejecutar_todo()
        elif arg in ("test", "--test", "-t"):
            ejecutar_pruebas()
        else:
            print(f"Argumento desconocido: {arg}. Usa 'all', 'test' o ejecuta sin argumentos para el menú.")
    else:
        mostrar_menu()
