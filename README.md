# Mini Proyecto ADA I - Análisis de Encuesta

Este proyecto implementa un sistema de análisis estadístico de encuestas para el curso Análisis y Diseño de Algoritmos I. Utiliza clases para representar encuestados, preguntas y temas, y calcula estadísticas como promedio, mediana, moda, extremismo y consenso. Todos los algoritmos de ordenamiento son implementados manualmente utilizando `insertion sort`, como se exige en el enunciado del proyecto.

## Estructura del Proyecto

- `Encuestado`: clase que representa a cada participante con su ID, nombre, nivel de experticia y opinión.
- `Pregunta`: clase que agrupa las opiniones sobre una pregunta específica y calcula estadísticas.
- `Tema`: clase que agrupa las preguntas bajo un mismo tema y calcula promedios generales.
- `Encuesta`: clase que agrupa todos los temas y todos los encuestados globales.
- `insertion_sort`: algoritmo de ordenamiento implementado manualmente en la solución 1

## Requisitos

- Python 3.x
- Archivos de entrada en formato `.txt` (por ejemplo, `Test1.txt`, `Test2.txt`, etc.)

## Instrucciones para Ejecutar

1. Coloca el archivo `main.py` y los archivos de prueba (por ejemplo, `Test1.txt`) en la misma carpeta.
2. Asegurarse de modificar al final del archivo `main.py` los nombres del archivo de entrada y salida si deseas correr un test diferente:

```python
archivo_entrada = "Testn.txt"   ## Aquí cambias el numero (n) según la prueba que se desee ejecutar (input)
archivo_salida = "Salida_Test1.txt" ## Al ejecutarse se obtendrá otro txt con la salida para el test (output)
