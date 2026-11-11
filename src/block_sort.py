"""
Implementación del algoritmo Block Sort (Merge-Insertion Sort / Timsort simplificado).

`block_sort` acepta un parámetro opcional `registrar` para observar cada paso
del algoritmo (útil para visualizarlo). Si no se pasa, no tiene ningún efecto.

Eventos que recibe `registrar(tipo, arr, **info)`:
- "fase":     info = inicio, fin, mitad (None en la fase de bloques), nombre
              ("bloque" o "fusion"). Marca el rango sobre el que se trabaja.
- "comparar": info = indice, elemento, otro. Se compara `elemento` con `otro`.
              En insertion sort `otro` es arr[indice]; en la fusión son los dos
              candidatos del búfer (izquierda y derecha) e `indice` es el destino.
- "mover":    info = indice, elemento. Se acaba de escribir `elemento` en arr[indice].
`arr` es la lista de trabajo en ese momento; quien registra debe copiarla si la guarda.
"""

TAM_BLOQUE = 32


def _insertion_sort(arr, start, end, key_func, reverse, registrar=None):
    """Ordena una sublista en el rango [start, end) usando insertion sort."""
    if registrar:
        registrar("fase", arr, inicio=start, fin=end, mitad=None, nombre="bloque")
    for i in range(start + 1, end):
        current = arr[i]
        j = i - 1
        while j >= start:
            if registrar:
                registrar("comparar", arr, indice=j, elemento=current, otro=arr[j])
            if not reverse:
                debe_mover = key_func(arr[j]) > key_func(current)
            else:
                debe_mover = key_func(arr[j]) < key_func(current)
            if not debe_mover:
                break
            arr[j + 1] = arr[j]
            if registrar:
                registrar("mover", arr, indice=j + 1, elemento=arr[j + 1])
            j -= 1
        arr[j + 1] = current
        if registrar:
            registrar("mover", arr, indice=j + 1, elemento=current)


def _merge(arr, start, mid, end, key_func, reverse, registrar=None):
    """Fusiona dos sublistas ordenadas arr[start:mid] y arr[mid:end]
    en un rango ordenado arr[start:end] utilizando un búfer temporal didáctico.
    """
    if registrar:
        registrar("fase", arr, inicio=start, fin=end, mitad=mid, nombre="fusion")
    left = arr[start:mid]
    right = arr[mid:end]

    i = 0
    j = 0
    k = start

    n_left = len(left)
    n_right = len(right)

    while i < n_left and j < n_right:
        if registrar:
            registrar("comparar", arr, indice=k, elemento=left[i], otro=right[j])
        if not reverse:
            toma_izquierda = key_func(left[i]) <= key_func(right[j])
        else:
            toma_izquierda = key_func(left[i]) >= key_func(right[j])
        if toma_izquierda:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        if registrar:
            registrar("mover", arr, indice=k, elemento=arr[k])
        k += 1

    while i < n_left:
        arr[k] = left[i]
        if registrar:
            registrar("mover", arr, indice=k, elemento=arr[k])
        i += 1
        k += 1

    while j < n_right:
        arr[k] = right[j]
        if registrar:
            registrar("mover", arr, indice=k, elemento=arr[k])
        j += 1
        k += 1


def block_sort(lista, key=None, reverse=False, tam_bloque=TAM_BLOQUE, registrar=None):
    """Ordenamiento por fusión estable (Block Sort):
    1. Divide la lista en bloques de tamaño fijo (tam_bloque, por defecto TAM_BLOQUE).
    2. Ordena cada bloque con insertion sort.
    3. Fusiona bloques vecinos de a pares, duplicando el ancho en cada pasada,
       hasta quedar un solo bloque.

    Utiliza un búfer temporal didáctico durante la fusión y mantiene
    la estabilidad tanto para reverse=False como para reverse=True.
    Devuelve una lista nueva sin modificar la original.

    `registrar`, si se indica, se llama en cada paso (ver docstring del módulo).
    """
    if not lista:
        return []

    arr = list(lista)
    n = len(arr)
    if n <= 1:
        return arr

    if tam_bloque < 1:
        raise ValueError("tam_bloque debe ser >= 1")

    key_func = key if key is not None else (lambda x: x)

    # 1 y 2. Dividir en bloques de tamaño tam_bloque y ordenar con insertion sort
    for i in range(0, n, tam_bloque):
        end = min(i + tam_bloque, n)
        _insertion_sort(arr, i, end, key_func, reverse, registrar)

    # 3. Fusionar bloques vecinos de a pares, duplicando el ancho en cada pasada
    width = tam_bloque
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)
            if mid < right:
                _merge(arr, left, mid, right, key_func, reverse, registrar)
        width *= 2

    return arr
