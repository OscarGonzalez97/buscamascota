from rest_framework import serializers

from app.models import Report, PetAdoptionModel


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class AdoptSerializer(serializers.ModelSerializer):
    class Beta:
        model = PetAdoptionModel
        fields = "__all__"
