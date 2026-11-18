import pathlib

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.conftest import PASTA_SCREENSHOTS

PAINEL = (pathlib.Path(__file__).parent.parent / "web" / "painel.html").resolve().as_uri()


@pytest.fixture
def driver(request):
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    drv = webdriver.Chrome(options=opts)
    yield drv
    # Evidencia: screenshot automatico se o teste falhou
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        PASTA_SCREENSHOTS.mkdir(exist_ok=True)
        drv.save_screenshot(str(PASTA_SCREENSHOTS / f"{request.node.name}.png"))
    drv.quit()


def solicitar(driver, nome, qtd):
    driver.get(PAINEL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "form-oxigenio")))
    driver.find_element(By.ID, "astronauta").send_keys(nome)
    driver.find_element(By.ID, "quantidade").send_keys(str(qtd))
    driver.find_element(By.ID, "btn-solicitar").click()
    return wait


def test_solicitacao_aprovada_atualiza_nivel(driver):
    wait = solicitar(driver, "Ana", 50)
    wait.until(EC.text_to_be_present_in_element((By.ID, "nivel-oxigenio"), "950"))
    assert "aprovada" in driver.find_element(By.ID, "mensagem").text


def test_solicitacao_acima_da_cota_e_negada(driver):
    wait = solicitar(driver, "Joao", 500)
    wait.until(EC.text_to_be_present_in_element((By.ID, "mensagem"), "negada"))
    assert driver.find_element(By.ID, "nivel-oxigenio").text == "1000"


def test_dados_invalidos(driver):
    wait = solicitar(driver, "", 10)
    wait.until(EC.text_to_be_present_in_element((By.ID, "mensagem"), "invalidos"))
