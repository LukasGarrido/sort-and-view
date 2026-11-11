"""
App Streamlit: visualiza paso a paso cómo Block Sort ordena los Pokémon.

Uso (desde la raíz del repo): streamlit run app.py
"""
import time

import pandas as pd
import streamlit as st

from src.block_sort import block_sort
from ui.controles import CARACTERISTICAS, mostrar_configuracion, mostrar_reproduccion
from ui.datos import cargar_datos
from ui.vistas import mostrar_leyenda, mostrar_paso

FPS_MAX = 20  # cuadros por segundo como máximo durante la reproducción


def generar_pasos(pokemones, campo, descendente, tam_bloque):
    """Ejecuta block_sort registrando cada evento; devuelve la lista de pasos.

    Cada paso es un dict: tipo, estado, info (datos del evento), fase (la fase
    activa: rango de bloque o fusión), marcados (posiciones que se comparan),
    corte (posición de la línea entre las dos mitades en una fusión) y los
    contadores acumulados de comparaciones y movimientos.

    `estado` es el estado *lógico* de la lista, sin las copias temporales que
    deja el algoritmo en el arreglo de trabajo:
    - En insertion sort, el elemento que se inserta se dibuja en el hueco
      que va dejando al desplazar los demás.
    - En la fusión, a partir de la posición de escritura se dibuja lo que
      queda en el búfer (mitad izquierda y luego mitad derecha).
    Así cada Pokémon aparece exactamente una vez en cada paso.
    """
    cuenta = {"comparar": 0, "mover": 0}

    def paso(tipo, estado, info, fase, marcados=(), corte=None):
        return {"tipo": tipo, "estado": estado, "info": info, "fase": fase,
                "marcados": set(marcados), "corte": corte,
                "comparaciones": cuenta["comparar"], "movimientos": cuenta["mover"]}

    pasos = [paso("inicio", list(pokemones), {}, None)]
    fase_actual = None
    en_mano = None             # insertion sort: elemento que se está insertando
    izq, der = [], []          # fusión: lo que queda en el búfer de cada mitad

    def vista_fusion(arr, escritos):
        """arr[:escritos] ya fusionado + búfer restante + resto del arreglo."""
        fin = fase_actual["fin"]
        return arr[:escritos] + izq + der + arr[fin:]

    def registrar(tipo, arr, **info):
        nonlocal fase_actual, en_mano, izq, der
        if tipo == "fase":
            fase_actual = info
            en_mano = None
            if info["nombre"] == "fusion":
                izq = arr[info["inicio"]:info["mitad"]]
                der = arr[info["mitad"]:info["fin"]]
                pasos.append(paso(tipo, list(arr), info, fase_actual, corte=info["mitad"]))
            else:
                pasos.append(paso(tipo, list(arr), info, fase_actual))
            return

        cuenta[tipo] += 1
        k = info["indice"]

        if fase_actual["nombre"] == "bloque":
            estado = list(arr)
            if tipo == "comparar":
                # Se compara arr[k] con el elemento en mano, que está en el hueco k+1
                en_mano = info["elemento"]
                estado[k + 1] = en_mano
                pasos.append(paso(tipo, estado, info, fase_actual, marcados=(k, k + 1)))
            else:
                if info["elemento"] is en_mano:   # el elemento llega a su sitio
                    en_mano = None
                else:                             # desplazamiento: el hueco pasa a k-1
                    estado[k - 1] = en_mano
                pasos.append(paso(tipo, estado, info, fase_actual))
            return

        # Fusión
        if tipo == "comparar":
            # Candidatos: primero de la izquierda (en k) y primero de la derecha
            pasos.append(paso(tipo, vista_fusion(arr, k), info, fase_actual,
                              marcados=(k, k + len(izq)), corte=k + len(izq)))
        else:
            if izq and izq[0] is info["elemento"]:
                izq = izq[1:]
            else:
                der = der[1:]
            pasos.append(paso(tipo, vista_fusion(arr, k + 1), info, fase_actual,
                              corte=k + 1 + len(izq)))

    ordenado = block_sort(pokemones, key=lambda p: p[campo], reverse=descendente,
                          tam_bloque=tam_bloque, registrar=registrar)
    pasos.append(paso("fin", ordenado, {}, None))
    return pasos


def _tabla_actual(paso, campo):
    """Tabla con los Pokémon en el orden del paso mostrado."""
    with st.expander("Ver la tabla de Pokémon en el orden actual"):
        st.dataframe(pd.DataFrame([
            {"Posición": i, "ID": p["id"], "Nombre": p["name"], "Tipo": p["tipo"],
             campo: p[campo]}
            for i, p in enumerate(paso["estado"])
        ]), hide_index=True, width="stretch")


def main():
    st.set_page_config(page_title="Pokedex Block Sort", page_icon="🔢", layout="wide")
    st.title("Pokedex Block Sort")
    st.caption("Visualiza paso a paso cómo Block Sort ordena los Pokémon.")

    datos = cargar_datos()
    if not datos:
        st.error("No se encontraron datos en data/pokemon.json.")
        st.stop()

    config = mostrar_configuracion(len(datos))

    if config["ordenar"]:
        st.session_state["pasos"] = generar_pasos(
            datos[:config["cantidad"]], config["campo"],
            config["descendente"], config["tam_bloque"],
        )
        st.session_state["campo"] = config["campo"]
        st.session_state["tam_bloque"] = config["tam_bloque"]
        st.session_state["paso"] = 0

    with st.sidebar:
        st.divider()
        mostrar_leyenda()

    pasos = st.session_state.get("pasos")
    if not pasos:
        st.info('Elige la configuración en la barra lateral y pulsa "Ordenar".')
        st.stop()

    # Si una reproducción anterior quedó a medias, retomamos desde ahí.
    if "_ir_a" in st.session_state:
        st.session_state["paso"] = st.session_state.pop("_ir_a")

    st.caption(f"{len(pasos)} pasos registrados")
    rep = mostrar_reproduccion(len(pasos))
    lienzo = st.empty()
    campo = st.session_state["campo"]
    etiqueta = {v: k for k, v in CARACTERISTICAS.items()}[campo]
    tam_bloque = st.session_state["tam_bloque"]

    def dibujar(i):
        with lienzo.container():
            mostrar_paso(pasos, i, campo, etiqueta, tam_bloque)

    if rep["reproducir"]:
        salto = max(1, rep["velocidad"] // FPS_MAX)
        pausa = salto / rep["velocidad"]
        inicio = st.session_state["paso"]
        if inicio >= len(pasos) - 1:  # ya estaba al final: empezar de nuevo
            inicio = 0
        for i in list(range(inicio, len(pasos), salto)) + [len(pasos) - 1]:
            st.session_state["_ir_a"] = i
            dibujar(i)
            time.sleep(pausa)
        st.rerun()

    dibujar(st.session_state["paso"])
    _tabla_actual(pasos[st.session_state["paso"]], campo)


main()
