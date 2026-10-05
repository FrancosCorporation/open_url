# MELHORIAS — open_url

> **Gerado por análise de código em 2026-10-05** · Stack: Python 3 + Selenium (Chrome WebDriver), sem requirements.txt
> Branch `main` · 1 arquivo de código (`openUrl.py`, ~21 linhas) · sem testes · sem CI
>
> **Este arquivo é um plano de execução.** Cada item tem ID, `arquivo:linha`, mudança exata,
> critério de aceite e comando de verificação.

---

## 0. Como usar este documento

1. Execute na ordem **P0 → P1 → P2 → P3**, respeitando as ondas da §8.
2. Ao terminar um item: marque `- [x]`, rode o **Verificação**, comite `fix(<ID>): descrição`.
3. **Atenção à finalidade:** este script automatiza visualizações de um vídeo do YouTube (abre N Chromes, dá play, dorme 601s, repete em loop). Qualquer robustez/escala passa antes pela decisão ética/legal da §9.
4. **Idioma:** português.

---

## 1. Diagnóstico executivo

Script Selenium de ~21 linhas: abre o Chrome anônimo, navega até vídeo fixo (`https://youtu.be/8rqgGZrsB7g`), clica play/mute/settings e dorme 10 min — dentro de `while(True)` que cria 10 drivers por iteração sem fechar os anteriores.

**O que está bem (não regredir):**

| Item | Evidência |
|---|---|
| Intenção legível em poucas linhas | `openUrl.py` inteiro tem ~21 linhas |
| `.gitignore` existe | `.gitignore` na raiz |

**O que está quebrado:**

1. **Não roda em ambiente atual** — usa `chrome_options=` e `find_element_by_xpath` (removidos no Selenium 4) e não tem `requirements.txt`.
2. **Vazamento de recursos:** `while(True)` + 10 Chromes por iteração, `quit()` só após `sleep(601)` dentro do `__init__`.
3. **Finalidade problemática:** automatizar views viola ToS do YouTube (ver §9).

---

## 2. Tabela de prioridades

| ID | Título | Sev | Arquivo | Depende de |
|---|---|---|---|---|
| BUG-01 | API Selenium 3 removida, script não executa | **P0** | `openUrl.py:6-15` | — |
| BUG-02 | Loop infinito abre Chromes sem fechar | **P0** | `openUrl.py:17-21` | BUG-01 |
| SEC-01 | Sem requirements.txt, dependência sem pin | **P1** | *(ausente)* `requirements.txt` | — |
| BUG-03 | driver local, quit() inalcançável em falha | **P1** | `openUrl.py:5-16` | BUG-01 |
| IMP-01 | URL hardcoded no código | **P2** | `openUrl.py:9` | — |
| TEST-01 | Zero testes | **P2** | *(ausente)* `test_*.py` | BUG-01 |
| DEVOPS-01 | Sem CI e sem lint | **P2** | *(ausente)* `.github/workflows/` | — |
| DOC-01 | README sem uso, pré-requisitos ou aviso de ToS | **P2** | `README.md` | — |

---

## 3. Segurança

### SEC-01 · Sem requirements.txt, dependência sem pin nem hash · [P1]

- **Arquivo:** *(ausente)* `requirements.txt`
- **Evidência:** único import externo é `from selenium import webdriver` (`openUrl.py:1`); nenhum `requirements.txt`, `pyproject.toml` ou pin no repo.
- **Impacto:** cada máquina instala "o Selenium que existir" — Selenium 3 (quando foi escrito) vs Selenium 4 (atual, que removeu as APIs usadas). Instalação irreproduzível, sem `pip audit`/Dependabot.
- **Mudança:** criar `requirements.txt` com `selenium==4.x.y` (versão testada após `BUG-01`).
- **Aceite:** `pip install -r requirements.txt` instala versão fixa e reproduzível.
- **Verificação:**
  ```bash
  cat requirements.txt
  ```
---

