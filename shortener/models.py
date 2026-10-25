from django.db import models

from shortener import codecs


class ShortUrl(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField(max_length=2048, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.code} -> {self.url}"

    @property
    def code(self) -> str:
        return codecs.encode(self.id)
