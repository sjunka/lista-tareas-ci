# Lista de tareas con pruebas

Actividad en clase de CI del curso Integración y Entrega Continua de Software (SI6008), Universidad EAFIT.

Autor: Sergio Junca

Es una lista de tareas sencilla hecha en Flask. Sobre ella hice pruebas unitarias con pytest, medí la cobertura con pytest-cov y escribí una prueba de aceptación con Selenium.

## 1. La aplicación

- Backend: `app.py`, con Flask. Las tareas se guardan en una lista en memoria, así que se pierden al reiniciar la aplicación.
- Frontend: `templates/index.html`, una página HTML con un campo para escribir la tarea, el botón "Agregar" y un botón "Eliminar" por cada tarea.

| Método | Ruta | Endpoint | Qué hace |
|---|---|---|---|
| GET | `/` | `listar_tareas` | Muestra la página con las tareas |
| POST | `/tareas` | `agregar_tarea` | Agrega la tarea del formulario. Si llega vacía responde 400 |
| POST | `/tareas/<id>/eliminar` | `eliminar_tarea` | Elimina la tarea. Si no existe responde 404 |

Eliminar usa POST y no DELETE porque un formulario HTML solo puede enviar GET o POST.

### Cómo ejecutarla

Probado con Python 3.12 y Google Chrome.

```bash
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

La aplicación queda en http://127.0.0.1:5000.

## 2. Pruebas unitarias y cobertura

### Pruebas unitarias

Están en `tests/test_app.py`. Hay una prueba por endpoint y dos más para los casos de error. Todas siguen la estructura AAA: Arrange prepara la lista, Act llama al endpoint y Assert revisa el resultado.

Usan el cliente de pruebas de Flask, que llama a cada endpoint sin levantar el servidor ni abrir un navegador. Además de revisar la respuesta, cada prueba revisa la lista interna `tareas`. Por ejemplo, la prueba de `agregar_tarea` comprueba que "Comprar pan" quedó guardada en la lista, no solo que la respuesta fue exitosa. Antes de cada prueba la lista se vacía, para que ninguna dependa de lo que dejó otra.

### Cómo se mide la cobertura

Con `pytest-cov`, un plugin de pytest que usa `coverage.py`. Mientras corren las pruebas, coverage.py registra qué líneas de `app.py` se ejecutan. Al final las compara con todas las líneas del archivo y calcula el porcentaje.

Con `--cov-branch` también mide ramas: revisa que cada `if` se haya probado tanto cuando la condición se cumple como cuando no. Una línea puede ejecutarse sin que se pruebe el otro camino del `if`, y la cobertura de líneas sola no lo muestra.

```bash
pytest tests/test_app.py --cov=app --cov-branch --cov-report=term-missing --cov-report=html
```

`term-missing` muestra en la terminal los números de las líneas sin probar. `html` genera la carpeta `htmlcov/`, y al abrir `htmlcov/index.html` se ve el código marcado línea por línea.

### Resultado y análisis

Primero medí solo con las tres pruebas mínimas, una por endpoint:

```
Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py      22      2      4      2    85%   21, 30
```

La cobertura era del 85%. Las líneas 21 y 30 son los `abort(400)` y `abort(404)`: ninguna prueba enviaba una tarea vacía ni intentaba eliminar una tarea que no existe. Por eso también aparecen 2 ramas parciales: esos dos `if` solo se habían probado por el lado en que todo sale bien.

Agregué dos pruebas para esos casos (`test_agregar_tarea_vacia_responde_400` y `test_eliminar_tarea_que_no_existe_responde_404`) y volví a medir:

```
Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py      22      0      4      0   100%
```

Quedó en 100% de líneas y ramas. Solo se excluye el bloque `if __name__ == "__main__"`, marcado con `# pragma: no cover`, porque únicamente arranca el servidor.

El 100% indica que todo el código se ejecutó durante las pruebas, no que esté libre de errores. Para comprobar que las pruebas sí detectan fallos, cambié la plantilla para que mostrara el id de la tarea en lugar del texto. Fallaron la prueba de `listar_tareas` y la de aceptación. Después dejé la plantilla como estaba.

## 3. Prueba de aceptación

### Investigación

Una prueba de aceptación necesita tres cosas: la aplicación corriendo, un navegador real y una herramienta que controle ese navegador desde el código. En Python las dos opciones más usadas son Selenium y Playwright. Elegí Selenium porque desde la versión 4.6 trae Selenium Manager, que descarga solo el driver compatible con Chrome, y porque es la herramienta que usa el curso.

### La prueba

Está en `tests/test_acceptance_app.py` y sigue el flujo del enunciado:

1. Inicia la aplicación. El fixture `url_app` la levanta en un hilo con el servidor de Werkzeug, que viene con Flask, en un puerto libre, y la apaga al terminar. No hace falta abrir otra terminal.
2. Abre Chrome en modo headless (sin ventana) en la página principal.
3. Busca el campo de texto y el botón "Agregar".
4. Escribe "Comprar pan" y hace clic en el botón.
5. Espera hasta 10 segundos a que "Comprar pan" aparezca en la lista. Si no aparece, la prueba falla.

```bash
pytest tests/test_acceptance_app.py -v
```

```
tests/test_acceptance_app.py::test_agregar_tarea_desde_el_navegador PASSED [100%]
============================== 1 passed in 4.97s ===============================
```

## Resumen de comandos

| Qué | Comando |
|---|---|
| Ejecutar la aplicación | `python app.py` |
| Pruebas unitarias con cobertura | `pytest tests/test_app.py --cov=app --cov-branch --cov-report=term-missing --cov-report=html` |
| Prueba de aceptación (requiere Chrome) | `pytest tests/test_acceptance_app.py -v` |
| Todas las pruebas | `pytest` |
