"""
Aplicación principal de Streamlit para el visor de Pokémon y Block Sort.
"""
import streamlit as st
from ui.datos import cargar_datos, obtener_tipos_disponibles, filtrar_y_ordenar
from ui.controles import renderizar_controles
from ui.vistas import mostrar_listado, mostrar_animacion_ordenamiento, mostrar_benchmark


def main():
    st.set_page_config(
        page_title="Pokedex Block Sort",
        layout="wide"
    )

    st.title("Pokedex con Algoritmo Block Sort")
    st.markdown(
        "Explora y ordena el dataset de Pokémon utilizando el algoritmo de ordenamiento híbrido **Block Sort**, "
        "visualiza la animación paso a paso de su funcionamiento y analiza sus métricas de rendimiento."
    )

    # Cargar datos
    pokemones = cargar_datos()
    if not pokemones:
        st.error("No se pudieron cargar los datos de los Pokémon. Verifique data/pokemon.json o la conexión a la API.")
        return

    tipos = obtener_tipos_disponibles(pokemones)

    # Renderizar controles en la barra lateral
    controles = renderizar_controles(tipos)

    # Filtrar y ordenar datos según controles
    pokemones_filtrados = filtrar_y_ordenar(
        pokemones,
        busqueda=controles["busqueda"],
        tipo=controles["tipo"],
        campo=controles["campo"],
        reverse=controles["reverse"]
    )

    # Navegación entre vistas
    if controles["vista"] == "Listado de Pokemon":
        mostrar_listado(pokemones_filtrados, controles["campo"])
    elif controles["vista"] == "Animacion de Ordenamiento":
        mostrar_animacion_ordenamiento(pokemones_filtrados, controles["campo"])
    else:
        mostrar_benchmark()


if __name__ == "__main__":
    main()
