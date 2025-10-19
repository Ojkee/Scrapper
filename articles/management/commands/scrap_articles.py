from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings

# from playwright.sync_api import sync_playwright

from articles.scrapers import ArticleScraper, ScrapError, ScrapSuccess
from articles.services import ArticleService


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

        for i, link in enumerate(links, start=1):
            self.stdout.write(f"\nParsing {i}/{n_links} ...")
            if ArticleService.exists(link):
                self.stdout.write(f"Cached: {link}")
                continue

            match ArticleScraper.parse(link):
                case ScrapError(msg=msg):
                    self.stdout.write(self.style.ERROR(msg))
                case ScrapSuccess(article=article):
                    self.stdout.write(
                        self.style.SUCCESS(f"Saved {link}:\n\t{article.title}")
                    )
                    ArticleService.save(article)

    def _urls_from_file(self, urls_file) -> list[str]:
        if not urls_file.exists():
            self.stderr.write(self.style.ERROR("Fail loading default urls data file"))
            return []

        with urls_file.open("r", encoding="utf-8") as urls:
            return [line.strip() for line in urls.readlines()]