## 4. Bugs e defeitos funcionais

### BUG-01 · API Selenium 3 removida, script não executa · [P0]

- **Arquivo:** `openUrl.py:6-15`
- **Evidência:** três APIs inexistentes no Selenium 4: `webdriver.Chrome(chrome_options=options)` (linha 8, hoje é `options=`) e `find_element_by_xpath(...)` (linhas 10-15, método removido). Levantam `TypeError`/`AttributeError` antes de qualquer navegação.
- **Impacto:** o programa **não roda**. Toda outra melhoria depende desta.
- **Mudança:** migrar para Selenium 4: `webdriver.Chrome(options=options)` e `driver.find_element(By.XPATH, "...")` com `from selenium.webdriver.common.by import By`.
- **Aceite:** navegador abre e navega (ou falha por ambiente, não por API removida).
- **Verificação:**
  ```bash
  grep -n 'find_element_by_xpath\|chrome_options' openUrl.py || echo "APIs antigas removidas"
  ```

### BUG-02 · Loop infinito abre Chromes sem fechar · [P0]

- **Arquivo:** `openUrl.py:17-21`
- **Evidência:** `while(True)` cria 10 `driverCall()` por iteração; cada um dorme 601s dentro do `__init__` antes do `quit()`. O loop não espera: abre +10 processos por ciclo até esgotar RAM/CPU.
- **Impacto:** travamento da máquina por exaustão de recursos. Defeito operacional mais grave do arquivo.
- **Mudança:** remover o `while(True)` (ou iterações finitas via argumento); `try/finally` com `quit()` garantido; fechar o driver anterior antes de abrir o próximo. **Só após decisão da §9.**
- **Aceite:** N iterações deixam zero processos chrome/chromedriver órfãos.
- **Verificação:**
  ```bash
  timeout 60 python openUrl.py & sleep 65; pgrep -c chrome || echo "nenhum chrome orfao"
  ```

### BUG-03 · driver local, quit() inalcançável em falha · [P1]

- **Arquivo:** `openUrl.py:5-16`
- **Evidência:** `driver` é variável local do `__init__`, nunca em `self.driver`. Se qualquer `find_element_*` lançar (seletor mudou), o `quit()` da linha 17 nunca executa — Chrome zumbi mesmo sem o loop.
- **Impacto:** cada falha de seletor (comum no YouTube) deixa um Chrome órfão.
- **Mudança:** guardar `self.driver` e envolver o corpo em `try/finally: self.driver.quit()`.
- **Aceite:** exceção no meio do fluxo ainda fecha o navegador.
- **Verificação:**
  ```bash
  grep -n 'self.driver\|finally' openUrl.py
  ```

---

## 5. Qualidade: testes

### TEST-01 · Zero testes · [P2]

- **Arquivo:** *(ausente)* `test_*.py`
- **Evidência:** `find . -name 'test_*' -not -path './.git/*'` retorna vazio.
- **Impacto:** regressões de API do Selenium (exato `BUG-01`) passam despercebidas.
- **Mudança:** se continuar: smoke test que importa o módulo e valida as `ChromeOptions` sem abrir navegador (mock de `webdriver.Chrome`).
- **Aceite:** `pytest` executa ao menos 1 teste.
- **Verificação:**
  ```bash
  python -m pytest -q 2>&1 | tail -3
  ```

---

## 6. DevOps / Infra

### IMP-01 · URL hardcoded no código · [P2]

- **Arquivo:** `openUrl.py:9`
- **Evidência:** `driver.get('https://youtu.be/8rqgGZrsB7g')` fixo no código.
- **Impacto:** trocar de vídeo exige editar código; script não reutilizável.
- **Mudança:** ler de `sys.argv` ou `TARGET_URL`, validando esquema `https://` antes do `get`.
- **Aceite:** outra URL sem editar o arquivo.
- **Verificação:**
  ```bash
  grep -n 'sys.argv\|TARGET_URL' openUrl.py
  ```

