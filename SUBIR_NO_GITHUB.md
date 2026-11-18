# Manual: subir o projeto AST13 no GitHub

Objetivo: ter um repositório **público** com o código na raiz e o workflow do GitHub Actions **verde**.

## 0. Pré-requisitos
- Conta no GitHub (https://github.com).
- Git instalado: no terminal rode `git --version`. Se não existir, instale em https://git-scm.com/download/win.
- Configure seu nome/e-mail uma única vez (se ainda não fez):
  ```bash
  git config --global user.name "Seu Nome"
  git config --global user.email "seu-email@exemplo.com"
  ```

## 1. Criar o repositório no GitHub
1. Acesse https://github.com/new
2. **Repository name:** `projeto-missao-marte`
3. Marque **Public**.
4. **NÃO** marque "Add a README", ".gitignore" nem "license" (o repositório precisa nascer vazio).
5. Clique em **Create repository** e copie a URL, algo como
   `https://github.com/SEU_USUARIO/projeto-missao-marte.git`

## 2. Ajustar a badge do README
Abra `AST13/README.md` e troque `SEU_USUARIO` pelo seu usuário do GitHub (2 ocorrências na primeira linha).
Se usou outro nome de repositório, troque também `projeto-missao-marte`.

## 3. Importante: criar um repositório Git NOVO só para a AST13
A pasta `AST04` já é um repositório git, então **não rode `git init` dentro de uma pasta que já está dentro de outro repo sem perceber**. O `git init` dentro de `AST13` cria um repo independente (é o que queremos). Confirme depois com `git rev-parse --show-toplevel`: deve mostrar o caminho da pasta `AST13`.

## 4. Comandos (PowerShell ou Git Bash)
```bash
cd "C:\Users\diova\OneDrive\Desktop\atividades\AST04\AST13"

git init
git branch -M main
git add .
git status          # confira: deve listar .github/, src/, tests/, web/, README.md, requirements.txt, pytest.ini...
git commit -m "Suite de testes ECLSS (pytest, mocks, selenium, bdd, CI)"

git remote add origin https://github.com/SEU_USUARIO/projeto-missao-marte.git
git push -u origin main
```

### Autenticação no push
O GitHub não aceita mais senha. Na primeira vez o Git for Windows abre uma janela do navegador para você entrar na conta: faça login e autorize. Se pedir senha no terminal, use um **Personal Access Token**:
GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate → marque o escopo `repo` → use o token no lugar da senha.

## 5. Conferir o CI (obrigatório estar verde)
1. No repositório, abra a aba **Actions**.
2. O workflow **Pipeline ECLSS** deve rodar sozinho após o push (leva 1–3 min).
3. Clique na execução e verifique o log do passo "Executar suite com cobertura": devem aparecer os testes passando e a tabela de cobertura.
4. Status verde (✔) = pronto. Atualize a página inicial do repositório: a badge do README mostra **passing**.

Se o Actions não aparecer: confirme que a pasta `.github/workflows/pipeline.yml` está na **raiz** do repositório (e não dentro de uma subpasta `AST13/`). Em Settings → Actions → General, verifique se as Actions estão habilitadas.

## 6. Se algo falhar
| Problema | Solução |
|---|---|
| `remote origin already exists` | `git remote set-url origin <URL>` |
| `failed to push ... rejected` (repo criado com README) | `git pull origin main --allow-unrelated-histories` e `git push` |
| Workflow vermelho por Selenium | Abra o log; o runner `ubuntu-latest` já vem com Chrome. Se falhar, baixe o artefato `screenshots` na página da execução |
| Badge cinza "no status" | Usuário/repo errados na URL da badge, ou o workflow ainda não rodou |
| Mudou algo e quer reenviar | `git add . && git commit -m "ajuste" && git push` (o CI roda de novo) |

## 7. Entrega
Envie na atividade a URL do repositório: `https://github.com/SEU_USUARIO/projeto-missao-marte`
Antes de enviar, abra-a em uma janela anônima para confirmar que está pública e com a badge verde.
