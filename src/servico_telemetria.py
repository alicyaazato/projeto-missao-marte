"""Servico de telemetria: comunicacao (de rede) com a estacao na Terra."""
import json
import urllib.request

URL_ESTACAO_TERRA = "https://estacao-terra.exemplo.invalid/api"


class ServicoTelemetriaEspacial:
    """Dependencia externa. Nos testes unitarios ela e SEMPRE substituida por um mock."""

    def __init__(self, url=URL_ESTACAO_TERRA, timeout=5):
        self.url = url
        self.timeout = timeout

    def _post(self, caminho, payload):
        req = urllib.request.Request(
            f"{self.url}/{caminho}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def enviar_relatorio(self, status):
        """Envia o relatorio de status do habitat para a Terra."""
        return self._post("relatorio", {"status": status})

    def disparar_alerta(self, nivel, mensagem):
        """Dispara um alerta de crise para a Terra."""
        return self._post("alerta", {"nivel": nivel, "mensagem": mensagem})
