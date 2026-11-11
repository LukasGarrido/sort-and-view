"""
Vistas de la interfaz:
- mostrar_paso(): gráfico de barras animable de un paso de Block Sort
  (colores por tipo, resaltado de comparaciones/movimientos, fase activa).
- mostrar_tablas(): tablas "Original" y "Ordenado" en dos columnas.
"""
import altair as alt
import pandas as pd
import streamlit as st

COLUMNAS = ["id", "name", "tipo", "height", "weight", "base_experience"]
RESALTADO = "background-color: rgba(255, 75, 75, 0.18); font-weight: bold"

COLOR_TIPO = {
    "normal": "#A8A77A", "fire": "#EE8130", "water": "#6390F0", "electric": "#F7D02C",
    "grass": "#7AC74C", "ice": "#96D9D6", "fighting": "#C22E28", "poison": "#A33EA1",
    "ground": "#E2BF65", "flying": "#A98FF3", "psychic": "#F95587", "bug": "#A6B91A",
    "rock": "#B6A136", "ghost": "#735797", "dragon": "#6F35FC", "dark": "#705746",
    "steel": "#B7B7CE", "fairy": "#D685AD",
}
TIPO_ES = {
    "normal": "Normal", "fire": "Fuego", "water": "Agua", "electric": "Eléctrico",
    "grass": "Planta", "ice": "Hielo", "fighting": "Lucha", "poison": "Veneno",
    "ground": "Tierra", "flying": "Volador", "psychic": "Psíquico", "bug": "Bicho",
    "rock": "Roca", "ghost": "Fantasma", "dragon": "Dragón", "dark": "Siniestro",
    "steel": "Acero", "fairy": "Hada",
}
# Color de resaltado según el estado de cada barra en el paso actual
ESTADOS = {
    "Comparando": "#FFD400",
    "Movimiento": "#FF2BD6",
    "Ordenado": "#2ECC71",
}
MAX_ETIQUETAS = 40  # con más barras se ocultan los nombres del eje X
NOMBRE_FASE = {"bloque": "Fase 1 · insertion sort en bloque", "fusion": "Fase 2 · fusionando"}


def _estado(pos, paso):
    """Estado de la barra en la posición `pos` para el paso dado."""
    tipo, info = paso["tipo"], paso["info"]
    if tipo == "fin":
        return "Ordenado"
    if tipo == "mover" and pos == info["indice"]:
        return "Movimiento"
    if tipo == "comparar" and pos in paso.get("marcados", ()):
        # Posiciones calculadas en generar_pasos: en insertion sort, arr[indice] y
        # el elemento en mano; en la fusión, los dos candidatos del búfer.
        return "Comparando"
    return "Normal"


def describir_paso(paso):
    """Texto corto que explica qué ocurre en el paso."""
    tipo, info, fase = paso["tipo"], paso["info"], paso["fase"]
    if tipo == "inicio":
        return "Lista original, sin ordenar"
    if tipo == "fin":
        return "¡Ordenamiento completo!"
    titulo = ""
    if fase:
        titulo = f"{NOMBRE_FASE[fase['nombre']]} [{fase['inicio']}..{fase['fin'] - 1}]"
        if fase["mitad"] is not None:
            titulo = (f"{NOMBRE_FASE['fusion']} [{fase['inicio']}..{fase['mitad'] - 1}]"
                      f" + [{fase['mitad']}..{fase['fin'] - 1}]")
    if tipo == "comparar":
        return f"{titulo} → comparando {info['elemento']['name']} con {info['otro']['name']}"
    if tipo == "mover":
        return f"{titulo} → {info['elemento']['name']} se escribe en la posición {info['indice']}"
    return titulo


