from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import socket

from articles.scrapers.date_parser import DateParser
from articles.scrapers.title_parser import TitleParser
from articles.scrapers.url_parser import UrlParser


class Command(BaseCommand):
    help: str = "Scrap `title` from given url"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "links",
            nargs="*",
            type=str,
        )

    def handle(self, *args: tuple[Any, ...], **options: dict[str, Any]) -> None:
        _ = args

        links = options["links"] if len(options["links"]) else self._urls_from_file()
        n_links = len(links)

        for i, link in enumerate(links):
            self.stdout.write(f"\nParsing {i + 1}/{n_links} ...")

            url = UrlParser(link).parse()
            if not url:
                self.stdout.write(self.style.ERROR(f"Invalid link: {link}"))
                continue

            soup = self._soup_from_url(url)
            if not soup:
                continue

            title = TitleParser(soup).parse()
            print(f"Title: {title}")

            date = DateParser(soup).parse()
            print(f"Date: {date}")

    def _soup_from_url(self, url: str) -> Optional[BeautifulSoup]:
        try:
            req = Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
            html_page = urlopen(req).read()
            return BeautifulSoup(html_page, "html.parser")
        except HTTPError as e:
            self.stdout.write(self.style.ERROR(f"HTTP {e.code}: `{url}` {e.reason}"))
        except URLError as e:
            self.stdout.write(
                self.style.ERROR(f"Link `{url}` does not exist: `{e.reason}`")
            )
        except socket.error as e:
            self.stdout.write(self.style.ERROR(f"Timeout handling `{url}`: `{e}`"))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"ValueError: `{e}`"))

        return None

    def _urls_from_file(self) -> list[str]:
        urls_file = settings.DATA_DIR / "urls.txt"
        if not urls_file.exists():
            self.stderr.write("FAIL")
            return []

        with urls_file.open("r", encoding="utf-8") as urls:
            return [line.strip() for line in urls.readlines()]
