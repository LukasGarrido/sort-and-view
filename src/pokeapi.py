"""
src/pokeapi.py

Cliente y procesador de datos de Pokémon (usando la API y el dataset local data/pokemon.json).
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
JSON_PATH = Path(__file__).resolve().parent.parent / "data" / "pokemon.json"


def listar_pokemon(limit=151):
    """Obtiene la lista de Pokemon (nombre y url) desde la API."""
    url = f"{BASE_URL}/pokemon?limit={limit}&offset=0"
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()["results"]
    except requests.RequestException as e:
        print(f"Error al listar Pokemon: {e}")
        return []


def detalle_pokemon(id_o_nombre):
    """Obtiene los datos crudos de un Pokemon por id o nombre desde la API."""
    url = f"{BASE_URL}/pokemon/{id_o_nombre}"
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException as e:
        print(f"Error al obtener {id_o_nombre}: {e}")
        return None


def cargar_pokemon(ruta=JSON_PATH):
    """Lee y devuelve los Pokémon del JSON local (data/pokemon.json)."""
    if not ruta.exists():
        return []
    return json.loads(ruta.read_text(encoding="utf-8"))


def all_pokemon(limit=151):
    """Devuelve la lista de Pokémon procesada.
    Prioriza cargar el conjunto de datos local de data/pokemon.json si existe.
    Si no existe, consulta la API remota.
    """
    if JSON_PATH.exists():
        pokemones = cargar_pokemon(JSON_PATH)
        if pokemones:
            return pokemones[:limit]

    # Fallback a la API si el JSON local no está disponible
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


def generar_json(limit=151, ruta=JSON_PATH):
    """Descarga los Pokémon de la API y los guarda en el JSON local."""
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
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(pokemones, indent=1), encoding="utf-8")
    return pokemones


def filtrar_por_tipo(tipo, ruta=JSON_PATH):
    """Filtra el conjunto de datos de Pokémon locales por tipo."""
    pokemones = cargar_pokemon(ruta)
    if not tipo:
        return pokemones
    return [p for p in pokemones if p.get("tipo", "").lower() == tipo.lower()]


def buscar_pokemon(nombre, ruta=JSON_PATH):
    """Busca Pokémon en el conjunto de datos local cuyo nombre coincida parcialmente."""
    pokemones = cargar_pokemon(ruta)
    if not nombre:
        return pokemones
    query = nombre.lower()
    return [p for p in pokemones if query in p.get("name", "").lower()]


if __name__ == "__main__":
    pokemones = all_pokemon(20)
    print(f"Total cargados desde dataset local: {len(pokemones)}")
    for p in pokemones[:5]:
        print(p)
