"""
Vistas y renderizado de componentes para la app de Streamlit.
"""
import streamlit as st
import pandas as pd
import json
import random
from pathlib import Path
import streamlit.components.v1 as components
from src.benchmark import ejecutar_benchmark
from src.block_sort import TAM_BLOQUE, block_sort_detailed_steps


@st.cache_data
def obtener_benchmark_cacheado():
    """Ejecuta y cachea el benchmark de block_sort."""
    return ejecutar_benchmark()


def mostrar_metricas_generales(pokemones):
    """Muestra métricas resumen de los Pokémon filtrados."""
    if not pokemones:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pokemon", len(pokemones))
    with col2:
        prom_alt = sum(p.get("height", 0) for p in pokemones) / len(pokemones)
        st.metric("Altura Promedio", f"{prom_alt:.1f} dm")
    with col3:
        prom_peso = sum(p.get("weight", 0) for p in pokemones) / len(pokemones)
        st.metric("Peso Promedio", f"{prom_peso:.1f} hg")
    with col4:
        prom_exp = sum(p.get("base_experience", 0) for p in pokemones) / len(pokemones)
        st.metric("Exp. Base Prom.", f"{prom_exp:.1f}")


def mostrar_listado(pokemones, campo_orden):
    """Muestra la tabla de Pokémon ordenados."""
    st.subheader("Listado de Pokemon Ordenados con Block Sort")
    
    if not pokemones:
        st.warning("No se encontraron Pokemon con los filtros seleccionados.")
        return

    mostrar_metricas_generales(pokemones)
    st.markdown("---")

    datos_tabla = []
    for p in pokemones:
        datos_tabla.append({
            "ID": p.get("id"),
            "Nombre": p.get("name").capitalize(),
            "Tipo": p.get("tipo", "N/A").capitalize(),
            "Altura (dm)": p.get("height"),
            "Peso (hg)": p.get("weight"),
            "Exp. Base": p.get("base_experience")
        })

    df = pd.DataFrame(datos_tabla)
    st.dataframe(df, use_container_width=True, hide_index=True)


def mostrar_animacion_ordenamiento(pokemones, campo, reverse=False):
    """Animación de Block Sort: los pasos se calculan aquí y se reproducen en el navegador (ui/animacion.html)."""
    st.subheader("Visualizador Animado de Block Sort")

    if not pokemones:
        st.warning("No hay datos disponibles para animar.")
        return

    col1, col2 = st.columns([3, 1])
    tam = col1.slider("Cantidad de elementos", min_value=10, max_value=min(40, len(pokemones)), value=20, step=5, key="anim_tam_simple")
    if col2.button("Mezclar de nuevo") or "anim_seed" not in st.session_state:
        st.session_state["anim_seed"] = random.random()

    muestra = list(pokemones[:tam])
    random.Random(st.session_state["anim_seed"]).shuffle(muestra)
    key_func = lambda p: p.get(campo, 0)

    pos = {id(p): k for k, p in enumerate(muestra)}
    pasos = list(block_sort_detailed_steps(muestra, key=key_func, reverse=reverse))
    # pasos de insercion = suma de los de cada bloque; el resto es fusion
    fase1 = sum(
        len(list(block_sort_detailed_steps(muestra[i:i + TAM_BLOQUE], key=key_func, reverse=reverse))) - 1
        for i in range(0, tam, TAM_BLOQUE)
    )
    # se descartan los pasos repetidos (el generador cede el mismo estado dos veces)
    unicos = [(0, pasos[0])] + [(k, b) for k, (a, b) in enumerate(zip(pasos, pasos[1:]), 1) if a != b]
    rank = {pos[id(p)]: r for r, p in enumerate(pasos[-1])}
    datos = {
        "items": [{"name": p["name"].capitalize(), "value": key_func(p), "rank": rank[k]} for k, p in enumerate(muestra)],
        "steps": [[pos[id(p)] for p in paso] for _, paso in unicos],
        "fase1": sum(1 for k, _ in unicos if k <= fase1) - 1,
        "bloque": TAM_BLOQUE,
        "campo": campo,
    }
    html = (Path(__file__).parent / "animacion.html").read_text(encoding="utf-8")
    components.html(html.replace("__DATOS__", json.dumps(datos)), height=510)


def mostrar_benchmark():
    """Muestra la vista de benchmark y rendimiento de block_sort."""
    st.subheader("Rendimiento del Algoritmo Block Sort (Benchmark)")
    st.markdown(
        r"Esta sección mide el rendimiento del algoritmo **Block Sort** implementado en `src/block_sort.py` "
        r"en términos de tiempo de ejecución ($\mu s$) y número de comparaciones para diferentes tamaños de dataset ($n$) "
        r"y características de los Pokémon."
    )

    with st.spinner("Ejecutando benchmarks..."):
        filas = obtener_benchmark_cacheado()

    df_bench = pd.DataFrame(filas, columns=["Campo", "Tamaño (n)", "Tiempo (s)", "Comparaciones"])
    df_bench[r"Tiempo ($\mu$s)"] = df_bench["Tiempo (s)"] * 1e6

    campo_sel = st.selectbox("Filtrar benchmark por campo:", df_bench["Campo"].unique())
    df_filtrado = df_bench[df_bench["Campo"] == campo_sel]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(rf"#### Tiempo de Ejecución ($\mu s$) - {campo_sel}")
        st.bar_chart(df_filtrado.set_index("Tamaño (n)")[r"Tiempo ($\mu$s)"])

    with col2:
        st.markdown(rf"#### Número de Comparaciones - {campo_sel}")
        st.bar_chart(df_filtrado.set_index("Tamaño (n)")["Comparaciones"])

    st.markdown("### Tabla detallada de Benchmark")
    st.dataframe(df_bench, use_container_width=True, hide_index=True)
