from django.urls import path

from shortener import views

app_name = "shortener"

urlpatterns = [
    path("", views.ShortUrlCreateView.as_view(), name="create"),
    path("<str:code>", views.ShortUrlResolveView.as_view(), name="resolve"),
]
