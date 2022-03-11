from django.urls import path, include

urlpatterns = [
    path("api/v1/", include(("app.api.urls", "app.api"), namespace="api")),
]
