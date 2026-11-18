import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.gerenciador_recursos import CotaExcedidaError, GerenciadorRecursosMarte

scenarios("features/solicitacao_oxigenio.feature")


@pytest.fixture
def contexto():
    return {}


@given(
    parsers.parse("um habitat com {oxigenio:g} kg de oxigenio e {astronautas:d} astronautas"),
    target_fixture="habitat",
)
def habitat(oxigenio, astronautas, telemetria_mock):
    return GerenciadorRecursosMarte(oxigenio, 2000.0, telemetria_mock, astronautas)


@when(parsers.parse('o astronauta "{nome}" solicita {qtd:g} kg de oxigenio'))
def solicitar(habitat, contexto, nome, qtd):
    try:
        contexto["resultado"] = habitat.solicitar_cota_extra(nome, qtd)
    except CotaExcedidaError as e:
        contexto["erro"] = e


@then("a solicitacao e aprovada")
def aprovada(contexto):
    assert "erro" not in contexto
    assert contexto["resultado"]["aprovado_kg"] > 0


@then("a solicitacao e negada por exceder a cota")
def negada(contexto):
    assert isinstance(contexto.get("erro"), CotaExcedidaError)


@then(parsers.parse("o estoque de oxigenio passa a ser {estoque:g} kg"))
def estoque(habitat, estoque):
    assert habitat.oxigenio_kg == pytest.approx(estoque)


@then("nenhum alerta e enviado para a Terra")
def sem_alerta(telemetria_mock):
    telemetria_mock.disparar_alerta.assert_not_called()


@then(parsers.parse('um alerta "{nivel}" e enviado para a Terra'))
def com_alerta(telemetria_mock, nivel):
    telemetria_mock.disparar_alerta.assert_called_once()
    assert telemetria_mock.disparar_alerta.call_args.args[0] == nivel
