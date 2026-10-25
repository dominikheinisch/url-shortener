from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shortener import codecs
from shortener.models import ShortUrl
from shortener.serializers import ShortUrlCreateSerializer


class LimitReached(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Short URL limit reached."
    default_code = "limit_reached"


class ShortUrlCreateView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ShortUrlCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                short_url, created = ShortUrl.objects.get_or_create(
                    url=serializer.validated_data["url"]
                )
                code = short_url.code
        except codecs.ShortCodeLimitReached as e:
            raise LimitReached from e

        return Response(
            {"short_url": request.build_absolute_uri(reverse("shortener:resolve", args=[code]))},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class ShortUrlResolveView(APIView):
    def get(self, request: Request, code: str) -> Response:
        try:
            id_ = codecs.decode(code)
        except codecs.InvalidShortCode as e:
            raise NotFound from e

        short_url = get_object_or_404(ShortUrl, pk=id_)
        return Response({"url": short_url.url})
