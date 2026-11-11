"""
src/pokeapi.py

Cliente de la PokeAPI.
"""
import json
import requests
import requests_cache
from pathlib import Path
import platformdirs

CACHE_DIR = Path(platformdirs.user_cache_dir("pokedex-blocksort"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

requests_cache.install_cache(
    str(CACHE_DIR / "pokeapi_cache"), backend="sqlite", expire_after=86400
)

BASE_URL = "https://pokeapi.co/api/v2"


def listar_pokemon(limit=151):
    """Obtiene la lista de Pokemon (nombre y url)."""
    url = f"{BASE_URL}/pokemon?limit={limit}&offset=0"
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()["results"]
    except requests.RequestException as e:
        print(f"Error al listar Pokemon: {e}")
        return []


def detalle_pokemon(id_o_nombre):
    """Obtiene los datos crudos de un Pokemon por id o nombre."""
    url = f"{BASE_URL}/pokemon/{id_o_nombre}"
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException as e:
        print(f"Error al obtener {id_o_nombre}: {e}")
        return None


def all_pokemon(limit=151):
    """Devuelve la lista de Pokemon con los campos que se van a ordenar."""
    pokemones = []
    for item in listar_pokemon(limit):
        d = detalle_pokemon(item["name"])
        if d:
            pokemones.append({
                "id": d["id"],
                "name": d["name"],
                "height": d["height"],
                "weight": d["weight"],
                "base_experience": d["base_experience"] or 0,
                "tipo": d["types"][0]["type"]["name"],
            })
    return pokemones


JSON_PATH = Path(__file__).resolve().parent.parent / "data" / "pokemon.json"


def generar_json(limit=151, ruta=JSON_PATH):
    """Descarga los Pokemon de la API y los guarda en un JSON local."""
    pokemones = all_pokemon(limit)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(pokemones, indent=1), encoding="utf-8")
    return pokemones


def cargar_pokemon(ruta=JSON_PATH):
    """Lee los Pokemon del JSON local (sin llamar a la API)."""
    return json.loads(ruta.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(f"Guardados: {len(generar_json())} en {JSON_PATH}")
