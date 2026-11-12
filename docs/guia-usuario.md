# Guía de Usuario - Pokedex Block Sort

Bienvenido a la guía de usuario oficial de **Pokedex Block Sort**, una aplicación web interactiva desarrollada con **Streamlit** que demuestra el funcionamiento del algoritmo de ordenamiento híbrido **Block Sort** aplicado a datos de Pokémon.

---

## 1. Requisitos e Instalación

### Requisitos previos
* **Python 3.8 o superior** instalado en el sistema.
* Entorno virtual recomendado (`venv`).

### Pasos de instalación y configuración

1. Clonar o acceder al directorio del proyecto:
   ```bash
   cd path/to/sort-and-view
   ```

2. Crear y activar un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv .venv
   # En Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # En macOS / Linux:
   source .venv/bin/activate
   ```

3. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar las pruebas unitarias para verificar la correcta instalación y funcionamiento del algoritmo:
   ```bash
   python -m pytest
   ```

---

## 2. Ejecución de la Aplicación Streamlit

Para iniciar la interfaz gráfica web interactiva, ejecuta:
```bash
streamlit run app.py
```
Esto abrirá automáticamente una pestaña en tu navegador web predeterminado (por defecto en `http://localhost:8501`).

---

## 3. Guía de Navegación y Funcionalidades

La barra lateral (*Sidebar*) de la aplicación ofrece controles dinámicos para buscar, filtrar y seleccionar vistas:

### Controles de Filtrado y Ordenamiento
* **Buscar Pokémon por nombre:** Permite filtrar instantáneamente la lista escribiendo parte del nombre (ej. "char", "pikachu").
* **Filtrar por tipo:** Desplegable con los tipos elementales disponibles ("Todos", "Grass", "Fire", "Water", "Electric", etc.).
* **Ordenar por característica:** Selecciona el atributo numérico o textual por el cual ordenar:
  * `ID`
  * `Nombre`
  * `Altura`
  * `Peso`
  * `Experiencia Base`
* **Orden descendente (Reverse):** Casilla de verificación para invertir el sentido del ordenamiento de manera estable.

### Vistas Principales (Navegación)

1. **Listado de Pokémon:**
   * Muestra tarjetas con métricas resumen (Total de Pokémon, Altura promedio, Peso promedio y Experiencia base promedio).
   * Presenta una tabla interactiva completa con todos los registros filtrados y ordenados mediante **Block Sort**.

2. **Animación de Ordenamiento:**
   * Permite visualizar paso a paso cómo actúa el algoritmo sobre una muestra de Pokémon (mínimo 25 elementos).
   * Incluye controles deslizantes para ajustar la cantidad de elementos y un botón para re-mezclar aleatoriamente el conjunto (*Mezclar de nuevo*).
   * Muestra gráficos dinámicos animados con **Altair** y un componente visualizador interactivo.
   * Incluye una sección inferior de código fuente con pestañas para inspeccionar la implementación de las funciones principales (`block_sort`, `_insertion_sort`, `_merge`) en tiempo real.

3. **Métricas de Benchmark (Block Sort):**
   * Evalúa y compara el rendimiento del algoritmo midiendo el tiempo de ejecución ($\mu s$) y el número de comparaciones.
   * Permite analizar el impacto del tamaño del dataset ($n$) y el tamaño de los bloques (`TAM_BLOQUE`) sobre diferentes atributos numéricos.
   * Muestra gráficos de líneas y tablas detalladas de rendimiento.

---

## 4. Ejecución de Benchmarks por Consola

También puedes ejecutar el módulo de benchmark directamente desde la terminal sin necesidad de abrir la interfaz gráfica:
```bash
python -m src.benchmark
```
Esto imprimirá en consola una tabla con los resultados de tiempo y comparaciones para diferentes tamaños de bloques y datasets.
