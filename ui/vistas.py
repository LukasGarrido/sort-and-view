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

# Bloques chicos solo para la animacion (el algoritmo real usa TAM_BLOQUE = 32)
BLOQUE_ANIM = 8


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
    pasos = list(block_sort_detailed_steps(muestra, key=key_func, reverse=reverse, bloque=BLOQUE_ANIM))
    rank = {pos[id(p)]: r for r, p in enumerate(pasos[-1][0])}
    datos = {
        "items": [{"name": p["name"].capitalize(), "value": key_func(p), "rank": rank[k]} for k, p in enumerate(muestra)],
        "steps": [[pos[id(p)] for p in paso] for paso, _ in pasos],
        "anchos": [ancho for _, ancho in pasos],
        "bloque": BLOQUE_ANIM,
        "campo": campo,
    }
    html = (Path(__file__).parent / "animacion.html").read_text(encoding="utf-8")
    components.html(html.replace("__DATOS__", json.dumps(datos)), height=510)
    mostrar_explicacion_block_sort()


def mostrar_explicacion_block_sort():
    """Explica el algoritmo en texto, pensado para leerse junto a la animación."""
    st.markdown("---")
    st.subheader("¿Cómo funciona Block Sort?")
    st.markdown(
        f"""
Ordenar una lista chica es fácil; ordenar una grande cuesta más. **Block Sort** parte la lista en
bloques chicos, ordena cada uno y después los une de a pares hasta quedar con uno solo.

1. **Dividir.** La lista se corta en bloques de tamaño fijo (las franjas de la animación). Aquí son de
   {BLOQUE_ANIM} para que se vean varios; el programa usa {TAM_BLOQUE} por defecto.
2. **Ordenar cada bloque con *insertion sort*.** Se toma cada elemento y se desliza hacia atrás mientras
   el de su izquierda sea mayor. Es rápido en listas chicas. Es la **Fase 1** de la animación.
3. **Fusionar de a pares.** Dos bloques vecinos ya ordenados se juntan en uno: se compara el primero de
   cada lado y siempre se queda el menor. Cada pasada duplica el tamaño de los grupos
   ({BLOQUE_ANIM} → {2 * BLOQUE_ANIM} → {4 * BLOQUE_ANIM}…) hasta que queda un solo bloque. Es la **Fase 2**.

**Cómo leer la animación:** el color de cada barra es su lugar final (si todo sale bien, termina como un
arcoíris de izquierda a derecha), el borde blanco marca las barras que se están moviendo y las franjas
muestran los bloques o grupos.

**Propiedades**
- **Estable:** si dos Pokémon empatan en la característica elegida, conservan su orden original.
- **Costo:** insertion sort en un bloque de tamaño *b* hace del orden de *b²* comparaciones, y hay *n/b* bloques,
  o sea unas *n·b* en total. Las fusiones necesitan unas *n·log₂(n/b)*. Por eso el tamaño del bloque importa:
  uno muy chico hace muchas fusiones y uno muy grande hace demasiado insertion sort. En
  *Métricas de Benchmark* se ve el efecto.
- **Memoria:** al fusionar se copia temporalmente cada mitad. La animación lo muestra como deslizamientos
  dentro de la misma lista para que sea más fácil de seguir.
"""
    )


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
