# Pokedex Block Sort: cómo está construido

Este documento explica cómo funciona el proyecto **Pokedex Block Sort**: qué hace cada archivo, cómo se conectan entre sí y cómo se comprueba que todo funcione bien.

---

## 1. La aplicación web

### `app.py`
Es la puerta de entrada. Con Streamlit levanta una página web interactiva donde puedes explorar Pokémon y ver cómo trabaja el algoritmo de ordenamiento.

**Qué hace:**
* Configura la página con diseño ancho para aprovechar toda la pantalla.
* Carga los datos de los Pokémon una sola vez y los guarda en caché (`cargar_datos`).
* Dibuja la barra lateral con los controles (`renderizar_controles`).
* Filtra y ordena los registros según lo que elijas (`filtrar_y_ordenar`).
* Te permite moverte entre tres vistas:
  1. **Listado de Pokémon:** una tabla interactiva con métricas resumen.
  2. **Animación de ordenamiento:** ves paso a paso cómo se ordena la lista con gráficos animados de Altair.
  3. **Métricas de benchmark:** análisis de rendimiento y comparaciones.

---

## 2. El corazón del proyecto (`src/`)

### `src/__init__.py`
Marca la carpeta `src` como paquete de Python.

### `src/block_sort.py`
Aquí vive el algoritmo **Block Sort**, un método híbrido inspirado en Merge-Insertion Sort y en una versión simplificada de Timsort.

**Funciones principales:**
* `_insertion_sort(arr, start, end, key_func, reverse)`: ordena un tramo pequeño de la lista, en el rango `[start, end)`, usando inserción. Es muy eficiente con bloques chicos.
* `_merge(arr, start, mid, end, key_func, reverse)`: une dos tramos ya ordenados que están uno al lado del otro. Mantiene la estabilidad y usa un búfer temporal pensado para que sea fácil de entender.
* `block_sort(lista, key=None, reverse=False)`: la función principal. Parte la lista en bloques de tamaño fijo (`TAM_BLOQUE = 32`), ordena cada uno por inserción y luego los va fusionando de a pares, duplicando el ancho en cada pasada. Devuelve una lista nueva y no modifica la original.
* `block_sort_detailed_steps(lista, key=None, reverse=False)`: un generador (`yield`) que entrega una copia de la lista en cada micro-paso, tanto en las inserciones como en las fusiones. Es lo que hace posible la animación paso a paso.

### `src/pokeapi.py`
Se encarga de hablar con la PokéAPI y de manejar el dataset local (`data/pokemon.json`).

**Características:**
* Usa una caché persistente en SQLite (con `requests_cache` y `platformdirs`) para no repetir peticiones de red y que la app arranque más rápido.
* `listar_pokemon(limit)`: obtiene el listado básico desde la API.
* `detalle_pokemon(id_o_nombre)`: consulta los datos completos de un Pokémon concreto.
* `cargar_pokemon(ruta)`: lee el dataset local guardado en `data/pokemon.json`.
* `all_pokemon(limit)`: intenta cargar primero el archivo local y, si no puede, recurre automáticamente a la API.
* `generar_json(limit, ruta)`: descarga el dataset desde la API y lo guarda en tu equipo.
* `filtrar_por_tipo` y `buscar_pokemon`: funciones auxiliares para filtrar y buscar.

### `src/benchmark.py`
Mide qué tan rápido y qué tan eficiente es `block_sort` en la práctica.

**Componentes:**
* Clase `_Contado`: envuelve los valores para interceptar y contar cuántas comparaciones (`<`, `>`, `<=`, `>=`) se hacen durante el ordenamiento.
* `_medir(datos)`: repite la prueba varias veces (`REPETICIONES = 20`), se queda con el mejor tiempo en microsegundos (`perf_counter`) y registra las comparaciones.
* `ejecutar_benchmark()`: evalúa el rendimiento con distintos campos (`height`, `weight`, `base_experience`) y diferentes tamaños de entrada (`25`, `50`, `100`, `151`).
* Se puede correr desde la consola con `python -m src.benchmark`.

