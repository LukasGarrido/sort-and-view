# Pokedex Block Sort

Proyecto algoritmo de ordenamiento con block sort usando la API publica [PokeAPI](https://pokeapi.co/) + visualizacion interactiva con **Streamlit**.

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
├── app.py
├── docs/
│   ├── decisiones.md
│   ├── guia-usuario.md
│   └── referencias.md
├── ui/
│   ├── __init__.py
│   ├── controles.py
│   ├── datos.py
│   └── vistas.py
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
