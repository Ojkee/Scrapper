from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError

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

        links = options["links"] if len(options["links"]) else self._default_urls()
        n_links = len(links)

        for i, link in enumerate(links):
            self.stdout.write(f"Parsing {i + 1}/{n_links} ...")

            url = UrlParser(link).parse()
            if not url:
                self.stdout.write(self.style.ERROR(f"Invalid link: {link}"))
                continue

            self.stdout.write(f"Parsing link: {link}")
            self._print_data_url(url)

    def _print_data_url(self, url: str) -> None:
        req = Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            html_page = urlopen(req).read()
            page = BeautifulSoup(html_page, "html.parser")
        except URLError as e:
            self.stdout.write(
                self.style.ERROR(f"Link `{url}` does not exist: {e.reason}")
            )
            return
        self._print_title(page)
        self._print_date(page)

    def _print_title(self, page: BeautifulSoup) -> None:
        assert page.title and page.title.string
        self.stdout.write(self.style.SUCCESS("TITLE:"))
        self.stdout.write(page.title.string)

    def _print_date(self, page: BeautifulSoup) -> None:
        self.stdout.write(self.style.SUCCESS("DATE:"))
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
            tag = page.select_one(selector)
            if tag:
                if tag.has_attr("content"):
                    print(tag["content"])
                elif tag.has_attr("datetime"):
                    print(tag["datatime"])
                else:
                    print(tag.get_text(strip=True))
                break
        else:
            print("Not found")

    def _default_urls(self) -> list[str]:
        urls_file = settings.DATA_DIR / "urls.txt"
        if not urls_file.exists():
            self.stderr.write("FAIL")
            return []

        with urls_file.open("r", encoding="utf-8") as urls:
            return [line.strip() for line in urls.readlines()]
