from rest_framework import serializers
from .models import Report, ReportImage, PetAdoptionModel



class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ReportImageSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(write_only=True)

    class Meta:
        model = ReportImage
        fields = ['picture', 'report_id', 'created_at']


class PetAdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetAdoptionModel
        fields = '__all__'


class AdoptDetailSerializer(serializers.ModelSerializer):  # Endpoint para detalle de adopciones
    class Meta:
        model = PetAdoptionModel
        fields = ['title', 'name', 'description', 'specie', 'age', 'sex', 'city', 'country', 'phone', 'picture']
