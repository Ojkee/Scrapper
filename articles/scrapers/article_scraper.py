from datetime import datetime
from articles.models.article import Article

from .url_parser import UrlParser
from .title_parser import TitleParser
from .date_parser import DateParser
from .content_parser import ContentParser

from .util import url_to_soup, SoupSuccess, SoupFailure
from .status import ScrapResult, ScrapSuccess, ScrapError


class ArticleScraper:
    @staticmethod
    def parse(link: str) -> ScrapResult:

        url = UrlParser(link).parse()
        if not url:
            return ScrapError(f"Invalid link: {link}")

        match url_to_soup(url):
            case SoupFailure(msg=msg):
                return ScrapError(msg)
            case SoupSuccess(value=soup):
                title = TitleParser(soup).parse()
                date = DateParser(soup).parse()
                publish_date = date if date else datetime(1, 1, 1)
                content_parser = ContentParser(soup)
                raw_content = content_parser.parse()
                plain_content = content_parser.parse(clean=True)
                artile = Article(
                    url=url,
                    title=title,
                    raw_text=raw_content,
                    plain_text=plain_content,
                    publish_date=publish_date,
                )
                return ScrapSuccess(artile)
