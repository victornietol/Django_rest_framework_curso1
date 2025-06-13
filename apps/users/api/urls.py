from django.urls import path
from apps.users.api.api import UserAPIView, user_api_view, user_detail_api_view

urlpatterns = [
    path("usuario/", UserAPIView.as_view(), name="usuario_api"),
    path("usuario_v2/", user_api_view, name="usuario_api"),
    path("usuario/<int:pk>/", user_detail_api_view, name="usuario_api"),
]