def _grafico(paso, campo, etiqueta, tam_bloque, max_valor, rangos=None):
    estado_lista = paso["estado"]
    n = len(estado_lista)
    fase = paso["fase"]
    inicio, fin = (fase["inicio"], fase["fin"]) if fase else (0, n)

    if campo == "name":
        # Los nombres no son numéricos: la altura es su posición alfabética
        # (calculada una vez con la lista inicial, para que no cambie entre pasos)
        valor = lambda p: rangos[p["name"]]
    else:
        valor = lambda p: p[campo]

    filas = []
    for pos, p in enumerate(estado_lista):
        est = _estado(pos, paso)
        color_tipo = COLOR_TIPO.get(p["tipo"], "#999999")
        filas.append({
            "pos": pos,
            "nombre": p["name"].capitalize(),
            "pokedex": f"#{p['id']:03d}",
            "tipo": TIPO_ES.get(p["tipo"], p["tipo"]),
            "valor": valor(p),
            "dato": p[campo],
            "bloque": pos // tam_bloque,
            "estado": est,
            "color": ESTADOS.get(est, color_tipo),
            "borde": "#000000" if est != "Normal" else color_tipo,
            "activo": 1.0 if inicio <= pos < fin else 0.3,
        })
    df = pd.DataFrame(filas)

    # Eje por posición (las barras no se reordenan solas); el nombre va de etiqueta
    nombres = [f"{f['pos']:02d} {f['nombre']}".replace("\\", "").replace("'", "\\'")
               for f in filas]
    label_expr = "[" + ",".join(f"'{e}'" for e in nombres) + "][datum.value]"
    if n <= MAX_ETIQUETAS:
        eje = alt.Axis(labelAngle=-65, labelFontSize=10, labelOverlap=False,
                       labelExpr=label_expr)
    else:  # demasiadas barras: sin nombres (siguen en el tooltip)
        eje = alt.Axis(labels=False, ticks=False)
    titulo_x = None if n <= MAX_ETIQUETAS else "Posición (pasa el ratón por una barra para ver el Pokémon)"
    x = alt.X("pos:O", title=titulo_x, scale=alt.Scale(domain=list(range(n))), axis=eje)
    barras = alt.Chart(df).mark_bar(strokeWidth=1.5).encode(
        x=x,
        y=alt.Y("valor:Q", title=etiqueta, scale=alt.Scale(domain=[0, max_valor * 1.08])),
        color=alt.Color("color:N", scale=None),
        stroke=alt.Stroke("borde:N", scale=None),
        opacity=alt.Opacity("activo:Q", scale=None),
        tooltip=[
            alt.Tooltip("nombre:N", title="Pokémon"),
            alt.Tooltip("pokedex:N", title="Pokédex"),
            alt.Tooltip("tipo:N", title="Tipo"),
            alt.Tooltip("dato:N", title=etiqueta),
            alt.Tooltip("pos:Q", title="Posición"),
            alt.Tooltip("bloque:Q", title="Bloque"),
            alt.Tooltip("estado:N", title="Estado"),
        ],
    )
    capas = [barras]
    if campo != "name" and n <= 60:
        capas.append(alt.Chart(df).mark_text(dy=-6, fontSize=9, color="#8A8F98").encode(
            x=x, y="valor:Q", text=alt.Text("valor:Q", format="~g"),
            opacity=alt.Opacity("activo:Q", scale=None),
        ))

    # Línea que separa las dos mitades durante una fusión
    if paso.get("corte") is not None and paso["corte"] < n:
        corte = pd.DataFrame({"pos": [paso["corte"]]})
        capas.append(alt.Chart(corte).mark_rule(color="#1E88E5", strokeWidth=2,
                                                strokeDash=[6, 3], xOffset=-6).encode(x=x))

    return alt.layer(*capas).properties(height=460)


def mostrar_leyenda():
    """Leyenda de colores de estado (para la barra lateral)."""
    st.markdown("**Leyenda**")
    for nombre, color in ESTADOS.items():
        st.markdown(f"<span style='color:{color};font-size:1.2em'>■</span> {nombre}",
                    unsafe_allow_html=True)
    st.caption("El resto de barras usa el color de su tipo. Las barras atenuadas "
               "están fuera del bloque o fusión en curso. La línea azul punteada "
               "separa las dos mitades que se fusionan.")


def mostrar_paso(pasos, indice, campo, etiqueta, tam_bloque):
    """Dibuja el paso `indice`: descripción, métricas acumuladas y gráfico."""
    paso = pasos[indice]
    total = len(pasos) - 1
    rangos = None
    if campo == "name":
        nombres = sorted({p["name"] for p in pasos[0]["estado"]})
        rangos = {v: i + 1 for i, v in enumerate(nombres)}
        max_valor = len(nombres)
    else:
        max_valor = max(p[campo] for p in pasos[0]["estado"]) or 1

    st.markdown(f"**Paso {indice}/{total}** — {describir_paso(paso)}")
    m1, m2, m3 = st.columns(3)
    m1.metric("Comparaciones", paso.get("comparaciones", 0))
    m2.metric("Movimientos", paso.get("movimientos", 0))
    m3.metric("Tamaño de bloque", tam_bloque)
    st.altair_chart(_grafico(paso, campo, etiqueta, tam_bloque, max_valor, rangos), width="stretch")


def _tabla(pokemones, campo=None):
    """Muestra una lista de Pokémon como tabla, resaltando la columna `campo`."""
    df = pd.DataFrame(pokemones, columns=COLUMNAS)
    datos = df.style.map(lambda _: RESALTADO, subset=[campo]) if campo else df
    st.dataframe(datos, hide_index=True, width="stretch")


def mostrar_tablas(original, ordenado=None, campo=None):
    """Dibuja dos columnas: la lista original y la lista ordenada por `campo`.

    Si `ordenado` es None (todavía no se pulsó "Ordenar"), la columna
    derecha muestra un mensaje de espera.
    """
    col_original, col_ordenado = st.columns(2)

    with col_original:
        st.subheader("Original")
        st.caption(f"{len(original)} Pokémon en el orden del dataset")
        _tabla(original)

    with col_ordenado:
        st.subheader("Ordenado")
        if ordenado is None:
            st.info('Elige una característica y pulsa "Ordenar".')
        else:
            st.caption(f"Ordenado con Block Sort por `{campo}`")
            _tabla(ordenado, campo)
