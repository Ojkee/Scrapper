from typing import Optional
from articles.models.article import Article


class ArticleService:
    @staticmethod
    def save(article: Article) -> None:
        article.save()

    @staticmethod
    def exists(link: str) -> Optional[bool]:
        return None
