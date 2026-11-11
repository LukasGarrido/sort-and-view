"""
Carga de datos para la interfaz (desde el JSON local, sin llamar a la API).
"""
import streamlit as st

from src.pokeapi import cargar_pokemon


@st.cache_data
def cargar_datos():
    """Devuelve la lista de Pokémon, cacheada entre ejecuciones de Streamlit."""
    return cargar_pokemon()
