## ¿Por qué Block Sort?

Es estable: si dos Pokémon empatan, conservan su orden original.
Casi no usa memoria extra, a diferencia del merge sort clásico.

## ¿Por qué Python?

Se lee casi como pseudocódigo, facilidad para explicar un algoritmo.
Tiene requests, pandas y streamlit, así que no hay que reinventar nada.

## ¿Por qué json y no PokeAPI directamente ?

- Los datos se extraen una sola vez de PokeAPI y se guardan solo con los campos que se ordenan (`id`, `name`, `height`, `weight`, `base_experience`, `tipo`).
- Ordenar y mostrar es instantáneo: evita las 152 peticiones en cada ejecución.
- La app funciona sin internet, lo que sirve como respaldo en la demo.
- Respeta a PokeAPI, que recomienda no repetir peticiones innecesarias.
- Los datos quedan ya normalizados (por ejemplo, `base_experience` nunca es `None`), así que el algoritmo trabaja con diccionarios simples.

## ¿Por qué Streamlit?

Una interfaz interactiva en pocas líneas, sin saber frontend.
No necesita endpoint propio: llama directo a las funciones.
Selector y botón en vivo hacen que el resultado se vea y se sienta dinámico.