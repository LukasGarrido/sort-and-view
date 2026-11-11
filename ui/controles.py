"""
Componentes de control y filtros en la barra lateral (Sidebar) de Streamlit.
"""
import streamlit as st


def renderizar_controles(tipos_disponibles):
    """Renderiza los controles de filtrado y ordenamiento en la barra lateral."""
    st.sidebar.header("Filtros y Ordenamiento")

    busqueda = st.sidebar.text_input("Buscar Pokemon por nombre", value="")

    opciones_tipo = ["Todos"] + tipos_disponibles
    tipo_seleccionado = st.sidebar.selectbox("Filtrar por tipo", opciones_tipo)

    st.sidebar.markdown("---")
    st.sidebar.header("Ordenamiento (Block Sort)")

    campos_disponibles = {
        "ID": "id",
        "Nombre": "name",
        "Altura": "height",
        "Peso": "weight",
        "Experiencia Base": "base_experience"
    }
    campo_etiqueta = st.sidebar.selectbox("Ordenar por caracteristica", list(campos_disponibles.keys()))
    campo_seleccionado = campos_disponibles[campo_etiqueta]

    reverse = st.sidebar.checkbox("Orden descendente (Reverse)", value=False)

    st.sidebar.markdown("---")
    vista = st.sidebar.radio("Navegacion", [
        "Listado de Pokemon",
        "Animacion de Ordenamiento",
        "Metricas de Benchmark (Block Sort)"
    ])

    return {
        "busqueda": busqueda,
        "tipo": tipo_seleccionado,
        "campo": campo_seleccionado,
        "reverse": reverse,
        "vista": vista
    }