### DEVOPS-01 · Sem CI e sem lint · [P2]

- **Arquivo:** *(ausente)* `.github/workflows/`
- **Evidência:** nenhum workflow; nenhum ruff/flake8 configurado.
- **Impacto:** `BUG-01` seria pego por `py_compile` + import em CI com Selenium novo.
- **Mudança:** workflow mínimo: `python -m py_compile openUrl.py` + `ruff check`.
- **Aceite:** push com erro de sintaxe/import bloqueado.
- **Verificação:**
  ```bash
  python -m py_compile openUrl.py && echo OK
  ```

---

## 7. Documentação

### DOC-01 · README sem uso, pré-requisitos ou aviso de ToS · [P2]

- **Arquivo:** `README.md`
- **Evidência:** README não lista Selenium, ChromeDriver, Python, execução — nem avisa sobre ToS do YouTube.
- **Impacto:** ninguém roda a partir do README; quem roda desconhece risco de bloqueio.
- **Mudança:** documentar pré-requisitos, comando e **aviso explícito** sobre automação de views vs ToS.
- **Aceite:** terceiro executa (ou decide não executar) com informação completa.
- **Verificação:**
  ```bash
  grep -ni 'selenium\|chromedriver\|termos\|ToS' README.md
  ```

---

## 8. Ordem de execução (waves)

### Wave 1 — Decisão de destino (antes de qualquer código)
1. **Ler §9** e decidir: arquivar ou continuar.

### Wave 2 — Fazer rodar (P0)
2. **`BUG-01`** — migrar para Selenium 4.
3. **`BUG-02`** — eliminar o loop vazador (mesmo teste manual).

### Wave 3 — Robustez (P1/P2)
4. **`SEC-01`** + **`BUG-03`** + **`IMP-01`** — pins, try/finally, URL parametrizável.
5. **`TEST-01`** + **`DEVOPS-01`** + **`DOC-01`** — teste, CI, README.

**Dependências que não podem ser invertidas:** `BUG-02` junto com `BUG-01` · `BUG-03` depois do `BUG-01`.

---

## 9. Fora de escopo / riscos

| Item | Decisão | Motivo |
|---|---|---|
| Escalar (mais instâncias, proxies, farm) | **Não, sem decisão do dono** | Automatizar views viola ToS do YouTube; escalar agrava risco de bloqueio e pode caracterizar fraude de métricas. |
| Trocar seletores XPath | **Só se continuar** | Seletores mudam sempre; custo contínuo sem valor se arquivar. |
| Migrar para Playwright/yt-dlp | **Não, aqui** | Troca de ferramenta não resolve finalidade + loop vazador. |

**Riscos desta execução:**

- **Finalidade:** decidir continuar (legítimo, documentado) ou arquivar antes de investir.
- **`BUG-02` pode travar a máquina de teste** — rodar com `timeout` e `pgrep chrome`.

---

## 10. Definição de pronto (DoD)

**Funcional**
- [ ] `BUG-01` — sem TypeError/AttributeError de API removida
- [ ] `BUG-02` — zero Chromes órfãos após N iterações
- [ ] `BUG-03` — exceção ainda fecha o navegador

**Segurança/qualidade**
- [ ] `SEC-01` — requirements.txt com versão fixa
- [ ] `IMP-01` — URL via argumento/env
- [ ] `TEST-01` — ao menos 1 teste executável
- [ ] `DEVOPS-01` — CI com py_compile + lint
- [ ] `DOC-01` — README com pré-requisitos e aviso de ToS

**Validação final:**
```bash
python -m py_compile openUrl.py && echo OK
grep -n 'find_element_by_xpath\|chrome_options' openUrl.py || echo "APIs antigas removidas"
cat requirements.txt
```

---

*Fim do plano. Gerado por leitura direta do código em 2026-10-05. Nenhum item já estava corrigido*
*— todos apontam para defeitos ainda presentes.*
