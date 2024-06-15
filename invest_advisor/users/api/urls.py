from django.urls import path

from invest_advisor.users.api.views import RegisterUserAPIView, UserAPIView

app_name = "users"

urlpatterns = [
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("self/", UserAPIView.as_view(), name="user-detail"),
]
