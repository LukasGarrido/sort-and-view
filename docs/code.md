# Pokedex Block Sort: Arquitectura y Diseño del Código

Este documento explica en profundidad la arquitectura del proyecto **Pokedex Block Sort**: la estructura de directorios, la responsabilidad de cada módulo, el funcionamiento interno del algoritmo de ordenamiento, la capa de datos con la PokéAPI, la interfaz de usuario en Streamlit y la suite de pruebas unitarias.

---

## 1. Estructura del Proyecto

```text
C:\Users\lukas\Desktop\Projects\sort-and-view\
├── app.py                  # Punto de entrada de la aplicación Streamlit
├── requirements.txt        # Dependencias de Python
├── README.md               # Descripción general del proyecto
├── data\
│   ├── pokemon.json        # Dataset estático local (151 Pokémon)
│   └── sprites\            # Sprites gráficos en PNG por ID de Pokémon
├── docs\
│   ├── code.md             # Documentación técnica y arquitectura
│   ├── decisiones.md       # Registro de decisiones de diseño
│   ├── guia-usuario.md     # Guía para el usuario final
│   └── referencias.md      # Referencias bibliográficas y teóricas
├── src\
│   ├── __init__.py         # Paquete principal de lógica
│   ├── benchmark.py        # Módulo de medición de rendimiento
│   ├── block_sort.py       # Implementación del algoritmo Block Sort
│   └── pokeapi.py          # Cliente PokeAPI y gestor de datos locales
├── tests\
│   ├── test_block_sort.py  # Pruebas unitarias para Block Sort
│   └── test_pokeapi.py     # Pruebas unitarias para el cliente PokeAPI
└── ui\
    ├── __init__.py         # Paquete de interfaz gráfica
    ├── animacion.html      # Plantilla HTML/JS para la visualización animada
    ├── controles.py        # Componentes de la barra lateral (Sidebar)
    ├── datos.py            # Capa intermedia de filtrado y procesamiento
    └── vistas.py           # Renderizado de vistas en Streamlit (Listado, Animación, Benchmark)
```

---

## 2. La Aplicación Web (`app.py`)

`app.py` es el script principal que inicializa la aplicación web con **Streamlit**.

* Configura la página en modo ancho (`layout="wide"`).
* Carga el dataset de Pokémon llamando a `cargar_datos()` (con caché de Streamlit).
* Renderiza los controles interactivos de la barra lateral mediante `renderizar_controles()`.
* Filtra y ordena los registros según los parámetros elegidos (`filtrar_y_ordenar()`).
* Orquestra la navegación entre las tres vistas principales:
  1. **Listado de Pokémon:** Tabla interactiva con métricas y datos formateados.
  2. **Animación de Ordenamiento:** Visualización paso a paso del algoritmo.
  3. **Métricas de Benchmark:** Análisis comparativo de rendimiento.

---

## 3. El Corazón del Proyecto (`src/`)

### `src/block_sort.py`
Implementa el algoritmo **Block Sort**, un método de ordenamiento híbrido y estable inspirado en Merge-Insertion Sort y versiones simplificadas de Timsort.

* **`_insertion_sort(arr, start, end, key_func, reverse)`**: Ordena un segmento acotado `[start, end)` utilizando inserción directa. Es altamente eficiente para bloques pequeños (`TAM_BLOQUE = 32`).
* **`_merge(arr, start, mid, end, key_func, reverse)`**: Fusiona dos sublistas ordenadas adyacentes manteniendo la estabilidad mediante un búfer temporal didáctico.
* **`block_sort(lista, key=None, reverse=False, bloque=TAM_BLOQUE)`**: Función principal. Divide la lista en bloques de tamaño fijo, ordena cada uno por inserción y los fusiona de a pares duplicando el ancho en cada pasada. Retorna una nueva lista sin mutar la original.
* **`block_sort_steps(lista, key=None, reverse=False)`**: Generador que cede copias del arreglo en cada etapa intermedia.
* **`block_sort_detailed_steps(lista, key=None, reverse=False, bloque=TAM_BLOQUE)`**: Generador avanzado que cede tuplas con el estado del arreglo, el ancho del bloque y las comparaciones o intercambios, permitiendo la animación fluida en la UI.

