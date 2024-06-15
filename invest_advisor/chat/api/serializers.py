from django.db.models import QuerySet
from rest_framework import serializers

from invest_advisor.chat.models import BuildingSubmission, TechnoparkSubmission


class ListTechnoparkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnoparkSubmission
        fields = ["id", "name"]


class TechnoparkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnoparkSubmission
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
        }

    def create(self, validated_data):
        if self.context["request"].user.is_authenticated:
            validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class OptionsSerializer(serializers.Serializer):
    option = serializers.CharField()

    def to_representation(self, instance):
        if isinstance(instance, tuple):
            return {"start": instance[0], "end": instance[1]}
        elif (
            isinstance(instance, list)
            or isinstance(instance, set)
            or isinstance(instance, QuerySet)
        ):
            return {"options": [option for option in instance]}
        return super().to_representation({"option": instance})


class BuildingSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingSubmission
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
        }

    def create(self, validated_data):
        if self.context["request"].user.is_authenticated:
            validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ListBuildingSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingSubmission
        fields = ["id", "name"]
