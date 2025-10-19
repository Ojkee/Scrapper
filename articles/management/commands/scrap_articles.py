from datetime import datetime
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings

# from playwright.sync_api import sync_playwright

from articles.scrapers import (
    url_to_soup,
    SoupSuccess,
    SoupFailure,
    ContentParser,
    DateParser,
    TitleParser,
    UrlParser,
)


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

        urls_file = settings.DATA_DIR / "urls.txt"
        links = (
            options["links"]
            if len(options["links"])
            else self._urls_from_file(urls_file)
        )
        n_links = len(links)

        for i, link in enumerate(links):
            self.stdout.write(f"\nParsing {i + 1}/{n_links} ...")

            url = UrlParser(link).parse()
            if not url:
                self.stdout.write(self.style.ERROR(f"Invalid link: {link}"))
                continue

            # Check if url in base

            match url_to_soup(url):
                case SoupFailure(msg=msg):
                    self.stdout.write(self.style.ERROR(msg))
                    continue
                case SoupSuccess(value=soup):
                    url
                    title = TitleParser(soup).parse()
                    date = DateParser(soup).parse()
                    date = date if date else datetime(0, 0, 0)
                    date_f = date.strftime("%d.%m.%Y %H:%M:%S")
                    content_parser = ContentParser(soup)
                    raw_content = content_parser.parse()
                    plain_content = content_parser.parse(clean=True)

    def _urls_from_file(self, urls_file) -> list[str]:
        if not urls_file.exists():
            self.stderr.write(self.style.ERROR("Fail loading default urls data file"))
            return []

        with urls_file.open("r", encoding="utf-8") as urls:
            return [line.strip() for line in urls.readlines()]
