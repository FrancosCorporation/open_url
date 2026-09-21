# open_url

## ℹ️ Sobre este repositório

Script utilitário para abrir URLs.

Automação de navegador com **Selenium**: abre uma URL no Chrome, executa
interações (play, mudo, seleção de qualidade) e mantém a janela ativa.

![Python](https://img.shields.io/badge/Python-3-3776AB?style=flat-square&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=selenium&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-estudo-lightgrey?style=flat-square)

## Sobre

**Projeto de estudo** de automação web com Selenium WebDriver. O script abre
um vídeo no YouTube em modo anônimo, clica nos controles do player (play,
mudo, configurações e qualidade) e mantém a reprodução minimizada por cerca
de 10 minutos. Serve como exercício de localização de elementos por XPath e
controle de janelas do navegador.

> Uso educacional. Respeite os termos de serviço dos sites que automatizar.

## Funcionalidades

Comprovadas pelo código em `openUrl.py`:

- Inicialização do Chrome via Selenium com opções (`--incognito`,
  `window-size=500,500`).
- Interações no player do YouTube por XPath: play/pause, mudo e seleção de
  qualidade.
- Loop que mantém instâncias do navegador ativas (`time.sleep(601)`).

## Como rodar

Requisitos: Python 3, Google Chrome e um driver compatível
(`chromedriver`), além do Selenium:

```bash
pip install selenium
python openUrl.py
```

> O `chromedriver.exe` e o `geckodriver.log` que estavam versionados foram
> removidos do repositório (binários específicos de plataforma). Baixe o
> driver correspondente à sua versão do Chrome em
> https://chromedriver.chromium.org/.

## Licença

MIT — veja [LICENSE](LICENSE).
