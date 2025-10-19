from typing import Optional
from articles.models.article import Article


class ArticleService:
    @staticmethod
    def save(article: Article) -> None:
        article.save()

    @staticmethod
    def exists(link: str) -> bool:
        return Article.objects.filter(url=link).exists()
