"""
Medicion de tiempos y comparaciones.

Uso: python -m src.benchmark
"""
import time

from src.block_sort import block_sort
from src.pokeapi import cargar_pokemon

CAMPOS = ("height", "weight", "base_experience")
REPETICIONES = 20


def _tiempo(fn, datos):
    """Mejor tiempo (s) de REPETICIONES corridas sobre copias de datos."""
    mejor = float("inf")
    for _ in range(REPETICIONES):
        copia = list(datos)
        t0 = time.perf_counter()
        resultado = fn(copia)
        mejor = min(mejor, time.perf_counter() - t0)
    return mejor, resultado


def ejecutar_benchmark():
    """Compara block_sort contra sorted() por cada campo numerico; devuelve las filas."""
    pokemones = cargar_pokemon()
    filas = []
    for campo in CAMPOS:
        datos = [p[campo] for p in pokemones]
        t_bs, res = _tiempo(block_sort, datos)
        t_ref, esperado = _tiempo(sorted, datos)
        filas.append((campo, len(datos), t_bs, t_ref, res == esperado))
    return filas


if __name__ == "__main__":
    print(f"{'campo':<16}{'n':>5}{'block_sort':>13}{'sorted':>12}  correcto")
    for campo, n, t_bs, t_ref, ok in ejecutar_benchmark():
        print(f"{campo:<16}{n:>5}{t_bs * 1e6:>10.1f} us{t_ref * 1e6:>9.1f} us  {ok}")
