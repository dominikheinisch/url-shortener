from django.core.validators import URLValidator
from rest_framework import serializers


class ShortUrlCreateSerializer(serializers.Serializer[dict[str, str]]):
    url = serializers.URLField(
        max_length=2048,
        validators=[URLValidator(schemes=["http", "https"])],
    )
