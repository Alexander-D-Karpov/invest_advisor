from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("users/", include("invest_advisor.users.api.urls", namespace="users")),
    path("chat/", include("invest_advisor.chat.api.urls", namespace="chat")),
]
