import json

from src.servico_telemetria import ServicoTelemetriaEspacial


def _resposta_fake(mocker, corpo):
    resp = mocker.MagicMock()
    resp.read.return_value = json.dumps(corpo).encode()
    resp.__enter__.return_value = resp
    return resp


def test_disparar_alerta_usa_rede_mockada(mocker):
    urlopen = mocker.patch(
        "src.servico_telemetria.urllib.request.urlopen",
        return_value=_resposta_fake(mocker, {"ok": True}),
    )
    r = ServicoTelemetriaEspacial("http://x").disparar_alerta("CRITICO", "teste")
    assert r == {"ok": True}
    req = urlopen.call_args.args[0]
    assert req.full_url == "http://x/alerta"
    assert json.loads(req.data) == {"nivel": "CRITICO", "mensagem": "teste"}


def test_enviar_relatorio_usa_rede_mockada(mocker):
    mocker.patch(
        "src.servico_telemetria.urllib.request.urlopen",
        return_value=_resposta_fake(mocker, {"ok": 1}),
    )
    assert ServicoTelemetriaEspacial("http://x").enviar_relatorio({"a": 1}) == {"ok": 1}