---

## 3. La interfaz de usuario (`ui/`)

### `ui/__init__.py`
Marca la carpeta `ui` como paquete de Python.

### `ui/controles.py`
Maneja los controles interactivos de la barra lateral de Streamlit.

**Incluye:**
* Una caja de texto para buscar Pokémon por nombre.
* Un desplegable para filtrar por tipo elemental ("Todos", "Grass", "Fire", "Water", etc.).
* Un selector para elegir por qué característica ordenar ("ID", "Nombre", "Altura", "Peso", "Experiencia Base").
* Una casilla para invertir el orden (`reverse`).
* Un botón para elegir la vista principal.

### `ui/datos.py`
Es la capa intermedia que prepara los datos para la interfaz.

**Funciones:**
* `cargar_datos()`: carga los Pokémon usando la caché de Streamlit (`@st.cache_data`).
* `obtener_tipos_disponibles(pokemones)`: saca los tipos únicos del dataset y los ordena alfabéticamente.
* `filtrar_y_ordenar(...)`: aplica en cadena el filtro por tipo y la búsqueda por texto, y al final llama a `block_sort` con la clave elegida.

### `ui/vistas.py`
Se encarga de dibujar las vistas en Streamlit.

**Secciones:**
* `mostrar_metricas_generales(...)`: tarjetas con el total de Pokémon y los promedios de altura, peso y experiencia base.
* `mostrar_listado(...)`: tabla formateada con Pandas y Streamlit (`st.dataframe`).
* `mostrar_animacion_ordenamiento(...)`: visualizador interactivo con **Altair** (`st.altair_chart`), con controles para el tamaño de la muestra y la velocidad, barras de progreso y pasos detallados.

---

## 4. Pruebas unitarias (`tests/`)

### `tests/test_block_sort.py`
Verifica que `block_sort` ordene correctamente y sea estable.

**Casos de prueba:**
* `test_lista_vacia`: comprueba qué pasa con una lista vacía `[]`.
* `test_un_elemento`: valida listas de un solo elemento.
* `test_elementos_duplicados`: revisa el orden ascendente y descendente con valores repetidos.
* `test_coincidencia_con_sorted_numeros`: compara el resultado con `sorted()` de Python usando listas aleatorias de varios tamaños (menores, iguales y mayores a `TAM_BLOQUE = 32`).
* `test_con_key_funcion`: prueba el ordenamiento de diccionarios que simulan atributos de Pokémon usando `key=lambda x: ...`.
* `test_inmutabilidad_lista_original`: asegura que la lista original no se modifique.
* `test_estabilidad`: confirma que los elementos con la misma clave conservan su orden relativo, tanto en ascendente como en descendente.

### `tests/test_pokeapi.py`
Verifica el cliente de la API y el dataset local.

**Casos de prueba:**
* Que el directorio de caché (`CACHE_DIR`) exista y sea correcto.
* Que `requests_cache` esté instalado y funcione.
* Que los datos se carguen bien desde `data/pokemon.json`.
* Que `all_pokemon()` respete el límite indicado.
* Que el filtrado por tipo y la búsqueda por nombre funcionen.

---

## 5. Documentación y datos (`data/`, `docs/`)

* **`data/pokemon.json`:** dataset estático con los primeros 151 Pokémon y sus atributos clave (`id`, `name`, `height`, `weight`, `base_experience`, `tipo`). Permite que la app funcione sin conexión y arranque rápido.
* **`docs/decisiones.md`:** registro de las decisiones de arquitectura y diseño del proyecto.
* **`docs/guia-usuario.md`:** manual para el usuario final sobre cómo instalar y ejecutar la app web y el benchmark por consola.
* **`docs/referencias.md`:** referencias teóricas y bibliográficas sobre algoritmos de ordenamiento híbridos y Block Sort.