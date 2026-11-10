# pokedex-blocksort

pokedex-blocksort/
├── README.md
├── requirements.txt
├── main.py                  # CLI
├── src/
│   ├── __init__.py
│   ├── block_sort.py        # implementación del algoritmo
│   ├── pokeapi.py           # cliente de la API + caché
│   └── benchmark.py         # comparación contra otros algoritmos
└── tests/
    ├── test_block_sort.py   # correctitud y estabilidad
    └── test_pokeapi.py      # con datos simulados, sin red
