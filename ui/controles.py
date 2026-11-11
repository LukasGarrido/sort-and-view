"""
Controles de la interfaz:
- mostrar_configuracion(): qué ordenar y cómo (en la barra lateral) + botón "Ordenar".
- mostrar_reproduccion(): reproducir, velocidad y navegación paso a paso.
"""
import streamlit as st

# Etiqueta visible -> campo del diccionario de cada Pokémon
CARACTERISTICAS = {
    "Peso": "weight",
    "Altura": "height",
    "Experiencia base": "base_experience",
    "Nombre": "name",
    "ID": "id",
}
TAMANOS_BLOQUE = [4, 8, 16, 32]
VELOCIDADES = [1, 2, 5, 10, 25, 50, 100, 250, 500]  # pasos por segundo


def mostrar_configuracion(total_pokemon):
    """Dibuja la configuración en la barra lateral.

    Devuelve un dict con: campo, descendente, cantidad, tam_bloque, ordenar
    (ordenar es True solo en la ejecución en que se pulsó el botón).
    """
    with st.sidebar:
        st.header("Configuración")
        etiqueta = st.selectbox("Característica", list(CARACTERISTICAS))
        sentido = st.radio("Sentido", ["Ascendente", "Descendente"], horizontal=True)
        cantidad = st.slider("Cantidad de Pokémon", 10, total_pokemon, min(24, total_pokemon))
        tam_bloque = st.select_slider("Tamaño de bloque", TAMANOS_BLOQUE, value=8,
                                      help="Block Sort ordena bloques de este tamaño con "
                                           "insertion sort y luego los fusiona de a pares.")
        ordenar = st.button("Ordenar", type="primary", width="stretch")

    return {
        "campo": CARACTERISTICAS[etiqueta],
        "descendente": sentido == "Descendente",
        "cantidad": cantidad,
        "tam_bloque": tam_bloque,
        "ordenar": ordenar,
    }


def _mover_paso(delta, total):
    """Callback de los botones ◀ ▶: mueve el paso actual sin salirse del rango."""
    st.session_state["paso"] = max(0, min(total - 1, st.session_state["paso"] + delta))


def mostrar_reproduccion(total_pasos):
    """Dibuja los controles de reproducción. El paso actual vive en
    st.session_state["paso"] (lo comparten el slider y los botones ◀ ▶).

    Devuelve un dict con: reproducir (bool), velocidad (pasos por segundo).
    """
    st.session_state.setdefault("paso", 0)
    ultimo = total_pasos - 1

    col_play, col_vel, col_ant, col_sig = st.columns([2, 4, 1, 1], vertical_alignment="bottom")
    with col_play:
        reproducir = st.button("▶ Reproducir", type="primary", width="stretch")
    with col_vel:
        velocidad = st.select_slider("Velocidad (pasos/seg)", VELOCIDADES, value=25)
    with col_ant:
        st.button("◀", width="stretch", on_click=_mover_paso, args=(-1, total_pasos),
                  disabled=st.session_state["paso"] <= 0, help="Paso anterior")
    with col_sig:
        st.button("▶", width="stretch", on_click=_mover_paso, args=(1, total_pasos),
                  disabled=st.session_state["paso"] >= ultimo, help="Paso siguiente")

    st.slider("Paso", 0, ultimo, key="paso")

    return {"reproducir": reproducir, "velocidad": velocidad}
