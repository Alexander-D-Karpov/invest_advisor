from django.urls import path

from invest_advisor.chat.api.views import (
    BuildingOptionsAPIView,
    ListCreateBuildingSubmissionAPIView,
    ListCreateTechnoparkSubmissionAPIView,
    RetrieveUpdateDestroyBuildingSubmissionAPIView,
    RetrieveUpdateDestroyTechnoparkSubmissionAPIView,
    TechnoparkOptionsAPIView,
    SubmitTechnoparkSubmissionAPIView,
    ListChatAPIView,
    ListCreateChatMessageAPIView,
    SubmitBuildingSubmissionAPIView, RequestFileAPIView,
)

app_name = "chat"

urlpatterns = [
    path("", ListChatAPIView.as_view(), name="chat"),
    path(
        "<str:id>/messages/",
        ListCreateChatMessageAPIView.as_view(),
        name="chat-messages",
    ),
    path(
        "<str:id>/report/",
        RequestFileAPIView.as_view(),
        name="chat-report",
    ),
    path(
        "technopark/",
        ListCreateTechnoparkSubmissionAPIView.as_view(),
        name="technopark",
    ),
    path(
        "technopark/<str:id>",
        RetrieveUpdateDestroyTechnoparkSubmissionAPIView.as_view(),
        name="technopark-detail",
    ),
    path(
        "technopark/<str:id>/submit/",
        SubmitTechnoparkSubmissionAPIView.as_view(),
        name="technopark-detail",
    ),
    path(
        "technopark/<str:id>/question/<int:question>/options/",
        TechnoparkOptionsAPIView.as_view(),
        name="technopark-options",
    ),
    path(
        "building/",
        ListCreateBuildingSubmissionAPIView.as_view(),
        name="building",
    ),
    path(
        "building/<str:id>",
        RetrieveUpdateDestroyBuildingSubmissionAPIView.as_view(),
        name="building-detail",
    ),
    path(
        "building/<str:id>/question/<int:question>/options/",
        BuildingOptionsAPIView.as_view(),
        name="building-options",
    ),
    path(
        "building/<str:id>/submit/",
        SubmitBuildingSubmissionAPIView.as_view(),
        name="building-detail",
    ),
]
