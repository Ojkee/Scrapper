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
    try:
        req = Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
        raw = urlopen(req, timeout=10).read()
    except HTTPError as e:
        return SoupFailure(f"HTTP {e.code}: `{url}` {e.reason}")
    except URLError as e:
        return SoupFailure(f"Link `{url}` does not exist: `{e.reason}`")
    except socket.error as e:
        return SoupFailure(f"Timeout handling `{url}`: `{e}`")
    except ValueError as e:
        return SoupFailure(f"ValueError: `{e}`")

    html = raw.decode("utf-8")
    return SoupSuccess(BeautifulSoup(html, "html.parser"))
