# Pokedex Block Sort

Proyecto de ordenamiento con el algoritmo **Block Sort** (Merge-Insertion Sort) utilizando datos estructurados de Pokémon (`data/pokemon.json`) + visualización interactiva con **Streamlit**.

## Objetivo

- Implementar el algoritmo **Block Sort** en Python de forma **estable** y eficiente (con búfer temporal didáctico).
- Procesar un conjunto de datos local optimizado de Pokémon (`data/pokemon.json`) extraído de la PokeAPI.
- Visualizar, filtrar y ordenar los datos mediante una interfaz interactiva con Streamlit.

## Decisiones Clave (Resumen)

- **Block Sort**: Es estable (los Pokémon con valores idénticos preservan su orden original) y utiliza un búfer temporal eficiente. Funciona ordenando bloques de tamaño fijo (`TAM_BLOQUE = 32`) con Insertion Sort y fusionándolos iterativamente por pares.
- **Dataset Local (`data/pokemon.json`)**: Evita consultas repetitivas a la API remota, permite funcionamiento offline, garantiza datos limpios y normalizados (sin valores nulos) y acelera drásticamente las demostraciones.
- **Streamlit**: Permite una interfaz interactiva rápida y limpia sin necesidad de desarrollo frontend complejo.

Consulta [docs/decisiones.md](docs/decisiones.md) y [docs/referencias.md](docs/referencias.md) para más detalles técnicos.

## Estructura del Proyecto

```
pokedex-blocksort/
├── README.md
├── requirements.txt
├── app.py
├── data/
│   ├── pokemon.json
│   └── sprites/
├── docs/
│   ├── code.md
│   ├── decisiones.md
│   ├── guia-usuario.md
│   ├── referencias.md
│   └── src/
├── ui/
│   ├── __init__.py
│   ├── animacion.html
│   ├── controles.py
│   ├── datos.py
│   └── vistas.py
├── src/
│   ├── __init__.py      
│   ├── benchmark.py
│   ├── block_sort.py  
│   └── pokeapi.py    
└── tests/
    ├── test_block_sort.py
    └── test_pokeapi.py
```

## Instalación

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

## Ejecución de Pruebas

```bash
python -m unittest discover tests
```

## Ejecución de la App Streamlit

```bash
streamlit run app.py
```

## Stack Tecnológico

Python 3.10+, `requests`, `requests-cache`, `platformdirs`, `streamlit`, `pandas`, `pytest`.
