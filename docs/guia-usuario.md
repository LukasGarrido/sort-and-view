# Guia de Usuario - Pokedex Block Sort

Bienvenido a la guia de usuario de **Pokedex Block Sort**, una aplicacion interactiva para demostrar el algoritmo de ordenamiento **Block Sort** con datos de Pokemon.

---

## 1. Requisitos e Instalacion

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar pruebas unitarias:
   ```bash
   python -m pytest
   ```

---

## 2. Uso de la Aplicacion Streamlit

Inicia la interfaz gráfica con:
```bash
streamlit run app.py
```

### Secciones Principales (Barra Lateral):
1. **Listado de Pokemon**: Filtra por tipo, busca por nombre y ordena por altura, peso, experiencia o ID usando Block Sort.
2. **Animacion de Ordenamiento**: Selecciona la cantidad de elementos, ajusta la velocidad e inicia la animacion. Los datos se mezclan aleatoriamente y puedes ver en tiempo real cómo las barras con nombres en el eje X y colores unicos se mueven y ordenan paso a paso.
3. **Metricas de Benchmark**: Visualiza gráficos de tiempo ($\mu s$) y comparaciones de Block Sort segun el tamaño del dataset ($n$).
