"""
Vistas y renderizado de componentes para la app de Streamlit.
"""
import streamlit as st
import pandas as pd
import time
import random
import altair as alt
from src.benchmark import ejecutar_benchmark
from src.block_sort import block_sort_detailed_steps


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


def mostrar_animacion_ordenamiento(pokemones, campo):
    """Muestra una animación detallada y paso a paso del algoritmo Block Sort con nombres de Pokémon en el eje X."""
    st.subheader("Visualizador Animado y Detallado de Block Sort")
    st.markdown(
        "Seleccione la cantidad de elementos y pulse el boton para iniciar. "
        "Cada barra muestra el nombre del Pokemon en el eje X y tiene un color unico para que pueda rastrear "
        "cómo se desplaza y se ubica en su posicion correcta paso a paso."
    )

    if not pokemones:
        st.warning("No hay datos disponibles para animar.")
        return

    col1, col2 = st.columns(2)
    with col1:
        tam_muestra = st.slider("Cantidad de elementos", min_value=10, max_value=min(40, len(pokemones)), value=20, step=5, key="anim_tam_simple")
    with col2:
        velocidad = st.slider("Velocidad de animacion (segundos por paso)", min_value=0.05, max_value=0.8, value=0.25, step=0.05, key="anim_vel_simple")

    key_func = lambda p: p.get(campo, 0)

    if "anim_started" not in st.session_state:
        st.session_state["anim_started"] = False
    if "anim_step" not in st.session_state:
        st.session_state["anim_step"] = 0
    if "anim_steps_list" not in st.session_state:
        st.session_state["anim_steps_list"] = []

    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("Iniciar Animacion Detallada"):
        muestra = list(pokemones[:tam_muestra])
        random.shuffle(muestra)
        st.session_state["anim_steps_list"] = list(block_sort_detailed_steps(muestra, key=key_func))
        st.session_state["anim_step"] = 0
        st.session_state["anim_started"] = True
        st.rerun()

    if col_btn2.button("Detener Animacion"):
        st.session_state["anim_started"] = False
        st.rerun()

    if st.session_state.get("anim_started", False):
        steps = st.session_state["anim_steps_list"]
        step_idx = st.session_state["anim_step"]
        total = len(steps) - 1 if len(steps) > 1 else 0

        if total > 0:
            progreso = min(step_idx / total, 1.0)
            st.progress(progreso, text=f"Paso detallado {step_idx} de {total}")

            if step_idx == 0:
                st.info("Estado inicial aleatorio (desordenado). Las barras comenzaran a moverse...")
            elif step_idx <= total // 2:
                st.info("Recorrido activo: Ordenando bloques locales mediante insercion paso a paso.")
            else:
                st.info("Recorrido activo: Fusionando (Merge) bloques ordenados.")

            paso_actual = steps[step_idx]
            
            df_paso = pd.DataFrame({
                "Posicion": list(range(len(paso_actual))),
                "Valor": [p.get(campo, 0) for p in paso_actual],
                "Pokemon": [p.get("name", "").capitalize() for p in paso_actual]
            })

            # Gráfico con Altair mostrando los nombres de los Pokémon en el eje X y colores persistentes
            chart = alt.Chart(df_paso).mark_bar().encode(
                x=alt.X("Pokemon:N", title="Pokemon", sort=list(df_paso["Pokemon"])),
                y=alt.Y("Valor:Q", title=f"Valor ({campo})"),
                color=alt.Color("Pokemon:N", legend=None, scale=alt.Scale(scheme="category20")),
                tooltip=["Posicion", "Pokemon", "Valor"]
            ).properties(height=380)

            st.altair_chart(chart, use_container_width=True)

            with st.expander("Ver detalle de elementos en este micro-paso"):
                st.dataframe(df_paso[["Posicion", "Pokemon", "Valor"]], hide_index=True, use_container_width=True)

            if step_idx < total:
                time.sleep(velocidad)
                st.session_state["anim_step"] += 1
                st.rerun()
            else:
                st.session_state["anim_started"] = False
                st.success("¡Recorrido y ordenamiento completado con exito!")


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
