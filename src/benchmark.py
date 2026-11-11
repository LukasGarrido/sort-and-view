"""
Medicion de rendimiento de block_sort: tiempo y comparaciones segun el tamano de la lista y del bloque.

Uso: python -m src.benchmark
"""
import time

from src.block_sort import block_sort
from src.pokeapi import cargar_pokemon

CAMPOS = ("height", "weight", "base_experience")
TAMANOS = (20, 40, 60, 80, 100, 120, 151)
BLOQUES = (4, 8, 16, 32, 64)
REPETICIONES = 20


class _Contado:
    """Envuelve un valor y cuenta cada comparacion (<, >, <=, >=)."""
    comparaciones = 0

    def __init__(self, v):
        self.v = v

    def __lt__(self, otro):
        _Contado.comparaciones += 1
        return self.v < otro.v

    def __gt__(self, otro):
        _Contado.comparaciones += 1
        return self.v > otro.v

    def __le__(self, otro):
        _Contado.comparaciones += 1
        return self.v <= otro.v

    def __ge__(self, otro):
        _Contado.comparaciones += 1
        return self.v >= otro.v


def _medir(datos, bloque):
    """Devuelve (mejor tiempo en s, comparaciones) de block_sort sobre datos."""
    mejor = float("inf")
    for _ in range(REPETICIONES):
        copia = list(datos)
        t0 = time.perf_counter()
        block_sort(copia, bloque=bloque)
        mejor = min(mejor, time.perf_counter() - t0)
    _Contado.comparaciones = 0
    block_sort([_Contado(x) for x in datos], bloque=bloque)
    return mejor, _Contado.comparaciones


def ejecutar_benchmark():
    """Mide block_sort por campo, tamano de bloque y n; devuelve filas (campo, bloque, n, segundos, comparaciones)."""
    pokemones = cargar_pokemon()
    filas = []
    for campo in CAMPOS:
        for bloque in BLOQUES:
            for n in TAMANOS:
                datos = [p[campo] for p in pokemones[:n]]
                filas.append((campo, bloque, n, *_medir(datos, bloque)))
    return filas


if __name__ == "__main__":
    print(f"{'campo':<16}{'bloque':>7}{'n':>5}{'tiempo':>12}{'comparaciones':>15}")
    for campo, bloque, n, t, c in ejecutar_benchmark():
        print(f"{campo:<16}{bloque:>7}{n:>5}{t * 1e6:>9.1f} us{c:>15}")
