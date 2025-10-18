from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup

from articles.scrapers.base import SoupParser

type T = datetime


class DateParser(SoupParser[T]):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__()
        self._soup = soup

    def parse(self) -> Optional[T]:
        raise NotImplementedError("DateParser.parse not implemented")
