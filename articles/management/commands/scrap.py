from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError


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

        for link in links:
            if self._valid_url(link):
                self.stdout.write(f"Parsing link: {link}")
                self._print_title_url(link)
            else:
                self.stdout.write(self.style.ERROR(f"Invalid link: {link}"))

    def _valid_url(self, url: str) -> bool:
        result = urlparse(url)
        return result.scheme != "" and result.netloc != ""

    def _print_title_url(self, url: str) -> None:
        req = Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            html_page = urlopen(req).read()
            soup = BeautifulSoup(html_page, "html.parser")
        except URLError as e:
            self.stdout.write(
                self.style.ERROR(f"Link `{url}` does not exist: {e.reason}")
            )
            return
        assert soup.title
        print(soup.title.string)

    def _default_urls(self) -> list[str]:
        urls_file = settings.DATA_DIR / "urls.txt"
        if not urls_file.exists():
            self.stderr.write("FAIL")
            return []

        with urls_file.open("r", encoding="utf-8") as urls:
            return [line.strip() for line in urls.readlines()]
