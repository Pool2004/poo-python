"""
==============================================================================
Módulo: 07_proyecto_integrador / main.py
Tema: Ejecución y Demostración Integral del Sistema de Comercio Electrónico.
==============================================================================
"""

import sys

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .modelos import Cliente, ProductoFisico, ProductoDigital
    from .carrito import CarritoCompras
    from .pasarelas import StripePasarela, PayPalPasarela
    from .servicios import (
        ServicioCheckout,
        PublicadorEventos,
        NotificadorEmailCliente,
        AuditoriaFiscal,
        DescuentoPorcentaje
    )
except (ImportError, ValueError):
    from modelos import Cliente, ProductoFisico, ProductoDigital
    from carrito import CarritoCompras
    from pasarelas import StripePasarela, PayPalPasarela
    from servicios import (
        ServicioCheckout,
        PublicadorEventos,
        NotificadorEmailCliente,
        AuditoriaFiscal,
        DescuentoPorcentaje
    )


def ejecutar_demostracion():
    print("=" * 70)
    print("PROYECTO INTEGRADOR: Sistema de E-Commerce y Pasarela Multicanal")
    print("=" * 70)

    # 1. Creación de Actores del Sistema
    print("\n--- 1. Creación de Cliente (Encapsulación y Validación) ---")
    cliente = Cliente(
        id_usuario="USR-8841",
        nombre="Valeria Restrepo",
        email="valeria.restrepo@correo.com",
        direccion="Calle 72 # 11-45, Bogotá, Colombia",
        saldo_billetera=1200.0
    )
    print(f"Cliente registrado: {cliente}")

    # 2. Catálogo de Productos (Herencia y Polimorfismo)
    print("\n--- 2. Catálogo de Productos (Físicos y Digitales) ---")
    teclado = ProductoFisico("TEC-01", "Teclado Mecánico RGB", 120.0, peso_kg=1.2)
    monitor = ProductoFisico("MON-02", "Monitor Curvo 27''", 350.0, peso_kg=4.5)
    curso = ProductoDigital("CUR-03", "Masterclass en POO Python 3.11", 49.99, "https://academy.io/dl/curso-poo")

    print(f"Producto 1: {teclado} | Envío estimado: ${teclado.calcular_costo_envio():.2f}")
    print(f"Producto 2: {monitor} | Envío estimado: ${monitor.calcular_costo_envio():.2f}")
    print(f"Producto 3: {curso}   | Envío estimado: ${curso.calcular_costo_envio():.2f}")

    # 3. Construcción del Carrito (Dunder Methods)
    print("\n--- 3. Operaciones de Carrito con Dunder Methods ---")
    carrito = CarritoCompras()
    carrito.agregar(teclado, cantidad=1)
    carrito.agregar(monitor, cantidad=1)

    # Uso del operador + sobrecargado
    print("Agregando producto digital usando operador sobrecargado '+'...")
    carrito = carrito + curso

    print(f"Total unidades en carrito (len): {len(carrito)} unidades")
    print(f"¿Está el monitor en el carrito? ('MON-02' in carrito): {'MON-02' in carrito}")
    print(f"Resumen del carrito: {carrito}")

    # 4. Configuración del Bus de Eventos (Observer)
    print("\n--- 4. Configuración del Bus de Observadores (Pub/Sub) ---")
    bus_eventos = PublicadorEventos()
    bus_eventos.suscribir(NotificadorEmailCliente())
    bus_eventos.suscribir(AuditoriaFiscal())

    # 5. Inyección de Dependencias y Procesamiento de Checkout (SOLID + Strategy)
    print("\n--- 5. Ejecución del Checkout con Inyección de Dependencias ---")
    pasarela_stripe = StripePasarela(api_key="sk_live_master_992182")
    checkout = ServicioCheckout(pasarela=pasarela_stripe, publicador=bus_eventos)

    # Aplicamos estrategia de descuento (Black Friday 15%)
    promo_15 = DescuentoPorcentaje(15.0)

    orden_final = checkout.procesar_compra(
        cliente=cliente,
        carrito=carrito,
        estrategia_descuento=promo_15
    )

    print("\n" + "=" * 70)
    print("RESUMEN DE ORDEN GENERADA EXITOSAMENTE")
    print("=" * 70)
    print(f"ID Orden:         {orden_final.id_orden}")
    print(f"Subtotal Bruto:   ${orden_final.subtotal:>9.2f}")
    print(f"Descuento ({promo_15.descripcion}): -${orden_final.descuento:>8.2f}")
    print(f"Costo de Envío:   +${orden_final.envio:>8.2f}")
    print(f"Total Facturado:   ${orden_final.total:>9.2f}")
    print(f"Transacción:      {orden_final.transaccion}")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_demostracion()
