from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from invest_advisor.chat.api.serializers import (
    BuildingSubmissionSerializer,
    ListBuildingSubmissionSerializer,
    ListTechnoparkSubmissionSerializer,
    OptionsSerializer,
    TechnoparkSubmissionSerializer,
)
from invest_advisor.chat.models import BuildingSubmission, TechnoparkSubmission
from invest_advisor.chat.services import (
    filter_buildings,
    filter_technoparks,
    get_options_for_building_question,
    get_options_for_technopark_question,
)


class ListCreateTechnoparkSubmissionAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ListTechnoparkSubmissionSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListTechnoparkSubmissionSerializer
        return TechnoparkSubmissionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return TechnoparkSubmission.objects.filter(user=self.request.user)
        return TechnoparkSubmission.objects.none()

    @extend_schema(
        request=None, responses={200: ListTechnoparkSubmissionSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        request=TechnoparkSubmissionSerializer,
        responses={200: TechnoparkSubmissionSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RetrieveUpdateDestroyTechnoparkSubmissionAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [permissions.AllowAny]
    serializer_class = TechnoparkSubmissionSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    queryset = TechnoparkSubmission.objects.all()


class TechnoparkOptionsAPIView(generics.GenericAPIView):
    serializer_class = OptionsSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        submission = get_object_or_404(TechnoparkSubmission, id=self.kwargs["id"])
        try:
            question_id = int(self.kwargs["question"])
        except ValueError:
            return Response(
                {"error": "Question ID must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        options = get_options_for_technopark_question(
            question_id, filter_technoparks(submission)
        )
        serializer = self.get_serializer(options)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BuildingOptionsAPIView(generics.GenericAPIView):
    serializer_class = OptionsSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        submission = get_object_or_404(BuildingSubmission, id=self.kwargs["id"])
        try:
            question_id = int(self.kwargs["question"])
        except ValueError:
            return Response(
                {"error": "Question ID must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        options, next_question = get_options_for_building_question(
            question_id, filter_buildings(submission), submission
        )
        serializer = self.get_serializer(options)
        return Response(
            {**serializer.data, "next_question": next_question},
            status=status.HTTP_200_OK,
        )


class ListCreateBuildingSubmissionAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BuildingSubmissionSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListBuildingSubmissionSerializer
        return BuildingSubmissionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return BuildingSubmission.objects.filter(user=self.request.user)
        return BuildingSubmission.objects.none()

    @extend_schema(
        request=None, responses={200: ListBuildingSubmissionSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        request=BuildingSubmissionSerializer,
        responses={200: BuildingSubmissionSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RetrieveUpdateDestroyBuildingSubmissionAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [permissions.AllowAny]
    serializer_class = BuildingSubmissionSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    queryset = BuildingSubmission.objects.all()
