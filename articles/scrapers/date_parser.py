from __future__ import annotations
import dateparser
from dateutil.parser import ParserError, isoparse
from datetime import datetime
from typing import Callable, Optional

from bs4 import BeautifulSoup, element

from articles.scrapers.base import SoupParser

LANGUAGES: list[str] = ["en", "pl"]
DATE_ATTRS: list[str] = [
    "datetime",
    "title",
    "content",
    "data-time",
    "data-datetime",
]
DATE_SELECTORS = ", ".join(
    [
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
)

type T = datetime
type SeachDateFn = Callable[[BeautifulSoup], Optional[datetime]]


class DateParser(SoupParser[T]):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__()
        self._soup = soup
        self._seach_date_strategies: list[SeachDateFn] = [
            from_selectors,
            search_divs,
        ]

    def parse(self) -> Optional[T]:
        for search_date in self._seach_date_strategies:
            if date := search_date(self._soup):
                return date
        return None


def from_selectors(soup: BeautifulSoup) -> Optional[datetime]:
    tag = soup.select_one(DATE_SELECTORS)
    date_str = date_str_from_tag(tag)
    if not date_str:
        return None

    try:
        return isoparse(date_str)
    except (ValueError, ParserError):
        return dateparser.parse(date_str)


def date_str_from_tag(tag: Optional[element.Tag]) -> Optional[str]:
    if not tag:
        return None

    for attr in DATE_ATTRS:
        if tag.has_attr(attr):
            return str(tag[attr])
    return tag.get_text(strip=True)


def search_divs(soup: BeautifulSoup) -> Optional[datetime]:
    def dfs_seach(node: element.Tag) -> Optional[datetime]:
        for attr in DATE_ATTRS:
            if node.has_attr(attr):
                date = dateparser.parse(str(node[attr]), languages=["pl", "en"])
                if date:
                    return date
        if node.string:
            date = dateparser.parse(node.string, languages=LANGUAGES)
            if date:
                return date
        for child in node.children:
            if isinstance(child, element.Tag):
                date = dfs_seach(child)
                if date:
                    return date
        return None

    for tag in soup.find_all(["div", "p"]):
        if date := dfs_seach(tag):
            return date
    return None
