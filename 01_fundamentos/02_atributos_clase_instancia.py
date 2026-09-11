"""
==============================================================================
Módulo: 01_fundamentos / 02_atributos_clase_instancia.py
Tema: Atributos de Clase vs Atributos de Instancia y Trampas de Mutabilidad.
==============================================================================

Diferencia Fundamental:
-----------------------
1. Atributos de Instancia:
   - Se definen usualmente dentro de `__init__` precedidos por `self.`
   - Cada objeto tiene su propia copia independiente de estos datos.
   - Modificarlo en un objeto NO afecta a ningún otro objeto.

2. Atributos de Clase (Variables estáticas en otros lenguajes):
   - Se definen directamente dentro del cuerpo de la clase, fuera de cualquier método.
   - Son compartidos por TODAS las instancias de esa clase.
   - Existe una única copia en memoria asociada a la clase en sí.

Orden de Búsqueda de Atributos (Namespace Lookup):
-------------------------------------------------
Cuando haces `objeto.nombre_atributo`, Python busca en este orden:
1. En el diccionario de la instancia (`objeto.__dict__`).
2. Si no lo encuentra, busca en el diccionario de la clase (`Clase.__dict__`).
3. Si no lo encuentra, busca en las clases padre (según el MRO).
4. Si nadie lo tiene, lanza un error `AttributeError`.

⚠️ La trampa común de los atributos mutables de clase:
-----------------------------------------------------
Si declaras una lista o diccionario como atributo de clase, ¡TODAS las instancias
modificarán el mismo contenedor en memoria!
"""


class Empleado:
    """Demostración de atributos de clase e instancia bien implementados."""

    # --- ATRIBUTOS DE CLASE ---
    empresa: str = "TechCorp Global"
    tasa_aumento_anual: float = 1.05  # 5% de aumento estándar
    total_empleados: int = 0  # Contador global compartido

    def __init__(self, nombre: str, salario: float):
        # --- ATRIBUTOS DE INSTANCIA ---
        self.nombre = nombre
        self.salario = salario

        # Modificamos el atributo de clase compartido a través de la Clase
        Empleado.total_empleados += 1
        self.id_empleado = Empleado.total_empleados

    def aplicar_aumento(self) -> None:
        """Aplica el aumento utilizando la tasa actual."""
        # Se busca self.tasa_aumento_anual. Si la instancia no la sobreescribe,
        # toma la de la clase.
        self.salario *= self.tasa_aumento_anual

    def __str__(self) -> str:
        return f"Empleado #{self.id_empleado}: {self.nombre} | Salario: ${self.salario:,.2f} | Empresa: {self.empresa}"


# ==============================================================================
# DEMOSTRACIÓN DE LA TRAMPA DE MUTABILIDAD
# ==============================================================================
class UsuarioIncorrecto:
    """¡ANTIPATRÓN! Usa una lista mutable como atributo de clase."""
    amigos = []  # COMPARTIDO POR TODOS: GRAVE ERROR DE DISEÑO

    def __init__(self, nombre: str):
        self.nombre = nombre


class UsuarioCorrecto:
    """PATRÓN CORRECTO: Inicializa contenedores mutables por instancia."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.amigos: list[str] = []  # Cada usuario tiene su propia lista


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 02 - Atributos de Clase vs Instancia")
    print("=" * 65)

    print("\n--- 1. Compartición de Atributos de Clase ---")
    emp1 = Empleado("Ana Martínez", 50000)
    emp2 = Empleado("Carlos López", 65000)

    print(emp1)
    print(emp2)
    print(f"Total empleados registrados: {Empleado.total_empleados}")

    # 2. Modificar atributo de clase afecta a todas las instancias (si no lo han sobreescrito)
    print("\n--- 2. Modificando atributo de clase a nivel global ---")
    Empleado.empresa = "TechCorp Solutions (Adquirida)"
    print(f"Empresa de {emp1.nombre}: {emp1.empresa}")
    print(f"Empresa de {emp2.nombre}: {emp2.empresa}")

    # 3. Sobrescritura ("Shadowing") en una instancia específica
    print("\n--- 3. Shadowing: Crear atributo de instancia con mismo nombre ---")
    # Para Carlos damos un bono especial aumentando solo su tasa
    emp2.tasa_aumento_anual = 1.15  # 15% solo para Carlos

    emp1.aplicar_aumento()  # Usa 1.05 (de la clase)
    emp2.aplicar_aumento()  # Usa 1.15 (de su propia instancia)

    print(f"Nuevo salario {emp1.nombre} (tasa {emp1.tasa_aumento_anual}): ${emp1.salario:,.2f}")
    print(f"Nuevo salario {emp2.nombre} (tasa {emp2.tasa_aumento_anual}): ${emp2.salario:,.2f}")

    # Exploración de namespaces con __dict__
    print("\n--- 4. Inspección de __dict__ en memoria ---")
    print(f"Namespace emp1: {emp1.__dict__}")
    print(f"Namespace emp2 (tiene tasa_aumento_anual propia): {emp2.__dict__}")

    # 4. Trampa de la lista mutable
    print("\n--- 5. ¡CUIDADO! La trampa del atributo mutable de clase ---")
    u1 = UsuarioIncorrecto("Roberto")
    u2 = UsuarioIncorrecto("Lucía")

    u1.amigos.append("Pedro")  # Roberto agrega a Pedro

    print("Con Antipatrón (lista en clase):")
    print(f"Amigos de Roberto: {u1.amigos}")
    print(f"Amigos de Lucía:   {u2.amigos}  <- ¡Lucía tiene a Pedro sin haberlo agregado!")

    print("\nCon Diseño Correcto (lista en __init__):")
    c1 = UsuarioCorrecto("Roberto")
    c2 = UsuarioCorrecto("Lucía")

    c1.amigos.append("Pedro")
    print(f"Amigos de Roberto: {c1.amigos}")
    print(f"Amigos de Lucía:   {c2.amigos}  <- Lista completamente aislada e independiente.")
