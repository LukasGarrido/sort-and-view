"""
Implementación del algoritmo Block Sort (Merge-Insertion Sort / Timsort simplificado).
"""

TAM_BLOQUE = 32


def _insertion_sort(arr, start, end, key_func, reverse):
    """Ordena una sublista en el rango [start, end) usando insertion sort."""
    for i in range(start + 1, end):
        current = arr[i]
        j = i - 1
        if not reverse:
            while j >= start and key_func(arr[j]) > key_func(current):
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= start and key_func(arr[j]) < key_func(current):
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = current


def _merge(arr, start, mid, end, key_func, reverse):
    """Fusiona dos sublistas ordenadas arr[start:mid] y arr[mid:end]
    en un rango ordenado arr[start:end] utilizando un búfer temporal didáctico.
    """
    left = arr[start:mid]
    right = arr[mid:end]

    i = 0
    j = 0
    k = start

    n_left = len(left)
    n_right = len(right)

    if not reverse:
        while i < n_left and j < n_right:
            if key_func(left[i]) <= key_func(right[j]):
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
    else:
        while i < n_left and j < n_right:
            if key_func(left[i]) >= key_func(right[j]):
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

    while i < n_left:
        arr[k] = left[i]
        i += 1
        k += 1

    while j < n_right:
        arr[k] = right[j]
        j += 1
        k += 1


def block_sort(lista, key=None, reverse=False, bloque=TAM_BLOQUE):
    """Ordenamiento por fusión estable (Block Sort):
    1. Divide la lista en bloques de tamaño fijo (`bloque`, por defecto TAM_BLOQUE).
    2. Ordena cada bloque con insertion sort.
    3. Fusiona bloques vecinos de a pares, duplicando el ancho en cada pasada,
       hasta quedar un solo bloque.

    Utiliza un búfer temporal didáctico durante la fusión y mantiene
    la estabilidad tanto para reverse=False como para reverse=True.
    Devuelve una lista nueva sin modificar la original.
    """
    if not lista:
        return []

    arr = list(lista)
    n = len(arr)
    if n <= 1:
        return arr

    key_func = key if key is not None else (lambda x: x)

    # 1 y 2. Dividir en bloques de tamaño `bloque` y ordenar con insertion sort
    for i in range(0, n, bloque):
        end = min(i + bloque, n)
        _insertion_sort(arr, i, end, key_func, reverse)

    # 3. Fusionar bloques vecinos de a pares, duplicando el ancho en cada pasada
    width = bloque
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)
            if mid < right:
                _merge(arr, left, mid, right, key_func, reverse)
        width *= 2

    return arr


def block_sort_steps(lista, key=None, reverse=False):
    """Generador que cede (yield) copias del arreglo en cada paso intermedio
    de Block Sort (después de ordenar cada bloque y después de cada pasada de fusión).
    """
    if not lista:
        yield []
        return

    arr = list(lista)
    n = len(arr)
    if n <= 1:
        yield arr
        return

    key_func = key if key is not None else (lambda x: x)
    yield list(arr)

    for i in range(0, n, TAM_BLOQUE):
        end = min(i + TAM_BLOQUE, n)
        _insertion_sort(arr, i, end, key_func, reverse)
        yield list(arr)

    width = TAM_BLOQUE
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)
            if mid < right:
                _merge(arr, left, mid, right, key_func, reverse)
        yield list(arr)
        width *= 2


def block_sort_detailed_steps(lista, key=None, reverse=False, bloque=TAM_BLOQUE):
    """Generador que cede (yield) tuplas (copia del arreglo, ancho, comparacion) para animar el algoritmo.
    - Paso de comparacion: `comparacion` es (pos_a, pos_b), las dos posiciones que se comparan; el arreglo no cambia.
    - Paso de intercambio: `comparacion` es None y el arreglo cambia en un intercambio.
    `ancho` es el tamaño de los bloques que se están ordenando o fusionando.
    `bloque` permite usar bloques más chicos que TAM_BLOQUE para que se vean en la animación.
    """
    if not lista:
        yield [], bloque, None
        return

    arr = list(lista)
    n = len(arr)
    if n <= 1:
        yield arr, bloque, None
        return

    key_func = key if key is not None else (lambda x: x)
    yield list(arr), bloque, None

    def desordenados(x, y):
        """True si x no puede quedar antes que y (estricto, mantiene la estabilidad)."""
        return key_func(x) < key_func(y) if reverse else key_func(x) > key_func(y)

    # Cada yield es una permutación de la lista (solo se intercambian elementos),
    # así la animación puede mover una barra por elemento sin repetidos ni faltantes.

    # 1 y 2. Inserción detallada por bloques (intercambios con el vecino)
    for start in range(0, n, bloque):
        end = min(start + bloque, n)
        for i in range(start + 1, end):
            j = i - 1
            while j >= start:
                yield list(arr), bloque, (j, j + 1)
                if not desordenados(arr[j], arr[j + 1]):
                    break
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield list(arr), bloque, None
                j -= 1

    # 3. Fusión detallada: cada elemento de la derecha que debe ir antes se desliza hacia su lugar
    width = bloque
    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)
            i, j = left, mid
            while i < j < right:
                yield list(arr), 2 * width, (i, j)
                if desordenados(arr[i], arr[j]):
                    for k in range(j, i, -1):
                        arr[k], arr[k - 1] = arr[k - 1], arr[k]
                        yield list(arr), 2 * width, None
                    j += 1
                i += 1
        width *= 2
