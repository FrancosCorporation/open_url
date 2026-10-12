# open_url

Pequeno utilitário de estudo para abrir uma página HTTP(S) em uma única janela do Chrome usando Selenium.

## Requisitos

- Python 3.10 ou superior
- Google Chrome instalado
- Acesso à internet na primeira execução para o Selenium Manager localizar o driver compatível

O Selenium Manager acompanha a dependência e administra o driver quando ele não está instalado no `PATH`; não é necessário baixar `chromedriver` manualmente. Consulte a [documentação do Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/).

## Instalação e uso

```bash
python3 -m venv .venv
source .venv/bin/activate  # PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python openUrl.py https://example.com
```

O navegador permanece aberto até você pressionar Enter no terminal. `Ctrl+C` também encerra a execução. O programa fecha a sessão do WebDriver ao terminar ou quando ocorre uma exceção.

## Uso responsável

O script apenas abre a página indicada. Ele não clica em controles, não inicia reprodução e não repete sessões para gerar visualizações ou engajamento artificial. Respeite os termos de serviço e as regras dos sites acessados.

## Verificações estáticas

O workflow do GitHub Actions compila o arquivo e executa Ruff em Python 3.10 e 3.12, cobrindo a faixa mínima documentada. Não há testes automatizados de navegador neste repositório.

## Licença

MIT — veja [LICENSE](LICENSE).
