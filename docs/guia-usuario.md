# Guía de Usuario - Pokedex Block Sort

Bienvenido a la guía de usuario de **Pokedex Block Sort**, una aplicación educativa e interactiva diseñada para demostrar el funcionamiento del algoritmo de ordenamiento por fusión estable (**Block Sort**) utilizando datos de Pokémon.

---

## 1. Requisitos Previos

- Python 3.10 o superior instalado en tu sistema.
- Entorno virtual (recomendado).

---

## 2. Instalación y Configuración

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local:

1. **Clonar o abrir el repositorio** en tu directorio de trabajo.
2. **Crear y activar un entorno virtual**:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```
3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Ejecución de Pruebas Unitarias

Para validar que tanto el algoritmo `block_sort` como el cliente y procesador de la PokeAPI funcionan correctamente, ejecuta:

```bash
python -m unittest discover tests
```

Todas las pruebas unitarias (incluyendo casos borde, estabilidad, manejo de claves y procesamiento del dataset local) pasarán exitosamente.

---

## 4. Uso de la Aplicación Interactiva (Streamlit)

Para lanzar la interfaz gráfica interactiva y visualizar el ordenamiento en tiempo real:

```bash
streamlit run app.py
```

Una vez abierta la aplicación en tu navegador:
1. **Selecciona el criterio de ordenamiento (`key`)**: Puedes elegir entre peso (`weight`), altura (`height`), experiencia base (`base_experience`), nombre (`name`) o tipo (`tipo`).
2. **Elige el sentido del orden (`reverse`)**: Alterna entre orden ascendente y descendente manteniendo siempre la **estabilidad** del algoritmo (los elementos con claves iguales conservan su orden relativo original).
3. **Visualiza los resultados**: Explora la tabla de Pokémon ordenada mediante Block Sort, utilizando el conjunto de datos local optimizado (`data/pokemon.json`).