### `src/pokeapi.py`
Gestiona la comunicación con la **PokeAPI** y la lectura del dataset estático local (`data/pokemon.json`).

* Utiliza `requests_cache` junto con `platformdirs` para establecer una caché persistente en SQLite (`pokeapi_cache`), evitando solicitudes repetitivas a la red y acelerando los tiempos de arranque.
* **`listar_pokemon(limit)`**: Obtiene el listado básico desde la API.
* **`detalle_pokemon(id_o_nombre)`**: Consulta los datos completos de un Pokémon específico.
* **`cargar_pokemon(ruta)`**: Lee el dataset local JSON.
* **`all_pokemon(limit)`**: Carga prioritaria desde el archivo local con fallback automático a la API remota.
* **`generar_json(limit, ruta)`**: Descarga y normaliza el dataset desde la PokeAPI guardándolo en `data/pokemon.json`.
* Funciones auxiliares de filtrado (`filtrar_por_tipo`, `buscar_pokemon`).

### `src/benchmark.py`
Mide de forma empírica el rendimiento de `block_sort`.

* **`_Contado`**: Clase envoltorio que intercepta y cuenta cada comparación (`<`, `>`, `<=`, `>=`) realizada durante el ordenamiento.
* **`_medir(datos, bloque)`**: Realiza múltiples repeticiones (`REPETICIONES = 20`), toma el mejor tiempo de ejecución (`perf_counter`) y registra el número exacto de comparaciones.
* **`ejecutar_benchmark()`**: Evalúa combinaciones de campos (`height`, `weight`, `base_experience`), tamaños de bloque y tamaños de lista ($n$).
* Ejecutable directamente por consola (`python -m src.benchmark`).

---

## 4. La Interfaz de Usuario (`ui/`)

### `ui/controles.py`
Define los elementos interactivos de la barra lateral (*Sidebar*) en Streamlit (búsqueda por texto, filtrado por tipo elemental, selección de atributo de ordenamiento, checkbox de orden descendente y selector de vista).

### `ui/datos.py`
Capa intermedia que conecta los datos en caché con la lógica de filtrado y ordenamiento de la aplicación.

### `ui/vistas.py`
Contiene las funciones encargadas de renderizar las vistas en la interfaz:
* **`mostrar_metricas_generales(...)`**: Tarjetas métricas superiores con totales y promedios.
* **`mostrar_listado(...)`**: Tabla formateada con Pandas (`st.dataframe`).
* **`mostrar_animacion_ordenamiento(...)`**: Visualizador interactivo que integra la plantilla `animacion.html` mediante `streamlit.components.v1`.
* **`mostrar_explicacion_block_sort()`**: Pestañas con el código fuente real extraído directamente de `src/block_sort.py`.
* **`mostrar_benchmark()`**: Gráficos de líneas interactivos y tablas de rendimiento de benchmark.

---

## 5. Pruebas Unitarias (`tests/`)

### `tests/test_block_sort.py`
Verifica la corrección, estabilidad, manejo de casos borde (listas vacías, un elemento, duplicados) y correspondencia estricta con la función integrada `sorted()` de Python para diversos tamaños de entrada y funciones `key`.

### `tests/test_pokeapi.py`
Valida la existencia del directorio de caché, el funcionamiento de la caché HTTP y la correcta lectura y filtrado del dataset local de Pokémon.

---

## 6. Datos y Documentación (`data/`, `docs/`)

* **`data/pokemon.json`**: Dataset estático normalizado con los primeros 151 Pokémon y sus atributos clave (`id`, `name`, `height`, `weight`, `base_experience`, `tipo`).
* **`data/sprites/`**: Directorio con los iconos PNG de cada Pokémon utilizados en la animación.
* **`docs/decisiones.md`**: Registro de decisiones arquitectónicas y de diseño.
* **`docs/guia-usuario.md`**: Manual de usuario para instalación y ejecución.
* **`docs/referencias.md`**: Bibliografía teórica sobre algoritmos de ordenamiento híbridos, estabilidad y Block Sort.
