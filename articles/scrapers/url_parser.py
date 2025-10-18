from django.core.validators import URLValidator
from typing import Optional
from bs4 import BeautifulSoup
from .base import SoupParser

type T = str


class UrlParser(SoupParser[T]):
    def __init__(self, url: str) -> None:
        super().__init__()
        self._url = url

    def parse(self) -> Optional[T]:
        return self._url if URLValidator(self._url) else None
