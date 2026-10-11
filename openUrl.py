"""Open one HTTP(S) URL in an interactive Chrome window."""

from __future__ import annotations

import argparse
import sys
from urllib.parse import urlsplit

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def http_url(value: str) -> str:
    """Validate an HTTP(S) URL before passing it to the browser."""
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        _ = parsed.port  # Accessing port validates its numeric range and format.
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"URL inválida: {exc}") from exc

    if parsed.scheme not in {"http", "https"} or not hostname:
        raise argparse.ArgumentTypeError(
            "Informe uma URL completa começando com http:// ou https://."
        )
    if parsed.username is not None or parsed.password is not None:
        raise argparse.ArgumentTypeError(
            "Não inclua usuário ou senha na URL."
        )
    return value


def open_url(url: str) -> None:
    """Open a single page and always close the WebDriver session."""
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--window-size=500,500")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        try:
            input("Página aberta. Pressione Enter para fechar o navegador... ")
        except EOFError:
            # Non-interactive invocations should still release Chrome cleanly.
            pass
    finally:
        if driver is not None:
            driver.quit()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Abre uma URL HTTP(S) em uma única janela do Chrome."
    )
    parser.add_argument("url", type=http_url, help="endereço da página")
    args = parser.parse_args(argv)

    try:
        open_url(args.url)
    except KeyboardInterrupt:
        print("\nExecução interrompida.", file=sys.stderr)
        return 130
    except WebDriverException as exc:
        print(f"Não foi possível iniciar ou controlar o Chrome: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
