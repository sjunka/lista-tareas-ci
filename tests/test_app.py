import pytest

from app import app, tareas


@pytest.fixture
def cliente():
    tareas.clear()
    app.config["TESTING"] = True
    with app.test_client() as cliente:
        yield cliente


def test_listar_tareas_muestra_las_tareas(cliente):
    # Arrange
    tareas.append({"id": 1, "texto": "Comprar pan"})

    # Act
    respuesta = cliente.get("/")

    # Assert
    assert respuesta.status_code == 200
    assert "Comprar pan" in respuesta.get_data(as_text=True)


def test_agregar_tarea_la_guarda_en_la_lista(cliente):
    # Arrange
    datos = {"texto": "Comprar pan"}

    # Act
    respuesta = cliente.post("/tareas", data=datos)

    # Assert
    assert respuesta.status_code == 302
    assert [tarea["texto"] for tarea in tareas] == ["Comprar pan"]


def test_eliminar_tarea_la_quita_de_la_lista(cliente):
    # Arrange
    tareas.append({"id": 1, "texto": "Comprar pan"})

    # Act
    respuesta = cliente.post("/tareas/1/eliminar")

    # Assert
    assert respuesta.status_code == 302
    assert tareas == []


def test_agregar_tarea_vacia_responde_400(cliente):
    # Arrange
    datos = {"texto": "   "}

    # Act
    respuesta = cliente.post("/tareas", data=datos)

    # Assert
    assert respuesta.status_code == 400
    assert tareas == []


def test_eliminar_tarea_que_no_existe_responde_404(cliente):
    # Arrange
    tareas.append({"id": 1, "texto": "Comprar pan"})

    # Act
    respuesta = cliente.post("/tareas/99/eliminar")

    # Assert
    assert respuesta.status_code == 404
    assert len(tareas) == 1
