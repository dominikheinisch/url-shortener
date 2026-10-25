from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shortener import codecs
from shortener.serializers import ShortUrlCreateSerializer

urls: dict[int, str] = {}


class ShortUrlCreateView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ShortUrlCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_ = len(urls) + 1
        urls[id_] = serializer.validated_data["url"]
        code = codecs.encode(id_)

        return Response(
            {"short_url": request.build_absolute_uri(reverse("shortener:resolve", args=[code]))},
            status=status.HTTP_201_CREATED,
        )


class ShortUrlResolveView(APIView):
    def get(self, request: Request, code: str) -> Response:
        try:
            id_ = codecs.decode(code)
        except codecs.InvalidShortCode as e:
            raise NotFound from e

        if id_ not in urls:
            raise NotFound
        return Response({"url": urls[id_]})
