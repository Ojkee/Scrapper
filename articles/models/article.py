from django.db import models


class Article(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    raw_text = models.TextField()
    plain_text = models.TextField()
    publish_date = models.DateTimeField(blank=True, null=True)
