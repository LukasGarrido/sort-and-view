# Pokedex Block Sort

Proyecto pequeno que ordena Pokemon obtenidos desde [PokeAPI](https://pokeapi.co/) usando el algoritmo **Block Sort** (block merge sort) y visualizacion interactiva con **Streamlit**.

## Objetivo

- Implementar Block Sort en Python.
- Obtener datos reales de Pokemon desde PokeAPI (con cache local SQLite en directorio del sistema operativo).
- Visualizar y ordenar los datos mediante interfaz con Streamlit.

## Estructura

```
pokedex-blocksort/
├── README.md
├── requirements.txt
├── main.py
├── src/
│   ├── __init__.py      
│   ├── block_sort.py  
│   ├── pokeapi.py    
│   └── benchmark.py 
└── tests/
    ├── test_block_sort.py
    └── test_pokeapi.py
```

## Instalacion

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Stack

Python 3.10+, `requests`, `requests-cache`, `platformdirs`, `streamlit`, `pandas`, `pytest`.
