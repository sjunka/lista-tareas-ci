from itertools import count

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

# Las tareas viven en memoria: se pierden al reiniciar la aplicación.
tareas = []
ids = count(1)


@app.get("/")
def listar_tareas():
    return render_template("index.html", tareas=tareas)


@app.post("/tareas")
def agregar_tarea():
    texto = request.form.get("texto", "").strip()
    if not texto:
        abort(400)
    tareas.append({"id": next(ids), "texto": texto})
    return redirect(url_for("listar_tareas"))


@app.post("/tareas/<int:tarea_id>/eliminar")
def eliminar_tarea(tarea_id):
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if tarea is None:
        abort(404)
    tareas.remove(tarea)
    return redirect(url_for("listar_tareas"))


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True, port=5000)
