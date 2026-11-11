"""
Vistas y renderizado de componentes para la app de Streamlit.
"""
import streamlit as st
import pandas as pd
import base64
import inspect
import json
import random
from pathlib import Path
import streamlit.components.v1 as components
from src.benchmark import ejecutar_benchmark
from src.block_sort import TAM_BLOQUE, _insertion_sort, _merge, block_sort, block_sort_detailed_steps

# Bloques chicos solo para la animacion (el algoritmo real usa TAM_BLOQUE = 32)
BLOQUE_ANIM = 8
MIN_ANIM = 25  # minimo de datos pedido por la rubrica
SPRITES = Path(__file__).resolve().parent.parent / "data" / "sprites"


@st.cache_data
def _sprite(id_pokemon):
    """Sprite del Pokemon como data URI (el iframe de la animacion no puede leer archivos locales)."""
    ruta = SPRITES / f"{id_pokemon}.png"
    if not ruta.exists():
        return ""
    return "data:image/png;base64," + base64.b64encode(ruta.read_bytes()).decode()


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

    if len(pokemones) < MIN_ANIM:
        st.warning(f"La animación necesita al menos {MIN_ANIM} Pokémon y con el filtro actual hay {len(pokemones)}. Quita o cambia el filtro.")
        return

    col1, col2 = st.columns([3, 1])
    tam = col1.slider("Cantidad de elementos", min_value=MIN_ANIM, max_value=min(40, len(pokemones)), value=MIN_ANIM, step=1, key="anim_tam_simple")
    if col2.button("Mezclar de nuevo") or "anim_seed" not in st.session_state:
        st.session_state["anim_seed"] = random.random()

    muestra = list(pokemones[:tam])
    random.Random(st.session_state["anim_seed"]).shuffle(muestra)
    key_func = lambda p: p.get(campo, 0)

    pos = {id(p): k for k, p in enumerate(muestra)}
    pasos = list(block_sort_detailed_steps(muestra, key=key_func, reverse=reverse, bloque=BLOQUE_ANIM))
    rank = {pos[id(p)]: r for r, p in enumerate(pasos[-1][0])}
    datos = {
        "items": [{"name": p["name"].capitalize(), "value": key_func(p), "rank": rank[k], "img": _sprite(p.get("id"))} for k, p in enumerate(muestra)],
        "steps": [[pos[id(p)] for p in paso] for paso, _, _ in pasos],
        "anchos": [ancho for _, ancho, _ in pasos],
        "cmps": [cmp for _, _, cmp in pasos],
        "bloque": BLOQUE_ANIM,
        "campo": campo,
    }
    html = (Path(__file__).parent / "animacion.html").read_text(encoding="utf-8")
    components.html(html.replace("__DATOS__", json.dumps(datos)), height=610)
    mostrar_explicacion_block_sort()


def mostrar_explicacion_block_sort():
    """Muestra el código real de src/block_sort.py, por función, para leerlo junto a la animación."""
    st.markdown("---")
    st.subheader("Código del algoritmo")
    st.caption(
        f"Es el código de `src/block_sort.py`. La animación usa bloques de {BLOQUE_ANIM} para que se vean varios; "
        f"`block_sort` usa {TAM_BLOQUE} por defecto."
    )
    tabs = st.tabs(["block_sort (principal)", "Fase 1: _insertion_sort", "Fase 2: _merge"])
    partes = [
        (block_sort, "Orquesta todo: parte la lista en bloques, llama a `_insertion_sort` en cada uno y luego "
                     "fusiona de a pares con `_merge`, duplicando el ancho (`width`) en cada pasada hasta quedar un solo bloque."),
        (_insertion_sort, "Ordena un bloque: toma cada elemento y lo desliza hacia atrás mientras el de su "
                          "izquierda sea mayor. La comparación es estricta, por eso no cruza elementos iguales (estabilidad)."),
        (_merge, "Junta dos mitades ya ordenadas: copia cada una a un búfer, compara el primero de cada lado y "
                 "coloca el menor. Con `<=` gana el de la izquierda en los empates (estabilidad)."),
    ]
    for tab, (fn, texto) in zip(tabs, partes):
        with tab:
            st.markdown(texto)
            st.code(inspect.getsource(fn), language="python")


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

    df_bench = pd.DataFrame(filas, columns=["Campo", "Bloque", "Tamaño (n)", "Tiempo (s)", "Comparaciones"])
    df_bench["Tiempo (µs)"] = df_bench["Tiempo (s)"] * 1e6

    campo_sel = st.selectbox("Filtrar benchmark por campo:", df_bench["Campo"].unique())
    df_campo = df_bench[df_bench["Campo"] == campo_sel]

    st.markdown("### Efecto del tamaño de lista (una línea por tamaño de bloque)")
    col1, col2 = st.columns(2)
    for col, metrica in ((col1, "Tiempo (µs)"), (col2, "Comparaciones")):
        tabla = df_campo.pivot(index="Tamaño (n)", columns="Bloque", values=metrica)
        tabla.columns = [f"Bloque {b:02d}" for b in tabla.columns]
        col.markdown(f"#### {metrica} - {campo_sel}")
        col.line_chart(tabla, x_label="Cantidad de elementos (n)", y_label=metrica)

    n_max = df_campo["Tamaño (n)"].max()
    st.markdown(f"### Efecto del tamaño de bloque (n = {n_max})")
    st.caption(
        "Con bloques chicos hay más fusiones; con bloques grandes, más insertion sort. "
        "Si el bloque es mayor que n, todo el trabajo lo hace insertion sort."
    )
    df_n = df_campo[df_campo["Tamaño (n)"] == n_max]
    col3, col4 = st.columns(2)
    for col, metrica in ((col3, "Tiempo (µs)"), (col4, "Comparaciones")):
        col.markdown(f"#### {metrica} - {campo_sel}")
        col.line_chart(df_n, x="Bloque", y=metrica, x_label="Tamaño de bloque", y_label=metrica)

    st.markdown("### Tabla detallada de Benchmark")
    st.dataframe(df_bench.drop(columns="Tiempo (s)"), use_container_width=True, hide_index=True)
