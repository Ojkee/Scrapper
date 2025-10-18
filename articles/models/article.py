from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=256)
    raw_text = models.TextField()
    plain_text = models.TextField()
    url = models.URLField(unique=True)
    publish_date = models.DateTimeField(auto_now_add=True)
