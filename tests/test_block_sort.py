"""
Pruebas unitarias para Block Sort.
"""
import unittest
import random
from src.block_sort import block_sort, block_sort_detailed_steps, TAM_BLOQUE


class TestBlockSort(unittest.TestCase):

    def test_lista_vacia(self):
        self.assertEqual(block_sort([]), [])

    def test_un_elemento(self):
        self.assertEqual(block_sort([42]), [42])

    def test_elementos_duplicados(self):
        lista = [5, 2, 9, 2, 5, 1, 9]
        self.assertEqual(block_sort(lista), sorted(lista))
        self.assertEqual(block_sort(lista, reverse=True), sorted(lista, reverse=True))

    def test_coincidencia_con_sorted_numeros(self):
        import random
        # Probar con varios tamaños, incluyendo menores y mayores que TAM_BLOQUE
        for size in [0, 1, 5, 31, 32, 33, 100]:
            lista = [random.randint(-1000, 1000) for _ in range(size)]
            self.assertEqual(block_sort(lista), sorted(lista))
            self.assertEqual(block_sort(lista, reverse=True), sorted(lista, reverse=True))

    def test_con_key_funcion(self):
        # Simular diccionarios de Pokémon (weight, height, base_experience, name, tipo)
        pokemones = [
            {"id": 1, "name": "bulbasaur", "height": 7, "weight": 69, "base_experience": 64, "tipo": "grass"},
            {"id": 4, "name": "charmander", "height": 6, "weight": 85, "base_experience": 62, "tipo": "fire"},
            {"id": 7, "name": "squirtle", "height": 5, "weight": 90, "base_experience": 63, "tipo": "water"},
            {"id": 25, "name": "pikachu", "height": 4, "weight": 60, "base_experience": 112, "tipo": "electric"},
        ]

        # Ordenar por weight asc y desc
        res_weight_asc = block_sort(pokemones, key=lambda p: p["weight"])
        exp_weight_asc = sorted(pokemones, key=lambda p: p["weight"])
        self.assertEqual(res_weight_asc, exp_weight_asc)

        res_weight_desc = block_sort(pokemones, key=lambda p: p["weight"], reverse=True)
        exp_weight_desc = sorted(pokemones, key=lambda p: p["weight"], reverse=True)
        self.assertEqual(res_weight_desc, exp_weight_desc)

        # Ordenar por name asc y desc
        res_name_asc = block_sort(pokemones, key=lambda p: p["name"])
        exp_name_asc = sorted(pokemones, key=lambda p: p["name"])
        self.assertEqual(res_name_asc, exp_name_asc)

        res_name_desc = block_sort(pokemones, key=lambda p: p["name"], reverse=True)
        exp_name_desc = sorted(pokemones, key=lambda p: p["name"], reverse=True)
        self.assertEqual(res_name_desc, exp_name_desc)

    def test_inmutabilidad_lista_original(self):
        original = [3, 1, 4, 1, 5, 9, 2]
        copia = list(original)
        resultado = block_sort(original)
        self.assertEqual(original, copia)
        self.assertNotEqual(resultado, original)
        self.assertEqual(resultado, sorted(original))

    def test_estabilidad(self):
        # Objetos con clave duplicada para verificar estabilidad
        elementos = [
            {"key": 2, "orig_index": 0},
            {"key": 1, "orig_index": 1},
            {"key": 2, "orig_index": 2},
            {"key": 3, "orig_index": 3},
            {"key": 2, "orig_index": 4},
        ]

        # Orden ascendente
        res_asc = block_sort(elementos, key=lambda x: x["key"])
        keys_asc = [x["key"] for x in res_asc]
        self.assertEqual(keys_asc, [1, 2, 2, 2, 3])
        twos_asc = [x["orig_index"] for x in res_asc if x["key"] == 2]
        self.assertEqual(twos_asc, [0, 2, 4])

        # Orden descendente
        res_desc = block_sort(elementos, key=lambda x: x["key"], reverse=True)
        keys_desc = [x["key"] for x in res_desc]
        self.assertEqual(keys_desc, [3, 2, 2, 2, 1])
        twos_desc = [x["orig_index"] for x in res_desc if x["key"] == 2]
        self.assertEqual(twos_desc, [0, 2, 4])

    def test_pasos_detallados_son_permutaciones(self):
        """Cada paso de la animación contiene todos los elementos, sin repetidos ni faltantes."""
        for n in (5, TAM_BLOQUE + 8):
            for reverse in (False, True):
                datos = [(random.randint(1, 5), i) for i in range(n)]
                pasos = list(block_sort_detailed_steps(datos, key=lambda t: t[0], reverse=reverse))
                self.assertTrue(all(sorted(p) == sorted(datos) for p in pasos))
                self.assertEqual(pasos[-1], block_sort(datos, key=lambda t: t[0], reverse=reverse))


if __name__ == "__main__":
    unittest.main()
