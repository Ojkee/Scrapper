from dataclasses import dataclass

from articles.models.article import Article


type ScrapResult = ScrapSuccess | ScrapError


@dataclass
class ScrapSuccess:
    article: Article


@dataclass
class ScrapError:
    msg: str
