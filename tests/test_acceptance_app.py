import threading

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.serving import make_server

from app import app, tareas


@pytest.fixture
def url_app():
    # 1. Inicia la aplicación en un puerto libre (el 0 le pide uno al sistema).
    tareas.clear()
    servidor = make_server("127.0.0.1", 0, app)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{servidor.server_port}"
    servidor.shutdown()
    servidor.server_close()


@pytest.fixture
def navegador():
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--headless")
    driver = webdriver.Chrome(options=opciones)
    yield driver
    driver.quit()


def test_agregar_tarea_desde_el_navegador(url_app, navegador):
    # 2. Abre el navegador en la página principal.
    navegador.get(url_app)

    # 3 y 4. Escribe "Comprar pan" en el campo y hace clic en "Agregar".
    navegador.find_element(By.NAME, "texto").send_keys("Comprar pan")
    navegador.find_element(By.XPATH, "//button[text()='Agregar']").click()

    # 5. Verifica que "Comprar pan" aparece en la lista de la página.
    assert WebDriverWait(navegador, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "ul"), "Comprar pan")
    )
