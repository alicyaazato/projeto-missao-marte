import pathlib

import pytest

from src.gerenciador_recursos import GerenciadorRecursosMarte
from src.servico_telemetria import ServicoTelemetriaEspacial

PASTA_SCREENSHOTS = pathlib.Path(__file__).parent / "screenshots"


@pytest.fixture(scope="session")
def parametros_habitat():
    """Fixture global: parametros iniciais do habitat."""
    return {"oxigenio_kg": 1000.0, "agua_l": 2000.0, "astronautas": 4}


@pytest.fixture
def telemetria_mock(mocker):
    """Dubla o ServicoTelemetriaEspacial: nenhuma chamada de rede e feita."""
    mock = mocker.create_autospec(ServicoTelemetriaEspacial, instance=True)
    mock.enviar_relatorio.return_value = {"status": "recebido"}
    mock.disparar_alerta.return_value = {"status": "alerta_recebido"}
    return mock


@pytest.fixture
def gerenciador(parametros_habitat, telemetria_mock):
    """Instancia limpa por teste, com setup/teardown via yield."""
    g = GerenciadorRecursosMarte(telemetria=telemetria_mock, **parametros_habitat)
    yield g
    # teardown: garante que nenhum teste vazou estado negativo
    assert g.oxigenio_kg >= 0
    g.telemetria = None


# --- Evidencias para os testes Selenium -----------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
