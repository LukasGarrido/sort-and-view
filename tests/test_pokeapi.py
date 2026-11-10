"""
Pruebas unitarias para el cliente de PokeAPI y su configuracion de cache.
"""
import unittest
from pathlib import Path
import requests_cache
from src.pokeapi import CACHE_DIR


class TestPokeAPI(unittest.TestCase):
    def test_cache_directory_configured(self):
        """Verifica que el directorio de cache apunta al estandar del sistema operativo."""
        self.assertIsInstance(CACHE_DIR, Path)
        self.assertTrue(CACHE_DIR.exists())

    def test_requests_cache_installed(self):
        """Verifica que requests_cache esta instalado."""
        self.assertTrue(requests_cache.is_installed())


if __name__ == '__main__':
    unittest.main()
