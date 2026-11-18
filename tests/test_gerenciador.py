import pytest

from src.gerenciador_recursos import (
    CotaExcedidaError,
    GerenciadorRecursosMarte,
    NivelEmergenciaInvalidoError,
    OxigenioInsuficienteError,
)


def novo(telemetria, oxigenio=1000.0, astronautas=4):
    return GerenciadorRecursosMarte(oxigenio, 2000.0, telemetria, astronautas)


# ---------- Parametrizacao ----------
@pytest.mark.parametrize(
    "astronautas, nivel, esperado",
    [
        (1, 1, 0.84),
        (4, 1, 3.36),
        (4, 2, 5.04),
        (4, 3, 6.72),
        (6, 3, 10.08),
    ],
)
def test_consumo_diario_oxigenio(gerenciador, astronautas, nivel, esperado):
    assert gerenciador.consumo_diario_oxigenio(nivel, astronautas) == pytest.approx(esperado)


@pytest.mark.parametrize(
    "astronautas, nivel, esperado",
    [(1, 1, 3.0), (4, 2, 18.0), (5, 3, 30.0)],
)
def test_consumo_diario_agua(gerenciador, astronautas, nivel, esperado):
    assert gerenciador.consumo_diario_agua(nivel, astronautas) == pytest.approx(esperado)


@pytest.mark.parametrize("nivel, taxa", [(1, 1.0), (2, 1.5), (3, 2.0)])
def test_taxa_emergencia(gerenciador, nivel, taxa):
    assert gerenciador.taxa_emergencia(nivel) == taxa


def test_autonomia_usa_estoque_e_consumo(gerenciador):
    assert gerenciador.autonomia_oxigenio_dias() == pytest.approx(1000 / 3.36)


@pytest.mark.parametrize(
    "oxigenio, cota",
    [(1000.0, 100.0), (16.8, 25.0)],  # normal x racionamento
)
def test_cota_extra_depende_do_racionamento(telemetria_mock, oxigenio, cota):
    assert novo(telemetria_mock, oxigenio).cota_extra_atual() == cota


# ---------- Excecoes ----------
@pytest.mark.parametrize("nivel", [0, 4, -1, "alto", None])
def test_nivel_emergencia_invalido(gerenciador, nivel):
    with pytest.raises(NivelEmergenciaInvalidoError, match="invalido"):
        gerenciador.taxa_emergencia(nivel)


def test_oxigenio_insuficiente(telemetria_mock):
    g = novo(telemetria_mock, oxigenio=10.0)
    with pytest.raises(OxigenioInsuficienteError):
        g.solicitar_cota_extra("Ana", 50.0)
    assert g.oxigenio_kg == 10.0


def test_cota_excedida(gerenciador):
    with pytest.raises(CotaExcedidaError):
        gerenciador.solicitar_cota_extra("Ana", 101.0)


@pytest.mark.parametrize("qtd", [0, -5])
def test_quantidade_invalida(gerenciador, qtd):
    with pytest.raises(ValueError):
        gerenciador.solicitar_cota_extra("Ana", qtd)


@pytest.mark.parametrize("o2, agua, n", [(-1, 10, 4), (10, -1, 4), (10, 10, 0)])
def test_parametros_iniciais_invalidos(telemetria_mock, o2, agua, n):
    with pytest.raises(ValueError):
        GerenciadorRecursosMarte(o2, agua, telemetria_mock, n)


# ---------- Mocks: telemetria ----------
def test_solicitacao_normal_nao_dispara_alerta(gerenciador, telemetria_mock):
    r = gerenciador.solicitar_cota_extra("Ana", 50.0)
    assert r == {"astronauta": "Ana", "aprovado_kg": 50.0, "estoque_kg": 950.0}
    telemetria_mock.disparar_alerta.assert_not_called()


def test_estoque_critico_dispara_alerta_com_argumentos_corretos(telemetria_mock):
    g = novo(telemetria_mock, oxigenio=21.8)  # apos retirar 5 kg -> 16.8 kg = 5.0 dias
    g.solicitar_cota_extra("Joao", 5.0)
    telemetria_mock.disparar_alerta.assert_called_once_with(
        "CRITICO", "Autonomia de oxigenio critica: 5.0 dias"
    )


def test_verificar_estoque_saudavel_nao_alerta(gerenciador, telemetria_mock):
    assert gerenciador.verificar_estoque() is False
    telemetria_mock.disparar_alerta.assert_not_called()


def test_enviar_status_envia_relatorio(gerenciador, telemetria_mock):
    resposta = gerenciador.enviar_status()
    telemetria_mock.enviar_relatorio.assert_called_once_with(
        {"oxigenio_kg": 1000.0, "agua_l": 2000.0, "astronautas": 4}
    )
    assert resposta == {"status": "recebido"}


def test_resposta_simulada_da_terra_com_mocker_patch(mocker, gerenciador):
    mocker.patch.object(
        gerenciador.telemetria, "enviar_relatorio", return_value={"status": "ack-terra"}
    )
    assert gerenciador.enviar_status() == {"status": "ack-terra"}
