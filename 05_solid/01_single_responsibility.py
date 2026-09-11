"""
==============================================================================
Módulo: 05_solid / 01_single_responsibility.py
Tema: Principio de Responsabilidad Única (SRP - Single Responsibility Principle).
==============================================================================

Definición de Robert C. Martin ("Uncle Bob"):
---------------------------------------------
> "Una clase debe tener una, y sólo una, razón para cambiar."

Esto significa que cada clase debe encargarse de un único aspecto o responsabilidad
dentro del dominio del sistema. Si una clase hace demasiadas cosas, cualquier cambio
en una de ellas puede romper colateralmente las demás.

Antipatrón: La "Clase Dios" (God Class):
----------------------------------------
Una clase que almacena los datos de la factura, calcula impuestos, formatea en HTML,
guarda en la base de datos SQL y envía un correo electrónico al cliente.
- Si cambia la tasa de impuestos -> Modificas la clase.
- Si cambia el diseño visual -> Modificas la clase.
- Si cambias de MySQL a PostgreSQL -> Modificas la clase.
- Si cambias de SendGrid a Amazon SES -> Modificas la clase.
¡5 razones distintas para cambiar la misma clase!
"""

import sys

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. ANTIPATRÓN: CLASE DIOS QUE VIOLA SRP
# ==============================================================================
class FacturaMonoliticaIncorreta:
    """VIOLA SRP: Maneja datos, cálculo, persistencia y notificaciones."""

    def __init__(self, cliente: str, items: list[dict]):
        self.cliente = cliente
        self.items = items

    def calcular_total(self) -> float:
        subtotal = sum(i["precio"] * i["cantidad"] for i in self.items)
        return subtotal * 1.19  # IVA 19%

    def guardar_en_base_datos(self) -> None:
        print("💾 Guardando directamente en tabla SQL 'facturas'...")

    def enviar_por_email(self) -> None:
        print(f"📧 Conectando a servidor SMTP para enviar factura a {self.cliente}...")


# ==============================================================================
# 2. DISEÑO REFRACTORIZADO APLICANDO SRP
# ==============================================================================
class ItemFactura:
    """Responsabilidad 1: Modelar los ítems de venta."""

    def __init__(self, descripcion: str, precio: float, cantidad: int = 1):
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad

    @property
    def subtotal(self) -> float:
        return self.precio * self.cantidad


class Factura:
    """Responsabilidad 2: Contener los datos y calcular el total del pedido."""

    def __init__(self, id_factura: str, cliente: str, items: list[ItemFactura]):
        self.id_factura = id_factura
        self.cliente = cliente
        self.items = items

    def calcular_subtotal(self) -> float:
        return sum(item.subtotal for item in self.items)

    def calcular_total(self, tasa_iva: float = 0.19) -> float:
        return self.calcular_subtotal() * (1 + tasa_iva)


class RepositorioFacturas:
    """Responsabilidad 3: Persistencia de datos (BD / Archivos)."""

    def guardar(self, factura: Factura) -> None:
        print(f"💾 [DB]: Factura #{factura.id_factura} almacenada en base de datos.")


class ServicioImpresionFactura:
    """Responsabilidad 4: Formato y renderizado visual."""

    def renderizar_texto(self, factura: Factura) -> str:
        lineas = [
            f"┌{'─' * 45}┐",
            f"│ FACTURA: {factura.id_factura:<33} │",
            f"│ Cliente: {factura.cliente:<33} │",
            f"├{'─' * 45}┤"
        ]
        for item in factura.items:
            lineas.append(f"│ - {item.descripcion:<20} x{item.cantidad:<2} ${item.subtotal:>8.2f} │")
        lineas.append(f"├{'─' * 45}┤")
        lineas.append(f"│ Total con IVA (19%):        ${factura.calcular_total():>8.2f} │")
        lineas.append(f"└{'─' * 45}┘")
        return "\n".join(lineas)


class ServicioNotificacionFactura:
    """Responsabilidad 5: Comunicación y mensajería."""

    def notificar_cliente(self, factura: Factura, email: str) -> None:
        print(f"📧 [EMAIL]: Factura #{factura.id_factura} enviada a {email}")


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 01 - Principio de Responsabilidad Única (SRP)")
    print("=" * 65)

    # 1. Creamos la factura con sus ítems
    items = [
        ItemFactura("Monitor 4K IPS", 350.0, 1),
        ItemFactura("Cable HDMI 2.1", 15.0, 2)
    ]
    factura = Factura(id_factura="FAC-1001", cliente="Tecnología SAS", items=items)

    # 2. Cada servicio realiza de forma limpia e independiente su tarea
    impresora = ServicioImpresionFactura()
    repo = RepositorioFacturas()
    mailer = ServicioNotificacionFactura()

    print("\n--- 1. Renderizado de Factura ---")
    print(impresora.renderizar_texto(factura))

    print("\n--- 2. Persistencia ---")
    repo.guardar(factura)

    print("\n--- 3. Notificación ---")
    mailer.notificar_cliente(factura, "finanzas@tecnologia.com")
