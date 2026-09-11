"""
==============================================================================
Módulo: 04_avanzado / 04_typing_y_protocols.py
Tema: Tipado Estructural y Protocolos (typing.Protocol) en Python Moderno.
==============================================================================

Subtipado Nominal vs Subtipado Estructural:
-------------------------------------------
1. Subtipado Nominal (Clásico con `abc.ABC`):
   - Una clase `B` sólo es considerada compatible con `A` si declara EXPLÍCITAMENTE
     que hereda de ella: `class B(A):`.
   - Problema: Si usas una librería de terceros que ya tiene los métodos pero no hereda
     de tu clase ABC, no puedes pasarla sin envolverla en un adapter.

2. Subtipado Estructural (Duck Typing Estático con `typing.Protocol` - PEP 544):
   - Introducido en Python 3.8.
   - Una clase es compatible con un `Protocol` si tiene los MISMOS MÉTODOS Y FIRMAS,
     ¡sin necesidad de heredar de él!
   - Combina lo mejor de dos mundos:
     a) La libertad y flexibilidad del Duck Typing tradicional.
     b) La seguridad y validación en tiempo de desarrollo de analizadores estáticos (Mypy, Pyright, IDEs).

El Decorador `@runtime_checkable`:
---------------------------------
Permite que un `Protocol` pueda ser verificado en tiempo de ejecución mediante
`isinstance(objeto, MiProtocolo)`.
"""

import sys
from typing import Protocol, runtime_checkable


# ==============================================================================
# DEFINICIÓN DEL PROTOCOLO (CONTRATO ESTRUCTURAL)
# ==============================================================================
@runtime_checkable
class ExportablePDF(Protocol):
    """Cualquier clase que implemente 'obtener_contenido_pdf' y 'titulo' cumple el protocolo."""

    @property
    def titulo(self) -> str:
        ...

    def obtener_contenido_pdf(self) -> bytes:
        ...


# ==============================================================================
# CLASES CONCRETAS (¡NINGUNA hereda explícitamente de ExportablePDF!)
# ==============================================================================
class FacturaVenta:
    """Clase del módulo de Facturación."""

    def __init__(self, numero: str, total: float):
        self.numero = numero
        self.total = total

    @property
    def titulo(self) -> str:
        return f"Factura #{self.numero}"

    def obtener_contenido_pdf(self) -> bytes:
        texto = f"FACTURA: {self.numero} | TOTAL A PAGAR: ${self.total:,.2f}"
        return texto.encode("utf-8")


class CertificadoCurso:
    """Clase del módulo de Educación / LMS."""

    def __init__(self, estudiante: str, curso: str):
        self.estudiante = estudiante
        self.curso = curso

    @property
    def titulo(self) -> str:
        return f"Certificado de {self.estudiante}"

    def obtener_contenido_pdf(self) -> bytes:
        texto = f"Certificamos que {self.estudiante} completó exitosamente el curso '{self.curso}'."
        return texto.encode("utf-8")


class ArchivoIncompatible:
    """Clase que NO cumple con la firma esperada del protocolo."""

    def __init__(self, datos: str):
        self.datos = datos


# ==============================================================================
# SERVICIO CONSUMIDOR BASADO EN PROTOCOL
# ==============================================================================
def generar_archivo_descarga(documento: ExportablePDF) -> str:
    """Función de exportación protegida por el Protocol."""
    # Validación en tiempo de ejecución gracias a @runtime_checkable
    if not isinstance(documento, ExportablePDF):
        raise TypeError(f"El objeto {type(documento).__name__} no satisface el protocolo ExportablePDF")

    contenido_binario = documento.obtener_contenido_pdf()
    return (
        f"📄 Generando PDF para: '{documento.titulo}'\n"
        f"   Bytes generados: {len(contenido_binario)} bytes\n"
        f"   Vista previa:   {contenido_binario.decode('utf-8')}"
    )


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 04 - Protocols y Tipado Estructural")
    print("=" * 65)

    factura = FacturaVenta("FAC-2024-9981", 450.00)
    certificado = CertificadoCurso("Martín Carrera", "Arquitectura POO Avanzada")
    invalido = ArchivoIncompatible("datos sueltos")

    # 1. Verificación en tiempo de ejecución con isinstance()
    print("\n--- 1. Inspección de Tipos Estructurales con isinstance() ---")
    print(f"¿factura cumple ExportablePDF?     {isinstance(factura, ExportablePDF)}")
    print(f"¿certificado cumple ExportablePDF? {isinstance(certificado, ExportablePDF)}")
    print(f"¿invalido cumple ExportablePDF?    {isinstance(invalido, ExportablePDF)}")

    # 2. Ejecución con objetos compatibles
    print("\n--- 2. Exportación de Documentos Válidos ---")
    print(generar_archivo_descarga(factura))
    print()
    print(generar_archivo_descarga(certificado))

    # 3. Protección ante objetos incompatibles
    print("\n--- 3. Rechazo de Objeto Incompatible ---")
    try:
        generar_archivo_descarga(invalido)  # type: ignore
    except TypeError as err:
        print(f"🛡️ Error detectado con éxito: {err}")
