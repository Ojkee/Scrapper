from datetime import datetime
from typing import Any, Optional
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings

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

            match url_to_soup(url):
                case SoupFailure(msg=msg):
                    self.stdout.write(self.style.ERROR(msg))
                    continue
                case SoupSuccess(value=soup):
                    title = TitleParser(soup).parse()
                    print(f"Title: {title}")

                    date = DateParser(soup).parse()
                    date = date if date else datetime(0, 0, 0)
                    date_f = date.strftime("%d.%m.%Y %H:%M:%S")
                    print(f"Date: {date_f}")

                    content_parser = ContentParser(soup)
                    raw_content = content_parser.parse()
                    raw_content_str = raw_content if raw_content else None
                    # print(f"Raw Content: {raw_content_str}")

                    plain_content = content_parser.parse(clean=True)
                    plain_content_str = plain_content if plain_content else None
                    print(f"Plain Content: {plain_content_str}")

    def _urls_from_file(self, urls_file) -> list[str]:
        if not urls_file.exists():
            self.stderr.write(self.style.ERROR("Fail loading default urls data file"))
            return []

        with urls_file.open("r", encoding="utf-8") as urls:
            return [line.strip() for line in urls.readlines()]
