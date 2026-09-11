"""
==============================================================================
Módulo: 02_pilares / 04_polimorfismo.py
Tema: Cuarto Pilar: Polimorfismo y la Filosofía del Duck Typing.
==============================================================================

¿Qué es el Polimorfismo?
------------------------
Proviene del griego "muchas formas". Es la capacidad que tienen diferentes objetos
de responder al mismo mensaje (mismo nombre de método) cada uno con su propia lógica
especializada.

En lenguajes estáticos tradicionales (Java, C++), el polimorfismo suele depender
estrictamente de que las clases compartan una misma jerarquía de herencia o interfaz.

En Python: Duck Typing ("Tipado de Pato")
-----------------------------------------
En Python, el polimorfismo alcanza su máxima expresión gracias al adagio:
> "Si camina como un pato y grazna como un pato, para nosotros es un pato."

Esto significa que a una función no le importa el "tipo" o "árbol genealógico"
del objeto que recibe, sino las capacidades (métodos) que ese objeto puede realizar.
No hace falta heredar de una clase común; basta con que el objeto tenga el método
requerido.
"""

import sys


# ==============================================================================
# 1. POLIMORFISMO POR HERENCIA (Sobrescritura de Métodos)
# ==============================================================================
class Notificador:
    """Clase base de notificación."""

    def enviar(self, destinatario: str, mensaje: str) -> None:
        raise NotImplementedError("Las subclases deben implementar este método")


class NotificadorEmail(Notificador):
    def enviar(self, destinatario: str, mensaje: str) -> None:
        print(f"📧 Enviando Email a [{destinatario}]: '{mensaje}' (vía servidor SMTP)")


class NotificadorSMS(Notificador):
    def enviar(self, destinatario: str, mensaje: str) -> None:
        print(f"📱 Enviando SMS al [{destinatario}]: '{mensaje}' (vía Twilio API)")


# ==============================================================================
# 2. POLIMORFISMO POR DUCK TYPING (¡Sin herencia alguna!)
# ==============================================================================
class NotificadorDiscordWebhook:
    """Esta clase NO hereda de Notificador, pero 'sabe enviar'.

    Cumple con el contrato de forma implícita por Duck Typing.
    """

    def enviar(self, destinatario: str, mensaje: str) -> None:
        canal = destinatario
        print(f"🎮 Publicando en Discord #{canal}: '{mensaje}' (vía Webhook HTTP)")


# ==============================================================================
# 3. FUNCIÓN POLIMÓRFICA CONSUMIDORA
# ==============================================================================
def notificar_alerta_sistema(notificadores: list, usuarios: list[dict], alerta: str) -> None:
    """Función que consume múltiples notificadores sin importarle su clase exacta.

    Aplica polimorfismo puro.
    """
    for usuario in usuarios:
        print(f"\nProcesando alertas para usuario: {usuario['nombre']}")
        for n in notificadores:
            # Polimorfismo: se llama a .enviar() y cada clase reacciona a su manera
            n.enviar(usuario["contacto"], alerta)


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 04 - Polimorfismo y Duck Typing")
    print("=" * 65)

    lista_notificadores = [
        NotificadorEmail(),
        NotificadorSMS(),
        NotificadorDiscordWebhook(),  # Entra en la lista sin compartir clase base
    ]

    usuarios_sistema = [
        {"nombre": "Laura Gómez", "contacto": "laura@empresa.com"},
        {"nombre": "Servidor Alertas", "contacto": "canal-devops"},
    ]

    print("\n--- Ejecutando función polimórfica ---")
    notificar_alerta_sistema(
        notificadores=lista_notificadores,
        usuarios=usuarios_sistema,
        alerta="ALERTA CRÍTICA: Despliegue v2.4 completado con éxito."
    )

    print("\n--- Verificación de Tipos ---")
    for n in lista_notificadores:
        print(f"Clase: {n.__class__.__name__:<25} ¿Hereda de Notificador? {isinstance(n, Notificador)}")
