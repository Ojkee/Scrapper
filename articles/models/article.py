from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    raw_text = models.TextField()
    plain_text = models.TextField()
    url = models.URLField(unique=True)
    publish_date = models.DateTimeField(blank=True, null=True)
