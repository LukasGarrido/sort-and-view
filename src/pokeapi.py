"""
Cliente de la PokeAPI con soporte de caché.
"""

class PokeAPIClient:
    def __init__(self, cache_dir="./cache"):
        self.cache_dir = cache_dir

    def obtener_pokemon(self, pokemon_id):
        """Obtiene datos de un Pokémon desde la API o caché."""
        pass
