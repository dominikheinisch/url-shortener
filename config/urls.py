from django.urls import include, path

urlpatterns = [
    path("shrt/", include("shortener.urls")),
]
