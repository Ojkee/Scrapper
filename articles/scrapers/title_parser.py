from typing import Optional
from bs4 import BeautifulSoup
from .base import SoupParser


type T = str


class TitleParser(SoupParser[T]):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__()
        self._soup = soup

    def parse(self) -> Optional[T]:
        if self._soup.title and self._soup.title.string:
            return self._soup.title.string
        return None
