from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shortener import codecs
from shortener.serializers import ShortUrlCreateSerializer

acc = 1


class ShortUrlCreateView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ShortUrlCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        global acc
        code = acc
        acc += 1

        return Response(
            {"short_url": f"/shrt/{codecs.encode(code)}"},
            status=status.HTTP_201_CREATED,
        )
