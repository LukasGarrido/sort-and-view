"""
Pruebas unitarias para el cliente y procesador de PokeAPI / dataset local.
"""
import unittest
from pathlib import Path
import requests_cache
from src.pokeapi import CACHE_DIR, cargar_pokemon, all_pokemon, filtrar_por_tipo, buscar_pokemon, JSON_PATH


class TestPokeAPI(unittest.TestCase):
    def test_cache_directory_configured(self):
        """Verifica que el directorio de cache apunta al estandar del sistema operativo."""
        self.assertIsInstance(CACHE_DIR, Path)
        self.assertTrue(CACHE_DIR.exists())

    def test_requests_cache_installed(self):
        """Verifica que requests_cache esta instalado."""
        self.assertTrue(requests_cache.is_installed())

    def test_cargar_pokemon_local(self):
        """Verifica que se pueden cargar los Pokémon desde el archivo JSON local."""
        pokemones = cargar_pokemon()
        self.assertIsInstance(pokemones, list)
        self.assertGreater(len(pokemones), 0)
        # Verificar campos esperados
        p = pokemones[0]
        for campo in ["id", "name", "height", "weight", "base_experience", "tipo"]:
            self.assertIn(campo, p)

    def test_all_pokemon_limit(self):
        """Verifica que all_pokemon respeta el límite y carga desde el dataset local."""
        pokemones = all_pokemon(limit=10)
        self.assertEqual(len(pokemones), 10)

    def test_filtrar_por_tipo(self):
        """Verifica el filtrado de Pokémon por tipo."""
        grass_pokemones = filtrar_por_tipo("grass")
        self.assertGreater(len(grass_pokemones), 0)
        for p in grass_pokemones:
            self.assertEqual(p["tipo"].lower(), "grass")

    def test_buscar_pokemon(self):
        """Verifica la búsqueda de Pokémon por nombre."""
        resultados = buscar_pokemon("bulba")
        self.assertGreater(len(resultados), 0)
        self.assertEqual(resultados[0]["name"], "bulbasaur")


if __name__ == '__main__':
    unittest.main()
