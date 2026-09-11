"""
==============================================================================
Módulo: 03_dunder_methods / 04_contenedores_e_iteracion.py
Tema: Emulación de Contenedores (Secuencias) y Protocolo de Iteración.
==============================================================================

El Protocolo de Secuencia en Python:
------------------------------------
Permite que tus propios objetos se comporten exactamente como una lista, tupla
o diccionario de Python:

Método Dunder              Sintaxis / Uso en Python
-------------------------  ------------------------------------------
__len__(self)              len(objeto)
__getitem__(self, key)     objeto[key], objeto[inicio:fin:paso] (slices)
__setitem__(self, key, v)  objeto[key] = v
__delitem__(self, key)     del objeto[key]
__contains__(self, item)   item in objeto

El Protocolo de Iteración:
--------------------------
1. Iterable (`__iter__`):
   - Cualquier objeto que implemente `__iter__()` retornando un iterador.
   - Permite que el objeto sea usado en bucles `for x in coleccion:`,
     comprensiones de listas `[x for x in ...]`, y desempacado `a, b = coleccion`.

2. Iterador (`__next__`):
   - Devuelve el siguiente elemento disponible.
   - Cuando se terminan los datos, debe lanzar obligatoriamente la excepción `StopIteration`.
"""

import sys


class Cancion:
    """Representa una pista musical."""

    def __init__(self, titulo: str, artista: str, duracion_seg: int):
        self.titulo = titulo
        self.artista = artista
        self.duracion_seg = duracion_seg

    def __repr__(self) -> str:
        minutos = self.duracion_seg // 60
        segundos = self.duracion_seg % 60
        return f"'{self.titulo}' - {self.artista} ({minutos}:{segundos:02d})"


class Playlist:
    """Colección personalizada que implementa el protocolo completo de secuencia e iteración."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self._canciones: list[Cancion] = []

    def agregar(self, cancion: Cancion) -> None:
        self._canciones.append(cancion)

    # 1. Longitud: len(playlist)
    def __len__(self) -> int:
        return len(self._canciones)

    # 2. Acceso por índice y rebanado (Slicing): playlist[0], playlist[1:3]
    def __getitem__(self, item):
        # Si el usuario pide un slice [0:2], Python pasa un objeto `slice`
        return self._canciones[item]

    # 3. Asignación por índice: playlist[0] = nueva_cancion
    def __setitem__(self, index: int, cancion: Cancion) -> None:
        if not isinstance(cancion, Cancion):
            raise TypeError("Sólo se pueden asignar objetos de tipo Cancion.")
        self._canciones[index] = cancion

    # 4. Eliminación por índice: del playlist[0]
    def __delitem__(self, index: int) -> None:
        del self._canciones[index]

    # 5. Pertenencia: "cancion in playlist" o búsqueda por título
    def __contains__(self, item) -> bool:
        if isinstance(item, Cancion):
            return item in self._canciones
        elif isinstance(item, str):
            # Permite buscar si un título de canción está en la playlist: "Bohemian Rhapsody" in playlist
            return any(c.titulo.lower() == item.lower() for c in self._canciones)
        return False

    # 6. Protocolo de iteración: for c in playlist:
    def __iter__(self):
        # Forma más sencilla y eficiente: retornar el iterador de la lista interna
        return iter(self._canciones)


# ==============================================================================
# DEMOSTRACIÓN PRÁCTICA
# ==============================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 65)
    print("DEMOSTRACIÓN: 04 - Contenedores y Protocolo de Iteración")
    print("=" * 65)

    playlist = Playlist("Éxitos del Rock")
    c1 = Cancion("Bohemian Rhapsody", "Queen", 354)
    c2 = Cancion("Hotel California", "Eagles", 390)
    c3 = Cancion("Stairway to Heaven", "Led Zeppelin", 482)
    c4 = Cancion("Comfortably Numb", "Pink Floyd", 382)

    for c in [c1, c2, c3, c4]:
        playlist.agregar(c)

    # 1. Longitud con len()
    print("\n--- 1. Protocolo len() ---")
    print(f"Playlist '{playlist.nombre}' contiene {len(playlist)} canciones.")

    # 2. Indexación y Slices con []
    print("\n--- 2. Indexación y Rebanado (Slicing) ---")
    print(f"Primera pista (playlist[0]): {playlist[0]}")
    print(f"Última pista  (playlist[-1]): {playlist[-1]}")
    print(f"Rebanado      (playlist[1:3]): {playlist[1:3]}")

    # 3. Operador de pertenencia 'in' (__contains__)
    print("\n--- 3. Pertenencia 'in' (__contains__) ---")
    print(f"¿Está 'Hotel California' en la playlist? {'Hotel California' in playlist}")
    print(f"¿Está 'Despacito' en la playlist?        {'Despacito' in playlist}")

    # 4. Bucle for e iteración (__iter__)
    print("\n--- 4. Bucle for directo sobre el objeto Playlist ---")
    for i, pista in enumerate(playlist, start=1):
        print(f"  {i}. {pista}")

    # 5. Comprensión de listas y desempacado
    print("\n--- 5. Comprensiones y operaciones funcionales ---")
    canciones_largas = [c.titulo for c in playlist if c.duracion_seg > 400]
    print(f"Pistas de más de 6 minutos: {canciones_largas}")
