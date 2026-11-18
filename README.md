[![Pipeline ECLSS](https://github.com/SEU_USUARIO/projeto-missao-marte/actions/workflows/pipeline.yml/badge.svg)](https://github.com/SEU_USUARIO/projeto-missao-marte/actions/workflows/pipeline.yml)

# Missão Marte: ECLSS – Automação de Testes

Suíte de testes do sistema de suporte à vida do Habitat de Marte: pytest (fixtures, parametrização, exceções), mocks (pytest-mock), Selenium headless, BDD (pytest-bdd) e CI com GitHub Actions.

## Executar localmente
```bash
git clone https://github.com/SEU_USUARIO/projeto-missao-marte.git
cd projeto-missao-marte
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
```
Requer Google Chrome instalado (o Selenium Manager baixa o chromedriver sozinho). A cobertura é exibida no console automaticamente (`pytest.ini`). Screenshots de falhas Selenium ficam em `tests/screenshots/`.

Veja `PASSO_A_PASSO.md` para a explicação completa.
