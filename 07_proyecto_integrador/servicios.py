"""
==============================================================================
Módulo: 07_proyecto_integrador / servicios.py
Tema: Servicios de Negocio, Estrategias de Descuento (Strategy), Observadores (Observer) y Checkout.
==============================================================================
"""

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
try:
    from .modelos import Cliente
    from .carrito import CarritoCompras
    from .pasarelas import PasarelaPago, ResultadoTransaccion
    from .repositorios import IRepositorioOrden
except (ImportError, ValueError):
    from modelos import Cliente
    from carrito import CarritoCompras
    from pasarelas import PasarelaPago, ResultadoTransaccion
    try:
        from repositorios import IRepositorioOrden
    except ImportError:
        IRepositorioOrden = None

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# PATRÓN STRATEGY: ESTRATEGIAS DE DESCUENTO
# ==============================================================================
class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar_descuento(self, subtotal: float) -> float:
        pass

    @property
    @abstractmethod
    def descripcion(self) -> str:
        pass


class SinDescuento(EstrategiaDescuento):
    @property
    def descripcion(self) -> str:
        return "Sin Descuento"

    def aplicar_descuento(self, subtotal: float) -> float:
        return 0.0


class DescuentoPorcentaje(EstrategiaDescuento):
    def __init__(self, porcentaje: float):
        self.porcentaje = max(0.0, min(100.0, porcentaje))

    @property
    def descripcion(self) -> str:
        return f"Descuento Promo {self.porcentaje:.0f}%"

    def aplicar_descuento(self, subtotal: float) -> float:
        return subtotal * (self.porcentaje / 100.0)


# ==============================================================================
# PATRÓN OBSERVER: SISTEMA DE EVENTOS DE COMPRA (PUB/SUB)
# ==============================================================================
class EscuchadorEvento(ABC):
    @abstractmethod
    def on_orden_completada(self, orden_id: str, cliente: Cliente, monto: float) -> None:
        pass


class NotificadorEmailCliente(EscuchadorEvento):
    def on_orden_completada(self, orden_id: str, cliente: Cliente, monto: float) -> None:
        print(f"📧 [EMAIL CLIENTE]: Estimado/a {cliente.nombre}, confirmamos tu pedido #{orden_id} por ${monto:,.2f}.")


class AuditoriaFiscal(EscuchadorEvento):
    def on_orden_completada(self, orden_id: str, cliente: Cliente, monto: float) -> None:
        print(f"🏛️ [AUDITORÍA]: Impuesto registrado para orden #{orden_id} (Cliente: {cliente.id_usuario}).")


class PublicadorEventos:
    """Mantiene la lista de observadores y transmite novedades."""

    def __init__(self):
        self._escuchadores: list[EscuchadorEvento] = []

    def suscribir(self, escuchador: EscuchadorEvento) -> None:
        self._escuchadores.append(escuchador)

    def emitir_orden_completada(self, orden_id: str, cliente: Cliente, monto: float) -> None:
        for obs in self._escuchadores:
            obs.on_orden_completada(orden_id, cliente, monto)


# ==============================================================================
# SERVICIO DE CHECKOUT (ALTO NIVEL - INYECCIÓN DE DEPENDENCIAS)
# ==============================================================================
@dataclass
class ResumenOrden:
    id_orden: str
    cliente: Cliente
    subtotal: float
    descuento: float
    envio: float
    total: float
    transaccion: ResultadoTransaccion


class ServicioCheckout:
    """Orquestador del proceso de compra desacoplado por DIP."""

    def __init__(
        self,
        pasarela: PasarelaPago,
        publicador: PublicadorEventos,
        repositorio_orden: "IRepositorioOrden | None" = None
    ):
        # Inyección de dependencias
        self.pasarela = pasarela
        self.publicador = publicador
        self.repositorio_orden = repositorio_orden

    def procesar_compra(
        self,
        cliente: Cliente,
        carrito: CarritoCompras,
        estrategia_descuento: EstrategiaDescuento | None = None
    ) -> ResumenOrden:
        if len(carrito) == 0:
            raise ValueError("No se puede procesar una orden con el carrito vacío.")

        descuento_calc = estrategia_descuento or SinDescuento()

        subtotal = carrito.calcular_subtotal()
        monto_descuento = descuento_calc.aplicar_descuento(subtotal)
        envio = carrito.calcular_envio()
        total_a_pagar = (subtotal - monto_descuento) + envio

        id_orden = f"ORD-{abs(hash(cliente.email + str(total_a_pagar))) % 100000:05d}"

        print(f"\n💳 [CHECKOUT]: Solicitando cobro a través de {self.pasarela.nombre}...")
        resultado_pago = self.pasarela.procesar_pago(total_a_pagar, referencia=id_orden)

        if not resultado_pago.exitoso:
            raise RuntimeError(f"El cobro no pudo procesarse: {resultado_pago.mensaje}")

        # Realizar entregas polimórficas de cada producto
        print("\n📦 [DESPACHO DE PRODUCTOS]:")
        for item in carrito:
            print(f"  - {item.producto.entregar(cliente)}")

        # Notificar a los observadores (Observer Pattern)
        self.publicador.emitir_orden_completada(id_orden, cliente, total_a_pagar)

        resumen = ResumenOrden(
            id_orden=id_orden,
            cliente=cliente,
            subtotal=subtotal,
            descuento=monto_descuento,
            envio=envio,
            total=total_a_pagar,
            transaccion=resultado_pago
        )

        # Persistencia en base de datos mediante el ORM (si el repositorio fue inyectado)
        if self.repositorio_orden is not None:
            self.repositorio_orden.guardar_orden(resumen, carrito)
            print(f"💾 [ORM PERSISTENCIA]: Orden #{id_orden} e items guardados exitosamente en MySQL.")

        return resumen
