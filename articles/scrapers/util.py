from dataclasses import dataclass
import socket
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

type SoupResult = SoupSuccess | SoupFailure


@dataclass
class SoupSuccess:
    value: BeautifulSoup


@dataclass
class SoupFailure:
    msg: str


def url_to_soup(url: str) -> SoupResult:
    page = read_page_form_url(url)
    if isinstance(page, SoupFailure):
        return page

    return soup_from_page(page)


def read_page_form_url(url: str) -> str | SoupFailure:
    try:
        req = Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
        raw = urlopen(req).read()
        html = raw.decode("utf-8")
        return html
    except HTTPError as e:
        return SoupFailure(f"HTTP {e.code}: `{url}` {e.reason}")
    except URLError as e:
        return SoupFailure(f"Link `{url}` does not exist: `{e.reason}`")
    except socket.error as e:
        return SoupFailure(f"Timeout handling `{url}`: `{e}`")
    except ValueError as e:
        return SoupFailure(f"ValueError: `{e}`")


def soup_from_page(html_page: str) -> SoupResult:
    # if not is_js_rendered(html_page):
    return SoupSuccess(BeautifulSoup(html_page, "html.parser"))
    return SoupFailure("not implemented")


def is_js_rendered(html_page: str) -> bool:
    indicators = [
        'id="__NEXT_DATA__"',
        "self.__next_f",
        "data-reactroot",
        'id="root"',
        "Hydration error",
    ]
    return any(ind in html_page for ind in indicators)
