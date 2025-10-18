from typing import Optional
from bs4 import BeautifulSoup
from .base import SoupParser

type T = str


class ContentParser(SoupParser[T]):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__()
        self._soup = soup

    def parse(self, soup) -> Optional[T]:
        return super().parse(soup)
