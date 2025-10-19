from rest_framework import serializers
from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    publish_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required=False)  # type: ignore

    class Meta:
        model = Article
        fields = "__all__"
