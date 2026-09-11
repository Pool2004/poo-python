"""
==============================================================================
Módulo: 01_fundamentos / 03_metodos_instancia_clase_estaticos.py
Tema: Métodos de Instancia, Métodos de Clase (@classmethod) y Métodos Estáticos (@staticmethod).
==============================================================================

Resumen Comparativo:
---------------------------------------------------------------------------------------
Tipo de Método       Decorador       1er Parámetro   Acceso a Instancia?  Acceso a Clase?
---------------------------------------------------------------------------------------
De Instancia         (Ninguno)       self            Sí                   Sí (self.__class__)
De Clase             @classmethod    cls             No                   Sí
Estático             @staticmethod   (Ninguno)       No                   No
---------------------------------------------------------------------------------------

Cuándo usar cada uno:
---------------------
1. Métodos de Instancia:
   - Es el método estándar.
   - Se usa cuando el método necesita leer o modificar el estado de la instancia individual.

2. Métodos de Clase (@classmethod):
   - Recibe `cls` como primer argumento en lugar de `self`.
   - Modifica o consulta el estado de la clase en su conjunto.
   - **Caso de uso número uno**: "Constructores Alternativos" (Factory Methods)
     para crear instancias desde diferentes formatos (ej. desde un string, json o dict).

3. Métodos Estáticos (@staticmethod):
   - No recibe ni `self` ni `cls`.
   - Se comporta como una función ordinaria, pero colocada lógicamente dentro del namespace
     de la clase porque tiene una estrecha relación conceptual con ella.
   - Se usa para funciones auxiliares de validación, cálculos o utilidades.
"""

from datetime import date


class Fecha:
    """Clase que representa una fecha y demuestra los 3 tipos de métodos."""

    def __init__(self, dia: int, mes: int, anio: int):
        # Validación básica usando un método estático de la propia clase
        if not self.es_fecha_valida(dia, mes, anio):
            raise ValueError(f"Fecha inválida: {dia}/{mes}/{anio}")

        self.dia = dia
        self.mes = mes
        self.anio = anio

    # --------------------------------------------------------------------------
    # 1. MÉTODO DE INSTANCIA (opera sobre `self`)
    # --------------------------------------------------------------------------
    def formato_legible(self) -> str:
        """Devuelve la fecha en formato legible. Requiere acceso al estado de self."""
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        return f"{self.dia:02d} de {meses[self.mes - 1]} de {self.anio}"

    # --------------------------------------------------------------------------
    # 2. MÉTODO DE CLASE (opera sobre `cls` - Constructores alternativos)
    # --------------------------------------------------------------------------
    @classmethod
    def desde_cadena(cls, texto_fecha: str) -> "Fecha":
        """Constructor alternativo: Crea una instancia a partir de un texto 'DD-MM-YYYY'.

        `cls` hace referencia a la clase Fecha (o cualquier subclase que la herede).
        """
        partes = texto_fecha.split("-")
        if len(partes) != 3:
            raise ValueError("El formato debe ser DD-MM-YYYY")

        dia, mes, anio = map(int, partes)
        return cls(dia, mes, anio)  # Equivale a Fecha(dia, mes, anio)

    @classmethod
    def hoy(cls) -> "Fecha":
        """Constructor alternativo: Crea una instancia con la fecha actual del sistema."""
        fecha_actual = date.today()
        return cls(fecha_actual.day, fecha_actual.month, fecha_actual.year)

    # --------------------------------------------------------------------------
    # 3. MÉTODO ESTÁTICO (función utilitaria pura, independiente de estado)
    # --------------------------------------------------------------------------
    @staticmethod
    def es_bisiesto(anio: int) -> bool:
        """Calcula si un año es bisiesto. No depende de ninguna instancia."""
        return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)

    @staticmethod
    def es_fecha_valida(dia: int, mes: int, anio: int) -> bool:
        """Valida si una combinación de día, mes y año es coherente en el calendario."""
        if anio < 1 or not (1 <= mes <= 12) or dia < 1:
            return False

        dias_por_mes = [31, 29 if Fecha.es_bisiesto(anio) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return dia <= dias_por_mes[mes - 1]


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN: 03 - Métodos de Instancia, Clase y Estáticos")
    print("=" * 65)

    # 1. Constructor tradicional (Método de instancia)
    print("\n--- 1. Constructor Tradicional ---")
    f1 = Fecha(15, 8, 2024)
    print(f"Fecha creada: {f1.formato_legible()}")

    # 2. Constructores alternativos con @classmethod
    print("\n--- 2. Constructores Alternativos (@classmethod) ---")
    f2 = Fecha.desde_cadena("25-12-2025")
    print(f"Desde cadena: {f2.formato_legible()}")

    f3 = Fecha.hoy()
    print(f"Fecha de hoy: {f3.formato_legible()}")

    # 3. Métodos estáticos (@staticmethod)
    print("\n--- 3. Métodos Estáticos (@staticmethod) ---")
    anios_prueba = [2000, 2023, 2024, 2100]
    for anio in anios_prueba:
        bisiesto = Fecha.es_bisiesto(anio)
        estado = "Sí" if bisiesto else "No"
        print(f"¿El año {anio} es bisiesto? -> {estado}")

    # Los métodos estáticos se pueden llamar tanto desde la clase como desde una instancia
    print(f"Llamada desde clase:     Fecha.es_bisiesto(2024) -> {Fecha.es_bisiesto(2024)}")
    print(f"Llamada desde instancia: f1.es_bisiesto(2024)    -> {f1.es_bisiesto(2024)}")
