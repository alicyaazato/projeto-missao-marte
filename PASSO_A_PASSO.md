# Explicação e passo a passo – AST13 (Missão Marte: ECLSS)

## 1. Estrutura
```
.github/workflows/pipeline.yml   CI (Requisito 5)
src/gerenciador_recursos.py      regras de negócio + exceções customizadas
src/servico_telemetria.py        dependência externa (rede) -> sempre mockada
web/painel.html                  painel web com formulário de cota extra
tests/conftest.py                fixtures + hook de evidência
tests/test_gerenciador.py        Req. 1 e 2
tests/test_servico_telemetria.py cobre o serviço de rede com urlopen mockado
tests/test_selenium_e2e.py       Req. 3
tests/test_bdd.py + features/    Req. 4
pytest.ini  requirements.txt  README.md
```

## 2. Como cada requisito foi atendido
**Req. 1 – Pytest**
- `parametros_habitat` (scope=session, em `conftest.py`) = fixture global com os parâmetros iniciais.
- `gerenciador` (scope=function) cria uma instância limpa por teste e usa `yield` para o teardown.
- `@pytest.mark.parametrize` em consumo de O₂/água, taxas de emergência e cotas (astronautas × nível).
- `pytest.raises` para `OxigenioInsuficienteError`, `NivelEmergenciaInvalidoError`, `CotaExcedidaError` e `ValueError`.

**Req. 2 – Mocks**
- `telemetria_mock` usa `mocker.create_autospec(ServicoTelemetriaEspacial)`: nenhuma chamada de rede acontece; o autospec ainda garante que só métodos/assinaturas reais sejam usados.
- `assert_called_once_with("CRITICO", "Autonomia de oxigenio critica: 5.0 dias")` valida o alerta de crise; `assert_not_called()` valida o caso normal; `mocker.patch.object` simula resposta da Terra.

**Req. 3 – Selenium**
- Fixture `driver`: Chrome `--headless=new`, `driver.quit()` no teardown.
- O `painel.html` responde após 600 ms (setTimeout); os testes usam `WebDriverWait` + `expected_conditions` (nunca `time.sleep`).
- Evidência: o hook `pytest_runtest_makereport` (conftest) anexa o resultado ao teste; se falhou, a fixture chama `driver.save_screenshot()` antes do `quit()`. No CI as imagens são enviadas como artefato.

**Req. 4 – BDD**
- `solicitacao_oxigenio.feature` (Gherkin em português, `# language: pt`) com 3 cenários: normal, crise e acima da cota.
- `test_bdd.py` mapeia com `@given`, `@when`, `@then` e `parsers.parse`; `scenarios(...)` liga o arquivo.

**Req. 5 – CI**
- Dispara em `push` e `pull_request`; `actions/checkout@v4`, `actions/setup-python@v5`, `pip install -r requirements.txt`, `pytest -v`.
- A cobertura (`--cov=src --cov-report=term-missing`) está no `pytest.ini`, portanto aparece no log. O runner `ubuntu-latest` já tem Chrome.

## 3. Resultado local
39 testes passando, 100% de cobertura de `src/`.

## 4. O que VOCÊ precisa fazer para entregar (passo a passo)
1. Crie um repositório **público** no GitHub (ex.: `projeto-missao-marte`).
2. Copie o conteúdo da pasta `AST13` para a raiz desse repositório (a pasta `.github` precisa ficar na raiz).
3. Em `README.md`, troque `SEU_USUARIO` (e o nome do repo, se mudar) na badge.
4. Envie:
   ```bash
   git init && git add . && git commit -m "Suite de testes ECLSS"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/projeto-missao-marte.git
   git push -u origin main
   ```
5. Abra a aba **Actions** do repositório e confirme que o workflow ficou verde; a badge no README passará a mostrar "passing".
6. Entregue a URL do repositório.

Observação: a AST13 deve ir para um repositório próprio (não dentro do repo `AST04`/`AST12`, que já têm outros `.git`), senão o GitHub Actions não encontrará `.github/workflows` na raiz.
