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


def block_sort(lista, key=None, reverse=False):
    """Ordenamiento por fusión estable (Block Sort):
    1. Divide la lista en bloques de tamaño fijo (TAM_BLOQUE).
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

    # 1 y 2. Dividir en bloques de tamaño TAM_BLOQUE y ordenar con insertion sort
    for i in range(0, n, TAM_BLOQUE):
        end = min(i + TAM_BLOQUE, n)
        _insertion_sort(arr, i, end, key_func, reverse)

    # 3. Fusionar bloques vecinos de a pares, duplicando el ancho en cada pasada
    width = TAM_BLOQUE
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)
            if mid < right:
                _merge(arr, left, mid, right, key_func, reverse)
        width *= 2

    return arr
