from rest_framework import generics

from articles.models.article import Article
from articles.serializers import ArticleSerializer


class ArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()
        source = self.request.GET.get("source")
        if source:
            queryset = queryset.filter(url__icontains=source)
        return queryset


class ArticleDetail(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
