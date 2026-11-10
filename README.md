# Pokédex Block Sort

Proyecto pequeño que ordena Pokémon obtenidos desde [PokeAPI](https://pokeapi.co/) usando el algoritmo **Block Sort** (block merge sort). ¿Por qué?, por que es un ordenamiento estable que trabaja casi sin memoria extra (in-place).

## Objetivo

- Implementar Block Sort en Python.
- Obtener datos reales de Pokémon desde PokeAPI (con caché local).
- Ordenarlos por distintos campos: `name`, `weight`, `height`, `base_experience`, `tipo`.

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

## Instalación

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Stack

Python 3.10+, `requests`, `requests-cache`, `pytest`.
