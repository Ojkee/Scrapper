from dateutil.parser import isoparse
from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup, element

from articles.scrapers.base import SoupParser

type T = datetime


class DateParser(SoupParser[T]):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__()
        self._soup = soup

    def parse(self) -> Optional[T]:
        return self._from_selectors()

    def _from_selectors(self) -> Optional[datetime]:
        selectors = [
            'meta[property="article:published_time"]',
            'meta[name="pubdate"]',
            'meta[name="date"]',
            'meta[name="DC.date.issued"]',
            'meta[itemprop="datePublished"]',
            "time",
            ".date",
            ".published",
            ".post-date",
            "[datetime]",
        ]
        for selector in selectors:
            tag = self._soup.select_one(selector)
            date_str = self._date_str_from_tag(tag)
            if date_str:
                return isoparse(date_str)
        return None

    def _date_str_from_tag(self, tag: Optional[element.Tag]) -> Optional[str]:
        if not tag:
            return None

        attrs = ["content", "datetime"]
        for attr in attrs:
            if tag.has_attr(attr):
                return str(tag[attr])
        return tag.get_text(strip=True)
