"""
==============================================================================
Módulo: 02_pilares / 01_encapsulamiento.py
Tema: Primer Pilar: Encapsulamiento, Visibilidad y el Decorador @property.
==============================================================================

¿Qué es el Encapsulamiento?
---------------------------
Es el principio de ocultar el estado interno y los detalles de implementación
de un objeto, exponiendo únicamente una interfaz pública y segura para interactuar
con él. Sus metas son:
1. Proteger los datos contra modificaciones erróneas o estados inválidos.
2. Desacoplar la implementación interna del código cliente exterior.

Niveles de Acceso en Python:
----------------------------
A diferencia de Java o C++, en Python "todos somos adultos responsables". No existen
palabras reservadas como `private` o `protected` a nivel de máquina virtual, sino
convenciones sintácticas muy respetadas:

1. Público (`self.nombre`):
   - Accesible libremente desde cualquier lugar fuera o dentro de la clase.

2. Protegido (`self._saldo` con un guion bajo):
   - Convención: "Por favor no toques esto desde fuera; es de uso interno de la clase
     o de sus subclases". No hay restricción forzada, es un pacto entre programadores.

3. Privado (`self.__clave` con doble guion bajo):
   - Activa el mecanismo de **Name Mangling** (transformación de nombres).
   - Python renombra automáticamente el atributo internamente como `_NombreClase__clave`.
   - Su objetivo principal es evitar colisiones accidentales de nombres en jerarquías
     de herencia complejas.

El Camino Idiomático en Python: `@property`
-------------------------------------------
En lugar de escribir molestos métodos al estilo Java como `get_saldo()` y `set_saldo()`,
Python utiliza el decorador `@property`. Permite acceder a un método con la sintaxis
natural de un atributo (`cuenta.saldo = 100`) mientras ejecuta lógica de validación
detrás de escena.
"""

import sys


class CuentaBancaria:
    """Modela una cuenta bancaria con estricto encapsulamiento y validaciones."""

    def __init__(self, titular: str, saldo_inicial: float = 0.0, pin: str = "1234"):
        # Atributo público
        self.titular = titular

        # Atributo protegido (convención interna)
        self._numero_cuenta = f"CTA-{hash(titular) % 100000:05d}"

        # Atributo privado (sufrirá Name Mangling)
        self.__pin = str(pin)

        # Usamos el setter de la property para validar el saldo inicial
        self._saldo = 0.0
        self.saldo = saldo_inicial  # Invoca a @saldo.setter

    # --- GETTER ---
    @property
    def saldo(self) -> float:
        """Getter: Permite leer el saldo de forma segura."""
        return self._saldo

    # --- SETTER ---
    @saldo.setter
    def saldo(self, nuevo_saldo: float) -> None:
        """Setter: Valida que el saldo nunca sea negativo."""
        if not isinstance(nuevo_saldo, (int, float)):
            raise TypeError("El saldo debe ser un número numérico válido.")
        if nuevo_saldo < 0:
            raise ValueError("El saldo no puede ser negativo. Transacción rechazada.")
        self._saldo = float(nuevo_saldo)

    # --- MÉTODO PARA PROPIEDAD DE SÓLO LECTURA ---
    @property
    def numero_cuenta(self) -> str:
        """Propiedad de sólo lectura: No tiene setter, nadie puede sobreescribirla directamente."""
        return self._numero_cuenta

    def depositar(self, monto: float) -> str:
        """Operación de negocio para agregar fondos."""
        if monto <= 0:
            raise ValueError("El monto a depositar debe ser mayor a cero.")
        self._saldo += monto
        return f"💵 Depósito exitoso: +${monto:,.2f}. Saldo actual: ${self._saldo:,.2f}"

    def retirar(self, monto: float, pin_ingresado: str) -> str:
        """Operación de negocio que exige autenticación de PIN."""
        if pin_ingresado != self.__pin:
            return "❌ Error de seguridad: PIN incorrecto."

        if monto <= 0:
            return "❌ El monto a retirar debe ser positivo."

        if monto > self._saldo:
            return f"❌ Fondos insuficientes. Saldo disponible: ${self._saldo:,.2f}"

        self._saldo -= monto
        return f"🏧 Retiro exitoso: -${monto:,.2f}. Saldo restante: ${self._saldo:,.2f}"


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 01 - Encapsulamiento y Decorador @property")
    print("=" * 65)

    cuenta = CuentaBancaria("Alejandro Gomez", saldo_inicial=500.0, pin="9876")

    # 1. Lectura transparente mediante @property
    print("\n--- 1. Acceso a Properties de Lectura ---")
    print(f"Titular (Público):      {cuenta.titular}")
    print(f"Cuenta (Sólo Lectura):  {cuenta.numero_cuenta}")
    print(f"Saldo (Vía @property):  ${cuenta.saldo:,.2f}")

    # 2. Modificación controlada mediante @setter
    print("\n--- 2. Modificación Válida vía @saldo.setter ---")
    cuenta.saldo = 750.0  # Parece un atributo ordinario, pero ejecuta validación
    print(f"Nuevo saldo asignado: ${cuenta.saldo:,.2f}")

    # 3. Intentar asignar un estado inválido activa las defensas de la clase
    print("\n--- 3. Protección contra Datos Inválidos ---")
    try:
        cuenta.saldo = -200.0  # Intentamos dejar saldo negativo
    except ValueError as err:
        print(f"🛡️ Bloqueado por setter: {err}")

    # 4. Intentar modificar propiedad de sólo lectura
    try:
        cuenta.numero_cuenta = "CTA-HACKED"
    except AttributeError as err:
        print(f"🛡️ Bloqueado intento de cambiar propiedad sólo lectura: {err}")

    # 5. Name Mangling: ¿Qué pasó con __pin?
    print("\n--- 4. Demostración de Name Mangling (Atributos Privados) ---")
    try:
        # Intentar acceder directamente a __pin falla
        print(cuenta.__pin)
    except AttributeError:
        print("🔒 Acceso directo 'cuenta.__pin' falló: El atributo fue renombrado.")

    # Python lo transformó en `_CuentaBancaria__pin`
    print(f"🔍 Acceso tras el 'mangling': cuenta._CuentaBancaria__pin = '{cuenta._CuentaBancaria__pin}'")
    print("   (Demuestra que Python no bloquea a la fuerza, sino que protege los nombres).")

    # 6. Uso a través de la interfaz pública
    print("\n--- 5. Interacción mediante Métodos de Negocio Seguros ---")
    print(cuenta.depositar(250.0))
    print(cuenta.retirar(100.0, pin_ingresado="0000"))  # PIN incorrecto
    print(cuenta.retirar(100.0, pin_ingresado="9876"))  # PIN correcto
