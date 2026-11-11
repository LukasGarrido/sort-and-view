"""
Carga y procesamiento de datos para la interfaz de Streamlit.
"""
import streamlit as st
from src.pokeapi import cargar_pokemon
from src.block_sort import block_sort


@st.cache_data
def cargar_datos():
    """Devuelve la lista de Pokémon, cacheada entre ejecuciones de Streamlit."""
    return cargar_pokemon()


def obtener_tipos_disponibles(pokemones):
    """Extrae los tipos únicos de la lista de Pokémon."""
    tipos = set(p.get("tipo", "unknown") for p in pokemones if p.get("tipo"))
    return sorted(list(tipos))


def filtrar_y_ordenar(pokemones, busqueda="", tipo="", campo="id", reverse=False):
    """Filtra por búsqueda y tipo, y luego ordena usando block_sort."""
    resultado = pokemones

    if tipo and tipo != "Todos":
        resultado = [p for p in resultado if p.get("tipo", "").lower() == tipo.lower()]

    if busqueda:
        query = busqueda.lower()
        resultado = [p for p in resultado if query in p.get("name", "").lower()]

    key_func = lambda p: p.get(campo, 0)

    return block_sort(resultado, key=key_func, reverse=reverse)
